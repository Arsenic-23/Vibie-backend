# app/db/models.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Song(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration: int  # duration in seconds
    url: str


class User(BaseModel):
    user_id: str
    username: str
    photo_url: Optional[str] = None
    joined_at: datetime


class Stream(BaseModel):
    stream_id: str
    creator: User
    song_queue: List[Song] = []
    current_song: Optional[Song] = None
    listeners: List[User] = []
    created_at: datetime
    updated_at: datetime

    def add_song_to_queue(self, song: Song) -> None:
        """Add a song to the stream's queue."""
        self.song_queue.append(song)
        self.updated_at = datetime.utcnow()

    def remove_song_from_queue(self, song: Song) -> None:
        """Remove a song from the stream's queue if it exists."""
        try:
            self.song_queue.remove(song)
            self.updated_at = datetime.utcnow()
        except ValueError:
            pass

    def add_listener(self, user: User) -> None:
        """Add a user to the listener list if not already present."""
        if user not in self.listeners:
            self.listeners.append(user)
            self.updated_at = datetime.utcnow()

    def remove_listener(self, user: User) -> None:
        """Remove a user from the listener list if present."""
        if user in self.listeners:
            self.listeners.remove(user)
            self.updated_at = datetime.utcnow()