from datetime import datetime
from googleapiclient.discovery import build
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Set this in your environment variables
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_youtube_hits(query: str, max_results: int = 50):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        videoCategoryId="10"  # Music category
    )
    response = request.execute()

    songs = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        video_id = item["id"]["videoId"]
        songs.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_time": snippet["publishedAt"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
    return songs

def get_explore_data():
    trending = fetch_youtube_hits("trending music")
    new_releases = fetch_youtube_hits("new songs 2024")
    top_charts = fetch_youtube_hits("top hits global")

    return {
        "date": datetime.utcnow().isoformat(),
        "trending": trending,
        "new_releases": new_releases,
        "top_charts": top_charts
    }