from ytmusicapi import YTMusic
from datetime import datetime

ytmusic = YTMusic()

def fetch_youtube_music_chart(limit=50):
    charts = ytmusic.get_charts(country="US")  # You can change to "IN", "UK", etc.
    top_songs = charts.get("chart", [])[:limit]

    result = []
    for item in top_songs:
        result.append({
            "title": item["title"],
            "video_id": item["videoId"],
            "url": f"https://www.youtube.com/watch?v={item['videoId']}",
            "artist": ", ".join([a['name'] for a in item.get("artists", [])]),
            "thumbnail": item["thumbnails"][-1]["url"] if item.get("thumbnails") else None,
            "views": item.get("views"),
            "rank": item.get("rank"),
            "isAvailable": item.get("isAvailable")
        })

    return result

def get_explore_data():
    hits = fetch_youtube_music_chart(limit=50)

    # Simulate categories from the hits list
    return {
        "date": datetime.utcnow().isoformat(),
        "trending": hits[:15],
        "new_releases": hits[15:30],
        "top_charts": hits[30:50]
    }