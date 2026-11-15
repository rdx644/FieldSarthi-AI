"""IMP-04A (FR-06..15, NFR-03/05/14): offline, privacy-preserving ASR metrics.

This module intentionally imports neither application configuration nor providers.
It reads explicit local JSON files and never contacts a network or database.
"""

import argparse
import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path

FIELDS = {"location_code", "asset_code", "issue_category", "priority_suggestion"}
LANGUAGES = {"hi-IN", "en-IN", "ta-IN"}
TAGS = {"Hindi", "English", "Hinglish", "Tamil"}
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z")
NORMALIZATION = {
    "unicode": "NFC",
    "case": "casefold",
    "punctuation": "Unicode punctuation replaced with spaces",
    "words": "whitespace-delimited; scripts and numbers preserved without transliteration",
    "characters": "Unicode codepoints after normalization, whitespace excluded; not graphemes",
    "alignment": "Levenshtein; ties prefer substitution, deletion, insertion",
}


def normalize(text):
    text = unicodedata.normalize("NFC", text).casefold()
    return " ".join(
        "".join(" " if unicodedata.category(c).startswith("P") else c for c in text).split()
    )


def edit_counts(reference, hypothesis):
    """Return one deterministic minimal edit alignment using linear row storage."""
    previous = [(0, 0, j) for j in range(len(hypothesis) + 1)]
    for i, source in enumerate(reference, 1):
        current = [(0, i, 0)]
        for j, target in enumerate(hypothesis, 1):
            if source == target:
                current.append(previous[j - 1])
                continue
            sub, delete, insert = previous[j - 1], previous[j], current[j - 1]
            choices = [
                (sub[0] + 1, sub[1], sub[2]),
                (delete[0], delete[1] + 1, delete[2]),
                (insert[0], insert[1], insert[2] + 1),
            ]
            current.append(min(choices, key=sum))
        previous = current
    substitutions, deletions, insertions = previous[-1]
    return {
        "substitutions": substitutions,
        "deletions": deletions,
        "insertions": insertions,
        "reference_units": len(reference),
    }


def validate(manifest, responses, dataset_id, parser_version):
    def require(condition):
        if not condition:
            raise ValueError("Invalid offline manifest/results; check the documented schema.")

    require(isinstance(manifest, dict) and manifest.get("schema_version") == 1)
    require(TOKEN.fullmatch(dataset_id) and TOKEN.fullmatch(parser_version))
    require(manifest.get("dataset_id") == dataset_id)
    require(manifest.get("split") in {"development", "heldout"})
    require(manifest.get("evidence_kind") in {"genuine_human_audio", "synthetic_fixture"})
    require(isinstance(manifest.get("conditions"), dict))
    if manifest["split"] == "heldout":
        independence = manifest.get("independence", {})
        require(isinstance(independence, dict))
        require(independence.get("independent_of_tuning") is True)
        require(independence.get("criteria_frozen_before_evaluation") is True)
        require(
            isinstance(independence.get("frozen_source_sha"), str)
            and re.fullmatch(r"[a-fA-F0-9]{40}", independence["frozen_source_sha"])
        )
    cases = manifest.get("cases")
    require(isinstance(cases, list) and len(cases) <= 1000)
    require(isinstance(responses, list) and len(responses) == len(cases))
    indexed = {}
    for response in responses:
        require(isinstance(response, dict))
        require(
            set(response)
            <= {
                "case_id",
                "provider_status",
                "transcript",
                "parser_version",
                "observed_fields",
                "safety_blocked",
                "error_code",
            }
        )
        identifier = response.get("case_id")
        require(isinstance(identifier, str) and 0 < len(identifier) <= 200)
        require(identifier not in indexed)
        require(response.get("provider_status") in {"success", "failed", "empty"})
        require(
            response.get("error_code") is None
            or isinstance(response.get("error_code"), str)
            and len(response["error_code"]) <= 100
        )
        require(response.get("provider_status") == "failed" or not response.get("error_code"))
        require(isinstance(response.get("transcript", ""), str))
        require(len(response.get("transcript", "")) <= 4000)
        require(response.get("parser_version") == parser_version)
        require(isinstance(response.get("observed_fields", {}), dict))
        require(set(response.get("observed_fields", {})) <= FIELDS)
        require(
            all(
                value is None or isinstance(value, str) and len(value) <= 200
                for value in response.get("observed_fields", {}).values()
            )
        )
        require(type(response.get("safety_blocked")) in {bool, type(None)})
        if response.get("provider_status") == "empty":
            require(not response.get("transcript", "").strip())
        indexed[identifier] = response
    seen = set()
    for case in cases:
        require(isinstance(case, dict))
        identifier = case.get("case_id")
        require(isinstance(identifier, str) and identifier in indexed and identifier not in seen)
        seen.add(identifier)
        require(case.get("split", manifest["split"]) == manifest["split"])
        require(case.get("evidence_kind", manifest["evidence_kind"]) == manifest["evidence_kind"])
        require(case.get("language_code") in LANGUAGES)
        tags = case.get("spoken_language_tags")
        require(isinstance(tags, list) and bool(tags))
        require(all(isinstance(tag, str) and tag in TAGS for tag in tags))
        require(len(set(tags)) == len(tags))
        require(case.get("consent_obtained") is True)
        duration = case.get("audio_duration_seconds")
        require(type(duration) in {int, float} and math.isfinite(duration) and 0 < duration <= 30)
        reference = case.get("reference_transcript")
        require(reference is None or isinstance(reference, str) and len(reference) <= 4000)
        require(reference is None or case.get("reference_verified") is True)
        require(type(case.get("expected_safety_block")) in {bool, type(None)})
        require(isinstance(case.get("expected_fields", {}), dict))
        require(set(case.get("expected_fields", {})) <= FIELDS)
        require(
            all(
                value is None or isinstance(value, str) and len(value) <= 200
                for value in case.get("expected_fields", {}).values()
            )
        )
        require(case.get("expected_error") in {None, "NO_SPEECH_DETECTED"})
        if case.get("expected_error"):
            require(not case.get("expected_fields") and case.get("expected_safety_block") is True)
    return [(case, indexed[case["case_id"]]) for case in cases]


