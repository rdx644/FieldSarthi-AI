"""IMP-05 unit guards: reject invalid operations before any database/provider work."""

import pytest

from app.core.errors import AppError
from app.core.limits import ProviderBudget


def test_invalid_operation_is_denied_before_reservation(monkeypatch):
    monkeypatch.setenv("GNANI_REQUESTS_ENABLED", "true")
    with pytest.raises(AppError) as error:
        ProviderBudget().check("worker", "UNKNOWN")
    assert error.value.code == "INVALID_PROVIDER_OPERATION"
