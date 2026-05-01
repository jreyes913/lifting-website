"""
Integration tests for the /exercise_block/ and /exercise_blocks/ endpoints.
"""


class TestCreateExerciseBlock:
    def test_returns_success_message(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        assert block["lift_id"] == lift["id"]

    def test_response_contains_id(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        assert "id" in block
        assert isinstance(block["id"], int)

    def test_response_shape(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        assert set(block.keys()) == {"id", "lift_id", "exercise_id", "block_order", "goal_id"}

    def test_persists_exercise_and_order(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"], exercise_id=3, block_order=2)
        assert block["exercise_id"] == 3
        assert block["block_order"] == 2

    def test_create_returns_200(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        r = client.post("/exercise_block/", json={
            "lift_id": lift["id"],
            "exercise_id": 1,
            "block_order": 1,
            "goal_id": 0,
        })
        assert r.status_code == 200
        assert r.json()["message"] == "success"


class TestGetAllExerciseBlocks:
    def test_empty_list_on_fresh_state(self, client):
        r = client.get("/exercise_blocks/")
        assert r.status_code == 200
        assert r.json()["exercise_blocks"] == []

    def test_returns_one_after_create(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        make_block(lift_id=lift["id"])
        blocks = client.get("/exercise_blocks/").json()["exercise_blocks"]
        assert len(blocks) == 1

    def test_returns_multiple_blocks_for_same_lift(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        make_block(lift_id=lift["id"], exercise_id=1, block_order=1)
        make_block(lift_id=lift["id"], exercise_id=2, block_order=2)
        blocks = client.get("/exercise_blocks/").json()["exercise_blocks"]
        assert len(blocks) == 2

    def test_block_orders_are_preserved(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        make_block(lift_id=lift["id"], block_order=1)
        make_block(lift_id=lift["id"], block_order=2)
        orders = {b["block_order"] for b in client.get("/exercise_blocks/").json()["exercise_blocks"]}
        assert orders == {1, 2}


class TestGetExerciseBlockById:
    def test_returns_correct_block(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        created = make_block(lift_id=lift["id"], exercise_id=5, block_order=3)
        r = client.get("/exercise_block/", params={"id": created["id"]})
        assert r.status_code == 200
        block = r.json()["exercise_block"]
        assert block["id"] == created["id"]
        assert block["exercise_id"] == 5
        assert block["block_order"] == 3

    def test_response_message_is_success(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        created = make_block(lift_id=lift["id"])
        r = client.get("/exercise_block/", params={"id": created["id"]})
        assert r.json()["message"] == "success"


class TestDeleteExerciseBlock:
    def test_delete_removes_block_from_list(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        client.delete("/exercise_block/", params={"id": block["id"]})
        blocks = client.get("/exercise_blocks/").json()["exercise_blocks"]
        assert all(b["id"] != block["id"] for b in blocks)

    def test_delete_returns_success_message(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        r = client.delete("/exercise_block/", params={"id": block["id"]})
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_delete_leaves_other_blocks_intact(self, client, make_athlete, make_lift, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        b1 = make_block(lift_id=lift["id"], block_order=1)
        b2 = make_block(lift_id=lift["id"], block_order=2)
        r = client.delete("/exercise_block/", params={"id": b1["id"]})
        remaining_ids = [b["id"] for b in r.json()["exercise_blocks"]]
        assert b2["id"] in remaining_ids
        assert b1["id"] not in remaining_ids
