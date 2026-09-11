from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


# ---- Profile -----------------------------------------------------------
class ProfileIn(BaseModel):
    displayName: str = Field(default="", max_length=60)
    avatar: str = Field(default="🙂", max_length=8)
    locale: Literal["pt", "en", "es"] = "pt"
    updatedAt: str | None = None


class ProfileOut(ProfileIn):
    pass


# ---- Plan --------------------------------------------------------------
class PlanKindIn(BaseModel):
    data: dict[str, Any]
    updatedAt: str


class PlanOut(BaseModel):
    checklist: dict[str, Any] | None = None
    budget: dict[str, Any] | None = None
    trip: dict[str, Any] | None = None


# ---- Location share ----------------------------------------------------
class ShareIn(BaseModel):
    mode: Literal["venue", "gps"]
    venueId: str | None = None
    lat: float | None = None
    lng: float | None = None
    durationMin: int = Field(ge=5, le=240)  # 5 min .. 4h
    crewCode: str | None = Field(default=None, max_length=24)
    statusText: str | None = Field(default=None, max_length=80)

    @field_validator("crewCode")
    @classmethod
    def _clean_crew(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        return v or None

    def validate_mode(self) -> None:
        if self.mode == "venue" and not self.venueId:
            raise ValueError("venueId required when mode is 'venue'")
        if self.mode == "gps" and (self.lat is None or self.lng is None):
            raise ValueError("lat and lng required when mode is 'gps'")


class Peer(BaseModel):
    sub: str
    displayName: str
    avatar: str
    mode: Literal["venue", "gps"]
    venueId: str | None = None
    lat: float | None = None
    lng: float | None = None
    statusText: str | None = None
    sharedAt: int
    expiresAt: int


class ShareStatus(BaseModel):
    sharing: bool
    scope: str | None = None
    mode: Literal["venue", "gps"] | None = None
    venueId: str | None = None
    expiresAt: int | None = None
