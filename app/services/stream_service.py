import requests
import yt_dlp
from app.db.repositories import StreamRepository
from app.models.stream import Stream
from app.models.song import Song
from typing import Optional

SEARCH_API_URL = "https://vibie-backend.onrender.com/api/search/search/"  

class StreamService:
    def __init__(self, broadcast_message):
        self.stream_repo = StreamRepository()
        self.broadcast_message = broadcast_message

    def get_or_create_stream_by_chat(self, chat_id: str) -> Stream:
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if stream:
            return stream

        stream = Stream(chat_id=chat_id, now_playing=None, song_queue=[], active=True)
        self.stream_repo.create_stream(stream)
        return stream

    def search_song(self, query: str) -> Song:
        res = requests.get(SEARCH_API_URL, params={"query": query})
        if res.status_code != 200 or not res.json().get("results"):
            raise Exception("No search results found")

        top_result = res.json()["results"][0]
        video_id = top_result["video_id"]
        title = top_result["title"]
        artist = top_result.get("artist", "Unknown")
        thumbnail = top_result.get("thumbnail")

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
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'extract_flat': False,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            for f in info.get("formats", []):
                if f.get("acodec") != "none" and f.get("vcodec") == "none":
                    return f["url"]

        raise Exception("No audio stream found")

    def play_song_now(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        self.stream_repo.update_stream(stream)

        self.broadcast_message(chat_id, {
            "type": "stream_update",
            "now_playing": song.dict(),
            "queue": [s.dict() for s in stream.song_queue],
            "users": stream.users,
        })

    def play_song_force(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        stream.now_playing = song
        stream.song_queue = []
        self.stream_repo.update_stream(stream)

        self.broadcast_message(chat_id, {
            "type": "stream_update",
            "now_playing": song.dict(),
            "queue": [],
            "users": stream.users,
        })

    def skip_to_next_song_by_chat(self, chat_id: str):
        stream = self.stream_repo.get_stream_by_chat_id(chat_id)
        if not stream:
            raise Exception("Stream not found")

        if stream.song_queue:
            stream.now_playing = stream.song_queue.pop(0)
        else:
            stream.now_playing = None

        self.stream_repo.update_stream(stream)

        self.broadcast_message(chat_id, {
            "type": "stream_update",
            "now_playing": stream.now_playing.dict() if stream.now_playing else None,
            "queue": [s.dict() for s in stream.song_queue],
            "users": stream.users,
        })

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

    def add_song_to_queue(self, chat_id: str, song: Song):
        stream = self.get_or_create_stream_by_chat(chat_id)
        if not stream.now_playing:
            stream.now_playing = song
        else:
            stream.song_queue.append(song)
        self.stream_repo.update_stream(stream)

        self.broadcast_message(chat_id, {
            "type": "stream_update",
            "now_playing": stream.now_playing.dict() if stream.now_playing else None,
            "queue": [s.dict() for s in stream.song_queue],
            "users": stream.users,
        })