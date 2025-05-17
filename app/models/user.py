from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.song import Song


class User(BaseModel):
    user_id: str
    favorites: List[Song] = Field(default_factory=list)
    history: List[Song] = Field(default_factory=list)
    total_songs_played: int = 0

    def add_to_history(self, song: Song):
        self.history.insert(0, song)
        self.total_songs_played += 1
        # Optional: Trim history length if needed
        self.history = self.history[:100]

    def add_to_favorites(self, song: Song):
        if not any(s.id == song.id for s in self.favorites):
            self.favorites.append(song)

    def remove_from_favorites(self, song_id: str):
        self.favorites = [s for s in self.favorites if s.id != song_id]