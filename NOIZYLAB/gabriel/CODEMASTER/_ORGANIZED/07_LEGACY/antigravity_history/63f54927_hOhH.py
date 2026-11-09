
# ============================================================================
# GABRIEL SERVER (API GATEWAY)
# Version: 2.0 (Async / Zero Latency)
# ============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gabriel_brain import GabrielBrain
import uvicorn
import os

app = FastAPI(title="Gabriel API", version="2.0")

# CORS for local Avatar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brain = GabrielBrain()

class InteractionRequest(BaseModel):
    text: str

class InteractionResponse(BaseModel):
    response: str
    action: str | None = None
    timestamp: float

@app.on_event("startup")
async def startup_event():
    await brain.wake_up()

@app.get("/")
async def read_root():
    return {"name": "Gabriel API", "status": "ONLINE", "mode": "Async/Zero-Latency"}

@app.get("/status")
async def get_status():
    return brain.get_status()

@app.post("/interact", response_model=InteractionResponse)
async def interact(request: InteractionRequest):
    return await brain.process_input(request.text)

if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible on network
    # Workers=1 for now, but in prod we might increase
    uvicorn.run(app, host="0.0.0.0", port=8000)
