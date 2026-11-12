from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


_COMMUNITY_RE = re.compile(r"^[A-Za-z0-9_-]{3,24}$")
_IATA_RE = re.compile(r"^[A-Z]{3}$")
_LOCAL_DT_FMT = "%Y-%m-%dT%H:%M"


def _clean_community(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    if not _COMMUNITY_RE.match(v):
        raise ValueError("community must be 3-24 chars: letters, numbers, '-' or '_'")
    return v


# ---- Profile -----------------------------------------------------------
class ProfileIn(BaseModel):
    displayName: str = Field(default="", max_length=60)
    avatar: str = Field(default="🙂", max_length=8)
    locale: Literal["pt", "en", "es"] = "pt"
    email: str | None = Field(default=None, max_length=120)
    community: str | None = Field(default=None, max_length=24)
    updatedAt: str | None = None

    @field_validator("community")
    @classmethod
    def _v_community(cls, v: str | None) -> str | None:
        return _clean_community(v)


class ProfileOut(BaseModel):
    displayName: str = ""
    avatar: str = "🙂"
    locale: Literal["pt", "en", "es"] = "pt"
    community: str = "CommunityBR"
    updatedAt: str | None = None


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
    statusText: str | None = Field(default=None, max_length=80)

    def validate_mode(self) -> None:
        if self.mode == "venue" and not self.venueId:
            raise ValueError("venueId required when mode is 'venue'")
        if self.mode == "gps" and (self.lat is None or self.lng is None):
            raise ValueError("lat and lng required when mode is 'gps'")


class Peer(BaseModel):
    sub: str
    displayName: str
    avatar: str
    isPepper: bool = False
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


# ---- Flights (Feature 14) ----------------------------------------------
class FlightIn(BaseModel):
    originIata: str
    destIata: str
    departAt: str  # local time at origin, "YYYY-MM-DDTHH:MM"
    arriveAt: str  # local time at destination, "YYYY-MM-DDTHH:MM"
    flightNumber: str | None = Field(default=None, max_length=8)
    note: str | None = Field(default=None, max_length=80)

    @field_validator("originIata", "destIata")
    @classmethod
    def _iata(cls, v: str) -> str:
        v = v.strip().upper()
        if not _IATA_RE.match(v):
            raise ValueError("IATA code must be 3 letters")
        return v

    @field_validator("departAt", "arriveAt")
    @classmethod
    def _local_dt(cls, v: str) -> str:
        datetime.strptime(v, _LOCAL_DT_FMT)  # raises ValueError -> 422
        return v

    @field_validator("flightNumber")
    @classmethod
    def _fn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            return None
        if not re.match(r"^[A-Z0-9 ]{2,8}$", v):
            raise ValueError("invalid flight number")
        return v

    @field_validator("note")
    @classmethod
    def _note(cls, v: str | None) -> str | None:
        return (v.strip() or None) if v else None

    def validate_route(self) -> None:
        if self.originIata == self.destIata:
            raise ValueError("origin and destination must differ")


class FlightOut(BaseModel):
    id: str
    sub: str
    displayName: str
    avatar: str
    isPepper: bool = False
    originIata: str
    destIata: str
    departAt: str
    arriveAt: str
    flightNumber: str | None = None
    note: str | None = None
    mine: bool = False
