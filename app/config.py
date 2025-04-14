import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "vibie_db")

    API_KEY = os.getenv("API_KEY", "")
    SEARCH_API = os.getenv("SEARCH_API", "")
    HITS_API = os.getenv("HITS_API", "")

    WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8001))
    WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")

    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Config()