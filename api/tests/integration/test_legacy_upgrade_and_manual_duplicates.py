from uuid import uuid4

from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from test_workflow import login, payload

from alembic import command
from app.db.models import User
from app.db.session import SessionLocal, engine
from app.main import app
from app.seed import seed, stable


def test_upgrade_legacy_table_role_check_allows_judge_seed(accounts, monkeypatch):
    # Reproduce the actual older table-level check, which fresh metadata hides.
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE users DROP CONSTRAINT users_role_check"))
        connection.execute(
            text(
                "ALTER TABLE users ADD CONSTRAINT users_check "
                "CHECK (role IN ('WORKER','SUPERVISOR'))"
            )
        )
        connection.execute(text("UPDATE alembic_version SET version_num='0003'"))
    command.upgrade(Config("alembic.ini"), "head")
    monkeypatch.setenv("PUBLIC_JUDGE_DEMO_ENABLED", "true")
    with SessionLocal() as db:
        seed(db)
        assert db.get(User, stable("public-judge")).role == "JUDGE"
        assert db.scalar(select(User.id).where(User.role == "JUDGE"))


def test_manual_duplicate_hints_match_voice_ownership_scope(accounts):
    with TestClient(app) as client:
        for account in accounts[:2]:
            headers = login(client, account)
            intake = client.post(
                "/api/v1/intakes/manual", headers=headers, json={"text": "Block B pump leaking"}
            )
            assert intake.status_code == 201
            assert intake.json()["possible_duplicates"] == 0
            created = client.post(
                "/api/v1/work-orders",
                json=payload(intake.json()["id"]),
                headers={**headers, "Idempotency-Key": str(uuid4())},
            )
            assert created.status_code == 201
        headers = login(client, accounts[0])
        response = client.post(
            "/api/v1/intakes/manual", headers=headers, json={"text": "Block B pump leaking"}
        )
        assert response.json()["possible_duplicates"] == 1
