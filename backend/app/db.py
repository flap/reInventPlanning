"""DynamoDB single-table access layer (ADR-010).

Table (single-table design), PK/SK:

  USER#{sub}  PROFILE                -> profile
  USER#{sub}  PLAN#checklist         -> checklist state
  USER#{sub}  PLAN#budget            -> budget state
  USER#{sub}  PLAN#trip              -> trip state
  SHARE#{scope}  USER#{sub}          -> ephemeral location (TTL via `expiresAt`)

`scope` is either "GLOBAL" (open reciprocal pool) or a crew code.
Location items always carry `expiresAt` (epoch seconds) so DynamoDB TTL removes
them automatically even if the client disappears.
"""

from __future__ import annotations

import time
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from app.config import settings

_PLAN_KINDS = ("checklist", "budget", "trip")


def _now() -> int:
    return int(time.time())


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
        self._table.put_item(Item=item)
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

    # ---- Account deletion (right to erasure, F11.8) --------------------
    def delete_all_user_data(self, sub: str) -> int:
        """Delete profile + plan items + any share items for the user."""
        deleted = 0
        # USER# partition (profile + plan)
        resp = self._table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{sub}")
        )
        with self._table.batch_writer() as batch:
            for item in resp.get("Items", []):
                batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
                deleted += 1
        # Share items live under SHARE#{scope} partitions; we can't query by sub
        # without a GSI, so callers pass known scopes. GLOBAL is always cleaned.
        for scope in ("GLOBAL",):
            existing = self._table.get_item(
                Key={"PK": f"SHARE#{scope}", "SK": f"USER#{sub}"}
            ).get("Item")
            if existing:
                self._table.delete_item(
                    Key={"PK": f"SHARE#{scope}", "SK": f"USER#{sub}"}
                )
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
