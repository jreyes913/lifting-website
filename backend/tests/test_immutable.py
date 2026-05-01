"""
Tests for the immutable (read-only) reference-data endpoints.
All data is seeded once in conftest.py and never mutated.
"""


class TestGroups:
    def test_get_all_groups_returns_success(self, client):
        r = client.get("/groups/")
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_get_all_groups_count(self, client):
        groups = client.get("/groups/").json()["groups"]
        assert len(groups) == 5

    def test_get_all_groups_names(self, client):
        names = {g["name"] for g in client.get("/groups/").json()["groups"]}
        assert names == {"Chest", "Back", "Shoulders", "Arms", "Legs"}

    def test_get_group_by_id(self, client):
        r = client.get("/group/", params={"id": 1})
        assert r.status_code == 200
        body = r.json()
        assert body["message"] == "success"
        assert body["group"]["id"] == 1
        assert body["group"]["name"] == "Chest"

    def test_get_group_response_shape(self, client):
        group = client.get("/group/", params={"id": 2}).json()["group"]
        assert set(group.keys()) == {"id", "name"}


class TestGenders:
    def test_get_all_genders_returns_success(self, client):
        r = client.get("/genders/")
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_get_all_genders_count(self, client):
        assert len(client.get("/genders/").json()["genders"]) == 2

    def test_get_all_genders_values(self, client):
        names = {g["name"] for g in client.get("/genders/").json()["genders"]}
        assert names == {"Male", "Female"}

    def test_get_gender_by_id(self, client):
        r = client.get("/gender/", params={"id": 1})
        assert r.status_code == 200
        gender = r.json()["gender"]
        assert gender["id"] == 1
        assert gender["name"] == "Male"

    def test_get_gender_female(self, client):
        gender = client.get("/gender/", params={"id": 2}).json()["gender"]
        assert gender["name"] == "Female"


class TestTypes:
    def test_get_all_types_returns_success(self, client):
        r = client.get("/types/")
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_get_all_types_count(self, client):
        assert len(client.get("/types/").json()["types"]) == 5

    def test_get_all_types_names(self, client):
        names = {t["name"] for t in client.get("/types/").json()["types"]}
        assert names == {"Machine", "Body Weight", "Barbell", "Dumbbell", "Cable"}

    def test_get_type_by_id(self, client):
        r = client.get("/type/", params={"id": 3})
        assert r.status_code == 200
        ex_type = r.json()["type"]
        assert ex_type["id"] == 3
        assert ex_type["name"] == "Barbell"

    def test_get_type_response_shape(self, client):
        ex_type = client.get("/type/", params={"id": 1}).json()["type"]
        assert set(ex_type.keys()) == {"id", "name"}


class TestExercises:
    def test_get_all_exercises_returns_success(self, client):
        r = client.get("/exercises/")
        assert r.status_code == 200
        assert r.json()["message"] == "success"

    def test_get_all_exercises_count(self, client):
        assert len(client.get("/exercises/").json()["exercises"]) == 10

    def test_get_exercise_by_id(self, client):
        r = client.get("/exercise/", params={"id": 1})
        assert r.status_code == 200
        exercise = r.json()["exercise"]
        assert exercise["id"] == 1
        assert exercise["name"] == "BB Bench Press"

    def test_get_exercise_response_shape(self, client):
        exercise = client.get("/exercise/", params={"id": 1}).json()["exercise"]
        assert set(exercise.keys()) == {"id", "name", "type_id", "group_id"}

    def test_get_exercise_foreign_keys(self, client):
        # BB Bench Press: type=Barbell(3), group=Chest(1)
        exercise = client.get("/exercise/", params={"id": 1}).json()["exercise"]
        assert exercise["type_id"] == 3
        assert exercise["group_id"] == 1

    def test_exercises_include_back_exercises(self, client):
        exercises = client.get("/exercises/").json()["exercises"]
        back_exercises = [e for e in exercises if e["group_id"] == 2]
        assert len(back_exercises) == 5
