# app/models/stream.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    telegram_id: int
    username: Optional[str]
    full_name: Optional[str]
    profile_pic: Optional[str] = None
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class Stream(BaseModel):
    group_id: int
    stream_id: str
    current_song: Optional[dict] = None
    queue: List[dict] = []
    vibers: List[User] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
