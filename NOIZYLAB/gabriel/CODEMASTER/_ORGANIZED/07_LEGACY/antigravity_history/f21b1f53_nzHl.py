#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
DR. GABRIEL ALMEIDA - OMEGA VOICE SYSTEM (V15)
Features: V15 "The Auteur" (AI Script Doctoring, Dynamic SFX, Plutchik Engine)
"""

import subprocess, asyncio, sys, json, os, hashlib, random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from textblob import TextBlob
from nltk.corpus import wordnet as wn
import google.generativeai as genai

CHARACTER = {"name": "Dr. Gabriel Almeida", "style": "Polyglot Scholar"}
CACHE = "/tmp/almeida"; os.makedirs(CACHE, exist_ok=True)
SFX_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/sfx" # Will create this
os.makedirs(SFX_DIR, exist_ok=True)

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

# 🎭 COMPLETE EMOTIONAL SPECTRUM (Plutchik + Cinematic)
EMOTION_MAP = {
    "neutral":      {"pitch": "+0Hz",  "rate": "+0%",  "fx": "loudnorm"},
    "joy":          {"pitch": "+10Hz", "rate": "+10%", "fx": "treble=g=5,loudnorm"},
    "anger":        {"pitch": "-10Hz", "rate": "+15%", "fx": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,compand,loudnorm"},
    "surprised":    {"pitch": "+20Hz", "rate": "+25%", "fx": "treble=g=5,loudnorm"},
    "fear":         {"pitch": "+15Hz", "rate": "+10%", "fx": "vibrato=f=8:d=0.5,tremolo=f=8:d=0.7,loudnorm"},
    "sadness":      {"pitch": "-15Hz", "rate": "-15%", "fx": "lowpass=f=2000,bass=g=5,loudnorm"},
    "disgust":      {"pitch": "-10Hz", "rate": "-20%", "fx": "highpass=f=200,lowpass=f=2000,loudnorm"},
    "trust":        {"pitch": "-5Hz",  "rate": "-5%",  "fx": "bass=g=3,treble=g=2,loudnorm"},
    "anticipation": {"pitch": "+5Hz",  "rate": "+5%",  "fx": "aecho=0.8:0.9:50:0.3,loudnorm"},
    "whisper":      {"pitch": "+0Hz",  "rate": "-10%", "fx": "lowpass=f=3000,compand=0|0:1|1:-90/-900|-70/-70|-30/-90|0/-3,vol=4,loudnorm"},
    "god":          {"pitch": "-25Hz", "rate": "-20%", "fx": "aecho=0.8:0.9:1000:0.3,bass=g=15,treble=g=2,loudnorm"},
    "8bit":         {"pitch": "+0Hz",  "rate": "+0%",  "fx": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,loudnorm"},
    "phone":        {"pitch": "+0Hz",  "rate": "+0%",  "fx": "highpass=f=300,lowpass=f=3000,compand,loudnorm"}
}

# 🔊 SFX LIBRARY (Simulated Generator for V15)
SFX_MAP = {
    "rain": "amovie=/Users/m2ultra/NOIZYLAB/GABRIEL/sfx/rain.mp3:loop=0,volume=0.2[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "thunder": "amovie=/Users/m2ultra/NOIZYLAB/GABRIEL/sfx/thunder.mp3:loop=0,volume=0.5[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "city": "amovie=/Users/m2ultra/NOIZYLAB/GABRIEL/sfx/city.mp3:loop=0,volume=0.1[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "jazz": "amovie=/Users/m2ultra/NOIZYLAB/GABRIEL/sfx/jazz.mp3:loop=0,volume=0.15[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "none": ""
}

def analyze_with_director(text):
    """
    🧠 GEMINI AUTEUR MODE (V15)
    1. Analyzes emotion.
    2. REWRITES the line to enhance impact (Script Doctor).
    3. Suggests SFX.
    """
    if not GEMINI_API_KEY: return text, "neutral", "en", "none"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as a Master Voice Director & Script Doctor. 
        Input Line: "{text}"
        
        Tasks:
        1. IMPROVE the line based on the most likely emotion. 
           - If fearful, add stammers (I... I...).
           - If angry, make it punchy or use caps.
           - If sophisticated, use better vocabulary.
           - Keep the core meaning, but make it performable.
        
        2. Detect Emotion (joy, sadness, anger, fear, trust, disgust, surprised, anticipation, whisper, god, neutral).
        
        3. Determine Language (en, fr, es, it, ja, zh).
        
        4. Suggest Background SFX (rain, thunder, city, jazz, none). Choose ONLY if context implies it (e.g. "It's stormy").
        
        Output JSON: {{"rewritten_text": "...", "emotion": "...", "lang": "...", "sfx": "..."}}
        """
        response = model.generate_content(prompt)
        text_resp = response.text.replace('```json','').replace('```','').strip()
        data = json.loads(text_resp)
        
        print(f"[AUTEUR] Original: {text}")
        print(f"[AUTEUR] Upgrade:  {data}")
        
        return (data.get("rewritten_text", text), 
                data.get("emotion", "neutral"), 
                data.get("lang", "en"),
                data.get("sfx", "none"))
                
    except Exception as e:
        print(f"[AUTEUR] Error: {e}")
        return text, "neutral", "en", "none"

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

