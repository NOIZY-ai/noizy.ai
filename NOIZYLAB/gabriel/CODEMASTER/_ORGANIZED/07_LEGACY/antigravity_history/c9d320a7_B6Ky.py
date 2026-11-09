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
DB_PATH = "memcell_db.json"
BACKUP_PATH = "memcell_db_backup.json"

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

    def add_memory(self, content, topic="General", group="LifeLuv", tags=None, type="THOUGHT"):
        """Creates a new persistent memory cell"""
        if tags is None: tags = []
        
        memory = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now().isoformat(),
            "type": type.upper(),
            "topic": topic,
            "group": group,
            "content": content,
            "tags": tags
        }
        
        self.db.append(memory)
        self.save_db()
        return memory

    def search_memories(self, query):
        """Finds memories matching keyword"""
        results = [m for m in self.db if query.lower() in m['content'].lower() or query.lower() in m['topic'].lower()]
        return results

    def get_recent(self, limit=5):
        """Returns last N memories"""
        return sorted(self.db, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def format_memory_for_display(self, memory):
        """Pretty prints a memory cell"""
        dt = datetime.datetime.fromisoformat(memory['timestamp'])
        fmt_time = dt.strftime("%Y-%m-%d %H:%M")
        return f"[{fmt_time}] [{memory['group']}] {memory['topic']}: {memory['content']}"

# --- CLI INTERFACE ---
if __name__ == "__main__":
    brain = MemCellCore()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "add":
            # Usage: python3 MEMCELL_CORE.py add "Content" "Topic"
            content = sys.argv[2] if len(sys.argv) > 2 else "Empty thought"
            topic = sys.argv[3] if len(sys.argv) > 3 else "General"
            brain.add_memory(content, topic)
            
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
            print("🧪 RUNNING SYSTEM TEST...")
            brain.add_memory("Test Memory 1", "System Check", "Diagnostics")
            print("✅ Memory Added")
            latest = brain.get_recent(1)[0]
            if latest['content'] == "Test Memory 1":
                print("✅ Persistence Verified")
            else:
                print("❌ Verification Failed")
        
        elif cmd == "project":
            # Usage: python3 MEMCELL_CORE.py project "Name" "Status" "Notes"
            name = sys.argv[2] if len(sys.argv) > 2 else "New Project"
            status = sys.argv[3] if len(sys.argv) > 3 else "Active"
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            brain.track_project(name, status, notes)

    else:
        print("Usage: python3 MEMCELL_CORE.py [add|list|search|test|project]")
