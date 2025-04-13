from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

class Config:
    # MongoDB URI for the database (or you can use DATABASE_URL)
    MONGO_URI = os.getenv("MONGO_URI", "your-default-mongo-uri")
    
    # Database name
    DB_NAME = os.getenv("DB_NAME", "vibie_db")
    
    # API keys
    API_KEY = os.getenv("API_KEY", "your-api-key")
    SEARCH_API = os.getenv("SEARCH_API", "your-search-api")
    HITS_API = os.getenv("HITS_API", "your-hits-api")
    
    # WebSocket settings
    WEBSOCKET_PORT = int(os.getenv("WEBSOCKET_PORT", 8001))
    WS_BROADCAST_URL = os.getenv("WS_BROADCAST_URL", "ws://localhost:8000/ws/stream/")
    
    # Secret key for JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    
    # JWT Algorithm
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    
    # Access token expiration time in minutes
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Logging level
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")