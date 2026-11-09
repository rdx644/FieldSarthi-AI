"""FR-06..09: real Prisma v2.5 REST adapter. No production fixture path.
Contract: https://docs.gnani.ai/api/STT/speech-to-text
HTTPX: https://www.python-httpx.org/advanced/timeouts/
"""

from __future__ import annotations

import asyncio
import json
import random
from time import perf_counter
from typing import Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

STT_URL = "https://api.vachana.ai/stt/v3"
MODEL = "prisma-v2.5"
MAX_RESPONSE_BYTES = 1_048_576


class GnaniError(Exception):
    """Only safe application codes leave the integration boundary."""

    def __init__(self, code: str, provider_status: int | None = None) -> None:
        self.code = code
        self.provider_status = provider_status
        super().__init__(code)


class ProviderResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="ignore")
    success: Literal[True]

    @field_validator("success", mode="before")
    @classmethod
    def require_true(cls, value: object) -> object:
        if value is not True:
            raise ValueError("success must be JSON true")
        return value

    transcript: str
    request_id: str = Field(min_length=1, max_length=160, pattern=r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    model: str = Field(min_length=1)
    truncated: bool = False
    processing_time: float | None = Field(default=None, ge=0, allow_inf_nan=False)
    end_to_end_latency: float | None = Field(default=None, ge=0, allow_inf_nan=False)


class Transcription(ProviderResult):
    correlation_id: str
    language_code: str
    http_status: int
    elapsed_seconds: float


class GnaniSpeechClient:
    """Use one shared instance per process; its semaphore serializes provider calls.

    The caller owns AsyncClient lifecycle. Retries are capped at two and never
    applied after read/write timeout, where billing outcome may be uncertain.
    """

    def __init__(
        self, api_key: str, *, http: httpx.AsyncClient | None = None, retries: int = 1
    ) -> None:
        if not api_key.strip() or api_key.startswith("REPLACE"):
            raise GnaniError("GNANI_NOT_CONFIGURED")
        if retries not in (0, 1, 2):
            raise ValueError("retries must be 0, 1 or 2")
        self._api_key = api_key
        self._http = http
        self._retries = retries
        self._semaphore = asyncio.Semaphore(1)

    async def transcribe(
        self,
        audio_bytes: bytes,
        language: str,
        correlation_id: str,
        *,
        filename: str = "report.wav",
    ) -> Transcription:
        if language not in {"hi-IN", "en-IN", "ta-IN"}:
            raise GnaniError("INVALID_LANGUAGE")
        if not audio_bytes or len(audio_bytes) > 10_485_760:
            raise GnaniError("INVALID_AUDIO")
        if not correlation_id.strip() or len(correlation_id) > 128:
            raise GnaniError("INVALID_CORRELATION_ID")
        if self._http is None:
            async with httpx.AsyncClient(follow_redirects=False) as http:
                return await self._transcribe(http, audio_bytes, language, correlation_id, filename)
        return await self._transcribe(self._http, audio_bytes, language, correlation_id, filename)

    async def _transcribe(
        self, http: httpx.AsyncClient, audio: bytes, language: str, correlation: str, filename: str
    ) -> Transcription:
        async with self._semaphore:
            started = perf_counter()
            for attempt in range(self._retries + 1):
                try:
                    # Overall wall deadline also bounds a slow trickle response.
                    async with asyncio.timeout(60):
                        result, status = await self._request(
                            http, audio, language, correlation, filename
                        )
                    return Transcription(
                        **result.model_dump(),
                        correlation_id=correlation,
                        language_code=language,
                        http_status=status,
                        elapsed_seconds=perf_counter() - started,
                    )
                except (httpx.ConnectError, httpx.ConnectTimeout):
                    error = GnaniError("GNANI_UNAVAILABLE")
                    retryable = True
                except (httpx.TimeoutException, TimeoutError):
                    raise GnaniError("GNANI_TIMEOUT") from None
                except httpx.RequestError:
                    raise GnaniError("GNANI_UNAVAILABLE") from None
                except GnaniError as exc:
                    error = exc
                    retryable = exc.provider_status in {429, 502, 503, 504}
                if not retryable or attempt == self._retries:
                    raise error from None
                await asyncio.sleep(min(2.0, 0.25 * 2**attempt + random.uniform(0, 0.15)))
        raise AssertionError("unreachable")

    async def _request(
        self, http: httpx.AsyncClient, audio: bytes, language: str, correlation: str, filename: str
    ) -> tuple[ProviderResult, int]:
        # HTTPX creates the multipart boundary. Never set Content-Type manually.
        async with http.stream(
            "POST",
            STT_URL,
            headers={"X-API-Key-ID": self._api_key, "X-API-Request-ID": correlation},
            data={"language_code": language, "model": MODEL},
            files={"audio_file": (filename, audio, "audio/wav")},
            timeout=httpx.Timeout(45.0, connect=10.0, pool=5.0),
            follow_redirects=False,
        ) as response:
            status = response.status_code
            if status != 200:
                code = {
                    400: "GNANI_INVALID_REQUEST",
                    422: "GNANI_INVALID_REQUEST",
                    401: "GNANI_AUTH_FAILURE",
                    403: "GNANI_AUTH_FAILURE",
                    402: "GNANI_QUOTA_EXHAUSTED",
                    429: "GNANI_RATE_LIMITED",
                    504: "GNANI_TIMEOUT",
                }.get(status, "GNANI_TRANSCRIPTION_FAILED")
                raise GnaniError(code, status)
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise GnaniError("GNANI_INVALID_RESPONSE", status)
        try:
            payload = json.loads(body)
            # Short/no-speech responses legitimately omit model/timings.
            if (
                isinstance(payload, dict)
                and payload.get("success") is True
                and isinstance(payload.get("transcript"), str)
                and not payload["transcript"].strip()
            ):
                raise GnaniError("NO_SPEECH_DETECTED", status)
            result = ProviderResult.model_validate(payload)
        except (ValueError, ValidationError):
            raise GnaniError("GNANI_INVALID_RESPONSE", status) from None
        if not result.request_id.strip() or result.model != MODEL:
            raise GnaniError("GNANI_INVALID_PROVENANCE", status)
        if result.truncated:
            raise GnaniError("GNANI_TRUNCATED_TRANSCRIPT", status)
        return result, status
