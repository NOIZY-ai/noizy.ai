"""
NOIZY Fish — Real-time Events
===============================

Server-Sent Events (SSE) stream for real-time updates.

Supports:
- Live inquiry notifications
- Consent change broadcasts
- License activation events
- Royalty milestones

Usage:
    GET /events              — All events
    GET /events?creator={id} — Events for a creator
    GET /events?type={type}  — Events of a specific type

WebSocket support also available for bidirectional communication.
"""

import asyncio
import json
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Set, AsyncGenerator
from uuid import uuid4


# ═══════════════════════════════════════════════════════════════════════════
# Event Stream
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class StreamClient:
    """A connected SSE client."""
    client_id: str = field(default_factory=lambda: str(uuid4()))
    connected_at: datetime = field(default_factory=datetime.utcnow)
    creator_filter: Optional[str] = None
    event_type_filter: Optional[str] = None
    queue: asyncio.Queue = field(default_factory=asyncio.Queue)


class EventStream:
    """
    Event stream manager for real-time updates.
    Handles multiple connected clients with filtering.
    """

    def __init__(self):
        self.clients: dict[str, StreamClient] = {}
        self._lock = asyncio.Lock()

    async def connect(
        self,
        creator_filter: Optional[str] = None,
        event_type_filter: Optional[str] = None
    ) -> StreamClient:
        """Register a new client connection."""
        client = StreamClient(
            creator_filter=creator_filter,
            event_type_filter=event_type_filter
        )

        async with self._lock:
            self.clients[client.client_id] = client

        return client

    async def disconnect(self, client_id: str):
        """Disconnect a client."""
        async with self._lock:
            if client_id in self.clients:
                del self.clients[client_id]

    async def broadcast(self, event: dict):
        """Broadcast an event to all matching clients."""
        event_type = event.get("event_type", "")
        creator_id = event.get("creator_id")

        async with self._lock:
            for client in self.clients.values():
                # Apply filters
                if client.creator_filter and creator_id != client.creator_filter:
                    continue
                if client.event_type_filter and event_type != client.event_type_filter:
                    continue

                try:
                    await client.queue.put(event)
                except Exception:
                    pass  # Client disconnected

    async def stream(self, client: StreamClient) -> AsyncGenerator[str, None]:
        """Generate SSE stream for a client."""
        try:
            # Send initial connection event
            yield self._format_sse({
                "event_type": "connected",
                "client_id": client.client_id,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Stream events
            while True:
                try:
                    event = await asyncio.wait_for(
                        client.queue.get(),
                        timeout=30.0  # Heartbeat every 30 seconds
                    )
                    yield self._format_sse(event)
                except asyncio.TimeoutError:
                    # Send heartbeat
                    yield self._format_sse({
                        "event_type": "heartbeat",
                        "timestamp": datetime.utcnow().isoformat()
                    })
        finally:
            await self.disconnect(client.client_id)

    def _format_sse(self, data: dict) -> str:
        """Format data as SSE message."""
        event_type = data.get("event_type", "message")
        json_data = json.dumps(data)
        return f"event: {event_type}\ndata: {json_data}\n\n"

    def client_count(self) -> int:
        """Get number of connected clients."""
        return len(self.clients)


# ═══════════════════════════════════════════════════════════════════════════
# FastAPI Integration
# ═══════════════════════════════════════════════════════════════════════════

# Global stream instance
_event_stream: Optional[EventStream] = None


def get_event_stream() -> EventStream:
    """Get the global event stream."""
    global _event_stream
    if _event_stream is None:
        _event_stream = EventStream()
    return _event_stream


async def broadcast_event(event: dict):
    """Broadcast an event to all connected clients."""
    stream = get_event_stream()
    await stream.broadcast(event)


def create_sse_routes(app):
    """Add SSE routes to a FastAPI app."""
    from fastapi import Query
    from fastapi.responses import StreamingResponse

    @app.get("/events")
    async def event_stream(
        creator: Optional[str] = Query(None, description="Filter by creator"),
        type: Optional[str] = Query(None, description="Filter by event type")
    ):
        """
        Server-Sent Events stream for real-time updates.

        Connect to receive live events:
        - inquiry.approved
        - inquiry.denied
        - consent.rule.updated
        - license.created
        - royalty.earned
        """
        stream = get_event_stream()
        client = await stream.connect(
            creator_filter=creator,
            event_type_filter=type
        )

        return StreamingResponse(
            stream.stream(client),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )

    @app.get("/events/status")
    async def event_stream_status():
        """Get event stream status."""
        stream = get_event_stream()
        return {
            "connected_clients": stream.client_count(),
            "status": "active"
        }

    return app


# ═══════════════════════════════════════════════════════════════════════════
# Event Broadcasting from Notifications
# ═══════════════════════════════════════════════════════════════════════════

def setup_realtime_integration():
    """
    Set up integration between notification system and realtime stream.
    Call this during app startup.
    """
    from .notifications import get_notification_service, Event

    service = get_notification_service()
    stream = get_event_stream()

    # Register handler for all events
    async def broadcast_to_stream(event: Event):
        await stream.broadcast(event.to_dict())

    service.on("*", broadcast_to_stream)


# ═══════════════════════════════════════════════════════════════════════════
# WebSocket Support
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class WebSocketClient:
    """A WebSocket client."""
    client_id: str = field(default_factory=lambda: str(uuid4()))
    websocket: any = None
    creator_filter: Optional[str] = None
    subscriptions: Set[str] = field(default_factory=set)


class WebSocketManager:
    """
    WebSocket connection manager.
    Supports bidirectional communication for interactive clients.
    """

    def __init__(self):
        self.clients: dict[str, WebSocketClient] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket, creator_filter: Optional[str] = None) -> WebSocketClient:
        """Accept a new WebSocket connection."""
        client = WebSocketClient(
            websocket=websocket,
            creator_filter=creator_filter
        )

        async with self._lock:
            self.clients[client.client_id] = client

        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "client_id": client.client_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        return client

    async def disconnect(self, client_id: str):
        """Disconnect a WebSocket client."""
        async with self._lock:
            if client_id in self.clients:
                del self.clients[client_id]

    async def subscribe(self, client_id: str, event_types: list[str]):
        """Subscribe client to event types."""
        async with self._lock:
            if client_id in self.clients:
                self.clients[client_id].subscriptions.update(event_types)

    async def unsubscribe(self, client_id: str, event_types: list[str]):
        """Unsubscribe client from event types."""
        async with self._lock:
            if client_id in self.clients:
                self.clients[client_id].subscriptions.difference_update(event_types)

    async def broadcast(self, event: dict):
        """Broadcast event to matching WebSocket clients."""
        event_type = event.get("event_type", "")
        creator_id = event.get("creator_id")

        async with self._lock:
            for client in self.clients.values():
                # Check creator filter
                if client.creator_filter and creator_id != client.creator_filter:
                    continue

                # Check subscriptions (empty = all)
                if client.subscriptions and event_type not in client.subscriptions:
                    continue

                try:
                    await client.websocket.send_json(event)
                except Exception:
                    pass  # Client disconnected

    async def handle_message(self, client_id: str, message: dict) -> dict:
        """Handle incoming WebSocket message."""
        msg_type = message.get("type", "")

        if msg_type == "subscribe":
            await self.subscribe(client_id, message.get("events", []))
            return {"type": "subscribed", "events": message.get("events", [])}

        elif msg_type == "unsubscribe":
            await self.unsubscribe(client_id, message.get("events", []))
            return {"type": "unsubscribed", "events": message.get("events", [])}

        elif msg_type == "ping":
            return {"type": "pong", "timestamp": datetime.utcnow().isoformat()}

        else:
            return {"type": "error", "message": f"Unknown message type: {msg_type}"}


# Global WebSocket manager
_ws_manager: Optional[WebSocketManager] = None


def get_ws_manager() -> WebSocketManager:
    """Get the global WebSocket manager."""
    global _ws_manager
    if _ws_manager is None:
        _ws_manager = WebSocketManager()
    return _ws_manager


def create_websocket_routes(app):
    """Add WebSocket routes to a FastAPI app."""
    from fastapi import WebSocket, WebSocketDisconnect, Query

    @app.websocket("/ws")
    async def websocket_endpoint(
        websocket: WebSocket,
        creator: Optional[str] = Query(None)
    ):
        """
        WebSocket endpoint for bidirectional communication.

        Messages:
        - {"type": "subscribe", "events": ["inquiry.approved", ...]}
        - {"type": "unsubscribe", "events": [...]}
        - {"type": "ping"}
        """
        await websocket.accept()
        manager = get_ws_manager()
        client = await manager.connect(websocket, creator_filter=creator)

        try:
            while True:
                data = await websocket.receive_json()
                response = await manager.handle_message(client.client_id, data)
                await websocket.send_json(response)
        except WebSocketDisconnect:
            await manager.disconnect(client.client_id)

    return app


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

async def demo():
    """Demonstrate real-time events."""
    print("\n" + "=" * 70)
    print("NOIZY FISH REAL-TIME EVENTS — DEMO")
    print("=" * 70)

    stream = EventStream()

    # Connect clients
    print("\n" + "─" * 50)
    print("CONNECTING CLIENTS")
    print("─" * 50)

    client1 = await stream.connect()
    print(f"  Client 1: {client1.client_id[:8]}... (all events)")

    client2 = await stream.connect(creator_filter="creator-123")
    print(f"  Client 2: {client2.client_id[:8]}... (creator-123 only)")

    client3 = await stream.connect(event_type_filter="inquiry.approved")
    print(f"  Client 3: {client3.client_id[:8]}... (approvals only)")

    print(f"\n  Total clients: {stream.client_count()}")

    # Broadcast events
    print("\n" + "─" * 50)
    print("BROADCASTING EVENTS")
    print("─" * 50)

    events = [
        {"event_type": "inquiry.approved", "creator_id": "creator-123", "amount": 15000},
        {"event_type": "inquiry.denied", "creator_id": "creator-456", "reason": "AI training denied"},
        {"event_type": "consent.updated", "creator_id": "creator-123", "use": "sync_film"}
    ]

    for event in events:
        await stream.broadcast(event)
        print(f"  Broadcast: {event['event_type']}")

    # Check queues
    print("\n" + "─" * 50)
    print("CLIENT QUEUE STATUS")
    print("─" * 50)

    print(f"  Client 1 queue size: {client1.queue.qsize()} (should be 3 - all events)")
    print(f"  Client 2 queue size: {client2.queue.qsize()} (should be 2 - creator-123 only)")
    print(f"  Client 3 queue size: {client3.queue.qsize()} (should be 1 - approvals only)")

    # Cleanup
    await stream.disconnect(client1.client_id)
    await stream.disconnect(client2.client_id)
    await stream.disconnect(client3.client_id)

    print(f"\n  Clients after disconnect: {stream.client_count()}")

    print("\n" + "═" * 70)
    print("DEMO COMPLETE")
    print("═" * 70)
    print("""
To test SSE in browser:

    // In browser console
    const eventSource = new EventSource('http://localhost:8765/events');
    eventSource.onmessage = (e) => console.log(JSON.parse(e.data));

To test WebSocket:

    // In browser console
    const ws = new WebSocket('ws://localhost:8765/ws');
    ws.onmessage = (e) => console.log(JSON.parse(e.data));
    ws.send(JSON.stringify({type: 'subscribe', events: ['inquiry.approved']}));
    """)


if __name__ == "__main__":
    asyncio.run(demo())
