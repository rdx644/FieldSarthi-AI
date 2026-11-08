import asyncio
import io
import wave

import httpx
import pytest

from app.integrations.gnani import GnaniError
from app.integrations.tts import TimbreClient


def wav():
    target = io.BytesIO()
    with wave.open(target, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes(b"\0\0" * 4800)
    return target.getvalue()


def test_streaming_wav_header_is_repaired_using_actual_bytes():
    data = bytearray(wav())
    data[4:8] = (0xFFFFFFFF).to_bytes(4, "little")
    data[40:44] = (0xFFFFFFFF).to_bytes(4, "little")

    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda r: httpx.Response(
                    200, content=bytes(data), headers={"content-type": "audio/wav"}
                )
            )
        ) as http:
            return await TimbreClient("fixture-key", http=http).synthesize("WO-FIXTURE")

    output = asyncio.run(run())
    with wave.open(io.BytesIO(output), "rb") as w:
        assert w.getnframes() == 4800


@pytest.mark.parametrize("status", [401, 402, 403, 429, 500, 503])
def test_tts_failure_never_returns_success_audio(status):
    async def run():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda r: httpx.Response(status, json={"detail": "fixture-secret"})
            )
        ) as http:
            return await TimbreClient("fixture-key", http=http).synthesize("WO-FIXTURE")

    with pytest.raises(GnaniError, match="TTS_UNAVAILABLE"):
        asyncio.run(run())
