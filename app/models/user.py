from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    telegramId: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None

class UserInDB(UserCreate):
    id: Optional[str] = Field(alias="_id")