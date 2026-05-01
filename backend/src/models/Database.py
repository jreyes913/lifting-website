from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db.Database import Base


# ===== Immutable Columns ===== #
class Genders(Base):
    __tablename__ = "genders_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class Groups(Base):
    __tablename__ = "groups_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class Types(Base):
    __tablename__ = "types_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class Exercises(Base):
    __tablename__ = "exercises_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, nullable=False)


# ===== Mutable Columns ===== #
class Athletes(Base):
    __tablename__ = "athletes_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    dob: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    gender_id: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    xp: Mapped[int] = mapped_column(Integer, nullable=False)


class Goals(Base):
    __tablename__ = "goals_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    athlete_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int]


class Lifts(Base):
    __tablename__ = "lifts_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    athlete_id: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    body_weight: Mapped[int] = mapped_column(Integer, nullable=False)


class ExerciseBlocks(Base):
    __tablename__ = "exercise_blocks_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    lift_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_id: Mapped[int] = mapped_column(Integer, nullable=False)
    block_order: Mapped[int] = mapped_column(Integer, nullable=False)
    goal_id: Mapped[int] = mapped_column(Integer, nullable=False)


class ExerciseSets(Base):
    __tablename__ = "exercise_sets_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    rtl: Mapped[int] = mapped_column(Integer, nullable=False)
    set_order: Mapped[int] = mapped_column(Integer, nullable=False)


# ===== Program/Preset Tables ===== #
class Programs(Base):
    __tablename__ = "programs_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    athlete_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class Presets(Base):
    __tablename__ = "presets_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    program_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class PresetBlocks(Base):
    __tablename__ = "preset_blocks_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    preset_id: Mapped[int] = mapped_column(Integer, nullable=False)
    exercise_id: Mapped[int] = mapped_column(Integer, nullable=False)
    block_order: Mapped[int] = mapped_column(Integer, nullable=False)
    goal_id: Mapped[int] = mapped_column(Integer, nullable=False)


class PresetSets(Base):
    __tablename__ = "preset_sets_table"
    id: Mapped[int] = mapped_column(Integer, init=False, primary_key=True)
    preset_block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    set_order: Mapped[int] = mapped_column(Integer, nullable=False)
