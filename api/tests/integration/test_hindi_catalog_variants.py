from app.db.session import SessionLocal
from app.seed import stable
from app.services.extraction import extract


def test_hindi_transliterated_catalog_and_mechanical_phrase(accounts):
    with SessionLocal() as db:
        result = extract("वेयरहाउस में फैन बंद है", db)
    assert result["suggested_fields"]["location_id"] == stable("WH-C")
    assert result["suggested_fields"]["asset_id"] == stable("FAN-C03")
    assert result["suggested_fields"]["issue_category"] == "MECHANICAL"


def test_two_asset_report_in_hindi_requires_choice(accounts):
    with SessionLocal() as db:
        result = extract("ब्लॉक बी पंप और फैन दोनों खराब हैं", db)
    assert result["suggested_fields"]["asset_id"] is None
    assert "asset_id" in result["unresolved_fields"]


def test_unknown_location_asr_word_is_not_repaired_into_catalog(accounts):
    with SessionLocal() as db:
        result = extract("the water pump at unknownsite second floor is leaking", db)
    assert result["suggested_fields"]["location_id"] is None
    assert result["suggested_fields"]["asset_id"] is None
