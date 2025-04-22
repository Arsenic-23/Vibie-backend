from datetime import datetime
from typing import List, Optional
from app.db.models import Stream, User, Song
from app.db.mongodb import db

class StreamRepository:
    
    @staticmethod
    def create_stream(chat_id: str, owner: User) -> Stream:
        """Creates a new stream."""
        stream = Stream(
            chat_id=chat_id,
            owner_id=owner.user_id,
            song_queue=[],
            users=[owner.user_id],
            now_playing=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.streams.insert_one(stream.dict())
        return stream

    @staticmethod
    def get_stream_by_chat_id(chat_id: str) -> Optional[Stream]:
        """Fetches a stream by its chat ID."""
        stream_data = db.streams.find_one({"chat_id": chat_id})
        if stream_data:
            return Stream(**stream_data)
        return None

    @staticmethod
    def add_song_to_stream_queue(chat_id: str, song: Song) -> bool:
        """Adds a song to the stream's queue."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream:
            stream.add_song_to_queue(song)
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue], "updated_at": datetime.utcnow()}}
            )
            return True
        return False

    @staticmethod
    def remove_song_from_stream_queue(chat_id: str, song: Song) -> bool:
        """Removes a song from the stream's queue."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream:
            stream.remove_song_from_queue(song)
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue], "updated_at": datetime.utcnow()}}
            )
            return True
        return False

    @staticmethod
    def add_user_to_stream(chat_id: str, user: User) -> bool:
        """Adds a user to the stream."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream:
            stream.add_user(user.user_id)
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"users": stream.users, "updated_at": datetime.utcnow()}}
            )
            return True
        return False

    @staticmethod
    def remove_user_from_stream(chat_id: str, user: User) -> bool:
        """Removes a user from the stream."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream:
            stream.remove_user(user.user_id)
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"users": stream.users, "updated_at": datetime.utcnow()}}
            )
            return True
        return False

    @staticmethod
    def skip_to_next_song(chat_id: str) -> bool:
        """Skips to the next song in the stream's queue."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream and stream.song_queue:
            stream.skip_to_next_song()
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"song_queue": [s.dict() for s in stream.song_queue], "now_playing": stream.now_playing.dict() if stream.now_playing else None, "updated_at": datetime.utcnow()}}
            )
            return True
        return False

    @staticmethod
    def clear_stream_queue(chat_id: str) -> bool:
        """Clears the stream's song queue."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream:
            stream.clear_queue()
            db.streams.update_one(
                {"chat_id": chat_id},
                {"$set": {"song_queue": [], "updated_at": datetime.utcnow()}}
            )
            return True
        return False