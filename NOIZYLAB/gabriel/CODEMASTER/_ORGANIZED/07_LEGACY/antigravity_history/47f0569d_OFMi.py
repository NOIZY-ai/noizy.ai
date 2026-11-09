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

# Import GraphRAG from packages
try:
    pkg_path = BASE_DIR.parent / "packages" / "memcell"
    sys.path.append(str(pkg_path))
    from graph_rag import get_graph_rag
except ImportError:
    print("⚠️ MEMCELL: GraphRAG module not found. Visualization disabled.")
    get_graph_rag = None

class MemCellCore:
    def __init__(self):
        self.db = []
        self.graph = get_graph_rag() if get_graph_rag else None
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
        
        # Hydrate Graph if empty but DB exists (One-time sync)
        if self.graph and len(self.graph.graph.nodes()) == 0 and len(self.db) > 0:
            print("🧠 MEMCELL: Hydrating Knowledge Graph from Memory DB...")
            for mem in self.db:
                self.graph.add_memcell(mem, auto_save=False)
            self.graph.save()
            print("🧠 MEMCELL: Graph hydration complete.")

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

    def optimize_overlaps(self):
        """
        GENIUS MODE: Semantic Overlap Detection
        Scans all memories to find connections based on keywords and subject matter.
        Links are bidirectional and persistent.
        """
        print(f"  🧠 GENIUS SCAN: Analyzing {len(self.db)} memories for semantic connections...")
        
        updates = 0
        
        # Create a simple keyword map for "Semantic Matching" simulation
        # In a real scenario, this would use embeddings
        keyword_map = {}
        for mem in self.db:
            words = set(mem['content'].lower().split())
            if 'subject' in mem: words.add(mem['subject'].lower())
            if 'topic' in mem: words.add(mem['topic'].lower())
            
            # Filter stop words (very basic)
            stop_words = {'the', 'a', 'is', 'in', 'to', 'of', 'and', 'for', 'with', 'on'}
            unique_keywords = words - stop_words
            
            for word in unique_keywords:
                if len(word) > 4: # Minimal complexity
                    if word not in keyword_map: keyword_map[word] = []
                    keyword_map[word].append(mem['id'])

        # Find collisions
        for word, ids in keyword_map.items():
            if len(ids) > 1:
                # We have a connection!
                for id_a in ids:
                    for id_b in ids:
                        if id_a == id_b: continue
                        
                        # Find memory objects
                        mem_a = next((m for m in self.db if m['id'] == id_a), None)
                        mem_b = next((m for m in self.db if m['id'] == id_b), None)
                        
                        if mem_a and mem_b:
                            if 'overlap' not in mem_a: mem_a['overlap'] = []
                            
                            if id_b not in mem_a['overlap']:
                                mem_a['overlap'].append(id_b)
                                updates += 1
                                # Auto-Graph Trigger
                                if self.graph:
                                    self.graph.graph.add_edge(id_a, id_b, relation="SEMANTIC_LINK", weight=0.5)

        if updates > 0:
            print(f"  ✨ GENIUS RESULT: Discovered {updates} new semantic connections.")
            self.save_db()
        else:
            print("  ✨ GENIUS RESULT: Knowledge Graph is coherent.")
            
        return updates

    def find_overlaps(self, subject, author):
        # Legacy Wrapper
        return []

    def optimize_db(self):
        """Maintains database hygiene"""
        initial_len = len(self.db)
        # Deduplicate by ID
        unique_db = {m['id']: m for m in self.db}.values()
        self.db = sorted(list(unique_db), key=lambda x: x['timestamp'])
        removed = initial_len - len(self.db)
        if removed > 0:
            print(f"✨ Optimized: Removed {removed} duplicates.")
            
        # Run Genius Scan periodically (or on every save for now)
        # self.optimize_overlaps() 
        
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
        
        # Push to Graph
        if self.graph:
            self.graph.add_memcell(memory)
            
        return memory

    def search_memories(self, query):
        """Finds memories matching keyword"""
        results = [m for m in self.db if query.lower() in m['content'].lower() or query.lower() in m['topic'].lower()]
        return results

    def get_recent(self, limit=5):
        """Returns last N memories"""
        return sorted(self.db, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def track_project(self, name, status, notes="", assigned_to=None):
        """Specialized memory for Project Tracking with Team Roster."""
        if assigned_to is None: assigned_to = []

        team_str = f" | Team: {', '.join(assigned_to)}" if assigned_to else ""
        content = f"Project Update: {name} is {status}.{team_str} {notes}"

        # Add assigned_to to tags for easy searching
        extra_tags = ["Tracking", status] + assigned_to

        memory = self.add_memory(content, topic=f"Project: {name}", group="Projects", tags=extra_tags, type="PROJECT", subject=name)

        # Inject metadata if supported (future proofing) or just rely on content/tags
        memory['assigned_to'] = assigned_to
        self.optimize_db() # Save again with new field

        print(f"📊 MEMCELL: Tracking project '{name}' with team {assigned_to}")

    def get_project_roster(self, project_name):
        """Returns the team assigned to a project."""
        # Find latest project update
        updates = [m for m in self.db if m['type'] == 'PROJECT' and project_name.lower() in m['topic'].lower()]
        if not updates:
            return []

        # Sort by latest
        latest = sorted(updates, key=lambda x: x['timestamp'], reverse=True)[0]
        return latest.get('assigned_to', [])

    def register_expertise(self, author, skill):
        """Registers a specific skill for an AI author."""
        # Check if already exists to avoid dupes
        exists = [m for m in self.db if m['type'] == 'EXPERTISE' and m['author'] == author and skill.lower() in m['content'].lower()]
        if exists:
            print(f"  🧠 Known: {author} is already an expert in {skill}.")
            return

        content = f"{author} is an expert in {skill}"
        self.add_memory(content, topic="Expertise Registry", group="Matrix", type="EXPERTISE", author=author, subject="Skill")
        print(f"  🧬 EXPERTISE REGISTERED: {author} -> {skill}")

    def find_expert(self, skill):
        """Finds who is good at a specific skill."""
        experts = []
        for m in self.db:
            if m['type'] == 'EXPERTISE' and skill.lower() in m['content'].lower():
                experts.append(m['author'])
        return list(set(experts))

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

        elif cmd == "expert":
            # Usage: python3 MEMCELL_CORE.py expert "Skill" OR "register" "Author" "Skill"
            sub = sys.argv[2] if len(sys.argv) > 2 else ""
            if sub == "register":
                auth = sys.argv[3]
                skill = sys.argv[4]
                brain.register_expertise(auth, skill)
            else:
                skill = sub
                experts = brain.find_expert(skill)
                if experts:
                    print(f"\n🧬 EXPERTS IN '{skill.upper()}': {', '.join(experts)}")
                else:
                    print(f"No experts found for {skill}")

        elif cmd == "project":
            # Usage: python3 MEMCELL_CORE.py project "Name" "Status" "Notes" "Team,CSV"
            name = sys.argv[2] if len(sys.argv) > 2 else "New Project"
            status = sys.argv[3] if len(sys.argv) > 3 else "Active"
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            team_raw = sys.argv[5] if len(sys.argv) > 5 else ""
            team = [t.strip() for t in team_raw.split(',') if t.strip()]

            brain.track_project(name, status, notes, assigned_to=team)

        elif cmd == "roster":
            name = sys.argv[2]
            team = brain.get_project_roster(name)
            print(f"\n👥 TEAM FOR '{name}': {', '.join(team) if team else 'None assigned'}")

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

            # Test 3: Expertise
            print("  3. Registering Expertise...")
            brain.register_expertise("SHIRL", "Quantum Mechanics")
            experts = brain.find_expert("Quantum")
            if "SHIRL" in experts:
                 print("  ✅ EXPERTISE VERIFIED: SHIRL knows Quantum.")
            else:
                 print("  ❌ EXPERTISE FAILED.")

            print("✅ Diagnostics Complete.")
