from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING
from app.config import Config

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def connect_to_mongo():
    """Connects to MongoDB and ensures necessary indexes are created."""
    global client, db
    try:
        client = AsyncIOMotorClient(Config.MONGO_URI)
        db = client[Config.DB_NAME]

        # Ensure indexes
        await db.users.create_index([("telegram_id", ASCENDING)], unique=True)
        await db.streams.create_index([("group_id", ASCENDING)], unique=True, sparse=True)

        print("Successfully connected to MongoDB and ensured indexes.")

    except DuplicateKeyError as e:
        print(f"Error creating index: {e}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise RuntimeError("Failed to connect to MongoDB")

async def close_mongo_connection():
    """Closes the MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")
    else:
        print("MongoDB connection is not established.")

def get_db() -> AsyncIOMotorDatabase:
    """Returns the MongoDB database instance."""
    if db is None:
        raise RuntimeError("Database connection is not established.")
    return db