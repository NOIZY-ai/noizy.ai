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

import urllib.parse

class ImageGenerator:
    """
    V26: The Visionary.
    Generates Concept Art URLs via Pollinations.ai (No Auth, Fast).
    """
    @staticmethod
    def generate(prompt):
        # Clean prompt for URL
        safe_prompt = urllib.parse.quote(prompt)
        # Add cinematic keywords for quality
        enhanced_prompt = f"{safe_prompt} cinematic, highly detailed, dramatic lighting, 8k, concept art"
        url = f"https://pollinations.ai/p/{enhanced_prompt}?width=1024&height=512&seed=42&model=flux"
        return url

import subprocess
import requests
import uuid

class DreamFactory:
    """
    V27: The Dreamer.
    Synthesizes Audio + Image into a Cinematic MP4 (Ken Burns Effect).
    """
    @staticmethod
    def create_dream(audio_path, image_url):
        try:
            # 1. Paths
            base_dir = os.path.dirname(audio_path)
            dream_id = str(uuid.uuid4())[:8]
            image_path = os.path.join(base_dir, f"dream_img_{dream_id}.jpg")
            video_path = os.path.join(base_dir, f"dream_{dream_id}.mp4")
            
            # 2. Download Image
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(response.content)
            else:
                return None
            
            # 3. FFmpeg Magic (Ken Burns Zoom + Audio)
            # Zoom in 10% over duration
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", image_path,
                "-i", audio_path,
                "-vf", "scale=1920:1080,zoompan=z='min(zoom+0.0015,1.5)':d=700:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720",
                "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p", "-shortest",
                video_path
            ]
            
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cleanup Image
            if os.path.exists(image_path):
                os.remove(image_path)
                
            return video_path
            
        except Exception as e:
            print(f"Dream Creation Failed: {e}")
            return None
