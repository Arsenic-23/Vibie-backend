from fastapi import APIRouter, HTTPException
from app.services.stream_service import StreamService
import os

broadcast_message = os.getenv("BROADCAST_MESSAGE", "Default broadcast message")

stream_service = StreamService(broadcast_message)

router = APIRouter()

@router.post("/stream/group/{chat_id}/play")
async def play_song(chat_id: str, query: str):
    try:
        song = await stream_service.search_song_async(query)
        stream_service.add_song_to_queue(chat_id, song)
        return {"message": f"Song '{song.title}' queued or playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream/group/{chat_id}/playforce")
async def force_play_song(chat_id: str, query: str):
    try:
        song = await stream_service.search_song_async(query)
        stream_service.play_song_force(chat_id, song)
        return {"message": f"Song '{song.title}' force-played"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream/group/{chat_id}/skip")
async def skip_song(chat_id: str):
    try:
        stream_service.skip_to_next_song_by_chat(chat_id)
        return {"message": "Skipped to next song"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream/group/{chat_id}/end")
async def end_stream(chat_id: str):
    try:
        stream_service.end_stream(chat_id)
        return {"message": "Stream ended"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stream/group/{chat_id}")
async def get_stream_data(chat_id: str):
    try:
        return stream_service.get_stream_data_by_chat(chat_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Stream not found")