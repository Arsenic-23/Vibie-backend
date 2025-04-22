import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING
from app.config import settings

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_to_mongo():
    global client, db
    try:
        logger.info("Connecting to MongoDB...")
        client = AsyncIOMotorClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]
        logger.info(f"Connected to MongoDB: {settings.DB_NAME}")

        # Ensure indexes
        await db.streams.create_index(
            [("chat_id", ASCENDING)],  # Changed from 'group_id' to 'chat_id'
            unique=True,
            partialFilterExpression={"chat_id": {"$exists": True}},
        )
        await db.users.create_index("telegram_id", unique=True)

        logger.info("Indexes ensured on 'streams' and 'users' collections.")

    except Exception as e:
        logger.exception("Error connecting to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        logger.info("Closing MongoDB connection...")
        client.close()
        logger.info("MongoDB connection closed.")

def get_db() -> AsyncIOMotorDatabase:
    if db is None:
        logger.error("Database connection is not established.")
        raise RuntimeError("Database connection is not established.")
    return db