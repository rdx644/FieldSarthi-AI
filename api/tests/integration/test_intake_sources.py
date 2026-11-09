import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from test_workflow import login, payload

from app.db.session import engine
from app.main import app
from app.routers import intakes


def test_manual_text_is_explicit_and_has_no_provider_provenance(accounts, monkeypatch):
    async def forbidden(*args, **kwargs):
        raise AssertionError("Manual reporting must never call Gnani")

    monkeypatch.setattr(intakes.speech, "transcribe", forbidden)
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        result = client.post(
            "/api/v1/intakes/manual",
            headers=headers,
            json={"text": "Block B pump leaking urgently", "language_code": "en-IN"},
        )
        assert result.status_code == 201, result.text
        intake = result.json()
        assert intake["source_type"] == "MANUAL_TEXT"
        assert intake["provider"] is None
        assert intake["audio_duration_seconds"] is None and intake["stt_latency_ms"] is None
        assert client.get("/api/v1/work-orders", headers=headers).json()["total"] == 0
        order = client.post(
            "/api/v1/work-orders",
            headers={**headers, "Idempotency-Key": "manual-test"},
            json=payload(intake["id"]),
        )
        assert order.status_code == 201, order.text
        assert order.json()["audit"][0]["details"]["source_type"] == "MANUAL_TEXT"
        assert order.json()["intake"]["provider"] is None
    with pytest.raises(DBAPIError, match="provenance is immutable"):
        with engine.begin() as connection:
            connection.execute(
                text("UPDATE report_intakes SET source_type='GNANI_STT' WHERE id=:id"),
                {"id": intake["id"]},
            )


@pytest.mark.parametrize(
    "body",
    [
        {"text": "    "},
        {"text": "abc"},
        {"text": "x" * 4001},
        {"text": "Block B pump leak", "provider_request_id": "forged"},
    ],
)
def test_manual_input_rejects_blank_oversized_or_forged_provenance(accounts, body):
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        assert client.post("/api/v1/intakes/manual", headers=headers, json=body).status_code == 422


def test_manual_route_is_reporter_only(accounts):
    with TestClient(app) as client:
        headers = login(client, accounts[2])
        assert (
            client.post(
                "/api/v1/intakes/manual", headers=headers, json={"text": "Block B pump leak"}
            ).status_code
            == 403
        )
