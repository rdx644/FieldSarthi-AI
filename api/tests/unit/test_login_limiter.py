"""IMP-05: atomic bounded process-local login admission under threaded requests."""

import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.core.errors import AppError
from app.routers import auth


@pytest.fixture(autouse=True)
def isolated_login_attempts():
    auth.attempts.clear()
    yield
    auth.attempts.clear()


def test_threaded_login_admission_never_exceeds_twenty_attempts():
    def attempt(_):
        try:
            auth.check_login_attempt("test-only-address")
            return True
        except AppError as error:
            assert error.status == 429 and error.code == "RATE_LIMITED"
            return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(attempt, range(40)))
    assert outcomes.count(True) == 20
    assert outcomes.count(False) == 20
    assert len(auth.attempts["test-only-address"]) == 20


def test_login_count_check_and_append_are_atomic_when_threads_interleave():
    class DelayedSnapshotDeque(deque):
        def __len__(self):
            result = super().__len__()
            if result == 19:
                # Permit another thread to run between reading count and appending.
                time.sleep(0.02)
            return result

    auth.attempts["test-only-address"] = DelayedSnapshotDeque([time.monotonic()] * 19)
    start = threading.Barrier(2)

    def attempt(_):
        start.wait(timeout=2)
        try:
            auth.check_login_attempt("test-only-address")
            return True
        except AppError as error:
            assert error.code == "RATE_LIMITED"
            return False

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(attempt, range(2)))
    assert outcomes.count(True) == 1
    assert len(auth.attempts["test-only-address"]) == 20


def test_login_map_is_bounded_and_existing_address_can_continue(monkeypatch):
    monkeypatch.setattr(auth.time, "monotonic", lambda: 10000.0)
    for index in range(10000):
        auth.attempts[str(index)] = deque([10000.0])
    with pytest.raises(AppError) as error:
        auth.check_login_attempt("new-address")
    assert error.value.code == "RATE_LIMITED" and "new-address" not in auth.attempts
    auth.check_login_attempt("0")
    assert len(auth.attempts) == 10000 and len(auth.attempts["0"]) == 2


def test_expired_login_entries_are_pruned_before_new_admission(monkeypatch):
    monkeypatch.setattr(auth.time, "monotonic", lambda: 10000.0)
    auth.attempts["expired-address"] = deque([9099.0])
    auth.check_login_attempt("new-address")
    assert set(auth.attempts) == {"new-address"}
    assert list(auth.attempts["new-address"]) == [10000.0]
