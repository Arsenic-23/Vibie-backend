import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "vibie")

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None
_db = None

async def connect_to_mongo():
    global _client, _db
    _client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    _db = _client[DB_NAME]
    print(f"[MongoDB] Connected to database '{DB_NAME}' at {MONGO_URI}")

def get_db():
    if _db is None:
        raise RuntimeError("Database not connected. Please call connect_to_mongo() during startup.")
    return _db