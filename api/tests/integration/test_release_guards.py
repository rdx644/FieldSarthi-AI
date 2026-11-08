from uuid import uuid4

from fastapi.testclient import TestClient
from test_workflow import fixture_intake, login, payload

from app.integrations.gnani import GnaniError
from app.integrations.tts import TimbreClient
from app.main import app


def test_numeric_confirmation_is_not_human_confirmation(accounts):
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        body = payload(fixture_intake())
        body["confirmed"] = 1
        result = client.post(
            "/api/v1/work-orders", json=body, headers={**headers, "Idempotency-Key": str(uuid4())}
        )
        assert result.status_code == 422


def test_tts_failure_keeps_order_saved(accounts, monkeypatch):
    async def fail(*args, **kwargs):
        raise GnaniError("TTS_UNAVAILABLE", 503)

    monkeypatch.setattr(TimbreClient, "synthesize", fail)
    monkeypatch.setenv("GNANI_TTS_ENABLED", "true")
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        created = client.post(
            "/api/v1/work-orders",
            json=payload(fixture_intake()),
            headers={**headers, "Idempotency-Key": str(uuid4())},
        )
        oid = created.json()["id"]
        failed = client.post(
            "/api/v1/work-orders/" + oid + "/acknowledgment-audio", headers=headers
        )
        assert failed.status_code == 503
        saved = client.get("/api/v1/work-orders/" + oid, headers=headers).json()
        assert saved["id"] == oid and saved["version"] == 1 and len(saved["audit"]) == 1


def test_body_limit_before_parsing(accounts):
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        result = client.post(
            "/api/v1/intakes/transcribe",
            content=b"",
            headers={**headers, "Content-Length": str(20_000_000)},
        )
        assert result.status_code == 413


def test_successful_tts_body_is_delivered_as_binary(accounts, monkeypatch):
    from test_intakes import wav

    expected = wav()

    async def success(*args, **kwargs):
        return expected

    monkeypatch.setattr(TimbreClient, "synthesize", success)
    monkeypatch.setenv("GNANI_TTS_ENABLED", "true")
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        created = client.post(
            "/api/v1/work-orders",
            json=payload(fixture_intake()),
            headers={**headers, "Idempotency-Key": str(uuid4())},
        )
        result = client.post(
            "/api/v1/work-orders/" + created.json()["id"] + "/acknowledgment-audio", headers=headers
        )
        assert result.status_code == 200
        assert result.headers["content-type"] == "audio/wav"
        assert result.content == expected
