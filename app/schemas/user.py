
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    telegram_id: int
    name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None


class UserResponse(BaseModel):
    telegram_id: int
    name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse