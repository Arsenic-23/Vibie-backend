import json
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from app.services.stream_service import StreamService

class StreamWebSocket:
    def __init__(self):
        self.stream_service = StreamService(self.broadcast_stream_update)
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, stream_id: str):
        await websocket.accept()

        if stream_id not in self.active_connections:
            self.active_connections[stream_id] = []

        self.active_connections[stream_id].append(websocket)

        # Send initial stream data (e.g., current song, user count, queue length)
        stream_data = self.stream_service.get_stream_data_by_chat(stream_id)
        await websocket.send_json({
            "type": "initial_stream_data",
            "data": stream_data
        })

    async def disconnect(self, websocket: WebSocket, stream_id: str):
        if stream_id in self.active_connections:
            if websocket in self.active_connections[stream_id]:
                self.active_connections[stream_id].remove(websocket)

            if not self.active_connections[stream_id]:
                del self.active_connections[stream_id]

    async def broadcast_stream_update(self, stream_id: str, data: dict):
        for connection in self.active_connections.get(stream_id, []):
            await connection.send_json(data)

    async def update_stream_state(self, stream_id: str, action: str):
        # Perform the necessary action using StreamService
        if action == "skip":
            await self.stream_service.skip_to_next_song_by_chat(stream_id)
        elif action == "end":
            await self.stream_service.end_stream(stream_id)

        # Broadcast the updated stream state
        updated_stream = self.stream_service.get_stream_data_by_chat(stream_id)
        await self.broadcast_stream_update(stream_id, {
            "type": "stream_update",
            "data": updated_stream
        })

    async def update_queue(self, stream_id: str):
        queue_data = self.stream_service.get_stream_data_by_chat(stream_id)
        await self.broadcast_stream_update(stream_id, {
            "type": "queue_update",
            "data": queue_data
        })


# Define the actual WebSocket endpoint to be mounted
stream_ws = StreamWebSocket()

async def stream_ws_endpoint(websocket: WebSocket, stream_id: str):
    try:
        await stream_ws.connect(websocket, stream_id)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "action":
                action = message.get("action")
                await stream_ws.update_stream_state(stream_id, action)
            elif message.get("type") == "queue_update":
                await stream_ws.update_queue(stream_id)

    except WebSocketDisconnect:
        await stream_ws.disconnect(websocket, stream_id)
    except WebSocketException:
        await websocket.close()