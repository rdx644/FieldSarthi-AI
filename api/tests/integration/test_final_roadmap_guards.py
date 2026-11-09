from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from test_workflow import fixture_intake, login, payload

from app.db.models import Order
from app.db.session import SessionLocal
from app.main import app
from app.seed import stable
from app.services.extraction import extract


@pytest.mark.parametrize(
    "cue,warning",
    [
        ("sparking", True),
        ("sparks", True),
        ("short circuit", True),
        ("electric shock", True),
        ("चिंगारी", True),
        ("धुआँ", True),
        ("gas leak", True),
        ("noise", False),
        ("flicker", False),
        ("sparkling clean", False),
    ],
)
def test_explicit_hazards_show_emergency_protocol_warning(accounts, cue, warning):
    with SessionLocal() as db:
        result = extract("Block B pump " + cue, db)
    assert result["emergency_warning"] is warning


@pytest.mark.parametrize(
    "patch,sqlstate",
    [
        ({"status": "INVALID"}, "23514"),
        ({"priority": "URGENT"}, "23514"),
        ({"issue_category": "INVALID"}, "23514"),
        ({"description": "   "}, "23514"),
        ({"version": 0}, "23514"),
        ({"status": "ASSIGNED", "assignee_id": None}, "23514"),
        ({"asset_id": str(uuid4())}, "23503"),
        ({"location_id": str(uuid4())}, "23503"),
        ({"reporter_id": str(uuid4())}, "23503"),
        ({"intake_id": str(uuid4())}, "23503"),
        ({"assignee_id": str(uuid4())}, "23503"),
    ],
)
def test_database_rejects_invalid_rows_directly(accounts, patch, sqlstate):
    fields = {
        "public_code": "WO-DIRECT-NEGATIVE",
        "intake_id": fixture_intake(),
        "reporter_id": stable("worker@fieldsaarthi.demo"),
        "location_id": stable("BLK-B-F2"),
        "asset_id": stable("PUMP-B02"),
        "issue_category": "LEAKAGE",
        "description": "Synthetic pump leak",
    }
    with pytest.raises(IntegrityError) as failure:
        with SessionLocal() as db:
            db.add(Order(**{**fields, **patch}))
            db.commit()
    assert failure.value.orig.sqlstate == sqlstate
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Order)) == 0


@pytest.mark.parametrize("attack", ["' OR 1=1 --", "'; DROP TABLE work_orders; --"])
def test_search_injection_is_literal_and_preserves_ownership_and_tables(accounts, attack):
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        other = login(client, accounts[1])
        assert (
            client.post(
                "/api/v1/work-orders",
                json=payload(fixture_intake()),
                headers={**worker, "Idempotency-Key": str(uuid4())},
            ).status_code
            == 201
        )
        assert client.get("/api/v1/work-orders", headers=worker).json()["total"] == 1
        for headers in [worker, other]:
            response = client.get("/api/v1/work-orders", headers=headers, params={"q": attack})
            assert response.status_code == 200 and response.json()["total"] == 0
        assert client.get("/api/v1/work-orders", headers=worker).json()["total"] == 1
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Order)) == 1
