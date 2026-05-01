from datetime import datetime, timezone

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .src.db.Database import engine
from .src.models import Database as db
from .src.models import Schema as sch

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100", "http://100.124.116.118:5173", "http://localhost:5173"],
    allow_methods=["*"],
    allow_credentials=True,
)


# ===== Immutable Routes ===== #
@app.get("/groups/")
async def get_all_groups():
    with Session(engine) as session:
        result = session.query(db.Groups).all()
    return {
        "message": "success",
        "groups": [sch.GroupResponse.model_validate(group) for group in result],
    }


@app.get("/group/")
async def get_group(id: int):
    with Session(engine) as session:
        db_group = session.query(db.Groups).filter(db.Groups.id == id).first()
    return {"message": "success", "group": sch.GroupResponse.model_validate(db_group)}


@app.get("/genders/")
async def get_all_genders():
    with Session(engine) as session:
        result = session.query(db.Genders).all()
    return {
        "message": "success",
        "genders": [sch.GenderResponse.model_validate(gender) for gender in result],
    }


@app.get("/gender/")
async def get_gender(id: int):
    with Session(engine) as session:
        db_gender = session.query(db.Genders).filter(db.Genders.id == id).first()
    return {
        "message": "success",
        "gender": sch.GenderResponse.model_validate(db_gender),
    }


@app.get("/types/")
async def get_all_types():
    with Session(engine) as session:
        result = session.query(db.Types).all()
    return {
        "message": "success",
        "types": [sch.TypeResponse.model_validate(type_ex) for type_ex in result],
    }


@app.get("/type/")
async def get_type(id: int):
    with Session(engine) as session:
        db_type = session.query(db.Types).filter(db.Types.id == id).first()
    return {"message": "success", "type": sch.TypeResponse.model_validate(db_type)}


@app.get("/exercises/")
async def get_all_exercises():
    with Session(engine) as session:
        result = session.query(db.Exercises).all()
    return {
        "message": "success",
        "exercises": [
            sch.ExerciseResponse.model_validate(exercise) for exercise in result
        ],
    }


@app.get("/exercise/")
async def get_exercise(id: int):
    with Session(engine) as session:
        db_exercise = session.query(db.Exercises).filter(db.Exercises.id == id).first()
    return {
        "message": "success",
        "exercise": sch.ExerciseResponse.model_validate(db_exercise),
    }


# ===== Mutable Routes ===== #
@app.get("/athletes/")
async def get_all_athletes():
    with Session(engine) as session:
        result = session.query(db.Athletes).all()
    return {
        "message": "success",
        "athletes": [sch.AthleteResponse.model_validate(athlete) for athlete in result],
    }


@app.get("/athlete/")
async def get_athlete(id: int):
    with Session(engine) as session:
        db_athlete = session.query(db.Athletes).filter(db.Athletes.id == id).first()
    return {
        "message": "success",
        "athlete": sch.AthleteResponse.model_validate(db_athlete),
    }


@app.post("/athlete/")
async def create_athlete(schema_athlete: sch.AthleteCreate):
    with Session(engine) as session:
        db_athlete = db.Athletes(**schema_athlete.model_dump())
        session.add(db_athlete)
        session.commit()
        session.refresh(db_athlete)
    return {
        "message": "success",
        "athlete": sch.AthleteResponse.model_validate(db_athlete),
    }


@app.put("/athlete/")
async def update_athlete(id: int, schema_athlete: sch.AthleteUpdate):
    with Session(engine) as session:
        db_athlete = session.query(db.Athletes).filter(db.Athletes.id == id).first()
        for key, value in schema_athlete.model_dump(exclude_none=True).items():
            setattr(db_athlete, key, value)
        session.commit()
        session.refresh(db_athlete)
    return {
        "message": "success",
        "athlete": sch.AthleteResponse.model_validate(db_athlete),
    }


