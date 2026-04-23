import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from uuid6 import uuid7

# database.py
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./insighta.db")

# FIX: Railway gives 'postgres://', but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid7()))
    name = Column(String, unique=True, index=True, nullable=False)
    gender = Column(String)
    gender_probability = Column(Float)
    age = Column(Integer)
    age_group = Column(String)
    country_id = Column(String(2))
    country_name = Column(String) # Required for Stage 2
    country_probability = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)