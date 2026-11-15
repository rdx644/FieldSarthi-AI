"""Container timeouts must preserve user resources and remove invocation-owned ones."""

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.mark.parametrize("failure_phase", ["network", "database", "helper", "application"])
def test_timeout_cleanup_removes_only_invocation_owned_resources(
    tmp_path, monkeypatch, failure_phase
):
    path = Path(__file__).resolve().parents[1] / "container/release_check.py"
    spec = importlib.util.spec_from_file_location("release_check_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    containers = {"existing-user-app": "another-owner"}
    networks = {"existing-user-network": "another-owner"}
    failed = False

    def result(stdout="", returncode=0):
        return SimpleNamespace(stdout=stdout, stderr="", returncode=returncode)

    def docker(*args, check=True):
        nonlocal failed
        if args[:2] == ("image", "inspect"):
            return result("sha256:test-only-image")
        if args[:2] == ("network", "create"):
            networks[args[-1]] = module.TOKEN
            if failure_phase == "network":
                raise subprocess.TimeoutExpired("TEST_ONLY_DOCKER_CLIENT", 90)
            return result()
        if args[:2] == ("network", "inspect"):
            return result(networks.get(args[-1], ""), 0 if args[-1] in networks else 1)
        if args[:2] == ("network", "rm"):
            if any(owner == module.TOKEN for owner in containers.values()):
                return result(returncode=1)
            networks.pop(args[-1], None)
            return result()
        if args[0] == "run":
            helper = "--entrypoint" in args
            name = args[args.index("--name") + 1] if "--name" in args else "anonymous-helper"
            containers[name] = module.TOKEN if "--label" in args else "unlabelled"
            phase = "helper" if helper else "application" if name.endswith("-stage") else "database"
            if phase == failure_phase and not failed:
                failed = True
                raise subprocess.TimeoutExpired("TEST_ONLY_DOCKER_CLIENT", 90)
            if "--rm" in args:
                containers.pop(name)
            return result()
        if args[0] == "inspect":
            return result(containers.get(args[-1], ""), 0 if args[-1] in containers else 1)
        if args[0] == "rm":
            containers.pop(args[-1], None)
            return result()
        if args[0] == "exec":
            return result("{}\n" if "psql" in args else "")
        raise AssertionError("Unexpected fake Docker operation")

    monkeypatch.setattr(module, "docker", docker)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "release_check.py",
            "--candidate-image",
            "TEST_ONLY_CANDIDATE",
            "--bridge-image",
            "TEST_ONLY_BRIDGE",
            "--output",
            str(tmp_path / "result.json"),
        ],
    )
    with pytest.raises(subprocess.TimeoutExpired):
        module.main()
    assert containers == {"existing-user-app": "another-owner"}
    assert networks == {"existing-user-network": "another-owner"}


def test_docker_output_preserves_unicode_on_windows(monkeypatch):
    path = Path(__file__).resolve().parents[1] / "container/release_check.py"
    spec = importlib.util.spec_from_file_location("release_check_unicode_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = "\u092a\u093e\u0928\u0940 \u0baa\u0bae\u0bcd\u0baa\u0bcd"
    run = subprocess.run

    def emit_unicode(arguments, **kwargs):
        return run(
            [
                sys.executable,
                "-c",
                "import sys; sys.stdout.buffer.write(" + repr(expected) + ".encode('utf-8'))",
            ],
            **kwargs,
        )

    monkeypatch.setattr(module.subprocess, "run", emit_unicode)
    assert module.docker("TEST_ONLY_UNICODE_OUTPUT").stdout == expected
