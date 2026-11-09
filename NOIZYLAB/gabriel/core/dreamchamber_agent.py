import platform
import psutil
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DreamChamber Agent", version="1.0")

# Enable CORS for Mac Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"system": "DreamChamber", "status": "ONLINE", "lifeluv": "LINKED"}

@app.get("/status")
def get_status():
    mem = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": mem.percent,
        "memory_used_gb": round(mem.used / (1024**3), 1),
        "memory_total_gb": round(mem.total / (1024**3), 1),
        "os": platform.system(),
        "node": platform.node()
    }

@app.post("/speak")
def speak(payload: dict):
    # Uses Windows PowerShell TTS
    text = payload.get("text", "System Online")
    cmd = f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{text}")'
    import subprocess
    subprocess.Popen(["powershell", "-c", cmd])
    return {"status": "speaking", "text": text}

@app.post("/launch")
def launch_app(payload: dict):
    # Launch generic apps or URLs
    target = payload.get("target", "")
    if not target: return {"error": "No target specified"}
    
    import os
    try:
        os.startfile(target)
        return {"status": "launched", "target": target}
    except Exception as e:
        return {"error": str(e)}

@app.get("/clipboard")
def get_clipboard():
    # Read Windows Clipboard via PowerShell
    import subprocess
    try:
        cmd = "powershell -command Get-Clipboard"
        text = subprocess.check_output(cmd, shell=True).decode().strip()
        return {"content": text}
    except Exception as e:
        return {"error": str(e)}

@app.post("/clipboard")
def set_clipboard(payload: dict):
    # Set Windows Clipboard via PowerShell
    text = payload.get("content", "")
    import subprocess
    try:
        # Escape quotes for PowerShell
        safe_text = text.replace('"', '\\"')
        cmd = f'powershell -command Set-Clipboard -Value "{safe_text}"'
        subprocess.call(cmd, shell=True)
        return {"status": "copied", "content": text[:50] + "..."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Host 0.0.0.0 is critical for LAN access
    print("⚡ DREAMCHAMBER ACTIVE CONTROL NODE STARTING ON PORT 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
