import pytest
from datetime import datetime

class TestUpdateEndpoints:
    def test_update_athlete(self, client, make_athlete):
        athlete = make_athlete(name="Original", height=170)
        id = athlete["id"]
        
        payload = {"name": "Updated Name", "height": 185}
        r = client.put(f"/athlete/?id={id}", json=payload)
        assert r.status_code == 200
        updated = r.json()["athlete"]
        assert updated["name"] == "Updated Name"
        assert updated["height"] == 185
        assert updated["xp"] == athlete["xp"] # preserved

    def test_update_goal(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        goal = make_goal(athlete["id"], weight=100, reps=5)
        id = goal["id"]
        
        payload = {"weight": 110, "reps": 3}
        r = client.put(f"/goal/?id={id}", json=payload)
        assert r.status_code == 200
        updated = r.json()["goal"]
        assert updated["weight"] == 110
        assert updated["reps"] == 3

    def test_update_lift(self, client, make_athlete, make_lift):
        athlete = make_athlete()
        lift = make_lift(athlete["id"], body_weight=200)
        id = lift["id"]
        
        payload = {"body_weight": 195}
        r = client.put(f"/lift/?id={id}", json=payload)
        assert r.status_code == 200
        updated = r.json()["lift"]
        assert updated["body_weight"] == 195

    def test_update_exercise_block(self, client, make_athlete, make_lift, make_goal, make_block):
        athlete = make_athlete()
        lift = make_lift(athlete["id"])
        goal = make_goal(athlete["id"])
        block = make_block(lift["id"], goal["id"], block_order=1)
        id = block["id"]
        
        payload = {"block_order": 2}
        r = client.put(f"/exercise_block/?id={id}", json=payload)
        assert r.status_code == 200
        updated = r.json()["exercise_block"]
        assert updated["block_order"] == 2

    def test_update_exercise_set(self, client, make_athlete, make_lift, make_goal, make_block, make_set):
        athlete = make_athlete()
        lift = make_lift(athlete["id"])
        goal = make_goal(athlete["id"])
        block = make_block(lift["id"], goal["id"])
        eset = make_set(block["id"], weight=100, reps=5, rtl=2)
        id = eset["id"]
        
        payload = {"weight": 105, "rtl": 1}
        r = client.put(f"/exercise_set/?id={id}", json=payload)
        assert r.status_code == 200
        updated = r.json()["exercise_set"]
        assert updated["weight"] == 105
        assert updated["rtl"] == 1
        assert updated["reps"] == 5 # preserved

    def test_update_program(self, client, make_athlete):
        athlete = make_athlete()
        # No make_program fixture, so we create it manually
        payload = {"athlete_id": athlete["id"], "name": "Old Program"}
        p = client.post("/program/", json=payload).json()["program"]
        
        r = client.put(f"/program/?id={p['id']}", json={"name": "New Program"})
        assert r.status_code == 200
        assert r.json()["program"]["name"] == "New Program"

    def test_update_preset(self, client, make_athlete):
        athlete = make_athlete()
        p = client.post("/program/", json={"athlete_id": athlete["id"], "name": "P"}).json()["program"]
        preset = client.post("/preset/", json={"program_id": p["id"], "name": "Old"}).json()["preset"]
        
        r = client.put(f"/preset/?id={preset['id']}", json={"name": "New"})
        assert r.status_code == 200
        assert r.json()["preset"]["name"] == "New"

    def test_update_preset_block(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        p = client.post("/program/", json={"athlete_id": athlete["id"], "name": "P"}).json()["program"]
        preset = client.post("/preset/", json={"program_id": p["id"], "name": "Pr"}).json()["preset"]
        goal = make_goal(athlete["id"])
        
        pb_payload = {
            "preset_id": preset["id"],
            "exercise_id": 1,
            "block_order": 1,
            "goal_id": goal["id"]
        }
        pb = client.post("/preset_block/", json=pb_payload).json()["preset_block"]
        
        r = client.put(f"/preset_block/?id={pb['id']}", json={"block_order": 5})
        assert r.status_code == 200
        assert r.json()["preset_block"]["block_order"] == 5

    def test_update_preset_set(self, client, make_athlete, make_goal):
        athlete = make_athlete()
        p = client.post("/program/", json={"athlete_id": athlete["id"], "name": "P"}).json()["program"]
        preset = client.post("/preset/", json={"program_id": p["id"], "name": "Pr"}).json()["preset"]
        goal = make_goal(athlete["id"])
        pb = client.post("/preset_block/", json={
            "preset_id": preset["id"], "exercise_id": 1, "block_order": 1, "goal_id": goal["id"]
        }).json()["preset_block"]
        
        ps = client.post("/preset_set/", json={
            "preset_block_id": pb["id"], "reps": 8, "set_order": 1
        }).json()["preset_set"]
        
        r = client.put(f"/preset_set/?id={ps['id']}", json={"reps": 12})
        assert r.status_code == 200
        assert r.json()["preset_set"]["reps"] == 12
