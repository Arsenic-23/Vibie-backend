from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Song model with title, artist, album, duration, and URL
class Song(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration: int  # duration in seconds
    url: str


# User model with telegram_id (integer), username, photo_url, and joined_at timestamp
class User(BaseModel):
    telegram_id: int  # Change telegram_id to integer
    username: str
    photo_url: Optional[str] = None
    joined_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# Stream model with methods to add/remove songs and listeners, with timestamps
class Stream(BaseModel):
    stream_id: str
    creator: User
    song_queue: List[Song] = []
    current_song: Optional[Song] = None
    listeners: List[User] = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    # Method to add a song to the queue
    def add_song_to_queue(self, song: Song) -> None:
        self.song_queue.append(song)
        self.updated_at = datetime.utcnow()

    # Method to remove a song from the queue
    def remove_song_from_queue(self, song: Song) -> None:
        try:
            self.song_queue.remove(song)
            self.updated_at = datetime.utcnow()
        except ValueError:
            pass

    # Method to add a listener to the stream
    def add_listener(self, user: User) -> None:
        if user not in self.listeners:
            self.listeners.append(user)
            self.updated_at = datetime.utcnow()

    # Method to remove a listener from the stream
    def remove_listener(self, user: User) -> None:
        if user in self.listeners:
            self.listeners.remove(user)
            self.updated_at = datetime.utcnow()