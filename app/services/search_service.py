# app/services/search_service.py

import httpx
import os

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class SearchService:
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    async def search_songs(self, query: str, max_results: int = 10):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL,
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": max_results,
                    "key": YOUTUBE_API_KEY
                }
            )
            data = response.json()
            results = []

            for item in data.get("items", []):
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                channel_title = item["snippet"]["channelTitle"]
                thumbnail = item["snippet"]["thumbnails"]["high"]["url"]

                results.append({
                    "video_id": video_id,
                    "title": title,
                    "artist": channel_title,
                    "thumbnail": thumbnail,
                    "source": "YouTube"
                })

            return results