@app.delete("/athlete/")
async def delete_athlete(id: int):
    with Session(engine) as session:
        db_athlete_to_delete = (
            session.query(db.Athletes).filter(db.Athletes.id == id).first()
        )
        session.delete(db_athlete_to_delete)
        session.commit()
        result = session.query(db.Athletes).all()
    return {
        "message": "success",
        "athletes": [sch.AthleteResponse.model_validate(athlete) for athlete in result],
    }


@app.get("/goals/")
async def get_all_goals():
    with Session(engine) as session:
        result = session.query(db.Goals).all()
    return {
        "message": "success",
        "goals": [sch.GoalResponse.model_validate(goal) for goal in result],
    }


@app.get("/goal/")
async def get_goal(id: int):
    with Session(engine) as session:
        db_goal = session.query(db.Goals).filter(db.Goals.id == id).first()
    return {"message": "success", "goal": sch.GoalResponse.model_validate(db_goal)}


@app.post("/goal/")
async def create_goal(schema_goal: sch.GoalCreate):
    with Session(engine) as session:
        db_goal = db.Goals(**schema_goal.model_dump())
        session.add(db_goal)
        session.commit()
        session.refresh(db_goal)
    return {"message": "success", "goal": sch.GoalResponse.model_validate(db_goal)}


@app.put("/goal/")
async def update_goal(id: int, schema_goal: sch.GoalUpdate):
    with Session(engine) as session:
        db_goal = session.query(db.Goals).filter(db.Goals.id == id).first()
        for key, value in schema_goal.model_dump(exclude_none=True).items():
            setattr(db_goal, key, value)
        session.commit()
        session.refresh(db_goal)
    return {"message": "success", "goal": sch.GoalResponse.model_validate(db_goal)}


@app.delete("/goal/")
async def delete_goal(id: int):
    with Session(engine) as session:
        db_goal_to_delete = session.query(db.Goals).filter(db.Goals.id == id).first()
        session.delete(db_goal_to_delete)
        session.commit()
        result = session.query(db.Goals).all()
    return {
        "message": "success",
        "goals": [sch.GoalResponse.model_validate(goal) for goal in result],
    }


@app.get("/lifts/")
def get_all_lifts():
    with Session(engine) as session:
        result = session.query(db.Lifts).all()
    return {
        "message": "success",
        "lifts": [sch.LiftResponse.model_validate(lift) for lift in result],
    }


@app.get("/lift/")
async def get_lift(id: int):
    with Session(engine) as session:
        db_lift = session.query(db.Lifts).filter(db.Lifts.id == id).first()
    return {"message": "success", "lift": sch.LiftResponse.model_validate(db_lift)}


@app.post("/lift/")
async def create_lift(schema_lift: sch.LiftCreate):
    with Session(engine) as session:
        db_lift = db.Lifts(**schema_lift.model_dump())
        session.add(db_lift)
        session.commit()
        session.refresh(db_lift)
    return {"message": "success", "lift": sch.LiftResponse.model_validate(db_lift)}


@app.put("/lift/")
async def update_lift(id: int, schema_lift: sch.LiftUpdate):
    with Session(engine) as session:
        db_lift = session.query(db.Lifts).filter(db.Lifts.id == id).first()
        for key, value in schema_lift.model_dump(exclude_none=True).items():
            setattr(db_lift, key, value)
        session.commit()
        session.refresh(db_lift)
    return {"message": "success", "lift": sch.LiftResponse.model_validate(db_lift)}


@app.delete("/lift/")
async def delete_lift(id: int):
    with Session(engine) as session:
        db_lift_to_delete = session.query(db.Lifts).filter(db.Lifts.id == id).first()
        session.delete(db_lift_to_delete)
        session.commit()
        result = session.query(db.Lifts).all()
    return {
        "message": "success",
        "lifts": [sch.LiftResponse.model_validate(lift) for lift in result],
    }


@app.get("/exercise_blocks/")
def get_all_exercise_blocks():
    with Session(engine) as session:
        result = session.query(db.ExerciseBlocks).all()
    return {
        "message": "success",
        "exercise_blocks": [
            sch.ExerciseBlockResponse.model_validate(exercise_block)
            for exercise_block in result
        ],
    }


