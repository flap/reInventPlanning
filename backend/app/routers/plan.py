from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends

from app.db import Repository, get_repository
from app.dependencies import get_current_user_sub
from app.schemas import PlanKindIn, PlanOut, ProfileIn, ProfileOut

router = APIRouter()


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/profile", response_model=ProfileOut)
def get_profile(
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> ProfileOut:
    item = repo.get_profile(sub) or {}
    return ProfileOut(
        displayName=item.get("displayName", ""),
        avatar=item.get("avatar", "🙂"),
        locale=item.get("locale", "pt"),
        updatedAt=item.get("updatedAt"),
    )


@router.put("/profile", response_model=ProfileOut)
def put_profile(
    body: ProfileIn,
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> ProfileOut:
    payload = body.model_dump()
    payload["updatedAt"] = payload.get("updatedAt") or _iso_now()
    saved = repo.put_profile(sub, payload)
    return ProfileOut(**{k: saved[k] for k in ("displayName", "avatar", "locale", "updatedAt")})


@router.get("/plan", response_model=PlanOut)
def get_plan(
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> PlanOut:
    plan = repo.get_plan(sub)
    return PlanOut(**{k: plan.get(k) for k in ("checklist", "budget", "trip")})


@router.put("/plan/{kind}")
def put_plan_kind(
    kind: Literal["checklist", "budget", "trip"],
    body: PlanKindIn,
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> dict:
    saved = repo.put_plan_kind(sub, kind, body.data, body.updatedAt)
    return {"kind": kind, "updatedAt": saved["updatedAt"]}


@router.delete("/account", status_code=200)
def delete_account(
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> dict:
    """Right to erasure (F11.8): remove all plan + location data for the user.

    NOTE: the Cognito user record itself is deleted by the caller/gateway layer
    (AdminDeleteUser); this endpoint guarantees the data-store side is wiped.
    """
    deleted = repo.delete_all_user_data(sub)
    return {"deleted": deleted}
