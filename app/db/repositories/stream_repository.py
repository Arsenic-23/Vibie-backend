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
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
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
        result = db.streams.update_one(
            {"chat_id": chat_id},
            {
                "$push": {"song_queue": song.dict()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

    @staticmethod
    def remove_song_from_stream_queue(chat_id: str, song_id: str) -> bool:
        """Removes a song from the stream's queue by song ID."""
        result = db.streams.update_one(
            {"chat_id": chat_id},
            {
                "$pull": {"song_queue": {"id": song_id}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

    @staticmethod
    def add_user_to_stream(chat_id: str, user: User) -> bool:
        """Adds a user to the stream."""
        result = db.streams.update_one(
            {"chat_id": chat_id},
            {
                "$addToSet": {"users": user.user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

    @staticmethod
    def remove_user_from_stream(chat_id: str, user_id: str) -> bool:
        """Removes a user from the stream."""
        result = db.streams.update_one(
            {"chat_id": chat_id},
            {
                "$pull": {"users": user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        return result.modified_count > 0

    @staticmethod
    def skip_to_next_song(chat_id: str) -> bool:
        """Skips to the next song in the stream's queue."""
        stream = StreamRepository.get_stream_by_chat_id(chat_id)
        if stream and stream.song_queue:
            next_song = stream.song_queue.pop(0)
            now_playing = next_song

            db.streams.update_one(
                {"chat_id": chat_id},
                {
                    "$set": {
                        "song_queue": [s.dict() for s in stream.song_queue],
                        "now_playing": now_playing.dict(),
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return True
        return False

    @staticmethod
    def clear_stream_queue(chat_id: str) -> bool:
        """Clears the stream's song queue."""
        result = db.streams.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "song_queue": [],
                    "now_playing": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0