#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
DR. GABRIEL ALMEIDA - OMEGA VOICE SYSTEM (V13)
Features: Gemini Director Mode (Humour/Sarcasm), Extended Vocal Range (Whisper/Shout), Polyglot
"""

import subprocess, asyncio, sys, json, os, hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from textblob import TextBlob
from nltk.corpus import wordnet as wn
import google.generativeai as genai

CHARACTER = {"name": "Dr. Gabriel Almeida", "style": "Polyglot Scholar"}
CACHE = "/tmp/almeida"; os.makedirs(CACHE, exist_ok=True)

# 🔑 GEMINI SETUP
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  GEMINI_API_KEY not found. Director Mode disabled.")

# 🌍 MULTILINGUAL VOICE MAP
VOICES = {
    "en":    {"id": "en-GB-RyanNeural",         "rate": "-8%", "pitch": "-4Hz"}, 
    "fr":    {"id": "fr-FR-RemyMultilingualNeural", "rate": "-5%", "pitch": "-2Hz"},
    "es":    {"id": "es-ES-AlvaroNeural",       "rate": "-5%", "pitch": "-2Hz"},
    "it":    {"id": "it-IT-GiuseppeMultilingualNeural", "rate": "-5%", "pitch": "-2Hz"},
    "ja":    {"id": "ja-JP-KeitaNeural",        "rate": "+0%", "pitch": "-2Hz"},
    "zh":    {"id": "zh-CN-YunjianNeural",      "rate": "+0%", "pitch": "-2Hz"},
    "zh-hk": {"id": "zh-HK-WanLungNeural",      "rate": "+0%", "pitch": "-2Hz"},
    "zh-tw": {"id": "zh-TW-YunJheNeural",       "rate": "+0%", "pitch": "-2Hz"}
}

# 🎭 EXTENDED EMOTION FX CHAINS (FFmpeg)
FX = {
    # Core Persona
    "weathered": "vibrato=f=3:d=0.05,bass=g=1.5,treble=g=-0.5,loudnorm", 
    "bright":    "treble=g=2,loudnorm",
    "warm":      "bass=g=2,treble=g=-1,loudnorm",
    "dark":      "lowpass=f=1000,bass=g=5,loudnorm",
    
    # Extended Range (Comedic/Dramatic)
    "whisper":   "lowpass=f=3000,compand=0|0:1|1:-90/-900|-70/-70|-30/-90|0/-3,vol=2,loudnorm",
    "shout":     "treble=g=5,bass=g=-5,compand=0|0:1|1:-90/-900|-70/-70|-30/-90|0/-3,vol=0.8,loudnorm",
    "phone":     "highpass=f=300,lowpass=f=3000,compand,loudnorm",
    "dream":     "aecho=0.8:0.9:500:0.5,lowpass=f=800,loudnorm",
    "8bit":      "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,loudnorm",
    "god":       "aecho=0.8:0.9:1000:0.3,bass=g=10,loudnorm",
    
    "none":      "loudnorm"
}

def analyze_with_director(text):
    """
    🧠 GEMINI DIRECTOR MODE (ENHANCED)
    Analyzes text context to determine the best emotion, FX, and comedic timing.
    """
    if not GEMINI_API_KEY: return "weathered", "en"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as a Voice Director. Analyze this line: "{text}"
        
        Determine:
        1. Emotion/Style (choose BEST matching: weathered, bright, warm, dark, whisper, shout, phone, dream, 8bit, god)
           - Use 'whisper' for secrets or hesitation.
           - Use 'shout' for anger or excitement.
           - Use 'god' for absolute authority.
           - Use '8bit' for robotic or glitched speech.
           
        2. Language Code (en, fr, es, it, ja, zh) - only if clearly foreign.
        
        Output JSON only: {{"emotion": "...", "lang": "..."}}
        """
        response = model.generate_content(prompt)
        text_resp = response.text.replace('```json','').replace('```','').strip()
        data = json.loads(text_resp)
        
        print(f"[DIRECTOR] Analysis: {data}")
        return data.get("emotion", "weathered"), data.get("lang", "en")
    except Exception as e:
        print(f"[DIRECTOR] Error: {e}")
        return "weathered", "en"

