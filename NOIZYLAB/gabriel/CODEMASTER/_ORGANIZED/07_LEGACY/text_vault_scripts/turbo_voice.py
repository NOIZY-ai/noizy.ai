#!/usr/bin/env python3
"""
🗣️ GABRIEL VOICE ENGINE
Zero-latency voice synthesis for the Gabriel AI system.

Supports:
1. macOS `say` (FREE, instant, always available)
2. ElevenLabs API (premium, realistic)
3. Local Piper TTS (if installed)

Usage:
    python3 turbo_voice.py "Hello, I am Gabriel."
    python3 turbo_voice.py --persona solar "The system is ready."
    python3 turbo_voice.py --backend elevenlabs "Premium voice test."
"""

import os
import sys
import json
import subprocess
import tempfile
import hashlib
from pathlib import Path
from datetime import datetime

# ==============================================================================
# CONFIGURATION
# ==============================================================================
SCRIPTS_DIR = Path(__file__).resolve().parent
VOICE_CACHE_DIR = SCRIPTS_DIR.parent / "VoiceCache"
VOICE_CACHE_DIR.mkdir(exist_ok=True)

# Persona -> Voice Mapping (macOS)
MAC_VOICES = {
    "titan": "Daniel",      # British, authoritative
    "solar": "Alex",        # American, warm
    "void": "Bad News",     # Dramatic, deep
    "nature": "Samantha",   # Calm, pleasant
    "omega": "Whisper",     # Ethereal
    "default": "Daniel"
}

# Persona -> ElevenLabs Voice IDs (if configured)
ELEVENLABS_VOICES = {
    "titan": "pNInz6obpgDQGcFmaJgB",   # Adam
    "solar": "ErXwobaYiN019PkySvjV",   # Antoni
    "void": "VR6AewLTigWG4xSOukaG",    # Arnold
    "nature": "EXAVITQu4vr4xnSDxMaL",  # Bella
    "omega": "onwK4e9ZLuTAKqWW03F9",   # Drew (Whispery)
    "default": "pNInz6obpgDQGcFmaJgB"
}

