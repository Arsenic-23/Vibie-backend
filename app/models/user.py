# app/models/user.py

from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    telegramId: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    photo_url: Optional[str]

class UserInDB(UserCreate):
    id: Optional[str] = Field(alias="_id")