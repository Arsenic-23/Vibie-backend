from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from collections import defaultdict
from app.db.models import Stream
from app.db.repositories import StreamRepository

router = APIRouter()

# In-memory store for active WebSocket connections per stream
active_connections = defaultdict(list)  # stream_id: [WebSocket]

@router.websocket("/ws/stream/{stream_id}")
async def websocket_endpoint(websocket: WebSocket, stream_id: str):
    """Handles WebSocket connections for a specific stream."""
    
    # Accept WebSocket connection
    await websocket.accept()
    
    # Add the connection to the active connections list
    active_connections[stream_id].append(websocket)

    try:
        # Notify all connected clients that a new user joined
        for conn in active_connections[stream_id]:
            if conn != websocket:
                await conn.send_json({"message": f"New user joined stream {stream_id}"})

        # Listen for incoming messages and broadcast them to other connections in the same stream
        while True:
            data = await websocket.receive_json()
            # Broadcast the data to all other WebSocket clients in the same stream
            for conn in active_connections[stream_id]:
                if conn != websocket:
                    await conn.send_json(data)

    except WebSocketDisconnect:
        # Remove the disconnected WebSocket from the list
        active_connections[stream_id].remove(websocket)

        # If no active connections remain, delete the stream from active connections
        if not active_connections[stream_id]:
            del active_connections[stream_id]
        
        # Optionally, notify others that a user has left the stream
        for conn in active_connections[stream_id]:
            await conn.send_json({"message": f"A user has left stream {stream_id}"})