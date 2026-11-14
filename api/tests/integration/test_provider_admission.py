"""IMP-05 / T-IMP-050..056: real test-PostgreSQL, zero provider requests."""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import func, inspect, select, text, update
from sqlalchemy.exc import OperationalError
from test_workflow import fixture_intake, login, payload

from alembic import command
from app.core.errors import AppError
from app.core.limits import ProviderBudget
from app.db.models import ProviderAdmission, User
from app.db.session import SessionLocal, engine
from app.main import app
from app.routers import intakes, orders
from app.seed import stable
from app.services import provider_admission


def actor(accounts, index=0):
    return stable(accounts[index]["email"])


def count_admissions():
    with SessionLocal() as db:
        return db.scalar(select(func.count()).select_from(ProviderAdmission))


def admit(actor_id, operation):
    try:
        ProviderBudget().check(actor_id, operation)
        return "admitted"
    except AppError as error:
        assert error.code == "PROVIDER_BUDGET" and error.status == 429
        return "denied"


def test_actor_cap_is_shared_by_stt_tts_and_new_instances(accounts, monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    for index in range(24):
        # A new object/session for every reservation models process recreation.
        ProviderBudget().check(actor(accounts), "STT" if index % 2 else "TTS")
    with pytest.raises(AppError) as error:
        ProviderBudget().check(actor(accounts), "TTS")
    assert error.value.status == 429 and error.value.code == "PROVIDER_BUDGET"
    assert count_admissions() == 24
    restarted = subprocess.run(
        [
            sys.executable,
            "-c",
            "from app.db.session import engine; "
            "assert engine.url.database == 'fieldsaarthi_test'; "
            "from app.core.limits import ProviderBudget; "
            "from app.core.errors import AppError\n"
            "try:\n"
            f"    ProviderBudget().check({actor(accounts)!r}, 'TTS')\n"
            "except AppError as error:\n"
            "    print(error.status, error.code)\n",
        ],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=True,
        timeout=15,
    )
    assert restarted.stdout.strip() == "429 PROVIDER_BUDGET"
    with SessionLocal() as db:
        assert set(db.scalars(select(ProviderAdmission.operation))) == {"STT", "TTS"}
    assert set(column["name"] for column in inspect(engine).get_columns("provider_admissions")) == {
        "id",
        "actor_id",
        "operation",
        "admitted_at",
    }


def test_global_cap_and_concurrent_operations_do_not_oversubscribe(accounts, monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    actors = []
    with SessionLocal.begin() as db:
        for index in range(8):
            user = User(
                display_name="Test-only admission actor",
                email=f"budget-{index}@test.invalid",
                password_hash="TEST-ONLY-unusable-hash",
                role="WORKER",
            )
            db.add(user)
            db.flush()
            actors.append(user.id)
    # Both operation types, multiple actors and independent transactions compete.
    tasks = [(actors[index % 8], "STT" if index % 2 else "TTS") for index in range(96)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(lambda task: admit(*task), tasks))
    assert outcomes.count("admitted") == 80
    assert outcomes.count("denied") == 16
    assert count_admissions() == 80
    with pytest.raises(AppError) as error:
        ProviderBudget().check(actor(accounts), "STT")
    assert error.value.status == 429


def test_concurrent_same_actor_limit_is_atomic(accounts, monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(
            pool.map(lambda index: admit(actor(accounts), "STT" if index % 2 else "TTS"), range(40))
        )
    assert outcomes.count("admitted") == 24 and outcomes.count("denied") == 16
    assert count_admissions() == 24


def test_expired_reservations_release_capacity_by_database_time(accounts, monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    for _ in range(24):
        ProviderBudget().check(actor(accounts))
    with SessionLocal.begin() as db:
        db.execute(
            update(ProviderAdmission).values(admitted_at=func.now() - timedelta(seconds=3601))
        )
    ProviderBudget().check(actor(accounts), "TTS")
    assert count_admissions() == 25


def test_cleanup_is_bounded_and_keeps_recent_reservations(accounts):
    with SessionLocal.begin() as db:
        old = db.scalar(select(func.now())) - timedelta(days=8)
        for _ in range(503):
            db.add(ProviderAdmission(actor_id=actor(accounts), operation="STT", admitted_at=old))
        db.add(ProviderAdmission(actor_id=actor(accounts), operation="TTS", admitted_at=func.now()))
    assert provider_admission.cleanup_provider_admissions() == 500
    assert count_admissions() == 4
    assert provider_admission.cleanup_provider_admissions() == 3
    assert count_admissions() == 1


def test_pause_inactive_and_judge_do_not_reserve(accounts, monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "false")
    with pytest.raises(AppError) as error:
        ProviderBudget().check(actor(accounts))
    assert error.value.code == "GNANI_REQUESTS_PAUSED"
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    with SessionLocal.begin() as db:
        db.get(User, actor(accounts)).is_active = False
        judge = User(
            display_name="Test-only read-only judge",
            email="budget-judge@test.invalid",
            password_hash="TEST-ONLY-unusable-hash",
            role="JUDGE",
        )
        db.add(judge)
        db.flush()
        judge_id = judge.id
    for actor_id in (actor(accounts), judge_id):
        with pytest.raises(AppError) as error:
            ProviderBudget().check(actor_id)
        assert error.value.status == 403
    assert count_admissions() == 0


def test_admission_transaction_rolls_back_failed_commit(accounts, monkeypatch):
    from sqlalchemy import event

    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")

    def reject_new_ledger_row(session):
        if any(isinstance(row, ProviderAdmission) for row in session.new):
            raise OperationalError("TEST-ONLY commit failure", {}, Exception("private detail"))

    event.listen(SessionLocal.class_, "before_commit", reject_new_ledger_row)
    try:
        with pytest.raises(AppError) as error:
            ProviderBudget().check(actor(accounts))
        assert error.value.status == 503 and error.value.code == "PROVIDER_BUDGET"
    finally:
        event.remove(SessionLocal.class_, "before_commit", reject_new_ledger_row)
    assert count_admissions() == 0


def test_denied_database_admission_never_calls_provider_or_changes_saved_order(
    accounts, monkeypatch
):
    from test_intakes import wav

    async def forbidden(*args, **kwargs):
        raise AssertionError("Denied admission must not call a speech provider")

    class UnavailableSessions:
        def begin(self):
            raise OperationalError("TEST-ONLY unavailable ledger", {}, Exception("private detail"))

    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    monkeypatch.setenv("GNANI_TTS_ENABLED", "true")
    monkeypatch.setattr(intakes.speech, "transcribe", forbidden)
    monkeypatch.setattr(orders.TimbreClient, "synthesize", forbidden)
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        saved = client.post(
            "/api/v1/work-orders",
            headers={**headers, "Idempotency-Key": str(uuid4())},
            json=payload(fixture_intake()),
        ).json()
        before = client.get("/api/v1/work-orders/" + saved["id"], headers=headers).json()
        monkeypatch.setattr(provider_admission, "SessionLocal", UnavailableSessions())
        transcribe = client.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("test.wav", wav(), "audio/wav")},
        )
        tts = client.post(
            "/api/v1/work-orders/" + saved["id"] + "/acknowledgment-audio", headers=headers
        )
        for response in (transcribe, tts):
            assert response.status_code == 503
            assert response.json()["error"]["code"] == "PROVIDER_BUDGET"
        assert client.get("/api/v1/work-orders/" + saved["id"], headers=headers).json() == before
        manual = client.post(
            "/api/v1/intakes/manual", headers=headers, json={"text": "Block B pump leak"}
        )
        assert manual.status_code == 201
    assert count_admissions() == 0


def test_0004_upgrade_preserves_domain_data_and_exposes_rollback_readiness_gate(
    accounts, monkeypatch
):
    import app.main as main_module

    with TestClient(app) as client:
        headers = login(client, accounts[0])
        saved = client.post(
            "/api/v1/work-orders",
            headers={**headers, "Idempotency-Key": str(uuid4())},
            json=payload(fixture_intake()),
        ).json()
        before = client.get("/api/v1/work-orders/" + saved["id"], headers=headers).json()
        # Recreate the actual pre-ledger 0004 shape, exclusively in fieldsaarthi_test.
        assert engine.url.database == "fieldsaarthi_test"
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE provider_admissions"))
            connection.execute(text("UPDATE alembic_version SET version_num='0004'"))
        command.upgrade(Config("alembic.ini"), "head")
        assert client.get("/health/ready").status_code == 200
        assert client.get("/api/v1/work-orders/" + saved["id"], headers=headers).json() == before
        # Old application checks an exact 0004 head: additive SQL is readable, but
        # its readiness still fails. Production rollout requires a compatibility plan.
        monkeypatch.setattr(main_module, "schema_heads", {"0004"})
        assert client.get("/health/ready").status_code == 503