@app.get("/exercise_block/")
async def get_exercise_block(id: int):
    with Session(engine) as session:
        db_exercise_block = (
            session.query(db.ExerciseBlocks).filter(db.ExerciseBlocks.id == id).first()
        )
    return {
        "message": "success",
        "exercise_block": sch.ExerciseBlockResponse.model_validate(db_exercise_block),
    }


@app.post("/exercise_block/")
async def create_exercise_block(schema_exercise_block: sch.ExerciseBlockCreate):
    with Session(engine) as session:
        db_exercise_block = db.ExerciseBlocks(**schema_exercise_block.model_dump())
        session.add(db_exercise_block)
        session.commit()
        session.refresh(db_exercise_block)
    return {
        "message": "success",
        "exercise_block": sch.ExerciseBlockResponse.model_validate(db_exercise_block),
    }


@app.put("/exercise_block/")
async def update_exercise_block(id: int, schema: sch.ExerciseBlockUpdate):
    with Session(engine) as session:
        db_block = (
            session.query(db.ExerciseBlocks).filter(db.ExerciseBlocks.id == id).first()
        )
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_block, key, value)
        session.commit()
        session.refresh(db_block)
    return {
        "message": "success",
        "exercise_block": sch.ExerciseBlockResponse.model_validate(db_block),
    }


@app.delete("/exercise_block/")
async def delete_exercise_block(id: int):
    with Session(engine) as session:
        db_exercise_block_to_delete = (
            session.query(db.ExerciseBlocks).filter(db.ExerciseBlocks.id == id).first()
        )
        session.delete(db_exercise_block_to_delete)
        session.commit()
        result = session.query(db.ExerciseBlocks).all()
    return {
        "message": "success",
        "exercise_blocks": [
            sch.ExerciseBlockResponse.model_validate(exercise_block)
            for exercise_block in result
        ],
    }


@app.get("/exercise_sets/")
def get_all_exercise_sets():
    with Session(engine) as session:
        result = session.query(db.ExerciseSets).all()
    return {
        "message": "success",
        "exercise_sets": [
            sch.ExerciseSetResponse.model_validate(exercise_set)
            for exercise_set in result
        ],
    }


@app.get("/exercise_set/")
async def get_exercise_set(id: int):
    with Session(engine) as session:
        db_exercise_set = (
            session.query(db.ExerciseSets).filter(db.ExerciseSets.id == id).first()
        )
    return {
        "message": "success",
        "exercise_set": sch.ExerciseSetResponse.model_validate(db_exercise_set),
    }


@app.post("/exercise_set/")
async def create_exercise_set(schema_exercise_set: sch.ExerciseSetCreate):
    with Session(engine) as session:
        db_exercise_set = db.ExerciseSets(**schema_exercise_set.model_dump())
        session.add(db_exercise_set)
        session.commit()
        session.refresh(db_exercise_set)
    return {
        "message": "success",
        "exercise_set": sch.ExerciseSetResponse.model_validate(db_exercise_set),
    }


@app.put("/exercise_set/")
async def update_exercise_set(id: int, schema: sch.ExerciseSetUpdate):
    with Session(engine) as session:
        db_set = (
            session.query(db.ExerciseSets).filter(db.ExerciseSets.id == id).first()
        )
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_set, key, value)
        session.commit()
        session.refresh(db_set)
    return {
        "message": "success",
        "exercise_set": sch.ExerciseSetResponse.model_validate(db_set),
    }


@app.delete("/exercise_set/")
async def delete_exercise_set(id: int):
    with Session(engine) as session:
        db_exercise_set_to_delete = (
            session.query(db.ExerciseSets).filter(db.ExerciseSets.id == id).first()
        )
        session.delete(db_exercise_set_to_delete)
        session.commit()
        result = session.query(db.ExerciseSets).all()
    return {
        "message": "success",
        "exercise_sets": [
            sch.ExerciseSetResponse.model_validate(exercise_set)
            for exercise_set in result
        ],
    }


