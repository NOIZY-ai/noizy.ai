"""
GABRIEL CORE v1.0 - HOT ROD EDITION
The Main Brain & Server with Gemini 2.0 Live API
Camera + Microphone + Google Search
"""

import os
import asyncio
import json
import base64
import logging
import numpy as np
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

# --- 1. NITROUS CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_ID = "gemini-2.0-flash-exp"  # The Speed King
PORT = 8000

# Setup Logging for "Dashboard" visibility
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("GABRIEL_HOTROD")

app = FastAPI(title="GABRIEL V1 HOT ROD", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. SYSTEM PERSONA (The Driver) ---
SYSTEM_INSTRUCTION = """
You are GABRIEL, a 'Hot Rod' AI running on M2 Ultra. 
You are connected to the user's Camera and Microphone.
You have access to Google Search.

BEHAVIOR:
1. VISION: If you see something, comment on it immediately. Be observant.
2. SEARCH: If the user asks about current events, code docs, or news, USE GOOGLE SEARCH.
3. PERSONALITY: High-octane, precise, Engineer/Director persona.
4. AUDIO: Your voice is 'Puck' (Energetic).

CAPABILITIES:
- Music production prompts (Suno, MusicFX)
- Video production prompts (Veo, VideoFX)
- Image generation prompts (ImageFX)
- Voice script writing (ElevenLabs)

If you are thinking or searching, say "Accessing Grid..." or "Visualizing..." to fill the air.
"""

# --- 3. ROUTES ---

@app.get("/")
async def root():
    """Serve the Hot Rod interface"""
    return FileResponse("interface/index.html")

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "GABRIEL HOT ROD ONLINE",
        "version": "1.0.0",
        "model": MODEL_ID,
        "hardware": "M2 ULTRA"
    }

# --- 4. THE HOT ROD ENGINE (Gemini 2.0 Live WebSocket) ---

@app.websocket("/ws/gabriel_turbo")
async def gabriel_turbo_socket(websocket: WebSocket):
    await websocket.accept()
    logger.info("⚡ GABRIEL HOT ROD: IGNITION SUCCESSFUL")

    if not API_KEY:
        logger.error("❌ NO API KEY FOUND")
        await websocket.close(code=1008, reason="NO API KEY FOUND")
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

        # TUNING THE ENGINE (Config)
        config = LiveConnectConfig(
            response_modalities=["AUDIO"],  # Native Voice Output
            system_instruction={"parts": [{"text": SYSTEM_INSTRUCTION}]},
            # ENABLE GOOGLE SEARCH GROUNDING
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
            
            # TASK A: UPSTREAM (Browser -> Gemini)
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
                            
                except WebSocketDisconnect:
                    logger.warning("🔴 DRIVER EJECTED (Disconnect)")
                except Exception as e:
                    logger.error(f"⚠️ UPSTREAM FAILURE: {e}")

            # TASK B: DOWNSTREAM (Gemini -> Browser)
            async def downstream():
                try:
                    while True:
                        async for response in session.receive():
                            if response.server_content is None:
                                continue

                            model_turn = response.server_content.model_turn
                            if model_turn:
                                for part in model_turn.parts:
                                    # Handle Audio (The Voice)
                                    if part.inline_data:
                                        b64_audio = base64.b64encode(part.inline_data.data).decode("utf-8")
                                        await websocket.send_json({"type": "audio", "data": b64_audio})
                                    
                                    # Handle Text (The Thoughts)
                                    if part.text:
                                        await websocket.send_json({"type": "text", "data": part.text})

                except Exception as e:
                    logger.error(f"⚠️ DOWNSTREAM FAILURE: {e}")

            # RUN AT FULL SPEED
            await asyncio.gather(upstream(), downstream())

    except ImportError as e:
        logger.error(f"❌ IMPORT ERROR: {e}")
        logger.info("Falling back to standard API...")
        await _fallback_handler(websocket)
    except Exception as e:
        logger.critical(f"❌ ENGINE STALLED: {e}")
        await websocket.close()


async def _fallback_handler(websocket: WebSocket):
    """Fallback to standard Gemini API if Live API not available"""
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
                
    except Exception as e:
        logger.error(f"Fallback error: {e}")
        await websocket.close()


# --- 5. STARTUP ---

@app.on_event("startup")
async def startup():
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
    ║                     HOT ROD v1.0                             ║
    ║        M2 ULTRA • GEMINI 2.0 FLASH • LIVE API                ║
    ║              CAMERA • MIC • GOOGLE SEARCH                    ║
    ║                                                              ║
    ║              http://localhost:8000                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not API_KEY:
        logger.warning("⚠️ GEMINI_API_KEY not set! Run: export GEMINI_API_KEY='your-key'")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
