from uuid import uuid4

from fastapi.testclient import TestClient
from test_workflow import fixture_intake, login, payload

from app.main import app
from app.seed import stable


def test_cancellation_requires_audited_reason_and_is_terminal(accounts):
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        supervisor = login(client, accounts[2])
        created = client.post(
            "/api/v1/work-orders",
            json=payload(fixture_intake()),
            headers={**worker, "Idempotency-Key": str(uuid4())},
        ).json()
        path = "/api/v1/work-orders/" + created["id"]
        body = {"status": "CANCELLED", "expected_version": 1}
        for note in [None, "   "]:
            result = client.patch(
                path + "/status", headers=supervisor, json={**body, "cancellation_note": note}
            )
            assert result.status_code == 422
        result = client.patch(
            path + "/status",
            headers=supervisor,
            json={**body, "cancellation_note": "Duplicate verified on site"},
        )
        assert result.status_code == 200, result.text
        detail = client.get(path, headers=worker).json()
        assert detail["audit"][-1]["details"]["cancellation_note"] == "Duplicate verified on site"
        assert detail["status"] == "CANCELLED" and detail["version"] == 2
        assert (
            client.patch(
                path + "/priority",
                headers=supervisor,
                json={"priority": "HIGH", "expected_version": 2},
            ).status_code
            == 409
        )


def test_combined_queue_filters_and_paging_preserve_ownership(accounts):
    with TestClient(app) as client:
        worker = login(client, accounts[0])
        other = login(client, accounts[1])
        supervisor = login(client, accounts[2])
        for index in range(3):
            result = client.post(
                "/api/v1/work-orders",
                json=payload(fixture_intake()),
                headers={**worker, "Idempotency-Key": str(uuid4())},
            )
            assert result.status_code == 201
            oid = result.json()["id"]
            if index == 0:
                assert (
                    client.patch(
                        "/api/v1/work-orders/" + oid + "/assignment",
                        headers=supervisor,
                        json={
                            "assignee_id": stable("worker2@fieldsaarthi.demo"),
                            "expected_version": 1,
                        },
                    ).status_code
                    == 200
                )
                assert (
                    client.patch(
                        "/api/v1/work-orders/" + oid + "/priority",
                        headers=supervisor,
                        json={"priority": "HIGH", "expected_version": 2},
                    ).status_code
                    == 200
                )
        params = {
            "status": "ASSIGNED",
            "priority": "HIGH",
            "location_id": stable("BLK-B-F2"),
            "assignee_id": stable("worker2@fieldsaarthi.demo"),
            "q": "pump",
            "page_size": 1,
        }
        assert (
            client.get("/api/v1/work-orders", headers=supervisor, params=params).json()["total"]
            == 1
        )
        assert client.get("/api/v1/work-orders", headers=other, params=params).json()["total"] == 0
        assert client.get(
            "/api/v1/work-orders", headers=worker, params={"page_size": 2, "page": 2}
        ).json()["items"]
        assert (
            client.get(
                "/api/v1/work-orders", headers=worker, params={"status": "BOGUS"}
            ).status_code
            == 422
        )
