# app/routes/register.py or inside auth.py if you prefer

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_db
from bson import ObjectId

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    username: str = ""
    photo_url: str = ""

@router.post("/register")
async def register_user(user: UserRegister):
    db = get_db()

    # Optional: check if a user already exists by username
    if user.username:
        existing = await db["users"].find_one({"username": user.username})
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

    user_data = {
        "name": user.name,
        "username": user.username,
        "photo_url": user.photo_url,
        "favorites": [],
        "history": []
    }

    result = await db["users"].insert_one(user_data)

    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "username": user.username,
        "photo_url": user.photo_url,
    }