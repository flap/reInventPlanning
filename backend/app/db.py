"""DynamoDB single-table access layer (ADR-010).

Table (single-table design), PK/SK:

  USER#{sub}  PROFILE                -> profile
  USER#{sub}  PLAN#checklist         -> checklist state
  USER#{sub}  PLAN#budget            -> budget state
  USER#{sub}  PLAN#trip              -> trip state
  SHARE#{scope}  USER#{sub}          -> ephemeral location (TTL via `expiresAt`)
  USER#{sub}  FLIGHT#{id}            -> flight leg (owner copy, TTL)
  FLIGHT#{scope}  {sub}#{id}         -> flight leg (community index, TTL)

`scope` is the user's community (profile.community, upper-cased), derived
server-side (ADR-012). The legacy "GLOBAL" scope no longer exists.
Location items always carry `expiresAt` (epoch seconds) so DynamoDB TTL removes
them automatically even if the client disappears.
"""

from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from app.config import settings

_PLAN_KINDS = ("checklist", "budget", "trip")


def _now() -> int:
    return int(time.time())


def scope_for(profile: dict[str, Any] | None) -> str:
    """Community scope for a profile (ADR-012). Defaults to CommunityBR."""
    community = ((profile or {}).get("community") or settings.default_community).strip()
    return community.upper()


