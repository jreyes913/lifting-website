import os

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import create_engine

db_path = os.getenv('DATABASE_URL', 'sqlite:///./data/database.db')
engine = create_engine(db_path)

class Base(MappedAsDataclass, DeclarativeBase):
    pass
