import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.api import stream_routes, search_routes, user_routes
from app.routes.register import router as register_router
from app.websockets.stream_ws import stream_ws_endpoint
from app.db.mongodb import connect_to_mongo, close_mongo_connection

# Load environment variables from .env
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(stream_routes.router, prefix="/api/stream", tags=["Stream"])
app.include_router(search_routes.router, prefix="/api/search", tags=["Search"])
app.include_router(user_routes.router, prefix="/api/user", tags=["User"])
app.include_router(register_router, prefix="/api/user", tags=["Register"])

# WebSocket
app.websocket("/ws/stream/{stream_id}")(stream_ws_endpoint)

# Global Exception Handler
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error."},
        )

# Startup / Shutdown
@app.on_event("startup")
async def startup_db():
    try:
        await connect_to_mongo()
        logger.info("✅ Connected to MongoDB.")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")

@app.on_event("shutdown")
async def shutdown_db():
    try:
        await close_mongo_connection()
        logger.info("🔌 MongoDB connection closed.")
    except Exception as e:
        logger.warning(f"⚠️ Error closing MongoDB: {e}")