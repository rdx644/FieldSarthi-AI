from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

from app.db.models import Audit, Intake, Order
from app.db.session import SessionLocal, engine
from app.main import app
from app.seed import stable


def login(client, account):
    result = client.post(
        "/api/v1/auth/login",
        headers={"Origin": "http://testserver", "X-Requested-With": "FieldSaarthi"},
        json={"email": account["email"], "password": account["password"]},
    )
    assert result.status_code == 200
    return {"Authorization": "Bearer " + result.json()["access_token"]}


def fixture_intake():
    with SessionLocal() as db:
        row = Intake(
            reporter_id=stable("worker@fieldsaarthi.demo"),
            status="READY_FOR_REVIEW",
            language_code="hi-IN",
            provider_model="prisma-v2.5",
            provider_request_id="TEST-FIXTURE-NOT-LIVE",
            raw_transcript="block b pump leak urgent",
        )
        db.add(row)
        db.commit()
        return row.id


def payload(intake_id):
    return {
        "intake_id": intake_id,
        "location_id": stable("BLK-B-F2"),
        "asset_id": stable("PUMP-B02"),
        "issue_category": "LEAKAGE",
        "description": "Water pump leaking",
        "priority_suggestion": "HIGH",
        "confirmed": True,
    }


def test_end_to_end_order_and_supervisor_state(accounts):
    with TestClient(app) as c:
        worker = login(c, accounts[0])
        supervisor = login(c, accounts[2])
        intake = fixture_intake()
        body = payload(intake)
        key = str(uuid4())
        headers = {**worker, "Idempotency-Key": key}
        first = c.post("/api/v1/work-orders", headers=headers, json=body)
        assert first.status_code == 201, first.text
        order = first.json()
        oid = order["id"]
        replay = c.post("/api/v1/work-orders", headers=headers, json=body)
        assert replay.status_code == 200 and replay.json()["id"] == oid
        conflict = c.post(
            "/api/v1/work-orders", headers=headers, json={**body, "description": "Changed report"}
        )
        assert conflict.status_code == 409
        assert (
            c.patch(
                f"/api/v1/work-orders/{oid}/priority",
                headers=worker,
                json={"priority": "HIGH", "expected_version": 1},
            ).status_code
            == 403
        )
        assignment = c.patch(
            f"/api/v1/work-orders/{oid}/assignment",
            headers=supervisor,
            json={"assignee_id": stable("worker2@fieldsaarthi.demo"), "expected_version": 1},
        )
        assert assignment.status_code == 200
        assert assignment.json()["status"] == "ASSIGNED"
        stale = c.patch(
            f"/api/v1/work-orders/{oid}/priority",
            headers=supervisor,
            json={"priority": "HIGH", "expected_version": 1},
        )
        assert stale.status_code == 409
        assert (
            c.patch(
                f"/api/v1/work-orders/{oid}/status",
                headers=supervisor,
                json={"status": "RESOLVED", "expected_version": 2, "resolution_note": "fixed"},
            ).status_code
            == 409
        )
        assert (
            c.patch(
                f"/api/v1/work-orders/{oid}/status",
                headers=supervisor,
                json={"status": "IN_PROGRESS", "expected_version": 2},
            ).status_code
            == 200
        )
        resolved = c.patch(
            f"/api/v1/work-orders/{oid}/status",
            headers=supervisor,
            json={
                "status": "RESOLVED",
                "expected_version": 3,
                "resolution_note": "Replaced pump seal",
            },
        )
        assert resolved.status_code == 200
        detail = c.get(f"/api/v1/work-orders/{oid}", headers=worker).json()
        assert detail["status"] == "RESOLVED" and detail["version"] == 4
        assert [x["action"] for x in detail["audit"]] == [
            "CREATED",
            "ASSIGNED",
            "STATUS_CHANGED",
            "STATUS_CHANGED",
        ]
        assert detail["intake"]["raw_transcript"] == "block b pump leak urgent"