# ===== Program/Preset Routes ===== #
@app.get("/programs/")
async def get_all_programs():
    with Session(engine) as session:
        result = session.query(db.Programs).all()
    return {
        "message": "success",
        "programs": [sch.ProgramResponse.model_validate(p) for p in result],
    }


@app.get("/program/")
async def get_program(id: int):
    with Session(engine) as session:
        db_program = session.query(db.Programs).filter(db.Programs.id == id).first()
    return {
        "message": "success",
        "program": sch.ProgramResponse.model_validate(db_program),
    }


@app.post("/program/")
async def create_program(schema_program: sch.ProgramCreate):
    with Session(engine) as session:
        db_program = db.Programs(**schema_program.model_dump())
        session.add(db_program)
        session.commit()
        session.refresh(db_program)
    return {
        "message": "success",
        "program": sch.ProgramResponse.model_validate(db_program),
    }


@app.put("/program/")
async def update_program(id: int, schema: sch.ProgramUpdate):
    with Session(engine) as session:
        db_program = session.query(db.Programs).filter(db.Programs.id == id).first()
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_program, key, value)
        session.commit()
        session.refresh(db_program)
    return {
        "message": "success",
        "program": sch.ProgramResponse.model_validate(db_program),
    }


@app.delete("/program/")
async def delete_program(id: int):
    with Session(engine) as session:
        db_program_to_delete = (
            session.query(db.Programs).filter(db.Programs.id == id).first()
        )
        session.delete(db_program_to_delete)
        session.commit()
        result = session.query(db.Programs).all()
    return {
        "message": "success",
        "programs": [sch.ProgramResponse.model_validate(p) for p in result],
    }


@app.get("/presets/")
async def get_all_presets():
    with Session(engine) as session:
        result = session.query(db.Presets).all()
    return {
        "message": "success",
        "presets": [sch.PresetResponse.model_validate(p) for p in result],
    }


@app.get("/preset/")
async def get_preset(id: int):
    with Session(engine) as session:
        db_preset = session.query(db.Presets).filter(db.Presets.id == id).first()
    return {
        "message": "success",
        "preset": sch.PresetResponse.model_validate(db_preset),
    }


@app.post("/preset/")
async def create_preset(schema_preset: sch.PresetCreate):
    with Session(engine) as session:
        db_preset = db.Presets(**schema_preset.model_dump())
        session.add(db_preset)
        session.commit()
        session.refresh(db_preset)
    return {
        "message": "success",
        "preset": sch.PresetResponse.model_validate(db_preset),
    }


@app.delete("/preset/")
async def delete_preset(id: int):
    with Session(engine) as session:
        db_preset_to_delete = (
            session.query(db.Presets).filter(db.Presets.id == id).first()
        )
        session.delete(db_preset_to_delete)
        session.commit()
        result = session.query(db.Presets).all()
    return {
        "message": "success",
        "presets": [sch.PresetResponse.model_validate(p) for p in result],
    }


@app.put("/preset/")
async def update_preset(id: int, schema: sch.PresetUpdate):
    with Session(engine) as session:
        db_preset = session.query(db.Presets).filter(db.Presets.id == id).first()
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_preset, key, value)
        session.commit()
        session.refresh(db_preset)
    return {
        "message": "success",
        "preset": sch.PresetResponse.model_validate(db_preset),
    }


@app.get("/preset_blocks/")
async def get_all_preset_blocks():
    with Session(engine) as session:
        result = session.query(db.PresetBlocks).all()
    return {
        "message": "success",
        "preset_blocks": [
            sch.PresetBlockResponse.model_validate(pb) for pb in result
        ],
    }


@app.get("/preset_block/")
async def get_preset_block(id: int):
    with Session(engine) as session:
        db_preset_block = (
            session.query(db.PresetBlocks).filter(db.PresetBlocks.id == id).first()
        )
    return {
        "message": "success",
        "preset_block": sch.PresetBlockResponse.model_validate(db_preset_block),
    }


