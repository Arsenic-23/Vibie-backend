from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING
from app.config import settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # Ensure indexes
    await db.streams.create_index(
        [("group_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"group_id": {"$exists": True}}  # Index only if group_id exists
    )
    await db.users.create_index("user_id", unique=True)

async def close_mongo_connection():
    if client:
        client.close()

def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("Database is not connected. Call connect_to_mongo first.")
    return db