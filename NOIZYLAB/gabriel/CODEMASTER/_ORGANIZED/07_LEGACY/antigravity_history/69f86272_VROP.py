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
        
        # Simple parsing logic
        # 1. Read file
        # 2. Extract headers as Topics
        # 3. Inject into MemCell
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Regex to find headers and content
            # Matches # Header \n content...
            sections = re.split(r'(^|\n)#+\s+', content)
            
            # Skip the first split if empty
            for i in range(1, len(sections), 2):
                if i+1 >= len(sections): break
                
                header = sections[i].strip()
                body = sections[i+1].strip()
                
                if not header or not body: continue
                
                # Check duplication via Search (simple check)
                # In V3, we rely on Overlap/Reinforcement, so re-adding is okay (reinforces!)
                # But to save time on massive run, we might check if 'content' roughly exists.
                # For this implementation, we just Inject. V3 handles dedupe/reinforcement.
                
                # Truncate body if too massive for a single cell (Limit 1000 chars approx)
                if len(body) > 1000:
                    body = body[:1000] + "... [TRUNCATED]"

                self.brain.add_memory(
                    content=body,
                    topic=header,
                    subject=filename,
                    type="KNOWLEDGE",
                    author="INGESTER",
                    tags=["MusicIntelligence", "GeniusMode"]
                )
                self.stats["facts"] += 1
                
                print(f"  🔹 Learned: [{filename}] {header}")

        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")

if __name__ == "__main__":
    ingester = KnowledgeIngester()
    ingester.scan_and_absorb()
