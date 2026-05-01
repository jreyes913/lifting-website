"""
Integration tests for the /exercise_set/ and /exercise_sets/ endpoints.
"""


class TestCreateExerciseSet:
    def test_returns_success_message(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"])
        assert ex_set["block_id"] == block["id"]

    def test_response_contains_id(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"])
        assert "id" in ex_set
        assert isinstance(ex_set["id"], int)

    def test_response_shape(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"])
        assert set(ex_set.keys()) == {"id", "block_id", "weight", "reps", "rtl", "set_order"}

    def test_persists_all_set_values(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"], weight=80, reps=6, rtl=3, set_order=2)
        assert ex_set["weight"] == 80
        assert ex_set["reps"] == 6
        assert ex_set["rtl"] == 3
        assert ex_set["set_order"] == 2

    def test_create_returns_200(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        r = client.post("/exercise_set/", json={
            "block_id": block["id"],
            "weight": 60,
            "reps": 10,
            "rtl": 2,
            "set_order": 1,
        })
        assert r.status_code == 200
        assert r.json()["message"] == "success"


class TestGetAllExerciseSets:
    def test_empty_list_on_fresh_state(self, client):
        r = client.get("/exercise_sets/")
        assert r.status_code == 200
        assert r.json()["exercise_sets"] == []

    def test_returns_one_after_create(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        make_set(block_id=block["id"])
        sets = client.get("/exercise_sets/").json()["exercise_sets"]
        assert len(sets) == 1

    def test_returns_multiple_sets_for_same_block(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        make_set(block_id=block["id"], set_order=1)
        make_set(block_id=block["id"], set_order=2)
        make_set(block_id=block["id"], set_order=3)
        sets = client.get("/exercise_sets/").json()["exercise_sets"]
        assert len(sets) == 3

    def test_sets_across_multiple_blocks(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        b1 = make_block(lift_id=lift["id"], block_order=1)
        b2 = make_block(lift_id=lift["id"], block_order=2)
        make_set(block_id=b1["id"])
        make_set(block_id=b2["id"])
        block_ids = {s["block_id"] for s in client.get("/exercise_sets/").json()["exercise_sets"]}
        assert block_ids == {b1["id"], b2["id"]}


class TestGetExerciseSetById:
    def test_returns_correct_set(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        created = make_set(block_id=block["id"], weight=100, reps=5)
        r = client.get("/exercise_set/", params={"id": created["id"]})
        assert r.status_code == 200
        ex_set = r.json()["exercise_set"]
        assert ex_set["id"] == created["id"]
        assert ex_set["weight"] == 100
        assert ex_set["reps"] == 5

    def test_response_message_is_success(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        created = make_set(block_id=block["id"])
        r = client.get("/exercise_set/", params={"id": created["id"]})
        assert r.json()["message"] == "success"


class TestDeleteExerciseSet:
    def test_delete_removes_set_from_list(self, client, make_athlete, make_lift, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"])
        client.delete("/exercise_set/", params={"id": ex_set["id"]})
        sets = client.get("/exercise_sets/").json()["exercise_sets"]
        assert all(s["id"] != ex_set["id"] for s in sets)

    def test_delete_returns_success_message(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        ex_set = make_set(block_id=block["id"])
        r = client.delete("/exercise_set/", params={"id": ex_set["id"]})
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_delete_leaves_sibling_sets_intact(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        s1 = make_set(block_id=block["id"], set_order=1)
        s2 = make_set(block_id=block["id"], set_order=2)
        r = client.delete("/exercise_set/", params={"id": s1["id"]})
        remaining_ids = [s["id"] for s in r.json()["exercise_sets"]]
        assert s2["id"] in remaining_ids
        assert s1["id"] not in remaining_ids
