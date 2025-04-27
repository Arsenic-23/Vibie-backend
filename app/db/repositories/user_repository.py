from typing import Optional
from app.db.models import User
from app.db.mongodb import db

class UserRepository:

    @staticmethod
    def add_user(user: User) -> User:
        """Adds a new user to the database."""
        db.users.insert_one(user.dict())
        return user

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Fetches a user by their user ID."""
        user_data = db.users.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def update_user(user_id: str, username: Optional[str] = None, profile_pic: Optional[str] = None) -> Optional[User]:
        """Updates the user's details."""
        update_data = {}
        if username:
            update_data["username"] = username
        if profile_pic:
            update_data["profile_pic"] = profile_pic

        if update_data:
            db.users.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )

        user_data = db.users.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Deletes a user from the database."""
        result = db.users.delete_one({"user_id": user_id})
        return result.deleted_count > 0