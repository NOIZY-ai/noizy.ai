#!/usr/bin/env python3
"""
AUDIO ALIAS MANAGER (Google Drive Prep)
Finds all audio, renames with "NewAge" aliases, and organizes for upload.
"""
import os
import shutil
from pathlib import Path
import datetime

AUDIO_EXTS = {'.wav', '.mp3', '.aif', '.aiff', '.flac', '.ogg'}
SOURCE_ROOT = Path("..") # Scan from NOIZYLAB root (since script is in PROJECTS_MASTER/GABRIEL_CORE or similar) or cwd
DEST_ROOT = Path("../GOOGLE_DRIVE_AUDIO")

class AudioAliasManager:
    def __init__(self):
        self.dest = DEST_ROOT.resolve()
        self.dest.mkdir(parents=True, exist_ok=True)
        self.count = 0

    def generate_alias(self, file_path):
        """
        Creates a "NewAge" alias.
        Format: [Type]_[Name]_[Hash].ext
        Real logic would enable deep analysis. For now, we make it clean.
        """
        original_name = file_path.stem.replace(" ", "_").replace("-", "_")
        parent_folder = file_path.parent.name.replace(" ", "_")
        
        # Simple heuristic for "Mood" based on keywords
        mood = "Raw"
        name_lower = original_name.lower()
        if "pad" in name_lower or "ambient" in name_lower: mood = "Ethereal"
        elif "kick" in name_lower or "bass" in name_lower: mood = "Heavy"
        elif "fx" in name_lower or "sweep" in name_lower: mood = "Cinematic"
        elif "loop" in name_lower: mood = "Rhythmic"
        
        timestamp = datetime.datetime.now().strftime("%f")[:4]
        
        # New Alias: Mood_ParentFolder_OriginalName.ext
        return f"{mood}_{parent_folder}_{original_name}{file_path.suffix}"

    def execute(self):
        print(f"🎵 SCANNING FOR AUDIO IN {Path('.').resolve()}...")
        
        # We assume this script runs from NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE or similar
        # Let's scan the whole NOIZYLAB structure (up one level)
        scan_root = Path("../..").resolve() 
        
        for file_path in scan_root.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in AUDIO_EXTS:
                # Skip the destination folder itself to avoid loops if re-running
                if self.dest in file_path.parents:
                    continue
                    
                alias = self.generate_alias(file_path)
                dest_path = self.dest / alias
                
                print(f"  ✨ Aliasing: {file_path.name} -> {alias}")
                try:
                    shutil.copy2(file_path, dest_path)
                    self.count += 1
                except Exception as e:
                    print(f"  ❌ Error copying {file_path.name}: {e}")

        print(f"\n✅ AUDIO AGGREGATION COMPLETE.")
        print(f"   📂 Total Files: {self.count}")
        print(f"   📍 Location: {self.dest}")

if __name__ == "__main__":
    manager = AudioAliasManager()
    manager.execute()
