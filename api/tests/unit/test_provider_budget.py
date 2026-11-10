"""NFR-13: fail-closed pause and shared hourly request admission limits."""

import pytest

from app.core.errors import AppError
from app.core.limits import ProviderBudget


@pytest.mark.parametrize("value", ["false", "", "typo", "0"])
def test_operator_pause_fails_closed_without_charging_counters(monkeypatch, value):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", value)
    budget = ProviderBudget()
    with pytest.raises(AppError) as error:
        budget.check("worker")
    assert error.value.code == "GNANI_REQUESTS_PAUSED"
    assert not budget.entries


def test_shared_hourly_limits_and_expiration(monkeypatch):
    monkeypatch.delenv("GNANI_REQUESTS_ENABLED", raising=False)
    clock = [10000.0]
    monkeypatch.setattr("app.core.limits.time.monotonic", lambda: clock[0])
    budget = ProviderBudget()
    for index in range(80):
        budget.check("worker-" + str(index // 24))
    with pytest.raises(AppError):
        budget.check("another-worker")
    assert len(budget.entries["__global__"]) == 80
    clock[0] += 3601
    for _ in range(24):
        budget.check("same-worker")
    with pytest.raises(AppError):
        budget.check("same-worker")
    assert len(budget.entries["same-worker"]) == 24