def aggregate(rows):
    asr = {
        scope: {
            metric: {
                "substitutions": 0,
                "deletions": 0,
                "insertions": 0,
                "reference_units": 0,
                "scored_case_count": 0,
            }
            for metric in ("wer", "cer")
        }
        for scope in ("end_to_end", "successful_nonempty")
    }
    per_field = {}
    safety = dict.fromkeys(
        [
            "expected_and_blocked",
            "false_accepts",
            "false_blocks",
            "expected_and_accepted",
            "unassessed_provider_failures_or_empty",
            "unassessed_missing_observation",
        ],
        0,
    )
    nonempty = missing_reference = empty_reference = complete = field_cases = 0
    for case, result in rows:
        available = result["provider_status"] == "success" and bool(
            result.get("transcript", "").strip()
        )
        nonempty += available
        reference = case.get("reference_transcript")
        if reference is None:
            missing_reference += 1
        elif not normalize(reference):
            empty_reference += 1
        else:
            reference = normalize(reference)
            hypothesis = normalize(result.get("transcript", "")) if available else ""
            for metric, source, target in (
                ("wer", reference.split(), hypothesis.split()),
                ("cer", list("".join(reference.split())), list("".join(hypothesis.split()))),
            ):
                counts = edit_counts(source, target)
                for scope in ("end_to_end", "successful_nonempty"):
                    if scope == "successful_nonempty" and not available:
                        continue
                    for key, value in counts.items():
                        asr[scope][metric][key] += value
                    asr[scope][metric]["scored_case_count"] += 1
        expected = case.get("expected_fields", {})
        observed = result.get("observed_fields", {})
        field_cases += bool(expected)
        correct = True
        for field, value in expected.items():
            counts = per_field.setdefault(
                field,
                {
                    "end_to_end": {"correct": 0, "total": 0},
                    "successful_nonempty": {"correct": 0, "total": 0},
                },
            )
            matched = available and field in observed and observed[field] == value
            correct &= matched
            counts["end_to_end"]["total"] += 1
            counts["end_to_end"]["correct"] += matched
            if available:
                counts["successful_nonempty"]["total"] += 1
                counts["successful_nonempty"]["correct"] += matched
        expected_block = case.get("expected_safety_block")
        blocked = result.get("safety_blocked")
        safety_correct = expected_block is None or blocked is expected_block
        expected_error = case.get("expected_error")
        error_correct = (
            expected_error
            and result["provider_status"] == "failed"
            and result.get("error_code") == expected_error
        )
        if expected_block is not None:
            if error_correct:
                safety["expected_and_blocked"] += 1
            elif not available:
                safety["unassessed_provider_failures_or_empty"] += 1
            elif blocked is None:
                safety["unassessed_missing_observation"] += 1
            else:
                label = (
                    "expected_and_blocked"
                    if expected_block and blocked
                    else "false_accepts"
                    if expected_block
                    else "false_blocks"
                    if blocked
                    else "expected_and_accepted"
                )
                safety[label] += 1
        # A matching expected provider error is explicit (e.g. consented silence),
        # never accidental credit for a transport outage or empty success.
        if expected_error:
            complete += bool(error_correct)
        elif set(expected) == FIELDS:
            complete += available and correct and safety_correct
    for scopes in asr.values():
        for metric in scopes.values():
            edits = metric["substitutions"] + metric["deletions"] + metric["insertions"]
            metric["rate"] = (
                edits / metric["reference_units"] if metric["reference_units"] else None
            )
    return {
        "attempted_count": len(rows),
        "nonempty_count": nonempty,
        "failed_or_empty_count": len(rows) - nonempty,
        "coverage": nonempty / len(rows) if rows else None,
        "missing_verified_reference_count": missing_reference,
        "empty_normalized_reference_count": empty_reference,
        "asr": asr,
        "per_field": per_field,
        "safety": safety,
        "automatic_complete_case_count": complete,
        "automatic_complete_case_denominator": len(rows),
        "field_expected_case_count": field_cases,
        "correction_recovery": "not measured; no corrected transcripts are scored",
    }


