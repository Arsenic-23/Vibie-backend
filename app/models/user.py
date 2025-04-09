# app/models/user.py

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    telegramId: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    photo_url: Optional[str]