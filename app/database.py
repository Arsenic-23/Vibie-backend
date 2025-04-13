from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.config import settings  # Import settings from the config file

SQLALCHEMY_DATABASE_URL = settings.MONGO_URI  # Adjusted to use MONGO_URI or DATABASE_URL as needed

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()