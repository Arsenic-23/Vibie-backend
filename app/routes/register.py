from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from app.db.mongodb import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()


class RegisterRequest(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None


class RegisterResponse(BaseModel):
    telegram_id: int
    name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/register", response_model=RegisterResponse)
async def register_user(user: RegisterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        users_collection = db["users"]

        # Check for existing telegram_id
        if await users_collection.find_one({"telegram_id": user.telegram_id}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registered"
            )

        # Check for username conflict
        if user.username:
            if await users_collection.find_one({"username": user.username}):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )

        user_doc = user.dict()
        user_doc["favorites"] = []
        user_doc["history"] = []

        await users_collection.insert_one(user_doc)

        return RegisterResponse(**user_doc)

    except Exception as e:
        print("Registration error:", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")