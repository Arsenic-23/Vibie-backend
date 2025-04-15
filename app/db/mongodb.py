from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from app.config import settings

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    # Ensure indexes
    await db.streams.create_index(
        [("group_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"group_id": {"$exists": True, "$ne": None}}
    )
    await db.users.create_index("user_id", unique=True)

async def close_mongo_connection():
    if client:
        client.close()

def get_db():
    return db