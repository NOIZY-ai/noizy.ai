
# ============================================================================
# GABRIEL SERVER (API GATEWAY)
# ============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gabriel_brain import GabrielBrain
import uvicorn
import os

app = FastAPI(title="Gabriel API", version="1.0")

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

@app.on_event("startup")
async def startup_event():
    brain.wake_up()

@app.get("/")
def read_root():
    return {"name": "Gabriel API", "status": "ONLINE"}

@app.get("/status")
def get_status():
    return brain.get_status()

@app.post("/interact")
def interact(request: InteractionRequest):
    return brain.process_input(request.text)

if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible on network
    uvicorn.run(app, host="0.0.0.0", port=8000)
