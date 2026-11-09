"""Allowlisted stage events: no bodies, transcripts, credentials or exception text."""

import json
import logging
from time import perf_counter


def stage_event(
    request_id: str,
    stage: str,
    started: float,
    *,
    code: str = "OK",
    model: str | None = None,
    provider_request_id: str | None = None,
) -> None:
    logging.getLogger("fieldsaarthi").info(
        json.dumps(
            {
                "event": "stage_completed",
                "entry_point": "http_api",
                "request_id": request_id,
                "stage": stage,
                "code": code,
                "elapsed_ms": round((perf_counter() - started) * 1000),
                "provider_model": model,
                "provider_request_id": provider_request_id,
            }
        )
    )
