"""NFR-13: fail-closed pause and durable admission delegation (no database I/O)."""

import pytest
from sqlalchemy.exc import OperationalError

from app.core.errors import AppError
from app.core.limits import ProviderBudget
from app.services import provider_admission


@pytest.mark.parametrize("value", ["false", "", "typo", "0"])
def test_operator_pause_fails_closed_without_charging_counters(monkeypatch, value):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", value)

    def forbidden(*args):
        raise AssertionError("Paused operation must not reserve admission")

    monkeypatch.setattr(provider_admission, "reserve_provider_admission", forbidden)
    with pytest.raises(AppError) as error:
        ProviderBudget().check("worker")
    assert error.value.code == "GNANI_REQUESTS_PAUSED"


def test_both_audio_operations_use_shared_durable_admission(monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    operations = []
    monkeypatch.setattr(
        provider_admission,
        "reserve_provider_admission",
        lambda actor, operation: operations.append((actor, operation)),
    )
    ProviderBudget().check("worker")
    ProviderBudget().check("worker", "TTS")
    assert operations == [("worker", "STT"), ("worker", "TTS")]


def test_database_failure_fails_closed_without_driver_details(monkeypatch):
    class UnavailableSessions:
        def begin(self):
            raise OperationalError(
                "test-only private SQL", {}, Exception("test-only driver detail")
            )

    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    monkeypatch.setattr(provider_admission, "SessionLocal", UnavailableSessions())
    with pytest.raises(AppError) as error:
        ProviderBudget().check("worker")
    assert error.value.status == 503
    assert error.value.code == "PROVIDER_BUDGET"
    assert "driver detail" not in error.value.message
