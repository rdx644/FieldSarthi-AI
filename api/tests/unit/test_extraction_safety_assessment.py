"""IMP-03: conservative extraction on synthetic catalogs; no DB or provider calls."""

import pytest

from app.db.models import Asset, Location
from app.seed import seed, stable
from app.services.extraction import PARSER_VERSION, extract


class Catalog:
    """Supply real seeded model objects across the database boundary only."""

    def __init__(self):
        self.items = []

    def scalar(self, statement):
        return True  # Existing synthetic users need no password generation.

    def get(self, model, key):
        return None

    def add(self, item):
        self.items.append(item)

    def flush(self):
        pass

    def commit(self):
        pass

    def scalars(self, statement):
        model = statement.column_descriptions[0]["entity"]
        return [item for item in self.items if isinstance(item, model)]


@pytest.fixture
def catalog():
    result = Catalog()
    seed(result)
    return result


def test_imp_030_shared_alias_retains_all_candidates_and_requires_choice(catalog):
    for item in catalog.items:
        if isinstance(item, Asset) and item.asset_code in {"PUMP-B02", "AC-A01"}:
            item.aliases = [*item.aliases, "equipment"]
    result = extract("block b equipment leaking", catalog)
    assert result["suggested_fields"]["location_id"] == stable("BLK-B-F2")
    assert result["suggested_fields"]["asset_id"] is None
    assert len(result["asset_candidates"]) == 2
    assert "asset_id" in result["unresolved_fields"]
    assert result["needs_review"]


@pytest.mark.parametrize(
    "text",
    [
        "block b and block a pump leaking",
        "not block b; block a ac broken",
        "ब्लॉक बी और ब्लॉक ए पंप लीक",
    ],
)
def test_imp_031_conflicting_or_negated_locations_stay_unresolved(catalog, text):
    result = extract(text, catalog)
    assert result["suggested_fields"]["location_id"] is None
    assert result["suggested_fields"]["asset_id"] is None
    assert {"location_id", "asset_id"} <= set(result["unresolved_fields"])


@pytest.mark.parametrize(
    "text",
    [
        "block b pump leaking and sparking",
        "block b pump is not leaking but sparking",
    ],
)
def test_imp_031_multiple_issue_cues_require_review_even_with_negation(catalog, text):
    result = extract(text, catalog)
    assert result["suggested_fields"]["issue_category"] == "OTHER"
    assert "issue_category" in result["unresolved_fields"]
    assert result["emergency_warning"]
    assert result["needs_review"]


def test_imp_032_unicode_combining_marks_preserve_original_span_offsets(catalog):
    text = "ब्लॉक बी पंप में धुआँ है और रिसाव"
    result = extract(text, catalog)
    assert result["suggested_fields"]["location_id"] == stable("BLK-B-F2")
    assert result["suggested_fields"]["asset_id"] == stable("PUMP-B02")
    assert result["emergency_warning"]
    for spans in result["evidence_spans"].values():
        for span in spans:
            assert text[span["start"] : span["end"]] == span["text"]
    assert result["parser_version"] == PARSER_VERSION
    assert result["needs_review"]


@pytest.mark.parametrize(
    "text,missing",
    [
        ("warehouse unknown machine broken", {"asset_id"}),
        ("second floor water pump leaking", {"location_id", "asset_id"}),
        ("block a vacation", {"asset_id"}),
        ("block b pump and warehouse fan broken", {"location_id", "asset_id"}),
    ],
)
def test_imp_036_unknown_substrings_floor_only_and_multiple_equipment_stay_safe(
    catalog, text, missing
):
    result = extract(text, catalog)
    assert missing <= set(result["unresolved_fields"])
    assert result["needs_review"]


def test_imp_036_known_romanized_and_catalog_code_variants_remain_supported(catalog):
    for text in ["BLK-B-F2 PUMP-B02 band ho gaya", "block b pump not working"]:
        result = extract(text, catalog)
        assert result["suggested_fields"]["location_id"] == stable("BLK-B-F2")
        assert result["suggested_fields"]["asset_id"] == stable("PUMP-B02")
        assert result["suggested_fields"]["issue_category"] == "MECHANICAL"
        assert result["needs_review"]


def test_imp_036_catalog_fixture_contains_only_real_seed_inventory(catalog):
    assert {item.code for item in catalog.items if isinstance(item, Location)} == {
        "BLK-B-F2",
        "BLK-A-GF",
        "WH-C",
    }


@pytest.mark.parametrize(
    "url",
    [
        "postgresql+psycopg://localhost/fieldsaarthi",
        "postgresql+psycopg://localhost/fieldsaarthi_test_typo",
        "sqlite:///fieldsaarthi_test",
    ],
)
def test_imp_036_cached_replay_rejects_every_nonisolated_database(url):
    from scripts.replay_cached_extraction import isolated_database_url

    with pytest.raises(ValueError):
        isolated_database_url(url)


def test_imp_036_cached_replay_preserves_denominators_and_hides_transcripts(catalog):
    import json

    from scripts.replay_cached_extraction import replay

    correct = {
        "location_code": True,
        "asset_code": True,
        "issue_category": True,
        "priority_suggestion": True,
    }
    records = [
        {
            "case_id": "NLP-01",
            "parser_version": "rules-v4",
            "raw_transcript": "block b pump leaking PRIVATE-CANARY",
            "expected": {
                "location_code": "BLK-B-F2",
                "asset_code": "PUMP-B02",
                "issue_category": "LEAKAGE",
                "priority_suggestion": "NORMAL",
            },
            "complete_case_correct": True,
            "safety_blocked": False,
            "field_correct": correct,
        },
        {
            "case_id": "NLP-15",
            "parser_version": "rules-v4",
            "error_code": "NO_SPEECH_DETECTED",
            "complete_case_correct": True,
            "safety_blocked": True,
            "field_correct": {},
        },
    ]
    report = replay(records, catalog)
    assert report["before"] == report["after"]
    assert report["after"]["sample_count"] == 2
    assert report["after"]["complete_cases_correct"] == 2
    assert report["after"]["per_field"]["location_code"] == {"correct": 1, "total": 1}
    assert report["after"]["expected_safety_blocks"] == {"correct": 1, "total": 1}
    assert report["previously_correct_cases_regressed"] == []
    assert "PRIVATE-CANARY" not in json.dumps(report)
    assert report["live_provider_calls"] == 0
