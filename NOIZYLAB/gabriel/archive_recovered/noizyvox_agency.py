#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
🏢 NOIZYVOX AGENCY ROUTER (V16)
The Central "Brain" that manages multiple AI Voice Actors.
"""

import os, json, asyncio, subprocess, sys
import google.generativeai as genai

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)

class Agent:
    def __init__(self, name, description, capabilities):
        self.name = name
        self.description = description
        self.capabilities = capabilities # ["emotional", "fast", "multilingual"]

    async def speak(self, text, emotion="neutral"):
        raise NotImplementedError

class GabrielAgent(Agent):
    """The Resident Polyglot Scholar (EdgeTTS)"""
    def __init__(self):
        super().__init__("Gabriel", "A weathered 50yo Brazilian scholar. Intellectual, poetic, deep.", ["emotional", "multilingual", "sfx"])
        
    async def speak(self, text, emotion="neutral"):
        # We call the existing gabriel_voice.py logic (simulated import or direct call)
        # For now, we just shell out to the running server for reliability
        cmd = f"curl -s 'http://localhost:5176/speak?text={text}&emotion={emotion}&director=true'"
        subprocess.run(cmd, shell=True)
        return "gabriel_output_simulated.mp3"

class RivaAgent(Agent):
    """NVIDIA Riva - Broadcast Quality"""
    def __init__(self):
        super().__init__("Riva", "Standard American Neutral. Professional, newscaster, assistant.", ["fast", "clean"])
        
    async def speak(self, text, emotion="neutral"):
        # Placeholder for NVIDIA Riva Client
        print(f"[RIVA] Speaking: {text}")
        subprocess.run(["say", "-v", "Samantha", text]) # Fallback for now
        return "riva_output.wav"

class JamieAgent(Agent):
    """Custom Cloned Voice"""
    def __init__(self):
        super().__init__("Jamie", "Young, energetic, casual. 20s American.", ["emotional", "cloned"])
        
    async def speak(self, text, emotion="neutral"):
        # Check if trained model exists
        print(f"[JAMIE] Speaking: {text}")
        subprocess.run(["say", "-v", "Jamie (Premium)", text]) # Fallback until XTTS trained
        return "jamie_output.wav"

class Agency:
    def __init__(self):
        self.agents = [GabrielAgent(), RivaAgent(), JamieAgent()]
        self.director_model = genai.GenerativeModel('gemini-1.5-flash')

    def cast_actor(self, text):
        """
        Gemini decides who should speak this line.
        """
        if not GEMINI_API_KEY: return self.agents[0] # Default to Gabriel

        prompt = f"""
        CASTING DIRECTOR: Who should speak this line?
        
        Line: "{text}"
        
        Agents:
        1. Gabriel: Weathered scholar, poetic, deep, poetic. (Best for: Theory, Philosophy, Dark)
        2. Riva: Professional newscaster, assistant, neutral. (Best for: News, Facts, alerts)
        3. Jamie: Young, energetic, casual, friend. (Best for: Hype, slang, chat)
        
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
            return self.agents[0]
        except:
            return self.agents[0]

    async def direct(self, text):
        actor = self.cast_actor(text)
        await actor.speak(text)

async def main():
    agency = Agency()
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = "Welcome to the NoizyVox Agency. We are ready to serve."
        
    await agency.direct(text)

if __name__ == "__main__":
    import sys
    asyncio.run(main())
