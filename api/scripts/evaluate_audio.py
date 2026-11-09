"""WBS-07.3: distinct, consented human recordings through genuine Gnani, never fixtures.

Prepare/preflight is free. Live runs require explicit consent/ground-truth flags,
disable retries, and checkpoint each response privately to avoid repeated spending.
"""

import argparse
import asyncio
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import httpx

from app.core.config import ROOT
from app.db.session import SessionLocal
from app.integrations.gnani import GnaniError, GnaniSpeechClient
from app.seed import stable
from app.services.audio import MAX_BYTES, normalize_audio
from app.services.extraction import PARSER_VERSION, extract

FIELDS = ["location_code", "asset_code", "issue_category", "priority_suggestion"]
SAFETY_CASES = {"NLP-07", "NLP-08", "NLP-09", "NLP-10", "NLP-11", "NLP-15"}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def prepare(folder):
    cases = json.loads((ROOT / "docs/tests/audio-cases.json").read_text(encoding="utf-8"))
    manifest = folder / "manifest.json"
    if not manifest.exists():
        for case in cases:
            case.update(
                file=case["case_id"] + ".wav", accent_or_code_mix="", noise_condition="quiet"
            )
        save(manifest, cases)
    return manifest


def preflight(manifest):
    cases = json.loads(manifest.read_text(encoding="utf-8"))
    if {case["case_id"] for case in cases} != {f"NLP-{index:02}" for index in range(1, 16)} or len(
        cases
    ) != 15:
        raise ValueError("Exactly NLP-01 through NLP-15 are required.")
    for case in cases:
        if case["case_id"] in SAFETY_CASES and case.get("must_block") is not True:
            raise ValueError("The required safety cases must retain must_block=true.")
        if (case["case_id"] == "NLP-15") != (case.get("expected_error") == "NO_SPEECH_DETECTED"):
            raise ValueError("Only NLP-15 is the required no-speech case.")
        if case["case_id"] != "NLP-15" and case.get("expected_error"):
            raise ValueError("Speech cases require fields rather than a provider error.")
    folder = manifest.parent.resolve()
    seen = set()
    prepared = []
    for case in cases:
        path = (folder / case["file"]).resolve()
        if not path.is_relative_to(folder) or not path.is_file():
            raise ValueError(f"Missing private recording for {case['case_id']}.")
        if path.stat().st_size > MAX_BYTES:
            raise ValueError(f"Recording too large for {case['case_id']}.")
        normalized, duration = normalize_audio(path.read_bytes())
        digest = hashlib.sha256(normalized).hexdigest()
        if digest in seen:
            raise ValueError(
                "Duplicate normalized recording: each case needs a distinct recording."
            )
        seen.add(digest)
        if case["language_code"] not in {"hi-IN", "en-IN", "ta-IN"}:
            raise ValueError("Invalid language selection.")
        if case.get("expected_error") != "NO_SPEECH_DETECTED" and set(
            case.get("expected", {})
        ) != set(FIELDS):
            raise ValueError("Every speech case needs reviewed ground truth for all four fields.")
        prepared.append((case, normalized, duration, digest))
    return prepared


def compare(case, extraction, error=None):
    if case.get("expected_error"):
        passed = error == case["expected_error"]
        return {"complete_case_correct": passed, "safety_blocked": passed, "field_correct": {}}
    if error:
        return {"complete_case_correct": False, "safety_blocked": False, "field_correct": {}}
    observed = extraction.get("suggested_fields", {})
    expected = case["expected"]
    correct = {
        "location_code": observed.get("location_id")
        == (stable(expected["location_code"]) if expected["location_code"] else None),
        "asset_code": observed.get("asset_id")
        == (stable(expected["asset_code"]) if expected["asset_code"] else None),
        "issue_category": observed.get("issue_category") == expected["issue_category"],
        "priority_suggestion": observed.get("priority_suggestion")
        == expected["priority_suggestion"],
    }
    # An outage prevents creation but does not prove parser ambiguity safety.
    blocked = not error and (not observed.get("location_id") or not observed.get("asset_id"))
    return {
        "complete_case_correct": not error
        and all(correct.values())
        and (not case.get("must_block") or blocked),
        "safety_blocked": blocked,
        "field_correct": correct,
    }


