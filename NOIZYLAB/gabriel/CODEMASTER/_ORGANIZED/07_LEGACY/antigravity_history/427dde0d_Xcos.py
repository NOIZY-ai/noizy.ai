#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
DR. GABRIEL ALMEIDA - OMEGA VOICE SYSTEM (V14)
Features: Plutchik's Emotional Engine (Complete Range), Gemini Director, Polyglot
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

# 🎭 COMPLETE EMOTIONAL SPECTRUM (Plutchik + Cinematic)
EMOTION_MAP = {
    # BASE
    "neutral":      {"pitch": "+0Hz",  "rate": "+0%",  "fx": "loudnorm"},
    
    # INTENSE (High Arousal)
    "joy":          {"pitch": "+10Hz", "rate": "+10%", "fx": "treble=g=5,loudnorm"},
    "anger":        {"pitch": "-10Hz", "rate": "+15%", "fx": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,compand,loudnorm"},
    "surprised":    {"pitch": "+20Hz", "rate": "+25%", "fx": "treble=g=5,loudnorm"},
    "fear":         {"pitch": "+15Hz", "rate": "+10%", "fx": "vibrato=f=8:d=0.5,tremolo=f=8:d=0.7,loudnorm"},
    
    # SUBDUED (Low Arousal)
    "sadness":      {"pitch": "-15Hz", "rate": "-15%", "fx": "lowpass=f=2000,bass=g=5,loudnorm"},
    "disgust":      {"pitch": "-10Hz", "rate": "-20%", "fx": "highpass=f=200,lowpass=f=2000,loudnorm"},
    "trust":        {"pitch": "-5Hz",  "rate": "-5%",  "fx": "bass=g=3,treble=g=2,loudnorm"},
    "anticipation": {"pitch": "+5Hz",  "rate": "+5%",  "fx": "aecho=0.8:0.9:50:0.3,loudnorm"},
    
    # CINEMATIC / FX
    "whisper":      {"pitch": "+0Hz",  "rate": "-10%", "fx": "lowpass=f=3000,compand=0|0:1|1:-90/-900|-70/-70|-30/-90|0/-3,vol=4,loudnorm"},
    "god":          {"pitch": "-25Hz", "rate": "-20%", "fx": "aecho=0.8:0.9:1000:0.3,bass=g=15,treble=g=2,loudnorm"},
    "8bit":         {"pitch": "+0Hz",  "rate": "+0%",  "fx": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,loudnorm"},
    "phone":        {"pitch": "+0Hz",  "rate": "+0%",  "fx": "highpass=f=300,lowpass=f=3000,compand,loudnorm"}
}

def analyze_with_director(text):
    """
    🧠 GEMINI DIRECTOR V14
    Maps text to the Complete Emotional Spectrum.
    """
    if not GEMINI_API_KEY: return "neutral", "en"
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as a Voice Director. Analyze this line: "{text}"
        
        Task 1: Detect Emotion (Select ONE from list):
        - joy (Excited, Happy)
        - sadness (Depressed, Grief)
        - anger (Rage, Frustration)
        - fear (Terrified, Anxious)
        - trust (Warm, Reassuring)
        - disgust (Repulsed)
        - surprised (Shocked)
        - anticipation (Curious)
        - whisper (Secretive)
        - god (Authoritative)
        - neutral (Default)

        Task 2: Detect Language Code (en, fr, es, it, ja, zh) - only if clearly foreign.
        
        Output JSON only: {{"emotion": "...", "lang": "..."}}
        """
        response = model.generate_content(prompt)
        text_resp = response.text.replace('```json','').replace('```','').strip()
        data = json.loads(text_resp)
        
        print(f"[DIRECTOR] Analysis: {data}")
        return data.get("emotion", "neutral"), data.get("lang", "en")
    except Exception as e:
        print(f"[DIRECTOR] Error: {e}")
        return "neutral", "en"

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

async def generate_speech(text, lang="en", emotion="neutral"):
    lang = lang.lower()
    if lang not in VOICES: lang = "en"
    
    # 1. Get Base Voice
    base_voice = VOICES[lang]
    
    # 2. Get Emotion Modifiers (Default to neutral if not found)
    emo_config = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"])
    
    # 3. Calculate Final Params (Base + Emotion Modifier)
    # Note: EdgeTTS strings are like "-10%", we need to be careful combining them.
    # For V14 simplicity, we will OVERRIDE base settings with Emotion settings if Emotion is strong.
    # If Neutral, we use Base settings.
    
    final_rate = base_voice["rate"]
    final_pitch = base_voice["pitch"]
    
    if emotion != "neutral":
        final_rate = emo_config["rate"]
        final_pitch = emo_config["pitch"]
        
    final_fx = emo_config["fx"]
    
    h = hashlib.md5(f"{text}{lang}{emotion}".encode()).hexdigest()[:10]
    raw = f"{CACHE}/{h}_raw.mp3"
    final = f"{CACHE}/{h}.mp3"
    
    if os.path.exists(final): return final
    
    import edge_tts
    comm = edge_tts.Communicate(text, base_voice["id"], rate=final_rate, pitch=final_pitch)
    await comm.save(raw)
    
    subprocess.run(["ffmpeg", "-y", "-i", raw, "-af", final_fx, "-q:a", "0", final], 
                   capture_output=True)
    
    return final if os.path.exists(final) else raw

def speak_sync(text, lang="en", emotion="neutral", use_director=False):
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
            # Use 'neutral' as default if not specified
            emotion = q.get("emotion", ["neutral"])[0]
            
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
                "emotions": list(EMOTION_MAP.keys())
            })
            
    def _json(self, d):
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())
        
    def log_message(self, *a): pass

if __name__ == "__main__":
    print(f"\n⚡ GABRIEL OMEGA - POLYGLOT VOICE SERVER (V14)")
    print(f"🧠 Director Mode: {'ENABLED' if GEMINI_API_KEY else 'DISABLED'}")
    print(f"🎭 Emotional Range: {len(EMOTION_MAP)} Core States")
    
    # Startup Sound
    speak_sync("Gabriel system V 14 online. Emotional spectrum initialized.", "en", "trust")
    
    HTTPServer(("", 5176), H).serve_forever()
