import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
API_KEY = os.getenv("API_KEY", "")
SEARCH_API = os.getenv("SEARCH_API", "https://your-music-api.com/search")
HITS_API = os.getenv("HITS_API", "https://your-music-api.com/hits")

# WebSocket
WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")
