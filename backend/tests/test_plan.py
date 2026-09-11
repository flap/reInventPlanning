from __future__ import annotations

from tests.conftest import auth


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_plan_requires_auth(client):
    r = client.get("/api/v1/plan")
    assert r.status_code == 401


def test_profile_roundtrip(client):
    r = client.put(
        "/api/v1/profile",
        json={"displayName": "Ana", "avatar": "🦄", "locale": "pt"},
        headers=auth("user-1"),
    )
    assert r.status_code == 200
    r = client.get("/api/v1/profile", headers=auth("user-1"))
    assert r.json()["displayName"] == "Ana"
    assert r.json()["avatar"] == "🦄"


def test_profile_email_not_exposed_but_drives_pepper(client):
    # The pepper user saves profile with the special email.
    client.put(
        "/api/v1/profile",
        json={"displayName": "Flavio", "avatar": "🙂", "locale": "pt", "email": "flaviopimenta@gmail.com"},
        headers=auth("pepper"),
    )
    # GET profile must NOT leak the email field.
    prof = client.get("/api/v1/profile", headers=auth("pepper")).json()
    assert "email" not in prof

    # A normal user saves a profile too.
    client.put(
        "/api/v1/profile",
        json={"displayName": "Normal", "avatar": "🙂", "locale": "pt", "email": "someone@else.com"},
        headers=auth("normal"),
    )

    # Both share; pepper is flagged, normal is not; neither peer exposes email.
    client.post("/api/v1/share", json={"mode": "venue", "venueId": "venetian-expo", "durationMin": 60}, headers=auth("pepper"))
    client.post("/api/v1/share", json={"mode": "venue", "venueId": "venetian-expo", "durationMin": 60}, headers=auth("normal"))

    peers = client.get("/api/v1/share", headers=auth("normal")).json()
    pepper_peer = next(p for p in peers if p["sub"] == "pepper")
    assert pepper_peer["isPepper"] is True
    assert "email" not in pepper_peer

    peers2 = client.get("/api/v1/share", headers=auth("pepper")).json()
    normal_peer = next(p for p in peers2 if p["sub"] == "normal")
    assert normal_peer["isPepper"] is False


def test_plan_put_and_get(client):
    body = {"data": {"items": {"doc-001": {"completed": True}}}, "updatedAt": "2026-09-11T10:00:00Z"}
    r = client.put("/api/v1/plan/checklist", json=body, headers=auth("user-1"))
    assert r.status_code == 200

    r = client.get("/api/v1/plan", headers=auth("user-1"))
    assert r.status_code == 200
    assert r.json()["checklist"]["items"]["doc-001"]["completed"] is True


def test_plan_last_write_wins(client):
    newer = {"data": {"v": "new"}, "updatedAt": "2026-09-11T12:00:00Z"}
    older = {"data": {"v": "old"}, "updatedAt": "2026-09-11T09:00:00Z"}
    client.put("/api/v1/plan/budget", json=newer, headers=auth("u"))
    client.put("/api/v1/plan/budget", json=older, headers=auth("u"))  # should NOT overwrite
    r = client.get("/api/v1/plan", headers=auth("u"))
    assert r.json()["budget"]["v"] == "new"


def test_account_deletion_wipes_data(client):
    client.put(
        "/api/v1/plan/trip",
        json={"data": {"hotel": "venetian"}, "updatedAt": "2026-09-11T10:00:00Z"},
        headers=auth("gone"),
    )
    r = client.delete("/api/v1/account", headers=auth("gone"))
    assert r.status_code == 200
    assert r.json()["deleted"] >= 1
    r = client.get("/api/v1/plan", headers=auth("gone"))
    assert r.json()["trip"] is None
