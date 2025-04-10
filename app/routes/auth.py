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

    # Verify Telegram authentication
    if not verify_telegram_auth(auth_data):
        raise HTTPException(status_code=401, detail="Invalid Telegram data")

    db = get_db()
    telegram_id = str(auth_data["id"])

    # Check if user exists
    user = await db["users"].find_one({"telegramId": telegram_id})

    if not user:
        # Insert new user
        user_data = {
            "telegramId": telegram_id,
            "first_name": auth_data["first_name"],
            "last_name": auth_data["last_name"],
            "username": auth_data["username"],
            "photo_url": auth_data["photo_url"],
            "favorites": [],
            "history": []
        }
        result = await db["users"].insert_one(user_data)
        user = user_data
        user["_id"] = str(result.inserted_id)

    # Generate JWT token
    token = jwt.encode(
        {"id": telegram_id, "exp": datetime.utcnow() + timedelta(days=7)},
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "token": token,
        "profile": {
            "name": f"{auth_data['first_name']} {auth_data['last_name']}".strip(),
            "username": auth_data["username"],
            "photo": auth_data["photo_url"],
            "id": telegram_id
        },
    }