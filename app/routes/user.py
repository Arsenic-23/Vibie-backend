from fastapi import APIRouter, Request, HTTPException
from app.database import get_db

router = APIRouter()

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    db = get_db()
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user["_id"],
        "name": f'{user.get("first_name", "")} {user.get("last_name", "")}'.strip(),
        "username": user.get("username", ""),
        "photo_url": user.get("photo_url", "")
    }

@router.get("/favorites/{user_id}")
async def get_favorites(user_id: str):
    db = get_db()
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get("favorites", [])

@router.get("/history/{user_id}")
async def get_history(user_id: str):
    db = get_db()
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.get("history", [])