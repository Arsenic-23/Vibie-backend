from fastapi import APIRouter, HTTPException
from app.database import get_db
from bson import ObjectId

router = APIRouter()

# Helper function to fetch user by ID
async def get_user_by_id(user_id: str):
    db = get_db()
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    user = await get_user_by_id(user_id)
    return {
        "id": str(user["_id"]),
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