"""NFR-01: opt-in ten genuine hosted voice-to-resolved workflows, using a consented clip.

This repeats one clip to measure workflow reliability, not distinct-clip ASR accuracy.
Team credentials and raw responses remain private. Stop on the first failure.
"""

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import httpx

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://fieldsaarthi-ai.onrender.com"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--clip", type=Path, default=ROOT / "private/sample_hi.wav")
    args = parser.parse_args()
    if not args.live:
        parser.error("--live authorizes up to ten genuine hosted STT uploads")
    audio = args.clip.read_bytes()
    accounts = json.loads((ROOT / "private/demo-accounts.json").read_text(encoding="utf-8"))
    worker_account = next(
        account for account in accounts if account["email"] == "worker@fieldsaarthi.demo"
    )
    supervisor_account = next(account for account in accounts if account["role"] == "SUPERVISOR")
    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "base_url": BASE,
        "input": "one consenting prerecorded clip repeated; not a distinct-recording evaluation",
        "target_consecutive_workflows": 10,
        "application_transcription_requests": 0,
        "successful_workflows": 0,
        "runs": [],
        "passed": False,
    }
    target = ROOT / "docs/evidence/hosted/reliability.json"
    checkpoint = ROOT / "private/hosted-reliability-run.json"
    if checkpoint.exists():
        parser.error(
            "An earlier live run is already checkpointed; inspect/archive it before spending again."
        )
    with (
        httpx.Client(
            base_url=BASE, headers={"Origin": BASE, "X-Requested-With": "FieldSaarthi"}, timeout=120
        ) as worker,
        httpx.Client(
            base_url=BASE, headers={"Origin": BASE, "X-Requested-With": "FieldSaarthi"}, timeout=120
        ) as supervisor,
    ):

        def request(client, method, path, **kwargs):
            response = client.request(method, "/api/v1" + path, **kwargs)
            if response.status_code not in {200, 201}:
                raise RuntimeError(
                    f"{method} {path.split('?')[0]} returned HTTP {response.status_code}"
                )
            return response.json(), response.status_code

        for client, account in [(worker, worker_account), (supervisor, supervisor_account)]:
            request(
                client,
                "POST",
                "/auth/login",
                json={"email": account["email"], "password": account["password"]},
            )
        people, _ = request(supervisor, "GET", "/users")
        assignee = next(
            person["id"] for person in people if person["email"] == "worker2@fieldsaarthi.demo"
        )
        try:
            for index in range(10):
                started = perf_counter()
                report["application_transcription_requests"] += 1
                checkpoint.write_text(json.dumps(report, indent=2), encoding="utf-8")
                intake, _ = request(
                    worker,
                    "POST",
                    "/intakes/transcribe",
                    files={"audio_file": (args.clip.name, audio, "audio/wav")},
                    data={"language_code": "hi-IN"},
                )
                provider = intake["provider"]
                assert provider["model"] == "prisma-v2.5" and provider["request_id"]
                fields = intake["suggested_fields"]
                assert fields["location_id"] and fields["asset_id"], (
                    "Review unresolved catalog fields before continuing"
                )
                body = {
                    "intake_id": intake["intake_id"],
                    **fields,
                    "confirmed": True,
                    "description": f"Synthetic reliability run {index + 1:02}: equipment fault",
                }
                headers = {"Idempotency-Key": str(uuid4())}
                order, status = request(worker, "POST", "/work-orders", json=body, headers=headers)
                assert status == 201
                replay, status = request(worker, "POST", "/work-orders", json=body, headers=headers)
                assert status == 200 and replay["id"] == order["id"]
                path = "/work-orders/" + order["id"]
                for endpoint, command in [
                    ("assignment", {"assignee_id": assignee, "expected_version": 1}),
                    ("status", {"status": "IN_PROGRESS", "expected_version": 2}),
                    (
                        "status",
                        {
                            "status": "RESOLVED",
                            "expected_version": 3,
                            "resolution_note": "Synthetic exercise; no real maintenance claimed.",
                        },
                    ),
                ]:
                    request(supervisor, "PATCH", path + "/" + endpoint, json=command)
                saved, _ = request(worker, "GET", path)
                assert saved["status"] == "RESOLVED" and saved["version"] == 4
                assert len(saved["audit"]) == 4
                assert saved["intake"]["provider"] == provider
                report["runs"].append(
                    {
                        "run": index + 1,
                        "public_code": order["public_code"],
                        "order_id": order["id"],
                        "provider": provider,
                        "final_status": saved["status"],
                        "audit_event_count": len(saved["audit"]),
                        "idempotent_replay": True,
                        "persisted_read_back": True,
                        "elapsed_seconds": round(perf_counter() - started, 3),
                    }
                )
                report["successful_workflows"] += 1
                checkpoint.write_text(json.dumps(report, indent=2), encoding="utf-8")
                print("Genuine hosted workflow", index + 1, "passed")
            assert len({run["provider"]["request_id"] for run in report["runs"]}) == 10
            report["passed"] = True
        except Exception as exc:
            report["failure_type"] = type(exc).__name__
            raise
        finally:
            report["completed_at_utc"] = datetime.now(UTC).isoformat()
            checkpoint.write_text(json.dumps(report, indent=2), encoding="utf-8")
            target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
