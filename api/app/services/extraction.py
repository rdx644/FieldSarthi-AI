"""Catalog-backed, Unicode-aware suggestions. Unknown facts stay unresolved."""

import unicodedata
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Asset, Location

PARSER_VERSION = "rules-v2"


def normalized_source(value: str) -> tuple[str, list[tuple[int, int]]]:
    """Search normalization with offsets into the untouched Unicode source."""
    chars: list[str] = []
    offsets: list[tuple[int, int]] = []
    start = 0
    while start < len(value):
        end = start + 1
        while end < len(value) and unicodedata.category(value[end]).startswith("M"):
            end += 1
        for char in unicodedata.normalize("NFKC", value[start:end]).casefold():
            char = char if unicodedata.category(char)[0] in "LNM" else " "
            if char == " " and (not chars or chars[-1] == " "):
                continue
            chars.append(char)
            offsets.append((start, end))
        start = end
    if chars and chars[-1] == " ":
        chars.pop()
        offsets.pop()
    return "".join(chars), offsets


def source_spans(transcript: str, aliases: list[str]) -> list[dict[str, Any]]:
    text, offsets = normalized_source(transcript)
    found: dict[tuple[int, int], dict[str, Any]] = {}
    for alias in aliases:
        needle = normalize(alias)
        if not needle:
            continue
        offset = 0
        while (index := text.find(needle, offset)) >= 0:
            stop = index + len(needle)
            if (index == 0 or text[index - 1] == " ") and (stop == len(text) or text[stop] == " "):
                start, end = offsets[index][0], offsets[stop - 1][1]
                found[start, end] = {"text": transcript[start:end], "start": start, "end": end}
            offset = index + 1
    return [found[key] for key in sorted(found)]


def normalize(value: str) -> str:
    return normalized_source(value)[0]


def matches(text: str, aliases: list[str]) -> list[str]:
    return [alias for alias in aliases if " " + normalize(alias) + " " in " " + text + " "]


def extract(transcript: str, db: Session) -> dict[str, Any]:
    text = normalize(transcript)
    locations = list(db.scalars(select(Location).where(Location.is_active)))
    assets = list(db.scalars(select(Asset).where(Asset.is_active)))
    locs = [(x, matches(text, [x.name, x.code, *x.aliases])) for x in locations]
    locs = [(x, evidence) for x, evidence in locs if evidence]
    location = locs[0][0] if len(locs) == 1 else None
    candidates = [(x, matches(text, [x.name, x.asset_code, *x.aliases])) for x in assets]
    candidates = [(x, evidence) for x, evidence in candidates if evidence]
    asset = (
        candidates[0][0]
        if len(candidates) == 1 and location and candidates[0][0].location_id == location.id
        else None
    )
    cues = {
        "LEAKAGE": ["leak", "leaks", "leaking", "leakage", "लीक", "रिसाव", "கசிவு", "கசிகிறது"],
        "ELECTRICAL": [
            "spark",
            "sparking",
            "electric",
            "flicker",
            "flickering",
            "short circuit",
            "चिंगारी",
            "बिजली",
            "மின்சாரம்",
        ],
        "MECHANICAL": [
            "broken",
            "stuck",
            "noise",
            "not working",
            "not cooling",
            "band ho gaya",
            "खराब",
            "आवाज",
            "சத்தம்",
            "வேலை செய்யவில்லை",
        ],
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
    evidence_aliases = {
        "location": locs[0][1] if location else [],
        "asset": candidates[0][1] if asset else [],
        "issue": issues[0][1] if len(issues) == 1 else [],
        "urgency": urgency,
    }
    spans = {
        field: source_spans(transcript, aliases) for field, aliases in evidence_aliases.items()
    }
    return {
        "parser_version": PARSER_VERSION,
        "suggested_fields": {
            "location_id": location.id if location else None,
            "asset_id": asset.id if asset else None,
            "issue_category": issues[0][0] if len(issues) == 1 else "OTHER",
            "priority_suggestion": "HIGH" if urgency else "NORMAL",
        },
        "field_evidence": {
            field: [span["text"] for span in items] for field, items in spans.items()
        },
        "evidence_spans": spans,
        "asset_candidates": [
            {"id": item.id, "name": item.name, "location_id": item.location_id}
            for item, _ in candidates
        ],
        "unresolved_fields": unresolved,
        "needs_review": True,
        "emergency_warning": bool(
            matches(text, ["fire", "gas", "smoke", "spark", "आग", "धुआं", "गैस", "चिंगारी"])
        ),
    }
