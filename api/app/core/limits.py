import os

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.errors import AppError


class BodyLimit:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        cap = 10_485_760 + 131_072 if scope["path"] == "/api/v1/intakes/transcribe" else 65_536
        headers = dict(scope.get("headers", []))
        try:
            length = int(headers.get(b"content-length", b"0"))
            if length < 0:
                raise ValueError
        except ValueError:
            length = cap + 1
        if length > cap:
            response = JSONResponse(
                {
                    "error": {
                        "code": "BODY_TOO_LARGE",
                        "message": "This upload is too large.",
                        "request_id": scope.get("state", {}).get("request_id", ""),
                    }
                },
                status_code=413,
            )
            await response(scope, receive, send)
            return
        total = 0

        async def limited_receive() -> Message:
            nonlocal total
            message = await receive()
            total += len(message.get("body", b""))
            if total > cap:
                raise AppError(413, "BODY_TOO_LARGE", "This upload is too large.")
            return message

        await self.app(scope, limited_receive, send)


def provider_requests_enabled() -> bool:
    """An unset flag preserves the demo default; explicit invalid values pause it."""
    return os.getenv("GNANI_REQUESTS_ENABLED", "true").lower() == "true"


def ensure_provider_requests_enabled() -> None:
    if not provider_requests_enabled():
        raise AppError(
            503,
            "GNANI_REQUESTS_PAUSED",
            "Live audio is paused by the operator. Type your report; saved work remains available.",
        )


class ProviderBudget:
    """Shared durable operation admission. Audio execution still uses one worker."""

    def check(self, actor_id: str, operation: str = "STT") -> None:
        ensure_provider_requests_enabled()
        if operation not in {"STT", "TTS"}:
            raise AppError(422, "INVALID_PROVIDER_OPERATION", "Unsupported audio operation.")
        from app.services.provider_admission import reserve_provider_admission

        reserve_provider_admission(actor_id, operation)


provider_budget = ProviderBudget()
