from fastapi import APIRouter, HTTPException, Query
from app.services.stream_service import StreamService
import os

broadcast_message = os.getenv("BROADCAST_MESSAGE", "Default broadcast message")
stream_service = StreamService(broadcast_message)

router = APIRouter()

# --- Stream Controls ---

@router.post("/stream/group/{chat_id}/play")
async def play_song(chat_id: str, query: str, user_id: str = Query(..., description="User ID adding the song")):
    try:
        song = await stream_service.search_song_async(query)
        stream_service.add_song_to_queue(chat_id, song, user_id)
        return {"message": f"Song '{song.title}' queued or playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stream/group/{chat_id}/playforce")
async def force_play_song(chat_id: str, query: str, user_id: str = Query(..., description="User ID force-playing the song")):
    try:
        song = await stream_service.search_song_async(query)
        stream_service.play_song_force(chat_id, song, user_id)
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

# --- User Favorites and History ---

@router.post("/user/{user_id}/favorites/add")
async def add_to_favorites(user_id: str, song_id: str = Query(...), title: str = Query(...), artist: str = Query("Unknown"), thumbnail: str = Query(None), audio_url: str = Query(...)):
    try:
        song = {
            "id": song_id,
            "title": title,
            "artist": artist,
            "thumbnail": thumbnail,
            "audio_url": audio_url,
            "source": "YouTube"
        }
        stream_service.add_to_favorites(user_id, song)
        return {"message": f"Song '{title}' added to favorites"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/user/{user_id}/favorites/remove")
async def remove_from_favorites(user_id: str, song_id: str = Query(...)):
    try:
        stream_service.remove_from_favorites(user_id, song_id)
        return {"message": f"Song removed from favorites"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}/favorites")
async def get_favorites(user_id: str):
    try:
        favorites = stream_service.get_user_favorites(user_id)
        return {"favorites": favorites}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/user/{user_id}/history")
async def get_history(user_id: str):
    try:
        history = stream_service.get_user_history(user_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))