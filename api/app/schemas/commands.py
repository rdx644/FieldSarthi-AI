from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Priority = Literal["LOW", "NORMAL", "HIGH"]
Issue = Literal["LEAKAGE", "ELECTRICAL", "MECHANICAL", "CLEANING", "OTHER"]
Status = Literal["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CANCELLED"]


class Command(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Login(Command):
    email: str = Field(min_length=3, max_length=200)
    password: str = Field(min_length=1, max_length=200)


class Confirm(Command):
    intake_id: str = Field(min_length=36, max_length=36)
    location_id: str = Field(min_length=36, max_length=36)
    asset_id: str = Field(min_length=36, max_length=36)
    issue_category: Issue
    description: str = Field(min_length=5, max_length=2000)
    priority_suggestion: Priority = "NORMAL"
    edited_transcript: str | None = Field(default=None, max_length=4000)
    confirmed: Literal[True]

    @field_validator("confirmed", mode="before")
    @classmethod
    def explicit_confirmation(cls, value: object) -> object:
        if value is not True:
            raise ValueError("Explicit JSON true confirmation is required")
        return value


class Review(Command):
    edited_transcript: str = Field(min_length=1, max_length=4000)


class ManualIntake(Command):
    text: str = Field(min_length=5, max_length=4000)
    language_code: Literal["hi-IN", "en-IN", "ta-IN"] = "hi-IN"


class Assignment(Command):
    assignee_id: str = Field(min_length=36, max_length=36)
    expected_version: int = Field(ge=1)


class PriorityChange(Command):
    priority: Priority
    expected_version: int = Field(ge=1)


class StatusChange(Command):
    status: Status
    expected_version: int = Field(ge=1)
    resolution_note: str | None = Field(default=None, max_length=1000)
    cancellation_note: str | None = Field(default=None, max_length=1000)
