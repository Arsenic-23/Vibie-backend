from fastapi import APIRouter, HTTPException
from app.database import get_db
from uuid import uuid4
from datetime import datetime

router = APIRouter()

@router.post("/create")
async def create_stream(data: dict):
    user_id = data.get("user_id")
    song = data.get("song")

    if not user_id or not song:
        raise HTTPException(status_code=400, detail="Missing user_id or song")

    db = get_db()
    stream_id = str(uuid4())[:8]

    stream = {
        "_id": stream_id,
        "creator_id": user_id,
        "song": song,
        "users": [user_id],
        "status": "playing",
        "created_at": datetime.utcnow(),
        "start_time": datetime.utcnow()
    }

    await db.streams.insert_one(stream)

    return {
        "stream_id": stream_id,
        "join_url": f"https://t.me/YOUR_BOT_USERNAME?start=stream_{stream_id}"
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
        "start_time": stream.get("start_time")
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

    if user_id not in stream["users"]:
        stream["users"].append(user_id)
        await db.streams.update_one(
            {"_id": stream_id},
            {"$set": {"users": stream["users"]}}
        )

    return {"message": "Joined stream", "song": stream["song"]}