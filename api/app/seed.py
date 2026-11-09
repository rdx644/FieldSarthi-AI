import json
import os
import secrets
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import APP_ENV, ROOT
from app.core.security import password_hash
from app.db.models import Asset, Location, User
from app.db.session import SessionLocal


def stable(value: str) -> str:
    return str(uuid5(NAMESPACE_URL, "fieldsaarthi/" + value))


def seed(db: Session) -> list[dict[str, str]]:
    accounts = []
    for name, email, role in [
        ("Asha Rao", "worker@fieldsaarthi.demo", "WORKER"),
        ("Ravi Kumar", "worker2@fieldsaarthi.demo", "WORKER"),
        ("Meera Shah", "supervisor@fieldsaarthi.demo", "SUPERVISOR"),
    ]:
        if not db.scalar(select(User).where(User.email == email)):
            env_name = {
                "worker@fieldsaarthi.demo": "DEMO_WORKER_PASSWORD",
                "worker2@fieldsaarthi.demo": "DEMO_WORKER2_PASSWORD",
                "supervisor@fieldsaarthi.demo": "DEMO_SUPERVISOR_PASSWORD",
            }[email]
            password = os.getenv(env_name) or secrets.token_urlsafe(15)
            if APP_ENV == "production" and not os.getenv(env_name):
                raise RuntimeError("Provision all private demo passwords before production seed.")
            if len(password) < 12:
                raise RuntimeError("Demo passwords must contain at least 12 characters.")
            db.add(
                User(
                    id=stable(email),
                    display_name=name,
                    email=email,
                    role=role,
                    password_hash=password_hash.hash(password),
                )
            )
            accounts.append({"name": name, "email": email, "role": role, "password": password})
    locations = [
        ("BLK-B-F2", "Block B / Floor 2", ["block b", "ब्लॉक बी", "ब्लाक बी", "பிளாக் பி"]),
        ("BLK-A-GF", "Block A / Ground Floor", ["block a", "ब्लॉक ए", "பிளாக் ஏ"]),
        ("WH-C", "Warehouse C", ["warehouse c", "warehouse", "गोदाम", "கிடங்கு"]),
    ]
    for code, name, aliases in locations:
        if not db.get(Location, stable(code)):
            db.add(Location(id=stable(code), code=code, name=name, aliases=aliases))
    db.flush()
    assets = [
        (
            "PUMP-B02",
            "Water Pump B-02",
            "BLK-B-F2",
            ["water pump", "pump", "वाटर पंप", "पानी पंप", "पंप", "मोटर", "பம்ப்"],
        ),
        ("AC-A01", "Air Conditioner A-01", "BLK-A-GF", ["air conditioner", "ac", "एसी", "ஏசி"]),
        ("FAN-C03", "Exhaust Fan C-03", "WH-C", ["exhaust", "fan", "पंखा", "விசிறி"]),
        ("LIGHT-C04", "Bay Light C-04", "WH-C", ["light", "bulb", "लाइट", "விளக்கு"]),
    ]
    for code, name, loc, aliases in assets:
        existing = db.get(Asset, stable(code))
        if existing:
            existing.aliases = list(dict.fromkeys([*existing.aliases, *aliases]))
        else:
            db.add(
                Asset(
                    id=stable(code),
                    asset_code=code,
                    name=name,
                    location_id=stable(loc),
                    aliases=aliases,
                )
            )
    if os.getenv("PUBLIC_JUDGE_DEMO_ENABLED", "false").lower() == "true":
        if not db.get(User, stable("public-judge")):
            db.add(
                User(
                    id=stable("public-judge"),
                    display_name="Judge · read-only demo",
                    email="judge@fieldsaarthi.demo",
                    role="JUDGE",
                    password_hash=password_hash.hash(secrets.token_urlsafe(32)),
                )
            )
    db.commit()
    return accounts


def write_accounts(accounts: list[dict[str, str]], *, root: Path = ROOT) -> None:
    target = root / "private/demo-accounts.json"
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    existing = json.loads(target.read_text(encoding="utf-8")) if target.exists() else []
    by_email = {account["email"]: account for account in existing}
    by_email.update({account["email"]: account for account in accounts})
    target.write_text(json.dumps(list(by_email.values()), indent=2), encoding="utf-8")


if __name__ == "__main__":
    (ROOT / "private").mkdir(parents=True, exist_ok=True, mode=0o700)
    with SessionLocal() as db:
        accounts = seed(db)
    if accounts:
        write_accounts(accounts)
        print(
            "Synthetic accounts created; credentials saved privately to private/demo-accounts.json"
        )
    else:
        print("Seed already present; existing passwords unchanged.")
