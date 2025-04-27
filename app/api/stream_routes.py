from fastapi import APIRouter, HTTPException
from app.services.stream_service import StreamService
import os

from app.services.broadcast import broadcast_message  # <- Import the real function, not env string!

router = APIRouter()

# Initialize StreamService with actual broadcast function
def broadcast_message(chat_id: str, data: dict):
    print(f"[Broadcast] chat_id={chat_id} data={data}")

stream_service = StreamService(broadcast_message)

@router.post("/stream/group/{chat_id}/play")
async def play_song(chat_id: str, query: str):
    try:
        song = await stream_service.search_song_async(query)
        if not song:
            raise HTTPException(status_code=404, detail="No song found")
        stream_service.add_song_to_queue(chat_id, song)
        return {"message": f"Song '{song.title}' queued or playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream/group/{chat_id}/playforce")
async def force_play_song(chat_id: str, query: str):
    try:
        song = await stream_service.search_song_async(query)
        if not song:
            raise HTTPException(status_code=404, detail="No song found")
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
        raise HTTPException(status_code=404, detail=str(e))