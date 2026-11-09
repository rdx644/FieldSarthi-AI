import hashlib
import json
from typing import Any
from uuid import uuid4

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.db.models import Asset, Audit, Idempotency, Intake, Location, Order, User, now
from app.schemas.commands import Confirm

TRANSITIONS = {
    "OPEN": {"CANCELLED"},
    "ASSIGNED": {"IN_PROGRESS", "CANCELLED"},
    "IN_PROGRESS": {"RESOLVED", "CANCELLED"},
    "RESOLVED": set(),
    "CANCELLED": set(),
}


def intake_json(row: Intake) -> dict[str, Any]:
    return {
        "intake_id": row.id,
        "id": row.id,
        "source_type": row.source_type,
        "status": row.status,
        "input_language_code": row.language_code,
        "raw_transcript": row.raw_transcript,
        "edited_transcript": row.edited_transcript,
        "provider": None
        if row.source_type == "MANUAL_TEXT"
        else {
            "name": "Gnani AI",
            "model": row.provider_model,
            "request_id": row.provider_request_id,
        },
        "audio_duration_seconds": row.audio_duration_seconds,
        "stt_latency_ms": row.stt_latency_ms,
        "error_code": row.error_code,
        **row.extraction,
    }


def order_json(row: Order, db: Session, detail: bool = False) -> dict[str, Any]:
    asset = db.get(Asset, row.asset_id)
    loc = db.get(Location, row.location_id)
    assignee = db.get(User, row.assignee_id) if row.assignee_id else None
    result: dict[str, Any] = {
        "id": row.id,
        "public_code": row.public_code,
        "intake_id": row.intake_id,
        "reporter_id": row.reporter_id,
        "location_id": row.location_id,
        "asset_id": row.asset_id,
        "asset_name": asset.name if asset else "",
        "location_name": loc.name if loc else "",
        "issue_category": row.issue_category,
        "description": row.description,
        "priority": row.priority,
        "priority_suggestion": row.priority_suggestion,
        "status": row.status,
        "assignee_id": row.assignee_id,
        "assignee_name": assignee.display_name if assignee else None,
        "version": row.version,
        "created_at": row.created_at.isoformat(),
        "updated_at": row.updated_at.isoformat(),
        "resolved_at": row.resolved_at.isoformat() if row.resolved_at else None,
    }
    if detail:
        intake = db.get(Intake, row.intake_id)
        result["intake"] = intake_json(intake) if intake else None
        result["audit"] = [
            {
                "id": a.id,
                "action": a.action,
                "actor_name": actor_name(db, a.actor_id),
                "from_state": a.from_state,
                "to_state": a.to_state,
                "details": a.details,
                "occurred_at": a.occurred_at.isoformat(),
            }
            for a in db.scalars(
                select(Audit)
                .where(Audit.work_order_id == row.id)
                .order_by(Audit.occurred_at, Audit.id)
            )
        ]
    return result


def accessible_order(db: Session, oid: str, user: User, *, lock: bool = False) -> Order:
    query = select(Order).where(Order.id == oid)
    if lock:
        query = query.with_for_update()
    row = db.scalar(query)
    if (
        not row
        or (user.role == "JUDGE" and not row.judge_visible)
        or (user.role == "WORKER" and row.reporter_id != user.id)
    ):
        raise AppError(404, "NOT_FOUND", "Work order not found.")
    return row


