#!/usr/bin/env python3
# 🧠 MEMCELL CORE - PERSISTENT AI MEMORY SYSTEM
# Version 1.0 (Built for 2nd Act Rebuild)
# 
# Purpose: Long-term memory storage for Date, Time, Topic, Groups
# Specs: JSON Database, UUID index, Search capability

import json
import uuid
import datetime
import os
import sys
import time

# Configuration
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "memcell_db.json"
BACKUP_PATH = BASE_DIR / "memcell_db_backup.json"

class MemCellCore:
    def __init__(self):
        self.db = []
        self.load_db()

    def load_db(self):
        """Loads memory database from disk"""
        if os.path.exists(DB_PATH):
            try:
                with open(DB_PATH, 'r') as f:
                    self.db = json.load(f)
                print(f"🧠 MEMCELL: Loaded {len(self.db)} memories.")
            except json.JSONDecodeError:
                print("⚠️ MEMCELL: Database corrupted. Starting fresh.")
                self.db = []
        else:
            print("🧠 MEMCELL: New neural network initialized.")
            self.db = []

    def save_db(self):
        """Saves memory database to disk (Atomic write simulation)"""
        # Create backup first if exists
        if os.path.exists(DB_PATH):
            os.system(f"cp {DB_PATH} {BACKUP_PATH}")
            
        with open(DB_PATH, 'w') as f:
            json.dump(self.db, f, indent=2)
        print("💾 MEMCELL: Memory Hard-Saved.")

    def add_memory(self, content, topic="General", group="LifeLuv", tags=None, type="THOUGHT", author="SHIRL", subject="General", overlap=None):
        """Creates a new persistent memory cell with God Mode tracking"""
        if tags is None: tags = []
        if overlap is None: overlap = []
        
        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "god_mode_timestamp": time.time_ns(),
            "type": type.upper(),
            "author": author,
            "subject": subject,
            "topic": topic,
            "group": group,
            "content": content,
            "tags": tags,
            "overlap": overlap
        }
        
        self.db.append(memory)
        self.save_db()
        return memory

    def find_overlaps(self, subject, author):
        """
        GOD MODE: Automatically finds memories with the same subject 
        but from a different author (e.g., if SHIRL speaks, find ENGR's thoughts).
        """
        overlaps = []
        if not subject or subject == "General":
            return overlaps
            
        print(f"  👁️  Scanning for overlaps on subject: '{subject}'...")
        for m in self.db:
            # Match subject, different author
            if m.get('subject') == subject and m.get('author') != author:
                overlaps.append(m['id'])
        
        if overlaps:
            print(f"  🔗 Found {len(overlaps)} overlapping memories from other minds.")
        return overlaps

    def optimize_db(self):
        """Maintains database hygiene"""
        initial_len = len(self.db)
        # Deduplicate by ID
        unique_db = {m['id']: m for m in self.db}.values()
        self.db = sorted(list(unique_db), key=lambda x: x['timestamp'])
        removed = initial_len - len(self.db)
        if removed > 0:
            print(f"✨ Optimized: Removed {removed} duplicates.")
        self.save_db()

    def add_memory(self, content, topic="General", group="LifeLuv", tags=None, type="THOUGHT", author="SHIRL", subject="General", overlap=None):
        """Creates a new persistent memory cell with God Mode tracking"""
        if tags is None: tags = []
        if overlap is None: overlap = []
        
        # 1. Auto-Detect Overlap if not provided
        if not overlap and subject != "General":
            overlap = self.find_overlaps(subject, author)
            
        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "god_mode_timestamp": time.time_ns(),
            "type": type.upper(),
            "author": author,
            "subject": subject,
            "topic": topic,
            "group": group,
            "content": content,
            "tags": tags,
            "overlap": overlap
        }
        
        self.db.append(memory)
        self.optimize_db() # Save included in optimize
        return memory

    def search_memories(self, query):
        """Finds memories matching keyword"""
        results = [m for m in self.db if query.lower() in m['content'].lower() or query.lower() in m['topic'].lower()]
        return results

    def get_recent(self, limit=5):
        """Returns last N memories"""
        return sorted(self.db, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def track_project(self, name, status, notes=""):
        """Specialized memory for Project Tracking"""
        content = f"Project Update: {name} is {status}. {notes}"
        self.add_memory(content, topic=f"Project: {name}", group="Projects", tags=["Tracking", status], type="PROJECT")
        print(f"📊 MEMCELL: Tracking project '{name}'")

    def format_memory_for_display(self, memory):
        """Pretty prints a memory cell"""
        dt = datetime.datetime.fromisoformat(memory['timestamp'])
        fmt_time = dt.strftime("%Y-%m-%d %H:%M")
        
        subject_str = f" [Subj: {memory.get('subject', 'N/A')}]"
        overlap_str = f" [🔗 {len(memory.get('overlap', []))}]" if memory.get('overlap') else ""
        
        return f"[{fmt_time}] [{memory.get('author', 'AI')}]{subject_str}{overlap_str} {memory['topic']}: {memory['content']}"

# --- CLI INTERFACE ---
if __name__ == "__main__":
    brain = MemCellCore()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "add":
            # UPDATED CLI FOR GOD MODE
            # Usage: python3 MEMCELL_CORE.py add "Content" "Topic" "Author" "Subject" "Tags,CSV"
            content = sys.argv[2] if len(sys.argv) > 2 else "Empty thought"
            topic = sys.argv[3] if len(sys.argv) > 3 else "General"
            author = sys.argv[4] if len(sys.argv) > 4 else "SHIRL"
            subject = sys.argv[5] if len(sys.argv) > 5 else "General"
            tags_raw = sys.argv[6] if len(sys.argv) > 6 else ""
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
            
            brain.add_memory(content, topic, author=author, subject=subject, tags=tags)
            print("✅ Memory Injected.")
            
        elif cmd == "list":
            print("\n📜 RECENT MEMORIES:")
            for m in brain.get_recent(10):
                print(brain.format_memory_for_display(m))
                
        elif cmd == "search":
            q = sys.argv[2] if len(sys.argv) > 2 else ""
            print(f"\n🔍 SEARCH RESULTS FOR '{q}':")
            for m in brain.search_memories(q):
                print(brain.format_memory_for_display(m))
                
        elif cmd == "test":
            print("🧪 RUNNING GOD MODE DIAGNOSTICS...")
            
            # Test 1: Injection
            print("  1. Injecting SHIRL memory...")
            m1 = brain.add_memory("The quantum field is vibrating.", topic="Physics", author="SHIRL", subject="Quantum Dynamics")
            
            # Test 2: Overlap
            print("  2. Injecting ENGR memory (Should overlap)...")
            m2 = brain.add_memory("Measuring the vibration frequency.", topic="Measurement", author="ENGR", subject="Quantum Dynamics")
            
            if m1['id'] in m2['overlap']:
                print("  ✅ OVERLAP DETECTED: ENGR saw SHIRL's memory.")
            else:
                print(f"  ❌ OVERLAP FAILED. m2 overlap: {m2['overlap']}")
                
            print("✅ Diagnostics Complete.")
        
        elif cmd == "project":
            # Usage: python3 MEMCELL_CORE.py project "Name" "Status" "Notes"
            name = sys.argv[2] if len(sys.argv) > 2 else "New Project"
            status = sys.argv[3] if len(sys.argv) > 3 else "Active"
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            brain.track_project(name, status, notes)

    else:
        print("Usage: python3 MEMCELL_CORE.py [add|list|search|test|project]")
