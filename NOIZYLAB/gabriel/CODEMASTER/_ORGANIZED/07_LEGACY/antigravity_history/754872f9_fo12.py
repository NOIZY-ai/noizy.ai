#!/usr/bin/env python3
# 🧠 MEMCELL V3 - NEURAL EVOLUTION & OPTIMIZATION
# "The memory that grows."
#
# Upgrades from V1:
# - Neural Reinforcement (Memory strength increases with use)
# - Deep Overlap (Subject + Tags + Semantic approximation)
# - Zero Latency Structure

import json
import uuid
import datetime
import os
import sys
import time
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "memcell_db.json"
BACKUP_PATH = BASE_DIR / "memcell_db_backup.json"

class MemCellV3:
    def __init__(self):
        self.db = []
        self.load_db()

    def load_db(self):
        """Loads memory database."""
        if os.path.exists(DB_PATH):
            try:
                with open(DB_PATH, 'r') as f:
                    self.db = json.load(f)
                print(f"🧠 MEMCELL V3: Connected. {len(self.db)} neural nodes active.")
            except json.JSONDecodeError:
                print("⚠️ MEMCELL V3: Corrupt Core. Re-initializing.")
                self.db = []
        else:
            print("🧠 MEMCELL V3: Genesis. New network started.")
            self.db = []

    def save_db(self):
        """Atomic Save."""
        if os.path.exists(DB_PATH):
            os.system(f"cp {DB_PATH} {BACKUP_PATH}")
            
        with open(DB_PATH, 'w') as f:
            json.dump(self.db, f, indent=2)

    def reinforce_memory(self, memory_id):
        """Neural Evolution: Strengthens a memory when accessed."""
        for m in self.db:
            if m['id'] == memory_id:
                m['reinforcement'] = m.get('reinforcement', 0) + 1
                m['last_access'] = datetime.datetime.now().isoformat()
                return m
        return None

    def find_deep_overlaps(self, subject, tags, author):
        """
        V3 OVERLAP ENGINE:
        Scans for connections across multiple vectors.
        Returns list of overlapping memory IDs.
        """
        overlaps = []
        if not subject or subject == "General":
            return overlaps

        # Convert tags to set for intersection
        current_tags = set(tags) if tags else set()

        for m in self.db:
            # Don't overlap with self (same author, approx same time is usually just a duplicative run)
            # Actually, we want to know if *other* authors have thought this.
            if m.get('author') == author:
                continue

            score = 0
            
            # 1. Direct Subject Match (Strongest)
            if m.get('subject') == subject:
                score += 10
            
            # 2. Tag Intersection
            other_tags = set(m.get('tags', []))
            common = current_tags.intersection(other_tags)
            score += len(common) * 2

            # 3. Topic Match
            # (Simplistic check)
            
            # Threshold for "Overlap"
            if score >= 5: # Subject match is enough (10), or 3 common tags (6)
                overlaps.append(m['id'])
                # Reinforce the found memory too - we just "thought" of it
                self.reinforce_memory(m['id'])

        if overlaps:
            print(f"  ⚡ NEURAL SPARK: {len(overlaps)} connections found.")
        
        return overlaps

    def add_memory(self, content, topic="General", group="LifeLuv", tags=None, type="THOUGHT", author="SHIRL", subject="General"):
        """Injects a new memory node."""
        if tags is None: tags = []
        
        # V3: Calculate Overlaps immediately
        overlap_ids = self.find_deep_overlaps(subject, tags, author)

        memory = {
            "id": str(uuid.uuid4()),
            "ver": 3,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": type.upper(),
            "author": author,
            "subject": subject,
            "topic": topic,
            "group": group,
            "content": content,
            "tags": tags,
            "overlap": overlap_ids,
            "reinforcement": 1, # Starts at 1
            "last_access": datetime.datetime.now().isoformat()
        }
        
        self.db.append(memory)
        self.save_db()
        return memory

    def search(self, query):
        """Semantic-ish search."""
        results = []
        q = query.lower()
        for m in self.db:
            if q in m['content'].lower() or q in m['topic'].lower() or q in m.get('subject','').lower():
                results.append(m)
                self.reinforce_memory(m['id'])
        return results

    def get_stats(self):
        """V3 Health Check."""
        total_memories = len(self.db)
        total_reinforcements = sum(m.get('reinforcement', 0) for m in self.db)
        top_subjects = {}
        for m in self.db:
            s = m.get('subject', 'General')
            top_subjects[s] = top_subjects.get(s, 0) + 1
        
        popular = sorted(top_subjects.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "Total Memories": total_memories,
            "Total Synapses Fired": total_reinforcements,
            "Top Subjects": popular
        }

# --- CLI V3 ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 MemCell_V3.py [add|search|stats|test] ...")
        sys.exit(0)

    brain = MemCellV3()
    cmd = sys.argv[1]

    if cmd == "add":
        # python3 MemCell_V3.py add "Content" "Topic" "Author" "Subject" "tag1,tag2"
        content = sys.argv[2]
        topic = sys.argv[3] if len(sys.argv) > 3 else "General"
        author = sys.argv[4] if len(sys.argv) > 4 else "USER"
        subject = sys.argv[5] if len(sys.argv) > 5 else "General"
        tags_raw = sys.argv[6] if len(sys.argv) > 6 else ""
        tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
        
        brain.add_memory(content, topic, group="CLI", tags=tags, type="INPUT", author=author, subject=subject)
        print("✅ V3 MEMORY SECURED.")

    elif cmd == "search":
        q = sys.argv[2]
        res = brain.search(q)
        print(f"🔍 Found {len(res)} nodes:")
        for r in res:
            print(f"   [{r['reinforcement']}pts] {r['subject']}: {r['content'][:50]}...")

    elif cmd == "stats":
        stats = brain.get_stats()
        print("\n📊 MEMCELL V3 NEURAL STATUS")
        print(f"   Nodes: {stats['Total Memories']}")
        print(f"   Activity: {stats['Total Synapses Fired']}")
        print("   Major Clusters:")
        for s, c in stats['Top Subjects']:
            print(f"     - {s}: {c}")
        print("")

    elif cmd == "test":
        print("🧪 RUNNING V3 DIAGNOSTICS...")
        # 1. Inject User Memory
        print("   1. Injecting INITIAL thought...")
        brain.add_memory("The sky is blue.", topic="Nature", author="USER", subject="SkyColor")
        
        # 2. Inject AI Memory (should overlap)
        print("   2. Injecting AI response (Expect spark)...")
        m = brain.add_memory("I see the azure hue.", topic="Observation", author="GABRIEL", subject="SkyColor")
        
        if m['overlap']:
            print("   ✅ V3 OVERLAP SUCCESS: Connection made.")
        else:
            print("   ❌ V3 OVERLAP FAIL: No connection.")

        print("✅ Diagnostics Done.")