def test_idor_invalid_asset_and_unconfirmed_create_nothing(accounts):
    with TestClient(app) as c:
        h = login(c, accounts[0])
        other = login(c, accounts[1])
        iid = fixture_intake()
        body = payload(iid)
        assert c.get("/api/v1/intakes/" + iid, headers=other).status_code == 404

        def submit(data, headers=h):
            return c.post(
                "/api/v1/work-orders",
                headers={**headers, "Idempotency-Key": str(uuid4())},
                json=data,
            )

        assert submit(body, other).status_code == 404
        assert submit({**body, "asset_id": stable("AC-A01")}).status_code == 422
        assert submit({**body, "confirmed": False}).status_code == 422
        with SessionLocal() as db:
            assert list(db.scalars(select(Order))) == []


def test_concurrent_different_keys_same_intake_exactly_one_order(accounts):
    with TestClient(app) as c:
        h = login(c, accounts[0])
        body = payload(fixture_intake())

        def submit(_):
            return c.post(
                "/api/v1/work-orders", headers={**h, "Idempotency-Key": str(uuid4())}, json=body
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(submit, range(2)))
        assert all(r.status_code in [200, 201] for r in responses), [r.text for r in responses]
        assert len({r.json()["id"] for r in responses}) == 1
        with SessionLocal() as db:
            assert len(list(db.scalars(select(Order)))) == 1
            assert len(list(db.scalars(select(Audit)))) == 1


def test_audit_and_provider_provenance_are_immutable(accounts):
    iid = fixture_intake()
    with pytest.raises(DBAPIError, match="provider provenance is immutable"):
        with engine.begin() as c:
            c.execute(
                text("UPDATE report_intakes SET raw_transcript='tampered' WHERE id=:id"),
                {"id": iid},
            )


def test_worker_cannot_read_other_order(accounts):
    with TestClient(app) as c:
        first = login(c, accounts[0])
        other = login(c, accounts[1])
        result = c.post(
            "/api/v1/work-orders",
            headers={**first, "Idempotency-Key": str(uuid4())},
            json=payload(fixture_intake()),
        )
        assert result.status_code == 201
        assert c.get("/api/v1/work-orders/" + result.json()["id"], headers=other).status_code == 404
        assert c.get("/api/v1/work-orders", headers=other).json()["total"] == 0


def test_malformed_bearer_does_not_bypass_cookie_csrf(accounts):
    with TestClient(app) as c:
        login(c, accounts[0])
        iid = fixture_intake()
        result = c.patch(
            "/api/v1/intakes/" + iid,
            headers={"Authorization": "Basic junk"},
            json={"edited_transcript": "tampered through cookie"},
        )
        assert result.status_code in {401, 403}


def test_distinct_key_conflicting_replay_is_409_even_for_mismatched_asset(accounts):
    with TestClient(app) as c:
        headers = login(c, accounts[0])
        body = payload(fixture_intake())
        assert (
            c.post(
                "/api/v1/work-orders",
                headers={**headers, "Idempotency-Key": str(uuid4())},
                json=body,
            ).status_code
            == 201
        )
        body["asset_id"] = stable("AC-A01")
        assert (
            c.post(
                "/api/v1/work-orders",
                headers={**headers, "Idempotency-Key": str(uuid4())},
                json=body,
            ).status_code
            == 409
        )


def test_database_rejects_audit_truncation(accounts):
    with pytest.raises(DBAPIError, match="audit events are immutable"):
        with engine.begin() as c:
            c.execute(text("TRUNCATE audit_events"))


def test_database_rejects_completed_intake_deletion(accounts):
    iid = fixture_intake()
    with pytest.raises(DBAPIError, match="provider provenance is immutable"):
        with engine.begin() as c:
            c.execute(text("DELETE FROM report_intakes WHERE id=:id"), {"id": iid})
