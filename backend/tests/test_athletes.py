"""
Integration tests for the /athlete/ and /athletes/ endpoints.
Each test gets a clean mutable-table state via the autouse fixture in conftest.py.
"""


class TestCreateAthlete:
    def test_returns_success_message(self, client, make_athlete):
        athlete = make_athlete()
        assert athlete["name"] == "Test Athlete"

    def test_response_contains_id(self, client, make_athlete):
        athlete = make_athlete()
        assert "id" in athlete
        assert isinstance(athlete["id"], int)

    def test_response_shape(self, client, make_athlete):
        athlete = make_athlete()
        assert set(athlete.keys()) == {"id", "name", "dob", "gender_id", "height", "xp"}

    def test_persists_provided_values(self, client, make_athlete):
        athlete = make_athlete(name="Jane Doe", height=162, xp=5, gender_id=2)
        assert athlete["name"] == "Jane Doe"
        assert athlete["height"] == 162
        assert athlete["xp"] == 5
        assert athlete["gender_id"] == 2

    def test_dob_is_returned(self, client, make_athlete):
        athlete = make_athlete(dob="1995-11-20T00:00:00")
        assert "1995-11-20" in athlete["dob"]

    def test_create_returns_200(self, client):
        payload = {
            "name": "Status Check",
            "dob": "2000-01-01T00:00:00",
            "gender_id": 1,
            "height": 180,
            "xp": 1,
        }
        r = client.post("/athlete/", json=payload)
        assert r.status_code == 200
        assert r.json()["message"] == "success"


class TestGetAllAthletes:
    def test_empty_list_on_fresh_state(self, client):
        r = client.get("/athletes/")
        assert r.status_code == 200
        assert r.json()["athletes"] == []

    def test_message_is_success(self, client):
        assert client.get("/athletes/").json()["message"] == "success"

    def test_returns_one_after_create(self, client, make_athlete):
        make_athlete()
        athletes = client.get("/athletes/").json()["athletes"]
        assert len(athletes) == 1

    def test_returns_two_after_two_creates(self, client, make_athlete):
        make_athlete(name="Athlete A")
        make_athlete(name="Athlete B")
        athletes = client.get("/athletes/").json()["athletes"]
        assert len(athletes) == 2

    def test_athlete_names_preserved(self, client, make_athlete):
        make_athlete(name="Alpha")
        make_athlete(name="Beta")
        names = {a["name"] for a in client.get("/athletes/").json()["athletes"]}
        assert names == {"Alpha", "Beta"}


class TestGetAthleteById:
    def test_returns_correct_athlete(self, client, make_athlete):
        created = make_athlete(name="Lookup Me")
        r = client.get("/athlete/", params={"id": created["id"]})
        assert r.status_code == 200
        athlete = r.json()["athlete"]
        assert athlete["id"] == created["id"]
        assert athlete["name"] == "Lookup Me"

    def test_response_message_is_success(self, client, make_athlete):
        created = make_athlete()
        r = client.get("/athlete/", params={"id": created["id"]})
        assert r.json()["message"] == "success"

    def test_multiple_athletes_correct_lookup(self, client, make_athlete):
        a1 = make_athlete(name="First")
        a2 = make_athlete(name="Second")
        assert client.get("/athlete/", params={"id": a1["id"]}).json()["athlete"]["name"] == "First"
        assert client.get("/athlete/", params={"id": a2["id"]}).json()["athlete"]["name"] == "Second"


class TestDeleteAthlete:
    def test_delete_removes_athlete_from_list(self, client, make_athlete):
        athlete = make_athlete()
        client.delete("/athlete/", params={"id": athlete["id"]})
        athletes = client.get("/athletes/").json()["athletes"]
        assert all(a["id"] != athlete["id"] for a in athletes)

    def test_delete_returns_success_message(self, client, make_athlete):
        athlete = make_athlete()
        r = client.delete("/athlete/", params={"id": athlete["id"]})
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_delete_returns_remaining_athletes(self, client, make_athlete):
        a1 = make_athlete(name="Keep")
        a2 = make_athlete(name="Remove")
        r = client.delete("/athlete/", params={"id": a2["id"]})
        remaining = r.json()["athletes"]
        names = [a["name"] for a in remaining]
        assert "Keep" in names
        assert "Remove" not in names

    def test_delete_all_athletes_leaves_empty_list(self, client, make_athlete):
        a = make_athlete()
        client.delete("/athlete/", params={"id": a["id"]})
        assert client.get("/athletes/").json()["athletes"] == []
