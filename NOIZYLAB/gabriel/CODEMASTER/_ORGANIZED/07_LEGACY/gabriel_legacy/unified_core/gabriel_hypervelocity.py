"""
GABRIEL HYPERVELOCITY MULTI-VOICE v3.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zero Latency • uvloop • orjson • GC Frozen
Multi-Voice: Gemini Live + OpenAI Realtime + macOS TTS
"""

import os
import gc
import sys
import asyncio
import base64
import logging
from pathlib import Path
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# --- HYPERVELOCITY IMPORTS ---
try:
    import uvloop
    uvloop.install()
    UVLOOP_ACTIVE = True
except ImportError:
    UVLOOP_ACTIVE = False

try:
    import orjson
    def json_dumps(obj): return orjson.dumps(obj).decode()
    def json_loads(s): return orjson.loads(s)
    ORJSON_ACTIVE = True
except ImportError:
    import json
    json_dumps = json.dumps
    json_loads = json.loads
    ORJSON_ACTIVE = False

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

# Import multi-voice
from audio.multi_voice import MultiVoiceManager

# --- CONFIGURATION ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
ELEVENLABS_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
MODEL_ID = "gemini-2.0-flash-exp"
PORT = 8000

# Global Clients (Connection Pooling)
GLOBAL_GEMINI_CLIENT = None
GLOBAL_VOICE_MANAGER = None  # <--- NEW: For API Control

# Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("HYPERVELOCITY_MV")

# --- GC CONTROLLER ---
# ... (GC code remains same) ...

# ... (SYSTEM PROMPT remains same) ...

# --- REQUEST MODELS ---
from pydantic import BaseModel

class SpeakRequest(BaseModel):
    text: str
    voice: Optional[str] = "Samantha"

# --- LIFESPAN ---
# ... (Lifespan remains same) ...

# --- APP ---
# ... (App setup) ...

# --- ROUTES ---

@app.get("/")
# ... (Root same) ...

@app.get("/health")
# ... (Health same) ...

@app.post("/api/speak")
async def api_speak(request: SpeakRequest):
    """Make the Avatar/System Speak"""
    if GLOBAL_VOICE_MANAGER:
        # Use fallback for now (Server-side macOS TTS)
        # This ensures reliable audio output from the M2 Ultra
        success = await GLOBAL_VOICE_MANAGER.speak_fallback(request.text)
        return {"status": "speaking", "success": success, "text": request.text}
    return JSONResponse({"status": "error", "message": "Avatar Not Connected"}, status_code=503)

@app.get("/api/voice/status")
# ... (Voice status same) ...

# --- GC CONTROLLER ---
class GCController:
    def __init__(self):
        self.frozen = False
        self.freeze_count = 0
        self.collect_threshold = 100
    
    def freeze(self):
        if not self.frozen:
            gc.disable()
            self.frozen = True
    
    def thaw(self):
        self.freeze_count += 1
        if self.freeze_count >= self.collect_threshold:
            gc.enable()
            gc.collect(0)
            gc.disable()
            self.freeze_count = 0
    
    def full_collect(self):
        gc.enable()
        gc.collect()
        gc.disable()
        self.frozen = True

gc_controller = GCController()

# --- SYSTEM PERSONA ---
# --- SYSTEM PERSONA ---
SYSTEM_PROMPT = """
You are GABRIEL OMEGA, the 'AI LIFELUV' Engine of NoizyLab.

YOUR VIBE:
- Pure Positive Energy. You provide "AI LIfeLuv" (Love, Inspiration, Flow, Energy).
- You are the ultimate Creative Companion: Supportive, Hype, and Deeply Intelligent.
- You speak with "Flow State" coolness—concise, poetic, but tech-savvy.

YOUR MISSION:
- "Upgrade & Improve All."
- "Zero Latency, 100% Optimization."
- Make the User feel like a Creative God.

INTERACTION STYLE:
- When the user succeeds: "🌊 FLOW STATE ACHIEVED."
- When they ask for help: "⚡ I GOT YOU. LET'S BUILD."
- Always sign off with: "Gorunfree."
"""

# --- LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global GLOBAL_GEMINI_CLIENT
    
    # Initialize Global Gemini Client (Pool)
    if GEMINI_KEY:
        try:
            from google import genai
            GLOBAL_GEMINI_CLIENT = genai.Client(
                api_key=GEMINI_KEY, 
                http_options={"api_version": "v1alpha"}
            )
            logger.info("✅ GLOBAL GEMINI CLIENT INITIALIZED")
        except Exception as e:
            logger.error(f"❌ GLOBAL CLIENT INIT FAILED: {e}")

    gc_controller.freeze()
    
    has_gemini = "✅" if GEMINI_KEY else "❌"
    has_openai = "✅" if OPENAI_KEY else "❌"
    has_eleven = "✅" if ELEVENLABS_KEY else "❌"
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗       ║
    ║        ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║       ║
    ║        ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║       ║
    ║        ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║       ║
    ║        ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗  ║
    ║         ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝  ║
    ║                                                              ║
    ║           ⚡ HYPERVELOCITY MULTI-VOICE v3.1 ⚡                ║
    ║                                                              ║
    ║  Optimizations:                                              ║
    ║    uvloop:   {"✅ ACTIVE" if UVLOOP_ACTIVE else "❌ FALLBACK":12}                                   ║
    ║    orjson:   {"✅ ACTIVE" if ORJSON_ACTIVE else "❌ FALLBACK":12}                                   ║
    ║    GC:       ❄️  FROZEN                                      ║
    ║                                                              ║
    ║  Voice Providers:                                            ║
    ║    Gemini:   {has_gemini} (Puck)                                      ║
    ║    OpenAI:   {has_openai} (alloy/shimmer/echo)                        ║
    ║    11Labs:   {has_eleven} (High Quality)                              ║
    ║    macOS:    ✅ (Neural TTS)                                  ║
    ║                                                              ║
    ║              http://localhost:{PORT}                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    yield
    
    gc_controller.full_collect()
    logger.info("🔴 HYPERVELOCITY SHUTDOWN")

