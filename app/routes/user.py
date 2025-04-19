from fastapi import APIRouter, HTTPException, Body
from app.db.mongodb import get_db
from app.schemas.user import UserUpdate
from typing import Optional, List

router = APIRouter()

# Utility function to fetch user by Telegram ID
async def get_user_by_id(user_id: int):
    db = get_db()
    try:
        user = await db["users"].find_one({"telegram_id": user_id})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Get user profile
@router.get("/profile/{user_id}")
async def get_profile(user_id: int):
    user = await get_user_by_id(user_id)
    return {
        "id": user.get("telegram_id"),
        "name": f'{user.get("first_name", "")} {user.get("last_name", "")}'.strip(),
        "username": user.get("username", ""),
        "photo_url": user.get("photo_url", "")
    }


# Get user favorites
@router.get("/favorites/{user_id}")
async def get_favorites(user_id: int):
    user = await get_user_by_id(user_id)
    return {
        "favorites": user.get("favorites", [])
    }


# Get user history
@router.get("/history/{user_id}")
async def get_history(user_id: int):
    user = await get_user_by_id(user_id)
    return {
        "history": user.get("history", [])
    }


# Update user profile
@router.put("/profile/{user_id}")
async def update_profile(user_id: int, payload: UserUpdate = Body(...)):
    db = get_db()
    update_data = {k: v for k, v in payload.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    result = await db["users"].update_one(
        {"telegram_id": user_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db["users"].find_one({"telegram_id": user_id})
    return {
        "id": updated_user.get("telegram_id"),
        "name": f'{updated_user.get("first_name", "")} {updated_user.get("last_name", "")}'.strip(),
        "username": updated_user.get("username", ""),
        "photo_url": updated_user.get("photo_url", "")
    }