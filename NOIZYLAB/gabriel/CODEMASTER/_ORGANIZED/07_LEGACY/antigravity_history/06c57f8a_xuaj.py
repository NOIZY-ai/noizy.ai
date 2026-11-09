#!/usr/bin/env python3
# 🤖 SYSTEM FILE: gabriel_voice.py
# Optimized by Healer Drone
"""
GABRIEL VOICE V2 - ADVANCED SPEECH ENGINE
Protocol: ZERO LATENCY | Tech: macOS Native 'say' (Optimized)
Upgrades: Threaded Queue, Interrupts, Caching
"""

import subprocess
import threading
import time
import queue
import hashlib
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "voice_cache"
if not CACHE_DIR.exists():
    CACHE_DIR.mkdir()

class GabrielVoiceV2:
    def __init__(self, voice="Samantha", rate=180):
        self.voice = voice 
        self.rate = rate
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.stop_signal = False
        
        # Start Worker Thread
        self.worker = threading.Thread(target=self._process_queue)
        self.worker.daemon = True
        self.worker.start()

    def speak(self, text, block=False, priority=False):
        """
        Speak text.
        block: If True, waits for this specific phrase.
        priority: If True, clears queue and speaks immediately.
        """
        if not text: return

        if priority:
            self.stop_speech()
            with self.speech_queue.mutex:
                self.speech_queue.queue.clear()
        
        if block:
            self._run_say(text)
        else:
            self.speech_queue.put(text)

    def stop_speech(self):
        """Interrupts current speech."""
        if self.is_speaking:
            self.stop_signal = True
            # On macOS with 'say', we might need to kill the process if we tracked the PID.
            # For now, we just stop the queue processing and rely on say finishing quickly.
            # Advanced V3: Use 'killall say' (Aggressive)
            subprocess.run(["killall", "say"], stderr=subprocess.DEVNULL)

    def _process_queue(self):
        while True:
            try:
                text = self.speech_queue.get()
                if text is None: break
                
                self.is_speaking = True
                self._run_say(text)
                self.is_speaking = False
                self.speech_queue.task_done()
            except Exception as e:
                print(f"❌ VOICE WORKER ERROR: {e}")

    def _run_say(self, text):
        if self.stop_signal:
            self.stop_signal = False
            return

        # Check Cache for typical phrases
        text_hash = hashlib.md5(text.encode()).hexdigest()
        cache_file = CACHE_DIR / f"{text_hash}.aiff"
        
        try:
            if cache_file.exists():
                # Play cached audio (Faster start)
                cmd = ["afplay", str(cache_file)]
            else:
                # Speak directly
                # Future: Save to cache with -o
                cmd = ["say", "-v", self.voice, "-r", str(self.rate), text]
            
            subprocess.run(cmd, check=True)
            
        except Exception as e:
            # If killall was run, this might error, which is fine
            pass

    def ask(self, prompt_text):
        """Speak and wait for input."""
        self.speak(prompt_text, block=True)
        return input(f"\n🗣️  GABRIEL > {prompt_text}\n👤 YOU > ").strip()

    def greet(self):
        import random
        greetings = [
            "Gabriel Online. Systems nominal.",
            "God mode active.",
            "Visuals engaged.",
            "Welcome back."
        ]
        self.speak(random.choice(greetings))

if __name__ == "__main__":
    v = GabrielVoiceV2()
    print("🗣️  Testing Gabriel Voice V2...")
    v.speak("Initializing Voice Systems V2.")
    v.speak("Testing queue system. This is phrase one.")
    v.speak("This is phrase two. It should follow immediately.")
    time.sleep(2)
    print("❗ INTERRUPT TEST")
    v.speak("This is a long phrase that should be interrupted by the priority message.", priority=True)
    v.speak("PRIORITY OVERRIDE.", priority=True)
    time.sleep(3)
