"""WBS-01 opt-in live call. Never runs in the ordinary contract suite."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import io
import json
import os
import subprocess
import sys
import wave
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from app.integrations.gnani import MODEL, STT_URL, GnaniError, GnaniSpeechClient

ROOT = Path(__file__).resolve().parents[3]


def validate_wav(path: Path) -> tuple[bytes, float]:
    if not path.is_file() or not 44 < path.stat().st_size <= 10_485_760:
        raise GnaniError("INVALID_AUDIO")
    audio = path.read_bytes()
    try:
        with wave.open(io.BytesIO(audio), "rb") as source:
            duration = source.getnframes() / source.getframerate()
            if (
                source.getcomptype() != "NONE"
                or source.getnchannels() != 1
                or source.getsampwidth() != 2
                or source.getframerate() != 16000
                or not 0.1 <= duration <= 25
            ):
                raise GnaniError("EXPECTED_MONO_PCM16_16KHZ_WAV_0.1_TO_25_SECONDS")
            expected = source.getnframes() * source.getnchannels() * source.getsampwidth()
            if len(source.readframes(source.getnframes())) != expected:
                raise GnaniError("INVALID_AUDIO")
    except (wave.Error, EOFError, ZeroDivisionError):
        raise GnaniError("INVALID_AUDIO") from None
    return audio, duration


def curl_call(audio_path: Path, key: str, language: str, correlation: str) -> dict[str, object]:
    # Key goes through stdin config, never argv, history, or printed output.
    if any(c in key for c in "\r\n"):
        raise GnaniError("GNANI_NOT_CONFIGURED")
    quoted_key = key.replace("\\", "\\\\").replace('"', '\\"')
    config = f'header = "X-API-Key-ID: {quoted_key}"\n'
    try:
        completed = subprocess.run(
            [
                "curl.exe" if os.name == "nt" else "curl",
                "--disable",
                "--max-filesize",
                "1048576",
                "--silent",
                "--show-error",
                "--max-time",
                "60",
                "--request",
                "POST",
                "--url",
                STT_URL,
                "--config",
                "-",
                "--header",
                f"X-API-Request-ID: {correlation}",
                "--form",
                f"audio_file=@{audio_path.resolve()};type=audio/wav",
                "--form",
                f"language_code={language}",
                "--form",
                f"model={MODEL}",
                "--write-out",
                "\n%{http_code}",
            ],
            input=config,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=65,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise GnaniError("CURL_UNAVAILABLE_OR_TIMEOUT") from None
    if completed.returncode:
        raise GnaniError("CURL_TRANSPORT_FAILURE")
    try:
        body, code = completed.stdout.rsplit("\n", 1)
        payload = json.loads(body)
        status = int(code)
    except (ValueError, TypeError):
        raise GnaniError("GNANI_INVALID_RESPONSE") from None
    if status != 200:
        raise GnaniError("CURL_PROVIDER_FAILURE", status)
    if not isinstance(payload, dict):
        raise GnaniError("GNANI_INVALID_RESPONSE", status)
    from pydantic import ValidationError

    from app.integrations.gnani import ProviderResult

    try:
        result = ProviderResult.model_validate(payload)
    except ValidationError:
        raise GnaniError("GNANI_INVALID_RESPONSE", status) from None
    if not result.transcript.strip() or not result.request_id.strip():
        raise GnaniError("GNANI_EMPTY_PROOF", status)
    if result.model != MODEL or result.truncated:
        raise GnaniError("GNANI_INVALID_PROVENANCE", status)
    return {
        **result.model_dump(),
        "http_status": status,
        "correlation_id": correlation,
        "language_code": language,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--live", action="store_true", help="Explicitly spend a real API request")
    parser.add_argument("--synthetic-consented", action="store_true")
    parser.add_argument("--language", choices=["hi-IN", "en-IN", "ta-IN"], default="hi-IN")
    parser.add_argument("--transport", choices=["httpx", "curl"], default="httpx")
    args = parser.parse_args()
    if not args.live or not args.synthetic_consented:
        parser.error("Both --live and --synthetic-consented are required")
    load_dotenv(ROOT / ".env", override=False)
    try:
        audio, duration = validate_wav(args.audio)
        key = os.environ.get("GNANI_API_KEY_ID", "").strip()
        if not key or key.startswith("REPLACE"):
            raise GnaniError("GNANI_NOT_CONFIGURED")
        correlation = str(uuid4())
        if args.transport == "curl":
            result = curl_call(args.audio, key, args.language, correlation)
        else:
            client = GnaniSpeechClient(key, retries=0)
            result = asyncio.run(client.transcribe(audio, args.language, correlation)).model_dump()
        timestamp = datetime.now(UTC).isoformat()
        # Transcript retained privately; public proof contains no audio or transcript.
        private = ROOT / "private"
        private.mkdir(exist_ok=True)
        stem = f"gnani-{args.transport}-{correlation}"
        (private / f"{stem}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        safe = {k: v for k, v in result.items() if k not in {"transcript"}}
        safe.update(
            timestamp_utc=timestamp,
            transport=args.transport,
            audio_seconds=duration,
            audio_sha256=hashlib.sha256(audio).hexdigest(),
            transcript_nonempty=True,
            transcript_sha256=hashlib.sha256(str(result["transcript"]).encode()).hexdigest(),
        )
        target = ROOT / "docs/evidence" / f"{stem}.json"
        target.write_text(json.dumps(safe, indent=2), encoding="utf-8")
        print(f"Verified genuine {args.transport} response; sanitized evidence: {target}")
        print("G1 review still requires account/deployment-key confirmation; see tasks/todo.md")
        return 0
    except GnaniError as exc:
        print(f"Live gate NOT passed: {exc.code}; HTTP={exc.provider_status}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
