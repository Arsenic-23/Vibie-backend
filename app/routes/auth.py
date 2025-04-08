from fastapi import APIRouter, Request, HTTPException
from app.utils.telegram_auth import verify_telegram_auth
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/telegram")
async def telegram_login(request: Request):
    data = await request.json()
    init_data = data.get("initData")

    if not init_data:
        raise HTTPException(status_code=400, detail="initData missing")

    user_info = verify_telegram_auth(init_data)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Telegram login")

    db = get_db()
    user_id = str(user_info["id"])

    existing_user = await db.users.find_one({"_id": user_id})
    if not existing_user:
        new_user = {
            "_id": user_id,
            "first_name": user_info.get("first_name", ""),
            "last_name": user_info.get("last_name", ""),
            "username": user_info.get("username", ""),
            "photo_url": user_info.get("photo_url", ""),
            "created_at": datetime.utcnow(),
            "favorites": [],
            "history": []
        }
        await db.users.insert_one(new_user)

    return {
        "id": user_id,
        "name": f'{user_info.get("first_name", "")} {user_info.get("last_name", "")}'.strip(),
        "username": user_info.get("username", ""),
        "photo_url": user_info.get("photo_url", "")
    }