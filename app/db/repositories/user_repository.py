from google.cloud import firestore
from app.models.user import User
from app.models.song import Song

class UserRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("users")

    def get_user(self, user_id: str) -> User:
        doc = self.collection.document(user_id).get()
        if doc.exists:
            return User(**doc.to_dict())
        return User(user_id=user_id)

    def save_user(self, user: User):
        self.collection.document(user.user_id).set(user.dict())

    def add_song_to_history(self, user_id: str, song: Song):
        user = self.get_user(user_id)
        user.add_to_history(song)
        self.save_user(user)

    def add_song_to_favorites(self, user_id: str, song: Song):
        user = self.get_user(user_id)
        user.add_to_favorites(song)
        self.save_user(user)

    def remove_song_from_favorites(self, user_id: str, song_id: str):
        user = self.get_user(user_id)
        user.remove_from_favorites(song_id)
        self.save_user(user)

    def get_favorites(self, user_id: str):
        user = self.get_user(user_id)
        return user.favorites

    def get_history(self, user_id: str):
        user = self.get_user(user_id)
        return user.history