from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from bson import ObjectId

router = APIRouter()

# Input model
class UserRegister(BaseModel):
    name: str
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

# Response model
class UserRegisterResponse(BaseModel):
    user_id: str
    name: str
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

@router.post("/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegister):
    db = get_db()

    # Check if username is already taken
    if user.username:
        existing = await db["users"].find_one({"username": user.username})
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

    # Generate unique user ID
    user_id = str(ObjectId())

    # Build user data
    user_data = {
        "user_id": user_id,
        "name": user.name,
        "username": user.username,
        "photo_url": user.photo_url,
        "favorites": [],
        "history": []
    }

    # Save to DB
    await db["users"].insert_one(user_data)

    # Return structured response
    return UserRegisterResponse(
        user_id=user_id,
        name=user.name,
        username=user.username,
        photo_url=user.photo_url
    )