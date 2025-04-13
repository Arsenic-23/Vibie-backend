# app/models/stream.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.models.user import User
from app.models.song import Song

class Stream(BaseModel):
    stream_id: str
    creator: User
    current_song: Optional[Song] = None
    song_queue: List[Song] = []
    listeners: List[User] = []
    created_at: datetime
    updated_at: datetime

    def add_song_to_queue(self, song: Song):
        self.song_queue.append(song)

    def remove_song_from_queue(self, song: Song):
        self.song_queue = [s for s in self.song_queue if s.id != song.id]

    def add_listener(self, user: User):
        if all(u.id != user.id for u in self.listeners):
            self.listeners.append(user)

    def remove_listener(self, user: User):
        self.listeners = [u for u in self.listeners if u.id != user.id]