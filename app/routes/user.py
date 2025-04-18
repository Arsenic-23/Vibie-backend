from fastapi import APIRouter, HTTPException, Body
from app.database import get_db
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class UserUpdate(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    username: Optional[str] = ""
    photo_url: Optional[str] = ""
    favorites: Optional[list] = []
    history: Optional[list] = []


async def get_user_by_id(user_id: str):
    db = get_db()
    try:
        user = await db["users"].find_one({"telegramId": user_id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    user = await get_user_by_id(user_id)
    return {
        "id": user.get("telegramId"),
        "name": f'{user.get("first_name", "")} {user.get("last_name", "")}'.strip(),
        "username": user.get("username", ""),
        "photo_url": user.get("photo_url", "")
    }


@router.get("/favorites/{user_id}")
async def get_favorites(user_id: str):
    user = await get_user_by_id(user_id)
    return {
        "favorites": user.get("favorites", [])
    }


@router.get("/history/{user_id}")
async def get_history(user_id: str):
    user = await get_user_by_id(user_id)
    return {
        "history": user.get("history", [])
    }


@router.put("/profile/{user_id}")
async def update_profile(user_id: str, payload: UserUpdate = Body(...)):
    db = get_db()

    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    result = await db["users"].update_one(
        {"telegramId": user_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db["users"].find_one({"telegramId": user_id})
    return {
        "id": updated_user.get("telegramId"),
        "name": f'{updated_user.get("first_name", "")} {updated_user.get("last_name", "")}'.strip(),
        "username": updated_user.get("username", ""),
        "photo_url": updated_user.get("photo_url", "")
    }