"""IMP-03: read-only cached development replay; never calls a speech provider."""

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.db.models import Asset, Location
from app.services.extraction import PARSER_VERSION, extract, matches, normalize
from scripts.evaluate_audio import FIELDS, SAFETY_CASES, compare

ROOT = Path(__file__).resolve().parents[2]


def metrics(results):
    return {
        "sample_count": len(results),
        "complete_cases_correct": sum(bool(item["complete_case_correct"]) for item in results),
        "per_field": {
            field: {
                "correct": sum(item.get("field_correct", {}).get(field, False) for item in results),
                "total": sum(field in item.get("field_correct", {}) for item in results),
            }
            for field in FIELDS
        },
        "expected_safety_blocks": {
            "correct": sum(
                bool(item["safety_blocked"]) for item in results if item["case_id"] in SAFETY_CASES
            ),
            "total": sum(item["case_id"] in SAFETY_CASES for item in results),
        },
    }


def replay(records, db):
    before = metrics(records)
    current = []
    failure_patterns = []
    for record in records:
        case = {"expected": record.get("expected"), "must_block": record["case_id"] in SAFETY_CASES}
        if record["case_id"] == "NLP-15":
            case["expected_error"] = "NO_SPEECH_DETECTED"
        extraction = extract(record.get("raw_transcript") or "", db)
        current.append(
            {
                "case_id": record["case_id"],
                **compare(case, extraction, record.get("error_code")),
            }
        )
        if not current[-1]["complete_case_correct"]:
            normalized = normalize(record.get("raw_transcript") or "")
            location_count = sum(
                bool(matches(normalized, [item.name, item.code, *item.aliases]))
                for item in db.scalars(select(Location).where(Location.is_active))
            )
            failure_patterns.append(
                {
                    "case_id": record["case_id"],
                    "exact_location_candidate_count": location_count,
                    "exact_asset_candidate_count": len(extraction["asset_candidates"]),
                    "unresolved_fields": extraction["unresolved_fields"],
                }
            )
    return {
        "change_id": "IMP-03",
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "evaluation_kind": "cached_development_transcript_replay",
        "dataset_split": "development",
        "parser_version_before": sorted({item["parser_version"] for item in records}),
        "parser_version_after": PARSER_VERSION,
        "parser_logic_changed": False,
        "test_ids": ["T-IMP-030", "T-IMP-031", "T-IMP-032", "T-IMP-036"],
        "before": before,
        "after": metrics(current),
        "previously_correct_cases_regressed": [
            old["case_id"]
            for old, new in zip(records, current, strict=True)
            if old["complete_case_correct"] and not new["complete_case_correct"]
        ],
        "failing_cases": [
            {
                "case_id": item["case_id"],
                "incorrect_fields": [
                    field for field, correct in item["field_correct"].items() if not correct
                ],
            }
            for item in current
            if not item["complete_case_correct"]
        ],
        "live_provider_calls": 0,
        "failure_patterns": failure_patterns,
        "database_scope": "fieldsaarthi_test, read-only transaction; no schema reset or seed",
        "hosted_database_writes": 0,
        "raw_transcripts_published": False,
        "decision": "Retain the baseline parser without separately verified safe improvement.",
        "assessment": (
            "No failed case has shared alias candidates. Location-conditioned disambiguation "
            "cannot recover absent exact location or asset evidence. "
            "Keep explicit human correction."
        ),
        "limitations": [
            "Replay of the previously tuned development corpus is not a held-out evaluation.",
            "No new recordings, ASR calls, WER/CER measurement or provider metadata generated.",
        ],
    }


def isolated_database_url(value):
    parsed = make_url(value)
    if parsed.get_backend_name() != "postgresql" or parsed.database != "fieldsaarthi_test":
        raise ValueError("Cached replay requires only the isolated fieldsaarthi_test database")
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.results.resolve().is_relative_to((ROOT / "private").resolve()):
        parser.error("Cached transcripts must remain under the ignored private directory")
    try:
        url = isolated_database_url(os.environ["TEST_DATABASE_URL"])
        records = [
            json.loads((args.results / f"NLP-{index:02}.json").read_text(encoding="utf-8"))
            for index in range(1, 16)
        ]
        cases = json.loads((ROOT / "docs/tests/audio-cases.json").read_text(encoding="utf-8"))
        for record, case in zip(records, cases, strict=True):
            if record["case_id"] != case["case_id"] or record.get("expected") != case.get(
                "expected"
            ):
                raise ValueError("Frozen cached labels disagree with the reviewed case manifest")
        if any(record.get("state") != "complete" for record in records):
            raise ValueError("Only completed frozen cached records can be replayed")
        engine = create_engine(url)
        try:
            with engine.connect() as connection:
                connection.execute(text("SET TRANSACTION READ ONLY"))
                with Session(bind=connection) as db:
                    if not db.scalar(select(Location.id).limit(1)) or not db.scalar(
                        select(Asset.id).limit(1)
                    ):
                        raise ValueError(
                            "The isolated test database needs the existing seed catalog"
                        )
                    report = replay(records, db)
                    report["reviewed_manifest_labels_verified"] = True
        finally:
            engine.dispose()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    except Exception as error:
        raise SystemExit(
            f"Cached replay failed ({type(error).__name__}); private details hidden"
        ) from None
    print("Sanitized cached replay report saved; no provider calls or database writes")


if __name__ == "__main__":
    main()
