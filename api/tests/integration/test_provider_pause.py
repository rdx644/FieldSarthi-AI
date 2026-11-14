"""NFR-13: operator can pause billable audio while saved workflows stay available."""

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from test_intakes import wav
from test_workflow import fixture_intake, login, payload

from app.db.models import ProviderAdmission
from app.db.session import SessionLocal
from app.main import app
from app.routers import intakes, orders


def test_paused_stt_never_decodes_or_reserves(accounts, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Paused STT must not decode, reserve or call a provider")

    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "false")
    monkeypatch.setattr(intakes, "normalize_audio", forbidden)
    monkeypatch.setattr(intakes.provider_budget, "check", forbidden)
    monkeypatch.setattr(intakes.speech, "transcribe", forbidden)
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        response = client.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("corrupt.wav", b"not audio", "audio/wav")},
        )
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "GNANI_REQUESTS_PAUSED"
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(ProviderAdmission)) == 0


def test_provider_pause_blocks_stt_tts_and_preserves_saved_work(accounts, monkeypatch):
    async def forbidden(*args, **kwargs):
        raise AssertionError("Paused provider must never be called")

    monkeypatch.setattr(intakes.speech, "transcribe", forbidden)
    monkeypatch.setattr(orders.TimbreClient, "synthesize", forbidden)
    monkeypatch.setenv("GNANI_TTS_ENABLED", "true")
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "false")
    with TestClient(app) as c:
        headers = login(c, accounts[0])
        iid = fixture_intake()
        saved = c.post(
            "/api/v1/work-orders",
            headers={**headers, "Idempotency-Key": "pause-test-key"},
            json=payload(iid),
        )
        assert saved.status_code == 201
        oid = saved.json()["id"]
        before = c.get("/api/v1/work-orders/" + oid, headers=headers).json()
        stt = c.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("test.wav", wav(), "audio/wav")},
        )
        tts = c.post(f"/api/v1/work-orders/{oid}/acknowledgment-audio", headers=headers)
        for response in [stt, tts]:
            assert response.status_code == 503
            assert response.json()["error"]["code"] == "GNANI_REQUESTS_PAUSED"
        assert (
            c.get("/api/v1/work-orders/capabilities/audio", headers=headers).json()["tts_enabled"]
            is False
        )
        assert c.get("/api/v1/work-orders/" + oid, headers=headers).json() == before
        manual = c.post(
            "/api/v1/intakes/manual", headers=headers, json={"text": "Block B pump leak"}
        )
        assert manual.status_code == 201 and manual.json()["provider"] is None
        assert c.get("/health/ready").status_code == 200
        monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
        assert (
            c.get("/api/v1/work-orders/capabilities/audio", headers=headers).json()["tts_enabled"]
            is True
        )
