from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.song import Song


class Stream(BaseModel):
    stream_id: str  # e.g., groupId_userId (unique room link)
    chat_id: str
    now_playing: Optional[Song] = None
    song_queue: List[Song] = Field(default_factory=list)
    users: List[str] = Field(default_factory=list)
    active: bool = True

    def add_song_to_queue(self, song: Song):
        self.song_queue.append(song)

    def skip_to_next_song(self):
        if self.song_queue:
            self.now_playing = self.song_queue.pop(0)
        else:
            self.now_playing = None

    def clear_queue(self):
        self.song_queue = []