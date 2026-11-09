#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
🏢 NOIZYVOX UNIFIED AGENCY (V18: THE STAGE)
The Central "Brain" that manages multiple AI Voice Actors across environments.
Includes Auteur Mode (Emotion + SFX) and Visual UI Support.
"""

import os, json, asyncio, subprocess, sys, time
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# 📚 V18 SHARED UTILS
from agency_utils import process_audio_fx, EMOTION_MAP, SFX_MAP

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY") 
XTTS_PYTHON = "/Users/m2ultra/NOIZYLAB/GABRIEL/xtts_venv/bin/python3"
XTTS_RUNNER = "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/xtts_runner.py"
RVC_RUNNER = "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/rvc_runner.py"

if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)

# Try importing RVC directly for ZERO LATENCY (V21 Synapse)
RVC_IN_MEMORY = False
try:
    from rvc_python.infer import RVCInference
    RVC_IN_MEMORY = True
except ImportError:
    pass

class Agent:
    def __init__(self, name, description, capabilities):
        self.name = name
        self.description = description
        self.capabilities = capabilities 
        self.last_audio_path = None 

    async def speak(self, text, emotion="neutral", sfx="none"):
        raise NotImplementedError

class GabrielAgent(Agent):
    """The Resident Polyglot Scholar (EdgeTTS + RVC + DeepFilter)"""
    def __init__(self):
        super().__init__("Gabriel", "A weathered 50yo Brazilian scholar. Intellectual, poetic, deep.", ["deep_filter", "rvc", "sfx"])
        
        # V21: PRE-LOAD MODEL INTO MEMORY (The Synapse)
        self.rvc_engine = None
        self.model_path = os.environ.get("RVC_MODEL_PATH", "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/models/gabriel_rvc.pth")
        
        if RVC_IN_MEMORY and os.path.exists(self.model_path):
            try:
                print(f"[GABRIEL] 🧠 Loading RVC Memory Synapse: {os.path.basename(self.model_path)}")
                # Initialize implementation (MPS enabled)
                self.rvc_engine = RVCInference(device="mps", model_path=self.model_path)
            except Exception as e:
                print(f"[GABRIEL] ⚠️ Memory Load Failed: {e}")
        
    async def speak(self, text, emotion="neutral", sfx="none"):
        print(f"[GABRIEL] Speaking: {text} | Emo: {emotion} | SFX: {sfx}")
        base_file = "gabriel_base.mp3"
        
        # 1. Generate Base Audio (EdgeTTS)
        voice = "en-GB-RyanNeural" 
        cmd_tts = f"edge-tts --text '{text}' --write-media {base_file} --voice {voice}"
        subprocess.run(cmd_tts, shell=True)
        
        # 2. RVC Conversion
        current_file = base_file
        rvc_out = "gabriel_rvc.wav"
        
        # CHECK: Use In-Memory Engine (Zero Latency) or Fallback?
        if self.rvc_engine:
            try:
                print(f"[GABRIEL] ⚡ Synapse Fire (In-Memory Inference)...")
                self.rvc_engine.set_params(f0up_key=-12, f0method="harvest", index_rate=0.5, protect=0.33)
                self.rvc_engine.infer_file(current_file, rvc_out)
                current_file = rvc_out
            except Exception as e:
                print(f"[GABRIEL] ❌ Synapse Error: {e}")
                
        elif os.path.exists(self.model_path): # Fallback to CLI if memory load failed
             print(f"[GABRIEL] 🐢 Slow-Path (Subprocess)...")
             cmd_rvc = [XTTS_PYTHON, RVC_RUNNER, "--input", current_file, "--model", self.model_path, "--out", rvc_out, "--pitch", "-12"]
             if subprocess.run(cmd_rvc).returncode == 0:
                 current_file = rvc_out
        
        # 3. Auteur FX (Emotion + SFX Post-Processing)
        post_processed_file = "gabriel_final.mp3"
        process_audio_fx(current_file, post_processed_file, emotion, sfx)
        
        # Playback
        subprocess.run(["afplay", post_processed_file])
        self.last_audio_path = post_processed_file
        return post_processed_file

class RivaAgent(Agent):
    """ElevenLabs Premium (High Quality + SFX)"""
    def __init__(self):
        super().__init__("Riva", "Standard American Neutral. Professional, newscaster, assistant.", ["elevenlabs", "premium", "mixed"])
        
    async def speak(self, text, emotion="neutral", sfx="none"):
        print(f"[RIVA] Speaking (ElevenLabs): {text}")
        if not client_el:
            fallback = "fallback.wav"
            subprocess.run(["say", "-v", "Samantha", "-o", fallback, text])
            subprocess.run(["afplay", fallback])
            return fallback

        try:
            # Generate clean audio
            audio = client_el.generate(text=text, voice="Rachel", model="eleven_monolingual_v1")
            base_file = "riva_base.mp3"
            save(audio, base_file)
            
            # Apply SFX if requested
            final_file = "riva_final.mp3"
            process_audio_fx(base_file, final_file, "neutral", sfx) # Neutral EQ for Riva, she's perfect already
            
            subprocess.run(["afplay", final_file])
            self.last_audio_path = final_file
            return final_file
        except Exception as e:
            print(f"   ⚠️ ElevenLabs Error: {e}")
            subprocess.run(["say", "-v", "Samantha", text])
            return "error.wav"

class JamieAgent(Agent):
    """Custom Cloned Voice (XTTS + SFX)"""
    def __init__(self):
        super().__init__("Jamie", "Young, energetic, casual. 20s American.", ["cloned", "local", "emotional"])
        self.ref_wav = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_ref.wav"
        
    async def speak(self, text, emotion="neutral", sfx="none"):
        print(f"[JAMIE] Speaking (XTTS): {text}")
        out_file = "jamie_latest.wav"
        
        cmd = [XTTS_PYTHON, XTTS_RUNNER, "--text", text, "--ref", self.ref_wav, "--out", out_file, "--lang", "en"]
        
        if not os.path.exists(self.ref_wav):
            subprocess.run(["say", "-v", "Junior", text])
            return "fallback.wav"

        process = subprocess.run(cmd, capture_output=True)
        if process.returncode == 0:
            final_file = "jamie_final.wav"
            # XTTS is already emotional, but we can add SFX
            process_audio_fx(out_file, final_file, "neutral", sfx)
            subprocess.run(["afplay", final_file])
            self.last_audio_path = final_file
            return final_file
        else:
            subprocess.run(["say", "-v", "Junior", text])
            return "error.wav"

class Agency:
    def __init__(self):
        self.agents = [GabrielAgent(), RivaAgent(), JamieAgent()]
        self.director_model = genai.GenerativeModel('gemini-flash-latest')

    def cast_actor(self, text, force_agent=None):
        """
        Gemini decides who speaks, how they speak, and the atmosphere (SFX).
        """
        if force_agent:
            # If UI forces an agent, we still might want emotion/sfx analysis?
            # For now, simplistic fallback if forced.
            found = next((a for a in self.agents if a.name == force_agent), self.agents[0])
            return found, "neutral", "none", "User Override"

        if not GEMINI_API_KEY: 
            return self.agents[0], "neutral", "none", "No Gemini Key"

        prompt = f"""
        CASTING DIRECTOR & AUTEUR: Analyze this line.
        
        Line: "{text}"
        
        1. Select Agent:
           - Gabriel: Philosophical, Poetic, Dark.
           - Riva: News, Professional, Neutral.
           - Jamie: Casual, Slang, Hype.
           
        2. Detect Emotion (joy, sadness, anger, fear, whisper, god, neutral).
        
        3. Suggest SFX (rain, thunder, city, jazz, none). ONLY if context suggests it creates atmosphere.
        
        Output JSON: {{"agent": "Name", "reason": "...", "emotion": "...", "sfx": "..."}}
        """
        
        try:
            resp = self.director_model.generate_content(prompt)
            data = json.loads(resp.text.replace('```json','').replace('```','').strip())
            name = data.get("agent", "Gabriel")
            emotion = data.get("emotion", "neutral")
            sfx = data.get("sfx", "none")
            reason = data.get("reason", "AI Decision")
            
            found_agent = next((a for a in self.agents if a.name == name), self.agents[0])
            print(f"🎬 CASTING: {found_agent.name} | Emo: {emotion} | SFX: {sfx} | Why: {reason}")
            return found_agent, emotion, sfx, reason
            
        except Exception as e:
            print(f"   ⚠️ Casting Error: {e}")
            return self.agents[0], "neutral", "none", f"Error: {e}"

    async def direct(self, text):
        actor, emotion, sfx, _ = self.cast_actor(text)
        await actor.speak(text, emotion, sfx)

async def main():
    agency = Agency()
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = "The agency is now upgraded. V 18 is online."
        
    await agency.direct(text)

if __name__ == "__main__":
    import sys
    asyncio.run(main())
