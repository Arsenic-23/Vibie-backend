from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user import User
from app.models.song import Song
from uuid import uuid4

class Stream(BaseModel):
    chat_id: str  # Unique chat ID for the group stream
    owner_id: str  # Telegram user ID or internal user ID
    song_queue: List[Song] = []
    users: List[str] = []  # List of user IDs currently in the stream
    now_playing: Optional[Song] = None  # Current song being played
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_song_to_queue(self, song: Song):
        """Add a song to the queue."""
        self.song_queue.append(song)
        self.updated_at = datetime.utcnow()

    def remove_song_from_queue(self, song: Song):
        """Remove a song from the queue."""
        self.song_queue = [s for s in self.song_queue if s.id != song.id]
        self.updated_at = datetime.utcnow()

    def add_user(self, user_id: str):
        """Add a user to the stream."""
        if user_id not in self.users:
            self.users.append(user_id)
        self.updated_at = datetime.utcnow()

    def remove_user(self, user_id: str):
        """Remove a user from the stream."""
        self.users = [uid for uid in self.users if uid != user_id]
        self.updated_at = datetime.utcnow()

    def skip_to_next_song(self):
        """Skip to the next song in the queue."""
        if self.song_queue:
            self.now_playing = self.song_queue.pop(0)  # Update now playing song
        else:
            self.now_playing = None
        self.updated_at = datetime.utcnow()

    def clear_queue(self):
        """Clear the song queue."""
        self.song_queue = []
        self.updated_at = datetime.utcnow()