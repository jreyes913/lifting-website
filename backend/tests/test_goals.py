"""
Integration tests for the /goal/ and /goals/ endpoints.
"""


class TestCreateGoal:
    def test_returns_success_message(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"])
        assert goal["athlete_id"] == athlete["id"]

    def test_response_contains_id(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"])
        assert "id" in goal
        assert isinstance(goal["id"], int)

    def test_response_shape(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"])
        assert set(goal.keys()) == {
            "id", "athlete_id", "start_date", "duration",
            "exercise_id", "reps", "weight",
        }

    def test_persists_provided_values(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"], duration=60, reps=5, weight=120, exercise_id=2)
        assert goal["duration"] == 60
        assert goal["reps"] == 5
        assert goal["weight"] == 120
        assert goal["exercise_id"] == 2

    def test_create_returns_200(self, client, make_athlete):
        athlete = make_athlete()
        payload = {
            "athlete_id": athlete["id"],
            "start_date": "2024-01-01T00:00:00",
            "duration": 30,
            "exercise_id": 1,
            "reps": 8,
            "weight": 100,
        }
        r = client.post("/goal/", json=payload)
        assert r.status_code == 200
        assert r.json()["message"] == "success"


class TestGetAllGoals:
    def test_empty_list_on_fresh_state(self, client):
        r = client.get("/goals/")
        assert r.status_code == 200
        assert r.json()["goals"] == []

    def test_returns_one_after_create(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        make_goal(athlete_id=athlete["id"])
        goals = client.get("/goals/").json()["goals"]
        assert len(goals) == 1

    def test_returns_two_goals_for_same_athlete(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        make_goal(athlete_id=athlete["id"], exercise_id=1)
        make_goal(athlete_id=athlete["id"], exercise_id=2)
        goals = client.get("/goals/").json()["goals"]
        assert len(goals) == 2

    def test_goals_for_different_athletes(self, client, make_athlete, make_goal):
        a1 = make_athlete(name="A1")
        a2 = make_athlete(name="A2")
        make_goal(athlete_id=a1["id"])
        make_goal(athlete_id=a2["id"])
        all_goals = client.get("/goals/").json()["goals"]
        athlete_ids = {g["athlete_id"] for g in all_goals}
        assert athlete_ids == {a1["id"], a2["id"]}


class TestGetGoalById:
    def test_returns_correct_goal(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        created = make_goal(athlete_id=athlete["id"], reps=12)
        r = client.get("/goal/", params={"id": created["id"]})
        assert r.status_code == 200
        goal = r.json()["goal"]
        assert goal["id"] == created["id"]
        assert goal["reps"] == 12

    def test_response_message_is_success(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        created = make_goal(athlete_id=athlete["id"])
        r = client.get("/goal/", params={"id": created["id"]})
        assert r.json()["message"] == "success"


class TestDeleteGoal:
    def test_delete_removes_goal_from_list(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"])
        client.delete("/goal/", params={"id": goal["id"]})
        goals = client.get("/goals/").json()["goals"]
        assert all(g["id"] != goal["id"] for g in goals)

    def test_delete_returns_success_message(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete_id=athlete["id"])
        r = client.delete("/goal/", params={"id": goal["id"]})
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_delete_returns_remaining_goals(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        g1 = make_goal(athlete_id=athlete["id"], exercise_id=1)
        g2 = make_goal(athlete_id=athlete["id"], exercise_id=2)
        r = client.delete("/goal/", params={"id": g1["id"]})
        remaining_ids = [g["id"] for g in r.json()["goals"]]
        assert g2["id"] in remaining_ids
        assert g1["id"] not in remaining_ids
