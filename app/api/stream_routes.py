from fastapi import APIRouter, HTTPException
from app.services.stream_service import StreamService
from app.models.song import Song
import os

# Retrieve broadcast_message from an environment variable or use a default value
broadcast_message = os.getenv("BROADCAST_MESSAGE", "Default broadcast message")

# Instantiate StreamService with the required broadcast_message argument
stream_service = StreamService(broadcast_message)

router = APIRouter()

@router.post("/stream/group/{chat_id}/play")
async def play_song(chat_id: str, query: str):
    """
    Add a song to the group stream. Start playing if nothing is playing.
    """
    try:
        song = stream_service.search_song(query)
        stream_service.add_song_to_queue(chat_id, song)

        return {"message": f"Song '{song.title}' queued or playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream/group/{chat_id}/playforce")
async def force_play_song(chat_id: str, query: str):
    """
    Force play a song in the group stream, clearing the queue.
    """
    try:
        song = stream_service.search_song(query)
        stream_service.play_song_force(chat_id, song)
        return {"message": f"Song '{song.title}' force-played"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream/group/{chat_id}/skip")
async def skip_song(chat_id: str):
    """
    Skip to the next song in the queue.
    """
    try:
        stream_service.skip_to_next_song_by_chat(chat_id)
        return {"message": "Skipped to next song"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream/group/{chat_id}/end")
async def end_stream(chat_id: str):
    """
    End the current group stream.
    """
    try:
        stream_service.end_stream(chat_id)
        return {"message": "Stream ended"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stream/group/{chat_id}")
async def get_stream_data(chat_id: str):
    """
    Get stream data by chat_id.
    """
    try:
        return stream_service.get_stream_data_by_chat(chat_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Stream not found")