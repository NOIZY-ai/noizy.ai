#!/usr/bin/env python3
"""
GABRIEL PLAYER - NATIVE AUDIO INTERFACE
Protocol: HIGH FIDELITY | Tech: macOS 'afplay'
"""

import subprocess
import threading
import time
import os
import random
from pathlib import Path

class GabrielPlayer:
    def __init__(self):
        self.process = None
        self.current_track = None
        self.is_playing = False
        self.volume = 1.0 # 0.0 to 1.0 (afplay uses -v 1 (approx))

        # Audio Search Paths
        self.library_paths = [
            Path("/System/Library/Sounds"), # Fallback (System Sounds)
            Path("../GOOGLE_DRIVE_AUDIO"),
            Path("../../GOOGLE_DRIVE_AUDIO"),
            Path.home() / "Music"
        ]

    def scan_library(self):
        """Scans known paths for audio files."""
        tracks = []
        exts = {'.mp3', '.wav', '.aif', '.aiff', '.m4a'}

        for p in self.library_paths:
            if p.exists():
                for f in p.rglob("*"):
                    if f.suffix.lower() in exts:
                        tracks.append(f)
        return tracks

    def play(self, file_path, block=False):
        """Plays an audio file."""
        self.stop() # Stop any current track

        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return

        self.current_track = file_path.name
        self.is_playing = True

        if block:
            self._run_afplay(file_path)
        else:
            t = threading.Thread(target=self._run_afplay, args=(file_path,))
            t.daemon = True
            t.start()

    def _run_afplay(self, file_path):
        try:
            # afplay -v [volume] -q [quality 1=high]
            cmd = ["afplay", "-v", str(self.volume), "-q", "1", str(file_path)]
            self.process = subprocess.Popen(cmd)
            self.process.wait()
        except Exception as e:
            print(f"⚠️  PLAYER ERROR: {e}")
        finally:
            self.is_playing = False
            self.current_track = None

    def stop(self):
        """Stops playback."""
        if self.process:
            self.process.terminate()
            self.process = None
        self.is_playing = False

    def dj_random(self):
        """Plays a random track from library."""
        tracks = self.scan_library()
        if tracks:
            track = random.choice(tracks)
            print(f"🎧 DJ GABRIEL DROPPING: {track.name}")
            self.play(track, block=False)
            return track.name
        else:
            print("❌ No tracks found in library.")
            return None

if __name__ == "__main__":
    p = GabrielPlayer()
    p.dj_random()
    time.sleep(5)
    p.stop()
