from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class Song(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration: int  # in seconds
    url: str


class User(BaseModel):
    telegram_id: int
    username: str
    photo_url: Optional[str] = None
    joined_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True


class Stream(BaseModel):
    stream_id: str
    creator: User
    song_queue: List[Song] = []
    current_song: Optional[Song] = None
    listeners: List[User] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_song_to_queue(self, song: Song) -> None:
        self.song_queue.append(song)
        self.updated_at = datetime.utcnow()

    def remove_song_from_queue(self, song: Song) -> None:
        try:
            self.song_queue.remove(song)
            self.updated_at = datetime.utcnow()
        except ValueError:
            pass

    def add_listener(self, user: User) -> None:
        if all(u.telegram_id != user.telegram_id for u in self.listeners):
            self.listeners.append(user)
            self.updated_at = datetime.utcnow()

    def remove_listener(self, user: User) -> None:
        self.listeners = [u for u in self.listeners if u.telegram_id != user.telegram_id]
        self.updated_at = datetime.utcnow()