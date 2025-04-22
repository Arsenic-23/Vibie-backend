from app.db.repositories import StreamRepository

class QueueService:
    def __init__(self):
        self.stream_repo = StreamRepository()

    async def add_song_to_queue(self, chat_id: str, song: dict):
        """
        Add a song to the queue for a group stream
        """
        return await self.stream_repo.push_song_to_queue_by_chat(chat_id, song)

    async def get_queue(self, chat_id: str):
        """
        Get the current song queue for the group stream
        """
        stream = await self.stream_repo.get_stream_by_chat_id(chat_id)
        return stream.get("song_queue", []) if stream else []

    async def remove_song_from_queue(self, chat_id: str, song_id: str):
        """
        Remove a song from the queue
        """
        return await self.stream_repo.remove_song_from_queue_by_chat(chat_id, song_id)

    async def clear_queue(self, chat_id: str):
        """
        Clear the queue for a specific group stream
        """
        return await self.stream_repo.update_queue_by_chat(chat_id, [])

    async def get_next_song(self, chat_id: str):
        """
        Get the next song in the queue
        """
        queue = await self.get_queue(chat_id)
        return queue[0] if queue else None