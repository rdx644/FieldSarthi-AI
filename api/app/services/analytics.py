"""Role-scoped operational counts, independent of search filters and pagination."""

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.models import Intake, Order, User
from app.schemas.responses import IssueCount, QueueSummary


def accessible_orders(user: User) -> Select[tuple[Order]]:
    query = select(Order)
    if user.role == "WORKER":
        query = query.where(Order.reporter_id == user.id)
    elif user.role == "JUDGE":
        query = query.where(Order.judge_visible)
    return query


def queue_summary(db: Session, scope: Select[tuple[Order]]) -> QueueSummary:
    rows = scope.subquery()
    duration = func.extract("epoch", rows.c.resolved_at - rows.c.created_at)
    valid_resolution = (rows.c.status == "RESOLVED") & (duration >= 0)
    values = (
        db.execute(
            select(
                func.count().label("total"),
                *[
                    func.count().filter(rows.c.status == status).label(status.lower())
                    for status in ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CANCELLED"]
                ],
                func.count()
                .filter(
                    rows.c.status.in_(["OPEN", "ASSIGNED", "IN_PROGRESS"])
                    & (rows.c.priority == "HIGH")
                )
                .label("active_high_priority"),
                func.count().filter(Intake.source_type == "GNANI_STT").label("voice_intake"),
                func.count().filter(Intake.source_type == "MANUAL_TEXT").label("manual_intake"),
                func.avg(duration).filter(valid_resolution).label("mean_resolution_seconds"),
                func.count().filter(valid_resolution).label("resolution_sample_count"),
            )
            .select_from(rows)
            .join(Intake, Intake.id == rows.c.intake_id)
        )
        .mappings()
        .one()
    )
    issues = db.execute(
        select(rows.c.issue_category, func.count())
        .group_by(rows.c.issue_category)
        .order_by(rows.c.issue_category)
    )
    return QueueSummary(
        **values,
        issue_counts=[IssueCount(issue_category=issue, count=count) for issue, count in issues],
    )
