from pydantic import BaseModel


class UserCreate(BaseModel):
    telegram_id: str
    name: str = ""
    username: str = ""
    photo_url: str = ""


class UserResponse(BaseModel):
    telegram_id: str
    name: str
    username: str
    photo_url: str