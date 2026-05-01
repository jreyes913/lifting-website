from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ===== Immutable Schemas ===== #
class GenderResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: int
    name: str
    type_id: int
    group_id: int

    class Config:
        from_attributes = True


# ===== Create Schemas ===== #
class AthleteCreate(BaseModel):
    name: str
    dob: datetime
    gender_id: int
    height: int
    xp: int


class GoalCreate(BaseModel):
    athlete_id: int
    start_date: datetime
    duration: int
    exercise_id: int
    reps: int
    weight: int


class LiftCreate(BaseModel):
    athlete_id: int
    date: datetime
    body_weight: int


class ExerciseBlockCreate(BaseModel):
    lift_id: int
    exercise_id: int
    block_order: int
    goal_id: int


class ExerciseSetCreate(BaseModel):
    block_id: int
    weight: int
    reps: int
    rtl: int
    set_order: int


# ===== Update Schemas ===== #
class AthleteUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[datetime] = None
    gender_id: Optional[int] = None
    height: Optional[int] = None
    xp: Optional[int] = None


class GoalUpdate(BaseModel):
    start_date: Optional[datetime] = None
    duration: Optional[int] = None
    exercise_id: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[int] = None


class LiftUpdate(BaseModel):
    date: Optional[datetime] = None
    body_weight: Optional[int] = None


class ExerciseBlockUpdate(BaseModel):
    exercise_id: Optional[int] = None
    block_order: Optional[int] = None
    goal_id: Optional[int] = None


class ExerciseSetUpdate(BaseModel):
    weight: Optional[int] = None
    reps: Optional[int] = None
    rtl: Optional[int] = None
    set_order: Optional[int] = None


# ===== Response Schemas ===== #
class AthleteResponse(BaseModel):
    id: int
    name: str
    dob: datetime
    gender_id: int
    height: int
    xp: int

    class Config:
        from_attributes = True


class GoalResponse(BaseModel):
    id: int
    athlete_id: int
    start_date: datetime
    duration: int
    exercise_id: int
    reps: int
    weight: int

    class Config:
        from_attributes = True


class LiftResponse(BaseModel):
    id: int
    athlete_id: int
    date: datetime
    body_weight: int

    class Config:
        from_attributes = True


class ExerciseBlockResponse(BaseModel):
    id: int
    lift_id: int
    exercise_id: int
    block_order: int
    goal_id: int

    class Config:
        from_attributes = True


class ExerciseSetResponse(BaseModel):
    id: int
    block_id: int
    weight: int
    reps: int
    rtl: int
    set_order: int

    class Config:
        from_attributes = True


# ===== Program/Preset Create Schemas ===== #
class ProgramCreate(BaseModel):
    athlete_id: int
    name: str


class PresetCreate(BaseModel):
    program_id: int
    name: str


class PresetBlockCreate(BaseModel):
    preset_id: int
    exercise_id: int
    block_order: int
    goal_id: int


class PresetSetCreate(BaseModel):
    preset_block_id: int
    reps: int
    set_order: int


# ===== Program/Preset Update Schemas ===== #
class ProgramUpdate(BaseModel):
    name: Optional[str] = None


class PresetUpdate(BaseModel):
    name: Optional[str] = None


class PresetBlockUpdate(BaseModel):
    exercise_id: Optional[int] = None
    block_order: Optional[int] = None
    goal_id: Optional[int] = None


class PresetSetUpdate(BaseModel):
    reps: Optional[int] = None
    set_order: Optional[int] = None


# ===== Program/Preset Response Schemas ===== #
class ProgramResponse(BaseModel):
    id: int
    athlete_id: int
    name: str

    class Config:
        from_attributes = True


class PresetResponse(BaseModel):
    id: int
    program_id: int
    name: str

    class Config:
        from_attributes = True


class PresetBlockResponse(BaseModel):
    id: int
    preset_id: int
    exercise_id: int
    block_order: int
    goal_id: int

    class Config:
        from_attributes = True


class PresetSetResponse(BaseModel):
    id: int
    preset_block_id: int
    reps: int
    set_order: int

    class Config:
        from_attributes = True


# ===== Apply Preset Schema ===== #
class ApplyPresetRequest(BaseModel):
    lift_id: int
    preset_id: int


# ===== Import/Export Schemas (Flat Table Structure) ===== #

class GenderImport(BaseModel):
    id: int
    name: str

class GroupImport(BaseModel):
    id: int
    name: str

class TypeImport(BaseModel):
    id: int
    name: str

class ExerciseImport(BaseModel):
    id: int
    name: str
    type_id: int
    group_id: int

class AthleteImport(BaseModel):
    id: int
    name: str
    dob: datetime
    gender_id: int
    height: int
    xp: int

class GoalImport(BaseModel):
    id: int
    athlete_id: int
    start_date: datetime
    duration: int
    exercise_id: int
    reps: int
    weight: int

class LiftImport(BaseModel):
    id: int
    athlete_id: int
    date: datetime
    body_weight: int

class ExerciseBlockImport(BaseModel):
    id: int
    lift_id: int
    exercise_id: int
    block_order: int
    goal_id: int

class ExerciseSetImport(BaseModel):
    id: int
    block_id: int
    weight: int
    reps: int
    rtl: int
    set_order: int

class ProgramImport(BaseModel):
    id: int
    athlete_id: int
    name: str

class PresetImport(BaseModel):
    id: int
    program_id: int
    name: str

class PresetBlockImport(BaseModel):
    id: int
    preset_id: int
    exercise_id: int
    block_order: int
    goal_id: int

class PresetSetImport(BaseModel):
    id: int
    preset_block_id: int
    reps: int
    set_order: int

class ImportData(BaseModel):
    export_metadata: dict | None = None
    genders: list[GenderImport] = Field(default_factory=list)
    groups: list[GroupImport] = Field(default_factory=list)
    types: list[TypeImport] = Field(default_factory=list)
    exercises: list[ExerciseImport] = Field(default_factory=list)
    athletes: list[AthleteImport] = Field(default_factory=list)
    goals: list[GoalImport] = Field(default_factory=list)
    lifts: list[LiftImport] = Field(default_factory=list)
    exercise_blocks: list[ExerciseBlockImport] = Field(default_factory=list)
    exercise_sets: list[ExerciseSetImport] = Field(default_factory=list)
    programs: list[ProgramImport] = Field(default_factory=list)
    presets: list[PresetImport] = Field(default_factory=list)
    preset_blocks: list[PresetBlockImport] = Field(default_factory=list)
    preset_sets: list[PresetSetImport] = Field(default_factory=list)
