import asyncio
import os
from time import perf_counter
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.errors import AppError
from app.core.limits import provider_budget
from app.core.security import current_user, worker
from app.core.telemetry import stage_event
from app.db.models import Intake, Order, User
from app.db.session import get_db
from app.integrations.gnani import GnaniError, GnaniSpeechClient
from app.integrations.tts import provider_slots
from app.schemas.commands import ManualIntake, Review
from app.schemas.responses import IntakeResponse
from app.services.audio import MAX_BYTES, normalize_audio
from app.services.extraction import extract
from app.services.orders import intake_json

router = APIRouter(prefix="/api/v1/intakes")
DB = Annotated[Session, Depends(get_db)]
Worker = Annotated[User, Depends(worker)]
Current = Annotated[User, Depends(current_user)]
speech = GnaniSpeechClient(os.getenv("GNANI_API_KEY_ID", ""))
slots = provider_slots


@router.post("/transcribe", status_code=201, response_model=IntakeResponse)
async def transcribe(
    request: Request,
    user: Worker,
    db: DB,
    audio_file: Annotated[UploadFile, File()],
    language_code: Annotated[str, Form()] = "hi-IN",
) -> dict[str, Any]:
    if language_code not in {"hi-IN", "en-IN", "ta-IN"}:
        raise AppError(422, "INVALID_LANGUAGE", "Select Hindi, English or Tamil.")
    try:
        data = await audio_file.read(MAX_BYTES + 1)
    finally:
        await audio_file.close()
    if len(data) > MAX_BYTES:
        raise AppError(413, "AUDIO_TOO_LARGE", "Audio must be under 10 MiB.")
    started = perf_counter()
    try:
        normalized, duration = await run_in_threadpool(normalize_audio, data)
    except AppError as exc:
        stage_event(request.state.request_id, "audio_normalize", started, code=exc.code)
        raise
    stage_event(request.state.request_id, "audio_normalize", started)
    provider_budget.check(user.id)
    row = Intake(
        reporter_id=user.id,
        language_code=language_code,
        audio_duration_seconds=duration,
        status="TRANSCRIBING",
    )
    db.add(row)
    db.commit()
    try:
        started = perf_counter()
        async with asyncio.timeout(90):
            async with slots:
                result = await speech.transcribe(
                    normalized, language_code, request.state.request_id
                )
        stage_event(
            request.state.request_id,
            "provider_stt",
            started,
            model=result.model,
            provider_request_id=result.request_id,
        )
        # Compute suggestions before mutating the intake: catalog queries can autoflush.
        started = perf_counter()
        extraction = extract(result.transcript, db)
        stage_event(request.state.request_id, "extraction", started)
        row.raw_transcript = result.transcript
        row.provider_model = result.model
        row.provider_request_id = result.request_id
        row.stt_latency_ms = round(result.elapsed_seconds * 1000)
        row.extraction = extraction
        row.status = "READY_FOR_REVIEW"
        db.commit()
    except (GnaniError, TimeoutError) as exc:
        code = exc.code if isinstance(exc, GnaniError) else "GNANI_TIMEOUT"
        stage_event(request.state.request_id, "provider_stt", started, code=code)
        row.status = "FAILED"
        row.error_code = code
        db.commit()
        status = 422 if code == "NO_SPEECH_DETECTED" else 503
        messages = {
            "NO_SPEECH_DETECTED": "No speech was heard. Record a clear report and try again.",
            "GNANI_AUTH_FAILURE": (
                "Speech recognition needs operator attention. Type your report or contact the team."
            ),
            "GNANI_QUOTA_EXHAUSTED": (
                "Speech credits are exhausted. Type your report or contact the team."
            ),
            "GNANI_RATE_LIMITED": (
                "Speech recognition is busy. Wait before retrying, or type your report."
            ),
            "GNANI_TIMEOUT": (
                "Speech timed out. No order was created. Retry once or type your report."
            ),
            "GNANI_INVALID_REQUEST": (
                "Speech recognition could not accept this clip. Rerecord or type your report."
            ),
        }
        raise AppError(
            status,
            code,
            messages.get(
                code,
                "Speech recognition is unavailable. No order was created. "
                "Retry later or type your report.",
            ),
        ) from None
    output = intake_json(row)
    asset = row.extraction.get("suggested_fields", {}).get("asset_id")
    # Never disclose another reporter's private report in duplicate hints.
    output["possible_duplicates"] = (
        len(
            list(
                db.scalars(
                    select(Order.id)
                    .where(
                        Order.asset_id == asset,
                        Order.reporter_id == user.id,
                        Order.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
                    )
                    .limit(10)
                )
            )
        )
        if asset
        else 0
    )
    return output


@router.post("/manual", status_code=201, response_model=IntakeResponse)
def manual(body: ManualIntake, user: Worker, db: DB) -> dict[str, Any]:
    row = Intake(
        reporter_id=user.id,
        source_type="MANUAL_TEXT",
        status="READY_FOR_REVIEW",
        language_code=body.language_code,
        raw_transcript=body.text,
        extraction=extract(body.text, db),
    )
    db.add(row)
    db.commit()
    return intake_json(row)


@router.get("/{iid}", response_model=IntakeResponse)
def detail(iid: str, user: Current, db: DB) -> dict[str, Any]:
    row = db.get(Intake, iid)
    if not row or (row.reporter_id != user.id and user.role != "SUPERVISOR"):
        raise AppError(404, "NOT_FOUND", "Voice report not found.")
    return intake_json(row)


@router.patch("/{iid}", response_model=IntakeResponse)
def review(iid: str, body: Review, user: Worker, db: DB) -> dict[str, Any]:
    row = db.scalar(select(Intake).where(Intake.id == iid).with_for_update())
    if not row or row.reporter_id != user.id:
        raise AppError(404, "NOT_FOUND", "Voice report not found.")
    if row.status != "READY_FOR_REVIEW":
        raise AppError(409, "INTAKE_LOCKED", "This report cannot be edited.")
    row.edited_transcript = body.edited_transcript
    db.commit()
    return intake_json(row)
