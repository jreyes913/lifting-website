# Testing Implementation Report

## Overview

- **Date**: 2026-04-04
- **Stack**: FastAPI + SQLAlchemy 2.0 (Python), Vanilla JS (frontend)
- **Test Runner**: pytest 9.0.2
- **Test DB**: SQLite in-memory (`StaticPool`) — zero impact on production data
- **Total Tests**: 102 — all passing
- **Run Time**: ~1 second

### How to Run

```bash
# From the project root (lifting-website/)
# 1. Activate the venv
backend\.venv\Scripts\activate

# 2. Install test dependency (one-time)
pip install -r backend/requirements-dev.txt

# 3. Run all tests
python -m pytest
```

---

## Backend Coverage

### Suite: `backend/tests/test_immutable.py` (21 tests)

**Focus:** Validates that all seeded reference-data endpoints return correct payloads.

| Class | Endpoints Covered | What Is Tested |
|---|---|---|
| `TestGroups` | `GET /groups/`, `GET /group/` | Count (5), names, shape, ID lookup |
| `TestGenders` | `GET /genders/`, `GET /gender/` | Count (2), Male/Female values, lookup |
| `TestTypes` | `GET /types/`, `GET /type/` | Count (5), all type names, shape, lookup |
| `TestExercises` | `GET /exercises/`, `GET /exercise/` | Count (10), shape, FK values, group distribution |

---

### Suite: `backend/tests/test_athletes.py` (18 tests)

**Focus:** Full CRUD lifecycle for athletes.

| Class | What Is Tested |
|---|---|
| `TestCreateAthlete` | POST returns 200 + `message: success`, ID assigned, shape, value persistence, DOB round-trip |
| `TestGetAllAthletes` | Empty list on clean state, count after 1/2 creates, name set correctness |
| `TestGetAthleteById` | Correct record returned, message, multi-athlete disambiguation |
| `TestDeleteAthlete` | Record removed from list, remaining list returned, empty-list after last delete |

---

### Suite: `backend/tests/test_goals.py` (13 tests)

**Focus:** Full CRUD lifecycle for goals.

| Class | What Is Tested |
|---|---|
| `TestCreateGoal` | POST shape, value persistence (duration, reps, weight, exercise_id), 200 status |
| `TestGetAllGoals` | Empty state, single/multi create counts, multi-athlete goal distribution |
| `TestGetGoalById` | ID and field lookup |
| `TestDeleteGoal` | Removal from list, correct remaining entries returned |

---

### Suite: `backend/tests/test_lifts.py` (13 tests)

**Focus:** Full CRUD lifecycle for lift sessions.

| Class | What Is Tested |
|---|---|
| `TestCreateLift` | POST shape, `body_weight` and `date` persistence, 200 status |
| `TestGetAllLifts` | Empty state, same-athlete multi-lift, cross-athlete lift set |
| `TestGetLiftById` | ID and field lookup |
| `TestDeleteLift` | Removal, sibling lifts untouched, correct remaining list |

---

### Suite: `backend/tests/test_exercise_blocks.py` (14 tests)

**Focus:** Full CRUD lifecycle for exercise blocks.

| Class | What Is Tested |
|---|---|
| `TestCreateExerciseBlock` | POST shape, exercise_id/block_order persistence, 200 status |
| `TestGetAllExerciseBlocks` | Empty state, same-lift multi-block, block_order set |
| `TestGetExerciseBlockById` | ID, exercise_id, block_order lookup |
| `TestDeleteExerciseBlock` | Removal, sibling blocks preserved, correct remaining list |

---

### Suite: `backend/tests/test_exercise_sets.py` (13 tests)

**Focus:** Full CRUD lifecycle for exercise sets.

| Class | What Is Tested |
|---|---|
| `TestCreateExerciseSet` | POST shape, all fields (weight, reps, rtl, set_order), 200 status |
| `TestGetAllExerciseSets` | Empty state, multi-set same block (3 sets), cross-block set distribution |
| `TestGetExerciseSetById` | ID and field lookup |
| `TestDeleteExerciseSet` | Removal, sibling sets in block untouched |

---

