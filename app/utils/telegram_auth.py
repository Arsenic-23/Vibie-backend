# telegram_auth.py
import hashlib
import hmac
import os
from fastapi import APIRouter, HTTPException
from app.database import get_db
from jose import jwt
from datetime import timedelta, datetime

router = APIRouter()
BOT_TOKEN = os.getenv("BOT_TOKEN")
JWT_SECRET = os.getenv("JWT_SECRET")

@router.post("/telegram")
async def telegram_login(authData: dict):
    hash_ = authData.pop("hash", None)
    data_check_string = "\n".join(
        [f"{k}={authData[k]}" for k in sorted(authData)]
    )
    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != hash_:
        raise HTTPException(status_code=401, detail="Invalid Telegram data")

    db = get_db()
    existing = await db.users.find_one({"telegramId": str(authData["id"])})
    if not existing:
        await db.users.insert_one({
            "telegramId": str(authData["id"]),
            "first_name": authData.get("first_name"),
            "last_name": authData.get("last_name"),
            "username": authData.get("username"),
            "photo_url": authData.get("photo_url"),
        })

    token = jwt.encode(
        {"id": authData["id"], "exp": datetime.utcnow() + timedelta(days=7)},
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "token": token,
        "profile": {
            "name": f"{authData.get('first_name', '')} {authData.get('last_name', '')}".strip(),
            "username": authData.get("username"),
            "photo": authData.get("photo_url"),
        }
    }