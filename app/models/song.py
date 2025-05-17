# app/models/song.py

from pydantic import BaseModel, Field
from typing import Optional


class Song(BaseModel):
    id: str
    title: str
    artist: Optional[str] = "Unknown"
    thumbnail: Optional[str] = None
    audio_url: str
    source: str = Field(default="YouTube")

    def dict(self, *args, **kwargs):
        # Override to ensure Firestore-safe dict if needed
        return super().dict(*args, **kwargs)