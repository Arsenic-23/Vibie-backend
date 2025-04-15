# app/models/user.py

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str] = None
    profile_picture_url: Optional[str] = None