def score_dataset(manifest, responses, dataset_id, parser_version):
    rows = validate(manifest, responses, dataset_id, parser_version)
    # Never copy private conditions, original identifiers, field values or text.
    return {
        "schema_version": 1,
        "dataset_id": dataset_id,
        "parser_version": parser_version,
        "split": manifest["split"],
        "evidence_kind": manifest["evidence_kind"],
        "normalization": NORMALIZATION,
        "source_attestation": "Operator-supplied; scorer does not authenticate audio or provider",
        "heldout_independence": manifest.get("independence")
        and {
            "independent_of_tuning": True,
            "criteria_frozen_before_evaluation": True,
            "frozen_source_sha": manifest["independence"]["frozen_source_sha"],
        }
        if manifest["split"] == "heldout"
        else None,
        "case_ids": [f"CASE-{index:04}" for index in range(1, len(rows) + 1)],
        **aggregate(rows),
        "by_language_code": {
            language: aggregate([row for row in rows if row[0]["language_code"] == language])
            for language in sorted({row[0]["language_code"] for row in rows})
        },
        "by_spoken_language_tag": {
            tag: aggregate([row for row in rows if tag in row[0]["spoken_language_tags"]])
            for tag in sorted({tag for row in rows for tag in row[0]["spoken_language_tags"]})
        },
        "language_tag_denominators_overlap": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--transcripts", type=Path, required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--parser-version", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        # Cap local input size; reject output aliasing so private originals survive.
        paths = [args.manifest.resolve(), args.transcripts.resolve()]
        output = args.output.resolve()
        if (
            output in paths
            or output.exists()
            and any(output.samefile(path) for path in paths)
            or any(path.stat().st_size > 16 * 1024 * 1024 for path in paths)
        ):
            raise ValueError("Input/output path or size invalid.")
        raw_inputs = [path.read_bytes() for path in paths]
        report = score_dataset(
            json.loads(raw_inputs[0]),
            json.loads(raw_inputs[1]),
            args.dataset_id,
            args.parser_version,
        )
        report["private_input_sha256"] = [hashlib.sha256(raw).hexdigest() for raw in raw_inputs]
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        parser.exit(
            2,
            "Offline scoring failed; check input schema and local paths. No text was emitted.\n",
        )


if __name__ == "__main__":
    main()
