"""
Test configuration for the lifting-website backend.

Strategy:
- Patches `backend.src.db.Database.engine` with an in-memory SQLite engine
  BEFORE `backend.app` is imported, so all routes use the test DB.
- Seeds the four immutable tables once at session start.
- Cleans all mutable tables after each test to ensure isolation.
"""
import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

# ---------------------------------------------------------------------------
# 1. Ensure the project root (parent of 'backend/') is importable
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# ---------------------------------------------------------------------------
# 2. Build the test engine and patch the module-level `engine` variable
#    BEFORE backend.app is imported (app does `from .src.db.Database import engine`)
# ---------------------------------------------------------------------------
_TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # share one connection so all sessions see the same DB
)

import backend.src.db.Database as _db_module  # noqa: E402

_db_module.engine = _TEST_ENGINE  # patch before app import

# ---------------------------------------------------------------------------
# 3. Import app (picks up patched engine), create all tables
# ---------------------------------------------------------------------------
from backend.app import app  # noqa: E402
from backend.src.models.Database import (  # noqa: E402
    Athletes,
    Base,
    ExerciseBlocks,
    ExerciseSets,
    Exercises,
    Genders,
    Goals,
    Groups,
    Lifts,
    Types,
)
from fastapi.testclient import TestClient  # noqa: E402

Base.metadata.create_all(_TEST_ENGINE)

# ---------------------------------------------------------------------------
# 4. Seed immutable reference data (mirrors setup.py)
# ---------------------------------------------------------------------------
def _seed_immutable() -> None:
    with Session(_TEST_ENGINE) as session:
        session.add_all([Genders(name="Male"), Genders(name="Female")])
        session.add_all(
            [
                Groups(name="Chest"),
                Groups(name="Back"),
                Groups(name="Shoulders"),
                Groups(name="Arms"),
                Groups(name="Legs"),
            ]
        )
        session.add_all(
            [
                Types(name="Machine"),
                Types(name="Body Weight"),
                Types(name="Barbell"),
                Types(name="Dumbbell"),
                Types(name="Cable"),
            ]
        )
        session.add_all(
            [
                Exercises(name="BB Bench Press", type_id=3, group_id=1),
                Exercises(name="DB Bench Press", type_id=4, group_id=1),
                Exercises(name="DB Incline Bench Press", type_id=4, group_id=1),
                Exercises(name="Machine Flies", type_id=1, group_id=1),
                Exercises(name="Standing Cable Flies", type_id=5, group_id=1),
                Exercises(name="BB Bent Over Rows", type_id=3, group_id=2),
                Exercises(name="DB Incline Rows", type_id=4, group_id=2),
                Exercises(name="DB Rows", type_id=4, group_id=2),
                Exercises(name="Lat Pull Downs", type_id=1, group_id=2),
                Exercises(name="Seated Cable Rows", type_id=5, group_id=2),
            ]
        )
        session.commit()


_seed_immutable()

# ---------------------------------------------------------------------------
# 5. Shared fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_mutable_tables():
    """Wipe all mutable rows after each test to guarantee isolation."""
    yield
    with Session(_TEST_ENGINE) as session:
        session.query(ExerciseSets).delete()
        session.query(ExerciseBlocks).delete()
        session.query(Goals).delete()
        session.query(Lifts).delete()
        session.query(Athletes).delete()
        session.commit()


# ---------------------------------------------------------------------------
# 6. Data factories
# ---------------------------------------------------------------------------
@pytest.fixture
def make_athlete(client):
    def _create(**overrides):
        payload = {
            "name": "Test Athlete",
            "dob": "2000-06-15T00:00:00",
            "gender_id": 1,
            "height": 175,
            "xp": 3,
            **overrides,
        }
        r = client.post("/athlete/", json=payload)
        assert r.status_code == 200, r.text
        return r.json()["athlete"]

    return _create


@pytest.fixture
def make_lift(client):
    def _create(athlete_id: int, **overrides):
        payload = {
            "athlete_id": athlete_id,
            "date": "2024-03-01T09:00:00",
            "body_weight": 80,
            **overrides,
        }
        r = client.post("/lift/", json=payload)
        assert r.status_code == 200, r.text
        return r.json()["lift"]

    return _create


@pytest.fixture
def make_goal(client):
    def _create(athlete_id: int, exercise_id: int = 1, **overrides):
        payload = {
            "athlete_id": athlete_id,
            "start_date": "2024-03-01T00:00:00",
            "duration": 30,
            "exercise_id": exercise_id,
            "reps": 8,
            "weight": 100,
            **overrides,
        }
        r = client.post("/goal/", json=payload)
        assert r.status_code == 200, r.text
        return r.json()["goal"]

    return _create


@pytest.fixture
def make_block(client):
    def _create(lift_id: int, exercise_id: int = 1, goal_id: int = 0, **overrides):
        payload = {
            "lift_id": lift_id,
            "exercise_id": exercise_id,
            "block_order": 1,
            "goal_id": goal_id,
            **overrides,
        }
        r = client.post("/exercise_block/", json=payload)
        assert r.status_code == 200, r.text
        return r.json()["exercise_block"]

    return _create


@pytest.fixture
def make_set(client):
    def _create(block_id: int, **overrides):
        payload = {
            "block_id": block_id,
            "weight": 60,
            "reps": 10,
            "rtl": 2,
            "set_order": 1,
            **overrides,
        }
        r = client.post("/exercise_set/", json=payload)
        assert r.status_code == 200, r.text
        return r.json()["exercise_set"]

    return _create
