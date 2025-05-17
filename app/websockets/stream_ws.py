import json
from fastapi import WebSocket, WebSocketDisconnect, Query
from typing import Dict, List
from app.services.stream_service import StreamService

class StreamWebSocketManager:
    def __init__(self, broadcast_message):
        self.stream_service = StreamService(broadcast_message)
        self.active_connections: Dict[str, List[WebSocket]] = {}  # stream_id -> connections
        self.stream_users: Dict[str, set] = {}  # stream_id -> set of user_ids

    async def connect(self, websocket: WebSocket, stream_id: str, user_id: str):
        await websocket.accept()

        # Track connection
        if stream_id not in self.active_connections:
            self.active_connections[stream_id] = []
            self.stream_users[stream_id] = set()
        self.active_connections[stream_id].append(websocket)
        self.stream_users[stream_id].add(user_id)

        # Update users in stream object
        self.stream_service.update_users_in_stream(stream_id, list(self.stream_users[stream_id]))

        # Send initial stream data
        stream_data = self.stream_service.get_stream_data_by_chat(stream_id)
        await websocket.send_json({
            "type": "initial_stream_data",
            "data": stream_data
        })

        # Notify others user joined
        await self.broadcast_stream_update(stream_id, {
            "type": "user_joined",
            "user_id": user_id,
            "users": list(self.stream_users[stream_id])
        }, exclude=[websocket])

    async def disconnect(self, websocket: WebSocket, stream_id: str, user_id: str):
        if stream_id in self.active_connections:
            if websocket in self.active_connections[stream_id]:
                self.active_connections[stream_id].remove(websocket)

            # Remove user if no other connections of same user remain (optional enhancement)
            # For simplicity, we remove user immediately
            if user_id in self.stream_users.get(stream_id, set()):
                self.stream_users[stream_id].remove(user_id)

            # Update users in stream object
            self.stream_service.update_users_in_stream(stream_id, list(self.stream_users.get(stream_id, [])))

            # Notify others user left
            await self.broadcast_stream_update(stream_id, {
                "type": "user_left",
                "user_id": user_id,
                "users": list(self.stream_users.get(stream_id, []))
            }, exclude=[websocket])

            if not self.active_connections[stream_id]:
                del self.active_connections[stream_id]
                del self.stream_users[stream_id]

    async def broadcast_stream_update(self, stream_id: str, data: dict, exclude: List[WebSocket] = []):
        for conn in self.active_connections.get(stream_id, []):
            if conn not in exclude:
                try:
                    await conn.send_json(data)
                except Exception:
                    # Handle broken connections
                    self.active_connections[stream_id].remove(conn)

    async def handle_message(self, stream_id: str, data: dict):
        msg_type = data.get("type")
        if msg_type == "action":
            action = data.get("action")
            if action == "skip":
                self.stream_service.skip_to_next_song_by_chat(stream_id)
            elif action == "end":
                self.stream_service.end_stream(stream_id)
            # Add more actions if needed

        elif msg_type == "queue_update":
            # Could be used to add/remove songs in queue if extended

            pass

        # After action, broadcast updated stream state
        updated_stream = self.stream_service.get_stream_data_by_chat(stream_id)
        await self.broadcast_stream_update(stream_id, {
            "type": "stream_update",
            "data": updated_stream
        })

stream_ws_manager = StreamWebSocketManager(broadcast_message="")  # Or pass actual broadcast function if needed

async def websocket_endpoint(websocket: WebSocket, stream_id: str, user_id: str = Query(...)):
    try:
        await stream_ws_manager.connect(websocket, stream_id, user_id)

        while True:
            data_text = await websocket.receive_text()
            data = json.loads(data_text)
            await stream_ws_manager.handle_message(stream_id, data)

    except WebSocketDisconnect:
        await stream_ws_manager.disconnect(websocket, stream_id, user_id)
    except Exception:
        await websocket.close()