"""Named negative and transactional scenarios missing from the original audit."""

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, func, select, text
from sqlalchemy.exc import DBAPIError
from test_workflow import fixture_intake, login, payload

from app.core.config import JWT_SECRET
from app.db.models import Audit, Idempotency, Intake, Order
from app.db.session import SessionLocal, engine
from app.main import app
from app.seed import stable


def submit(client, headers, body, key=None):
    return client.post(
        "/api/v1/work-orders",
        json=body,
        headers={**headers, "Idempotency-Key": key or str(uuid4())},
    )


@pytest.mark.parametrize(
    "replacement",
    [
        {"asset_id": str(uuid4())},
        {"location_id": str(uuid4())},
        {"asset_id": ""},
        {"description": "    "},
        {"description": ""},
        {"confirmed": "true"},
    ],
)
def test_invalid_required_fields_never_create_order(accounts, replacement):
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        assert (
            submit(client, headers, {**payload(fixture_intake()), **replacement}).status_code == 422
        )
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Order)) == 0
        assert db.scalar(select(func.count()).select_from(Audit)) == 0


def test_failed_intake_cannot_be_confirmed(accounts):
    with SessionLocal() as db:
        intake = Intake(
            reporter_id=stable("worker@fieldsaarthi.demo"),
            language_code="hi-IN",
            status="FAILED",
            error_code="GNANI_TIMEOUT",
        )
        db.add(intake)
        db.commit()
        iid = intake.id
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        assert submit(client, headers, payload(iid)).status_code == 409


def test_injected_audit_failure_rolls_back_order_intake_and_idempotency(accounts):
    iid = fixture_intake()

    def fail_audit(mapper, connection, target):
        raise RuntimeError("TEST-ONLY injected write failure")

    event.listen(Audit, "before_insert", fail_audit)
    try:
        with TestClient(app) as client:
            headers = login(client, accounts[0])
            assert submit(client, headers, payload(iid)).status_code == 500
    finally:
        event.remove(Audit, "before_insert", fail_audit)
    with SessionLocal() as db:
        for model in [Order, Audit, Idempotency]:
            assert db.scalar(select(func.count()).select_from(model)) == 0
        assert db.get(Intake, iid).status == "READY_FOR_REVIEW"


def test_concurrent_same_key_is_exactly_one_order_and_audit(accounts):
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        body = payload(fixture_intake())
        key = str(uuid4())
        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(lambda _: submit(client, headers, body, key), range(2)))
        assert sorted(response.status_code for response in responses) == [200, 201]
        assert len({response.json()["id"] for response in responses}) == 1
    with SessionLocal() as db:
        for model in [Order, Audit, Idempotency]:
            assert db.scalar(select(func.count()).select_from(model)) == 1


@pytest.mark.parametrize("token_kind", ["expired", "invalid-signature", "garbage"])
def test_expired_and_invalid_tokens_are_denied(accounts, token_kind):
    token = jwt.encode(
        {
            "sub": stable("worker@fieldsaarthi.demo"),
            "iss": "fieldsaarthi",
            "aud": "fieldsaarthi-web",
            "exp": datetime.now(UTC) + timedelta(minutes=-1 if token_kind == "expired" else 5),
        },
        JWT_SECRET if token_kind == "expired" else "test-only-invalid-signature-key-32plus",
        algorithm="HS256",
    )
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/me",
            headers={
                "Authorization": "Bearer " + ("garbage" if token_kind == "garbage" else token)
            },
        )
        assert response.status_code == 401


def test_readiness_fails_when_database_is_unavailable(monkeypatch):
    def unavailable():
        raise OSError("TEST-ONLY unreachable database")

    monkeypatch.setattr(engine, "connect", unavailable)
    with TestClient(app) as client:
        assert client.get("/health/ready").status_code == 503
        assert client.get("/health/live").status_code == 200


def test_edit_preserves_original_and_locks_provenance_after_confirmation(accounts):
    iid = fixture_intake()
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        edited = "Human correction: Block B pump leaking"
        assert (
            client.patch(
                "/api/v1/intakes/" + iid, headers=headers, json={"edited_transcript": edited}
            ).status_code
            == 200
        )
        created = submit(client, headers, {**payload(iid), "edited_transcript": edited}).json()
        intake = created["intake"]
        assert intake["raw_transcript"] == "block b pump leak urgent"
        assert intake["edited_transcript"] == edited
        assert created["audit"][0]["details"]["edited_transcript"] == edited
        assert (
            client.patch(
                "/api/v1/intakes/" + iid, headers=headers, json={"edited_transcript": "Late edit"}
            ).status_code
            == 409
        )
    for column, value in [
        ("raw_transcript", "forged"),
        ("provider_request_id", "forged"),
        ("language_code", "en-IN"),
        ("extraction", '{"tampered":true}'),
    ]:
        with pytest.raises(DBAPIError, match="provenance is immutable"):
            with engine.begin() as connection:
                connection.execute(
                    text(f"UPDATE report_intakes SET {column}=:value WHERE id=:id"),
                    {"value": value, "id": iid},
                )


@pytest.mark.parametrize(
    "scenario", ["active-same", "resolved-only", "distinct-asset", "other-owner"]
)
def test_duplicate_warning_scope(accounts, scenario):
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        supervisor = login(client, accounts[2])
        first = submit(client, worker, payload(fixture_intake())).json()
        if scenario == "resolved-only":
            for endpoint, body in [
                (
                    "assignment",
                    {"assignee_id": stable("worker2@fieldsaarthi.demo"), "expected_version": 1},
                ),
                ("status", {"status": "IN_PROGRESS", "expected_version": 2}),
                (
                    "status",
                    {"status": "RESOLVED", "expected_version": 3, "resolution_note": "Fixed seal"},
                ),
            ]:
                assert (
                    client.patch(
                        "/api/v1/work-orders/" + first["id"] + "/" + endpoint,
                        headers=supervisor,
                        json=body,
                    ).status_code
                    == 200
                )
        body = payload(fixture_intake())
        if scenario == "distinct-asset":
            body.update(location_id=stable("WH-C"), asset_id=stable("FAN-C03"))
        second = submit(client, worker, body).json()
        if scenario == "other-owner":
            with SessionLocal() as db:
                db.get(Order, first["id"]).reporter_id = stable("worker2@fieldsaarthi.demo")
                db.commit()
        duplicates = client.get(
            "/api/v1/work-orders/" + second["id"] + "/duplicates", headers=worker
        ).json()
        assert len(duplicates) == (1 if scenario == "active-same" else 0)
