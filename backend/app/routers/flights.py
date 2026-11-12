from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.db import Repository, get_repository, scope_for
from app.dependencies import get_current_user_sub
from app.schemas import FlightIn, FlightOut

router = APIRouter()


def _out(item: dict, sub: str) -> FlightOut:
    return FlightOut(
        id=item["id"],
        sub=item["sub"],
        displayName=item.get("displayName", "re:Invent peer"),
        avatar=item.get("avatar", "🙂"),
        isPepper=bool(item.get("isPepper", False)),
        originIata=item["originIata"],
        destIata=item["destIata"],
        departAt=item["departAt"],
        arriveAt=item["arriveAt"],
        flightNumber=item.get("flightNumber"),
        note=item.get("note"),
        mine=item["sub"] == sub,
    )


@router.get("", response_model=list[FlightOut])
def list_flights(
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> list[FlightOut]:
    """Flights of the caller's community only (ADR-012), earliest departure first."""
    scope = scope_for(repo.get_profile(sub))
    items = sorted(repo.list_flights(scope), key=lambda i: i["departAt"])
    return [_out(i, sub) for i in items]


@router.post("", response_model=FlightOut, status_code=201)
def add_flight(
    body: FlightIn,
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> FlightOut:
    try:
        body.validate_route()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if len(repo.list_my_flights(sub)) >= settings.flight_max_per_user:
        raise HTTPException(
            status_code=409,
            detail=f"limit of {settings.flight_max_per_user} flights reached",
        )
    profile = repo.get_profile(sub) or {}
    is_pepper = (profile.get("email") or "").strip().lower() == settings.pepper_email.strip().lower()
    item = repo.add_flight(
        sub,
        scope_for(profile),
        body.model_dump(),
        {**profile, "isPepper": is_pepper},
    )
    return _out(item, sub)


@router.delete("/{flight_id}", status_code=200)
def delete_flight(
    flight_id: str,
    sub: str = Depends(get_current_user_sub),
    repo: Repository = Depends(get_repository),
) -> dict:
    if not repo.delete_flight(sub, flight_id):
        raise HTTPException(status_code=404, detail="flight not found")
    return {"deleted": flight_id}
