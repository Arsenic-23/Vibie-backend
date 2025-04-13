# app/websockets/stream_ws.py

import json
from fastapi import WebSocket, WebSocketDisconnect
from app.services.stream_service import StreamService

class StreamWebSocket:
    def __init__(self):
        self.stream_service = StreamService()
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, stream_id: str):
        await websocket.accept()

        if stream_id not in self.active_connections:
            self.active_connections[stream_id] = []
        
        self.active_connections[stream_id].append(websocket)

        # Send initial stream data (e.g., current song, user count)
        stream_data = self.stream_service.get_stream_data(stream_id)
        await websocket.send_json(stream_data)

    async def disconnect(self, websocket: WebSocket, stream_id: str):
        self.active_connections[stream_id].remove(websocket)

        if len(self.active_connections[stream_id]) == 0:
            del self.active_connections[stream_id]

    async def broadcast_stream_update(self, stream_id: str, data: dict):
        for connection in self.active_connections.get(stream_id, []):
            await connection.send_json(data)

    async def update_stream_state(self, stream_id: str, action: str):
        # Update playback state, e.g., play, pause, next song, etc.
        action_data = {
            "action": action,
            "stream_id": stream_id
        }
        await self.broadcast_stream_update(stream_id, action_data)

    async def update_queue(self, stream_id: str):
        # Send updated queue information to all connected users
        queue_data = self.stream_service.get_queue_data(stream_id)
        await self.broadcast_stream_update(stream_id, queue_data)
