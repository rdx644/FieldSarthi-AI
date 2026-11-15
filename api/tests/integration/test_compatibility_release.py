"""T-IMP-056/063: real old-application bridge; test DB only, no provider calls."""

import json
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text
from test_workflow import fixture_intake, login, payload

from app.core.limits import ProviderBudget
from app.db.session import engine
from app.main import app
from app.seed import stable
from scripts.prepare_compatibility_release import prepare_release

ROOT = Path(__file__).resolve().parents[3]
DOMAIN_TABLES = (
    "users",
    "locations",
    "assets",
    "report_intakes",
    "work_orders",
    "audit_events",
    "idempotency_keys",
)


@pytest.fixture(scope="module")
def bridge(tmp_path_factory):
    target = tmp_path_factory.mktemp("bridge-parent") / "source"
    return prepare_release(target)


def snapshot():
    assert engine.url.database == "fieldsaarthi_test"
    with engine.connect() as connection:
        return {
            table: sorted(
                json.dumps(dict(row), sort_keys=True, default=str)
                for row in connection.execute(text("SELECT * FROM " + table)).mappings()
            )
            for table in DOMAIN_TABLES
        }


def subprocess_env():
    return {
        **os.environ,
        "DATABASE_URL": engine.url.render_as_string(hide_password=False),
        "GNANI_API_KEY_ID": "CI_TEST_KEY_NOT_A_REAL_PROVIDER_CREDENTIAL",
        "GNANI_REQUESTS_ENABLED": "true",
        "APP_ENV": "development",
    }


def start_and_probe(source):
    code = """
import json, os, runpy
from sqlalchemy import text
from app.db.session import engine
assert engine.url.database == 'fieldsaarthi_test'
os.execvp = lambda *args: None
runpy.run_path('scripts/start.py', run_name='__main__')
from app.main import app
from fastapi.testclient import TestClient
with TestClient(app) as client, engine.connect() as connection:
    print(json.dumps({'ready': client.get('/health/ready').status_code,
        'heads': sorted(connection.scalars(text('SELECT version_num FROM alembic_version'))),
        'speech_enabled': os.environ.get('GNANI_REQUESTS_ENABLED')}))
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=source / "api",
        env=subprocess_env(),
        capture_output=True,
        text=True,
        timeout=25,
    )
    if result.returncode:
        return result.returncode, None
    return 0, json.loads(result.stdout.splitlines()[-1])


def test_bridge_rejects_overwriting_any_existing_directory(bridge):
    marker = bridge / "local-preservation-canary.txt"
    marker.write_text("preserve existing source")
    with pytest.raises(FileExistsError):
        prepare_release(bridge)
    assert marker.read_text() == "preserve existing source"


def test_bridge_changes_only_the_reviewed_compatibility_files(bridge):
    manifest = json.loads((bridge / "compatibility-manifest.json").read_text())
    assert manifest["source_baseline"] == "0fca9716e3589eb9cac70f12e2468aacf7cadb5a"
    assert manifest["previous_application"] == "85e1a5e20c1f623c0ce664493c8f002e7d5cff10"
    assert manifest["previous_app_source_identical"] is True
    assert set(manifest["changed_files"]) == {
        "api/app/main.py",
        "api/scripts/start.py",
        "Dockerfile",
        "api/scripts/schema_bridge.py",
        "api/alembic/versions/0005_provider_admissions.py",
    }
    assert "scripts/schema_bridge.py" in (bridge / "Dockerfile").read_text()
    assert not (bridge / ".env").exists()
    assert not (bridge / "private").exists()


def test_staged_bridge_upgrade_rollback_and_restore_preserve_domain_and_admissions(
    accounts,
    bridge,
    monkeypatch,
):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    with TestClient(app) as client:
        headers = login(client, accounts[0])
        response = client.post(
            "/api/v1/work-orders",
            headers={**headers, "Idempotency-Key": str(uuid4())},
            json=payload(fixture_intake()),
        )
        assert response.status_code == 201
        order_path = "/api/v1/work-orders/" + response.json()["id"]
        before_detail = client.get(order_path, headers=headers).json()
        assert engine.url.database == "fieldsaarthi_test"
        with engine.begin() as connection:
            connection.execute(text("DROP TABLE provider_admissions"))
            connection.execute(text("UPDATE alembic_version SET version_num='0004'"))
        original = snapshot()
        assert start_and_probe(bridge) == (
            0,
            {"ready": 200, "heads": ["0004"], "speech_enabled": "false"},
        )
        assert "provider_admissions" not in inspect(engine).get_table_names()
        assert snapshot() == original
        # Candidate startup advances the additive schema, without a downgrade.
        assert start_and_probe(ROOT) == (
            0,
            {"ready": 200, "heads": ["0005"], "speech_enabled": "true"},
        )
        assert snapshot() == original
        ProviderBudget().check(stable(accounts[0]["email"]), "STT")
        ProviderBudget().check(stable(accounts[0]["email"]), "TTS")
        with engine.connect() as connection:
            admissions = list(
                connection.execute(
                    text(
                        "SELECT id, actor_id, operation, admitted_at "
                        "FROM provider_admissions ORDER BY id"
                    )
                )
            )
        assert len(admissions) == 2
        # Actual old application source, adapted only for compatibility, boots at 0005.
        assert start_and_probe(bridge) == (
            0,
            {"ready": 200, "heads": ["0005"], "speech_enabled": "false"},
        )
        assert snapshot() == original
        assert start_and_probe(ROOT)[0] == 0
        assert snapshot() == original
        with engine.connect() as connection:
            assert (
                list(
                    connection.execute(
                        text(
                            "SELECT id, actor_id, operation, admitted_at "
                            "FROM provider_admissions ORDER BY id"
                        )
                    )
                )
                == admissions
            )
        assert client.get(order_path, headers=headers).json() == before_detail
        assert client.get("/health/ready").status_code == 200


@pytest.mark.parametrize("heads", [[], ["0003"], ["0006"], ["0004", "0005"]])
def test_bridge_refuses_unapproved_schema_without_migrating_or_seeding(accounts, bridge, heads):
    original = snapshot()
    assert engine.url.database == "fieldsaarthi_test"
    with engine.begin() as connection:
        connection.execute(text("DELETE FROM alembic_version"))
        for head in heads:
            connection.execute(text("INSERT INTO alembic_version VALUES (:head)"), {"head": head})
    try:
        code, result = start_and_probe(bridge)
        assert code != 0 and result is None
        assert snapshot() == original
        with engine.connect() as connection:
            assert set(connection.scalars(text("SELECT version_num FROM alembic_version"))) == set(
                heads
            )
    finally:
        with engine.begin() as connection:
            connection.execute(text("DELETE FROM alembic_version"))
            connection.execute(text("INSERT INTO alembic_version VALUES ('0005')"))
