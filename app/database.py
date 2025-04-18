from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from app.config import Config

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]

    try:
        # Ensure indexes
        await db.users.create_index([("telegram_id", ASCENDING)], unique=True)
        await db.streams.create_index([("group_id", ASCENDING)], unique=True, sparse=True)
    except DuplicateKeyError as e:
        # Handle specific error if needed (e.g., log or pass)
        print(f"Error creating index: {e}")

async def close_mongo_connection():
    client.close()

def get_db():
    return db