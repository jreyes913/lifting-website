"""
Integration tests for the /lift/ and /lifts/ endpoints.
"""


class TestCreateLift:
    def test_returns_success_message(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        assert lift["athlete_id"] == athlete["id"]

    def test_response_contains_id(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        assert "id" in lift
        assert isinstance(lift["id"], int)

    def test_response_shape(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        assert set(lift.keys()) == {"id", "athlete_id", "date", "body_weight"}

    def test_persists_body_weight(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"], body_weight=95)
        assert lift["body_weight"] == 95

    def test_persists_date(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"], date="2024-06-15T10:30:00")
        assert "2024-06-15" in lift["date"]

    def test_create_returns_200(self, client, make_athlete):
        athlete = make_athlete()
        r = client.post("/lift/", json={
            "athlete_id": athlete["id"],
            "date": "2024-03-01T09:00:00",
            "body_weight": 80,
        })
        assert r.status_code == 200
        assert r.json()["message"] == "success"


class TestGetAllLifts:
    def test_empty_list_on_fresh_state(self, client):
        r = client.get("/lifts/")
        assert r.status_code == 200
        assert r.json()["lifts"] == []

    def test_returns_one_after_create(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        make_lift(athlete_id=athlete["id"])
        lifts = client.get("/lifts/").json()["lifts"]
        assert len(lifts) == 1

    def test_returns_multiple_lifts_for_same_athlete(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        make_lift(athlete_id=athlete["id"], date="2024-01-01T09:00:00")
        make_lift(athlete_id=athlete["id"], date="2024-01-08T09:00:00")
        lifts = client.get("/lifts/").json()["lifts"]
        assert len(lifts) == 2

    def test_lifts_from_different_athletes(self, client, make_athlete, make_lift):
        a1 = make_athlete(name="A1")
        a2 = make_athlete(name="A2")
        make_lift(athlete_id=a1["id"])
        make_lift(athlete_id=a2["id"])
        athlete_ids = {l["athlete_id"] for l in client.get("/lifts/").json()["lifts"]}
        assert athlete_ids == {a1["id"], a2["id"]}


class TestGetLiftById:
    def test_returns_correct_lift(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        created = make_lift(athlete_id=athlete["id"], body_weight=77)
        r = client.get("/lift/", params={"id": created["id"]})
        assert r.status_code == 200
        lift = r.json()["lift"]
        assert lift["id"] == created["id"]
        assert lift["body_weight"] == 77

    def test_response_message_is_success(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        created = make_lift(athlete_id=athlete["id"])
        r = client.get("/lift/", params={"id": created["id"]})
        assert r.json()["message"] == "success"


class TestDeleteLift:
    def test_delete_removes_lift_from_list(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        client.delete("/lift/", params={"id": lift["id"]})
        lifts = client.get("/lifts/").json()["lifts"]
        assert all(l["id"] != lift["id"] for l in lifts)

    def test_delete_returns_success_message(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        r = client.delete("/lift/", params={"id": lift["id"]})
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_delete_leaves_other_lifts_intact(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        l1 = make_lift(athlete_id=athlete["id"], date="2024-01-01T00:00:00")
        l2 = make_lift(athlete_id=athlete["id"], date="2024-01-08T00:00:00")
        r = client.delete("/lift/", params={"id": l1["id"]})
        remaining_ids = [l["id"] for l in r.json()["lifts"]]
        assert l2["id"] in remaining_ids
        assert l1["id"] not in remaining_ids
