from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: int
    name: str
    username: str
    photo_url: str = ""