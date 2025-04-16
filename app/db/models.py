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

    def add_song_to_queue(self, song: Song):
        self.song_queue.append(song)

    def remove_song_from_queue(self, song: Song):
        if song in self.song_queue:
            self.song_queue.remove(song)

    def add_listener(self, user: User):
        if user not in self.listeners:
            self.listeners.append(user)

    def remove_listener(self, user: User):
        if user in self.listeners:
            self.listeners.remove(user)
