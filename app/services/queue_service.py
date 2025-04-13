# app/services/queue_service.py

from app.db.repositories import StreamRepository


class QueueService:
    def __init__(self):
        self.stream_repo = StreamRepository()

    async def add_song_to_queue(self, stream_id: str, song: dict):
        return await self.stream_repo.push_song_to_queue(stream_id, song)

    async def get_queue(self, stream_id: str):
        stream = await self.stream_repo.get_stream_by_stream_id(stream_id)
        return stream.get("queue", []) if stream else []

    async def remove_song_from_queue(self, stream_id: str, song_id: str):
        return await self.stream_repo.remove_song_from_queue(stream_id, song_id)

    async def clear_queue(self, stream_id: str):
        return await self.stream_repo.update_queue(stream_id, [])

    async def get_next_song(self, stream_id: str):
        queue = await self.get_queue(stream_id)
        return queue[0] if queue else None
