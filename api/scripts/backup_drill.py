"""Create a private pg_dump and restore to a new isolated scratch database.

Never overwrites or drops the source database. Scratch DB retained for inspection.
"""

import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import psycopg
from psycopg import sql
from sqlalchemy.engine import make_url

from app.core.config import DATABASE_URL, ROOT


def main() -> None:
    url = make_url(DATABASE_URL)
    pg_bin = Path(os.getenv("PG_BIN", "C:/Program Files/PostgreSQL/18/bin"))
    dump = shutil.which("pg_dump") or str(pg_bin / "pg_dump.exe")
    restore = shutil.which("pg_restore") or str(pg_bin / "pg_restore.exe")
    env = {
        **os.environ,
        "PGHOST": url.host or "localhost",
        "PGPORT": str(url.port or 5432),
        "PGUSER": url.username or "",
        "PGPASSWORD": url.password or "",
    }
    name = "fieldsaarthi_restore_" + uuid4().hex[:8]
    backup = ROOT / "private" / ("backup-" + name + ".dump")
    subprocess.run(
        [
            dump,
            "--format=custom",
            "--no-owner",
            "--no-acl",
            "--file",
            str(backup),
            "--dbname",
            url.database or "fieldsaarthi",
        ],
        env=env,
        check=True,
        capture_output=True,
    )
    connection = {
        "host": url.host,
        "port": url.port or 5432,
        "user": url.username,
        "password": url.password,
    }
    with psycopg.connect(**connection, dbname="postgres", autocommit=True) as db:
        db.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
    subprocess.run(
        [restore, "--exit-on-error", "--no-owner", "--no-acl", "--dbname", name, str(backup)],
        env=env,
        check=True,
        capture_output=True,
    )
    tables = [
        "users",
        "locations",
        "assets",
        "report_intakes",
        "work_orders",
        "audit_events",
        "idempotency_keys",
    ]
    counts = {}
    for database in [url.database, name]:
        with psycopg.connect(**connection, dbname=database) as db:
            counts[database] = {
                table: db.execute(
                    sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table))
                ).fetchone()[0]
                for table in tables
            }
    assert counts[url.database] == counts[name]
    output = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "source_database": url.database,
        "scratch_database": name,
        "source_and_restore_counts_match": True,
        "counts": counts[url.database],
        "backup": "private/" + backup.name,
        "source_modified": False,
        "scratch_retained": True,
    }
    (ROOT / "docs/evidence/backup-restore.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print("Private backup restored to isolated scratch DB; table counts match. Source unchanged.")


if __name__ == "__main__":
    main()
