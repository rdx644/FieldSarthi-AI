"""IMP-05 regression: durable STT admission must work with one free DB slot."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from test_intakes import wav
from test_workflow import login

from app.db.models import Intake, ProviderAdmission
from app.db.session import engine, get_db
from app.integrations.gnani import Transcription
from app.main import app
from app.routers import intakes
from app.seed import stable
from app.services import provider_admission


def test_stt_releases_request_connection_before_durable_admission(accounts, monkeypatch):
    assert engine.url.database == "fieldsaarthi_test", "Never use a non-test database"
    restricted_engine = create_engine(
        engine.url,
        pool_size=1,
        max_overflow=0,
        pool_timeout=0.2,
        hide_parameters=True,
    )
    restricted_sessions = sessionmaker(restricted_engine, expire_on_commit=False)
    provider_calls = []
    actor_id = stable(accounts[0]["email"])

    def restricted_db():
        with restricted_sessions() as db:
            yield db

    async def fixture(audio, language_code, correlation_id):
        provider_calls.append(correlation_id)
        return Transcription(
            success=True,
            transcript="block b water pump leak urgent",
            request_id="TEST-ONLY-STT-POOL",
            model="prisma-v2.5",
            correlation_id=correlation_id,
            language_code=language_code,
            http_status=200,
            elapsed_seconds=0.01,
        )

    previous_override = app.dependency_overrides.get(get_db)
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    monkeypatch.setattr(provider_admission, "SessionLocal", restricted_sessions)
    monkeypatch.setattr(intakes.speech, "transcribe", fixture)
    app.dependency_overrides[get_db] = restricted_db
    try:
        with TestClient(app) as client:
            headers = login(client, accounts[0])
            result = client.post(
                "/api/v1/intakes/transcribe",
                headers=headers,
                files={"audio_file": ("test-only.wav", wav(), "audio/wav")},
            )
            assert result.status_code == 201, result.text
            assert result.json()["status"] == "READY_FOR_REVIEW"
        assert len(provider_calls) == 1
        with restricted_sessions() as db:
            admissions = list(db.scalars(select(ProviderAdmission)))
            assert len(admissions) == 1
            assert admissions[0].actor_id == actor_id
            assert admissions[0].operation == "STT"
            intake = db.scalar(select(Intake))
            assert intake is not None
            assert intake.reporter_id == actor_id
            assert intake.provider_request_id == "TEST-ONLY-STT-POOL"
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override
        restricted_engine.dispose()
