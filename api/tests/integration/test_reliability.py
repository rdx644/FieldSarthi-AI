"""NFR-01: ten consecutive full API workflows using TEST-ONLY STT responses."""

from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from test_intakes import wav
from test_workflow import login

from app.db.models import Audit, Order
from app.db.session import SessionLocal
from app.integrations.gnani import Transcription
from app.main import app
from app.routers import intakes
from app.seed import stable


def test_ten_consecutive_voice_to_resolved_workflows(accounts, monkeypatch):
    calls = []

    async def test_only_speech(audio, language, correlation):
        calls.append(correlation)
        return Transcription(
            success=True,
            transcript="Block B water pump leak urgent",
            request_id="TEST-ONLY-" + correlation,
            model="prisma-v2.5",
            correlation_id=correlation,
            language_code=language,
            http_status=200,
            elapsed_seconds=0.01,
        )

    monkeypatch.setattr(intakes.speech, "transcribe", test_only_speech)
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        supervisor = login(client, accounts[2])
        ids = set()
        for index in range(10):
            response = client.post(
                "/api/v1/intakes/transcribe",
                headers=worker,
                files={"audio_file": ("test-only.wav", wav(), "audio/wav")},
                data={"language_code": "en-IN"},
            )
            assert response.status_code == 201, f"run {index + 1}: {response.status_code}"
            intake = response.json()
            assert intake["status"] == "READY_FOR_REVIEW"
            assert client.get("/api/v1/work-orders", headers=worker).json()["total"] == index
            correction = "Reviewed synthetic pump report " + str(index)
            assert (
                client.patch(
                    "/api/v1/intakes/" + intake["id"],
                    headers=worker,
                    json={"edited_transcript": correction},
                ).status_code
                == 200
            )
            body = {
                "intake_id": intake["id"],
                **intake["suggested_fields"],
                "description": correction,
                "edited_transcript": correction,
                "confirmed": True,
            }
            headers = {**worker, "Idempotency-Key": str(uuid4())}
            created = client.post("/api/v1/work-orders", headers=headers, json=body)
            assert created.status_code == 201
            oid = created.json()["id"]
            ids.add(oid)
            replay = client.post("/api/v1/work-orders", headers=headers, json=body)
            assert replay.status_code == 200 and replay.json()["id"] == oid
            for endpoint, command in [
                (
                    "assignment",
                    {"assignee_id": stable("worker2@fieldsaarthi.demo"), "expected_version": 1},
                ),
                ("priority", {"priority": "HIGH", "expected_version": 2}),
                ("status", {"status": "IN_PROGRESS", "expected_version": 3}),
                (
                    "status",
                    {
                        "status": "RESOLVED",
                        "resolution_note": "Synthetic seal replacement",
                        "expected_version": 4,
                    },
                ),
            ]:
                assert (
                    client.patch(
                        "/api/v1/work-orders/" + oid + "/" + endpoint,
                        headers=supervisor,
                        json=command,
                    ).status_code
                    == 200
                )
            detail = client.get("/api/v1/work-orders/" + oid, headers=worker).json()
            assert detail["status"] == "RESOLVED" and detail["version"] == 5
            assert len(detail["audit"]) == 5
            assert detail["intake"]["provider"]["request_id"].startswith("TEST-ONLY-")
        assert len(ids) == len(set(calls)) == 10
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Order)) == 10
        assert db.scalar(select(func.count()).select_from(Audit)) == 50
