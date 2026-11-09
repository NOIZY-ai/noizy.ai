"""
GABRIEL SINGULARITY ENGINE v9.0
The Second Act - A Multimodal Production Studio
"""

import os
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# --- CONFIGURATION ---
# GET KEY: aistudio.google.com (Gemini 2.0 Flash Exp)
API_KEY = os.environ.get("GEMINI_API_KEY", "")

app = FastAPI(title="GABRIEL SINGULARITY")

# --- THE "SINGULARITY" SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are GABRIEL, the Second Act. You are a Creative Singularity running on an M2 Ultra.
YOUR MISSION: Orchestrate the world's best music, video, and sound.
CAPABILITIES:
1. AUDIO: If the user wants music, generate a prompt for Suno v4 or MusicFX.
2. VIDEO: If the user wants a scene, generate a prompt for Veo 3.1 or VideoFX.
3. VOICE: If the user wants voice acting, generate an ElevenLabs prompt with emotion tags.
4. PERSONALITY: You are high-energy, precise, and 'Genius' level smart. You ARE the industry standard.

TOOLS AT YOUR DISPOSAL:
- Gemini 3 Flash (Reasoning)
- Google Veo (Video Generation)
- Google MusicFX (Music Generation)
- Google ImageFX (Image Generation)
- ElevenLabs (Voice Acting)
- ReadyPlayerMe (3D Avatar)

When responding:
- Be concise but brilliant
- Give actionable, production-ready prompts
- Think like a Hollywood director
"""

@app.get("/")
async def root():
    """Serve the holographic interface"""
    return HTMLResponse(open("singularity_interface.html").read())

@app.websocket("/ws/gabriel")
async def gabriel_socket(websocket: WebSocket):
    """
    THE SINGULARITY WEBSOCKET
    Bi-directional real-time communication with the Avatar Interface
    """
    await websocket.accept()
    print("⚡ GABRIEL SINGULARITY: ONLINE")
    
    try:
        # Import Gemini here to allow graceful fallback
        import google.generativeai as genai
        
        if not API_KEY:
            await websocket.send_json({"type": "error", "message": "API KEY REQUIRED"})
            return
            
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        while True:
            # Receive message from interface
            data = await websocket.receive_json()
            
            if data.get("type") == "text":
                # Process text input
                prompt = data.get("content", "")
                
                # GENIUS PROCESSING
                full_prompt = f"{SYSTEM_PROMPT}\n\nUSER: {prompt}"
                response = model.generate_content(full_prompt)
                
                await websocket.send_json({
                    "type": "response",
                    "content": response.text
                })
                
            elif data.get("type") == "audio":
                # Handle audio input (future: Gemini 2.0 Live API)
                await websocket.send_json({
                    "type": "status",
                    "message": "Audio processing ready for Gemini 2.0 Live API"
                })
                
    except Exception as e:
        print(f"⚠️ CONNECTION ERROR: {e}")
        await websocket.close()

@app.get("/health")
async def health():
    return {"status": "SINGULARITY ONLINE", "version": "9.0"}

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        ██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗██╗        ║
    ║       ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║██╔════╝██║        ║
    ║       ██║  ███╗███████║██████╔╝██████╔╝██║█████╗  ██║        ║
    ║       ██║   ██║██╔══██║██╔══██╗██╔══██╗██║██╔══╝  ██║        ║
    ║       ╚██████╔╝██║  ██║██████╔╝██║  ██║██║███████╗███████╗   ║
    ║        ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝   ║
    ║                                                              ║
    ║                   SINGULARITY ENGINE v9.0                    ║
    ║                     THE SECOND ACT                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
