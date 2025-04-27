

# app/models/song.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Song(BaseModel):
    id: str  # Unique ID, e.g., YouTube video ID
    title: str
    artist: Optional[str] = None
    thumbnail: Optional[str] = None
    source: str = "YouTube"
    audio_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True