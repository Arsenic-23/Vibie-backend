# app/services/stream_service.py

from app.db.repositories import StreamRepository, SongRepository
from app.models.stream import Stream
from app.models.song import Song
from typing import List

class StreamService:
    def __init__(self):
        self.stream_repo = StreamRepository()
        self.song_repo = SongRepository()

    def create_stream(self, user_id: str, song_id: str) -> Stream:
        """
        Create a new stream, add the user, and add the first song to the stream's queue.
        """
        # Fetch the song
        song = self.song_repo.get_song_by_id(song_id)
        if not song:
            raise Exception("Song not found")
        
        # Create a new stream
        stream = Stream(owner_id=user_id, song_queue=[song], active=True)
        self.stream_repo.create_stream(stream)
        return stream

    def get_stream_data(self, stream_id: str):
        """
        Get current stream data including current song, and list of users in the stream.
        """
        stream = self.stream_repo.get_stream_by_id(stream_id)
        if not stream:
            raise Exception("Stream not found")
        
        # Fetch the current song
        current_song = stream.song_queue[0] if stream.song_queue else None
        
        return {
            "stream_id": stream.id,
            "current_song": current_song.title if current_song else None,
            "user_count": len(stream.users)
        }

    def skip_to_next_song(self, stream_id: str):
        """
        Skip to the next song in the queue.
        """
        stream = self.stream_repo.get_stream_by_id(stream_id)
        if not stream or not stream.song_queue:
            raise Exception("No songs in the queue")
        
        # Move to the next song in the queue
        stream.song_queue.pop(0)  # Remove the current song
        self.stream_repo.update_stream(stream)
        
        return stream

    def update_stream_state(self, stream_id: str, action: str):
        """
        Update the state of the stream (play, pause, etc.)
        """
        stream = self.stream_repo.get_stream_by_id(stream_id)
        if not stream:
            raise Exception("Stream not found")
        
        # Handle play/pause or other actions
        if action == "play":
            stream.active = True
        elif action == "pause":
            stream.active = False
        else:
            raise Exception("Invalid action")
        
        self.stream_repo.update_stream(stream)
        return stream