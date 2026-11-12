from __future__ import annotations

from tests.conftest import auth


def test_not_sharing_by_default_status(client):
    r = client.get("/api/v1/share/status", headers=auth("u1"))
    assert r.status_code == 200
    assert r.json()["sharing"] is False


def test_non_sharer_can_list_peers(client):
    # u2 is sharing; u1 is NOT sharing but must still be able to view (non-reciprocal).
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "venetian-expo", "durationMin": 120},
        headers=auth("u2"),
    )
    r = client.get("/api/v1/share", headers=auth("u1"))
    assert r.status_code == 200
    subs = {p["sub"] for p in r.json()}
    assert "u2" in subs  # non-sharer u1 sees sharer u2


def test_empty_list_when_nobody_sharing(client):
    # u1 not sharing, nobody else sharing -> empty list, still 200 (no 403).
    r = client.get("/api/v1/share", headers=auth("u1"))
    assert r.status_code == 200
    assert r.json() == []


def test_share_venue_and_list(client):
    # u1 shares a venue
    r = client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "venetian-expo", "durationMin": 120},
        headers=auth("u1"),
    )
    assert r.status_code == 200
    assert r.json()["sharing"] is True

    # u2 shares too
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "caesars-forum-main", "durationMin": 120},
        headers=auth("u2"),
    )

    # u1 (sharing) can now see u2, but not itself
    r = client.get("/api/v1/share", headers=auth("u1"))
    assert r.status_code == 200
    peers = r.json()
    subs = {p["sub"] for p in peers}
    assert "u2" in subs
    assert "u1" not in subs
    assert peers[0]["venueId"] in {"caesars-forum-main"}


def test_venue_mode_never_stores_coordinates(client):
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "wynn-sessions", "durationMin": 60},
        headers=auth("a"),
    )
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "wynn-sessions", "durationMin": 60},
        headers=auth("b"),
    )
    peers = client.get("/api/v1/share", headers=auth("a")).json()
    for p in peers:
        assert p["lat"] is None and p["lng"] is None


def test_gps_mode_requires_coords(client):
    r = client.post(
        "/api/v1/share",
        json={"mode": "gps", "durationMin": 60},
        headers=auth("a"),
    )
    assert r.status_code == 422


def test_stop_share_revokes_immediately(client):
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "wynn-sessions", "durationMin": 60},
        headers=auth("a"),
    )
    client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "wynn-sessions", "durationMin": 60},
        headers=auth("b"),
    )
    # b stops sharing
    r = client.delete("/api/v1/share", headers=auth("b"))
    assert r.json()["sharing"] is False
    # a still sharing -> should no longer see b
    peers = client.get("/api/v1/share", headers=auth("a")).json()
    assert all(p["sub"] != "b" for p in peers)


def _set_community(client, sub, community=None):
    body = {"displayName": sub, "avatar": "🙂", "locale": "pt"}
    if community:
        body["community"] = community
    r = client.put("/api/v1/profile", json=body, headers=auth(sub))
    assert r.status_code == 200
    return r.json()


def _share(client, sub):
    return client.post(
        "/api/v1/share",
        json={"mode": "venue", "venueId": "wynn-sessions", "durationMin": 60},
        headers=auth(sub),
    )


def test_community_scope_isolation(client):
    _set_community(client, "a", "Alpha")
    _set_community(client, "b", "alpha")  # case-insensitive: same community as a
    _set_community(client, "c")  # default CommunityBR
    for u in ("a", "b", "c"):
        _share(client, u)
    subs = {p["sub"] for p in client.get("/api/v1/share", headers=auth("a")).json()}
    assert subs == {"b"}  # sees b (same community), never c (CommunityBR)


def test_default_community_users_see_each_other(client):
    # No profile at all -> everybody defaults to CommunityBR.
    _share(client, "x")
    _share(client, "y")
    subs = {p["sub"] for p in client.get("/api/v1/share", headers=auth("x")).json()}
    assert subs == {"y"}


def test_client_cannot_choose_scope_via_query(client):
    _set_community(client, "a", "Alpha")
    _set_community(client, "b", "Beta")
    _share(client, "b")
    # a tries to peek at Beta through the legacy query param -> ignored.
    r = client.get("/api/v1/share?crewCode=Beta", headers=auth("a"))
    assert r.json() == []


def test_changing_community_stops_sharing(client):
    _set_community(client, "a", "Alpha")
    _share(client, "a")
    assert client.get("/api/v1/share/status", headers=auth("a")).json()["sharing"] is True
    _set_community(client, "a", "Beta")
    assert client.get("/api/v1/share/status", headers=auth("a")).json()["sharing"] is False


def test_gps_duration_capped(client):
    # request 600 min; gps cap is 240 min (4h). expiresAt-sharedAt should be <= 4h.
    import time

    before = int(time.time())
    r = client.post(
        "/api/v1/share",
        json={"mode": "gps", "lat": 36.12, "lng": -115.17, "durationMin": 240},
        headers=auth("a"),
    )
    exp = r.json()["expiresAt"]
    assert exp - before <= 4 * 60 * 60 + 5
