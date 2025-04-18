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
    telegram_id: int
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

    if not verify_telegram_auth(auth_data):
        raise HTTPException(status_code=401, detail="Invalid Telegram login payload")

    telegram_id = str(auth_data["id"])
    db = get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database not connected")

    users_collection = db["users"]
    name = f"{auth_data.get('first_name', '')} {auth_data.get('last_name', '')}".strip()

    existing_user = await users_collection.find_one({"telegram_id": telegram_id})

    if existing_user:
        await users_collection.update_one(
            {"telegram_id": telegram_id},
            {"$set": {
                "first_name": auth_data.get("first_name", ""),
                "last_name": auth_data.get("last_name", ""),
                "username": auth_data.get("username", ""),
                "photo_url": auth_data.get("photo_url", "")
            }}
        )
    else:
        user_data = {
            "telegram_id": telegram_id,
            "first_name": auth_data.get("first_name", ""),
            "last_name": auth_data.get("last_name", ""),
            "username": auth_data.get("username", ""),
            "photo_url": auth_data.get("photo_url", ""),
            "favorites": [],
            "history": []
        }
        await users_collection.insert_one(user_data)

    token_payload = {
        "sub": telegram_id,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS),
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

    profile = {
        "id": telegram_id,
        "name": name,
        "username": auth_data.get("username", ""),
        "photo_url": auth_data.get("photo_url", "")
    }

    return {
        "token": token,
        "profile": profile
    }