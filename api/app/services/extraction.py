"""Catalog-backed, Unicode-aware suggestions. Unknown facts stay unresolved."""

import unicodedata
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Asset, Location


def normalize(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(
        "".join(c if unicodedata.category(c)[0] in "LNM" else " " for c in text).split()
    )


def matches(text: str, aliases: list[str]) -> list[str]:
    return [alias for alias in aliases if " " + normalize(alias) + " " in " " + text + " "]


def extract(transcript: str, db: Session) -> dict[str, Any]:
    text = normalize(transcript)
    locations = list(db.scalars(select(Location).where(Location.is_active)))
    assets = list(db.scalars(select(Asset).where(Asset.is_active)))
    locs = [(x, matches(text, [x.name, x.code, *x.aliases])) for x in locations]
    locs = [(x, evidence) for x, evidence in locs if evidence]
    location = locs[0][0] if len(locs) == 1 else None
    candidates = [
        (x, matches(text, [x.name, x.asset_code, *x.aliases]))
        for x in assets
        if not location or x.location_id == location.id
    ]
    candidates = [(x, evidence) for x, evidence in candidates if evidence]
    asset = candidates[0][0] if len(candidates) == 1 and location else None
    cues = {
        "LEAKAGE": ["leak", "leaking", "leakage", "लीक", "रिसाव", "கசிவு"],
        "ELECTRICAL": [
            "spark",
            "sparking",
            "electric",
            "short circuit",
            "चिंगारी",
            "बिजली",
            "மின்சாரம்",
        ],
        "MECHANICAL": ["broken", "stuck", "noise", "not working", "खराब", "आवाज", "சத்தம்"],
        "CLEANING": ["dirty", "clean", "cleaning", "गंदा", "सफाई", "அழுக்கு"],
    }
    issues = [(category, matches(text, aliases)) for category, aliases in cues.items()]
    issues = [(category, evidence) for category, evidence in issues if evidence]
    urgency = matches(text, ["urgent", "immediately", "emergency", "अर्जेंट", "तुरंत", "जल्दी", "அவசரம்"])
    unresolved = []
    if not location:
        unresolved.append("location_id")
    if not asset:
        unresolved.append("asset_id")
    if len(issues) != 1:
        unresolved.append("issue_category")
    return {
        "suggested_fields": {
            "location_id": location.id if location else None,
            "asset_id": asset.id if asset else None,
            "issue_category": issues[0][0] if len(issues) == 1 else "OTHER",
            "priority_suggestion": "HIGH" if urgency else "NORMAL",
        },
        "field_evidence": {
            "location": locs[0][1] if location else [],
            "asset": candidates[0][1] if asset else [],
            "issue": issues[0][1] if len(issues) == 1 else [],
            "urgency": urgency,
        },
        "unresolved_fields": unresolved,
        "needs_review": True,
        "emergency_warning": bool(
            matches(text, ["fire", "gas", "smoke", "spark", "आग", "धुआं", "गैस", "चिंगारी"])
        ),
    }
