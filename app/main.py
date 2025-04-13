from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stream_routes, search_routes, user_routes
from app.websockets.stream_ws import stream_ws_endpoint
from app.db.mongodb import connect_to_mongo, close_mongo_connection

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(stream_routes.router, prefix="/api/stream", tags=["Stream"])
app.include_router(search_routes.router, prefix="/api/search", tags=["Search"])
app.include_router(user_routes.router, prefix="/api/user", tags=["User"])

# WebSocket endpoint for playback sync
app.websocket("/ws/stream/{stream_id}")(stream_ws_endpoint)

# MongoDB
@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()