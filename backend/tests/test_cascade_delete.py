"""
Integration tests that simulate the frontend's cascade-delete flows.

The backend has NO cascade-delete logic — it deletes one record at a time.
The frontend is responsible for orchestrating the order:
  Athlete delete: sets → blocks → lifts → goals → athlete
  Lift delete:    sets → blocks → lift
  Block delete:   sets → block

These tests verify that the backend supports these patterns correctly,
matching the sequence used in script.js.
"""


def _build_full_hierarchy(make_athlete, make_lift, make_goal, make_block, make_set):
    """
    Creates: 1 athlete → 1 goal → 1 lift → 2 blocks → 2 sets each.
    Returns a dict of all created entity dicts.
    """
    athlete = make_athlete()
    goal = make_goal(athlete_id=athlete["id"])
    lift = make_lift(athlete_id=athlete["id"])
    b1 = make_block(lift_id=lift["id"], block_order=1, goal_id=goal["id"])
    b2 = make_block(lift_id=lift["id"], block_order=2, goal_id=goal["id"])
    s1a = make_set(block_id=b1["id"], set_order=1)
    s1b = make_set(block_id=b1["id"], set_order=2)
    s2a = make_set(block_id=b2["id"], set_order=1)
    s2b = make_set(block_id=b2["id"], set_order=2)
    return {
        "athlete": athlete,
        "goal": goal,
        "lift": lift,
        "blocks": [b1, b2],
        "sets": [s1a, s1b, s2a, s2b],
    }


class TestAthleteFullCascadeDelete:
    """
    Simulates script.js deleteAthlete():
      1. For each lift: get blocks, for each block get sets, delete each set
      2. Delete each block
      3. Delete each lift
      4. Delete each goal
      5. Delete the athlete
    """

    def test_all_sets_removed_after_cascade(
        self, client, make_athlete, make_lift, make_goal, make_block, make_set
    ):
        h = _build_full_hierarchy(make_athlete, make_lift, make_goal, make_block, make_set)

        # Delete sets
        for s in h["sets"]:
            client.delete("/exercise_set/", params={"id": s["id"]})
        # Delete blocks
        for b in h["blocks"]:
            client.delete("/exercise_block/", params={"id": b["id"]})
        # Delete lift
        client.delete("/lift/", params={"id": h["lift"]["id"]})
        # Delete goal
        client.delete("/goal/", params={"id": h["goal"]["id"]})
        # Delete athlete
        client.delete("/athlete/", params={"id": h["athlete"]["id"]})

        assert client.get("/exercise_sets/").json()["exercise_sets"] == []
        assert client.get("/exercise_blocks/").json()["exercise_blocks"] == []
        assert client.get("/lifts/").json()["lifts"] == []
        assert client.get("/goals/").json()["goals"] == []
        assert client.get("/athletes/").json()["athletes"] == []

    def test_other_athletes_data_unaffected(
        self, client, make_athlete, make_lift, make_goal, make_block, make_set
    ):
        """Cascading an athlete's delete must not affect a sibling athlete's data."""
        h = _build_full_hierarchy(make_athlete, make_lift, make_goal, make_block, make_set)

        # Second athlete with their own lift and set
        a2 = make_athlete(name="Bystander")
        lift2 = make_lift(athlete_id=a2["id"])
        block2 = make_block(lift_id=lift2["id"])
        set2 = make_set(block_id=block2["id"])

        # Cascade-delete the first athlete
        for s in h["sets"]:
            client.delete("/exercise_set/", params={"id": s["id"]})
        for b in h["blocks"]:
            client.delete("/exercise_block/", params={"id": b["id"]})
        client.delete("/lift/", params={"id": h["lift"]["id"]})
        client.delete("/goal/", params={"id": h["goal"]["id"]})
        client.delete("/athlete/", params={"id": h["athlete"]["id"]})

        # Verify the second athlete's full tree is intact
        assert any(
            a["id"] == a2["id"] for a in client.get("/athletes/").json()["athletes"]
        )
        assert any(
            l["id"] == lift2["id"] for l in client.get("/lifts/").json()["lifts"]
        )
        assert any(
            b["id"] == block2["id"] for b in client.get("/exercise_blocks/").json()["exercise_blocks"]
        )
        assert any(
            s["id"] == set2["id"] for s in client.get("/exercise_sets/").json()["exercise_sets"]
        )


