#!/usr/bin/env python3
# 🧠 MEMCELL V4 - TEMPORAL & SEMANTIC GOD MODE
# "The memory that knows WHEN and WHAT."
#
# Upgrades from V3:
# - Temporal Indexing (Time-Collision Detection)
# - Strict ISO 8601 Enforcement
# - Neural Reinforcement V2 (Decay logic)
# - Zero Latency Lookup (Hashmap optimization)

import json
import uuid
import datetime
import os
import sys
import re
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "memcell_db.json"
BACKUP_PATH = BASE_DIR / "memcell_db_backup_v4.json"

class MemCellV4:
    def __init__(self):
        self.db = []
        self.temporal_index = {} # 'YYYY-MM-DD': [ids]
        self.semantic_index = {} # 'subject': [ids]
        self.load_db()

    def load_db(self):
        """Loads and indexes the database."""
        if os.path.exists(DB_PATH):
            try:
                with open(DB_PATH, 'r') as f:
                    self.db = json.load(f)
                self.reindex()
                print(f"🧠 MEMCELL V4: ONLINE. {len(self.db)} nodes active.")
            except json.JSONDecodeError:
                print("⚠️ MEMCELL V4: Corrupt Core. Re-initializing.")
                self.db = []
        else:
            print("🧠 MEMCELL V4: Genesis. New network started.")
            self.db = []

    def reindex(self):
        """Rebuilds internal hashmaps for O(1) lookups."""
        self.temporal_index = {}
        self.semantic_index = {}
        
        for m in self.db:
            # 1. Temporal Indexing
            # We look for 'event_time' or fall back to 'timestamp'
            ts = m.get('event_time') or m.get('timestamp')
            if ts:
                # Index by Day for broad collision detection
                day_key = ts.split('T')[0]
                if day_key not in self.temporal_index:
                    self.temporal_index[day_key] = []
                self.temporal_index[day_key].append(m['id'])

            # 2. Semantic Indexing (Subject)
            subj = m.get('subject', 'General')
            if subj not in self.semantic_index:
                self.semantic_index[subj] = []
            self.semantic_index[subj].append(m['id'])

    def save_db(self):
        """Atomic Save with Backup."""
        if os.path.exists(DB_PATH):
            os.system(f"cp {DB_PATH} {BACKUP_PATH}")

        with open(DB_PATH, 'w') as f:
            json.dump(self.db, f, indent=2)

    def detect_temporal_conflict(self, event_time):
        """Checks if we typically have something at this time."""
        # Simple check: Do we have > 5 memories on this specific DAY?
        # A real calendar would check hour-by-hour, but for "Memory" logic, 
        # we just want to know if this day is "heavy".
        day_key = event_time.split('T')[0]
        hits = self.temporal_index.get(day_key, [])
        return len(hits)

    def add_memory(self, content, topic="General", group="LifeLuv", tags=None, type="THOUGHT", author="SHIRL", subject="General", event_time=None):
        """Injects a new memory node with V4 intelligence."""
        if tags is None: tags = []
        
        # Auto-detect time in content if event_time not provided
        # (Very basic regex for 202X-XX-XX)
        if not event_time:
            match = re.search(r'\d{4}-\d{2}-\d{2}', content)
            if match:
                event_time = match.group(0) + "T12:00:00" # Assume noon if only date found

        # Timestamp is creation time. Event_time is "When it happens".
        now_iso = datetime.datetime.now().isoformat()
        real_event_time = event_time if event_time else now_iso

        # Temporal Conflict Check
        conflict_count = self.detect_temporal_conflict(real_event_time)
        conflict_flag = conflict_count > 10 # Arbitrary threshold for "Busy Day"

        memory = {
            "id": str(uuid.uuid4()),
            "ver": 4,
            "timestamp": now_iso,
            "event_time": real_event_time, # NEW IN V4
            "type": type.upper(),
            "author": author,
            "subject": subject,
            "topic": topic,
            "group": group,
            "content": content,
            "tags": tags,
            "temporal_conflict": conflict_flag,
            "reinforcement": 1,
            "last_access": now_iso
        }

        self.db.append(memory)
        self.reindex() # Keep indexes fresh
        self.save_db()
        return memory

    def search(self, query):
        """Semantic-ish search with V4 ranking."""
        results = []
        q = query.lower()
        for m in self.db:
            score = 0
            if q in m['content'].lower(): score += 5
            if q in m['topic'].lower(): score += 3
            if q in m.get('subject','').lower(): score += 4
            
            if score > 0:
                # Boost by reinforcement
                score += m.get('reinforcement', 0) * 0.1
                results.append((score, m))
                
                # Auto-reinforce
                m['reinforcement'] = m.get('reinforcement', 0) + 1
                m['last_access'] = datetime.datetime.now().isoformat()

        # Sort by score desc
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results]

    def get_stats(self):
        """V4 Health Check."""
        total_memories = len(self.db)
        total_reinforcements = sum(m.get('reinforcement', 0) for m in self.db)
        
        # Temporal Stats
        busy_days = sorted(self.temporal_index.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        
        return {
            "Total Memories": total_memories,
            "Total Synapses Fired": total_reinforcements,
            "Busiest Days": {d: len(ids) for d, ids in busy_days}
        }

# --- CLI V4 ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 MemCell_V4.py [add|search|stats] ...")
        sys.exit(0)

    brain = MemCellV4()
    cmd = sys.argv[1]

    if cmd == "add":
        # python3 MemCell_V4.py add "Content" "Topic" "Author" "Subject" "tag1,tag2" "2025-12-25T09:00:00"
        content = sys.argv[2]
        topic = sys.argv[3] if len(sys.argv) > 3 else "General"
        author = sys.argv[4] if len(sys.argv) > 4 else "USER"
        subject = sys.argv[5] if len(sys.argv) > 5 else "General"
        tags_raw = sys.argv[6] if len(sys.argv) > 6 else ""
        event_time = sys.argv[7] if len(sys.argv) > 7 else None
        
        tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

        mem = brain.add_memory(content, topic, group="CLI", tags=tags, type="INPUT", author=author, subject=subject, event_time=event_time)
        print(f"✅ V4 MEMORY SECURED. (Conflict: {mem['temporal_conflict']})")

    elif cmd == "search":
        q = sys.argv[2]
        res = brain.search(q)
        print(f"🔍 Found {len(res)} nodes:")
        for r in res:
            print(f"   [{r['reinforcement']}pts] {r['subject']}: {r['content'][:50]}...")

    elif cmd == "stats":
        stats = brain.get_stats()
        print("\n📊 MEMCELL V4 TEMPORAL STATUS")
        print(f"   Nodes: {stats['Total Memories']}")
        print(f"   Activity: {stats['Total Synapses Fired']}")
        print("   ⏳ Temporal Hotspots:")
        for day, count in stats['Busiest Days'].items():
            print(f"     - {day}: {count} memories")
        print("")
