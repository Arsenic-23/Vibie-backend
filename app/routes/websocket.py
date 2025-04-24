from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from collections import defaultdict
from app.db.models import Stream
from app.db.repositories import StreamRepository

router = APIRouter()

# In-memory store for active WebSocket connections per stream
active_connections = defaultdict(list)  # stream_id: [WebSocket]

async def broadcast_message(stream_id: str, message: dict, sender: WebSocket = None):
    """Broadcast a message to all connected WebSocket clients except the sender."""
    for conn in active_connections[stream_id]:
        if conn != sender:
            try:
                await conn.send_json(message)
            except Exception as e:
                # Handle WebSocket error (e.g., client disconnected)
                active_connections[stream_id].remove(conn)

async def notify_users(stream_id: str, message: str):
    """Send a notification to all users in the stream."""
    await broadcast_message(stream_id, {"message": message})

@router.websocket("/ws/stream/{stream_id}")
async def websocket_endpoint(websocket: WebSocket, stream_id: str):
    """Handles WebSocket connections for a specific stream."""
    
    # Accept WebSocket connection
    await websocket.accept()

    # Get the stream by stream_id
    stream_repo = StreamRepository()
    stream = stream_repo.get_stream_by_chat_id(stream_id)
    
    if stream is None:
        await websocket.close()
        return

    # Add the connection to the active connections list
    active_connections[stream_id].append(websocket)

    # Notify all connected clients that a new user joined
    await notify_users(stream_id, f"New user joined stream {stream_id}")

    # Send the current state to the new client
    await websocket.send_json({
        "type": "init_state",
        "now_playing": stream.now_playing.dict() if stream.now_playing else None,
        "queue": [song.dict() for song in stream.song_queue],
        "users": stream.users,
    })

    try:
        # Listen for incoming messages and broadcast them to other connections in the same stream
        while True:
            data = await websocket.receive_json()

            # Handle the incoming message (e.g., song request, skip, etc.)
            # For example, you can check the 'type' of the message and process accordingly

            # After handling any updates, broadcast the updated state
            await broadcast_message(stream_id, {
                "type": "stream_update",
                "now_playing": stream.now_playing.dict() if stream.now_playing else None,
                "queue": [song.dict() for song in stream.song_queue],
                "users": stream.users,
            }, sender=websocket)

    except WebSocketDisconnect:
        # Remove the disconnected WebSocket from the list
        active_connections[stream_id].remove(websocket)

        # If no active connections remain, delete the stream from active connections
        if not active_connections[stream_id]:
            del active_connections[stream_id]

        # Optionally, notify others that a user has left the stream
        await notify_users(stream_id, f"A user has left stream {stream_id}")