def create_order(db: Session, command: Confirm, user: User, key: str) -> tuple[Order, bool]:
    route = "/api/v1/work-orders"
    digest = hashlib.sha256(
        json.dumps(command.model_dump(), sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    lock_id = int.from_bytes(
        hashlib.sha256(f"{user.id}:{route}:{key}".encode()).digest()[:8], "big", signed=True
    )
    db.execute(text("SELECT pg_advisory_xact_lock(:lock)"), {"lock": lock_id})
    previous = db.scalar(
        select(Idempotency).where(
            Idempotency.actor_id == user.id, Idempotency.route == route, Idempotency.idem_key == key
        )
    )
    if previous:
        if previous.request_hash != digest:
            raise AppError(
                409,
                "IDEMPOTENCY_CONFLICT",
                "This submission key already belongs to another report.",
            )
        return accessible_order(db, previous.result_work_order_id, user), True
    intake = db.scalar(select(Intake).where(Intake.id == command.intake_id).with_for_update())
    if not intake or intake.reporter_id != user.id:
        raise AppError(404, "NOT_FOUND", "Voice report not found.")
    if (
        intake.status not in {"READY_FOR_REVIEW", "CONFIRMED"}
        or not intake.raw_transcript
        or (
            intake.source_type == "GNANI_STT"
            and (not intake.provider_request_id or not intake.provider_model)
        )
    ):
        raise AppError(409, "INTAKE_NOT_READY", "A completed voice or manual report is required.")
    existing = db.scalar(select(Order).where(Order.intake_id == intake.id))
    if existing:
        # A different key may replay the same intake, never silently change it.
        same = all(
            getattr(existing, k) == getattr(command, k)
            for k in [
                "location_id",
                "asset_id",
                "issue_category",
                "description",
                "priority_suggestion",
            ]
        )
        if not same or intake.edited_transcript != command.edited_transcript:
            raise AppError(
                409,
                "INTAKE_ALREADY_CONFIRMED",
                "This report was already confirmed with different details.",
            )
        row = existing
    else:
        asset = db.get(Asset, command.asset_id)
        location = db.get(Location, command.location_id)
        if not asset or not asset.is_active or not location or not location.is_active:
            raise AppError(422, "UNKNOWN_ASSET_OR_LOCATION", "Select a known asset and location.")
        if asset.location_id != location.id:
            raise AppError(
                422, "ASSET_LOCATION_MISMATCH", "The asset does not belong to this location."
            )
        row = Order(
            public_code="WO-" + uuid4().hex[:12].upper(),
            intake_id=intake.id,
            reporter_id=user.id,
            location_id=location.id,
            asset_id=asset.id,
            issue_category=command.issue_category,
            description=command.description,
            priority_suggestion=command.priority_suggestion,
            priority="NORMAL",
        )
        db.add(row)
        db.flush()
        intake.status = "CONFIRMED"
        intake.edited_transcript = command.edited_transcript
        db.add(
            Audit(
                work_order_id=row.id,
                actor_id=user.id,
                action="CREATED",
                to_state="OPEN",
                details={
                    "priority_suggestion": command.priority_suggestion,
                    "human_confirmed": True,
                    "source_type": intake.source_type,
                    "edited_transcript": command.edited_transcript,
                    "location_id": command.location_id,
                    "asset_id": command.asset_id,
                    "issue_category": command.issue_category,
                },
            )
        )
    db.add(
        Idempotency(
            actor_id=user.id,
            route=route,
            idem_key=key,
            request_hash=digest,
            result_work_order_id=row.id,
        )
    )
    db.commit()
    return row, bool(existing)


def change_order(
    db: Session,
    row: Order,
    actor: User,
    action: str,
    value: str,
    version: int,
    note: str | None = None,
) -> Order:
    if row.version != version:
        raise AppError(409, "VERSION_CONFLICT", "This report changed. Refresh and try again.")
    if row.status in {"RESOLVED", "CANCELLED"}:
        raise AppError(409, "INVALID_TRANSITION", "This work order is closed.")
    old = row.status
    details: dict[str, Any] = {}
    if action == "ASSIGNED":
        assignee = db.get(User, value)
        if not assignee or not assignee.is_active or assignee.role != "WORKER":
            raise AppError(422, "INVALID_ASSIGNEE", "Select an active worker.")
        details = {"old_assignee_id": row.assignee_id, "assignee_id": value}
        row.assignee_id = value
        if row.status == "OPEN":
            row.status = "ASSIGNED"
    elif action == "PRIORITY_CHANGED":
        details = {"old_priority": row.priority, "priority": value}
        row.priority = value
    else:
        if value not in TRANSITIONS[row.status]:
            raise AppError(409, "INVALID_TRANSITION", "This status transition is not allowed.")
        if value == "CANCELLED" and (not note or not note.strip()):
            raise AppError(
                422, "CANCELLATION_REQUIRED", "Add a reason before cancelling this work order."
            )
        if value == "RESOLVED":
            if not row.assignee_id or not note or not note.strip():
                raise AppError(
                    422, "RESOLUTION_REQUIRED", "Assign a worker and add a resolution note."
                )
            row.resolved_at = now()
        row.status = value
        note_key = "cancellation_note" if value == "CANCELLED" else "resolution_note"
        details = {note_key: note.strip()} if note else {}
    row.version += 1
    row.updated_at = now()
    db.add(
        Audit(
            work_order_id=row.id,
            actor_id=actor.id,
            action=action,
            from_state=old,
            to_state=row.status,
            details=details,
        )
    )
    db.commit()
    return row


def actor_name(db: Session, actor_id: str) -> str:
    actor = db.get(User, actor_id)
    return actor.display_name if actor else "Unknown actor"
