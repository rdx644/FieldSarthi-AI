import json

from fastapi.testclient import TestClient
from test_intakes import wav
from test_workflow import login

from app.integrations.gnani import GnaniError, Transcription
from app.main import app, logger
from app.routers import intakes


def test_stages_correlate_without_audio_transcript_or_credentials(accounts, monkeypatch, caplog):
    async def response(audio, language, correlation):
        return Transcription(
            success=True,
            transcript="DO-NOT-LOG-TRANSCRIPT block b pump leak",
            request_id="TEST-ONLY-provider-id",
            model="prisma-v2.5",
            correlation_id=correlation,
            language_code=language,
            http_status=200,
            elapsed_seconds=0.01,
        )

    monkeypatch.setattr(intakes.speech, "transcribe", response)
    logger.addHandler(caplog.handler)
    try:
        with TestClient(app) as client:
            headers = login(client, accounts[0])
            result = client.post(
                "/api/v1/intakes/transcribe",
                headers=headers,
                files={"audio_file": ("test.wav", wav(), "audio/wav")},
            )
            assert result.status_code == 201
        events = [
            json.loads(record.message) for record in caplog.records if record.name == "fieldsaarthi"
        ]
        stages = [entry for entry in events if entry["event"] == "stage_completed"]
        assert [entry["stage"] for entry in stages] == [
            "audio_normalize",
            "provider_stt",
            "extraction",
        ]
        assert all(entry["request_id"] == result.headers["X-Request-ID"] for entry in stages)
        assert all(entry["elapsed_ms"] >= 0 for entry in stages)
        assert "DO-NOT-LOG-TRANSCRIPT" not in json.dumps(events)
        assert accounts[0]["password"] not in json.dumps(events)
    finally:
        logger.removeHandler(caplog.handler)


def test_provider_failure_has_actionable_message_and_stage_code(accounts, monkeypatch):
    async def failure(*args, **kwargs):
        raise GnaniError("GNANI_AUTH_FAILURE", 401)

    monkeypatch.setattr(intakes.speech, "transcribe", failure)
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        response = client.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("test.wav", wav(), "audio/wav")},
        )
        assert response.status_code == 503
        assert "operator attention" in response.json()["error"]["message"]