### Suite: `backend/tests/test_cascade_delete.py` (8 tests)

**Focus:** Validates the backend supports the cascade-delete sequences orchestrated by the frontend (`script.js`).

> The backend has NO cascade-delete logic — it deletes one record at a time. The frontend drives the order. These tests confirm the API correctly supports all three cascade patterns.

| Class | Scenario Tested |
|---|---|
| `TestAthleteFullCascadeDelete` | Full hierarchy (athlete → goal → lift → 2 blocks → 4 sets) wiped to empty via frontend delete sequence |
| `TestAthleteFullCascadeDelete` | Sibling athlete's data (lift, block, set) untouched after first athlete cascade |
| `TestLiftCascadeDelete` | Lift's blocks and sets wiped; athlete row untouched |
| `TestLiftCascadeDelete` | Sibling lift's blocks and sets untouched after one lift cascade |
| `TestBlockCascadeDelete` | Block's sets wiped; block removed |
| `TestBlockCascadeDelete` | Sibling block's sets untouched after one block cascade |

---

## Test Infrastructure

### `backend/tests/conftest.py`

- **Engine patching**: `backend.src.db.Database.engine` is replaced with a `StaticPool` in-memory SQLite engine _before_ `backend.app` is imported, so all routes transparently use the test DB.
- **Immutable seeding**: Genders, Groups, Types, and Exercises are inserted once at session start, mirroring `setup.py`.
- **Mutable cleanup**: An `autouse` fixture wipes `exercise_sets`, `exercise_blocks`, `goals`, `lifts`, and `athletes` after every test, guaranteeing isolation with no test ordering dependencies.
- **Factories**: `make_athlete`, `make_lift`, `make_goal`, `make_block`, `make_set` fixtures provide reusable, DRY data creation across all test files.

### `pytest.ini`

Located at the project root. Configures `testpaths = backend/tests` so running `python -m pytest` from anywhere in the project root discovers all tests.

### `backend/requirements-dev.txt`

```
pytest>=8.0
```

`httpx` (required by FastAPI's `TestClient`) was already present in `requirements.txt`.

---

## Bugs Documented (Not Fixed)

The following issues were discovered during testing but are outside the scope of this suite (production logic was not modified per the instructions):

1. **No 404 handling on single-record fetches**: `GET /athlete/?id=999` (non-existent ID) causes a `500 Internal Server Error` because `session.query(...).first()` returns `None`, and `model_validate(None)` raises a Pydantic `ValidationError`. This applies to all `GET /entity/?id=X` and `DELETE /entity/?id=X` endpoints. A proper fix would add a `404 Not Found` response when the record does not exist.

2. **`GET /gender/` uses `GroupResponse` schema**: `app.py` line 50 calls `sch.GroupResponse.model_validate(db_gender)` instead of `sch.GenderResponse.model_validate(db_gender)`. Both schemas have identical fields (`id`, `name`), so no data is lost, but it is a latent defect if the schemas ever diverge.

3. **`ExerciseBlock.goal_id` is `NOT NULL` with no default**: Creating a block requires a `goal_id`. If an athlete has no goals, the frontend must supply a sentinel value (e.g., `0`), which is not a valid FK reference. SQLite does not enforce FK integrity by default, so this silently succeeds — but it is a data integrity risk.

4. **Pydantic V2 deprecation warnings**: All `class Config` definitions in `Schema.py` use the deprecated V1 style. These should be migrated to `model_config = ConfigDict(from_attributes=True)` before upgrading to Pydantic V3.

---

## Frontend Testing

Frontend testing (E2E/component) was not implemented in this pass. The frontend is a vanilla JS SPA with no build system, making Playwright (installable via `pip install playwright`) the appropriate tool. Recommended suites:

- `e2e/test_athlete_flow.py` — Create athlete → navigate to athlete page → create lift → verify render
- `e2e/test_block_flow.py` — Full drill-down: athlete → lift → block → add sets → verify display
- `e2e/test_delete_flows.py` — Delete at each level, verify UI updates (no ghost entries)

These are deferred due to requiring a live server (`uvicorn` + a static file server on port 8100).
