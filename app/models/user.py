from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    name: str
    username: Optional[str] = None
    profile_photo_url: Optional[str] = None