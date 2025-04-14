import json
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
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
        if stream_id in self.active_connections:
            if websocket in self.active_connections[stream_id]:
                self.active_connections[stream_id].remove(websocket)

            if not self.active_connections[stream_id]:
                del self.active_connections[stream_id]

    async def broadcast_stream_update(self, stream_id: str, data: dict):
        for connection in self.active_connections.get(stream_id, []):
            await connection.send_json(data)

    async def update_stream_state(self, stream_id: str, action: str):
        action_data = {
            "action": action,
            "stream_id": stream_id
        }
        await self.broadcast_stream_update(stream_id, action_data)

    async def update_queue(self, stream_id: str):
        queue_data = self.stream_service.get_queue_data(stream_id)
        await self.broadcast_stream_update(stream_id, queue_data)


# Define the actual WebSocket endpoint to be mounted
stream_ws = StreamWebSocket()

async def stream_ws_endpoint(websocket: WebSocket, stream_id: str):
    try:
        await stream_ws.connect(websocket, stream_id)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "action":
                await stream_ws.update_stream_state(stream_id, message.get("action"))
            elif message.get("type") == "queue_update":
                await stream_ws.update_queue(stream_id)

    except WebSocketDisconnect:
        await stream_ws.disconnect(websocket, stream_id)
    except WebSocketException:
        await websocket.close()