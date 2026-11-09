"""Evaluation tooling only; synthetic fixtures are not authentic speech results."""

import json

import pytest

from app.core.config import ROOT
from scripts.evaluate_audio import compare, preflight, summary


def test_wrong_extraction_and_unblocked_ambiguity_cannot_pass():
    case = {
        "expected": {
            "location_code": None,
            "asset_code": None,
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
        "must_block": True,
    }
    extraction = {
        "suggested_fields": {
            "location_id": None,
            "asset_id": None,
            "issue_category": "ELECTRICAL",
            "priority_suggestion": "NORMAL",
        },
        "unresolved_fields": ["asset_id", "location_id"],
    }
    result = compare(case, extraction)
    assert result["complete_case_correct"] is False
    assert result["field_correct"]["issue_category"] is False
    assert result["safety_blocked"] is True


def test_silence_requires_actual_no_speech_error():
    case = {"expected_error": "NO_SPEECH_DETECTED", "must_block": True}
    assert compare(case, {}, "NO_SPEECH_DETECTED")["complete_case_correct"] is True
    assert compare(case, {}, "GNANI_TIMEOUT")["complete_case_correct"] is False
    assert compare(case, {}, None)["complete_case_correct"] is False


def test_summary_requires_fifteen_and_all_safety_cases():
    results = [
        {
            "case_id": f"NLP-{index:02}",
            "complete_case_correct": True,
            "field_correct": {},
            "safety_blocked": True,
            "must_block": True,
        }
        for index in range(1, 16)
    ]
    assert summary(results)["target_passed"] is True
    assert summary(results[:14])["target_passed"] is False
    results[-1]["safety_blocked"] = False
    assert summary(results)["target_passed"] is False


def test_duplicate_normalized_recordings_are_rejected(tmp_path):
    import io
    import wave

    target = io.BytesIO()
    with wave.open(target, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b"\0\0" * 16000)
    cases = json.loads((ROOT / "docs/tests/audio-cases.json").read_text(encoding="utf-8"))
    for case in cases:
        case["file"] = case["case_id"] + ".wav"
        (tmp_path / case["file"]).write_bytes(target.getvalue())
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(cases), encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate normalized recording"):
        preflight(manifest)


def test_safety_uses_actual_required_fields_and_not_metadata():
    case = {
        "expected": {
            "location_code": "BLK-B-F2",
            "asset_code": "PUMP-B02",
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
        "must_block": True,
    }
    from app.seed import stable

    extraction = {
        "suggested_fields": {
            "location_id": stable("BLK-B-F2"),
            "asset_id": stable("PUMP-B02"),
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
        "unresolved_fields": ["asset_id"],
    }
    assert compare(case, extraction)["safety_blocked"] is False
    assert compare(case, extraction)["complete_case_correct"] is False
    assert compare(case, {}, "GNANI_TIMEOUT")["safety_blocked"] is False


def test_manifest_cannot_remove_required_safety_cases(tmp_path):
    cases = json.loads((ROOT / "docs/tests/audio-cases.json").read_text(encoding="utf-8"))
    del cases[6]["must_block"]
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps(cases), encoding="utf-8")
    with pytest.raises(ValueError, match="required safety cases"):
        preflight(manifest)


def test_paid_response_survives_parser_failure_without_repeating_call(tmp_path, monkeypatch):
    import asyncio
    from contextlib import nullcontext
    from types import SimpleNamespace

    from scripts import evaluate_audio

    calls = []

    class Speech:
        def __init__(self, *args, **kwargs):
            pass

        async def transcribe(self, *args):
            calls.append(True)
            return SimpleNamespace(
                transcript="test-only transcript",
                model="prisma-v2.5",
                request_id="TEST-ONLY-response",
                elapsed_seconds=0.01,
            )

    monkeypatch.setattr(evaluate_audio, "GnaniSpeechClient", Speech)
    monkeypatch.setattr(evaluate_audio, "SessionLocal", lambda: nullcontext(None))

    def fail(*args):
        raise RuntimeError("test-only parser failure after paid result")

    monkeypatch.setattr(evaluate_audio, "extract", fail)
    case = {
        "case_id": "NLP-07",
        "language_code": "en-IN",
        "must_block": True,
        "expected": {
            "location_code": None,
            "asset_code": None,
            "issue_category": "OTHER",
            "priority_suggestion": "NORMAL",
        },
    }
    prepared = [(case, b"test-only", 1.0, "test-digest")]
    with pytest.raises(RuntimeError, match="parser failure"):
        asyncio.run(evaluate_audio.evaluate(prepared, tmp_path))
    stored = json.loads((tmp_path / "results/NLP-07.json").read_text())
    assert stored["provider_request_id"] == "TEST-ONLY-response"
    assert stored["state"] == "provider_complete"
    monkeypatch.setattr(
        evaluate_audio,
        "extract",
        lambda *args: {
            "suggested_fields": {
                "location_id": None,
                "asset_id": None,
                "issue_category": "OTHER",
                "priority_suggestion": "NORMAL",
            }
        },
    )
    assert (
        asyncio.run(evaluate_audio.evaluate(prepared, tmp_path))[0]["complete_case_correct"] is True
    )
    assert len(calls) == 1
