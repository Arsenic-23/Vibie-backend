import httpx
from googleapiclient.discovery import build
from app.db.repositories import StreamRepository
from app.db.repositories.user_repository import UserRepository
from app.models.stream import Stream
from app.models.song import Song

YOUTUBE_API_KEY = 'AIzaSyDVknYzHSy7pgksqaLeBhhELJvMif0GNgk'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

SEARCH_API_URL = "https://vibie-backend.onrender.com/api/search/search/"


class StreamService:
    def __init__(self, broadcast_message):
        self.stream_repo = StreamRepository()
        self.user_repo = UserRepository()
        self.broadcast_message = broadcast_message

    def get_or_create_stream_by_chat(self, chat_id: str) -> Stream:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if stream:
            return stream
        stream = Stream(chat_id=chat_id, now_playing=None)
        self.stream_repo.create_stream(stream)
        return stream

    async def search_song_async(self, query: str) -> Song:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(SEARCH_API_URL, params={"query": query})
            res.raise_for_status()
            data = res.json()

        if not data.get("results"):
            raise Exception("No search results found")

        top_result = data["results"][0]
        return Song(
            id=top_result["video_id"],
            title=top_result["title"],
            artist=top_result.get("artist", "Unknown"),
            thumbnail=top_result.get("thumbnail"),
            audio_url=self.get_audio_url(top_result["video_id"]),
            source="YouTube"
        )

    def get_audio_url(self, video_id: str) -> str:
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()

        if not response.get('items'):
            raise Exception("No video found")
        return f"https://www.youtube.com/watch?v={video_id}"

    def add_song_to_queue(self, chat_id: str, song: Song, user_id: str):
        stream = self.get_or_create_stream_by_chat(chat_id)
        if not stream.now_playing:
            stream.now_playing = song
        else:
            stream.add_song_to_queue(song)
        self.stream_repo.update_stream(stream)

        # Save to user's history
        self.user_repo.add_song_to_history(user_id, song)
        self._broadcast_stream_update(stream)

    def play_song_force(self, chat_id: str, song: Song, user_id: str):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        stream.clear_queue()
        self.stream_repo.update_stream(stream)

        # Save to user's history
        self.user_repo.add_song_to_history(user_id, song)
        self._broadcast_stream_update(stream)

    def skip_to_next_song_by_chat(self, chat_id: str):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.skip_to_next_song()
        self.stream_repo.update_stream(stream)
        self._broadcast_stream_update(stream)

    def end_stream(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if stream:
            self.stream_repo.delete_stream_by_chat_id(chat_id)
            self.broadcast_message(chat_id, {
                "type": "stream_end",
                "message": f"Stream {chat_id} has ended."
            })

    def get_stream_data_by_chat(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if not stream:
            raise Exception("Stream not found")
        return {
            "now_playing": stream.now_playing.dict() if stream.now_playing else None,
            "queue": [s.dict() for s in stream.song_queue],
            "active": stream.active,
        }

    def get_now_playing(self, chat_id: str) -> dict:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        return stream.now_playing.dict() if stream and stream.now_playing else {}

    def get_queue_length(self, chat_id: str) -> int:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        return len(stream.song_queue) if stream else 0

    def _broadcast_stream_update(self, stream: Stream):
        self.broadcast_message(stream.chat_id, {
            "type": "stream_update",
            "now_playing": stream.now_playing.dict() if stream.now_playing else None,
            "queue": [s.dict() for s in stream.song_queue],
            "users": stream.users,
        })

    # --- New User Favorites Methods ---

    def add_to_favorites(self, user_id: str, song: Song):
        self.user_repo.add_song_to_favorites(user_id, song)

    def remove_from_favorites(self, user_id: str, song_id: str):
        self.user_repo.remove_song_from_favorites(user_id, song_id)

    def get_user_favorites(self, user_id: str):
        return [s.dict() for s in self.user_repo.get_favorites(user_id)]

    def get_user_history(self, user_id: str):
        return [s.dict() for s in self.user_repo.get_history(user_id)]