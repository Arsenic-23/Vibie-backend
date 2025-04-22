from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.database import get_db
from uuid import uuid4
from datetime import datetime

router = APIRouter()

# In-memory WebSocket connection mapping
active_connections: dict[str, list[WebSocket]] = {}

# Broadcast utility
async def broadcast(stream_id: str, message: str, sender: WebSocket = None):
    for conn in active_connections.get(stream_id, []):
        if conn != sender:
            try:
                await conn.send_text(message)
            except:
                active_connections[stream_id].remove(conn)

@router.post("/create")
async def create_stream(data: dict):
    user_id = data.get("user_id")
    song = data.get("song")
    group_id = data.get("group_id")  # Optional for group-based streams

    if not user_id or not song:
        raise HTTPException(status_code=400, detail="Missing user_id or song")

    db = get_db()

    # Prevent duplicate stream creation for a group
    if group_id:
        existing = await db.streams.find_one({"group_id": group_id})
        if existing:
            return {
                "stream_id": existing["_id"],
                "join_url": f"https://t.me/Vibie_bot?start=stream_{existing['_id']}",
                "message": "Stream already exists for this group"
            }

    stream_id = str(uuid4())[:8]

    stream = {
        "_id": stream_id,
        "creator_id": user_id,
        "song": song,
        "users": [user_id],
        "status": "playing",
        "created_at": datetime.utcnow().isoformat(),
        "start_time": datetime.utcnow().isoformat(),
    }

    if group_id:
        stream["group_id"] = group_id

    await db.streams.insert_one(stream)

    return {
        "stream_id": stream_id,
        "join_url": f"https://t.me/Vibie_bot?start=stream_{stream_id}",
        "message": "New stream created"
    }

@router.get("/{stream_id}")
async def get_stream(stream_id: str):
    db = get_db()
    stream = await db.streams.find_one({"_id": stream_id})
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    return {
        "song": stream["song"],
        "status": stream["status"],
        "users": stream["users"],
        "creator": stream["creator_id"],
        "start_time": stream.get("start_time"),
        "stream_url": f"https://t.me/Vibie_bot?start=stream_{stream_id}",
        "host": {
            "name": stream["creator_id"]
        }
    }

@router.post("/{stream_id}/join")
async def join_stream(stream_id: str, data: dict):
    user_id = data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    db = get_db()
    stream = await db.streams.find_one({"_id": stream_id})
    if not stream:
        raise HTTPException(status_code=404, detail="Stream not found")

    # Ensure user exists in the system (Optional)
    user = await db.users.find_one({"telegram_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id not in stream["users"]:
        stream["users"].append(user_id)
        await db.streams.update_one(
            {"_id": stream_id},
            {"$set": {"users": stream["users"]}}
        )

    return {
        "message": "Joined stream",
        "song": stream["song"],
        "stream_url": f"https://t.me/Vibie_bot?start=stream_{stream_id}"
    }

@router.get("/user/{user_id}")
async def get_user_streams(user_id: str):
    db = get_db()
    streams = await db.streams.find({"creator_id": user_id}).to_list(length=100)

    return {
        "streams": [
            {
                "stream_id": stream["_id"],
                "title": stream.get("song", "Untitled")
            } for stream in streams
        ]
    }

@router.websocket("/ws/{stream_id}")
async def stream_websocket(websocket: WebSocket, stream_id: str):
    await websocket.accept()

    if stream_id not in active_connections:
        active_connections[stream_id] = []
    active_connections[stream_id].append(websocket)

    await broadcast(stream_id, f"A user has joined the stream.", sender=websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await broadcast(stream_id, data, sender=websocket)
    except WebSocketDisconnect:
        active_connections[stream_id].remove(websocket)
        if not active_connections[stream_id]:
            del active_connections[stream_id]
        else:
            await broadcast(stream_id, f"A user has left the stream.")