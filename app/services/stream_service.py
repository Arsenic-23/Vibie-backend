from app.db.repositories import StreamRepository, SongRepository
from app.models.stream import Stream
from app.models.song import Song
from typing import Optional

class StreamService:
    def __init__(self):
        self.stream_repo = StreamRepository()
        self.song_repo = SongRepository()

    def get_or_create_stream_by_chat(self, chat_id: str) -> Stream:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if stream:
            return stream

        # Create a new empty stream for the group
        stream = Stream(
            chat_id=chat_id,
            now_playing=None,
            song_queue=[],
            active=True
        )
        self.stream_repo.create_stream(stream)
        return stream

    def search_song(self, query: str) -> Song:
        # You can replace this with a real search logic
        song = self.song_repo.search_by_title(query)
        if not song:
            raise Exception("Song not found")
        return song

    def play_song_now(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        self.stream_repo.update_stream(stream)

    def play_song_force(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        stream.song_queue = []  # Clear queue
        self.stream_repo.update_stream(stream)

    def skip_to_next_song_by_chat(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if not stream:
            raise Exception("Stream not found")

        if not stream.song_queue:
            stream.now_playing = None
        else:
            stream.now_playing = stream.song_queue.pop(0)

        self.stream_repo.update_stream(stream)

    def end_stream(self, chat_id: str):
        self.stream_repo.delete_stream_by_chat_id(chat_id)

    def get_stream_data_by_chat(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if not stream:
            raise Exception("Stream not found")

        return {
            "now_playing": stream.now_playing.title if stream.now_playing else None,
            "queue_length": len(stream.song_queue),
            "active": stream.active
        }