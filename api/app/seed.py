import json
import os
import secrets
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
            ["water pump", "pump", "वाटर पंप", "पानी पंप", "मोटर", "பம்ப்"],
        ),
        ("AC-A01", "Air Conditioner A-01", "BLK-A-GF", ["air conditioner", "ac", "एसी", "ஏசி"]),
        ("FAN-C03", "Exhaust Fan C-03", "WH-C", ["exhaust", "fan", "पंखा", "விசிறி"]),
        ("LIGHT-C04", "Bay Light C-04", "WH-C", ["light", "bulb", "लाइट", "விளக்கு"]),
    ]
    for code, name, loc, aliases in assets:
        if not db.get(Asset, stable(code)):
            db.add(
                Asset(
                    id=stable(code),
                    asset_code=code,
                    name=name,
                    location_id=stable(loc),
                    aliases=aliases,
                )
            )
    db.commit()
    return accounts


if __name__ == "__main__":
    with SessionLocal() as db:
        accounts = seed(db)
    if accounts:
        target = ROOT / "private/demo-accounts.json"
        existing = json.loads(target.read_text()) if target.exists() else []
        target.write_text(json.dumps(existing + accounts, indent=2), encoding="utf-8")
        print(
            "Synthetic accounts created; credentials saved privately to private/demo-accounts.json"
        )
    else:
        print("Seed already present; existing passwords unchanged.")
