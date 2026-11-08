import pytest

from app.db.session import SessionLocal
from app.seed import seed, stable
from app.services.extraction import extract

CASES = [
    ("block b water pump leak urgent", "BLK-B-F2", "PUMP-B02", "LEAKAGE"),
    ("Block B pump is leaking", "BLK-B-F2", "PUMP-B02", "LEAKAGE"),
    ("ब्लॉक बी वाटर पंप लीक अर्जेंट", "BLK-B-F2", "PUMP-B02", "LEAKAGE"),
    ("ब्लॉक बी मोटर खराब", "BLK-B-F2", "PUMP-B02", "MECHANICAL"),
    ("block a ac not working", "BLK-A-GF", "AC-A01", "MECHANICAL"),
    ("ब्लॉक ए एसी खराब", "BLK-A-GF", "AC-A01", "MECHANICAL"),
    ("warehouse c fan noise", "WH-C", "FAN-C03", "MECHANICAL"),
    ("warehouse light sparking", "WH-C", "LIGHT-C04", "ELECTRICAL"),
    ("गोदाम पंखा आवाज", "WH-C", "FAN-C03", "MECHANICAL"),
    ("गोदाम लाइट चिंगारी", "WH-C", "LIGHT-C04", "ELECTRICAL"),
    ("block b pump cleaning", "BLK-B-F2", "PUMP-B02", "CLEANING"),
    ("block a air conditioner dirty", "BLK-A-GF", "AC-A01", "CLEANING"),
    ("warehouse bulb broken", "WH-C", "LIGHT-C04", "MECHANICAL"),
    ("warehouse c exhaust stuck", "WH-C", "FAN-C03", "MECHANICAL"),
    ("block b pump रिसाव", "BLK-B-F2", "PUMP-B02", "LEAKAGE"),
]


@pytest.mark.parametrize(
    "utterance,location,asset,issue", CASES, ids=[f"case-{i}" for i in range(15)]
)
def test_ground_truth(utterance, location, asset, issue):
    with SessionLocal() as db:
        seed(db)
        result = extract(utterance, db)
    fields = result["suggested_fields"]
    assert fields["location_id"] == stable(location)
    assert fields["asset_id"] == stable(asset)
    assert fields["issue_category"] == issue


def test_missing_location_is_not_invented():
    with SessionLocal() as db:
        result = extract("pump leak", db)
    assert result["suggested_fields"]["asset_id"] is None
    assert "location_id" in result["unresolved_fields"]


def test_word_substrings_do_not_match():
    with SessionLocal() as db:
        result = extract("block a vacation", db)
    assert result["suggested_fields"]["asset_id"] is None