# ==============================================================================
# VOICE ENGINE
# ==============================================================================
class GabrielVoice:
    def __init__(self):
        self.cache_enabled = True
        self.current_backend = "macos"  # macos, elevenlabs, piper
        
        # Check ElevenLabs
        self.elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY", "")
        if self.elevenlabs_key:
            self.current_backend = "elevenlabs"
            print("VOICE > 🎤 ElevenLabs API Available")
        else:
            print("VOICE > 🎤 Using macOS TTS (Free)")
    
    def _cache_key(self, text: str, persona: str, backend: str) -> str:
        """Generate cache key from content hash"""
        content = f"{backend}:{persona}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached(self, cache_key: str) -> Path | None:
        """Check if audio exists in cache"""
        for ext in [".mp3", ".wav", ".aiff"]:
            cached = VOICE_CACHE_DIR / f"{cache_key}{ext}"
            if cached.exists():
                return cached
        return None
    
    # --------------------------------------------------------------------------
    # BACKEND: macOS say
    # --------------------------------------------------------------------------
    def _speak_macos(self, text: str, persona: str = "titan", output_file: Path = None) -> Path:
        """Use macOS say command for instant TTS"""
        voice = MAC_VOICES.get(persona, MAC_VOICES["default"])
        
        if output_file is None:
            output_file = VOICE_CACHE_DIR / f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.aiff"
        
        # Generate audio file
        cmd = ["say", "-v", voice, "-o", str(output_file), text]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"VOICE > ✅ Generated: {output_file.name} ({voice})")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"VOICE > ❌ macOS TTS Error: {e}")
            return None
    
    def _speak_macos_live(self, text: str, persona: str = "titan"):
        """Speak immediately without saving"""
        voice = MAC_VOICES.get(persona, MAC_VOICES["default"])
        subprocess.Popen(["say", "-v", voice, text])
        print(f"VOICE > 🔊 Speaking ({voice})")
    
    # --------------------------------------------------------------------------
    # BACKEND: ElevenLabs
    # --------------------------------------------------------------------------
    def _speak_elevenlabs(self, text: str, persona: str = "titan", output_file: Path = None) -> Path:
        """Use ElevenLabs API for premium TTS"""
        import urllib.request
        
        voice_id = ELEVENLABS_VOICES.get(persona, ELEVENLABS_VOICES["default"])
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        payload = json.dumps({
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if output_file is None:
                    output_file = VOICE_CACHE_DIR / f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                
                with open(output_file, 'wb') as f:
                    f.write(response.read())
                
                print(f"VOICE > ✅ Generated: {output_file.name} (ElevenLabs)")
                return output_file
        except Exception as e:
            print(f"VOICE > ❌ ElevenLabs Error: {e}")
            # Fallback to macOS
            return self._speak_macos(text, persona, output_file)
    
    # --------------------------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------------------------
    def speak(self, text: str, persona: str = "titan", save: bool = True, play: bool = True) -> Path | None:
        """
        Main speak function. Generates and optionally plays audio.
        
        Args:
            text: What to say
            persona: Voice persona (titan, solar, void, nature, omega)
            save: Save to file (vs temp)
            play: Play audio immediately
        
        Returns:
            Path to audio file
        """
        if not text.strip():
            print("VOICE > ⚠️ Empty text, nothing to speak")
            return None
        
        # Check cache
        cache_key = self._cache_key(text, persona, self.current_backend)
        if self.cache_enabled:
            cached = self._get_cached(cache_key)
            if cached:
                print(f"VOICE > ⚡ Cache hit: {cached.name}")
                if play:
                    self._play_audio(cached)
                return cached
        
        # Generate new audio
        if save:
            ext = ".mp3" if self.current_backend == "elevenlabs" else ".aiff"
            output_file = VOICE_CACHE_DIR / f"{cache_key}{ext}"
        else:
            output_file = None
        
        # Route to backend
        if self.current_backend == "elevenlabs" and self.elevenlabs_key:
            audio_file = self._speak_elevenlabs(text, persona, output_file)
        else:
            if play and not save:
                # Live speak (no file)
                self._speak_macos_live(text, persona)
                return None
            audio_file = self._speak_macos(text, persona, output_file)
        
        # Play if requested
        if play and audio_file:
            self._play_audio(audio_file)
        
        return audio_file
    
    def _play_audio(self, file_path: Path):
        """Play audio file using afplay (macOS)"""
        subprocess.Popen(["afplay", str(file_path)])
    
    def speak_now(self, text: str, persona: str = "titan"):
        """Immediate speech, no file saving"""
        self._speak_macos_live(text, persona)
    
    def get_available_voices(self) -> dict:
        """Return all available voices"""
        return {
            "macos": list(MAC_VOICES.keys()),
            "elevenlabs": list(ELEVENLABS_VOICES.keys()) if self.elevenlabs_key else [],
            "current_backend": self.current_backend
        }

# ==============================================================================
# API ENDPOINT (For Server Integration)
# ==============================================================================
def generate_voice_response(text: str, persona: str = "titan") -> dict:
    """
    API-friendly function for server integration.
    Returns dict with status, url, etc.
    """
    voice = GabrielVoice()
    audio_file = voice.speak(text, persona, save=True, play=False)
    
    if audio_file:
        return {
            "status": "ok",
            "url": f"/voice/{audio_file.name}",
            "file": str(audio_file),
            "persona": persona,
            "backend": voice.current_backend
        }
    return {"status": "error", "message": "Voice generation failed"}

# ==============================================================================
# MAIN CLI
# ==============================================================================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Gabriel Voice Engine")
    parser.add_argument("text", nargs="?", help="Text to speak")
    parser.add_argument("--persona", "-p", default="titan", 
                       choices=["titan", "solar", "void", "nature", "omega"],
                       help="Voice persona")
    parser.add_argument("--backend", "-b", choices=["macos", "elevenlabs"],
                       help="Force specific backend")
    parser.add_argument("--no-play", action="store_true", help="Don't play audio")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--demo", action="store_true", help="Demo all personas")
    
    args = parser.parse_args()
    
    voice = GabrielVoice()
    
    # Backend override
    if args.backend:
        voice.current_backend = args.backend
    
    if args.list_voices:
        voices = voice.get_available_voices()
        print("\n🎤 GABRIEL VOICE ENGINE")
        print(f"   Current Backend: {voices['current_backend']}")
        print(f"\n   macOS Voices: {', '.join(voices['macos'])}")
        if voices['elevenlabs']:
            print(f"   ElevenLabs: {', '.join(voices['elevenlabs'])}")
        else:
            print("   ElevenLabs: (Set ELEVENLABS_API_KEY to enable)")
        return
    
    if args.demo:
        print("\n🎤 GABRIEL VOICE DEMO\n")
        for persona in ["titan", "solar", "void", "nature"]:
            text = f"I am Gabriel, speaking as {persona}."
            print(f"   [{persona.upper()}] {text}")
            voice.speak_now(text, persona)
            import time
            time.sleep(3)  # Gap between demos
        print("\n✅ Demo complete.")
        return
    
    if args.text:
        voice.speak(args.text, args.persona, play=not args.no_play)
    else:
        # Interactive mode
        print("\n🎤 GABRIEL VOICE ENGINE (Interactive)")
        print("   Type text to speak, 'quit' to exit.\n")
        while True:
            try:
                text = input(f"[{args.persona.upper()}] > ")
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if text:
                    voice.speak_now(text, args.persona)
            except KeyboardInterrupt:
                break
        print("\n👋 Voice Engine offline.")

if __name__ == "__main__":
    main()