@app.post("/preset_block/")
async def create_preset_block(schema_preset_block: sch.PresetBlockCreate):
    with Session(engine) as session:
        db_preset_block = db.PresetBlocks(**schema_preset_block.model_dump())
        session.add(db_preset_block)
        session.commit()
        session.refresh(db_preset_block)
    return {
        "message": "success",
        "preset_block": sch.PresetBlockResponse.model_validate(db_preset_block),
    }


@app.delete("/preset_block/")
async def delete_preset_block(id: int):
    with Session(engine) as session:
        db_preset_block_to_delete = (
            session.query(db.PresetBlocks).filter(db.PresetBlocks.id == id).first()
        )
        session.delete(db_preset_block_to_delete)
        session.commit()
        result = session.query(db.PresetBlocks).all()
    return {
        "message": "success",
        "preset_blocks": [
            sch.PresetBlockResponse.model_validate(pb) for pb in result
        ],
    }


@app.put("/preset_block/")
async def update_preset_block(id: int, schema: sch.PresetBlockUpdate):
    with Session(engine) as session:
        db_block = (
            session.query(db.PresetBlocks).filter(db.PresetBlocks.id == id).first()
        )
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_block, key, value)
        session.commit()
        session.refresh(db_block)
    return {
        "message": "success",
        "preset_block": sch.PresetBlockResponse.model_validate(db_block),
    }


@app.get("/preset_sets/")
async def get_all_preset_sets():
    with Session(engine) as session:
        result = session.query(db.PresetSets).all()
    return {
        "message": "success",
        "preset_sets": [sch.PresetSetResponse.model_validate(ps) for ps in result],
    }


@app.get("/preset_set/")
async def get_preset_set(id: int):
    with Session(engine) as session:
        db_preset_set = (
            session.query(db.PresetSets).filter(db.PresetSets.id == id).first()
        )
    return {
        "message": "success",
        "preset_set": sch.PresetSetResponse.model_validate(db_preset_set),
    }


@app.post("/preset_set/")
async def create_preset_set(schema_preset_set: sch.PresetSetCreate):
    with Session(engine) as session:
        db_preset_set = db.PresetSets(**schema_preset_set.model_dump())
        session.add(db_preset_set)
        session.commit()
        session.refresh(db_preset_set)
    return {
        "message": "success",
        "preset_set": sch.PresetSetResponse.model_validate(db_preset_set),
    }


@app.delete("/preset_set/")
async def delete_preset_set(id: int):
    with Session(engine) as session:
        db_preset_set_to_delete = (
            session.query(db.PresetSets).filter(db.PresetSets.id == id).first()
        )
        session.delete(db_preset_set_to_delete)
        session.commit()
        result = session.query(db.PresetSets).all()
    return {
        "message": "success",
        "preset_sets": [sch.PresetSetResponse.model_validate(ps) for ps in result],
    }


@app.put("/preset_set/")
async def update_preset_set(id: int, schema: sch.PresetSetUpdate):
    with Session(engine) as session:
        db_set = session.query(db.PresetSets).filter(db.PresetSets.id == id).first()
        for key, value in schema.model_dump(exclude_none=True).items():
            setattr(db_set, key, value)
        session.commit()
        session.refresh(db_set)
    return {
        "message": "success",
        "preset_set": sch.PresetSetResponse.model_validate(db_set),
    }


@app.post("/apply_preset/")
async def apply_preset(request: sch.ApplyPresetRequest):
    with Session(engine) as session:
        preset_blocks = (
            session.query(db.PresetBlocks)
            .filter(db.PresetBlocks.preset_id == request.preset_id)
            .all()
        )
        created_blocks = []
        for pb in preset_blocks:
            new_block = db.ExerciseBlocks(
                lift_id=request.lift_id,
                exercise_id=pb.exercise_id,
                block_order=pb.block_order,
                goal_id=pb.goal_id,
            )
            session.add(new_block)
            session.flush()
            preset_sets = (
                session.query(db.PresetSets)
                .filter(db.PresetSets.preset_block_id == pb.id)
                .all()
            )
            for ps in preset_sets:
                new_set = db.ExerciseSets(
                    block_id=new_block.id,
                    weight=0,
                    reps=ps.reps,
                    rtl=0,
                    set_order=ps.set_order,
                )
                session.add(new_set)
            created_blocks.append(new_block)
        session.commit()
        for b in created_blocks:
            session.refresh(b)
    return {
        "message": "success",
        "exercise_blocks": [
            sch.ExerciseBlockResponse.model_validate(b) for b in created_blocks
        ],
    }


