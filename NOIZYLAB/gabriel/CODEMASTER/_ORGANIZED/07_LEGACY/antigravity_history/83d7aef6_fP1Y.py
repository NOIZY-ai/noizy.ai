
import os
import subprocess

class VoiceCore:
    def __init__(self):
        self.voice = "Samantha" # Or "Daniel", "Karen", etc.
        self.rate = 180

    def speak(self, text):
        """Speak text using macOS 'say' command."""
        try:
            # Run in background to not block server
            subprocess.Popen(["say", "-v", self.voice, "-r", str(self.rate), text])
        except Exception as e:
            print(f"❌ [VOICE] Error: {e}")

    def announce_overlord(self):
        self.speak("Gabriel System Omega. I am now the Overlord of this Domain.")

if __name__ == "__main__":
    v = VoiceCore()
    v.announce_overlord()
