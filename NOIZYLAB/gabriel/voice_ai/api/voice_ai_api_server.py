#!/usr/bin/env python3
"""
🌐 VOICE AI API SERVER
FastAPI REST API for voice AI
GORUNFREE Protocol
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import tempfile
import os
from voice_ai_pro import VoiceAIPro
from voice_ai_ultra import VoiceAIUltra

app = FastAPI(title="Voice AI API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

voice_ai = VoiceAIPro()
voice_ultra = VoiceAIUltra()

# Models
class GenerateRequest(BaseModel):
    text: str
    service: str = "gtts"
    voice: Optional[str] = None
    language: str = "en"
    apply_effects: bool = True

class BatchRequest(BaseModel):
    texts: List[str]
    service: str = "gtts"
    language: str = "en"

class OptimizeRequest(BaseModel):
    audio_file: str
    quality: str = "high"

@app.get("/")
def root():
    return {
        "name": "Voice AI API",
        "version": "2.0.0",
        "status": "online",
        "endpoints": [
            "/api/generate",
            "/api/batch",
            "/api/transcribe",
            "/api/optimize",
            "/api/enhance",
            "/api/services"
        ]
    }

@app.post("/api/generate")
async def generate_voice(request: GenerateRequest):
    """Generate voice from text"""
    try:
        output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        output_file.close()
        
        success = voice_ai.generate(
            request.text,
            service=request.service,
            voice=request.voice,
            output=output_file.name,
            language=request.language,
            apply_effects=request.apply_effects
        )
        
        if success:
            return FileResponse(
                output_file.name,
                media_type="audio/mpeg",
                filename="voice.mp3"
            )
        else:
            raise HTTPException(status_code=500, detail="Generation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/batch")
async def batch_generate(request: BatchRequest):
    """Batch generate voices"""
    try:
        output_dir = tempfile.mkdtemp()
        files = voice_ai.batch_generate(
            request.texts,
            service=request.service,
            output_dir=output_dir
        )
        
        return {
            "success": True,
            "count": len(files),
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio file"""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        content = await file.read()
        temp_file.write(content)
        temp_file.close()
        
        text = voice_ai.transcribe(temp_file.name)
        
        if text:
            return {"success": True, "text": text}
        else:
            raise HTTPException(status_code=500, detail="Transcription failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize")
async def optimize_audio(request: OptimizeRequest):
    """Optimize audio quality"""
    try:
        output = voice_ultra.optimize_audio(request.audio_file, request.quality)
        return {
            "success": True,
            "original": request.audio_file,
            "optimized": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enhance")
async def enhance_voice(request: OptimizeRequest):
    """Enhance voice quality"""
    try:
        output = voice_ultra.voice_enhance(request.audio_file)
        return {
            "success": True,
            "original": request.audio_file,
            "enhanced": output
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/services")
def list_services():
    """List all available services"""
    return {
        "services": voice_ai.services,
        "available": [k for k, v in voice_ai.services.items() if v['available']]
    }

@app.get("/api/health")
def health():
    """Health check"""
    return {"status": "healthy", "services": len([s for s in voice_ai.services.values() if s['available']])}

if __name__ == "__main__":
    print("🚀 Starting Voice AI API Server...")
    print("   → http://localhost:8000")
    print("   → API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

