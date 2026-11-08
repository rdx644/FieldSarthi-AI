from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def now() -> datetime:
    return datetime.now(UTC)


def uid() -> str:
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('WORKER','SUPERVISOR')"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    display_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    code: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    location_id: Mapped[str] = mapped_column(ForeignKey("locations.id"))
    asset_code: Mapped[str] = mapped_column(String(30), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Intake(Base):
    __tablename__ = "report_intakes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('TRANSCRIBING','READY_FOR_REVIEW','CONFIRMED','FAILED','DISCARDED')"
        ),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    reporter_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="TRANSCRIBING")
    language_code: Mapped[str] = mapped_column(String(10))
    provider_model: Mapped[str | None] = mapped_column(String(60))
    provider_request_id: Mapped[str | None] = mapped_column(String(160), index=True)
    raw_transcript: Mapped[str | None] = mapped_column(Text)
    edited_transcript: Mapped[str | None] = mapped_column(Text)
    extraction: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    audio_duration_seconds: Mapped[float | None]
    stt_latency_ms: Mapped[int | None]
    error_code: Mapped[str | None] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


class Order(Base):
    __tablename__ = "work_orders"
    __table_args__ = (
        CheckConstraint("status IN ('OPEN','ASSIGNED','IN_PROGRESS','RESOLVED','CANCELLED')"),
        CheckConstraint("priority IN ('LOW','NORMAL','HIGH')"),
        CheckConstraint(
            "issue_category IN ('LEAKAGE','ELECTRICAL','MECHANICAL','CLEANING','OTHER')"
        ),
        CheckConstraint("length(trim(description)) > 0"),
        CheckConstraint("version >= 1"),
        CheckConstraint(
            "status NOT IN ('ASSIGNED','IN_PROGRESS','RESOLVED') OR assignee_id IS NOT NULL"
        ),
    )
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    public_code: Mapped[str] = mapped_column(String(40), unique=True)
    intake_id: Mapped[str] = mapped_column(ForeignKey("report_intakes.id"), unique=True)
    reporter_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    location_id: Mapped[str] = mapped_column(ForeignKey("locations.id"))
    asset_id: Mapped[str] = mapped_column(ForeignKey("assets.id"), index=True)
    issue_category: Mapped[str] = mapped_column(String(20))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(10), default="NORMAL")
    priority_suggestion: Mapped[str] = mapped_column(String(10), default="NORMAL")
    status: Mapped[str] = mapped_column(String(20), default="OPEN", index=True)
    assignee_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Audit(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    work_order_id: Mapped[str] = mapped_column(ForeignKey("work_orders.id"), index=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(30))
    from_state: Mapped[str | None] = mapped_column(String(20))
    to_state: Mapped[str | None] = mapped_column(String(20))
    details: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Idempotency(Base):
    __tablename__ = "idempotency_keys"
    __table_args__ = (UniqueConstraint("actor_id", "route", "idem_key"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    route: Mapped[str] = mapped_column(String(60))
    idem_key: Mapped[str] = mapped_column(String(100))
    request_hash: Mapped[str] = mapped_column(String(64))
    result_work_order_id: Mapped[str] = mapped_column(ForeignKey("work_orders.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
