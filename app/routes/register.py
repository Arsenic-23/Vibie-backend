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

    # Generate a unique user ID (e.g., ObjectId)
    user_id = str(ObjectId())

    user_data = {
        "user_id": user_id,  # Add the user_id here
        "name": user.name,
        "username": user.username,
        "photo_url": user.photo_url,
        "favorites": [],
        "history": []
    }

    # Insert user data into the database with user_id as reference
    result = await db["users"].insert_one(user_data)

    return {
        "user_id": user_id,  # Return the user_id as part of the response
        "name": user.name,
        "username": user.username,
        "photo_url": user.photo_url,
    }