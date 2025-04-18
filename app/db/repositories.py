from datetime import datetime
from typing import List, Optional
from app.db.models import Stream, User, Song
from app.db.mongodb import db

class StreamRepository:
    
    @staticmethod
    def create_stream(stream_id: str, creator: User) -> Stream:
        """Creates a new stream."""
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
        """Fetches a stream by its ID."""
        stream_data = db.streams.find_one({"stream_id": stream_id})
        if stream_data:
            return Stream(**stream_data)
        return None

    @staticmethod
    def add_song_to_stream_queue(stream_id: str, song: Song) -> bool:
        """Adds a song to the stream's queue."""
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.add_song_to_queue(song)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue]}}
            )
            return True
        return False

    @staticmethod
    def remove_song_from_stream_queue(stream_id: str, song: Song) -> bool:
        """Removes a song from the stream's queue."""
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.remove_song_from_queue(song)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue]}}
            )
            return True
        return False

    @staticmethod
    def add_listener_to_stream(stream_id: str, user: User) -> bool:
        """Adds a listener to the stream."""
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.add_listener(user)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"listeners": [u.dict() for u in stream.listeners]}}
            )
            return True
        return False

    @staticmethod
    def remove_listener_from_stream(stream_id: str, user: User) -> bool:
        """Removes a listener from the stream."""
        stream = StreamRepository.get_stream_by_id(stream_id)
        if stream:
            stream.remove_listener(user)
            db.streams.update_one(
                {"stream_id": stream_id},
                {"$set": {"listeners": [u.dict() for u in stream.listeners]}}
            )
            return True
        return False

class SongRepository:

    @staticmethod
    def search_songs(query: str) -> List[Song]:
        """Searches for songs by title or artist."""
        songs_data = db.songs.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"artist": {"$regex": query, "$options": "i"}}
            ]
        }).limit(50)
        return [Song(**song) for song in songs_data]

    @staticmethod
    def get_song_by_id(song_id: str) -> Optional[Song]:
        """Fetches a song by its ID."""
        song_data = db.songs.find_one({"_id": song_id})
        if song_data:
            return Song(**song_data)
        return None

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Fetches a user by their ID."""
        user_data = db.users.find_one({"user_id": user_id})
        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def create_user(user: User) -> User:
        """Creates a new user."""
        db.users.insert_one(user.dict())
        return user

    @staticmethod
    def update_user(user_id: str, data: dict) -> Optional[User]:
        """Updates user information."""
        db.users.update_one({"user_id": user_id}, {"$set": data})
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Deletes a user by their ID."""
        result = db.users.delete_one({"user_id": user_id})
        return result.deleted_count > 0