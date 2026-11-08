import asyncio
import os
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, Query, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.limits import provider_budget
from app.core.security import current_user, supervisor, worker
from app.db.models import Order, User
from app.db.session import get_db
from app.integrations.gnani import GnaniError
from app.integrations.tts import TimbreClient, provider_slots
from app.schemas.commands import Assignment, Confirm, PriorityChange, StatusChange
from app.services.orders import accessible_order, change_order, create_order, order_json

router = APIRouter(prefix="/api/v1/work-orders")
DB = Annotated[Session, Depends(get_db)]
Current = Annotated[User, Depends(current_user)]
Supervisor = Annotated[User, Depends(supervisor)]
Worker = Annotated[User, Depends(worker)]


@router.get("/capabilities/audio")
def audio_capability(user: Current) -> dict[str, bool]:
    return {"tts_enabled": os.getenv("GNANI_TTS_ENABLED", "false").lower() == "true"}


@router.post("/{oid}/acknowledgment-audio")
async def acknowledgment(oid: str, user: Current, db: DB) -> Response:
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
        async with asyncio.timeout(90):
            async with provider_slots:
                data = await TimbreClient(os.environ["GNANI_API_KEY_ID"]).synthesize(code)
    except (GnaniError, TimeoutError):
        raise AppError(
            503, "TTS_UNAVAILABLE", "Audio is unavailable. Your work order remains saved."
        ) from None
    return Response(data, media_type="audio/wav", headers={"Cache-Control": "no-store"})


@router.post("")
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


@router.get("")
def queue(
    user: Current,
    db: DB,
    status: str | None = None,
    priority: str | None = None,
    location_id: str | None = None,
    assignee_id: str | None = None,
    q: Annotated[str, Query(max_length=100)] = "",
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, Any]:
    query = select(Order)
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


@router.get("/{oid}")
def detail(oid: str, user: Current, db: DB) -> dict[str, Any]:
    return order_json(accessible_order(db, oid, user), db, detail=True)


@router.patch("/{oid}/assignment")
def assign(oid: str, body: Assignment, user: Supervisor, db: DB) -> dict[str, Any]:
    row = accessible_order(db, oid, user, lock=True)
    return order_json(
        change_order(db, row, user, "ASSIGNED", body.assignee_id, body.expected_version), db, True
    )


@router.patch("/{oid}/priority")
def prioritize(oid: str, body: PriorityChange, user: Supervisor, db: DB) -> dict[str, Any]:
    row = accessible_order(db, oid, user, lock=True)
    return order_json(
        change_order(db, row, user, "PRIORITY_CHANGED", body.priority, body.expected_version),
        db,
        True,
    )


@router.patch("/{oid}/status")
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
            body.resolution_note,
        ),
        db,
        True,
    )


@router.get("/{oid}/duplicates")
def duplicates(oid: str, user: Current, db: DB) -> list[dict[str, Any]]:
    row = accessible_order(db, oid, user)
    query = select(Order).where(
        Order.asset_id == row.asset_id,
        Order.id != row.id,
        Order.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"]),
    )
    if user.role == "WORKER":
        query = query.where(Order.reporter_id == user.id)
    return [order_json(x, db) for x in db.scalars(query.limit(10))]
