from app.websockets.ws_stream import stream_ws  # Correct import based on your structure

def broadcast_message(chat_id: str, data: dict):
    """
    Broadcast a message to all WebSocket clients connected to a stream (chat_id).
    If no clients are connected, just log the message.
    """
    import asyncio

    if chat_id in stream_ws.active_connections:
        asyncio.create_task(stream_ws.broadcast_stream_update(chat_id, data))
    else:
        print(f"[Broadcast] No active connections for chat_id={chat_id}. Data: {data}")