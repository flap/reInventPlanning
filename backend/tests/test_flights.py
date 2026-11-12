from __future__ import annotations

from tests.conftest import auth

LEG = {
    "originIata": "gru",
    "destIata": "MIA",
    "departAt": "2030-11-29T22:10",
    "arriveAt": "2030-11-30T05:20",
    "flightNumber": "aa 930",
}


def _community(client, sub, community):
    client.put(
        "/api/v1/profile",
        json={"displayName": sub, "avatar": "🙂", "locale": "pt", "community": community},
        headers=auth(sub),
    )


def test_requires_auth(client):
    assert client.get("/api/v1/flights").status_code in (401, 403)


def test_profile_default_community(client):
    r = client.get("/api/v1/profile", headers=auth("u1"))
    assert r.json()["community"] == "CommunityBR"


def test_profile_community_validation(client):
    r = client.put(
        "/api/v1/profile",
        json={"displayName": "x", "community": "a b!"},
        headers=auth("u1"),
    )
    assert r.status_code == 422


def test_profile_omitted_community_is_kept(client):
    _community(client, "u1", "Alpha")
    client.put("/api/v1/profile", json={"displayName": "n"}, headers=auth("u1"))
    assert client.get("/api/v1/profile", headers=auth("u1")).json()["community"] == "Alpha"


def test_add_list_delete_flight(client):
    r = client.post("/api/v1/flights", json=LEG, headers=auth("u1"))
    assert r.status_code == 201
    f = r.json()
    assert f["originIata"] == "GRU" and f["flightNumber"] == "AA 930" and f["mine"] is True
    assert client.get("/api/v1/flights", headers=auth("u1")).json()[0]["id"] == f["id"]
    assert client.delete(f"/api/v1/flights/{f['id']}", headers=auth("u1")).status_code == 200
    assert client.get("/api/v1/flights", headers=auth("u1")).json() == []


def test_flight_validation(client):
    bad = {**LEG, "originIata": "GR"}
    assert client.post("/api/v1/flights", json=bad, headers=auth("u1")).status_code == 422
    same = {**LEG, "destIata": "GRU"}
    assert client.post("/api/v1/flights", json=same, headers=auth("u1")).status_code == 422
    baddt = {**LEG, "departAt": "30/11/2030 10:00"}
    assert client.post("/api/v1/flights", json=baddt, headers=auth("u1")).status_code == 422


def test_flight_limit(client):
    for _ in range(12):
        assert client.post("/api/v1/flights", json=LEG, headers=auth("u1")).status_code == 201
    assert client.post("/api/v1/flights", json=LEG, headers=auth("u1")).status_code == 409


def test_flights_visible_only_within_community(client):
    _community(client, "a", "Alpha")
    _community(client, "b", "Alpha")
    _community(client, "c", "Beta")
    client.post("/api/v1/flights", json=LEG, headers=auth("a"))
    client.post("/api/v1/flights", json=LEG, headers=auth("c"))
    seen = {f["sub"] for f in client.get("/api/v1/flights", headers=auth("b")).json()}
    assert seen == {"a"}
    mine = [f["mine"] for f in client.get("/api/v1/flights", headers=auth("a")).json()]
    assert mine == [True]


def test_cannot_delete_others_flight(client):
    fid = client.post("/api/v1/flights", json=LEG, headers=auth("a")).json()["id"]
    assert client.delete(f"/api/v1/flights/{fid}", headers=auth("b")).status_code == 404
    assert len(client.get("/api/v1/flights", headers=auth("a")).json()) == 1


def test_changing_community_moves_flights(client):
    _community(client, "a", "Alpha")
    _community(client, "b", "Alpha")
    client.post("/api/v1/flights", json=LEG, headers=auth("a"))
    _community(client, "a", "Beta")
    assert client.get("/api/v1/flights", headers=auth("b")).json() == []
    assert len(client.get("/api/v1/flights", headers=auth("a")).json()) == 1


def test_expired_flight_hidden(client):
    old = {**LEG, "departAt": "2001-01-01T10:00", "arriveAt": "2001-01-01T12:00"}
    client.post("/api/v1/flights", json=old, headers=auth("a"))
    assert client.get("/api/v1/flights", headers=auth("a")).json() == []


def test_no_email_in_flights(client):
    client.put(
        "/api/v1/profile",
        json={"displayName": "a", "email": "a@x.com", "community": "Alpha"},
        headers=auth("a"),
    )
    client.post("/api/v1/flights", json=LEG, headers=auth("a"))
    assert "a@x.com" not in client.get("/api/v1/flights", headers=auth("a")).text


def test_account_deletion_wipes_flights(client, dynamodb_table):
    client.post("/api/v1/flights", json=LEG, headers=auth("a"))
    client.delete("/api/v1/account", headers=auth("a"))
    assert dynamodb_table.scan()["Items"] == []
