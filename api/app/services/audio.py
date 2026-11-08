"""Bounded decoding of untrusted media; original bytes never persist after conversion."""

import io
import subprocess
import tempfile
import threading
import wave
from pathlib import Path

import imageio_ffmpeg

from app.core.errors import AppError

decode_slots = threading.BoundedSemaphore(2)
MAX_BYTES = 10_485_760


def normalize_audio(data: bytes) -> tuple[bytes, float]:
    if not data or len(data) > MAX_BYTES:
        raise AppError(
            413 if data else 400, "INVALID_AUDIO", "Use a nonempty audio file under 10 MiB."
        )
    known = (
        data.startswith((b"RIFF", b"OggS", b"fLaC", b"ID3", b"\x1a\x45\xdf\xa3", b"\xff"))
        or data[4:8] == b"ftyp"
    )
    if not known:
        raise AppError(400, "INVALID_AUDIO", "This recording format could not be recognized.")
    if not decode_slots.acquire(timeout=5):
        raise AppError(503, "AUDIO_BUSY", "Audio processing is busy. Please retry.")
    try:
        with tempfile.TemporaryDirectory(prefix="fieldsaarthi-") as folder:
            source = Path(folder) / "input.media"
            source.write_bytes(data)
            executable = imageio_ffmpeg.get_ffmpeg_exe()
            try:
                completed = subprocess.run(
                    [
                        executable,
                        "-nostdin",
                        "-v",
                        "error",
                        "-protocol_whitelist",
                        "file,pipe",
                        "-threads",
                        "1",
                        "-i",
                        str(source),
                        "-vn",
                        "-sn",
                        "-dn",
                        "-t",
                        "31",
                        "-ac",
                        "1",
                        "-ar",
                        "16000",
                        "-acodec",
                        "pcm_s16le",
                        "-f",
                        "s16le",
                        "pipe:1",
                    ],
                    capture_output=True,
                    timeout=20,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                raise AppError(
                    400, "AUDIO_CONVERSION_FAILED", "The recording could not be decoded safely."
                ) from None
            if completed.returncode or not completed.stdout:
                raise AppError(
                    400, "INVALID_AUDIO", "The recording is corrupt or contains no audio."
                )
            pcm = completed.stdout
            duration = len(pcm) / 32000
            if duration > 30:
                raise AppError(422, "AUDIO_TOO_LONG", "Keep your report under 30 seconds.")
            if duration < 0.1:
                raise AppError(
                    422, "AUDIO_TOO_SHORT", "Record a clear spoken report before submitting."
                )
            target = io.BytesIO()
            with wave.open(target, "wb") as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(16000)
                output.writeframes(pcm)
            return target.getvalue(), duration
    finally:
        decode_slots.release()
