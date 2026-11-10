"""FR-07/13..18: explicit correction recovery, never a new live ASR score.

CI uses synthetic fixtures. FIELD_SAARTHI_REPLAY_RESULTS optionally replays the
private cached development transcripts inside the isolated test database only.
"""

import json
import os
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from test_intakes import wav
from test_workflow import login

from app.db.models import Audit, Intake, Order
from app.db.session import SessionLocal
from app.integrations.gnani import Transcription
from app.main import app
from app.routers import intakes
from app.seed import stable


@pytest.mark.parametrize("case_id", ["NLP-04", "NLP-12", "NLP-14"])
def test_asr_failure_recovers_with_explicit_review(accounts, monkeypatch, case_id):
    root = Path(__file__).resolve().parents[3]
    case = next(
        c
        for c in json.loads((root / "docs/tests/audio-cases.json").read_text(encoding="utf-8"))
        if c["case_id"] == case_id
    )
    raw = {
        "NLP-04": "water pump on unrecognized floor is leaking",
        "NLP-12": "air conditioner at unrecognized ground floor is broken and urgent",
        "NLP-14": "Warehouse C has an unrecognized equipment problem",
    }[case_id]
    replay = os.getenv("FIELD_SAARTHI_REPLAY_RESULTS")
    cached = None
    if replay:
        cached = json.loads((Path(replay) / (case_id + ".json")).read_text(encoding="utf-8"))
        assert cached["state"] == "complete" and not cached.get("error_code")
        assert cached["complete_case_correct"] is False
        assert cached["expected"] == case["expected"]
        raw = cached["raw_transcript"]
    calls = []

    async def fixture(audio, language, correlation):
        calls.append(correlation)
        return Transcription(
            success=True,
            transcript=raw,
            request_id="TEST-ONLY-REPLAY-" + case_id,
            model="prisma-v2.5",
            correlation_id=correlation,
            language_code=language,
            http_status=200,
            elapsed_seconds=0.01,
        )

    monkeypatch.setattr(intakes.speech, "transcribe", fixture)
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        response = client.post(
            "/api/v1/intakes/transcribe",
            headers=headers,
            files={"audio_file": ("test-only.wav", wav(), "audio/wav")},
            data={"language_code": case["language_code"]},
        )
        assert response.status_code == 201
        intake = response.json()
        iid = intake["intake_id"]
        assert intake["unresolved_fields"]
        assert client.get("/api/v1/work-orders", headers=headers).json()["total"] == 0
        # Editing the transcript alone never auto-confirms or fabricates catalog facts.
        corrected = client.patch(
            f"/api/v1/intakes/{iid}",
            headers=headers,
            json={"edited_transcript": case["script"]},
        )
        assert corrected.status_code == 200
        assert corrected.json()["raw_transcript"] == raw
        assert corrected.json()["suggested_fields"] == intake["suggested_fields"]
        truth = case["expected"]
        body = {
            "intake_id": iid,
            "location_id": stable(truth["location_code"]),
            "asset_id": stable(truth["asset_code"]),
            "issue_category": truth["issue_category"],
            "priority_suggestion": truth["priority_suggestion"],
            "description": case["script"],
            "edited_transcript": case["script"],
            "confirmed": False,
        }
        create_headers = {**headers, "Idempotency-Key": str(uuid4())}
        assert (
            client.post("/api/v1/work-orders", headers=create_headers, json=body).status_code == 422
        )
        body["confirmed"] = True
        saved = client.post("/api/v1/work-orders", headers=create_headers, json=body)
        assert saved.status_code == 201
        order = saved.json()
        repeat = client.post("/api/v1/work-orders", headers=create_headers, json=body)
        assert repeat.status_code == 200 and repeat.json()["id"] == order["id"]
        detail = client.get("/api/v1/work-orders/" + order["id"], headers=headers).json()
        for field in [
            "location_id",
            "asset_id",
            "issue_category",
            "priority_suggestion",
            "description",
        ]:
            assert detail[field] == body[field]
        assert detail["intake"]["raw_transcript"] == raw
        assert detail["intake"]["edited_transcript"] == case["script"]
        assert detail["intake"]["provider"] == intake["provider"]
        assert detail["intake"]["suggested_fields"] == intake["suggested_fields"]
        assert detail["audit"][0]["details"]["human_confirmed"] is True
        assert detail["audit"][0]["details"]["edited_transcript"] == case["script"]
        assert (
            client.patch(
                f"/api/v1/intakes/{iid}",
                headers=headers,
                json={"edited_transcript": "Changed after confirmation"},
            ).status_code
            == 409
        )
    assert len(calls) == 1
    with SessionLocal() as db:
        assert len(list(db.scalars(select(Order)))) == 1
        assert len(list(db.scalars(select(Audit)))) == 1
        assert db.get(Intake, iid).raw_transcript == raw
    if cached:
        # Sanitized output is opt-in and private; source ASR evidence stays unchanged.
        destination = root / "private/asr-recovery" / (case_id + ".json")
        destination.parent.mkdir(exist_ok=True)
        destination.write_text(
            json.dumps(
                {
                    "case_id": case_id,
                    "passed": True,
                    "kind": "cached_asr_test_database_replay",
                    "original_provider_request_id": cached["provider_request_id"],
                    "explicit_correction": True,
                    "original_preserved": True,
                    "confirmation_required": True,
                    "idempotent": True,
                    "live_provider_calls": 0,
                    "hosted_database_writes": 0,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