def _epoch_from_local(local_dt: str) -> int:
    # Local airport time has no zone; interpret as UTC. The 72h TTL margin
    # absorbs any offset error.
    dt = datetime.strptime(local_dt, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


class Repository:
    def __init__(self) -> None:
        kwargs: dict[str, Any] = {"region_name": settings.aws_region}
        if settings.dynamodb_endpoint_url:
            kwargs["endpoint_url"] = settings.dynamodb_endpoint_url
        self._table = boto3.resource("dynamodb", **kwargs).Table(settings.table_name)

    # ---- Profile -------------------------------------------------------
    def get_profile(self, sub: str) -> dict[str, Any] | None:
        resp = self._table.get_item(Key={"PK": f"USER#{sub}", "SK": "PROFILE"})
        return resp.get("Item")

    def put_profile(self, sub: str, data: dict[str, Any]) -> dict[str, Any]:
        item = {
            "PK": f"USER#{sub}",
            "SK": "PROFILE",
            "displayName": data.get("displayName", ""),
            "avatar": data.get("avatar", "🙂"),
            "locale": data.get("locale", "pt"),
            "updatedAt": data.get("updatedAt") or _iso_now(),
        }
        old = self.get_profile(sub) or {}
        # Omitted community keeps the current one (older clients); else default.
        item["community"] = (
            data.get("community") or old.get("community") or settings.default_community
        )
        # Email is stored ONLY to derive the isPepper highlight server-side.
        # It is never returned in peer listings (privacy: ADR-011 minimization).
        email = (data.get("email") or "").strip().lower()
        if email:
            item["email"] = email
        self._table.put_item(Item=item)
        old_scope, new_scope = scope_for(old), scope_for(item)
        if old_scope != new_scope:
            # Community changed: stop sharing in the old community and move flights.
            self.delete_share(sub, old_scope)
            self._reindex_flights(sub, old_scope, new_scope)
        return item

    # ---- Plan (checklist / budget / trip) ------------------------------
    def get_plan(self, sub: str) -> dict[str, Any]:
        resp = self._table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{sub}")
            & Key("SK").begins_with("PLAN#")
        )
        plan: dict[str, Any] = {}
        for item in resp.get("Items", []):
            kind = str(item["SK"]).split("#", 1)[1]
            plan[kind] = item.get("data")
        return plan

    def put_plan_kind(
        self, sub: str, kind: str, data: dict[str, Any], updated_at: str
    ) -> dict[str, Any]:
        if kind not in _PLAN_KINDS:
            raise ValueError(f"invalid plan kind: {kind}")
        # Last-write-wins: only overwrite if incoming updatedAt is newer.
        existing = self._table.get_item(
            Key={"PK": f"USER#{sub}", "SK": f"PLAN#{kind}"}
        ).get("Item")
        if existing and existing.get("updatedAt", "") > updated_at:
            return existing
        item = {
            "PK": f"USER#{sub}",
            "SK": f"PLAN#{kind}",
            "data": data,
            "updatedAt": updated_at,
        }
        self._table.put_item(Item=item)
        return item

    # ---- Location share (ephemeral, TTL) -------------------------------
    def put_share(
        self,
        sub: str,
        *,
        scope: str,
        mode: str,
        display_name: str,
        avatar: str,
        venue_id: str | None,
        lat: float | None,
        lng: float | None,
        status_text: str | None,
        ttl_seconds: int,
        is_pepper: bool = False,
    ) -> dict[str, Any]:
        now = _now()
        item: dict[str, Any] = {
            "PK": f"SHARE#{scope}",
            "SK": f"USER#{sub}",
            "sub": sub,
            "scope": scope,
            "mode": mode,
            "displayName": display_name,
            "avatar": avatar,
            "isPepper": is_pepper,
            "sharedAt": now,
            "expiresAt": now + ttl_seconds,
        }
        if mode == "venue":
            item["venueId"] = venue_id
        elif mode == "gps":
            item["lat"] = str(lat)
            item["lng"] = str(lng)
        if status_text:
            item["statusText"] = status_text[:80]
        self._table.put_item(Item=item)
        return item

    def delete_share(self, sub: str, scope: str) -> None:
        self._table.delete_item(Key={"PK": f"SHARE#{scope}", "SK": f"USER#{sub}"})

    def get_my_share(self, sub: str, scope: str) -> dict[str, Any] | None:
        item = self._table.get_item(
            Key={"PK": f"SHARE#{scope}", "SK": f"USER#{sub}"}
        ).get("Item")
        if not item:
            return None
        # Defensive: honor expiry even if TTL sweep hasn't run yet.
        if int(item.get("expiresAt", 0)) <= _now():
            return None
        return item

    def list_shares(self, scope: str) -> list[dict[str, Any]]:
        resp = self._table.query(
            KeyConditionExpression=Key("PK").eq(f"SHARE#{scope}")
        )
        now = _now()
        return [i for i in resp.get("Items", []) if int(i.get("expiresAt", 0)) > now]

    # ---- Flights (Feature 14) ------------------------------------------
    def list_my_flights(self, sub: str) -> list[dict[str, Any]]:
        resp = self._table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{sub}")
            & Key("SK").begins_with("FLIGHT#")
        )
        now = _now()
        return [i for i in resp.get("Items", []) if int(i.get("expiresAt", 0)) > now]

    def add_flight(
        self, sub: str, scope: str, data: dict[str, Any], owner: dict[str, Any]
    ) -> dict[str, Any]:
        flight_id = uuid.uuid4().hex[:12]
        item: dict[str, Any] = {
            "id": flight_id,
            "sub": sub,
            "scope": scope,
            "displayName": owner.get("displayName") or "re:Invent peer",
            "avatar": owner.get("avatar") or "🙂",
            "isPepper": bool(owner.get("isPepper", False)),
            "originIata": data["originIata"],
            "destIata": data["destIata"],
            "departAt": data["departAt"],
            "arriveAt": data["arriveAt"],
            "expiresAt": _epoch_from_local(data["arriveAt"])
            + settings.flight_ttl_after_arrival_seconds,
        }
        if data.get("flightNumber"):
            item["flightNumber"] = data["flightNumber"]
        if data.get("note"):
            item["note"] = data["note"]
        self._table.put_item(Item={"PK": f"USER#{sub}", "SK": f"FLIGHT#{flight_id}", **item})
        self._table.put_item(
            Item={"PK": f"FLIGHT#{scope}", "SK": f"{sub}#{flight_id}", **item}
        )
        return item

    def delete_flight(self, sub: str, flight_id: str) -> bool:
        owner = self._table.get_item(
            Key={"PK": f"USER#{sub}", "SK": f"FLIGHT#{flight_id}"}
        ).get("Item")
        if not owner:
            return False
        self._table.delete_item(Key={"PK": f"USER#{sub}", "SK": f"FLIGHT#{flight_id}"})
        self._table.delete_item(
            Key={"PK": f"FLIGHT#{owner['scope']}", "SK": f"{sub}#{flight_id}"}
        )
        return True

    def list_flights(self, scope: str) -> list[dict[str, Any]]:
        resp = self._table.query(KeyConditionExpression=Key("PK").eq(f"FLIGHT#{scope}"))
        now = _now()
        return [i for i in resp.get("Items", []) if int(i.get("expiresAt", 0)) > now]

    def _reindex_flights(self, sub: str, old_scope: str, new_scope: str) -> None:
        for f in self.list_my_flights(sub):
            fid = f["id"]
            self._table.delete_item(
                Key={"PK": f"FLIGHT#{old_scope}", "SK": f"{sub}#{fid}"}
            )
            moved = {**f, "scope": new_scope}
            self._table.put_item(Item=moved)  # owner copy keeps new scope
            self._table.put_item(
                Item={**moved, "PK": f"FLIGHT#{new_scope}", "SK": f"{sub}#{fid}"}
            )

    # ---- Account deletion (right to erasure, F11.8) --------------------
    def delete_all_user_data(self, sub: str) -> int:
        """Delete profile + plan + flights + any share items for the user."""
        deleted = 0
        scope = scope_for(self.get_profile(sub))
        # Community-partition copies first (we need the owner copies to find them).
        for f in self.list_my_flights(sub):
            self._table.delete_item(Key={"PK": f"FLIGHT#{f['scope']}", "SK": f"{sub}#{f['id']}"})
            deleted += 1
        # Current community + legacy GLOBAL share items.
        for sc in {scope, "GLOBAL"}:
            key = {"PK": f"SHARE#{sc}", "SK": f"USER#{sub}"}
            if self._table.get_item(Key=key).get("Item"):
                self._table.delete_item(Key=key)
                deleted += 1
        # USER# partition (profile + plan + flight owner copies)
        resp = self._table.query(KeyConditionExpression=Key("PK").eq(f"USER#{sub}"))
        with self._table.batch_writer() as batch:
            for item in resp.get("Items", []):
                batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
                deleted += 1
        return deleted


def _iso_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


# Lazily-instantiated singleton so importing the module doesn't require AWS creds.
_repo: Repository | None = None


def get_repository() -> Repository:
    global _repo
    if _repo is None:
        _repo = Repository()
    return _repo
