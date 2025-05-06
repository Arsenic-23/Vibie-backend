from datetime import datetime
from youtubesearchpython import VideosSearch

def fetch_youtube_top_hits(query: str, limit: int = 50):
    search = VideosSearch(query, limit=limit)
    results = search.result().get("result", [])
    songs = []

    for item in results:
        songs.append({
            "title": item.get("title"),
            "channel": item.get("channel", {}).get("name"),
            "duration": item.get("duration"),
            "thumbnail": item.get("thumbnails", [{}])[0].get("url"),
            "video_id": item.get("id"),
            "url": f"https://www.youtube.com/watch?v={item.get('id')}",
            "view_count": item.get("viewCount", {}).get("short"),
            "published_time": item.get("publishedTime"),
        })

    return songs


def get_explore_data():
    trending = fetch_youtube_top_hits("trending music")
    new_releases = fetch_youtube_top_hits("latest music 2024")
    top_charts = fetch_youtube_top_hits("top hits global")

    return {
        "date": datetime.utcnow().isoformat(),
        "trending": trending,
        "new_releases": new_releases,
        "top_charts": top_charts
    }