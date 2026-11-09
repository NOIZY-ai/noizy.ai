#!/usr/bin/env python3
# 🧠 KNOWLEDGE INGESTER (MC96 GENIUS LAYER)
# Purpose: Absorb massive documentation into Neural Memory.

import os
import re
import sys
from pathlib import Path

# Adjust path to find MemCell_V3
sys.path.append(str(Path(__file__).parent.resolve()))
try:
    from MemCell_V3 import MemCellV3
except ImportError:
    # Fallback if running from a different CWD
    sys.path.append(str(Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL")))
    from MemCell_V3 import MemCellV3

BASE_DIR = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/MUSIC_INTELLIGENCE")

class KnowledgeIngester:
    def __init__(self):
        self.brain = MemCellV3()
        self.stats = {"files": 0, "facts": 0}

    def scan_and_absorb(self):
        print("🧠 INGESTER: Scanning Knowledge Base...")
        if not BASE_DIR.exists():
            print(f"❌ ERROR: Knowledge Base not found at {BASE_DIR}")
            return

        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                if file.endswith(".md"):
                    self.process_file(Path(root) / file)
        
        print(f"✅ INGESTION COMPLETE. Absorbed {self.stats['facts']} facts from {self.stats['files']} files.")

    def process_file(self, filepath):
        self.stats["files"] += 1
        filename = filepath.name.replace(".md", "").replace("_", " ")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            current_topic = "General"
            current_body = []
            
            for line in lines:
                if line.startswith("#"):
                    # New Section Found
                    # Save previous if exists
                    if current_body:
                        body_text = "".join(current_body).strip()
                        if body_text:
                            self._inject_memory(body_text, current_topic, filename)
                    
                    # Set new topic (remove # and newline)
                    current_topic = line.lstrip("#").strip()
                    current_body = []
                else:
                    current_body.append(line)
            
            # Save last section
            if current_body:
                body_text = "".join(current_body).strip()
                if body_text:
                    self._inject_memory(body_text, current_topic, filename)

        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")

    def _inject_memory(self, content, topic, subject):
        # Truncate if massive
        if len(content) > 2000:
            content = content[:2000] + "... [TRUNCATED]"
            
        self.brain.add_memory(
            content=content,
            topic=topic,
            subject=subject,
            type="KNOWLEDGE",
            author="INGESTER",
            tags=["MusicIntelligence", "GeniusMode"]
        )
        self.stats["facts"] += 1
        # print(f"  🔹 Learned: [{subject}] {topic}") # Reduced noise

if __name__ == "__main__":
    ingester = KnowledgeIngester()
    ingester.scan_and_absorb()
