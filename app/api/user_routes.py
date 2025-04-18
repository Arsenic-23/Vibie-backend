from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.db.repositories import UserRepository
from app.database import get_db
from app.utils.jwt_token import generate_access_token
from app.schemas import UserCreate, UserResponse, LoginResponse
from app.services.auth_service import authenticate_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    user_repo = UserRepository(db)
    
    # Check if user already exists
    existing_user = user_repo.get_user_by_telegram_id(user.telegram_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Create a new user in the database
    new_user = user_repo.create_user(user)
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Login a user and generate an access token
    """
    user_repo = UserRepository(db)
    
    authenticated_user = await authenticate_user(user.telegram_id, user.name)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = generate_access_token(data={"sub": authenticated_user.telegram_id})

    return {
        "access_token": access_token,
        "user": authenticated_user
    }


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(db: Session = Depends(get_db), current_user: User = Depends(authenticate_user)):
    """
    Fetch the user's profile information using the access token
    """
    user_repo = UserRepository(db)
    user_data = user_repo.get_user_by_telegram_id(current_user.telegram_id)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return user_data


@router.put("/update", response_model=UserResponse)
async def update_user_profile(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(authenticate_user)):
    """
    Update user profile data
    """
    user_repo = UserRepository(db)

    existing_user = user_repo.get_user_by_telegram_id(current_user.telegram_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = user_repo.update_user(current_user.telegram_id, user)
    return updated_user