# app/api/search_routes.py

from fastapi import APIRouter, HTTPException
from app.services.search_service import SearchService
from app.models.song import Song
from typing import List

router = APIRouter()

search_service = SearchService()

@router.get("/search/")
async def search_songs(query: str):
    """
    Search for songs based on a query.
    """
    try:
        results = await search_service.search_songs(query)
        if results:
            return {"results": results}
        else:
            return {"message": "No songs found"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/song/{song_id}")
async def get_song_details(song_id: str):
    """
    Get detailed information for a song by ID.
    """
    try:
        song = search_service.get_song_details(song_id)
        if song:
            return {"song": song}
        else:
            raise HTTPException(status_code=404, detail="Song not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
