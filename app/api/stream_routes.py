
from fastapi import APIRouter, HTTPException
from app.services.stream_service import StreamService
from app.services.queue_service import QueueService
from app.models.song import Song

router = APIRouter()

stream_service = StreamService()
queue_service = QueueService()

@router.post("/stream/group/{chat_id}/play")
async def play_song(chat_id: str, query: str):
    """
    Add a song to the group stream. Start playing if nothing is playing.
    """
    try:
        stream = stream_service.get_or_create_stream_by_chat(chat_id)
        song = stream_service.search_song(query)

        if not stream.now_playing:
            stream_service.play_song_now(chat_id, song)
        else:
            queue_service.add_song_to_queue(stream.id, song)

        return {"message": f"Song '{song.title}' queued or playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream/group/{chat_id}/playforce")
async def force_play_song(chat_id: str, query: str):
    """
    Force play a song in the group stream, clearing the queue.
    """
    try:
        stream = stream_service.get_or_create_stream_by_chat(chat_id)
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


@router.get("/stream/group/{chat_id}/queue")
async def get_queue(chat_id: str):
    """
    Get queue for group stream.
    """
    try:
        return queue_service.get_queue_for_chat(chat_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Queue not found")