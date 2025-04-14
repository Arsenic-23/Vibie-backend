from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from app.config import Config

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]

    # Ensure indexes
    await db.users.create_index("telegramId", unique=True)
    await db.streams.create_index([("group_id", ASCENDING)], unique=True)

async def close_mongo_connection():
    client.close()

def get_db():
    return db