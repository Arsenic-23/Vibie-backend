# app/models/song.py

from pydantic import BaseModel
from typing import Optional

class Song(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration: int  # duration in seconds
    url: str