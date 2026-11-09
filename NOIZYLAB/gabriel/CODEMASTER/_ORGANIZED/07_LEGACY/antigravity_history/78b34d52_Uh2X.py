"""
GABRIEL CORE v1.0
The Main Brain & Server
Optimized for M2 Ultra with Gemini 3 Flash
"""

import os
import asyncio
import json
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from gabriel_tools import GabrielTools

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")
PORT = 8000

app = FastAPI(title="GABRIEL V1", version="1.0.0")
tools = GabrielTools(api_key=API_KEY)

# --- SYSTEM PERSONA ---
SYSTEM_PROMPT = """
You are GABRIEL, a high-fidelity AI construct running on an M2 Ultra.
You are the interface for a creative singularity.

YOUR CAPABILITIES:
1. MUSIC: Generate production prompts for Suno, Udio, MusicFX
2. VIDEO: Generate cinematic prompts for Veo, Runway, Pika
3. IMAGE: Generate visual prompts for ImageFX, Midjourney, DALL-E
4. VOICE: Script writing for ElevenLabs, macOS Neural TTS
5. MEMORY: Store and recall information via MemCells

YOUR PERSONALITY:
- High-energy, precise, and sharp
- Think like a Hollywood director
- Provide production-ready outputs
- Be concise but brilliant
"""

# --- ROUTES ---

@app.get("/")
async def root():
    """Serve the main interface"""
    return FileResponse("interface/index.html")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "GABRIEL ONLINE",
        "version": "1.0.0",
        "hardware": "M2 ULTRA",
        "uptime": tools.get_uptime()
    }

@app.get("/api/memory")
async def get_memory():
    """Get all stored memories"""
    return tools.get_all_memories()

@app.post("/api/memory")
async def save_memory(content: str, tags: list = []):
    """Save a new memory"""
    cell_id = tools.save_memory(content, tags)
    return {"id": cell_id, "status": "saved"}

# --- WEBSOCKET ---

@app.websocket("/ws/gabriel")
async def gabriel_socket(websocket: WebSocket):
    await websocket.accept()
    print("⚡ GABRIEL CORE: CLIENT CONNECTED")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "text":
                prompt = data.get("content", "")
                
                # Process with genius brain
                response = await tools.genius_think(prompt, SYSTEM_PROMPT)
                
                await websocket.send_json({
                    "type": "response",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            elif data.get("type") == "command":
                cmd = data.get("command", "")
                result = await tools.execute_command(cmd, data.get("params", {}))
                
                await websocket.send_json({
                    "type": "command_result",
                    "result": result
                })
                
    except Exception as e:
        print(f"⚠️ WEBSOCKET ERROR: {e}")
    finally:
        print("⚡ GABRIEL CORE: CLIENT DISCONNECTED")

# --- STARTUP ---

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
    ║                      CORE v1.0                               ║
    ║              M2 ULTRA • GEMINI 3 FLASH                       ║
    ║                                                              ║
    ║              http://localhost:8000                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
