import io
import wave

from fastapi.testclient import TestClient
from sqlalchemy import select
from test_workflow import login

from app.db.models import Intake, Order
from app.db.session import SessionLocal
from app.integrations.gnani import GnaniError, Transcription
from app.main import app
from app.routers import intakes


def wav(seconds=1):
    target = io.BytesIO()
    with wave.open(target, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\0\0" * int(16000 * seconds))
    return target.getvalue()


def test_upload_provider_failure_creates_no_order(accounts, monkeypatch):
    async def fail(*args, **kwargs):
        raise GnaniError("GNANI_QUOTA_EXHAUSTED", 402)

    monkeypatch.setattr(intakes.speech, "transcribe", fail)
    with TestClient(app) as c:
        headers = login(c, accounts[0])
        r = c.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("x.wav", wav(), "audio/wav")},
            data={"language_code": "hi-IN"},
        )
        assert r.status_code == 503
        assert r.json()["error"]["code"] == "GNANI_QUOTA_EXHAUSTED"
    with SessionLocal() as db:
        assert list(db.scalars(select(Order))) == []
        row = db.scalar(select(Intake))
        assert row.status == "FAILED" and row.raw_transcript is None


def test_corrupt_and_long_audio_never_calls_provider(accounts, monkeypatch):
    async def forbidden(*args, **kwargs):
        raise AssertionError("Provider must not be called")

    monkeypatch.setattr(intakes.speech, "transcribe", forbidden)
    with TestClient(app) as c:
        headers = login(c, accounts[0])
        for audio, expected in [(b"corrupt", 400), (b"RIFFcorrupt", 400), (wav(31), 422)]:
            r = c.post(
                "/api/v1/intakes/transcribe",
                headers=headers,
                files={"audio_file": ("x.wav", audio, "audio/wav")},
            )
            assert r.status_code == expected, r.text


def test_transcription_is_ready_for_review_only_and_preserves_raw(accounts, monkeypatch):
    async def fixture(*args, **kwargs):
        return Transcription(
            success=True,
            transcript="block b water pump leak urgent",
            request_id="TEST-ONLY-FIXTURE",
            model="prisma-v2.5",
            correlation_id="fixture",
            language_code="hi-IN",
            http_status=200,
            elapsed_seconds=0.1,
        )

    monkeypatch.setattr(intakes.speech, "transcribe", fixture)
    with TestClient(app) as c:
        headers = login(c, accounts[0])
        r = c.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("x.wav", wav(), "audio/wav")},
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["status"] == "READY_FOR_REVIEW" and body["suggested_fields"]["asset_id"]
        assert c.get("/api/v1/work-orders", headers=headers).json()["total"] == 0


def test_cookie_refresh_and_csrf_guard(accounts):
    with TestClient(app) as c:
        login(c, accounts[0])
        assert c.get("/api/v1/me").status_code == 200
        result = c.post("/api/v1/auth/logout", headers={"Origin": "https://evil.invalid"})
        assert result.status_code == 403
        assert c.get("/api/v1/me").status_code == 200
        result = c.post(
            "/api/v1/auth/logout",
            headers={"Origin": "http://testserver", "X-Requested-With": "FieldSaarthi"},
        )
        assert result.status_code == 200
        assert c.get("/api/v1/me").status_code == 401
