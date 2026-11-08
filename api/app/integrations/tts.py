"""Gnani Timbre binary response; no invented provider response metadata."""

import asyncio
import io
import wave

import httpx

from app.integrations.gnani import GnaniError

TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"
provider_slots = asyncio.Semaphore(1)


def canonical_wav(data: bytes) -> bytes:
    try:
        with wave.open(io.BytesIO(data), "rb") as source:
            if (
                source.getnchannels() != 1
                or source.getsampwidth() != 2
                or source.getframerate() != 48000
                or source.getcomptype() != "NONE"
            ):
                raise GnaniError("TTS_INVALID_AUDIO")
            pcm = source.readframes(48000 * 31)
        # Streaming RIFF files can declare 0xffffffff rather than final byte length.
        if not pcm or len(pcm) > 48000 * 2 * 30 or len(pcm) % 2:
            raise GnaniError("TTS_INVALID_AUDIO")
        target = io.BytesIO()
        with wave.open(target, "wb") as result:
            result.setnchannels(1)
            result.setsampwidth(2)
            result.setframerate(48000)
            result.writeframes(pcm)
        return target.getvalue()
    except (wave.Error, EOFError):
        raise GnaniError("TTS_INVALID_AUDIO") from None


class TimbreClient:
    def __init__(self, key: str, *, http: httpx.AsyncClient | None = None) -> None:
        self._key = key
        self._http = http

    async def synthesize(self, code: str) -> bytes:
        if self._http is None:
            async with httpx.AsyncClient(follow_redirects=False) as http:
                return await self._request(http, code)
        return await self._request(self._http, code)

    async def _request(self, http: httpx.AsyncClient, code: str) -> bytes:
        try:
            async with asyncio.timeout(60):
                async with http.stream(
                    "POST",
                    TTS_URL,
                    headers={"X-API-Key-ID": self._key},
                    json={
                        "text": f"आपकी शिकायत दर्ज हो गई है। टिकट नंबर {code}।",
                        "model": "timbre-v2.5",
                        "voice": "Nalini",
                        "language": "hi-IN",
                        "speed": 1.0,
                        "audio_config": {
                            "sample_rate": 48000,
                            "num_channels": 1,
                            "sample_width": 2,
                            "encoding": "linear_pcm",
                            "container": "wav",
                        },
                    },
                    timeout=45,
                    follow_redirects=False,
                ) as response:
                    if response.status_code != 200:
                        raise GnaniError("TTS_UNAVAILABLE", response.status_code)
                    data = bytearray()
                    async for chunk in response.aiter_bytes():
                        data.extend(chunk)
                        if len(data) > 4_000_000:
                            raise GnaniError("TTS_INVALID_AUDIO")
                return canonical_wav(bytes(data))
        except (httpx.RequestError, TimeoutError):
            raise GnaniError("TTS_UNAVAILABLE") from None