class TestLiftCascadeDelete:
    """
    Simulates script.js deleteLift():
      1. For each block in lift: get sets, delete each set
      2. Delete each block
      3. Delete the lift
    """

    def test_lift_cascade_removes_blocks_and_sets(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        b1 = make_block(lift_id=lift["id"], block_order=1)
        b2 = make_block(lift_id=lift["id"], block_order=2)
        s1 = make_set(block_id=b1["id"])
        s2 = make_set(block_id=b2["id"])

        # Cascade delete
        for s in [s1, s2]:
            client.delete("/exercise_set/", params={"id": s["id"]})
        for b in [b1, b2]:
            client.delete("/exercise_block/", params={"id": b["id"]})
        client.delete("/lift/", params={"id": lift["id"]})

        assert client.get("/exercise_sets/").json()["exercise_sets"] == []
        assert client.get("/exercise_blocks/").json()["exercise_blocks"] == []
        assert client.get("/lifts/").json()["lifts"] == []

    def test_other_lifts_unaffected_by_lift_cascade(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift_del = make_lift(athlete_id=athlete["id"], date="2024-01-01T00:00:00")
        lift_keep = make_lift(athlete_id=athlete["id"], date="2024-01-08T00:00:00")

        block_del = make_block(lift_id=lift_del["id"])
        set_del = make_set(block_id=block_del["id"])

        block_keep = make_block(lift_id=lift_keep["id"])
        set_keep = make_set(block_id=block_keep["id"])

        # Only cascade-delete lift_del
        client.delete("/exercise_set/", params={"id": set_del["id"]})
        client.delete("/exercise_block/", params={"id": block_del["id"]})
        client.delete("/lift/", params={"id": lift_del["id"]})

        # The kept lift's data must still be present
        assert any(l["id"] == lift_keep["id"] for l in client.get("/lifts/").json()["lifts"])
        assert any(
            b["id"] == block_keep["id"]
            for b in client.get("/exercise_blocks/").json()["exercise_blocks"]
        )
        assert any(
            s["id"] == set_keep["id"]
            for s in client.get("/exercise_sets/").json()["exercise_sets"]
        )


class TestBlockCascadeDelete:
    """
    Simulates script.js deleteBlock():
      1. Delete all sets in the block
      2. Delete the block
    """

    def test_block_cascade_removes_sets(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        block = make_block(lift_id=lift["id"])
        s1 = make_set(block_id=block["id"], set_order=1)
        s2 = make_set(block_id=block["id"], set_order=2)

        client.delete("/exercise_set/", params={"id": s1["id"]})
        client.delete("/exercise_set/", params={"id": s2["id"]})
        client.delete("/exercise_block/", params={"id": block["id"]})

        assert client.get("/exercise_sets/").json()["exercise_sets"] == []
        assert client.get("/exercise_blocks/").json()["exercise_blocks"] == []

    def test_sibling_blocks_sets_unaffected(
        self, client, make_athlete, make_lift, make_block, make_set
    ):
        athlete = make_athlete()
        lift = make_lift(athlete_id=athlete["id"])
        b_del = make_block(lift_id=lift["id"], block_order=1)
        b_keep = make_block(lift_id=lift["id"], block_order=2)
        s_del = make_set(block_id=b_del["id"])
        s_keep = make_set(block_id=b_keep["id"])

        client.delete("/exercise_set/", params={"id": s_del["id"]})
        client.delete("/exercise_block/", params={"id": b_del["id"]})

        remaining_sets = client.get("/exercise_sets/").json()["exercise_sets"]
        assert any(s["id"] == s_keep["id"] for s in remaining_sets)
        remaining_blocks = client.get("/exercise_blocks/").json()["exercise_blocks"]
        assert any(b["id"] == b_keep["id"] for b in remaining_blocks)