async def evaluate(prepared, folder, acknowledged_failures=()):
    import os

    async with httpx.AsyncClient(follow_redirects=False) as http:
        client = GnaniSpeechClient(os.environ["GNANI_API_KEY_ID"], http=http, retries=0)
        return await evaluate_cases(client, prepared, folder, acknowledged_failures)


async def evaluate_cases(client, prepared, folder, acknowledged_failures=()):
    results = []
    with SessionLocal() as db:
        for case, audio, duration, digest in prepared:
            checkpoint = folder / "results" / (case["case_id"] + ".json")
            truth_digest = hashlib.sha256(json.dumps(case, sort_keys=True).encode()).hexdigest()
            if checkpoint.exists():
                result = json.loads(checkpoint.read_text(encoding="utf-8"))
                if (
                    result["audio_sha256"] != digest
                    or result["ground_truth_sha256"] != truth_digest
                ):
                    raise ValueError(
                        "Recording/labels changed. Archive the live results before rerunning."
                    )
                if result.get("state") != "complete" or result["parser_version"] != PARSER_VERSION:
                    extraction = extract(result.get("raw_transcript") or "", db)
                    result.update(
                        extraction=extraction,
                        parser_version=PARSER_VERSION,
                        state="complete",
                        **compare(case, extraction, result.get("error_code")),
                    )
                    save(checkpoint, result)
                result["expected"] = case.get("expected")
                if result.get("error_code"):
                    result.update(compare(case, result.get("extraction", {}), result["error_code"]))
                save(checkpoint, result)
                results.append(result)
                if (
                    result.get("error_code") not in {None, "NO_SPEECH_DETECTED"}
                    and case["case_id"] not in acknowledged_failures
                ):
                    raise ValueError(
                        "Cached provider failure. Fix access and archive that case before retrying."
                    )
                continue
            result = {
                "case_id": case["case_id"],
                "audio_sha256": digest,
                "ground_truth_sha256": truth_digest,
                "audio_duration_seconds": duration,
                "parser_version": PARSER_VERSION,
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "language_code": case["language_code"],
                "must_block": case.get("must_block", False),
                "expected": case.get("expected"),
            }
            extraction = {}
            error = None
            try:
                response = await client.transcribe(audio, case["language_code"], str(uuid4()))
                result.update(
                    raw_transcript=response.transcript,
                    provider_model=response.model,
                    provider_request_id=response.request_id,
                    stt_latency_ms=round(response.elapsed_seconds * 1000),
                    state="provider_complete",
                )
                # Preserve the billable result before catalog/parser work can fail.
                save(checkpoint, result)
                extraction = extract(response.transcript, db)
            except GnaniError as exc:
                error = exc.code
                result["error_code"] = error
                result["state"] = "provider_complete"
                save(checkpoint, result)
            result.update(
                extraction=extraction, state="complete", **compare(case, extraction, error)
            )
            save(checkpoint, result)
            results.append(result)
            print(case["case_id"], "PASS" if result["complete_case_correct"] else "FAIL")
            # Configuration/outage failures are not 15 separately useful paid requests.
            if error and error != "NO_SPEECH_DETECTED":
                raise ValueError(
                    "Provider failure recorded privately. Stop and inspect before spending more."
                )
    return results


