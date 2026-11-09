#!/usr/bin/env python3
"""
GABRIEL VOICE - SPEECH SYNTHESIS INTERFACE
Protocol: ZERO LATENCY | Tech: macOS Native 'say'
Created by: CB_01
Date: December 2025
"""

import subprocess
import threading
import time

class GabrielVoice:
    def __init__(self, voice="Samantha", rate=175):
        self.voice = voice # Options: Samantha, Alex, Fred, Victoria ...
        self.rate = rate   # Words per minute (approx)
        self.is_speaking = False

    def speak(self, text, block=True):
        """
        Speak the given text.
        block: If True, wait for speech to finish. If False, run in background.
        """
        if not text: return

        # CLI visual feedback is handled by the caller or we can verify here
        # print(f"🗣️  GABRIEL: {text}") 

        if block:
            self._run_say(text)
        else:
            t = threading.Thread(target=self._run_say, args=(text,))
            t.daemon = True
            t.start()

    def _run_say(self, text):
        self.is_speaking = True
        try:
            # -v Voice, -r Rate
            cmd = ["say", "-v", self.voice, "-r", str(self.rate), text]
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"⚠️  VOICE ERROR: {e}")
        finally:
            self.is_speaking = False

    def ask(self, prompt_text):
        """
        Speak the prompt, then wait for text input.
        Returns the user's input string.
        """
        self.speak(prompt_text, block=True)
        # Use simple print for visual cue as well
        return input(f"\n🗣️  GABRIEL > {prompt_text}\n👤 YOU > ").strip()

    def greet(self):
        """Randomized greeting."""
        import random
        greetings = [
            "Online. Systems nominal.",
            "Gabriel listening. God mode active.",
            "Visuals engaged. Audio systems ready.",
            "Welcome back, Commander.",
            "The universe is listening."
        ]
        self.speak(random.choice(greetings), block=False)

    def announce_status(self, component, status):
        """Speak a system status update."""
        if status == "ACTIVE" or status == "ONLINE" or status == "LOADED":
             self.speak(f"{component} is {status.lower()}.", block=False)
        elif status == "FAIL" or status == "OFFLINE" or status == "MISSING":
             self.speak(f"Warning. {component} is {status.lower()}.", block=True)

if __name__ == "__main__":
    # Test
    v = GabrielVoice()
    v.speak("Mic check one two. Gabriel Online.")
