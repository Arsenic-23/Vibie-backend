from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from app.config import Config  # Import Config class

# Get the database URL from the Config class
SQLALCHEMY_DATABASE_URL = Config.MONGO_URI  # or use Config.DB_NAME for specific database name if needed

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()