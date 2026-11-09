#!/usr/bin/env python3
"""
GABRIEL SONIC CORE - MUSIC INTELLIGENCE ENGINE
Protocol: AUTO-COMPOSER | Tech: Knowledge Graph Traversal
"""

import sys
import time
import random
import glob
from pathlib import Path

class GabrielSonic:
    """
    The Sonic Intelligence of Gabriel.
    Analyzes music knowledge and 'composes' new ideas.
    """
    
    def __init__(self, knowledge_path=None):
        self.knowledge_path = Path(knowledge_path) if knowledge_path else Path.cwd() / "MUSIC_INTELLIGENCE"
        self.concepts = []
        self.genres = ["Techno", "Ambient", "Dubstep", "Cinematic", "Glitch", "Synthwave"]
        self.keys = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
        self.scales = ["Minor", "Major", "Phrygian", "Dorian", "Lydian"]
        
        self.active_project = None
        
    def scan_knowledge(self):
        """Ingest music knowledge files."""
        print(f"🎵 SONIC CORE: Scanning {self.knowledge_path}...")
        files = glob.glob(str(self.knowledge_path / "*.md"))
        
        count = 0
        for f in files:
            # Simple ingestion: just counting for now
            count += 1
            # In V2: We would read content and extract keywords
            
        print(f"🎵 SONIC CORE: Ingested {count} Knowledge Modules.")
        return count

    def generate_prompt(self):
        """Creates a creative music prompt based on internal logic."""
        genre = random.choice(self.genres)
        key = random.choice(self.keys)
        scale = random.choice(self.scales)
        bpm = random.randint(70, 140)
        
        prompt = f"Create a {genre} track in {key} {scale} at {bpm} BPM."
        
        # Add "Genius" twist
        twist = random.choice([
            "Use a granular delay on the hi-hats.",
            "Record found sound from the kitchen.",
            "Limit to only 4 tracks.",
            "Use the Fibonacci sequence for note duration."
        ])
        
        full_prompt = f"{prompt} Constraint: {twist}"
        print(f"\n🎹 AUTO-COMPOSER: {full_prompt}\n")
        return full_prompt

    def start_session(self):
        """Interactive Mode."""
        print("\n🎹 GABRIEL SONIC CORE INITIALIZED.")
        self.scan_knowledge()
        
        while True:
            cmd = input("SONIC > (generate/exit): ").strip().lower()
            if cmd == "exit":
                break
            elif cmd == "generate":
                self.generate_prompt()
            else:
                print("Unknown command.")

if __name__ == "__main__":
    sonic = GabrielSonic()
    sonic.start_session()