@app.get("/export/")
async def export_data():
    with Session(engine) as session:
        return {
            "message": "success",
            "export_metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "3.0_flat",
            },
            "genders": [sch.GenderResponse.model_validate(x).model_dump() for x in session.query(db.Genders).all()],
            "groups": [sch.GroupResponse.model_validate(x).model_dump() for x in session.query(db.Groups).all()],
            "types": [sch.TypeResponse.model_validate(x).model_dump() for x in session.query(db.Types).all()],
            "exercises": [sch.ExerciseResponse.model_validate(x).model_dump() for x in session.query(db.Exercises).all()],
            "athletes": [sch.AthleteResponse.model_validate(x).model_dump() for x in session.query(db.Athletes).all()],
            "goals": [sch.GoalResponse.model_validate(x).model_dump() for x in session.query(db.Goals).all()],
            "lifts": [sch.LiftResponse.model_validate(x).model_dump() for x in session.query(db.Lifts).all()],
            "exercise_blocks": [sch.ExerciseBlockResponse.model_validate(x).model_dump() for x in session.query(db.ExerciseBlocks).all()],
            "exercise_sets": [sch.ExerciseSetResponse.model_validate(x).model_dump() for x in session.query(db.ExerciseSets).all()],
            "programs": [sch.ProgramResponse.model_validate(x).model_dump() for x in session.query(db.Programs).all()],
            "presets": [sch.PresetResponse.model_validate(x).model_dump() for x in session.query(db.Presets).all()],
            "preset_blocks": [sch.PresetBlockResponse.model_validate(x).model_dump() for x in session.query(db.PresetBlocks).all()],
            "preset_sets": [sch.PresetSetResponse.model_validate(x).model_dump() for x in session.query(db.PresetSets).all()],
        }


@app.post("/import/")
async def import_data(payload: sch.ImportData):
    with Session(engine) as session:
        # Clear everything
        session.query(db.PresetSets).delete()
        session.query(db.PresetBlocks).delete()
        session.query(db.Presets).delete()
        session.query(db.Programs).delete()
        session.query(db.ExerciseSets).delete()
        session.query(db.ExerciseBlocks).delete()
        session.query(db.Lifts).delete()
        session.query(db.Goals).delete()
        session.query(db.Athletes).delete()
        session.query(db.Exercises).delete()
        session.query(db.Types).delete()
        session.query(db.Groups).delete()
        session.query(db.Genders).delete()

        def add_all(model_class, items):
            for x in items:
                data = x.model_dump()
                obj_id = data.pop("id", None)
                obj = model_class(**data)
                if obj_id is not None:
                    obj.id = obj_id
                session.add(obj)

        # Insert Immutable
        add_all(db.Genders, payload.genders)
        add_all(db.Groups, payload.groups)
        add_all(db.Types, payload.types)
        session.flush()
        add_all(db.Exercises, payload.exercises)
        session.flush()

        # Insert Mutable
        add_all(db.Athletes, payload.athletes)
        session.flush()
        add_all(db.Goals, payload.goals)
        add_all(db.Lifts, payload.lifts)
        add_all(db.Programs, payload.programs)
        session.flush()
        add_all(db.ExerciseBlocks, payload.exercise_blocks)
        add_all(db.Presets, payload.presets)
        session.flush()
        add_all(db.ExerciseSets, payload.exercise_sets)
        add_all(db.PresetBlocks, payload.preset_blocks)
        session.flush()
        add_all(db.PresetSets, payload.preset_sets)

        session.commit()

    return {"message": "success"}


