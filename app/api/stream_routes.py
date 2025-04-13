# app/api/stream_routes.py

from fastapi import APIRouter, Depends, HTTPException
from app.services.stream_service import StreamService
from app.services.queue_service import QueueService
from app.models.stream import Stream
from app.models.song import Song

router = APIRouter()

stream_service = StreamService()
queue_service = QueueService()

@router.post("/create_stream")
async def create_stream(user_id: str, song_id: str):
    """
    Create a new stream and add the first song to the stream queue.
    """
    try:
        # Create the stream and add the song to the queue
        stream = stream_service.create_stream(user_id=user_id, song_id=song_id)
        return {"stream_id": stream.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add_to_queue")
async def add_to_queue(stream_id: str, song_id: str):
    """
    Add a song to the stream's queue.
    """
    try:
        song = Song(id=song_id)  # Assuming the Song model has an ID field
        queue_service.add_song_to_queue(stream_id, song)
        return {"message": "Song added to queue"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_stream_data")
async def get_stream_data(stream_id: str):
    """
    Get current data for the stream (e.g., current song, user count).
    """
    try:
        stream_data = stream_service.get_stream_data(stream_id)
        return stream_data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Stream not found")

@router.post("/next_song")
async def next_song(stream_id: str):
    """
    Skip to the next song in the queue.
    """
    try:
        stream_service.skip_to_next_song(stream_id)
        return {"message": "Next song is now playing"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_queue")
async def get_queue(stream_id: str):
    """
    Get the current song queue for the stream.
    """
    try:
        queue_data = queue_service.get_queue_for_stream(stream_id)
        return queue_data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Stream not found")

@router.post("/update_stream_state")
async def update_stream_state(stream_id: str, action: str):
    """
    Update the state of the stream (e.g., play, pause, next).
    """
    try:
        stream_service.update_stream_state(stream_id, action)
        return {"message": f"Stream state updated to {action}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
