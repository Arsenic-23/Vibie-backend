# app/routes/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.verify_telegram_auth import verify_telegram_auth
from app.database import get_db
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()

BOT_TOKEN = os.getenv("BOT_TOKEN")
JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key")
JWT_EXPIRE_DAYS = 7


class AuthData(BaseModel):
    id: int
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    photo_url: str = ""
    hash: str


class TelegramLoginRequest(BaseModel):
    authData: AuthData


@router.post("/telegram")
async def telegram_login(payload: TelegramLoginRequest):
    auth_data = payload.authData.dict()
    
    # Step 1: Validate Telegram payload
    if not verify_telegram_auth(auth_data):
        raise HTTPException(status_code=401, detail="Invalid Telegram login payload")

    telegram_id = str(auth_data["id"])
    db = get_db()

    # Step 2: Upsert user in MongoDB
    user = await db["users"].find_one({"telegramId": telegram_id})
    name = f"{auth_data.get('first_name', '')} {auth_data.get('last_name', '')}".strip()

    if user:
        # Update existing profile info
        await db["users"].update_one(
            {"telegramId": telegram_id},
            {"$set": {
                "first_name": auth_data.get("first_name", ""),
                "last_name": auth_data.get("last_name", ""),
                "username": auth_data.get("username", ""),
                "photo_url": auth_data.get("photo_url", "")
            }}
        )
    else:
        # Insert new user
        user_data = {
            "telegramId": telegram_id,
            "first_name": auth_data.get("first_name", ""),
            "last_name": auth_data.get("last_name", ""),
            "username": auth_data.get("username", ""),
            "photo_url": auth_data.get("photo_url", ""),
            "favorites": [],
            "history": [],
        }
        await db["users"].insert_one(user_data)

    # Step 3: Generate JWT token
    token_payload = {
        "sub": telegram_id,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS),
    }

    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

    # Step 4: Build profile response
    profile = {
        "id": telegram_id,
        "name": name,
        "username": auth_data.get("username", ""),
        "photo": auth_data.get("photo_url", "")
    }

    return {
        "token": token,
        "profile": profile,
    }