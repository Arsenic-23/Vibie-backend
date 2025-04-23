# app/routes/genres.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.services.genre_service import get_all_genres, get_genre_data

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get("")
async def genres():
    genres = get_all_genres()
    return JSONResponse(content={"genres": genres})

@router.get("/{genre_name}")
async def genre_detail(genre_name: str):
    genre_data = get_genre_data(genre_name)
    return JSONResponse(content=genre_data)