# app/repositories/song_repository.py

from typing import List, Optional
from app.db.models import Song
from app.db.mongodb import db

class SongRepository:

    @staticmethod
    def add_song(song: Song) -> Song:
        """Adds a new song to the database."""
        db.songs.insert_one(song.dict())
        return song

    @staticmethod
    def get_song_by_id(song_id: str) -> Optional[Song]:
        """Fetches a song by its ID."""
        song_data = db.songs.find_one({"id": song_id})
        if song_data:
            return Song(**song_data)
        return None

    @staticmethod
    def search_songs(query: str, limit: int = 10) -> List[Song]:
        """Searches for songs based on a query."""
        results = db.songs.find(
            {"title": {"$regex": query, "$options": "i"}}
        ).limit(limit)
        return [Song(**song) for song in results]

    @staticmethod
    def get_top_songs(limit: int = 10) -> List[Song]:
        """Fetches the top songs (sorted by popularity or any metric)."""
        results = db.songs.find().sort("play_count", -1).limit(limit)
        return [Song(**song) for song in results]

    @staticmethod
    def delete_song(song_id: str) -> bool:
        """Deletes a song by ID."""
        result = db.songs.delete_one({"id": song_id})
        return result.deleted_count > 0