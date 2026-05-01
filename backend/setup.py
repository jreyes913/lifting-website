import os

from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import Session
from src.db.Database import Base
from src.models.Database import *

db_path = "sqlite:///C:/Users/Jose/lifting-website/backend/data/database.db"
db_file = "C:/Users/Jose/lifting-website/backend/data/database.db"
if os.path.exists(db_file):
    os.remove(db_file)
engine = create_engine(db_path)
Base.metadata.create_all(engine)

with Session(engine) as session:
    genders = [Genders(name="Male"), Genders(name="Female")]
    session.add_all(genders)

    groups = [
        Groups(name="Chest"),
        Groups(name="Back"),
        Groups(name="Shoulders"),
        Groups(name="Arms"),
        Groups(name="Legs"),
    ]
    session.add_all(groups)

    types = [
        Types(name="Machine"),
        Types(name="Body Weight"),
        Types(name="Barbell"),
        Types(name="Dumbbell"),
        Types(name="Cable"),
    ]
    session.add_all(types)

    exercises = [
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
        Exercises(name="DB Lat Raise", type_id=4, group_id=3),
        Exercises(name="Rope Face Pulls", type_id=5, group_id=3),
        Exercises(name="DB Shoulder Press", type_id=4, group_id=3),
        Exercises(name="Machine Rear Delt Flies", type_id=1, group_id=3),
        Exercises(name="DB Shrugs", type_id=4, group_id=3),
        Exercises(name="BB Back Squat", type_id=3, group_id=5),
        Exercises(name="BB RDL", type_id=3, group_id=5),
        Exercises(name="RFE Split Squat", type_id=4, group_id=5),
        Exercises(name="Leg Press", type_id=1, group_id=5),
        Exercises(name="Leg Extention", type_id=1, group_id=5),
    ]
    session.add_all(exercises)

    session.commit()