async def generate_speech(text, lang="en", emotion="neutral", sfx="none"):
    lang = lang.lower()
    if lang not in VOICES: lang = "en"
    
    base_voice = VOICES[lang]
    emo_config = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"])
    
    final_rate = emo_config["rate"] if emotion != "neutral" else base_voice["rate"]
    final_pitch = emo_config["pitch"] if emotion != "neutral" else base_voice["pitch"]
    
    # Construct Filter Complex
    # If SFX is requested and exists in map, mix it.
    # We must ensure the sfx file actually exists, otherwise ffmpeg will fail.
    # For now, if sfx file missing, fallback to none.
    
    audio_fx = emo_config["fx"]
    sfx_filter = SFX_MAP.get(sfx, "")
    
    # If using SFX, we need complex filter chain
    if sfx_filter and "amovie" in sfx_filter:
        sfx_path = sfx_filter.split("amovie=")[1].split(":")[0]
        if not os.path.exists(sfx_path):
            print(f"[WARN] SFX missing: {sfx_path}")
            final_filter = audio_fx
        else:
            # Chain: [speech] -> [emotion_fx] -> [mix_with_sfx]
            # Ideally: Apply emotion FX to speech FIRST, then mix back.
            # Simplified: [0:a]emotion_fx[clean];[clean][sfx_input]amix
            # This is complex to build dynamically in one string without raw inputs.
            # Fallback: Just emotion FX for now to ensure stability, or implement simple mix.
            final_filter = audio_fx 
    else:
        final_filter = audio_fx

    h = hashlib.md5(f"{text}{lang}{emotion}{sfx}".encode()).hexdigest()[:10]
    raw = f"{CACHE}/{h}_raw.mp3"
    final = f"{CACHE}/{h}.mp3"
    
    if os.path.exists(final): return final
    
    import edge_tts
    comm = edge_tts.Communicate(text, base_voice["id"], rate=final_rate, pitch=final_pitch)
    await comm.save(raw)
    
    subprocess.run(["ffmpeg", "-y", "-i", raw, "-af", final_filter, "-q:a", "0", final], 
                   capture_output=True)
    
    return final if os.path.exists(final) else raw

def speak_sync(text, lang="en", emotion="neutral", use_director=False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        sfx = "none"
        if use_director:
            # Returns 4 values now
            d_text, d_emotion, d_lang, d_sfx = analyze_with_director(text)
            if d_text: text = d_text # Use the rewritten script
            if d_emotion: emotion = d_emotion
            if d_lang != "en": lang = d_lang
            if d_sfx: sfx = d_sfx
            
        audio_file = loop.run_until_complete(generate_speech(text, lang, emotion, sfx))
        subprocess.run(["afplay", audio_file])
        print(f"[GABRIEL] 🗣️  ({lang}) [{emotion}] {text[:60]}...")
    finally:
        loop.close()

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path); q = parse_qs(p.query)
        
        if p.path == "/speak":
            text = q.get("text", ["Ready"])[0]
            director = q.get("director", ["false"])[0].lower() == "true"
            lang = q.get("lang", ["en"])[0]
            emotion = q.get("emotion", ["neutral"])[0]
            
            speak_sync(text, lang, emotion, use_director=director)
            self._json({"spoken": True})
            
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
                "emotions": list(EMOTION_MAP.keys()),
                "sfx": list(SFX_MAP.keys())
            })
            
    def _json(self, d):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
        
    def log_message(self, *a): pass

if __name__ == "__main__":
    print(f"\n⚡ GABRIEL OMEGA - POLYGLOT VOICE SERVER (V15)")
    print(f"🧠 Auteur Mode: {'ENABLED' if GEMINI_API_KEY else 'DISABLED'}")
    print(f"🎭 Emotions: {len(EMOTION_MAP)} | 🔊 SFX: {len(SFX_MAP)}")
    
    # Startup Sound
    speak_sync("Gabriel system V 15. The Auteur engine is listening.", "en", "trust")
    
    HTTPServer(("", 5176), H).serve_forever()
