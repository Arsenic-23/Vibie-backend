import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MongoDB URI and Database name
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "vibie_db")

# API keys or any other sensitive information
API_KEY = os.getenv("AIzaSyDKZwdnrvfGJTiHdDGdemmjJ--jXnjwR1g")
SEARCH_API = os.getenv("AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")
HITS_API = os.getenv("AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")

# WebSocket configurations
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8001))  # Ensure the port is an integer
WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")

# Authentication Config
SECRET_KEY = os.getenv("83c2114f44b13d41e312ea6e3dbf6d4a7cde7af23bfb0f4f3d020947c7e5c5c")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Default to 30 minutes if not set

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Other configurations can be added here as needed