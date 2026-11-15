"""IMP-05: shared, restart-safe admission of operations, never monetary credits."""

from datetime import timedelta

from sqlalchemy import delete, func, select, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.errors import AppError
from app.db.models import ProviderAdmission, User
from app.db.session import SessionLocal

# Stable signed-bigint namespace shared by all application processes.
ADMISSION_LOCK = 6_114_542_871
ACTOR_HOURLY_LIMIT = 24
GLOBAL_HOURLY_LIMIT = 80


def reserve_provider_admission(actor_id: str, operation: str) -> None:
    """Commit a short reservation before provider waits; never refund failures."""
    try:
        with SessionLocal.begin() as db:
            db.execute(text("SET LOCAL lock_timeout = '3s'"))
            db.execute(text("SET LOCAL statement_timeout = '5s'"))
            actor = db.get(User, actor_id)
            if not actor or not actor.is_active or actor.role not in {"WORKER", "SUPERVISOR"}:
                raise AppError(403, "READ_ONLY_DEMO", "Live audio needs active team access.")
            db.execute(select(func.pg_advisory_xact_lock(ADMISSION_LOCK)))
            now = db.scalar(select(func.clock_timestamp()))
            if now is None:
                raise AppError(503, "PROVIDER_BUDGET", "Audio admission unavailable. Try later.")
            recent = ProviderAdmission.admitted_at > now - timedelta(hours=1)
            total, actor_total = db.execute(
                select(
                    func.count(),
                    func.count().filter(ProviderAdmission.actor_id == actor_id),
                ).where(recent)
            ).one()
            if total >= GLOBAL_HOURLY_LIMIT or actor_total >= ACTOR_HOURLY_LIMIT:
                raise AppError(
                    429, "PROVIDER_BUDGET", "Demo audio budget reached. Try again later."
                )
            db.add(ProviderAdmission(actor_id=actor_id, operation=operation, admitted_at=now))
    except SQLAlchemyError:
        # Do not expose driver exceptions/parameters; there is no RAM fallback.
        raise AppError(
            503,
            "PROVIDER_BUDGET",
            "Audio admission is unavailable. Try later or type your report.",
        ) from None


def cleanup_provider_admissions() -> int:
    """Operator-only bounded cleanup: at most 500 entries older than seven days."""
    with SessionLocal.begin() as db:
        expired = (
            select(ProviderAdmission.id)
            .where(ProviderAdmission.admitted_at < func.now() - timedelta(days=7))
            .order_by(ProviderAdmission.admitted_at, ProviderAdmission.id)
            .limit(500)
        )
        removed = db.scalars(
            delete(ProviderAdmission)
            .where(ProviderAdmission.id.in_(expired))
            .returning(ProviderAdmission.id)
        )
        return len(list(removed))
