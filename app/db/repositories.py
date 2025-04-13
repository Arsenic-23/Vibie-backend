# app/db/repositories.py

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
