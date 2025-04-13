from datetime import datetime
from typing import List, Optional
from app.db.models import Stream, User, Song
from app.db.mongodb import db

class StreamRepository:

    @staticmethod
    def create_stream(stream_id: str, creator: User) -> Stream:
        stream = Stream(
            stream_id=stream_id,
            creator=creator,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            listeners=[creator]
        )
        db.streams.insert_one(stream.dict())
        return stream

    @staticmethod
    def get_stream_by_id(stream_id: str) -> Optional[Stream]:
        stream_data = db.streams.find_one({"stream_id": stream_id})
        if stream_data:
            return Stream(**stream_data)
        return None

    @staticmethod
    def add_song_to_stream_queue(stream_id: str, song: Song):
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.add_song_to_queue(song)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue]}}
            )

    @staticmethod
    def remove_song_from_stream_queue(stream_id: str, song: Song):
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.remove_song_from_queue(song)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue]}}
            )

    @staticmethod
    def add_listener_to_stream(stream_id: str, user: User):
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.add_listener(user)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"listeners": [u.dict() for u in stream.listeners]}}
            )

    @staticmethod
    def remove_listener_from_stream(stream_id: str, user: User):
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.remove_listener(user)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"listeners": [u.dict() for u in stream.listeners]}}
            )

class SongRepository:

    @staticmethod
    def search_songs(query: str) -> List[Song]:
        songs_data = db.songs.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"artist": {"$regex": query, "$options": "i"}}
            ]
        }).limit(50)
        return [Song(**song) for song in songs_data]

    @staticmethod
    def get_song_by_id(song_id: str) -> Optional[Song]:
        song_data = db.songs.find_one({"_id": song_id})
        if song_data:
            return Song(**song_data)
        return None

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        user_data = db.users.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def create_user(user: User) -> User:
        db.users.insert_one(user.dict())
        return user

    @staticmethod
    def update_user(user_id: str, data: dict) -> Optional[User]:
        db.users.update_one({"user_id": user_id}, {"$set": data})
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def delete_user(user_id: str):
        db.users.delete_one({"user_id": user_id})