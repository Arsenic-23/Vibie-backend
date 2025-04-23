# app/routes/explore.py

from fastapi import APIRouter, Depends
from app.services.explore_service import get_explore_data
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/explore", tags=["Explore"])

@router.get("")
async def explore():
    data = get_explore_data()
    return JSONResponse(content=data)