#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
🏢 NOIZYVOX UNIFIED AGENCY (V16)
The Central "Brain" that manages multiple AI Voice Actors across environments.
"""

import os, json, asyncio, subprocess, sys
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY") # User must set this
XTTS_PYTHON = "/Users/m2ultra/NOIZYLAB/GABRIEL/xtts_venv/bin/python3"
XTTS_RUNNER = "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/xtts_runner.py"

if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)
# ElevenLabs client init
client_el = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None

class Agent:
    def __init__(self, name, description, capabilities):
        self.name = name
        self.description = description
        self.capabilities = capabilities 

    async def speak(self, text, emotion="neutral"):
        raise NotImplementedError

class GabrielAgent(Agent):
    """The Resident Polyglot Scholar (EdgeTTS)"""
    def __init__(self):
        super().__init__("Gabriel", "A weathered 50yo Brazilian scholar. Intellectual, poetic, deep.", ["emotional", "multilingual", "sfx"])
        
    async def speak(self, text, emotion="neutral"):
        print(f"[GABRIEL] Speaking: {text}")
        # Call V15 Server
        cmd = f"curl -s 'http://localhost:5176/speak?text={text}&emotion={emotion}&director=true'"
        subprocess.run(cmd, shell=True)
        return "gabriel_output_simulated.mp3"

class RivaAgent(Agent):
    """ElevenLabs Premium (High Quality)"""
    def __init__(self):
        super().__init__("Riva", "Standard American Neutral. Professional, newscaster, assistant.", ["pro", "clean", "expensive"])
        
    async def speak(self, text, emotion="neutral"):
        print(f"[RIVA] Speaking (ElevenLabs): {text}")
        if not client_el:
            print("   ⚠️ No ELEVENLABS_API_KEY found. Falling back to system voice.")
            subprocess.run(["say", "-v", "Samantha", text])
            return "fallback.wav"
        
        try:
            # Using 'Rachel' or similar broadcast voice
            audio = client_el.generate(
                text=text,
                voice="Rachel", 
                model="eleven_monolingual_v1"
            )
            save(audio, "riva_output.mp3")
            subprocess.run(["afplay", "riva_output.mp3"])
            return "riva_output.mp3"
        except Exception as e:
            print(f"   ⚠️ ElevenLabs Error: {e}")
            subprocess.run(["say", "-v", "Samantha", text])
            return "error.wav"

class JamieAgent(Agent):
    """Custom Cloned Voice (XTTS Local)"""
    def __init__(self):
        super().__init__("Jamie", "Young, energetic, casual. 20s American.", ["emotional", "cloned", "local"])
        self.ref_wav = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_ref.wav" # Needs a real ref file
        
    async def speak(self, text, emotion="neutral"):
        print(f"[JAMIE] Speaking (XTTS): {text}")
        out_file = "jamie_latest.wav"
        
        # Call the isolated XTTS runner
        cmd = [
            XTTS_PYTHON, XTTS_RUNNER,
            "--text", text,
            "--ref", self.ref_wav,
            "--out", out_file,
            "--lang", "en"
        ]
        
        # Check if ref exists, else mock it
        if not os.path.exists(self.ref_wav):
            print("   ⚠️ Reference audio missing. Recording mock ref...")
            # Ideally we'd have a file. For now, we mock or fail gracefully.
            # subprocess.run(["say", "-v", "Jamie", "-o", self.ref_wav, "Reference audio"]) 
            print("   ⚠️ Cannot run XTTS without reference audio.")
            subprocess.run(["say", "-v", "Junior", text])
            return "fallback.wav"

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        
        if process.returncode == 0:
            print(f"   ✅ Generated: {out_file}")
            subprocess.run(["afplay", out_file])
            return out_file
        else:
            print(f"   ❌ XTTS Failed: {err.decode()}")
            subprocess.run(["say", "-v", "Junior", text])
            return "error.wav"

class Agency:
    def __init__(self):
        self.agents = [GabrielAgent(), RivaAgent(), JamieAgent()]
        self.director_model = genai.GenerativeModel('gemini-pro')

    def cast_actor(self, text):
        if not GEMINI_API_KEY: 
            print("   ⚠️ No GEMINI_API_KEY found. Defaulting to Gabriel.")
            return self.agents[0] 

        prompt = f"""
        CASTING DIRECTOR: Who should speak this line?
        
        Line: "{text}"
        
        Agents:
        1. Gabriel: Weathered scholar, poetic, deep. (Best for: Theory, Philosophy, Dark, Storytelling)
        2. Riva: Professional newscaster, neutral, clear. (Best for: News, Facts, Alerts, Official)
        3. Jamie: Young, energetic, casual, friend. (Best for: Hype, Slang, Chat, Greeting)
        
        Output JSON: {{"agent": "Gabriel" | "Riva" | "Jamie", "reason": "..."}}
        """
        
        try:
            resp = self.director_model.generate_content(prompt)
            data = json.loads(resp.text.replace('```json','').replace('```','').strip())
            name = data.get("agent", "Gabriel")
            
            for a in self.agents:
                if a.name == name:
                    print(f"🎬 CASTING: {name} because {data.get('reason')}")
                    return a
            print(f"   ⚠️ Agent '{name}' not found. Defaulting to Gabriel.")
            return self.agents[0]
        except Exception as e:
            print(f"   ⚠️ Casting Error: {e}")
            return self.agents[0]

    async def direct(self, text):
        actor = self.cast_actor(text)
        await actor.speak(text)

async def main():
    agency = Agency()
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = "The agency is now online. We have full control."
        
    await agency.direct(text)

if __name__ == "__main__":
    import sys
    asyncio.run(main())
