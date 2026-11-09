import asyncio
import hashlib
import json
from contextlib import nullcontext

import pytest

from scripts import evaluate_audio


def test_acknowledged_timeout_stays_failed_and_is_not_sent_again(tmp_path, monkeypatch):
    class Speech:
        def __init__(self, *args, **kwargs):
            pass

        async def transcribe(self, *args):
            raise AssertionError("A cached timeout must not be sent again")

    monkeypatch.setenv("GNANI_API_KEY_ID", "test-only-placeholder")
    monkeypatch.setattr(evaluate_audio, "GnaniSpeechClient", Speech)
    monkeypatch.setattr(evaluate_audio, "SessionLocal", lambda: nullcontext(None))
    case = {
        "case_id": "NLP-02",
        "language_code": "hi-IN",
        "expected": {
            "location_code": "BLK-B-F2",
            "asset_code": "PUMP-B02",
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
    }
    result = {
        "case_id": "NLP-02",
        "audio_sha256": "test-audio-digest",
        "ground_truth_sha256": hashlib.sha256(
            json.dumps(case, sort_keys=True).encode()
        ).hexdigest(),
        "parser_version": evaluate_audio.PARSER_VERSION,
        "state": "complete",
        "error_code": "GNANI_TIMEOUT",
        "complete_case_correct": False,
        "safety_blocked": False,
        "field_correct": {"asset_code": False},
    }
    evaluate_audio.save(tmp_path / "results/NLP-02.json", result)
    prepared = [(case, b"test-only-audio", 1.0, "test-audio-digest")]
    with pytest.raises(ValueError, match="Cached provider failure"):
        asyncio.run(evaluate_audio.evaluate(prepared, tmp_path))
    results = asyncio.run(evaluate_audio.evaluate(prepared, tmp_path, {"NLP-02"}))
    assert results[0]["complete_case_correct"] is False
    assert (
        evaluate_audio.summary(results)["correction_confusion"]["unassessed_provider_errors"] == 1
    )