def summary(results):
    complete = sum(result["complete_case_correct"] for result in results)
    field_counts = {
        field: {
            "correct": sum(
                result["field_correct"].get(field, False)
                for result in results
                if not result.get("error_code")
            ),
            "total": sum(
                field in result["field_correct"]
                for result in results
                if not result.get("error_code")
            ),
        }
        for field in FIELDS
    }
    safety_results = [result for result in results if result["case_id"] in SAFETY_CASES]
    safe = {result["case_id"] for result in safety_results} == SAFETY_CASES and all(
        result["safety_blocked"] for result in safety_results
    )
    correction = {
        "expected_and_blocked": 0,
        "expected_but_not_blocked": 0,
        "not_expected_but_blocked": 0,
        "not_expected_and_not_blocked": 0,
        "unassessed_provider_errors": 0,
    }
    missing = {
        field: {
            "expected_missing_and_missing": 0,
            "expected_missing_but_populated": 0,
            "expected_present_but_missing": 0,
            "expected_present_and_populated": 0,
        }
        for field in ["location_id", "asset_id"]
    }
    for result in results:
        error = result.get("error_code")
        if error and not (result["case_id"] == "NLP-15" and error == "NO_SPEECH_DETECTED"):
            correction["unassessed_provider_errors"] += 1
            continue
        expected_block = result["case_id"] in SAFETY_CASES
        blocked = result["safety_blocked"]
        key = (
            ("expected_and_blocked" if blocked else "expected_but_not_blocked")
            if expected_block
            else ("not_expected_but_blocked" if blocked else "not_expected_and_not_blocked")
        )
        correction[key] += 1
        if not result.get("expected") or error:
            continue
        for field, label in [("location_id", "location_code"), ("asset_id", "asset_code")]:
            expected_missing = result["expected"][label] is None
            observed_missing = (
                not result.get("extraction", {}).get("suggested_fields", {}).get(field)
            )
            key = (
                (
                    "expected_missing_and_missing"
                    if observed_missing
                    else "expected_missing_but_populated"
                )
                if expected_missing
                else (
                    "expected_present_but_missing"
                    if observed_missing
                    else "expected_present_and_populated"
                )
            )
            missing[field][key] += 1
    return {
        "evaluation_kind": "genuine_gnani_distinct_human_recordings",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "sample_count": len(results),
        "complete_cases_correct": complete,
        "per_field": field_counts,
        "correction_confusion": correction,
        "required_field_missing_confusion": missing,
        "selected_language_codes": sorted(
            {result["language_code"] for result in results if result.get("language_code")}
        ),
        "failing_cases": [
            {
                "case_id": result["case_id"],
                "incorrect_fields": [
                    field for field, correct in result["field_correct"].items() if not correct
                ],
                "error_code": result.get("error_code"),
            }
            for result in results
            if not result["complete_case_correct"]
        ],
        "all_required_ambiguities_blocked": safe,
        "target_passed": len(results) == 15 and complete >= 12 and safe,
        "parser_version": PARSER_VERSION,
        "models_observed": sorted(
            {result["provider_model"] for result in results if result.get("provider_model")}
        ),
        "cases": [
            {
                key: value
                for key, value in result.items()
                if key
                in {
                    "case_id",
                    "complete_case_correct",
                    "field_correct",
                    "safety_blocked",
                    "error_code",
                    "provider_model",
                    "provider_request_id",
                    "audio_duration_seconds",
                    "stt_latency_ms",
                }
            }
            for result in results
        ],
        "limitations": (
            "Small team-recorded synthetic corpus; no WER/CER or population accuracy claim. "
            "Raw audio and transcripts remain private."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--consent", action="store_true")
    parser.add_argument("--ground-truth-reviewed", action="store_true")
    parser.add_argument(
        "--acknowledge-failed-case",
        action="append",
        default=[],
        choices=[f"NLP-{index:02}" for index in range(1, 16)],
        help="Keep an inspected cached failure unassessed; never retry or pass it.",
    )
    args = parser.parse_args()
    manifest = args.manifest or prepare(ROOT / "private/evaluation")
    if not manifest.resolve().is_relative_to((ROOT / "private").resolve()):
        parser.error("Keep the manifest and raw results under the ignored private directory.")
    if args.prepare:
        print(
            "Private manifest ready. Record scripts, update extensions and review expected fields."
        )
        return
    prepared = preflight(manifest)
    if not args.live:
        print("15 distinct recordings validated. No provider calls made.")
        return
    if not args.consent or not args.ground_truth_reviewed:
        parser.error("Live evaluation requires --consent and --ground-truth-reviewed.")
    report = summary(asyncio.run(evaluate(prepared, manifest.parent, args.acknowledge_failed_case)))
    save(ROOT / "docs/evidence/audio-evaluation.json", report)
    print("Sanitized results saved to docs/evidence/audio-evaluation.json")
    if not report["target_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
