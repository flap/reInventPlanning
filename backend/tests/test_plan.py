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
