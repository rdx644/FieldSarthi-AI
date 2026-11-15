"""IMP-04A: hand-computed, synthetic offline metrics; no speech-quality claims."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.score_transcripts import edit_counts, normalize, score_dataset


def dataset(cases=None, split="development", kind="synthetic_fixture"):
    return {
        "schema_version": 1,
        "dataset_id": "TEST-ONLY",
        "split": split,
        "evidence_kind": kind,
        "conditions": {"noise": "test-only"},
        "cases": cases if cases is not None else [case()],
    }


def case(identifier="CASE-01", reference="pump is leaking", language="en-IN"):
    return {
        "case_id": identifier,
        "language_code": language,
        "spoken_language_tags": ["English"],
        "reference_transcript": reference,
        "reference_verified": reference is not None,
        "consent_obtained": True,
        "audio_duration_seconds": 2.0,
        "expected_fields": {
            "location_code": "LOCATION-TEST",
            "asset_code": "PUMP-TEST",
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
        "expected_safety_block": False,
    }


def response(identifier="CASE-01", transcript="pump is leaking", status="success", **extra):
    return {
        "case_id": identifier,
        "provider_status": status,
        "transcript": transcript,
        "parser_version": "rules-test",
        "observed_fields": {
            "location_code": "LOCATION-TEST",
            "asset_code": "PUMP-TEST",
            "issue_category": "LEAKAGE",
            "priority_suggestion": "NORMAL",
        },
        "safety_blocked": False,
        **extra,
    }


def score(manifest=None, responses=None):
    return score_dataset(
        manifest or dataset(), responses or [response()], "TEST-ONLY", "rules-test"
    )


@pytest.mark.parametrize(
    ("reference", "hypothesis", "expected"),
    [
        (["pump"], ["fan"], (1, 0, 0)),
        (["pump", "leaks"], ["pump"], (0, 1, 0)),
        (["pump"], ["pump", "leaks"], (0, 0, 1)),
        ([], ["pump"], (0, 0, 1)),
    ],
)
def test_hand_computed_alignment(reference, hypothesis, expected):
    counts = edit_counts(reference, hypothesis)
    assert (counts["substitutions"], counts["deletions"], counts["insertions"]) == expected


def test_normalization_preserves_scripts_numbers_and_combining_marks():
    assert normalize("  PUMP, 42! café ") == "pump 42 café"
    assert normalize("cafe\u0301") == normalize("café")
    assert normalize("पानी नहीं आ रहा।") == "पानी नहीं आ रहा"
    assert normalize("पानी") != normalize("paani")


def test_micro_average_failures_and_nonempty_denominators_are_distinct():
    manifest = dataset([case("CASE-01"), case("CASE-02", "fan stops")])
    result = score(manifest, [response(), response("CASE-02", "", "failed")])
    assert result["attempted_count"] == 2
    assert result["nonempty_count"] == 1
    assert result["failed_or_empty_count"] == 1
    assert result["coverage"] == 0.5
    end_to_end = result["asr"]["end_to_end"]["wer"]
    assert end_to_end["reference_units"] == 5
    assert end_to_end["deletions"] == 2
    assert end_to_end["rate"] == 0.4
    assert result["asr"]["successful_nonempty"]["wer"]["rate"] == 0
    assert result["automatic_complete_case_count"] == 1
    assert result["per_field"]["asset_code"]["end_to_end"] == {"correct": 1, "total": 2}


def test_empty_success_is_all_deletions_and_wer_can_exceed_one():
    assert score(responses=[response(transcript="")])["asr"]["end_to_end"]["wer"]["rate"] == 1
    result = score(dataset([case(reference="pump")]), [response(transcript="pump is very loud")])
    assert result["asr"]["end_to_end"]["wer"]["rate"] == 3


def test_missing_and_empty_references_are_unmeasured_not_perfect():
    for reference in (None, "", "!!!"):
        result = score(dataset([case(reference=reference)]))
        assert result["asr"]["end_to_end"]["wer"]["rate"] is None
        assert result["asr"]["end_to_end"]["wer"]["reference_units"] == 0


def test_cer_uses_normalized_codepoints_without_whitespace():
    result = score(dataset([case(reference="ab cd")]), [response(transcript="ab xd")])
    metric = result["asr"]["end_to_end"]["cer"]
    assert metric["reference_units"] == 4
    assert metric["substitutions"] == 1
    assert metric["rate"] == 0.25


def test_language_breakdown_retains_selected_and_spoken_language_labels():
    hindi = case("CASE-02", "पानी", "hi-IN")
    hindi["spoken_language_tags"] = ["Hindi", "Hinglish"]
    result = score(dataset([case(), hindi]), [response(), response("CASE-02", "paani")])
    assert result["by_language_code"]["en-IN"]["attempted_count"] == 1
    assert result["by_language_code"]["hi-IN"]["asr"]["end_to_end"]["wer"]["rate"] == 1
    assert result["by_spoken_language_tag"]["Hinglish"]["attempted_count"] == 1


def test_safety_outage_is_unassessed_not_a_successful_block():
    unsafe = case()
    unsafe["expected_safety_block"] = True
    result = score(dataset([unsafe]), [response(status="failed", transcript="")])
    assert result["safety"]["unassessed_provider_failures_or_empty"] == 1
    assert result["safety"]["expected_and_blocked"] == 0
    assert result["automatic_complete_case_count"] == 0
    result = score(dataset([unsafe]), [response()])
    assert result["safety"]["false_accepts"] == 1


@pytest.mark.parametrize("change", ["consent", "split", "duplicate", "reference", "duration"])
def test_private_manifest_rejects_invalid_or_mixed_cases(change):
    manifest = dataset()
    if change == "consent":
        manifest["cases"][0]["consent_obtained"] = False
    elif change == "split":
        manifest["cases"][0]["split"] = "heldout"
    elif change == "duplicate":
        manifest["cases"].append(case())
    elif change == "reference":
        manifest["cases"][0]["reference_verified"] = False
    else:
        manifest["cases"][0]["audio_duration_seconds"] = 31
    with pytest.raises(ValueError):
        score(manifest)


def test_missing_results_cannot_be_silently_dropped_and_parser_version_must_match():
    with pytest.raises(ValueError):
        score(dataset([case(), case("CASE-02")]))
    with pytest.raises(ValueError):
        score(responses=[response(parser_version="other")])


@pytest.mark.parametrize(
    "extra", [{"success": False}, {"error_code": "GNANI_TIMEOUT"}, {"attempted": False}]
)
def test_contradictory_or_unsupported_status_fields_are_rejected(extra):
    with pytest.raises(ValueError):
        score(responses=[response(**extra)])


def test_failed_response_with_nonempty_text_never_earns_success_credit():
    result = score(responses=[response(status="failed", error_code="GNANI_TIMEOUT")])
    assert result["attempted_count"] == 1
    assert result["nonempty_count"] == 0
    assert result["asr"]["end_to_end"]["wer"]["rate"] == 1
    assert result["automatic_complete_case_count"] == 0
    assert result["per_field"]["asset_code"]["end_to_end"] == {"correct": 0, "total": 1}


def test_partial_field_expectations_cannot_inflate_complete_cases():
    partial = case()
    partial["expected_fields"] = {"asset_code": "PUMP-TEST"}
    result = score(dataset([partial]))
    assert result["per_field"]["asset_code"]["end_to_end"] == {"correct": 1, "total": 1}
    assert result["automatic_complete_case_count"] == 0


def test_missing_references_still_count_all_attempts_and_fields():
    result = score(dataset([case(reference=None)]))
    assert result["attempted_count"] == result["missing_verified_reference_count"] == 1
    assert result["coverage"] == 1
    assert result["asr"]["end_to_end"]["wer"]["scored_case_count"] == 0
    assert result["automatic_complete_case_count"] == 1


def test_empty_corpus_reports_null_rates_and_zero_attempts():
    result = score_dataset(dataset([]), [], "TEST-ONLY", "rules-test")
    assert result["attempted_count"] == 0
    assert result["coverage"] is None
    assert result["asr"]["end_to_end"]["wer"]["rate"] is None


def test_heldout_requires_predeclared_independence_and_stays_separate():
    manifest = dataset(split="heldout", kind="genuine_human_audio")
    with pytest.raises(ValueError):
        score(manifest)
    manifest["independence"] = {
        "independent_of_tuning": True,
        "criteria_frozen_before_evaluation": True,
        "frozen_source_sha": "a" * 40,
    }
    result = score(manifest)
    assert result["split"] == "heldout"
    assert result["attempted_count"] == 1
    manifest["cases"][0]["evidence_kind"] = "synthetic_fixture"
    with pytest.raises(ValueError):
        score(manifest)


def test_expected_silence_requires_real_matching_error_and_no_field_credit():
    silence = case(reference="")
    silence["expected_fields"] = {}
    silence["expected_safety_block"] = True
    silence["expected_error"] = "NO_SPEECH_DETECTED"
    result = score(
        dataset([silence]),
        [response(transcript="", status="failed", error_code="NO_SPEECH_DETECTED")],
    )
    assert result["automatic_complete_case_count"] == 1
    assert result["per_field"] == {}
    assert result["safety"]["expected_and_blocked"] == 1
    assert result["asr"]["end_to_end"]["wer"]["rate"] is None
    result = score(
        dataset([silence]), [response(transcript="", status="failed", error_code="GNANI_TIMEOUT")]
    )
    assert result["automatic_complete_case_count"] == 0
    assert result["safety"]["unassessed_provider_failures_or_empty"] == 1


def test_public_output_omits_transcripts_fields_conditions_and_original_ids():
    manifest = dataset([case("SECRET-PERSON-NAME", "PRIVATE REFERENCE CONTENT")])
    result = score(manifest, [response("SECRET-PERSON-NAME", "PRIVATE PROVIDER CONTENT")])
    rendered = json.dumps(result)
    for private in ("PRIVATE", "SECRET-PERSON", "PUMP-TEST", "test-only"):
        assert private not in rendered
    assert result["case_ids"] == ["CASE-0001"]
    assert result["split"] == "development"
    assert result["evidence_kind"] == "synthetic_fixture"


def test_cli_reads_explicit_local_files_and_emits_sanitized_summary(tmp_path):
    manifest = tmp_path / "manifest.json"
    transcripts = tmp_path / "transcripts.json"
    output = tmp_path / "summary.json"
    manifest.write_text(json.dumps(dataset()), encoding="utf-8")
    transcripts.write_text(json.dumps([response()]), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parents[2] / "scripts/score_transcripts.py"),
            "--manifest",
            str(manifest),
            "--transcripts",
            str(transcripts),
            "--dataset-id",
            "TEST-ONLY",
            "--parser-version",
            "rules-test",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "pump is leaking" not in completed.stdout + completed.stderr + output.read_text()
    assert json.loads(output.read_text())["attempted_count"] == 1


@pytest.mark.parametrize("aliased_input", ["manifest", "transcripts"])
def test_cli_rejects_hardlinked_output_without_changing_private_inputs(tmp_path, aliased_input):
    manifest = tmp_path / "manifest.json"
    transcripts = tmp_path / "transcripts.json"
    output = tmp_path / "summary.json"
    manifest.write_text(json.dumps(dataset()), encoding="utf-8")
    transcripts.write_text(json.dumps([response()]), encoding="utf-8")
    originals = {path: path.read_bytes() for path in (manifest, transcripts)}
    output.hardlink_to(manifest if aliased_input == "manifest" else transcripts)
    completed = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).resolve().parents[2] / "scripts/score_transcripts.py"),
            "--manifest",
            str(manifest),
            "--transcripts",
            str(transcripts),
            "--dataset-id",
            "TEST-ONLY",
            "--parser-version",
            "rules-test",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert {path: path.read_bytes() for path in originals} == originals
    assert "pump is leaking" not in completed.stdout + completed.stderr
