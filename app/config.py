import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Config values from the environment
MONGO_URI = os.getenv("MONGO_URI", "your-default-mongo-uri")  # Replace with your actual Mongo URI
DB_NAME = os.getenv("DB_NAME", "vibie_db")
API_KEY = os.getenv("API_KEY", "AIzaSyDKZwdnrvfGJTiHdDGdemmjJ--jXnjwR1g")  # Replace with your actual API key
SEARCH_API = os.getenv("SEARCH_API", "AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")  # Replace with your actual API key
HITS_API = os.getenv("HITS_API", "AIzaSyB4k_EuVJ3JLFU-ywJWExJKflgcEKy1omQ")  # Replace with your actual API key
WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8001))
WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")
SECRET_KEY = os.getenv("SECRET_KEY", "83c2114f44b13d41e312ea6e3dbf6d4a7cde7af23bfb0f4f3d020947c7e5c5c")  # Replace with your actual secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# If you still want to keep the Settings instance (optional), you can instantiate here.
# settings = Settings()  # However, Settings is not defined in your code, so this would cause an error.