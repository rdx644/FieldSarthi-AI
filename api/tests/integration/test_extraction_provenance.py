import pytest

from app.db.models import Asset
from app.db.session import SessionLocal
from app.seed import stable
from app.services.extraction import extract


def test_exact_original_spans_and_parser_version(accounts):
    transcript = "Ｂｌｏｃｋ B, WATER PUMP leaking — URGENT!"
    with SessionLocal() as db:
        result = extract(transcript, db)
    assert result["parser_version"] == "rules-v2"
    assert result["field_evidence"]["location"] == ["Ｂｌｏｃｋ B"]
    assert "WATER PUMP" in result["field_evidence"]["asset"]
    for spans in result["evidence_spans"].values():
        for span in spans:
            assert transcript[span["start"] : span["end"]] == span["text"]
    assert result["evidence_spans"]["urgency"][0]["text"] == "URGENT"


@pytest.mark.parametrize(
    "transcript,location,asset,issue,priority",
    [
        (
            "Block B second floor ka water pump leak ho raha hai, urgent hai.",
            "BLK-B-F2",
            "PUMP-B02",
            "LEAKAGE",
            "HIGH",
        ),
        (
            "ब्लॉक बी की दूसरी मंज़िल पर पानी का पंप लीक कर रहा है।",
            "BLK-B-F2",
            "PUMP-B02",
            "LEAKAGE",
            "NORMAL",
        ),
        (
            "The air conditioner on Block A ground floor is not cooling.",
            "BLK-A-GF",
            "AC-A01",
            "MECHANICAL",
            "NORMAL",
        ),
        ("பிளாக் பி இரண்டாவது மாடியில் தண்ணீர் பம்ப் கசிகிறது.", "BLK-B-F2", "PUMP-B02", "LEAKAGE", "NORMAL"),
        ("Warehouse C mein exhaust fan band ho gaya.", "WH-C", "FAN-C03", "MECHANICAL", "NORMAL"),
        ("गोदाम सी में लाइट खराब है।", "WH-C", "LIGHT-C04", "MECHANICAL", "NORMAL"),
        (
            "Air conditioner at Block A ground floor is broken and urgent.",
            "BLK-A-GF",
            "AC-A01",
            "MECHANICAL",
            "HIGH",
        ),
        ("ब्लॉक बी दूसरी मंज़िल, पंप में रिसाव।", "BLK-B-F2", "PUMP-B02", "LEAKAGE", "NORMAL"),
        (
            "Warehouse C ki bay light flicker kar rahi hai.",
            "WH-C",
            "LIGHT-C04",
            "ELECTRICAL",
            "NORMAL",
        ),
    ],
)
def test_original_roadmap_positive_scenarios(
    accounts, transcript, location, asset, issue, priority
):
    with SessionLocal() as db:
        result = extract(transcript, db)
    assert result["suggested_fields"] == {
        "location_id": stable(location),
        "asset_id": stable(asset),
        "issue_category": issue,
        "priority_suggestion": priority,
    }


@pytest.mark.parametrize(
    "transcript",
    [
        "The pump has a problem.",
        "तुरंत ठीक करो!",
        "Block A water pump leaks.",
        "இங்கே விளக்கு வேலை செய்யவில்லை.",
        "Block B mein pump or fan dono issue hain.",
        "",
        "Block B pump and Warehouse C fan broken",
        "warehouse fan and light broken",
    ],
)
def test_unsafe_or_incomplete_scenarios_remain_unresolved(accounts, transcript):
    with SessionLocal() as db:
        result = extract(transcript, db)
    assert result["suggested_fields"]["asset_id"] is None
    assert "asset_id" in result["unresolved_fields"]
    assert result["needs_review"] is True


def test_multiple_pumps_at_one_location_require_choice(accounts):
    with SessionLocal() as db:
        db.add(
            Asset(
                asset_code="TEST-PUMP",
                name="Second pump",
                aliases=["pump"],
                location_id=stable("BLK-B-F2"),
            )
        )
        db.flush()
        result = extract("block b pump leak", db)
    assert result["suggested_fields"]["asset_id"] is None
    assert len(result["asset_candidates"]) == 2
