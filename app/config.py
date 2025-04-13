import os
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "vibie_db")
API_KEY = os.getenv("AIzaSyDKZwdnrvfGJTiHdDGdemmjJ--jXnjwR1g")
SEARCH_API = os.getenv("AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")
HITS_API = os.getenv("AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8001))
WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")
SECRET_KEY = os.getenv("83c2114f44b13d41e312ea6e3dbf6d4a7cde7af23bfb0f4f3d020947c7e5c5c")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
settings = Settings()