# app/models/song.py

from pydantic import BaseModel
from typing import Optional

class Song(BaseModel):
    id: str  # Unique ID, e.g., YouTube video ID
    title: str
    artist: Optional[str] = None
    thumbnail: Optional[str] = None
    source: str = "YouTube"
    audio_url: Optional[str] = None  # Direct audio stream URL (from yt-dlp)