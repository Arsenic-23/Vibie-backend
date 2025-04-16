from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.user import User
from app.models.song import Song
from uuid import uuid4

class Stream(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    owner_id: str  # Telegram user ID or internal user ID
    song_queue: List[Song] = []
    users: List[str] = []  # List of user IDs currently in the stream
    current_song: Optional[Song] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_song_to_queue(self, song: Song):
        self.song_queue.append(song)
        self.updated_at = datetime.utcnow()

    def remove_song_from_queue(self, song: Song):
        self.song_queue = [s for s in self.song_queue if s.id != song.id]
        self.updated_at = datetime.utcnow()

    def add_user(self, user_id: str):
        if user_id not in self.users:
            self.users.append(user_id)
        self.updated_at = datetime.utcnow()

    def remove_user(self, user_id: str):
        self.users = [uid for uid in self.users if uid != user_id]
        self.updated_at = datetime.utcnow()