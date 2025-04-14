from app.db.repositories import UserRepository

async def authenticate_user(telegram_id: str, name: str):
    # Basic example, just checks if user exists
    user_repo = UserRepository()
    user = user_repo.get_user_by_telegram_id(telegram_id)
    if user and user.name == name:
        return user
    return None