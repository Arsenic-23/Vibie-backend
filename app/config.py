import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MongoDB URI and Database name
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://romanrule7668:2tNPrgHMf9xCM82a@vibie.mmq1pj4.mongodb.net/vibie?retryWrites=true&w=majority&appName=Vibie")
DB_NAME = os.getenv("DB_NAME", "vibie_db")

# API keys or any other sensitive information
API_KEY = os.getenv("API_KEY", "AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")
SEARCH_API = os.getenv("SEARCH_API", "https://your-music-api.com/search")
HITS_API = os.getenv("HITS_API", "https://your-music-api.com/hits")

# WebSocket configurations
WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT", 8001)
WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")

# Authentication Config
SECRET_KEY = os.getenv("SECRET_KEY", "1235679866_htrtjwwqeryoplknvxzdhj")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Other configurations can be added here as needed