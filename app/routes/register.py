import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db.mongodb import get_db

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

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

@router.post("/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegister):
    try:
        logger.info(f"Received registration for Telegram ID: {user.telegram_id}")
        db = get_db()
        if db is None:
            logger.error("Database connection not established.")
            raise HTTPException(status_code=500, detail="Database connection not established.")

        users_collection = db["users"]

        # Check if user already exists
        existing = await users_collection.find_one({"telegram_id": user.telegram_id})
        if existing:
            logger.warning(f"User with telegram_id {user.telegram_id} already exists.")
            raise HTTPException(status_code=400, detail="User already registered")

        # Check if username exists
        if user.username:
            existing_username = await users_collection.find_one({"username": user.username})
            if existing_username:
                logger.warning(f"Username '{user.username}' already taken.")
                raise HTTPException(status_code=400, detail="Username already exists")

        user_data = {
            "telegram_id": user.telegram_id,
            "name": user.name.strip(),
            "username": user.username,
            "photo_url": user.photo_url,
            "favorites": [],
            "history": []
        }

        await users_collection.insert_one(user_data)

        logger.info(f"User {user.telegram_id} registered successfully.")
        return UserRegisterResponse(
            telegram_id=user.telegram_id,
            name=user.name,
            username=user.username,
            photo_url=user.photo_url
        )

    except Exception as e:
        logger.error(f"Error in /register: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")