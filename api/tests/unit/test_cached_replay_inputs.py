"""IMP-03: replay reports must never replace cached inputs or reviewed labels."""

import json
import sys

import pytest

from scripts import replay_cached_extraction as replay_cli


class FakeContext:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, statement):
        return None

    def scalar(self, statement):
        return True

    def connect(self):
        return self

    def dispose(self):
        pass


@pytest.fixture
def replay_inputs(tmp_path, monkeypatch):
    results = tmp_path / "private/results"
    results.mkdir(parents=True)
    manifest = tmp_path / "docs/tests/audio-cases.json"
    manifest.parent.mkdir(parents=True)
    cases = []
    originals = {}
    for index in range(1, 16):
        case = {"case_id": f"NLP-{index:02}", "expected": {"asset_code": "TEST_ONLY"}}
        cases.append(case)
        path = results / (case["case_id"] + ".json")
        path.write_text(json.dumps({**case, "state": "complete"}), encoding="utf-8")
        originals[path] = path.read_bytes()
    manifest.write_text(json.dumps(cases), encoding="utf-8")
    originals[manifest] = manifest.read_bytes()
    monkeypatch.setattr(replay_cli, "ROOT", tmp_path)
    monkeypatch.setenv("TEST_DATABASE_URL", "postgresql+psycopg://localhost/fieldsaarthi_test")
    monkeypatch.setattr(replay_cli, "create_engine", lambda url: FakeContext())
    monkeypatch.setattr(replay_cli, "Session", lambda bind: FakeContext())
    monkeypatch.setattr(replay_cli, "replay", lambda records, db: {"test_only_report": True})
    return results, manifest, originals


@pytest.mark.parametrize(
    "alias", ["result", "hardlinked_result", "cache_history", "manifest", "hardlinked_manifest"]
)
def test_replay_rejects_outputs_that_replace_source_evidence(
    tmp_path,
    monkeypatch,
    replay_inputs,
    alias,
):
    results, manifest, originals = replay_inputs
    if alias == "result":
        output = results / "NLP-01.json"
    elif alias == "manifest":
        output = manifest
    elif alias == "cache_history":
        output = results / "attempts/old-response.json"
        output.parent.mkdir()
        output.write_text('{"TEST_ONLY": "preserve cached history"}')
        originals[output] = output.read_bytes()
    else:
        output = tmp_path / "report.json"
        output.hardlink_to(manifest if alias == "hardlinked_manifest" else results / "NLP-01.json")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "replay_cached_extraction",
            "--results",
            str(results),
            "--output",
            str(output),
        ],
    )
    with pytest.raises(SystemExit):
        replay_cli.main()
    assert {path: path.read_bytes() for path in originals} == originals


def test_replay_can_write_a_separate_private_report(tmp_path, monkeypatch, replay_inputs):
    results, _, originals = replay_inputs
    output = tmp_path / "private/reports/summary.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "replay_cached_extraction",
            "--results",
            str(results),
            "--output",
            str(output),
        ],
    )
    replay_cli.main()
    assert json.loads(output.read_text())["test_only_report"] is True
    assert {path: path.read_bytes() for path in originals} == originals
