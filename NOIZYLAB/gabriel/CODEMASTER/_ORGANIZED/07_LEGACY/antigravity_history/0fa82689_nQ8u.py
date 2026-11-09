# ============================================================================
# GABRIEL SERVER V3.0 (API GATEWAY)
# WebSocket + Streaming + Telemetry + Enhanced Endpoints
# ============================================================================

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
import asyncio
import json
import time
from pathlib import Path
from typing import Optional

from gabriel_brain import GabrielBrain

# ============================================================================
# CONFIGURATION
# ============================================================================

VERSION = "3.0"
PORT = 8000
AVATAR_DIR = Path(__file__).parent.parent / "avatar"

# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

brain = GabrielBrain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await brain.wake_up()
    yield
    # Cleanup on shutdown


# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = FastAPI(
    title="Gabriel API",
    version=VERSION,
    description="GABRIEL V4.0 - Omniscient God Mode API Gateway",
    lifespan=lifespan,
)

# CORS for local Avatar and cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class InteractionRequest(BaseModel):
    text: str
    stream: bool = False


class InteractionResponse(BaseModel):
    response: str
    action: Optional[str] = None
    meta: Optional[dict] = None


class ExecuteRequest(BaseModel):
    command: str
    confirm: bool = False


# ============================================================================
# WEBSOCKET CONNECTION MANAGER
# ============================================================================


class ConnectionManager:
    """Manage WebSocket connections for real-time communication."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connection_times: dict[WebSocket, float] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_times[websocket] = time.time()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_times:
            del self.connection_times[websocket]

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead.append(connection)
        for d in dead:
            self.disconnect(d)

    def get_stats(self) -> dict:
        return {
            "active_connections": len(self.active_connections),
            "longest_connection_seconds": max(
                (time.time() - t for t in self.connection_times.values()),
                default=0,
            ),
        }


manager = ConnectionManager()


# ============================================================================
# CORE ENDPOINTS
# ============================================================================


@app.get("/")
async def root():
    """Root endpoint - API info."""
    return {
        "name": "Gabriel API",
        "version": VERSION,
        "status": brain.status,
        "mode": "God Mode V4",
        "endpoints": [
            "/status",
            "/interact",
            "/stream",
            "/ws",
            "/health",
            "/metrics",
            "/memory",
        ],
    }


@app.get("/status")
async def get_status():
    """Get comprehensive system status."""
    return brain.get_status()


@app.get("/health")
async def health_check():
    """Simple health check for load balancers."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": time.time() - brain.boot_time,
    }


@app.get("/metrics")
async def get_metrics():
    """Get telemetry metrics."""
    metrics = brain.get_metrics()
    metrics["websocket"] = manager.get_stats()
    return metrics


@app.get("/memory")
async def get_memory_status():
    """Get memory/MemCell status."""
    return {
        "recall": brain.memory.recall(),
        "neural_state": brain.memory.memory.get("neural_state", {}),
        "personas": brain.memory.memory.get("personas", {}),
    }


# ============================================================================
# INTERACTION ENDPOINTS
# ============================================================================


@app.post("/interact", response_model=InteractionResponse)
async def interact(request: InteractionRequest):
    """Process a text interaction."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Empty input")

    result = await brain.process_input(request.text)

    # Broadcast to WebSocket clients
    await manager.broadcast(
        {
            "type": "interaction",
            "input": request.text,
            "response": result["response"],
            "meta": result["meta"],
        }
    )

    return result


@app.get("/stream")
async def stream_response(prompt: str):
    """Stream a response using Server-Sent Events."""
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    async def generate():
        async for token in brain.stream_response(prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time bidirectional communication."""
    await manager.connect(websocket)
    try:
        # Send welcome message
        await websocket.send_json(
            {
                "type": "connected",
                "status": brain.status,
                "message": "Gabriel WebSocket connected.",
            }
        )

        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                msg_type = message.get("type", "interact")
                content = message.get("content", message.get("text", ""))

                if msg_type == "ping":
                    await websocket.send_json({"type": "pong", "timestamp": time.time()})

                elif msg_type == "status":
                    await websocket.send_json(
                        {"type": "status", "data": brain.get_status()}
                    )

                elif msg_type == "interact" and content:
                    result = await brain.process_input(content)
                    await websocket.send_json(
                        {
                            "type": "response",
                            "input": content,
                            "response": result["response"],
                            "meta": result["meta"],
                        }
                    )
                    # Broadcast to other clients
                    await manager.broadcast(
                        {
                            "type": "activity",
                            "source": "websocket",
                            "summary": f"Processed: {content[:30]}...",
                        }
                    )

                elif msg_type == "stream" and content:
                    await websocket.send_json({"type": "stream_start"})
                    full_response = ""
                    async for token in brain.stream_response(content):
                        full_response += token
                        await websocket.send_json({"type": "stream_token", "token": token})
                    await websocket.send_json(
                        {"type": "stream_end", "full_response": full_response}
                    )

                else:
                    await websocket.send_json(
                        {"type": "error", "message": "Unknown message type or empty content"}
                    )

            except json.JSONDecodeError:
                # Treat as plain text interact
                result = await brain.process_input(data)
                await websocket.send_json(
                    {
                        "type": "response",
                        "input": data,
                        "response": result["response"],
                        "meta": result["meta"],
                    }
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ============================================================================
# AVATAR STATIC FILES
# ============================================================================


@app.get("/avatar")
@app.get("/avatar/")
async def serve_avatar():
    """Serve the avatar HTML page."""
    avatar_file = AVATAR_DIR / "index.html"
    if avatar_file.exists():
        return FileResponse(avatar_file)
    raise HTTPException(status_code=404, detail="Avatar not found")


@app.get("/avatar/{file_path:path}")
async def serve_avatar_files(file_path: str):
    """Serve avatar static files."""
    file = AVATAR_DIR / file_path
    if file.exists() and file.is_file():
        return FileResponse(file)
    raise HTTPException(status_code=404, detail="File not found")


# ============================================================================
# EXECUTION ENDPOINT (SAFETY GATED)
# ============================================================================


@app.post("/execute")
async def execute_command(request: ExecuteRequest):
    """Execute a system command (requires explicit confirmation)."""
    if not request.confirm:
        return {
            "status": "pending",
            "message": "Command queued. Set confirm=true to execute.",
            "command": request.command,
            "warning": "EXECUTE GATE: Destructive commands require explicit confirmation.",
        }

    # Log the action
    brain.memory.track(
        "EXECUTE",
        "Command",
        {"command": request.command, "confirmed": True},
    )

    # For safety, we only describe what would happen
    return {
        "status": "acknowledged",
        "message": f"Command acknowledged: {request.command}",
        "note": "Actual execution would occur via gabriel_cli.py",
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🧠 GABRIEL SERVER V3.0 STARTING...")
    print(f"🌐 http://localhost:{PORT}")
    print(f"📡 WebSocket: ws://localhost:{PORT}/ws")
    print(f"🎭 Avatar: http://localhost:{PORT}/avatar")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )
