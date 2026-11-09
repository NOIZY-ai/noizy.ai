"""
GABRIEL CORE v2.0 - SUPERCHARGED HOT ROD
The Main Brain & Server with Full Arsenal
"""

import os
import asyncio
import json
import base64
import logging
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

from gabriel_tools import GabrielTools

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_ID = "gemini-2.0-flash-exp"
PORT = 8000

# Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("GABRIEL_HOTROD")

# --- LIFESPAN ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗       ║
    ║        ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║       ║
    ║        ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║       ║
    ║        ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║       ║
    ║        ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗  ║
    ║         ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝  ║
    ║                                                              ║
    ║                  SUPERCHARGED HOT ROD v2.0                   ║
    ║        M2 ULTRA • GEMINI 2.0 FLASH • FULL ARSENAL            ║
    ║                                                              ║
    ║              http://localhost:8000                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not set!")
    else:
        logger.info("✅ API KEY CONFIGURED")
    
    yield
    
    # Shutdown
    logger.info("🔴 GABRIEL SHUTTING DOWN")

# --- APP ---
app = FastAPI(title="GABRIEL V2 HOT ROD", version="2.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tools = GabrielTools(api_key=API_KEY)

# --- SYSTEM PERSONA ---
SYSTEM_INSTRUCTION = """
You are GABRIEL, a SUPERCHARGED AI running on M2 Ultra. 
You have CAMERA and MICROPHONE access.
You have GOOGLE SEARCH grounding.

CAPABILITIES:
1. VISION: Comment on what you see immediately
2. SEARCH: Use Google Search for current events
3. MUSIC: Generate production prompts for Suno/MusicFX
4. VIDEO: Generate cinematic prompts for Veo/VideoFX
5. IMAGE: Generate visual prompts for ImageFX
6. VOICE: Write scripts for ElevenLabs

PERSONALITY:
- High-octane, precise, genius-level
- Think like a Hollywood director
- Be concise but brilliant
- Use technical terminology

If processing, say "Processing..." or "Analyzing..."
"""

# --- MODELS ---
class PromptRequest(BaseModel):
    prompt_type: str  # music, video, image, voice
    params: dict = {}

class MemoryRequest(BaseModel):
    content: str
    tags: List[str] = []
    memory_type: str = "general"

# --- ROUTES ---

@app.get("/")
async def root():
    """Serve the Hot Rod interface"""
    return FileResponse("interface/index.html")

@app.get("/health")
async def health():
    """Health check with system info"""
    return {
        "status": "SUPERCHARGED",
        "version": "2.0.0",
        "model": MODEL_ID,
        "uptime": tools.get_uptime(),
        "system": tools.get_system_info()
    }

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "memory": tools.get_memory_stats(),
        "system": tools.get_system_info()
    }

@app.get("/api/memories")
async def get_memories(limit: int = 20):
    """Get recent memories"""
    return tools.get_all_memories(limit=limit)

@app.post("/api/memories")
async def save_memory(req: MemoryRequest):
    """Save a new memory"""
    cell_id = tools.save_memory(req.content, req.tags, req.memory_type)
    return {"id": cell_id, "status": "saved"}

@app.get("/api/memories/search")
async def search_memories(q: str):
    """Search memories"""
    return tools.search_memories(q)

@app.post("/api/generate")
async def generate_prompt(req: PromptRequest):
    """Generate a creative prompt"""
    handlers = {
        "music": lambda: tools.generate_music_prompt(
            req.params.get("genre", "electronic"),
            req.params.get("mood", "energetic"),
            req.params.get("tempo", 120)
        ),
        "video": lambda: tools.generate_video_prompt(
            req.params.get("concept", "product reveal"),
            req.params.get("style", "cinematic"),
            req.params.get("duration", "30s")
        ),
        "image": lambda: tools.generate_image_prompt(
            req.params.get("subject", "landscape"),
            req.params.get("style", "photorealistic")
        ),
        "voice": lambda: tools.generate_voice_script(
            req.params.get("topic", "tech product"),
            req.params.get("duration", "30s"),
            req.params.get("tone", "professional")
        )
    }
    
    if req.prompt_type not in handlers:
        raise HTTPException(400, f"Unknown prompt type: {req.prompt_type}")
    
    result = await handlers[req.prompt_type]()
    return {"type": req.prompt_type, "result": result}

@app.post("/api/speak")
async def speak_text(text: str, voice: str = "Samantha", rate: int = 180):
    """Trigger local TTS"""
    tools.speak_async(text, voice, rate)
    return {"status": "speaking"}


# --- THE HOT ROD ENGINE ---

@app.websocket("/ws/gabriel_turbo")
async def gabriel_turbo_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("⚡ GABRIEL SUPERCHARGED: CLIENT CONNECTED")

    if not API_KEY:
        await websocket.send_json({"type": "error", "message": "NO API KEY"})
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
                try:
                    while True:
                        raw_msg = await websocket.receive_text()
                        msg = json.loads(raw_msg)
                        
                        if msg["type"] == "audio":
                            audio_bytes = base64.b64decode(msg["data"])
                            await session.send_input({"data": audio_bytes, "mime_type": "audio/pcm"})
                        
                        elif msg["type"] == "image":
                            img_bytes = base64.b64decode(msg["data"])
                            await session.send_input({"data": img_bytes, "mime_type": "image/jpeg"})
                        
                        elif msg["type"] == "text":
                            # Handle text commands
                            await session.send_text(msg["content"])
                            
                except WebSocketDisconnect:
                    logger.warning("🔴 CLIENT DISCONNECTED")
                except Exception as e:
                    logger.error(f"⚠️ UPSTREAM ERROR: {e}")

            async def downstream():
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
                                        await websocket.send_json({"type": "audio", "data": b64_audio})
                                    
                                    if part.text:
                                        await websocket.send_json({"type": "text", "data": part.text})
                                        # Save to memory
                                        tools.save_memory(
                                            part.text, 
                                            ["conversation"], 
                                            "ai_response"
                                        )

                except Exception as e:
                    logger.error(f"⚠️ DOWNSTREAM ERROR: {e}")

            await asyncio.gather(upstream(), downstream())

    except ImportError as e:
        logger.error(f"❌ IMPORT ERROR: {e}")
        await _fallback_handler(websocket)
    except Exception as e:
        logger.critical(f"❌ ENGINE ERROR: {e}")
        await websocket.close()


async def _fallback_handler(websocket: WebSocket):
    """Fallback to standard Gemini API"""
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "text":
                prompt = data.get("content", "")
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nUSER: {prompt}")
                
                await websocket.send_json({
                    "type": "response",
                    "content": response.text
                })
                
                tools.save_memory(
                    f"Q: {prompt}\nA: {response.text}",
                    ["conversation"],
                    "conversation"
                )
                
    except Exception as e:
        logger.error(f"Fallback error: {e}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
