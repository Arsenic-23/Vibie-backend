from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: str = Field(..., alias="telegramId")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        allow_population_by_field_name = True  # Allows using 'telegram_id' or 'telegramId'

class UserInDB(UserCreate):
    id: Optional[str] = Field(default=None, alias="_id")