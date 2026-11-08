"""FR-06..09: provider fixtures exist only in tests, never live evidence."""

import asyncio

import httpx
import pytest

from app.integrations.gnani import GnaniError, GnaniSpeechClient

KEY = "contract-test-secret"
GOOD = {
    "success": True,
    "transcript": "  पंप में रिसाव है।  ",
    "request_id": "fixture-request",
    "model": "prisma-v2.5",
}


def call(body=None, status=200, failure=None, **kwargs):
    requests = []

    def handler(request):
        requests.append(request)
        if failure:
            raise failure("failure", request=request)
        return httpx.Response(status, json=body)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = GnaniSpeechClient(KEY, http=http, retries=0)
            return await client.transcribe(b"audio", "hi-IN", "correlation", **kwargs)

    return asyncio.run(run()), requests


def test_success_preserves_raw_transcript_and_real_provenance():
    result, requests = call(GOOD)
    assert result.transcript == GOOD["transcript"]
    assert result.request_id == "fixture-request"
    assert result.model == "prisma-v2.5"
    assert result.http_status == 200
    assert result.correlation_id == "correlation"
    request = requests[0]
    assert str(request.url) == "https://api.vachana.ai/stt/v3"
    assert request.headers["X-API-Key-ID"] == KEY
    assert "boundary=" in request.headers["Content-Type"]
    assert b"hi-IN" in request.content and b"prisma-v2.5" in request.content
    assert b'name="audio_file"' in request.content


@pytest.mark.parametrize(
    "body", [{"success": True, "transcript": "", "request_id": "x"}, {**GOOD, "transcript": "  "}]
)
def test_no_speech_is_not_success(body):
    with pytest.raises(GnaniError, match="NO_SPEECH_DETECTED"):
        call(body)


@pytest.mark.parametrize(
    "status,code",
    [
        (400, "GNANI_INVALID_REQUEST"),
        (401, "GNANI_AUTH_FAILURE"),
        (402, "GNANI_QUOTA_EXHAUSTED"),
        (403, "GNANI_AUTH_FAILURE"),
        (422, "GNANI_INVALID_REQUEST"),
        (429, "GNANI_RATE_LIMITED"),
        (500, "GNANI_TRANSCRIPTION_FAILED"),
        (502, "GNANI_TRANSCRIPTION_FAILED"),
        (503, "GNANI_TRANSCRIPTION_FAILED"),
        (504, "GNANI_TIMEOUT"),
    ],
)
def test_http_status_is_authoritative_and_secret_safe(status, code):
    with pytest.raises(GnaniError) as exc:
        call({"success": True, "detail": KEY}, status)
    assert exc.value.code == code
    assert exc.value.provider_status == status
    assert KEY not in str(exc.value)


@pytest.mark.parametrize(
    "failure,code",
    [(httpx.ReadTimeout, "GNANI_TIMEOUT"), (httpx.ConnectError, "GNANI_UNAVAILABLE")],
)
def test_network_failure_is_explicit(failure, code):
    with pytest.raises(GnaniError, match=code):
        call(failure=failure)


@pytest.mark.parametrize(
    "patch",
    [
        {"success": False},
        {"success": "true"},
        {"request_id": ""},
        {"model": ""},
        {"model": "prisma-v3.0"},
        {"transcript": 123},
        {"truncated": True},
    ],
)
def test_bad_or_incomplete_provider_proof_is_rejected(patch):
    with pytest.raises(GnaniError):
        call({**GOOD, **patch})


def test_invalid_language_never_reaches_provider():
    with pytest.raises(GnaniError, match="INVALID_LANGUAGE"):

        async def run():
            async with httpx.AsyncClient() as http:
                await GnaniSpeechClient(KEY, http=http).transcribe(b"x", "indic-auto", "c")

        asyncio.run(run())


def test_empty_key_rejected():
    with pytest.raises(GnaniError, match="GNANI_NOT_CONFIGURED"):
        GnaniSpeechClient("")


def test_retry_is_bounded_for_transient_status():
    attempts = []

    def handler(request):
        attempts.append(request)
        return httpx.Response(503, json={"detail": "unavailable"})

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            await GnaniSpeechClient(KEY, http=http, retries=1).transcribe(b"x", "hi-IN", "c")

    with pytest.raises(GnaniError):
        asyncio.run(run())
    assert len(attempts) == 2


def test_auth_failure_is_never_retried():
    attempts = []

    def handler(request):
        attempts.append(request)
        return httpx.Response(401, json={"detail": "private"})

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            await GnaniSpeechClient(KEY, http=http, retries=2).transcribe(b"x", "hi-IN", "c")

    with pytest.raises(GnaniError):
        asyncio.run(run())
    assert len(attempts) == 1


def test_invalid_json_and_large_response_are_rejected():
    for content in [b"not-json", b"x" * 1_048_577]:

        async def run(body=content):
            transport = httpx.MockTransport(lambda r: httpx.Response(200, content=body))
            async with httpx.AsyncClient(transport=transport) as http:
                return await GnaniSpeechClient(KEY, http=http).transcribe(b"x", "hi-IN", "c")

        with pytest.raises(GnaniError, match="GNANI_INVALID_RESPONSE"):
            asyncio.run(run())


def test_numeric_success_is_not_true():
    with pytest.raises(GnaniError, match="GNANI_INVALID_RESPONSE"):
        call({**GOOD, "success": 1})
