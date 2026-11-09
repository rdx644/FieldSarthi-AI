"""T-AUD-02: exercise actual FFmpeg WebM/Opus decoding, with test-only audio."""

import io
import subprocess
import wave

import imageio_ffmpeg

from app.services.audio import normalize_audio


def test_actual_webm_opus_converts_to_provider_pcm_wav():
    output = subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-nostdin",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=0.5",
            "-ac",
            "1",
            "-c:a",
            "libopus",
            "-f",
            "webm",
            "pipe:1",
        ],
        capture_output=True,
        timeout=15,
        check=True,
    )
    assert output.stdout.startswith(b"\x1a\x45\xdf\xa3")
    normalized, duration = normalize_audio(output.stdout)
    with wave.open(io.BytesIO(normalized), "rb") as audio:
        assert audio.getnchannels() == 1
        assert audio.getsampwidth() == 2
        assert audio.getframerate() == 16000
        assert audio.getcomptype() == "NONE"
    assert 0.4 < duration < 0.7
