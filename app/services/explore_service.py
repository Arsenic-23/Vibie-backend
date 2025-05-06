from datetime import datetime
from googleapiclient.discovery import build
import os

# Load your API key (or use os.environ.get if using env variables)
YOUTUBE_API_KEY = "AIzaSyB_NBj0yHTYLqZE6lNoVFj9iflDV-28pb0"  # Replace with your key
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def fetch_top_music(query="top music 2024", max_results=50):
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        videoCategoryId="10",  # Music category
        maxResults=min(max_results, 50),  # YouTube API max per page is 50
        order="viewCount"
    ).execute()

    results = []
    for index, item in enumerate(search_response.get("items", [])):
        snippet = item["snippet"]
        video_id = item["id"]["videoId"]
        results.append({
            "title": snippet["title"],
            "artist": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "video_id": video_id,
            "rank": index + 1
        })

    return results

def get_explore_data():
    return {
        "date": datetime.utcnow().isoformat(),
        "trending": fetch_top_music("trending music 2024", 50),
        "new_releases": fetch_top_music("latest music 2024", 50),
        "top_charts": fetch_top_music("top hits 2024", 50)
    }
