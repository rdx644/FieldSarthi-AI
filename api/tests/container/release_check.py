"""T-IMP-056/063: actual container upgrade/rollback, isolated synthetic DB only.

Creates a uniquely labelled internal Docker network and PostgreSQL 18 container.
No existing DB/container, host port, real credential or provider endpoint is used.
"""

import argparse
import json
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

TABLES = (
    "users",
    "locations",
    "assets",
    "report_intakes",
    "work_orders",
    "audit_events",
    "idempotency_keys",
)
TOKEN = uuid4().hex[:12]
PREFIX = "fieldsaarthi-release-" + TOKEN
LABEL = "fieldsaarthi.release-test=" + TOKEN
ENVIRONMENT = {
    "APP_ENV": "development",
    "DATABASE_URL": "postgresql+psycopg://fieldsaarthi:CI_TEST_LOCAL_ONLY@database:5432/fieldsaarthi_test",
    "JWT_SECRET": "CI_TEST_ONLY_RELEASE_SIGNING_KEY_NOT_FOR_PRODUCTION",
    "GNANI_API_KEY_ID": "CI_TEST_KEY_NOT_A_REAL_PROVIDER_CREDENTIAL",
    "GNANI_REQUESTS_ENABLED": "true",
    "GNANI_TTS_ENABLED": "true",
    "PUBLIC_JUDGE_DEMO_ENABLED": "true",
    "DEMO_WORKER_PASSWORD": "CI_TEST_WORKER_ONLY_1234",
    "DEMO_WORKER2_PASSWORD": "CI_TEST_WORKER2_ONLY_1234",
    "DEMO_SUPERVISOR_PASSWORD": "CI_TEST_SUPERVISOR_ONLY_1234",
}
FIXTURE = """
from app.db.session import engine, SessionLocal
from app.db.models import Intake, User
from app.seed import stable
from app.schemas.commands import Confirm
from app.services.orders import create_order
assert engine.url.database == 'fieldsaarthi_test'
with SessionLocal() as db:
    intake = Intake(reporter_id=stable('worker@fieldsaarthi.demo'),
        source_type='MANUAL_TEXT', status='READY_FOR_REVIEW', language_code='en-IN',
        raw_transcript='TEST-ONLY synthetic pump leak')
    db.add(intake); db.commit()
    body = Confirm(intake_id=intake.id, location_id=stable('BLK-B-F2'),
        asset_id=stable('PUMP-B02'), issue_category='LEAKAGE',
        description='TEST-ONLY synthetic pump leak', priority_suggestion='NORMAL', confirmed=True)
    create_order(db, body, db.get(User, stable('worker@fieldsaarthi.demo')),
        'TEST-ONLY-COMPATIBILITY-KEY')
"""
PROBE = """
import json, os, httpx
with httpx.Client(base_url='http://127.0.0.1:8000') as client:
    ready = client.get('/health/ready')
    assert ready.status_code == 200
    assert client.get('/').status_code == 200
    session = client.post('/api/v1/auth/login', json={'email':'worker@fieldsaarthi.demo',
        'password':os.environ['DEMO_WORKER_PASSWORD']})
    assert session.status_code == 200
    voice = client.get('/api/v1/work-orders/capabilities/audio').json()['tts_enabled']
    queue = client.get('/api/v1/work-orders').json()
    assert queue['total'] == 1
    detail = client.get('/api/v1/work-orders/' + queue['items'][0]['id']).json()
    assert detail['intake']['source_type'] == 'MANUAL_TEXT'
    assert detail['intake']['provider'] is None
    print(json.dumps({'ready':200,'root':200,'work_order_count':1,'tts_enabled':voice,
        'manual_provenance_preserved':True}))
"""
RESERVE = """
from app.db.session import engine
from app.core.limits import ProviderBudget
from app.seed import stable
assert engine.url.database == 'fieldsaarthi_test'
ProviderBudget().check(stable('worker@fieldsaarthi.demo'),'STT')
ProviderBudget().check(stable('worker@fieldsaarthi.demo'),'TTS')
"""


