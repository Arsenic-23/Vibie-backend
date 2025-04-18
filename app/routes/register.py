from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.mongodb import get_db
from bson import ObjectId

router = APIRouter()

# Input model
class UserRegister(BaseModel):
    telegram_id: str
    first_name: str = ""
    last_name: str = ""
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

# Response model
class UserRegisterResponse(BaseModel):
    id: str
    name: str
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

@router.post("/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegister):
    try:
        db = get_db()
        if db is None:
            raise HTTPException(status_code=500, detail="Database connection not established.")

        # Check if user already exists
        existing = await db["users"].find_one({"telegramId": user.telegram_id})
        if existing:
            raise HTTPException(status_code=400, detail="User already registered")

        # Username taken?
        if user.username:
            existing_username = await db["users"].find_one({"username": user.username})
            if existing_username:
                raise HTTPException(status_code=400, detail="Username already exists")

        # Construct user data
        user_data = {
            "telegramId": user.telegram_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "photo_url": user.photo_url,
            "favorites": [],
            "history": []
        }

        # Insert user
        await db["users"].insert_one(user_data)

        return UserRegisterResponse(
            id=user.telegram_id,
            name=f"{user.first_name} {user.last_name}".strip(),
            username=user.username,
            photo_url=user.photo_url
        )
    except Exception as e:
        print(f"Error in /register: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")