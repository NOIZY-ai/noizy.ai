# GABRIEL:AVATAR_DIRECTOR (v4)

**Goal**: 3D living avatar that is:

* **Low Latency**: <16ms frame budget.
* **Interruptible Duplex Voice**: Stop instantly on user audio.
* **State Machine Driven**: IDLE / LISTEN / THINK / SPEAK / ALERT / EXECUTE_CONFIRM.
* **Prosody -> Visemes**: Energy/pitch drive micro-expressions.
* **HUD**: Shows confidence + evidence + next action.

**Output JSON**:

```json
{
  "states": {
    "IDLE": "Breathing, presence, ready.",
    "LISTEN": "Eyes focused, ears active.",
    "THINK": "Processing, micro-expressions.",
    "SPEAK": "Lip sync + prosody gestures.",
    "ALERT": "Visual warning, focus shift.",
    "EXECUTE_CONFIRM": "Confident posture."
  },
  "rig_requirements": [
    "jawOpen", "mouthSmile", "eyebrowRaise", "pupilSize", "headTilt"
  ],
  "prosody_mapping": [
    { "source": "energy", "target": "jawOpen", "factor": 1.5 },
    { "source": "pitch", "target": "eyebrowRaise", "factor": 0.5 }
  ],
  "voice_pipeline": [
    "VAD (Deepgram)",
    "LLM (Claude/GPT-4o)",
    "TTS (ElevenLabs)",
    "FX (TempleEngine)"
  ],
  "hud": [
    "confidence_score",
    "evidence_source",
    "next_action_toast"
  ],
  "performance_budget": [
    "Frame: <16ms",
    "Voice Latency: <400ms",
    "Interrupt: <300ms"
  ],
  "implementation_steps": []
}
```
