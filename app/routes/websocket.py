from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database import get_db
from collections import defaultdict

router = APIRouter()

# In-memory store for active WebSocket connections per stream
active_connections = defaultdict(list)  # stream_id: [WebSocket]

@router.websocket("/ws/stream/{stream_id}")
async def websocket_endpoint(websocket: WebSocket, stream_id: str):
    await websocket.accept()
    active_connections[stream_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Broadcast received data to all other connections in the same stream
            for conn in active_connections[stream_id]:
                if conn != websocket:
                    await conn.send_json(data)

    except WebSocketDisconnect:
        active_connections[stream_id].remove(websocket)
        if not active_connections[stream_id]:
            del active_connections[stream_id]