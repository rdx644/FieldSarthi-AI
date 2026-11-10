import asyncio
import os
from time import perf_counter
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Query, Request, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.limits import provider_budget, provider_requests_enabled
from app.core.security import current_user, supervisor, worker
from app.core.telemetry import stage_event
from app.db.models import Order, User
from app.db.session import get_db
from app.integrations.gnani import GnaniError
from app.integrations.tts import TimbreClient, provider_slots
from app.schemas.commands import Assignment, Confirm, Priority, PriorityChange, Status, StatusChange
from app.schemas.responses import OrderResponse, QueueResponse
from app.services.orders import accessible_order, change_order, create_order, order_json

router = APIRouter(prefix="/api/v1/work-orders")
DB = Annotated[Session, Depends(get_db)]
Current = Annotated[User, Depends(current_user)]
Supervisor = Annotated[User, Depends(supervisor)]
Worker = Annotated[User, Depends(worker)]


@router.get("/capabilities/audio")
def audio_capability(user: Current) -> dict[str, bool]:
    return {
        "tts_enabled": provider_requests_enabled()
        and user.role != "JUDGE"
        and os.getenv("GNANI_TTS_ENABLED", "false").lower() == "true"
    }


@router.post("/{oid}/acknowledgment-audio")
async def acknowledgment(oid: str, request: Request, user: Current, db: DB) -> Response:
    if user.role == "JUDGE":
        raise AppError(
            403, "READ_ONLY_DEMO", "The judge demo is read-only; live audio uses team access."
        )
    row = accessible_order(db, oid, user)
    code = row.public_code
    actor_id = user.id
    db.rollback()
    if os.getenv("GNANI_TTS_ENABLED", "false").lower() != "true":
        raise AppError(
            503,
            "TTS_UNAVAILABLE",
            "Spoken acknowledgment is not enabled. Your report remains saved.",
        )
    try:
        provider_budget.check(actor_id)
        started = perf_counter()
        async with asyncio.timeout(90):
            async with provider_slots:
                data = await TimbreClient(os.environ["GNANI_API_KEY_ID"]).synthesize(code)
        stage_event(request.state.request_id, "provider_tts", started)
    except (GnaniError, TimeoutError) as exc:
        stage_event(
            request.state.request_id,
            "provider_tts",
            started,
            code=exc.code if isinstance(exc, GnaniError) else "TTS_TIMEOUT",
        )
        raise AppError(
            503, "TTS_UNAVAILABLE", "Audio is unavailable. Your work order remains saved."
        ) from None
    return Response(data, media_type="audio/wav", headers={"Cache-Control": "no-store"})


@router.post("", response_model=OrderResponse)
def confirm(
    body: Confirm,
    response: Response,
    user: Worker,
    db: DB,
    idempotency_key: Annotated[str, Header(min_length=8, max_length=100)],
) -> dict[str, Any]:
    row, replay = create_order(db, body, user, idempotency_key)
    response.status_code = 200 if replay else 201
    return order_json(row, db, detail=True)


@router.get("", response_model=QueueResponse)
def queue(
    user: Current,
    db: DB,
    status: Status | None = None,
    priority: Priority | None = None,
    location_id: str | None = None,
    assignee_id: str | None = None,
    q: Annotated[str, Query(max_length=100)] = "",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, Any]:
    query = select(Order)
    if user.role == "JUDGE":
        query = query.where(Order.judge_visible)
    if user.role == "WORKER":
        query = query.where(Order.reporter_id == user.id)
    for name, value in [
        ("status", status),
        ("priority", priority),
        ("location_id", location_id),
        ("assignee_id", assignee_id),
    ]:
        if value:
            query = query.where(getattr(Order, name) == value)
    if q:
        query = query.where(
            Order.description.ilike("%" + q + "%") | Order.public_code.ilike("%" + q + "%")
        )
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = db.scalars(
        query.order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    )
    return {
        "items": [order_json(x, db) for x in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{oid}", response_model=OrderResponse)
def detail(oid: str, user: Current, db: DB) -> dict[str, Any]:
    return order_json(accessible_order(db, oid, user), db, detail=True)


@router.patch("/{oid}/assignment", response_model=OrderResponse)
def assign(oid: str, body: Assignment, user: Supervisor, db: DB) -> dict[str, Any]:
    row = accessible_order(db, oid, user, lock=True)
    return order_json(
        change_order(db, row, user, "ASSIGNED", body.assignee_id, body.expected_version), db, True
    )


@router.patch("/{oid}/priority", response_model=OrderResponse)
def prioritize(oid: str, body: PriorityChange, user: Supervisor, db: DB) -> dict[str, Any]:
    row = accessible_order(db, oid, user, lock=True)
    return order_json(
        change_order(db, row, user, "PRIORITY_CHANGED", body.priority, body.expected_version),
        db,
        True,
    )


@router.patch("/{oid}/status", response_model=OrderResponse)
def advance(oid: str, body: StatusChange, user: Supervisor, db: DB) -> dict[str, Any]:
    row = accessible_order(db, oid, user, lock=True)
    return order_json(
        change_order(
            db,
            row,
            user,
            "STATUS_CHANGED",
            body.status,
            body.expected_version,
            body.cancellation_note if body.status == "CANCELLED" else body.resolution_note,
        ),
        db,
        True,
    )


@router.get("/{oid}/duplicates", response_model=list[OrderResponse])
def duplicates(oid: str, user: Current, db: DB) -> list[dict[str, Any]]:
    row = accessible_order(db, oid, user)
    query = select(Order).where(
        Order.asset_id == row.asset_id,
        Order.id != row.id,
        Order.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
    )
    if user.role == "WORKER":
        query = query.where(Order.reporter_id == user.id)
    if user.role == "JUDGE":
        query = query.where(Order.judge_visible)
    return [order_json(x, db) for x in db.scalars(query.limit(10))]
