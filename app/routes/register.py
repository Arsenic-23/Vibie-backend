from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.mongodb import get_db

router = APIRouter()

# Input model
class UserRegister(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

    class Config:
        schema_extra = {
            "example": {
                "telegram_id": 12345678,
                "name": "John Doe",
                "username": "johndoe",
                "photo_url": "https://example.com/photo.jpg"
            }
        }

# Response model
class UserRegisterResponse(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str] = ""
    photo_url: Optional[str] = ""

@router.post("/register", response_model=UserRegisterResponse, operation_id="register_user_unique")
async def register_user(user: UserRegister):
    try:
        db = get_db()
        if db is None:
            raise HTTPException(status_code=500, detail="Database connection not established.")

        users_collection = db["users"]

        # Check if user already exists
        existing = await users_collection.find_one({"telegram_id": user.telegram_id})
        if existing:
            raise HTTPException(status_code=400, detail="User already registered")

        # Check if username exists
        if user.username:
            existing_username = await users_collection.find_one({"username": user.username})
            if existing_username:
                raise HTTPException(status_code=400, detail="Username already exists")

        # Construct user data
        user_data = {
            "telegram_id": user.telegram_id,
            "name": user.name.strip(),
            "username": user.username,
            "photo_url": user.photo_url,
            "favorites": [],
            "history": []
        }

        # Insert user
        await users_collection.insert_one(user_data)

        return UserRegisterResponse(
            telegram_id=user.telegram_id,
            name=user.name,
            username=user.username,
            photo_url=user.photo_url
        )

    except Exception as e:
        print(f"Error in /register: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")