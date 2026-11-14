"""T-IMP-020..024: synthetic DB counts, never live provider evidence."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from test_workflow import login

from app.db.models import Intake, Order
from app.db.session import SessionLocal
from app.main import app
from app.seed import seed, stable


def populate():
    with SessionLocal() as db:
        for index in range(25):
            reporter = stable(
                "worker@fieldsaarthi.demo" if index < 23 else "worker2@fieldsaarthi.demo"
            )
            intake = Intake(
                reporter_id=reporter,
                source_type="GNANI_STT" if index < 20 else "MANUAL_TEXT",
                status="CONFIRMED",
                language_code="en-IN",
                raw_transcript="TEST ONLY",
            )
            db.add(intake)
            db.flush()
            status = ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CANCELLED"][index % 5]
            created = datetime(2026, 1, 1, tzinfo=UTC)
            # Resolved records exercise valid, missing and negative durations.
            seconds = {3: 60, 8: 180, 13: -60}.get(index)
            db.add(
                Order(
                    public_code="TEST-" + uuid4().hex,
                    intake_id=intake.id,
                    reporter_id=reporter,
                    location_id=stable("BLK-B-F2"),
                    asset_id=stable("PUMP-B02"),
                    issue_category="LEAKAGE" if index < 24 else "OTHER",
                    description="Synthetic pump leak",
                    status=status,
                    priority="HIGH" if index % 2 == 0 else "NORMAL",
                    priority_suggestion="HIGH",
                    created_at=created,
                    assignee_id=stable("worker2@fieldsaarthi.demo")
                    if status in {"ASSIGNED", "IN_PROGRESS", "RESOLVED"}
                    else None,
                    resolved_at=created + timedelta(seconds=seconds)
                    if seconds is not None
                    else None,
                    judge_visible=index == 0,
                )
            )
        db.commit()


def test_summary_is_role_scoped_and_stable_across_pages_filters(accounts, monkeypatch):
    monkeypatch.setenv("PUBLIC_JUDGE_DEMO_ENABLED", "true")
    with SessionLocal() as db:
        seed(db)
    populate()
    with TestClient(app) as client:
        supervisor = login(client, accounts[2])
        first = client.get("/api/v1/work-orders", headers=supervisor)
        assert first.status_code == 200
        assert first.headers["Cache-Control"] == "no-store"
        body = first.json()
        assert len(body["items"]) == 20 and body["total"] == 25
        summary = body["summary"]
        assert summary == {
            "scope": "role_accessible_all",
            "total": 25,
            "open": 5,
            "assigned": 5,
            "in_progress": 5,
            "resolved": 5,
            "cancelled": 5,
            "active_high_priority": 8,
            "voice_intake": 20,
            "manual_intake": 5,
            "mean_resolution_seconds": 120.0,
            "resolution_sample_count": 2,
            "issue_counts": [
                {"issue_category": "LEAKAGE", "count": 24},
                {"issue_category": "OTHER", "count": 1},
            ],
        }
        for params, total in [
            ({"page": 2}, 25),
            ({"status": "CANCELLED"}, 5),
            ({"q": "absent"}, 0),
        ]:
            filtered = client.get("/api/v1/work-orders", headers=supervisor, params=params).json()
            assert filtered["total"] == total and filtered["summary"] == summary
        worker = login(client, accounts[0])
        own = client.get("/api/v1/work-orders", headers=worker).json()["summary"]
        assert own["total"] == 23 and own["manual_intake"] == 3
        assert own["issue_counts"] == [{"issue_category": "LEAKAGE", "count": 23}]
        other = login(client, accounts[1])
        assert client.get("/api/v1/work-orders", headers=other).json()["summary"]["total"] == 2
        client.cookies.clear()
        assert client.post("/api/v1/auth/judge-demo").status_code == 200
        public = client.get("/api/v1/work-orders").json()["summary"]
        assert public["total"] == public["open"] == public["voice_intake"] == 1
        assert public["mean_resolution_seconds"] is None
        assert public["resolution_sample_count"] == 0
        assert public["issue_counts"] == [{"issue_category": "LEAKAGE", "count": 1}]


def test_empty_summary_has_no_invented_resolution_time(accounts):
    with TestClient(app) as client:
        result = client.get("/api/v1/work-orders", headers=login(client, accounts[0])).json()
    summary = result["summary"]
    assert result["total"] == summary["total"] == 0
    assert summary["mean_resolution_seconds"] is None
    assert summary["resolution_sample_count"] == 0 and summary["issue_counts"] == []
    assert (
        sum(summary[key] for key in ["open", "assigned", "in_progress", "resolved", "cancelled"])
        == 0
    )
