import random
import string
from app.db.mongodb import db  # Add this line

def generate_stream_id(length=8):
    """Generate a unique stream ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_deep_link(stream_id: str) -> str:
    """Generate the deep link for a given stream"""
    return f"https://t.me/vibiebot?start=stream_{stream_id}"

def sanitize_song_metadata(song: dict) -> dict:
    """Sanitize or normalize song metadata"""
    return {
        "id": song.get("id"),
        "title": song.get("title"),
        "artist": song.get("artist", "Unknown Artist"),
        "duration": song.get("duration", 0),
        "thumbnail": song.get("thumbnail"),
        "url": song.get("url")  # High quality audio link
    }

def get_db():
    """Expose the shared database instance"""
    return db