from app.db.repositories import UserRepository

async def authenticate_user(telegram_id: str, name: str):
    try:
        user_repo = UserRepository()
        user = await user_repo.get_user_by_telegram_id(telegram_id)  # await required if it's async

        if user and user.get("first_name") == name:
            return user
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None