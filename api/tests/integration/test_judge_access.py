from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from test_intakes import wav
from test_workflow import fixture_intake, login, payload

from app.db.models import Order, ProviderAdmission
from app.db.session import SessionLocal
from app.main import app
from app.routers import intakes
from app.routers import orders as order_routes
from app.seed import stable


def test_public_judge_is_read_only_and_sees_only_approved_reports(accounts, monkeypatch):
    monkeypatch.setenv("PUBLIC_JUDGE_DEMO_ENABLED", "true")
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    monkeypatch.setenv("GNANI_TTS_ENABLED", "true")

    async def forbidden_provider(*args, **kwargs):
        raise AssertionError("Read-only judges must never invoke a provider")

    monkeypatch.setattr(intakes.speech, "transcribe", forbidden_provider)
    monkeypatch.setattr(order_routes.TimbreClient, "synthesize", forbidden_provider)
    from app.seed import seed

    with SessionLocal() as db:
        seed(db)
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        orders = []
        for _ in range(2):
            response = client.post(
                "/api/v1/work-orders",
                headers={**worker, "Idempotency-Key": str(uuid4())},
                json=payload(fixture_intake()),
            )
            assert response.status_code == 201
            orders.append(response.json())
        with SessionLocal() as db:
            db.get(Order, orders[0]["id"]).judge_visible = True
            db.commit()
        client.cookies.clear()
        demo = client.post("/api/v1/auth/judge-demo")
        assert demo.status_code == 200, demo.text
        assert demo.json()["user"]["role"] == "JUDGE"
        assert "access_token" not in demo.json()
        assert "httponly" in demo.headers["set-cookie"].lower()
        queue = client.get("/api/v1/work-orders").json()
        assert queue["total"] == 1 and queue["items"][0]["id"] == orders[0]["id"]
        for order, expected in [(orders[0], 200), (orders[1], 404)]:
            assert client.get("/api/v1/work-orders/" + order["id"]).status_code == expected
            assert client.get("/api/v1/intakes/" + order["intake_id"]).status_code == expected
        headers = {"Origin": "http://testserver", "X-Requested-With": "FieldSaarthi"}
        assert (
            client.post(
                "/api/v1/intakes/manual", headers=headers, json={"text": "block b pump leak"}
            ).status_code
            == 403
        )
        assert (
            client.patch(
                "/api/v1/work-orders/" + orders[0]["id"] + "/priority",
                headers=headers,
                json={"priority": "HIGH", "expected_version": 1},
            ).status_code
            == 403
        )
        assert (
            client.post(
                "/api/v1/work-orders/" + orders[0]["id"] + "/acknowledgment-audio", headers=headers
            ).status_code
            == 403
        )
        path = "/api/v1/work-orders/" + orders[0]["id"]
        before = client.get(path).json()
        assert (
            client.post(
                "/api/v1/intakes/transcribe",
                headers=headers,
                files={"audio_file": ("test-only.wav", wav(), "audio/wav")},
            ).status_code
            == 403
        )
        for endpoint, body in [
            ("assignment", {"assignee_id": stable(accounts[1]["email"]), "expected_version": 1}),
            ("status", {"status": "IN_PROGRESS", "expected_version": 1}),
        ]:
            assert (
                client.patch(path + "/" + endpoint, headers=headers, json=body).status_code == 403
            )
        assert (
            client.post(
                "/api/v1/work-orders",
                headers={**headers, "Idempotency-Key": str(uuid4())},
                json=payload(orders[0]["intake_id"]),
            ).status_code
            == 403
        )
        assert (
            client.patch(
                "/api/v1/intakes/" + orders[0]["intake_id"],
                headers=headers,
                json={"edited_transcript": "TEST ONLY denied judge correction"},
            ).status_code
            == 403
        )
        assert client.get(path).json() == before
        with SessionLocal() as db:
            assert db.scalar(select(func.count()).select_from(ProviderAdmission)) == 0
        assert client.get("/api/v1/users").status_code == 403
        assert client.get("/api/v1/work-orders/capabilities/audio").json()["tts_enabled"] is False
        assert client.get("/api/v1/auth/session").json()["user"]["role"] == "JUDGE"
        monkeypatch.setenv("PUBLIC_JUDGE_DEMO_ENABLED", "false")
        assert client.get("/api/v1/work-orders").status_code == 401
        assert client.get("/api/v1/work-orders/" + orders[0]["id"]).status_code == 401
        assert client.get("/api/v1/auth/session").json()["user"] is None


def test_public_judge_can_be_disabled(accounts, monkeypatch):
    monkeypatch.setenv("PUBLIC_JUDGE_DEMO_ENABLED", "false")
    with TestClient(app) as client:
        assert client.get("/api/v1/auth/demo").json()["enabled"] is False
        assert client.post("/api/v1/auth/judge-demo").status_code == 404
