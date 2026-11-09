"""Public JSON contracts. Historical extraction records may lack newer fields."""

from typing import Literal

from pydantic import BaseModel, Field, JsonValue

from app.schemas.commands import Issue, Priority, Status


class Provider(BaseModel):
    name: str
    model: str | None
    request_id: str | None


class Suggestions(BaseModel):
    location_id: str | None = None
    asset_id: str | None = None
    issue_category: Issue = "OTHER"
    priority_suggestion: Priority = "NORMAL"


class EvidenceSpan(BaseModel):
    text: str
    start: int
    end: int


class AssetCandidate(BaseModel):
    id: str
    name: str
    location_id: str


class IntakeResponse(BaseModel):
    id: str
    intake_id: str
    source_type: Literal["GNANI_STT", "MANUAL_TEXT"]
    status: str
    input_language_code: str
    raw_transcript: str | None
    edited_transcript: str | None
    provider: Provider | None
    audio_duration_seconds: float | None
    stt_latency_ms: int | None
    error_code: str | None
    parser_version: str | None = None
    suggested_fields: Suggestions = Field(default_factory=Suggestions)
    field_evidence: dict[str, list[str]] = Field(default_factory=dict)
    evidence_spans: dict[str, list[EvidenceSpan]] = Field(default_factory=dict)
    asset_candidates: list[AssetCandidate] = Field(default_factory=list)
    unresolved_fields: list[str] = Field(default_factory=list)
    needs_review: bool = True
    emergency_warning: bool = False
    possible_duplicates: int = 0


class AuditResponse(BaseModel):
    id: str
    action: str
    actor_name: str
    from_state: str | None
    to_state: str | None
    details: dict[str, JsonValue]
    occurred_at: str


class OrderResponse(BaseModel):
    id: str
    public_code: str
    intake_id: str
    reporter_id: str
    location_id: str
    asset_id: str
    asset_name: str
    location_name: str
    issue_category: Issue
    description: str
    priority: Priority
    priority_suggestion: Priority
    status: Status
    assignee_id: str | None
    assignee_name: str | None
    version: int
    created_at: str
    updated_at: str
    resolved_at: str | None
    intake: IntakeResponse | None = None
    audit: list[AuditResponse] = Field(default_factory=list)


class QueueResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int


class UserResponse(BaseModel):
    id: str
    display_name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class SessionResponse(BaseModel):
    user: UserResponse | None


class LocationResponse(BaseModel):
    id: str
    code: str
    name: str


class AssetResponse(AssetCandidate):
    asset_code: str