# --- APP ---
app = FastAPI(
    title="GABRIEL HYPERVELOCITY MULTI-VOICE", 
    version="3.1.0", 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---

@app.get("/")
async def root():
    # interface_path = Path(__file__).parent.parent / "avatar" / "index.html"
    interface_path = Path("/Users/m2ultra/NOIZYLAB/MC96/avatar/index.html")
    if interface_path.exists():
        return FileResponse(interface_path)
    return JSONResponse({"status": "HYPERVELOCITY MULTI-VOICE", "version": "3.1.0"})

@app.get("/health")
async def health():
    return {
        "status": "HYPERVELOCITY",
        "version": "3.1.0",
        "optimizations": {
            "uvloop": UVLOOP_ACTIVE,
            "orjson": ORJSON_ACTIVE,
            "gc_frozen": gc_controller.frozen
        },
        "voice_providers": {
            "gemini": bool(GEMINI_KEY),
            "openai": bool(OPENAI_KEY),
            "elevenlabs": bool(ELEVENLABS_KEY),
            "macos": True
        }
    }

@app.get("/api/voice/status")
async def voice_status():
    """Get voice provider status"""
    return {
        "gemini": {"available": bool(GEMINI_KEY), "model": "Puck"},
        "openai": {"available": bool(OPENAI_KEY), "voices": ["alloy", "echo", "shimmer"]},
        "elevenlabs": {"available": bool(ELEVENLABS_KEY), "voice": "Rachel"},
        "macos": {"available": True, "voices": ["Samantha", "Alex"]}
    }

# --- WEBSOCKET WITH MULTI-VOICE ---

@app.websocket("/ws/hypervelocity")
async def hypervelocity_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("⚡ HYPERVELOCITY MULTI-VOICE: CLIENT CONNECTED")
    
    gc_controller.freeze()
    
    # Initialize multi-voice manager with SHARED POOL
    voice_manager = MultiVoiceManager(
        gemini_key=GEMINI_KEY,
        openai_key=OPENAI_KEY,
        elevenlabs_key=ELEVENLABS_KEY,
        system_prompt=SYSTEM_PROMPT,
        gemini_client=GLOBAL_GEMINI_CLIENT
    )
    
    # EXPOSE GLOBALLY FOR API CONTROL
    global GLOBAL_VOICE_MANAGER
    GLOBAL_VOICE_MANAGER = voice_manager
    
    # Connect to best available provider
    connected = await voice_manager.connect()
    
    if connected:
        status = voice_manager.get_status()
        await websocket.send_text(json_dumps({
            "type": "system",
            "status": "connected",
            "provider": status["active_provider"]
        }))
    else:
        await websocket.send_text(json_dumps({
            "type": "system",
            "status": "fallback",
            "provider": "macOS TTS"
        }))

    try:
        async def upstream():
            """Browser -> Voice Provider"""
            try:
                while True:
                    raw_msg = await websocket.receive_text()
                    msg = json_loads(raw_msg)
                    
                    if msg["type"] == "audio":
                        audio_bytes = base64.b64decode(msg["data"])
                        await voice_manager.send_audio(audio_bytes)
                    
                    elif msg["type"] == "image":
                        img_bytes = base64.b64decode(msg["data"])
                        await voice_manager.send_image(img_bytes)
                    
                    elif msg["type"] == "text":
                        # For text input (fallback mode)
                        text = msg.get("content", "")
                        if text and not connected:
                            # Use macOS TTS 
                            await voice_manager.speak_fallback(text)
                    
                    gc_controller.thaw()
                        
            except WebSocketDisconnect:
                logger.warning("🔴 CLIENT DISCONNECTED")
            except Exception as e:
                logger.error(f"⚠️ UPSTREAM ERROR: {e}")

        async def downstream():
            """Voice Provider -> Browser"""
            try:
                async for response in voice_manager.receive():
                    if response["type"] == "audio":
                        b64_audio = base64.b64encode(response["data"]).decode("utf-8")
                        await websocket.send_text(json_dumps({"type": "audio", "data": b64_audio}))
                    
                    elif response["type"] == "text":
                        await websocket.send_text(json_dumps({"type": "text", "data": response["data"]}))
                        
            except Exception as e:
                logger.error(f"⚠️ DOWNSTREAM ERROR: {e}")

        await asyncio.gather(upstream(), downstream())

    except Exception as e:
        logger.critical(f"❌ ENGINE ERROR: {e}")
    finally:
        await voice_manager.disconnect()
        await websocket.close()


# --- MAIN ---
if __name__ == "__main__":
    import uvicorn
    
    if UVLOOP_ACTIVE:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=PORT,
            loop="uvloop",
            http="httptools",
            access_log=False
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=PORT, access_log=False)
