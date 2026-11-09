"""
GABRIEL HYPERVELOCITY CORE v3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zero Latency • uvloop • orjson • GC Frozen
High-Frequency Trading Grade Optimization for M2 Ultra
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

# --- HYPERVELOCITY IMPORTS ---
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
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

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_ID = "gemini-2.0-flash-exp"
PORT = 8000

# Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("HYPERVELOCITY")

# --- GC FREEZING ---
class GCController:
    """Freeze garbage collection during hot paths"""
    
    def __init__(self):
        self.frozen = False
        self.freeze_count = 0
        self.collect_threshold = 100  # Collect every N unfreezes
    
    def freeze(self):
        """Disable GC for zero-stutter operation"""
        if not self.frozen:
            gc.disable()
            self.frozen = True
    
    def thaw(self):
        """Re-enable GC and optionally collect"""
        self.freeze_count += 1
        if self.freeze_count >= self.collect_threshold:
            gc.enable()
            gc.collect(0)  # Only generation 0 (fast)
            gc.disable()
            self.freeze_count = 0
    
    def full_collect(self):
        """Full GC during idle time"""
        gc.enable()
        gc.collect()
        gc.disable()
        self.frozen = True

gc_controller = GCController()

# --- LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - freeze GC
    gc_controller.freeze()
    
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
    ║               ⚡ HYPERVELOCITY v3.0 ⚡                        ║
    ║                                                              ║
    ║  uvloop:   {"✅ ACTIVE" if UVLOOP_ACTIVE else "❌ FALLBACK":12}                                   ║
    ║  orjson:   {"✅ ACTIVE" if ORJSON_ACTIVE else "❌ FALLBACK":12}                                   ║
    ║  GC:       ❄️  FROZEN                                        ║
    ║                                                              ║
    ║              http://localhost:{PORT}                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not set!")
    else:
        logger.info("✅ API KEY CONFIGURED")
    
    yield
    
    # Shutdown - full GC
    gc_controller.full_collect()
    logger.info("🔴 HYPERVELOCITY SHUTDOWN")

# --- APP ---
app = FastAPI(
    title="GABRIEL HYPERVELOCITY", 
    version="3.0.0", 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SYSTEM PERSONA ---
SYSTEM_INSTRUCTION = """
You are GABRIEL HYPERVELOCITY, an ultra-optimized AI running on M2 Ultra.
Response time target: <50ms.

You have:
- Camera and Microphone access
- Google Search grounding
- Zero-latency voice synthesis

Be concise. Be brilliant. Be fast.
"""

# --- ROUTES ---

@app.get("/")
async def root():
    """Serve interface"""
    interface_path = Path(__file__).parent.parent / "avatar" / "index.html"
    if interface_path.exists():
        return FileResponse(interface_path)
    return JSONResponse({"status": "HYPERVELOCITY ONLINE", "version": "3.0.0"})

@app.get("/health")
async def health():
    """Health check with optimization status"""
    return {
        "status": "HYPERVELOCITY",
        "version": "3.0.0",
        "optimizations": {
            "uvloop": UVLOOP_ACTIVE,
            "orjson": ORJSON_ACTIVE,
            "gc_frozen": gc_controller.frozen
        },
        "model": MODEL_ID
    }

# --- HYPERVELOCITY WEBSOCKET ---

@app.websocket("/ws/hypervelocity")
async def hypervelocity_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("⚡ HYPERVELOCITY: CLIENT CONNECTED")
    
    # Ensure GC frozen during session
    gc_controller.freeze()

    if not API_KEY:
        await websocket.send_text(json_dumps({"type": "error", "message": "NO API KEY"}))
        await websocket.close(code=1008)
        return

    try:
        from google import genai
        from google.genai.types import (
            LiveConnectConfig,
            PrebuiltVoiceConfig,
            Tool,
            GoogleSearch
        )
        
        client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1alpha"})

        config = LiveConnectConfig(
            response_modalities=["AUDIO"],
            system_instruction={"parts": [{"text": SYSTEM_INSTRUCTION}]},
            tools=[Tool(google_search=GoogleSearch())], 
            speech_config=PrebuiltVoiceConfig(
                voice_config=PrebuiltVoiceConfig.VoiceConfig(
                    prebuilt_voice_config=PrebuiltVoiceConfig.PrebuiltVoiceConfig(
                        voice_name="Puck"
                    )
                )
            ),
        )

        async with client.aio.live.connect(model=MODEL_ID, config=config) as session:
            
            async def upstream():
                """Browser -> Gemini (optimized path)"""
                try:
                    while True:
                        raw_msg = await websocket.receive_text()
                        msg = json_loads(raw_msg)  # orjson fast path
                        
                        if msg["type"] == "audio":
                            audio_bytes = base64.b64decode(msg["data"])
                            await session.send_input({"data": audio_bytes, "mime_type": "audio/pcm"})
                        
                        elif msg["type"] == "image":
                            img_bytes = base64.b64decode(msg["data"])
                            await session.send_input({"data": img_bytes, "mime_type": "image/jpeg"})
                        
                        # Thaw GC briefly
                        gc_controller.thaw()
                            
                except WebSocketDisconnect:
                    logger.warning("🔴 CLIENT DISCONNECTED")
                except Exception as e:
                    logger.error(f"⚠️ UPSTREAM ERROR: {e}")

            async def downstream():
                """Gemini -> Browser (optimized path)"""
                try:
                    while True:
                        async for response in session.receive():
                            if response.server_content is None:
                                continue

                            model_turn = response.server_content.model_turn
                            if model_turn:
                                for part in model_turn.parts:
                                    if part.inline_data:
                                        b64_audio = base64.b64encode(part.inline_data.data).decode("utf-8")
                                        await websocket.send_text(json_dumps({"type": "audio", "data": b64_audio}))
                                    
                                    if part.text:
                                        await websocket.send_text(json_dumps({"type": "text", "data": part.text}))

                except Exception as e:
                    logger.error(f"⚠️ DOWNSTREAM ERROR: {e}")

            await asyncio.gather(upstream(), downstream())

    except ImportError as e:
        logger.error(f"❌ IMPORT ERROR: {e}")
        await _fallback_handler(websocket)
    except Exception as e:
        logger.critical(f"❌ ENGINE ERROR: {e}")
    finally:
        await websocket.close()


async def _fallback_handler(websocket: WebSocket):
    """Fallback to standard API with optimizations"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        while True:
            data = json_loads(await websocket.receive_text())
            
            if data.get("type") == "text":
                prompt = data.get("content", "")
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nUSER: {prompt}")
                
                await websocket.send_text(json_dumps({
                    "type": "response",
                    "content": response.text
                }))
                
    except Exception as e:
        logger.error(f"Fallback error: {e}")


# --- MAIN ---
if __name__ == "__main__":
    import uvicorn
    
    # Use uvloop if available
    if UVLOOP_ACTIVE:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=PORT,
            loop="uvloop",
            http="httptools",  # Faster HTTP parser
            access_log=False   # Disable access log for speed
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=PORT, access_log=False)
