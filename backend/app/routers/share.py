from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.config import settings
from app.db import Repository, get_repository
from app.dependencies import get_current_user_sub
from app.schemas import Peer, ShareIn, ShareStatus

router = APIRouter()


def _scope(crew_code: str | None) -> str:
    if crew_code:
        return crew_code.strip().upper()
    return "GLOBAL"


def _ttl_for(mode: str, duration_min: int) -> int:
    """Clamp the requested duration to the per-mode maximum (privacy: ADR-011)."""
    requested = duration_min * 60
    cap = settings.gps_max_ttl_seconds if mode == "gps" else settings.venue_max_ttl_seconds
    return min(requested, cap)


@router.post("", response_model=ShareStatus)
def start_or_update_share(
    body: ShareIn,
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> ShareStatus:
    try:
        body.validate_mode()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    scope = _scope(body.crewCode)
    profile = repo.get_profile(sub) or {}
    ttl = _ttl_for(body.mode, body.durationMin)

    # Derive the pepper highlight server-side from the stored profile email.
    # The email is compared here and never returned to other users.
    is_pepper = (profile.get("email") or "").strip().lower() == settings.pepper_email.strip().lower()

    item = repo.put_share(
        sub,
        scope=scope,
        mode=body.mode,
        display_name=profile.get("displayName", "re:Invent peer"),
        avatar=profile.get("avatar", "🙂"),
        venue_id=body.venueId,
        lat=body.lat,
        lng=body.lng,
        status_text=body.statusText,
        ttl_seconds=ttl,
        is_pepper=is_pepper,
    )
    return ShareStatus(
        sharing=True,
        scope=scope,
        mode=body.mode,
        venueId=body.venueId,
        expiresAt=int(item["expiresAt"]),
    )


@router.delete("", response_model=ShareStatus)
def stop_share(
    crewCode: str | None = Query(default=None),
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> ShareStatus:
    """Revoke immediately (F12.4). Deletes the location item now."""
    repo.delete_share(sub, _scope(crewCode))
    return ShareStatus(sharing=False)


@router.get("", response_model=list[Peer])
def list_peers(
    crewCode: str | None = Query(default=None),
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> list[Peer]:
    """Reciprocal read (ADR-011): only users who are themselves currently
    sharing in this scope may see peers. Enforced server-side — never trusted
    to the client."""
    scope = _scope(crewCode)
    mine = repo.get_my_share(sub, scope)
    if not mine:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be sharing your location to see peers (reciprocal visibility).",
        )

    peers: list[Peer] = []
    for item in repo.list_shares(scope):
        if item.get("sub") == sub:
            continue  # don't include self
        peers.append(
            Peer(
                sub=item["sub"],
                displayName=item.get("displayName", "re:Invent peer"),
                avatar=item.get("avatar", "🙂"),
                isPepper=bool(item.get("isPepper", False)),
                mode=item["mode"],
                venueId=item.get("venueId"),
                lat=float(item["lat"]) if item.get("lat") is not None else None,
                lng=float(item["lng"]) if item.get("lng") is not None else None,
                statusText=item.get("statusText"),
                sharedAt=int(item["sharedAt"]),
                expiresAt=int(item["expiresAt"]),
            )
        )
    return peers


@router.get("/status", response_model=ShareStatus)
def my_status(
    crewCode: str | None = Query(default=None),
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> ShareStatus:
    scope = _scope(crewCode)
    mine = repo.get_my_share(sub, scope)
    if not mine:
        return ShareStatus(sharing=False)
    return ShareStatus(
        sharing=True,
        scope=scope,
        mode=mine["mode"],
        venueId=mine.get("venueId"),
        expiresAt=int(mine["expiresAt"]),
    )
