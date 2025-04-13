from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from app.config import Config

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]

    # Ensure indexes (e.g. for stream_id to be unique)
    await db.streams.create_index([("group_id", ASCENDING)], unique=True)
    await db.users.create_index("user_id", unique=True)

async def close_mongo_connection():
    if client:
        client.close()

def get_db():
    return db