import json
import logging
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from starlette.exceptions import HTTPException
from starlette.responses import Response

from app.core.config import CORS_ORIGINS, ROOT
from app.core.errors import AppError
from app.core.limits import BodyLimit
from app.db.session import engine
from app.routers.auth import router as auth_router
from app.routers.intakes import router as intakes_router
from app.routers.orders import router as orders_router

app = FastAPI(title="FieldSaarthi AI", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Idempotency-Key",
        "X-Request-ID",
        "X-Requested-With",
    ],
)
logger = logging.getLogger("fieldsaarthi")
app.add_middleware(BodyLimit)


@app.middleware("http")
async def request_context(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request.state.request_id = str(uuid4())
    started = perf_counter()
    try:
        if (
            request.method in {"POST", "PATCH", "DELETE", "PUT"}
            and request.cookies.get("fieldsaarthi_session")
            and not request.headers.get("Authorization")
        ):
            origin = request.headers.get("Origin")
            allowed = [str(request.base_url).rstrip("/"), *CORS_ORIGINS]
            if origin not in allowed or request.headers.get("X-Requested-With") != "FieldSaarthi":
                raise AppError(403, "CSRF_REJECTED", "Refresh this page and try again.")
        response = await call_next(request)
    except AppError as exc:
        response = error_response(request, exc.status, exc.code, exc.message)
    except Exception:
        # Do not log exception values: they can include credentials, SQL or transcripts.
        logger.error(
            json.dumps({"event": "unhandled_error", "request_id": request.state.request_id})
        )
        response = error_response(
            request, 500, "INTERNAL_ERROR", "Something went wrong. Please retry."
        )
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "microphone=(self)"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; font-src 'self'; media-src 'self' blob:; "
        "connect-src 'self'; frame-ancestors 'none'"
    )
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    logger.info(
        json.dumps(
            {
                "request_id": request.state.request_id,
                "method": request.method,
                "status": response.status_code,
                "elapsed_ms": round((perf_counter() - started) * 1000),
            }
        )
    )
    return response


def error_response(request: Request, status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": getattr(request.state, "request_id", ""),
            }
        },
    )


@app.exception_handler(AppError)
async def app_error(request: Request, exc: AppError) -> JSONResponse:
    return error_response(request, exc.status, exc.code, exc.message)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    return error_response(request, 422, "INVALID_INPUT", "Check the required fields and try again.")


@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
    return error_response(
        request, exc.status_code, "REQUEST_FAILED", "The request could not be completed."
    )


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1 FROM alembic_version"))
    except Exception:
        raise AppError(
            503, "NOT_READY", "Database migrations or connectivity need attention."
        ) from None
    return {"status": "ready"}


app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(intakes_router)

web_dist = ROOT / "web/dist"
if (web_dist / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=web_dist / "assets"), name="web-assets")


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    if not (web_dist / "index.html").is_file():
        raise AppError(503, "FRONTEND_NOT_BUILT", "Build the frontend before starting the app.")
    return FileResponse(web_dist / "index.html")


@app.get("/favicon.svg", include_in_schema=False)
def favicon() -> FileResponse:
    return FileResponse(web_dist / "favicon.svg", media_type="image/svg+xml")
