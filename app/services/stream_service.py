# app/services/stream_service.py

from app.db.repositories import StreamRepository, UserRepository
from app.utils import generate_stream_id
from datetime import datetime


class StreamService:
    def __init__(self):
        self.stream_repo = StreamRepository()
        self.user_repo = UserRepository()

    async def create_or_get_stream(self, group_id: int):
        stream = await self.stream_repo.get_stream_by_group_id(group_id)
        if stream:
            return stream

        stream_id = generate_stream_id()
        new_stream = {
            "stream_id": stream_id,
            "group_id": group_id,
            "created_at": datetime.utcnow(),
            "queue": [],
            "current_song": None,
            "vibers": []
        }
        await self.stream_repo.create_stream(new_stream)
        return new_stream

    async def add_user_to_stream(self, stream_id: str, user_data: dict):
        await self.user_repo.upsert_user(user_data)
        await self.stream_repo.add_viber_to_stream(stream_id, user_data["user_id"])

    async def get_stream_by_id(self, stream_id: str):
        return await self.stream_repo.get_stream_by_stream_id(stream_id)

    async def get_stream_by_group(self, group_id: int):
        return await self.stream_repo.get_stream_by_group_id(group_id)

    async def get_vibers(self, stream_id: str):
        return await self.stream_repo.get_vibers_in_stream(stream_id)

    async def update_current_song(self, stream_id: str, song: dict):
        return await self.stream_repo.set_current_song(stream_id, song)
