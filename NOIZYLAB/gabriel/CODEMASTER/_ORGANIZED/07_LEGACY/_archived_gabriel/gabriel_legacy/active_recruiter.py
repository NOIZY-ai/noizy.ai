#!/Users/m2ultra/NOIZYLAB/GABRIEL/venv/bin/python3
"""
🎤 THE ACTIVE RECRUITER (V1.0)
Autonomous Voice Cloning Interviewer
"""

import os, sys, time, json, sounddevice as sd, scipy.io.wavfile as wav
import numpy as np
import google.generativeai as genai
import whisper
import subprocess

# Config
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DATASET_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/recruiter_session"
fs = 22050  # Sample rate (XTTS Requisite)
os.makedirs(DATASET_DIR, exist_ok=True)

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

# 🗣️ GABRIEL INTERFACE
def gabriel_speak(text, emotion="neutral"):
    print(f"\n[GABRIEL]: {text}")
    # Call V15 Server (Director Mode off to ensure he follows OUR script)
    subprocess.run(
        f"curl -s 'http://localhost:5176/speak?text={text}&emotion={emotion}&director=false'", 
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(1) # Wait for him to start

# 🎤 RECORDING INTERFACE
def record_audio(duration=5, filename="temp.wav"):
    print(f"   🔴 RECORDING ({duration}s)...")
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("   ✅ STOPPED")
    wav.write(filename, fs, (myrecording * 32767).astype(np.int16)) # Convert to 16-bit PCM
    return filename

# 🧠 ANALYST INTERFACE
def analyze_performance(text, target_emotion):
    if not GEMINI_API_KEY: return True, "I can't judge you without my brain."
    
    prompt = f"""
    ACTING COACH: Analyze this spoken line.
    Target Emotion: {target_emotion}
    Spoken Text: "{text}"
    
    Did the actor say something reasonable? (Doesn't have to be exact, but must be coherent).
    Output JSON: {{"pass": true/false, "critique": "Short feedback to the actor"}}
    """
    try:
        resp = model.generate_content(prompt)
        data = json.loads(resp.text.replace('```json','').replace('```','').strip())
        return data.get("pass", True), data.get("critique", "Good take.")
    except:
        return True, "Good take."

# 🎬 THE INTERVIEW LOOP
def run_interview():
    print("\n🎤 GABRIEL VOICE RECRUITER INITIALIZED")
    print("---------------------------------------")
    
    # 1. WHISPER LOAD
    print("   ⌛ Loading Ear Module (Whisper)...")
    w_model = whisper.load_model("base")
    
    # 2. INTRO
    gabriel_speak("Welcome to the recruitment center. I need to calibrate your voice.", "trust")
    time.sleep(3)
    
    questions = [
        {"q": "Please count from one to five clearly.", "emo": "neutral", "dur": 5},
        {"q": "Tell me a secret you have never told anyone.", "emo": "whisper", "dur": 8},
        {"q": "Imagine you just won the lottery! Shout it out!", "emo": "joy", "dur": 6},
        {"q": "You are furious at a machine that won't work. Yell at it.", "emo": "anger", "dur": 6},
        {"q": "You are terrified of the dark. Describe what you see.", "emo": "fear", "dur": 8},
        {"q": "State your name and your purpose here.", "emo": "god", "dur": 6}
    ]
    
    for i, item in enumerate(questions):
        idx = i + 1
        gabriel_speak(item["q"], "neutral") # He asks neutrally (or maybe in character?)
        time.sleep(len(item["q"]) * 0.1 + 1) # Wait for him to finish asking roughly
        
        # Record
        fname = f"{DATASET_DIR}/sample_{idx:03d}_{item['emo']}.wav"
        record_audio(item["dur"], fname)
        
        # Verify
        result = w_model.transcribe(fname)
        text = result["text"]
        print(f"   📝 Heard: {text}")
        
        passed, critique = analyze_performance(text, item["emo"])
        
        if passed:
            gabriel_speak(f"{critique} Saved.", "trust")
        else:
            gabriel_speak(f"{critique} Let's move on anyway.", "dark")
            
        time.sleep(2)

    gabriel_speak("Interview complete. Generating voice model configuration.", "trust")
    
    # Trigger Formatting & Training (Placeholder for now)
    # subprocess.run([sys.executable, "/Users/m2ultra/NOIZYLAB/GABRIEL/bin/train_xtts.py"]) 
    print("   [SYSTEM] Ready for XTTS Training. Run: bin/train_xtts.py")

if __name__ == "__main__":
    run_interview()
