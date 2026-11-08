import json
import logging

from fastapi.testclient import TestClient

from app.main import app, logger


def test_http_event_is_emitted_with_request_id_and_without_query_secrets(caplog):
    assert logger.isEnabledFor(logging.INFO)
    logger.addHandler(caplog.handler)
    try:
        with TestClient(app) as client:
            response = client.get("/health/live?private=test-secret-never-log")
        events = [
            json.loads(record.message) for record in caplog.records if record.name == "fieldsaarthi"
        ]
        event = next(x for x in events if x.get("event") == "http_request")
        assert event["request_id"] == response.headers["X-Request-ID"]
        assert event["route"] == "/health/live"
        assert "test-secret-never-log" not in json.dumps(events)
    finally:
        logger.removeHandler(caplog.handler)