def detect_language(text):
    try:
        b = TextBlob(text)
        if len(text) > 10: return b.detect_language()
    except: pass
    return "en"

def get_definition(word):
    syns = wn.synsets(word)
    if not syns: return None
    res = []
    for s in syns[:3]:
        lemma = s.lemmas()[0].name().replace('_', ' ')
        defi = s.definition()
        res.append(f"{lemma.capitalize()} ({s.pos()}): {defi}")
    return " | ".join(res)

async def generate_speech(text, lang="en", emotion="weathered"):
    lang = lang.lower()
    if lang not in VOICES: lang = "en"
    
    # 🎭 Dynamic Style Adjustments
    v = VOICES[lang].copy() # Copy to avoid mutating global
    if emotion == "whisper":
        v["pitch"] = "-10Hz" # Lower pitch for breathy effect
        v["rate"] = "-15%"   # Slower
    elif emotion == "shout":
        v["pitch"] = "+10Hz" # Higher pitch for straining
        v["rate"] = "+10%"   # Faster
    elif emotion == "god":
        v["pitch"] = "-15Hz" # Deep authority
        v["rate"] = "-20%"   # Very slow
    
    fx_filter = FX.get(emotion, FX["weathered"])
    
    h = hashlib.md5(f"{text}{lang}{emotion}".encode()).hexdigest()[:10]
    raw = f"{CACHE}/{h}_raw.mp3"
    final = f"{CACHE}/{h}.mp3"
    
    if os.path.exists(final): return final
    
    import edge_tts
    comm = edge_tts.Communicate(text, v["id"], rate=v["rate"], pitch=v["pitch"])
    await comm.save(raw)
    
    subprocess.run(["ffmpeg", "-y", "-i", raw, "-af", fx_filter, "-q:a", "0", final], 
                   capture_output=True)
    
    return final if os.path.exists(final) else raw

def speak_sync(text, lang="en", emotion="weathered", use_director=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if use_director:
            d_emotion, d_lang = analyze_with_director(text)
            if d_emotion: emotion = d_emotion
            if d_lang != "en": lang = d_lang
            
        audio_file = loop.run_until_complete(generate_speech(text, lang, emotion))
        subprocess.run(["afplay", audio_file])
        print(f"[GABRIEL] 🗣️  ({lang}) [{emotion}] {text[:40]}...")
    finally:
        loop.close()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path); q = parse_qs(p.query)
        
        # 🔊 SPEAK API
        if p.path == "/speak":
            text = q.get("text", ["Ready"])[0]
            director = q.get("director", ["false"])[0].lower() == "true"
            
            lang = q.get("lang", ["en"])[0]
            emotion = q.get("emotion", ["weathered"])[0]
            
            speak_sync(text, lang, emotion, use_director=director)
            self._json({"spoken": True})
            
        # 📖 DEFINE API
        elif p.path == "/define":
            word = q.get("word", [""])[0]
            defn = get_definition(word)
            if defn:
                speak_sync(f"The definition of {word} is: {defn.split(':')[1]}", "en")
                self._json({"word": word, "definition": defn, "found": True})
            else:
                self._json({"word": word, "found": False})
                
        else:
            self._json({
                **CHARACTER, 
                "languages": list(VOICES.keys()), 
                "director_mode": bool(GEMINI_API_KEY),
                "fx_styles": list(FX.keys())
            })
            
    def _json(self, d):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
        
    def log_message(self, *a): pass

if __name__ == "__main__":
    print(f"\n⚡ GABRIEL OMEGA - POLYGLOT VOICE SERVER (V13)")
    print(f"🧠 Director Mode: {'ENABLED' if GEMINI_API_KEY else 'DISABLED'}")
    print(f"🎭 FX Styles: {len(FX)} Active")
    
    # Startup Sound
    speak_sync("Gabriel system online. Extended range active.", "en", "god")
    
    HTTPServer(("", 5176), H).serve_forever()
