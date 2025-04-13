# app/models/song.py

from pydantic import BaseModel
from typing import Optional


class Song(BaseModel):
    video_id: str
    title: str
    artist: Optional[str] = None
    duration: int  # duration in seconds
    thumbnail: Optional[str] = None
    audio_url: Optional[str] = None  # Link to high-quality audio