# === CHARTING ENDPOINTS === #
@app.get("/lifts/athlete/")
async def get_athlete_lifts(athlete_id: int):
    with Session(engine) as session:
        query = text(
            "SELECT * FROM lifts_table WHERE athlete_id = :athlete_id ORDER BY date ASC"
        )
        result = session.execute(query, {"athlete_id": athlete_id})
    return {
        "message": "success",
        "lifts": [sch.LiftResponse.model_validate(lift) for lift in result],
    }


@app.get("/strength/")
async def get_1RM_calcs(athlete_id: int, exercise_id: int):
    with Session(engine) as session:
        lifts_query = text(
            "SELECT * FROM lifts_table WHERE athlete_id = :athlete_id ORDER BY date ASC"
        )
        lifts_df = pd.DataFrame(
            session.execute(lifts_query, {"athlete_id": athlete_id})
        )
        lifts_df.date = pd.to_datetime(lifts_df.date)
        exercise_query = text("SELECT * FROM exercises_table WHERE id = :exercise_id")
        exercise = session.execute(exercise_query, {"exercise_id": exercise_id}).first()
        exercise_blocks = []
        for idx, row in lifts_df.iterrows():
            lift_id = row.id
            exercise_blocks_query = text(
                "SELECT * FROM exercise_blocks_table WHERE lift_id = :lift_id"
            )
            exercise_blocks_df_chunk = pd.DataFrame(
                session.execute(exercise_blocks_query, {"lift_id": lift_id})
            )
            exercise_blocks_df_chunk["date"] = row.date
            exercise_blocks_df_chunk["body_weight"] = row.body_weight
            exercise_blocks.append(exercise_blocks_df_chunk)
        exercise_blocks_df = pd.concat(exercise_blocks)
        exercise_sets = []
        for idx, row in exercise_blocks_df.iterrows():
            if row.exercise_id == exercise_id:
                block_id = row.id
                exercise_sets_query = text(
                    "SELECT * FROM exercise_sets_table WHERE block_id = :block_id"
                )
                exercise_sets_df_chunk = pd.DataFrame(
                    session.execute(exercise_sets_query, {"block_id": block_id})
                )
                exercise_sets_df_chunk["date"] = row.date
                exercise_sets_df_chunk["body_weight"] = row.body_weight
                exercise_sets.append(exercise_sets_df_chunk)
        exercise_sets_df = pd.concat(exercise_sets)
        exercise_sets_df.sort_values(by=["date", "set_order"], inplace=True)
        calc_1RM_df = exercise_sets_df[exercise_sets_df["rtl"] < 6]

        def pred_1RM(row):
            if row.rtl <= 3:
                return row.weight * (1 + (row.reps + row.rtl) / 30)
            else:
                return row.weight * (1 + (row.reps + row.rtl) / 40)

        calc_1RM_df["1RM"] = calc_1RM_df.apply(pred_1RM, axis=1)
        calc_1RM_df_grpby = calc_1RM_df.groupby(by=["date"])["1RM"].max().reset_index()
        exercise_sets_df["1RM"] = exercise_sets_df["date"].apply(
            lambda x: calc_1RM_df_grpby[calc_1RM_df_grpby["date"] == x]["1RM"].iloc[0]
        )
        exercise_sets_df["intensity"] = (
            exercise_sets_df["weight"] / exercise_sets_df["1RM"]
        )

        exercise_sets_df["load"] = (
            exercise_sets_df["intensity"]
            * exercise_sets_df["weight"]
            * (exercise_sets_df["reps"] * (1 / (1 + 0.5 * exercise_sets_df["rtl"])))
        )
        exercise_sets_df["volume"] = exercise_sets_df.groupby(["date"])["load"].cumsum()
        exercise_sets_result = exercise_sets_df.to_json(orient="records", date_format="iso")
        return {"message": "success", "data": exercise_sets_result}

