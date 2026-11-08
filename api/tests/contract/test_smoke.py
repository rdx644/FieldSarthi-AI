"""WBS-01.1 audio validation; generated silence is a test fixture only."""

import io
import wave

import pytest

from app.integrations.gnani import GnaniError
from app.integrations.smoke import validate_wav


def wav(seconds=1, rate=16000, channels=1):
    target = io.BytesIO()
    with wave.open(target, "wb") as source:
        source.setnchannels(channels)
        source.setsampwidth(2)
        source.setframerate(rate)
        source.writeframes(b"\0\0" * int(seconds * rate) * channels)
    return target.getvalue()


def test_valid_pcm_metadata(tmp_path):
    path = tmp_path / "test.wav"
    path.write_bytes(wav())
    audio, duration = validate_wav(path)
    assert duration == 1
    assert audio == path.read_bytes()


@pytest.mark.parametrize(
    "data",
    [b"not wav", wav(26), wav(rate=48000), wav(channels=2), wav()[:-10]],
    ids=["corrupt", "too-long", "wrong-rate", "stereo", "truncated"],
)
def test_corrupt_oversize_duration_or_wrong_format_rejected(tmp_path, data):
    path = tmp_path / "bad.wav"
    path.write_bytes(data)
    with pytest.raises(GnaniError):
        validate_wav(path)


def test_config_root_is_project_not_user_home():
    from app.integrations.smoke import ROOT

    assert (ROOT / "api/pyproject.toml").is_file()
    assert ROOT.name == "fieldsaarthi-ai"


def test_curl_secret_only_in_stdin_and_default_config_disabled(monkeypatch, tmp_path):
    import json
    import subprocess

    from app.integrations.smoke import curl_call

    calls = []
    key = "private-test-key"
    body = {
        "success": True,
        "transcript": "पंप",
        "model": "prisma-v2.5",
        "request_id": "fixture",
    }

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, json.dumps(body) + "\n200", "")

    monkeypatch.setattr(subprocess, "run", run)
    result = curl_call(tmp_path / "sample.wav", key, "hi-IN", "correlation")
    argv, kwargs = calls[0]
    assert key not in " ".join(argv)
    assert key in kwargs["input"]
    assert argv[1] == "--disable"
    assert "--max-filesize" in argv
    assert result["request_id"] == "fixture"


@pytest.mark.parametrize("status", [401, 402, 403, 429, 500])
def test_curl_never_accepts_non_200(monkeypatch, tmp_path, status):
    import subprocess

    from app.integrations.smoke import curl_call

    def run(argv, **kwargs):
        return subprocess.CompletedProcess(argv, 0, '{"success":true}\n' + str(status), "")

    monkeypatch.setattr(subprocess, "run", run)
    with pytest.raises(GnaniError, match="CURL_PROVIDER_FAILURE"):
        curl_call(tmp_path / "sample.wav", "fixture-key", "hi-IN", "correlation")