def docker(*arguments, check=True):
    result = subprocess.run(
        ["docker", *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    if check and result.returncode:
        raise RuntimeError("Release-test Docker command failed: " + arguments[0])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-image", required=True)
    parser.add_argument("--bridge-image", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Preserve existing evidence; choose a new output file.")
    containers = []
    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "kind": "nonbillable_synthetic_isolated_container_release_rehearsal",
        "status": "not_completed",
        "provider_calls": 0,
        "production_changes": 0,
        "database_name": "fieldsaarthi_test",
        "internal_network_only": True,
        "phases": [],
    }
    environment = [value for pair in ENVIRONMENT.items() for value in ("--env", "=".join(pair))]
    try:
        images = {
            role: docker("image", "inspect", "--format", "{{.Id}}", image).stdout.strip()
            for role, image in (("candidate", args.candidate_image), ("bridge", args.bridge_image))
        }
        report["image_ids"] = images
        docker("network", "create", "--internal", "--label", LABEL, PREFIX)
        database = PREFIX + "-db"
        containers.append(database)
        docker(
            "run",
            "--detach",
            "--name",
            database,
            "--label",
            LABEL,
            "--network",
            PREFIX,
            "--network-alias",
            "database",
            "--env",
            "POSTGRES_USER=fieldsaarthi",
            "--env",
            "POSTGRES_PASSWORD=CI_TEST_LOCAL_ONLY",
            "--env",
            "POSTGRES_DB=fieldsaarthi_test",
            "postgres:18",
        )
        for _ in range(40):
            if (
                docker(
                    "exec",
                    database,
                    "pg_isready",
                    "-U",
                    "fieldsaarthi",
                    "-d",
                    "fieldsaarthi_test",
                    check=False,
                ).returncode
                == 0
            ):
                break
            time.sleep(1)
        else:
            raise RuntimeError("Isolated release-test PostgreSQL did not become ready")

        def run_python(image, *arguments):
            name = PREFIX + "-helper-" + str(len(containers))
            containers.append(name)
            return docker(
                "run",
                "--rm",
                "--name",
                name,
                "--label",
                LABEL,
                "--network",
                PREFIX,
                *environment,
                "--entrypoint",
                "python",
                image,
                *arguments,
            )

        def sql(query):
            return docker(
                "exec",
                database,
                "psql",
                "-X",
                "-A",
                "-t",
                "-U",
                "fieldsaarthi",
                "-d",
                "fieldsaarthi_test",
                "-c",
                query,
            ).stdout

        def snapshot(tables):
            return {
                table: sorted(
                    json.dumps(json.loads(row), sort_keys=True)
                    for row in sql("SELECT to_jsonb(t) FROM " + table + " t").splitlines()
                )
                for table in tables
            }

        def start(role, phase):
            print("Checking isolated container phase: " + phase, flush=True)
            name = PREFIX + "-" + phase
            containers.append(name)
            docker(
                "run",
                "--detach",
                "--name",
                name,
                "--label",
                LABEL,
                "--network",
                PREFIX,
                *environment,
                images[role],
            )
            for _ in range(50):
                probe = docker("exec", name, "python", "-c", PROBE, check=False)
                if probe.returncode == 0:
                    data = json.loads(probe.stdout.splitlines()[-1])
                    break
                if (
                    docker("inspect", "--format", "{{.State.Running}}", name).stdout.strip()
                    != "true"
                ):
                    raise RuntimeError("Release-test application exited before readiness")
                time.sleep(1)
            else:
                raise RuntimeError("Release-test application did not become ready")
            data.update(
                phase=phase, schema_head=sql("SELECT version_num FROM alembic_version").strip()
            )
            if role == "bridge":
                assert data["tts_enabled"] is False
            report["phases"].append(data)
            return name

        run_python(images["bridge"], "-m", "alembic", "upgrade", "0004")
        run_python(images["bridge"], "-m", "app.seed")
        run_python(images["candidate"], "-c", FIXTURE)
        original = snapshot(TABLES)
        assert len(original["work_orders"]) == len(original["audit_events"]) == 1
        first = start("bridge", "stage")
        assert report["phases"][-1]["schema_head"] == "0004"
        assert snapshot(TABLES) == original
        docker("stop", "--time", "5", first)
        candidate = start("candidate", "activate")
        assert report["phases"][-1]["schema_head"] == "0005"
        assert snapshot(TABLES) == original
        run_python(images["candidate"], "-c", RESERVE)
        admissions = snapshot(("provider_admissions",))
        assert len(admissions["provider_admissions"]) == 2
        docker("stop", "--time", "5", candidate)
        rollback = start("bridge", "rollback")
        assert report["phases"][-1]["schema_head"] == "0005"
        assert snapshot(TABLES) == original
        assert snapshot(("provider_admissions",)) == admissions
        docker("stop", "--time", "5", rollback)
        start("candidate", "restore")
        assert report["phases"][-1]["schema_head"] == "0005"
        assert snapshot(TABLES) == original
        assert snapshot(("provider_admissions",)) == admissions
        report.update(
            status="passed",
            domain_tables_unchanged=list(TABLES),
            synthetic_order_count=1,
            audit_event_count=1,
            admission_rows_preserved=2,
            schema_downgrades=0,
            existing_host_databases_or_containers_changed=False,
        )
    finally:
        # Only exact invocation-owned, labelled resources may be removed.
        # One failed inspect/removal must not skip later cleanup or the evidence report.
        cleanup_failures = []

        def cleanup(*arguments):
            try:
                result = docker(*arguments, check=False)
            except (subprocess.TimeoutExpired, OSError) as exc:
                cleanup_failures.append(
                    {
                        "operation": arguments[0],
                        "resource": arguments[-1],
                        "error": type(exc).__name__,
                    }
                )
                return None
            if result.returncode and (
                arguments[0] == "rm"
                or arguments[:2] == ("network", "rm")
                or result.stderr
                and "no such" not in result.stderr.lower()
            ):
                cleanup_failures.append(
                    {"operation": arguments[0], "resource": arguments[-1], "error": "nonzero_exit"}
                )
            return result

        for name in reversed(containers):
            observed = cleanup(
                "inspect",
                "--format",
                '{{index .Config.Labels "fieldsaarthi.release-test"}}',
                name,
            )
            if (
                observed is not None
                and observed.returncode == 0
                and observed.stdout.strip() == TOKEN
            ):
                cleanup("rm", "--force", "--volumes", name)
        network = cleanup(
            "network",
            "inspect",
            "--format",
            '{{index .Labels "fieldsaarthi.release-test"}}',
            PREFIX,
        )
        if network is not None and network.returncode == 0 and network.stdout.strip() == TOKEN:
            cleanup("network", "rm", PREFIX)
        report.update(cleanup_complete=not cleanup_failures, cleanup_failures=cleanup_failures)
        if cleanup_failures:
            report["status"] = "failed_cleanup"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "passed":
        raise RuntimeError("Release rehearsal cleanup failed; inspect the evidence report.")
    print("Isolated container release rehearsal passed; no live provider or production changes.")


if __name__ == "__main__":
    main()
