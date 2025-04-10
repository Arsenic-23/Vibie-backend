import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "vibie")

_client = None
_db = None

async def connect_to_mongo():
    global _client, _db
    _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    _db = _client[DB_NAME]
    print(f"Connected to MongoDB at {MONGO_URI}")

def get_db():
    if _db is None:
        raise Exception("Database connection has not been established. Call connect_to_mongo() first.")
    return _db