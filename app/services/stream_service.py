import httpx
from googleapiclient.discovery import build
from app.db.repositories import StreamRepository
from app.models.stream import Stream
from app.models.song import Song
from typing import Optional

# Setup the YouTube Data API
YOUTUBE_API_KEY = 'AIzaSyB_NBj0yHTYLqZE6lNoVFj9iflDV-28pb0'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

SEARCH_API_URL = "https://vibie-backend.onrender.com/api/search/search/"  # Optional external API for additional metadata

class StreamService:
    def __init__(self, broadcast_message):
        self.stream_repo = StreamRepository()
        self.broadcast_message = broadcast_message

    def get_or_create_stream_by_chat(self, chat_id: str) -> Stream:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if stream:
            return stream
        stream = Stream(chat_id=chat_id, now_playing=None)
        self.stream_repo.create_stream(stream)
        return stream

    async def search_song_async(self, query: str) -> Song:
        # First, search using the external API for a list of videos
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(SEARCH_API_URL, params={"query": query})
            res.raise_for_status()
            data = res.json()

        if not data.get("results"):
            raise Exception("No search results found")

        top_result = data["results"][0]
        video_id = top_result["video_id"]
        title = top_result["title"]
        artist = top_result.get("artist", "Unknown")
        thumbnail = top_result.get("thumbnail")

        # Use YouTube Data API to get video details (e.g., audio URL)
        audio_url = self.get_audio_url(video_id)

        return Song(
            id=video_id,
            title=title,
            artist=artist,
            thumbnail=thumbnail,
            audio_url=audio_url,
            source="YouTube"
        )

    def get_audio_url(self, video_id: str) -> str:
        # Fetch audio URL using YouTube Data API
        request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
        response = request.execute()

        if 'items' not in response or len(response['items']) == 0:
            raise Exception("No video found with the provided video ID")

        video_info = response['items'][0]
        # The 'audio_url' field would ideally be derived from the video or processed as needed
        # You can extract this from the video stream details via YouTube API
        audio_url = f"https://www.youtube.com/watch?v={video_id}"

        return audio_url

    def add_song_to_queue(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        if not stream.now_playing:
            stream.now_playing = song
        else:
            stream.add_song_to_queue(song)
        self.stream_repo.update_stream(stream)
        self._broadcast_stream_update(stream)

    def play_song_force(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        stream.clear_queue()
        self.stream_repo.update_stream(stream)
        self._broadcast_stream_update(stream)

    def skip_to_next_song_by_chat(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if not stream:
            raise Exception("Stream not found")
        stream.skip_to_next_song()
        self.stream_repo.update_stream(stream)
        self._broadcast_stream_update(stream)

    def end_stream(self, chat_id: str):
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

    def _broadcast_stream_update(self, stream: Stream):
        self.broadcast_message(stream.chat_id, {
            "type": "stream_update",
            "now_playing": stream.now_playing.dict() if stream.now_playing else None,
            "queue": [s.dict() for s in stream.song_queue],
            "users": stream.users,
        })