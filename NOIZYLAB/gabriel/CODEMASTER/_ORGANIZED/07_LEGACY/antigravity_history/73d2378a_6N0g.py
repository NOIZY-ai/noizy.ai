"""
🎭 AGENCY UTILITIES
Shared logic for Emotion Mapping, SFX Management, and Audio Processing.
Ported from V15 'Auteur' System.
"""

import os

# 🔊 SFX LIBRARY
# Maps simple keys to complex FFmpeg filter chains or file paths
SFX_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/sfx"

SFX_MAP = {
    "rain": f"amovie={SFX_DIR}/rain.mp3:loop=0,volume=0.2[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "thunder": f"amovie={SFX_DIR}/thunder.mp3:loop=0,volume=0.5[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "city": f"amovie={SFX_DIR}/city.mp3:loop=0,volume=0.1[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "jazz": f"amovie={SFX_DIR}/jazz.mp3:loop=0,volume=0.15[sfx];[0:a][sfx]amix=inputs=2:duration=first",
    "none": ""
}

# 🎭 COMPLETE EMOTIONAL SPECTRUM (Plutchik + Cinematic)
# Defines how base TTS should be modified for emotion
EMOTION_MAP = {
    "neutral":      {"pitch": "+0Hz",  "rate": "+0%",  "fx": "loudnorm"},
    "joy":          {"pitch": "+5Hz",  "rate": "+10%", "fx": "treble=g=3,loudnorm"},
    "anger":        {"pitch": "-5Hz",  "rate": "+10%", "fx": "compand,loudnorm"},
    "surprised":    {"pitch": "+10Hz", "rate": "+15%", "fx": "treble=g=3,loudnorm"},
    "fear":         {"pitch": "+5Hz",  "rate": "+5%",  "fx": "vibrato=f=6:d=0.3,loudnorm"},
    "sadness":      {"pitch": "-5Hz",  "rate": "-10%", "fx": "lowpass=f=2500,loudnorm"},
    "disgust":      {"pitch": "-5Hz",  "rate": "-15%", "fx": "highpass=f=200,loudnorm"},
    "trust":        {"pitch": "-2Hz",  "rate": "-5%",  "fx": "bass=g=3,loudnorm"},
    "anticipation": {"pitch": "+2Hz",  "rate": "+5%",  "fx": "loudnorm"},
    "whisper":      {"pitch": "+0Hz",  "rate": "-10%", "fx": "lowpass=f=3000,compand,vol=4,loudnorm"},
    "god":          {"pitch": "-12Hz", "rate": "-15%", "fx": "aecho=0.8:0.9:1000:0.3,bass=g=15,treble=g=2,loudnorm"},
    "8bit":         {"pitch": "+0Hz",  "rate": "+0%",  "fx": "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1,loudnorm"},
    "phone":        {"pitch": "+0Hz",  "rate": "+0%",  "fx": "highpass=f=300,lowpass=f=3000,compand,loudnorm"}
}

import subprocess

def process_audio_fx(input_file, output_file, emotion="neutral", sfx="none"):
    """
    Applies FFmpeg filters for emotion and mixes optional SFX.
    """
    emo_config = EMOTION_MAP.get(emotion, EMOTION_MAP["neutral"])
    audio_fx = emo_config["fx"]
    sfx_filter = SFX_MAP.get(sfx, "")
    
    # Construct Filter Chain
    final_filter = audio_fx
    
    # Simple SFX Logic for now:
    # If SFX requested, we assume we might need a complex filter.
    # But for stability, V18 will prioritize the Audio FX (EQ/Comp) first.
    # SFX mixing is "bonus" if we can do it reliably without complex graphs.
    # For now, let's just apply the emotional FX. Use 'amix' later if stable.
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-af", final_filter,
        output_file
    ]
    
    # Run FFmpeg
    # Suppress output unless error
    subprocess.run(cmd, shell=True)
    print(f"   ✅ FX Processed: {output_file}")
    
    return output_file if os.path.exists(output_file) else input_file

import psutil

class SystemMonitor:
    """
    V25: Biometric Dashboard for M2 Ultra.
    """
    @staticmethod
    def get_vitals():
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        
        # Mock Thermal (MacOS requires sudo usually, keeping simple for now)
        # Or check if we can get it via powermetrics? Just mocked for UI speed.
        thermal = "Normal"
        if cpu > 80: thermal = "High"
        if cpu > 95: thermal = "CRITICAL 🥵"
            
        return cpu, ram, thermal

    @staticmethod
    def get_heartbeat_status(cpu):
        if cpu < 20: return "RESTING 🧘"
        if cpu < 50: return "ACTIVE 🏃"
        if cpu < 80: return "INTENSE 🏋️"
        return "FATIGUED 🥵"
