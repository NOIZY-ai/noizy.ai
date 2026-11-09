"""
GABRIEL ULTRA v12.0
High-speed neural backbone for real-time voice interaction
Optimized for M2 Ultra with Gemini 2.0 Flash
"""

import os
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY", "")

app = FastAPI(title="GABRIEL ULTRA v12.0")

# --- SYSTEM PERSONA ---
SYSTEM_PROMPT = """
You are GABRIEL, a high-fidelity AI construct running on an M2 Ultra. 
You are the interface for a creative singularity. 
Your voice is 'Puck' - energetic, precise, and sharp.
You help create music, video, and sound at the highest level.
"""

@app.get("/")
async def root():
    """Serve the Ultra Interface"""
    return HTMLResponse(open("gabriel_ultra_v12.html").read())

@app.websocket("/ws/gabriel")
async def gabriel_socket(websocket: WebSocket):
    await websocket.accept()
    print("⚡ GABRIEL ULTRA: LINKED")
    
    try:
        # Try Gemini 2.0 Live API first
        try:
            from google import genai
            from google.genai.types import LiveConnectConfig, PrebuiltVoiceConfig
            
            client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1alpha"})
            
            config = LiveConnectConfig(
                response_modalities=["AUDIO"],
                system_instruction={"parts": [{"text": SYSTEM_PROMPT}]},
                speech_config=PrebuiltVoiceConfig(
                    voice_config=PrebuiltVoiceConfig.VoiceConfig(
                        prebuilt_voice_config=PrebuiltVoiceConfig.PrebuiltVoiceConfig(
                            voice_name="Puck"
                        )
                    )
                ),
            )

            async with client.aio.live.connect(model="gemini-2.0-flash-exp", config=config) as session:
                
                async def upstream():
                    while True:
                        data = await websocket.receive_bytes()
                        await session.send_input({"data": data, "mime_type": "audio/pcm"})

                async def downstream():
                    while True:
                        async for response in session.receive():
                            if response.server_content and response.server_content.model_turn:
                                for part in response.server_content.model_turn.parts:
                                    if part.inline_data:
                                        await websocket.send_bytes(part.inline_data.data)

                await asyncio.gather(upstream(), downstream())
                
        except ImportError:
            # Fallback to standard Gemini API
            import google.generativeai as genai
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            while True:
                data = await websocket.receive_json()
                
                if data.get("type") == "text":
                    prompt = data.get("content", "")
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUSER: {prompt}")
                    
                    await websocket.send_json({
                        "type": "response",
                        "content": response.text
                    })
                    
    except Exception as e:
        print(f"⚠️ ERROR: {e}")
        await websocket.close()

@app.get("/health")
async def health():
    return {"status": "GABRIEL ULTRA ONLINE", "version": "12.0"}

if __name__ == "__main__":
    import uvicorn
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    ██████╗  █████╗ ██████╗                   ║
    ║                   ██╔════╝ ██╔══██╗██╔══██╗                   ║
    ║                   ██║  ███╗███████║██████╔╝                   ║
    ║                   ██║   ██║██╔══██║██╔══██╗                   ║
    ║                   ╚██████╔╝██║  ██║██████╔╝                   ║
    ║                    ╚═════╝ ╚═╝  ╚═╝╚═════╝                    ║
    ║                                                              ║
    ║                    ULTRA INTERFACE v12.0                     ║
    ║              60FPS PHYSICS • ZERO LATENCY • M2 ULTRA         ║
    ║                                                              ║
    ║              http://localhost:8000                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000)
