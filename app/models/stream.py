from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.song import Song

class Stream(BaseModel):
    chat_id: str
    owner_id: Optional[str] = None
    song_queue: List[Song] = Field(default_factory=list)
    users: List[str] = Field(default_factory=list)
    now_playing: Optional[Song] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_song_to_queue(self, song: Song):
        self.song_queue.append(song)
        self.touch()

    def remove_song_from_queue(self, song: Song):
        self.song_queue = [s for s in self.song_queue if s.id != song.id]
        self.touch()

    def add_user(self, user_id: str):
        if user_id not in self.users:
            self.users.append(user_id)
            self.touch()

    def remove_user(self, user_id: str):
        self.users = [uid for uid in self.users if uid != user_id]
        self.touch()

    def skip_to_next_song(self):
        self.now_playing = self.song_queue.pop(0) if self.song_queue else None
        self.touch()

    def clear_queue(self):
        self.song_queue.clear()
        self.touch()

    def touch(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()