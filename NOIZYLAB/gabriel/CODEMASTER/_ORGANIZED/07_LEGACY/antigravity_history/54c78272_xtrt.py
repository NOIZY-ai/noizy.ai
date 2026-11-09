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

if __name__ == "__main__":
    # Host 0.0.0.0 is critical for LAN access
    print("⚡ DREAMCHAMBER AGENT STARTING ON PORT 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
