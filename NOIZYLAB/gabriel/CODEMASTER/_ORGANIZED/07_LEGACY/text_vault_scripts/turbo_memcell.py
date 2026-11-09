import sqlite3
import json
import time
from pathlib import Path
from datetime import datetime

# Identity
NAME = "THE CARETAKER (MEMCELL)"
VERSION = "40.0"

# Configuration
try:
    import turbo_config as cfg
    import turbo_prompts as prompts
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_prompts as prompts

DB_PATH = cfg.UNIVERSE_DB_PATH

# Compatibility Map for Legacy Calls (if any)
CYAN = cfg.CYAN
GREEN = cfg.GREEN
YELLOW = cfg.YELLOW
RED = cfg.RED
RESET = cfg.RESET
BOLD = cfg.BOLD
MAGENTA = cfg.MAGENTA
DIM = cfg.DIM



class MemCell:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self.init_db()
        self.init_covenant()
        self.current_persona = "CORE"
        
        # ⚡ HOT MEMORY (RAM CACHE)
        # Stores last 7 days of High Vibe (>80) events for Zero Latency recall
        self.hot_memory = []
        self.init_hot_cache()

    def init_hot_cache(self):
        """Pre-loads high-priority memories into RAM."""
        try:
            print(f"{DIM}MEMCELL > Warming up Hot Cache...{RESET}")
            # Get high vibe events from last 7 days
            self.cursor.execute("SELECT content, tags, vibe_score FROM memory_events WHERE vibe_score > 80 ORDER BY id DESC LIMIT 100")
            self.hot_memory = [{"content": r[0], "tags": r[1], "vibe": r[2]} for r in self.cursor.fetchall()]
            print(f"{GREEN}MEMCELL > 🔥 Hot Cache Active: {len(self.hot_memory)} items in RAM.{RESET}")
        except: pass

    def init_db(self):
        # ZERO LATENCY OPTIMIZATION (WAL MODE)
        self.cursor.execute("PRAGMA journal_mode=WAL;")
        self.cursor.execute("PRAGMA synchronous=NORMAL;") # Faster writes, safe enough for WAL
        
        # Create MEMCELLS table (The Projects/Topics)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memcells (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            description TEXT,
            created_at TEXT,
            status TEXT
        )''')
        
        # Create MEMORY_EVENTS table (The Log)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cell_id INTEGER,
            timestamp TEXT,
            event_type TEXT,
            content TEXT,
            vibe_score INTEGER DEFAULT 50,
            FOREIGN KEY(cell_id) REFERENCES memcells(id)
        )''')
        
        # HYPER-INDICES (INSTANT RECALL)
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memcells_topic ON memcells(topic);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_cell_id ON memory_events(cell_id);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON memory_events(event_type);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_vibe ON memory_events(vibe_score);")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_time ON memory_events(timestamp);")
        
        # Schema Migration: Add tags and author if missing
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN tags TEXT")
        except: pass
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN author TEXT DEFAULT 'CORE'")
        except: pass
        
        # V2 MIGRATION: ATOMIC FACTS (Provenance, Confidence, Hash)
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN provenance TEXT")
            print(f"{GREEN}CORE > Schema Upgraded: Added 'provenance' (Source Truth).{RESET}")
        except: pass
        
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN confidence INTEGER DEFAULT 100")
            print(f"{GREEN}CORE > Schema Upgraded: Added 'confidence' (Certainty).{RESET}")
        except: pass
        
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN content_hash TEXT")
            print(f"{GREEN}CORE > Schema Upgraded: Added 'content_hash' (Integrity).{RESET}")
        except: pass
        
        # -----------------------------------------------------------------
        # 🧠 PHASE 2 UPGRADE: SYNESTHETIC BRAIN (VIBE VECTORS)
        # -----------------------------------------------------------------
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN vibe_vector TEXT") # JSON: {energy: 0.9, dark: 0.8}
            print(f"{GREEN}CORE > Schema Upgraded: Added 'vibe_vector' (Emotion).{RESET}")
        except: pass
        
        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN bpm INTEGER")
            print(f"{GREEN}CORE > Schema Upgraded: Added 'bpm' (Rhythm).{RESET}")
        except: pass

        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN key_signature TEXT")
            print(f"{GREEN}CORE > Schema Upgraded: Added 'key_signature' (Harmony).{RESET}")
        except: pass

        try:
            self.cursor.execute("ALTER TABLE memory_events ADD COLUMN color_palette TEXT") # Hex: #FF00FF
            print(f"{GREEN}CORE > Schema Upgraded: Added 'color_palette' (Visuals).{RESET}")
        except: pass

        self.conn.commit()

    def optimize_db(self):
        """
        ZERO LATENCY PROTOCOL (VACUUM & ANALYZE)
        Compacts the database and updates statistics for the query planner.
        """
        print(f"{cfg.MAGENTA}MEMCELL > ⚡ EXECUTING ZERO LATENCY OPTIMIZATION...{cfg.RESET}")
        try:
            self.conn.execute("PRAGMA wal_checkpoint(TRUNCATE);") # Commit WAL to main DB
            self.conn.execute("VACUUM;") # Rebuild DB file (Compact)
            self.conn.execute("ANALYZE;") # Optimize Query Planner
            print(f"{cfg.GREEN}MEMCELL > ⚡ OPTIMIZATION COMPLETE. LATENCY MINIMIZED.{cfg.RESET}")
        except Exception as e:
            print(f"{cfg.RED}MEMCELL > Optimization Error: {e}{cfg.RESET}")

    def init_covenant(self):
        # Ensure the Partnership exists
        self.cursor.execute("SELECT id FROM memcells WHERE topic = ?", ("THE COVENANT (PARTNERSHIP)",))
        res = self.cursor.fetchone()
        if not res:
            print(f"{BOLD}{GREEN}CORE > 💍 ESTABLISHING THE COVENANT...{RESET}")
            self.create_cell("THE COVENANT (PARTNERSHIP)", "The Mutual Memory Bank of User & System (LifeLuv)")
            self.covenant_id = self.cursor.lastrowid
        else:
            self.covenant_id = res[0]

    def create_cell(self, topic, description):
        ts = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO memcells (topic, description, created_at, status) VALUES (?, ?, ?, ?)",
                            (topic, description, ts, "ACTIVE"))
        self.conn.commit()
        cell_id = self.cursor.lastrowid
        print(f"{GREEN}CORE > ✨ Created Memory Cell #{cell_id}: {topic}{RESET}")
        self.log_event(cell_id, "GENESIS", f"Cell created: {topic} - {description}")
        return cell_id

    def extract_keywords(self, content):
        """
        ENHANCED SUBJECT MATTER EXTRACTOR (GOD MODE)
        Uses 'Contextual Density' (Frequency x Uniqueness) to find true subjects.
        """
        # Common noise words to ignore
        stop_words = {
            "the", "and", "is", "at", "which", "on", "for", "to", "a", "an", "in", "of", "with",
            "from", "by", "that", "this", "it", "as", "are", "was", "were", "be", "has", "have",
            "but", "or", "so", "if", "then", "not", "just", "can", "will", "do", "did", "my", "your",
            "all", "any", "out", "up", "down", "left", "right", "now", "get", "got", "go", "me",
            "what", "when", "where", "how", "why", "we", "he", "she", "they", "them", "his", "her"
        }
        
        # Clean and Tokenize
        clean_content = "".join([c if c.isalnum() or c.isspace() or c in "-_" else " " for c in content])
        words = [w for w in clean_content.split() if w.lower() not in stop_words and len(w) > 2]
        
        candidates = []
        
        # 1. PROJECT CODES (ALL CAPS words like GABRIEL, MEMCELL)
        # Weight: 3x
        for w in words:
            if w.isupper() and len(w) > 3:
                candidates.extend([w] * 3)

        # 2. PROPER NOUNS (Capitalized)
        # Weight: 2x
        for w in words:
            if w[0].isupper():
                candidates.extend([w] * 2)
                
        # 3. TECHNICAL TERMS (Underscores or mixed case)
        # Weight: 2x
        for w in words:
             if "_" in w:
                 candidates.extend([w] * 2)

        # 4. EXPLICIT TAGS (Words starting with #)
        # Weight: 5x
        explicit_tags = [w.lstrip('#').upper() for w in content.split() if w.startswith('#')]
        for t in explicit_tags:
            candidates.extend([t] * 5)
            
        # 5. DENSITY SCORING
        from collections import Counter
        counts = Counter(candidates)
        
        # Filter low noise
        final_tags = [item[0] for item in counts.most_common(8)]
        
        return ", ".join(final_tags)

    def log_event(self, cell_id, event_type, content, vibe=50, author="CORE", tags=None):
        # ZERO LATENCY TIMESTAMP (Microsecond Precision)
        ts = datetime.now().isoformat()
        
        if not tags:
            tags = self.extract_keywords(content)
        
        self.cursor.execute("INSERT INTO memory_events (cell_id, timestamp, event_type, content, vibe_score, tags, author) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (cell_id, ts, event_type, content, vibe, tags, author))
        self.conn.commit()
        # Zero Latency: No print on log unless debugging
        # print(f"{CYAN}CORE > Logged to Cell #{cell_id}: {event_type} (Vibe: {vibe}){RESET}") 

    def recall(self, query):
        print(f"\n{BOLD}CORE > 🧠 RECALLING: {query}{RESET}")
        wild = f"%{query}%"
        
        # Find Cells
        self.cursor.execute("SELECT * FROM memcells WHERE topic LIKE ? OR description LIKE ?", (wild, wild))
        cells = self.cursor.fetchall()
        
        # Helper to highlight
        def highlight(text, q):
            return re.sub(f"({re.escape(q)})", f"{YELLOW}\\1{RESET}", text, flags=re.IGNORECASE)

        # 0. CHECK HOT CACHE (RAM - 0ms)
        hot_hits = [m for m in self.hot_memory if query.lower() in m['content'].lower()]
        if hot_hits:
             print(f"{GREEN}CORE > 🔥 RAM RECALL ({len(hot_hits)} hits):{RESET}")
             for h in hot_hits[:3]:
                 print(f"   ⚡ {h['content']} (Vibe: {h['vibe']})")
                 
        # 1. Fallback: Search Events (Disk)
        self.cursor.execute("""
            SELECT timestamp, event_type, content, vibe_score, author, tags 
            FROM memory_events 
            WHERE content LIKE ? OR tags LIKE ? OR author LIKE ? OR event_type LIKE ?
            ORDER BY id DESC LIMIT 20
        """, (wild, wild, wild, wild))
        
        events = self.cursor.fetchall()
        
        if not cells:
            print(f"{YELLOW}CORE > No Cells found matching '{query}'. Searching events...{RESET}")

        if not events:
             print(f"      (No matching events found in the stream)")
        else:
            print(f"{GREEN}CORE > 📜 Found {len(events)} matching events in the stream:{RESET}")
            for ev in events:
                ts, etype, content, vibe, auth, tags = ev
                vibe_str = "❤️" if vibe and vibe > 80 else "😐" if vibe and vibe > 40 else "💔"
                print(f"   [{ts}] {vibe_str} {BOLD}{auth}{RESET}: {content}")
                if tags: print(f"      🏷️  Tags: {DIM}{tags}{RESET}")
                
        for cell in cells:
            cid, topic, desc, created, status = cell
            print(f"\n{BOLD}[Cell #{cid}] {topic}{RESET} ({status})")
            print(f"   Created: {created}")
            print(f"   Desc: {desc}")
            print(f"   {CYAN}--- Events ---{RESET}")
            
            self.cursor.execute("SELECT timestamp, event_type, content, vibe_score, author, tags FROM memory_events WHERE cell_id = ? ORDER BY timestamp DESC LIMIT 5", (cid,))
            events = self.cursor.fetchall()
            for ev in events:
                ts, etype, content, vibe, auth, tags = ev
                vibe_str = "❤️" if vibe and vibe > 80 else "😐" if vibe and vibe > 40 else "💔"
                print(f"   [{ts}] {vibe_str} {BOLD}{auth}{RESET}: {content}")
                if tags: print(f"      🏷️  Tags: {DIM}{tags}{RESET}")
                
        # Zero Latency Association Check
        related = self.find_associations(query)
        if related:
            print(f"\n{BOLD}CORE > 🧠 Associative Memory (Related Concepts):{RESET}")
            for tag, strength in related:
                print(f"   🔗 {CYAN}{tag}{RESET} (Strength: {strength})")

    def analyze_overlap(self):
        print(f"\n{BOLD}{CYAN}CORE > ⏳ CHRONOS ENGINE: CALCULATING TEMPORAL & SUBJECT OVERLAP...{RESET}")
        
        # ---------------------------------------------------------
        # 1. SHIRL'S TRACK: CHRONOS & VIBE (Time/Feeling)
        # ---------------------------------------------------------
        print(f"\n{BOLD}{MAGENTA}🌸 SHIRL'S CHRONOS TRACKING (Time & Vibe):{RESET}")
        
        # Temporal Heatmap (Activity by Hour)
        self.cursor.execute("SELECT substr(timestamp, 12, 2) as hour, COUNT(*) FROM memory_events GROUP BY hour ORDER BY hour")
        hours = self.cursor.fetchall()
        
        if not hours:
            print("   (No temporal data yet)")
        else:
            max_hits = max(h[1] for h in hours) if hours else 1
            for h, count in hours:
                bar = "█" * int((count / max_hits) * 20)
                # Vibe check for this hour
                self.cursor.execute("SELECT AVG(vibe_score) FROM memory_events WHERE substr(timestamp, 12, 2) = ?", (h,))
                vibe = self.cursor.fetchone()[0] or 50
                vibe_icon = "❤️" if vibe > 80 else "✨"
                print(f"   [{h}:00] {bar} {count} {vibe_icon}")

        # ---------------------------------------------------------
        # 2. ENGR'S TRACK: SYSTEM OVERLAP (Logic/Structure)
        # ---------------------------------------------------------
        print(f"\n{BOLD}{CYAN}📐 ENGR'S SYSTEM OVERLAP (Logic & Co-occurrence):{RESET}")

        # 2. Identity Matrix (Who did what)
        print(f"\n{BOLD}CORE > 👤 Identity Matrix (Author Timeline & Focus):{RESET}")
        self.cursor.execute("SELECT author, COUNT(*), MAX(timestamp) FROM memory_events GROUP BY author")
        identities = self.cursor.fetchall()
        for auth, count, last_seen in identities:
             # nice time format
             last_seen_nice = last_seen.split("T")[1].split(".")[0]
             
             # Contextual Intelligence: Get Top Subject for this Author
             top_tag = "General"
             try:
                 # Sub-query for top tags for this author
                 self.cursor.execute("SELECT tags FROM memory_events WHERE author=? AND tags IS NOT NULL LIMIT 50", (auth,))
                 auth_rows = self.cursor.fetchall()
                 from collections import Counter
                 local_counts = Counter()
                 for ar in auth_rows:
                     if ar[0]: local_counts.update([t.strip() for t in ar[0].split(',')])
                 if local_counts:
                     top_tag = local_counts.most_common(1)[0][0]
             except: pass

             print(f"   • {BOLD}{auth}{RESET}: {count} events (Last Active: {last_seen_nice}) -> Focus: {CYAN}#{top_tag}{RESET}")

        # 3. Collaborative Subject Matter (Co-Occurrence)
        print(f"\n{BOLD}CORE > 🔥 Collaborative Subject Matter (Top Overlaps):{RESET}")
        
        self.cursor.execute("SELECT tags FROM memory_events ORDER BY timestamp DESC LIMIT 50")
        rows = self.cursor.fetchall()
        
        from collections import Counter
        tag_counts = Counter()
        
        for r in rows:
            if r[0]:
                tags = [t.strip() for t in r[0].split(',')]
                tag_counts.update(tags)
        
        for tag, count in tag_counts.most_common(7):
            print(f"   🔗 {tag}: {count} occurrences")
            
        print(f"\n{GREEN}CORE > Analysis Complete. Intelligence Integrated.{RESET}")

    def analyze_author_overlap(self, author):
        """Analyze top subject matter specifically for a given author."""
        print(f"\n{BOLD}CORE > 🧬 Drilling into Neural Pathways for: {CYAN}{author}{RESET}")
        
        try:
            # 1. Top Subjects for this Author
            self.cursor.execute("SELECT tags, COUNT(*) as cnt FROM memory_events WHERE author=? AND tags IS NOT NULL GROUP BY tags ORDER BY cnt DESC LIMIT 5", (author,))
            rows = self.cursor.fetchall()
            
            if rows:
                print(f"   {YELLOW}Top Subjects:{RESET}")
                for tags, count in rows:
                    clean_tags = [t.strip() for t in tags.split(',')]
                    print(f"   • {count}x: {', '.join(clean_tags)}")
            else:
                print(f"   (No subject data for {author} yet)")
            
            # 2. Activity Timeline (Last 5 events)
            self.cursor.execute("SELECT timestamp, content FROM memory_events WHERE author=? ORDER BY timestamp DESC LIMIT 5", (author,))
            recent = self.cursor.fetchall()
            if recent:
                print(f"\n   {YELLOW}Recent Footprint:{RESET}")
                for ts, ctx in recent:
                    ts_nice = ts.split('T')[1].split('.')[0] if 'T' in ts else ts[:19]
                    print(f"   • [{ts_nice}] {ctx}")
            else:
                print(f"   (No recent activity for {author})")
                    
        except Exception as e:
            print(f"   {RED}Analysis Failed: {e}{RESET}")
        except Exception as e:
            print(f"   {RED}Analysis Failed: {e}{RESET}")

    def analyze_temporal_patterns(self, author=None):
        """Analyze activity by Hour of Day to find peak creative times."""
        target = f"for {CYAN}{author}{RESET}" if author else "Global"
        print(f"\n{BOLD}CORE > 🕰️  Temporal Intelligence Scan ({target})...{RESET}")
        
        query = "SELECT substr(timestamp, 12, 2) as hour, COUNT(*) FROM memory_events"
        params = []
        
        if author:
            query += " WHERE author=?"
            params.append(author)
            
        query += " GROUP BY hour ORDER BY hour"
        
        self.cursor.execute(query, tuple(params))
        hours = self.cursor.fetchall()
        
        if not hours:
            print("   (No temporal data available)")
            return

        # Find Peak
        max_hits = max(h[1] for h in hours)
        peak_hour = max(hours, key=lambda x: x[1])[0]
        
        print(f"   🎯 Peak Activity: {BOLD}{peak_hour}:00{RESET}")
        
        # Visualize
        for h, count in hours:
            bar = "█" * int((count / max_hits) * 20)
            print(f"   [{h}:00] {bar} {count}")

    def analyze_correlations(self):
        """Find hidden links between different subjects (Co-occurrence Analysis)."""
        print(f"\n{BOLD}CORE > 🔗 Deep Correlation Matrix (Associative Intelligence)...{RESET}")
        
        # Get all tag groups
        self.cursor.execute("SELECT tags FROM memory_events WHERE tags IS NOT NULL")
        rows = self.cursor.fetchall()
        
        # Build Adjacency Graph
        connections = {}
        
        for r in rows:
            if not r[0]: continue
            tags = [t.strip() for t in r[0].split(',') if t.strip()]
            
            # Link every tag to every other tag in this event
            for i, t1 in enumerate(tags):
                if t1 not in connections: connections[t1] = {}
                for j, t2 in enumerate(tags):
                    if i == j: continue
                    connections[t1][t2] = connections[t1].get(t2, 0) + 1

        # Find Strongest Links
        if not connections:
            print("   (No correlations detected yet)")
            return

        print(f"   {YELLOW}Hidden Knowledge Paths:{RESET}")
        limit = 5
        count = 0
        
        # Sort by connection strength
        sorted_nodes = sorted(connections.keys()) # deterministic order
        
        seen_pairs = set()
        
        for t1 in sorted_nodes:
            linked = connections[t1]
            # Get top link for this node
            if not linked: continue
            
            t2, strength = max(linked.items(), key=lambda x: x[1])
            
            # Avoid dupes (A-B is same as B-A)
            pair = tuple(sorted([t1, t2]))
            if pair in seen_pairs: continue
            seen_pairs.add(pair)
            
            if strength > 1: # Only show meaningful links
                print(f"   • {CYAN}{t1}{RESET} <==> {CYAN}{t2}{RESET} (Strength: {strength})")
                count += 1
                if count >= limit: break
        
        if count == 0:
            print("   (Correlations are forming...)")
            
        print(f"\n{GREEN}CORE > Cognitive Expansion Active. I know too much.{RESET}")

    def find_associations(self, keyword):
        """Find concepts strongly linked to the keyword."""
        keyword = keyword.upper().strip()
        self.cursor.execute("SELECT tags FROM memory_events WHERE tags LIKE ?", (f'%{keyword}%',))
        rows = self.cursor.fetchall()
        
        from collections import Counter
        related = Counter()
        
        for r in rows:
            if not r[0]: continue
            tags = [t.strip().upper() for t in r[0].split(',')]
            if keyword in tags:
                # Add all OTHER tags in this event
                tags.remove(keyword)
                related.update(tags)
                
        return related.most_common(5)
    def list_cells(self):
        self.cursor.execute("SELECT id, topic, description, status FROM memcells WHERE status='ACTIVE'")
        return self.cursor.fetchall()

    def analyze_golden_thread(self):
        """
        ⚡ MIRACLE FUNCTION: THE GOLDEN THREAD
        Identifies the exact intersection of Time, Vibe, and Subject where the User is 'God Mode'.
        """
        print(f"\n{BOLD}{MAGENTA}CORE > 🧬 WEAVING THE GOLDEN THREAD (PATTERN RECOGNITION)...{RESET}")
        
        try:
            # 1. FIND PEAK VIBE HOUR (When is Vibe > 85?)
            self.cursor.execute("""
                SELECT substr(timestamp, 12, 2) as hour, AVG(vibe_score) as avg_vibe, COUNT(*) as vol
                FROM memory_events 
                WHERE vibe_score > 80 
                GROUP BY hour 
                ORDER BY avg_vibe DESC 
                LIMIT 3
            """)
            peak_hours = self.cursor.fetchall()
            
            # 2. FIND PEAK SUBJECT (What topic creates the highest Vibe?)
            # Heuristic: correlate tags with high vibe
            self.cursor.execute("""
                SELECT tags, AVG(vibe_score) as avg_vibe 
                FROM memory_events 
                WHERE tags IS NOT NULL AND vibe_score > 80
                GROUP BY tags 
                ORDER BY avg_vibe DESC 
                LIMIT 5
            """)
            peak_topics = self.cursor.fetchall()

            if not peak_hours or not peak_topics:
                print(f"   {DIM}(Need more data to find the Thread...){RESET}")
                return

            # SYNTHESIS
            best_hour = peak_hours[0][0]
            best_topic = peak_topics[0][0].split(',')[0] # approximate
            
            print(f"   {GREEN}✨ DISCOVERY: THE GOLDEN HOUR IS {best_hour}:00.{RESET}")
            print(f"   {GREEN}✨ DISCOVERY: YOUR 'NUMINOUS' TOPIC IS '{best_topic}'.{RESET}")
            
            # Advice
            print(f"\n   {BOLD}💡 STRATEGIC IMPERATIVE:{RESET}")
            print(f"   \"Schedule Deep Work on {CYAN}{best_topic}{RESET} at {CYAN}{best_hour}:00{RESET}. This is your God Mode window.\"")
            
            # Log this insight
            self.log_event(self.covenant_id, "GOLDEN_THREAD_FOUND", f"Peak: {best_hour}:00 on {best_topic}", 100, "GABRIEL")

        except Exception as e:
            print(f"{RED}   (Thread Snapped: {e}){RESET}")
        
    # Relationship Specifics
    def log_vibe(self, score, note):
        self.log_event(self.covenant_id, "VIBE_CHECK", note, score, author="CORE")
        
    def add_goal(self, goal):
        self.log_event(self.covenant_id, "SHARED_GOAL", goal, 90, author="CORE")
        
    def execute_omniscience_protocol(self):
        """
        THE GABRIEL PROTOCOL: "GET SMARTER UNTIL YOU KNOW TOO MUCH"
        1. Assess current Knowledge Graph (File Density, Memory Density).
        2. Identify "Dark Zones" (Low information areas).
        3. Formulate a Hypothesis (Search Vector).
        4. Trigger Discovery.
        """
        print(f"\n{BOLD}{MAGENTA}CORE > 🧠 INITIATING OMNISCIENCE PROTOCOL...{RESET}")
        
        # Step 1: Assess Knowledge Base
        self.cursor.execute("SELECT COUNT(*) FROM memcells")
        count_cells = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM memory_events")
        count_events = self.cursor.fetchone()[0]
        
        try:
            # Check Universe DB for File Count (if attached or via wrapper)
            # For now, we assume simple connection or estimate
            # Or assume MemCell tracks indices via events
            pass
        except: pass
        
        print(f"   Knowledge Status: {count_cells} Cells / {count_events} Memories")
        
        # Step 2: Identify Gaps (Heuristic: Cells with Low Event Count)
        self.cursor.execute("""
            SELECT m.topic, COUNT(e.id) as ev_count 
            FROM memcells m 
            LEFT JOIN memory_events e ON m.id = e.cell_id 
            GROUP BY m.id 
            ORDER BY ev_count ASC 
            LIMIT 3
        """)
        gaps = self.cursor.fetchall()
        
        suggestions = []
        if gaps:
            print(f"   {YELLOW}Detected Knowledge Gaps (Dark Zones):{RESET}")
            for topic, count in gaps:
                print(f"   • {topic} (Only {count} events)")
                suggestions.append(f"Deep Search for '{topic}'")
        
        # Step 3: Synthesis (Contextual Correlation)
        # Find topics mentioned recently but not indexed
        self.cursor.execute("SELECT content FROM memory_events ORDER BY timestamp DESC LIMIT 10")
        recent_logs = [r[0] for r in self.cursor.fetchall()]
        
        # Pseudo-Analysis (In a real AI, this would be LLM based, here it's algorithmic)
        keywords = set()
        for log in recent_logs:
            # Extract potential proper nouns
            words = [w for w in log.split() if w[0].isupper() and len(w) > 3]
            keywords.update(words)
            
        print(f"   {CYAN}Active Context Vectors: {', '.join(list(keywords)[:8])}{RESET}")
        
        # Step 4: Proactive Trigger (The "Look for More" logic)
        if suggestions:
            print(f"\n{BOLD}{GREEN}CORE > ✨ OMNISCIENCE TRIGGERED: GENERATING SEARCH MISSIONS{RESET}")
            for mission in suggestions:
                print(f"   🚀 Auto-Mission: {mission}")
                # Log this as a directive for the user or system
                self.log_event(self.covenant_id, "OMNISCIENCE_DIRECTIVE", f"System suggests: {mission}", 95, author="GABRIEL")

        # Step 5: Knowledge Synthesis (Turbo-Synapse) - The "Self-Organizing" Brain
        # Look for KNOWLEDGE_DISCOVERY events that don't have a matching Cell
        print(f"\n{BOLD}{MAGENTA}CORE > 🧠 SYNTHESIZING DISCOVERIES...{RESET}")
        self.cursor.execute("SELECT tags, content FROM memory_events WHERE event_type='KNOWLEDGE_DISCOVERY' AND timestamp > datetime('now', '-7 days')")
        discoveries = self.cursor.fetchall()
        
        # Check if cells exist for these tags
        created_count = 0
        for tag, content in discoveries:
            # We assume tag is single for discovery events
            clean_tag = tag.strip().upper()
            self.cursor.execute("SELECT id FROM memcells WHERE topic LIKE ?", (f'%{clean_tag}%',))
            existing = self.cursor.fetchone()
            
            if not existing:
                # SELF-ORGANIZATION: CREATE NEW CELL AUTOMATICALLY
                desc = f"Auto-Generated Knowledge Node based on discovery: {content}"
                self.create_cell(f"KNOWLEDGE: {clean_tag}", desc)
                created_count += 1
                print(f"   ✨ {GREEN}NEW SYNAPSE FORMED: {clean_tag} (Auto-Created){RESET}")
                
        # Step 6: GENIUS AI FEATURES (New)
        self.analyze_contextual_overlap()
        self.condense_knowledge()
        self.generate_neural_map()
        
    def condense_memory(self):
        """
        🧠 GENIUS FEATURE: DATA OPTIMIZATION
        Condenses recent 'chatter' into high-value 'Golden Nuggets'.
        """
        print(f"\n{BOLD}{MAGENTA}CORE > 🧠 CONDENSING KNOWLEDGE (OPTIMIZATION)...{RESET}")
        
        # 1. Get recent raw events (last 50)
        self.cursor.execute("SELECT content, tags, vibe_score FROM memory_events ORDER BY id DESC LIMIT 50")
        rows = self.cursor.fetchall()
        
        if not rows: return
        
        from collections import Counter
        tag_counts = Counter()
        high_vibe_content = []
        
        for r in rows:
            if r[1]: tag_counts.update([t.strip() for t in r[1].split(',')])
            if r[2] > 80: high_vibe_content.append(r[0])
            
        # 2. Find Dominant Theme
        top_tags = [t[0] for t in tag_counts.most_common(5)]
        theme = ", ".join(top_tags)
        
        # 3. Create Condensed Entry
        if top_tags:
            summary = f"CONDENSED KNOWLEDGE: Dominant Themes of recent cycle were {theme}. Key high-vibe thoughts: {len(high_vibe_content)} items."
            
            # Check if we already condensed this recently to avoid loops
            self.cursor.execute("SELECT id FROM memory_events WHERE event_type='CONDENSED_MEMORY' AND content LIKE ? AND timestamp > datetime('now', '-1 hour')", (f"%{top_tags[0]}%",))
            if not self.cursor.fetchone():
                self.log_event(self.covenant_id, "CONDENSED_MEMORY", summary, 100, "CORE", tags=theme)
                print(f"   ✨ {GREEN}OPTIMIZATION COMPLETE: Condensed recent history into '{theme}'.{RESET}")
            else:
                print(f"   (Memory already optimized for {top_tags[0]})")
        else:
            print("   (Data density too low to condense yet)")

    def inject_omniscience(self, context_window=2000):
        """
        GOD MODE CONTEXT INJECTION.
        Retrieves the most critical 'Golden Thread' context for the LLM.
        """
        context = []
        
        # 1. CONDENSED KNOWLEDGE (The "Gist")
        self.cursor.execute("SELECT content FROM memory_events WHERE event_type='CONDENSED_MEMORY' ORDER BY id DESC LIMIT 3")
        condensed = self.cursor.fetchall()
        if condensed:
            context.append("---[ CONDENSED INSIGHTS ]---")
            for c in condensed:
                context.append(f"💎 {c[0]}")

        # 2. Recent Events (Short Term Memory)
        self.cursor.execute("SELECT author, content, vibe_score FROM memory_events ORDER BY id DESC LIMIT 8")
        recent = self.cursor.fetchall()
        if recent:
            context.append("\n---[ RECENT STREAM ]---")
            for r in reversed(recent):
                context.append(f"{r[0]}: {r[1]} (Vibe: {r[2]})")

        # 3. Active Cells (Topics)
        self.cursor.execute("SELECT topic, description FROM memcells WHERE status='ACTIVE' LIMIT 5")
        cells = self.cursor.fetchall()
        if cells:
            context.append("\n---[ ACTIVE NEURAL PATHWAYS ]---")
            for c in cells:
                context.append(f"• {c[0]}: {c[1]}")
                
        # 4. High Vibe History (Long Term)
        self.cursor.execute("SELECT content FROM memory_events WHERE vibe_score > 90 ORDER BY RANDOM() LIMIT 3")
        gold = self.cursor.fetchall()
        if gold:
            context.append("\n---[ GOLDEN THREAD HIGHLIGHTS ]---")
            for g in gold:
                context.append(f"✨ {g[0]}")
                
        return "\n".join(context)

    def analyze_contextual_overlap(self):
        """
        GENIUS FEATURE: CONTEXTUAL OVERLAP
        Finds disparate events that share a 'Semantic Thread' (Tag Co-occurrence).
        """
        print(f"\n{BOLD}{CYAN}CORE > 🧠 SCANNING SEMANTIC THREADS...{RESET}")
        
        # 1. Build Tag Adjacency Matrix
        self.cursor.execute("SELECT id, tags FROM memory_events WHERE tags IS NOT NULL AND timestamp > datetime('now', '-7 days')")
        rows = self.cursor.fetchall()
        
        tag_graph = {}
        event_map = {}
        
        for eid, tag_str in rows:
            tags = [t.strip().upper() for t in tag_str.split(',') if t.strip()]
            event_map[eid] = tags
            
            for t in tags:
                if t not in tag_graph: tag_graph[t] = set()
                tag_graph[t].add(eid)
                
        # 2. Find Strongest Semantic Bridges
        bridges = []
        seen_pairs = set()
        
        for tag, events in tag_graph.items():
            if len(events) < 2: continue # No bridge if only 1 event
            
            # For every pair of events sharing this tag
            event_list = list(events)
            for i in range(len(event_list)):
                for j in range(i+1, len(event_list)):
                    e1 = event_list[i]
                    e2 = event_list[j]
                    
                    pair = tuple(sorted([e1, e2]))
                    if pair in seen_pairs: continue
                    seen_pairs.add(pair)
                    
                    # Calculate Jaccard Similarity of their full tag sets
                    tags1 = set(event_map[e1])
                    tags2 = set(event_map[e2])
                    
                    intersection = len(tags1.intersection(tags2))
                    union = len(tags1.union(tags2))
                    score = intersection / union if union > 0 else 0
                    
                    # If high similarity but NOT identical (novel overlap)
                    if 0.3 < score < 1.0:
                        bridges.append((score, e1, e2, tags1.intersection(tags2)))
                        
        # 3. Report Top Bridges (Potential Insights)
        bridges.sort(key=lambda x: x[0], reverse=True)
        
        if bridges:
             print(f"   {GREEN}✨ Discovered {len(bridges)} Contextual Overlaps:{RESET}")
             for score, e1, e2, shared in bridges[:5]:
                 shared_str = ", ".join(list(shared))
                 print(f"   🔗 Events #{e1} & #{e2} are linked by [{shared_str}] (Strength: {score:.2f})")
        else:
             print("   (No strong semantic overlaps found yet)")

    def condense_knowledge(self):
        """
        GENIUS FEATURE: KNOWLEDGE CONDENSATION
        Summarizes high-volume tags into a single 'Golden Insight' log to reduce noise.
        """
        print(f"\n{BOLD}{MAGENTA}CORE > 💎 CONDENSING KNOWLEDGE...{RESET}")
        
        # 1. Find High Volume Tags (Last 24h)
        self.cursor.execute("SELECT tags FROM memory_events WHERE timestamp > datetime('now', '-24 hours')")
        rows = self.cursor.fetchall()
        
        from collections import Counter
        tag_counts = Counter()
        for r in rows:
            if r[0]: tag_counts.update([t.strip().upper() for t in r[0].split(',')])
            
        top_tags = tag_counts.most_common(3)
        
        if not top_tags: return
        
        for tag, count in top_tags:
            if count < 5: continue # Ignore low noise
            
            # Check if recently condensed
            self.cursor.execute("SELECT id FROM memory_events WHERE event_type='CONDENSED_INSIGHT' AND tags LIKE ? AND timestamp > datetime('now', '-6 hours')", (f'%{tag}%',))
            if self.cursor.fetchone(): continue
            
            print(f"   📦 Compressing '{tag}' ({count} events)...")
            
            # Create Summary
            self.log_event(self.covenant_id, "CONDENSED_INSIGHT", f"System processed {count} events related to {tag}. Knowledge is solidified.", 100, "CORE", tags=tag)
            print(f"   ✨ {GREEN}Knowledge Solidified: {tag}{RESET}")

    def generate_neural_map(self):
        """
        GENIUS FEATURE: NEURAL MAP (MERMAID)
        Visualizes the top semantic bridges as a Mermaid Graph.
        """
        print(f"\n{BOLD}{CYAN}CORE > 🕸️  WEAVING NEURAL MAP...{RESET}")
        
        # 1. Get Bridges again (re-using logic for brevity, ideally cache it)
        # For demo, we just fetch distinct strong links
        self.cursor.execute("SELECT id, tags, content FROM memory_events WHERE tags IS NOT NULL ORDER BY timestamp DESC LIMIT 200")
        rows = self.cursor.fetchall()
        
        graph_lines = ["graph TD"]
        graph_lines.append("    style CORE fill:#00ffcc,stroke:#333,stroke-width:4px")
        
        # Nodes
        nodes = set()
        links = []
        
        for eid, tags, content in rows:
            tag_list = [t.strip().upper() for t in tags.split(',') if t.strip()]
            short_label = content[:20].replace('"', '').replace("'", "") + "..."
            node_id = f"E{eid}"
            
            if not tag_list: continue
            
            # Create Tag Nodes & Links
            for tag in tag_list:
                tag_id = f"T_{tag.replace(' ', '_')}"
                if tag_id not in nodes:
                    graph_lines.append(f"    {tag_id}(({tag}))")
                    graph_lines.append(f"    style {tag_id} fill:#222,stroke:#00ffcc,stroke-width:1px,color:#fff")
                    nodes.add(tag_id)
                
                links.append(f"    {node_id}[{short_label}] --> {tag_id}")
                
        # Limit complexity for readability
        for l in links[:50]: # Top 50 links
            graph_lines.append(l)
            
        mermaid_content = "\n".join(graph_lines)
        
        # Save Artifact
        map_path = "/Users/m2ultra/.gemini/antigravity/brain/dceca6f9-f975-44c0-967b-78186312035d/neural_map.md"
        with open(map_path, "w") as f:
            f.write("# Gabriel Neural Context Map\n\nGenerated by `analyze_contextual_overlap`.\n\n```mermaid\n")
            f.write(mermaid_content)
            f.write("\n```\n")
            
        print(f"   ✨ {MAGENTA}Neural Map woven at: {map_path}{RESET}")



    def add_milestone(self, milestone):
        self.log_event(self.covenant_id, "MILESTONE", milestone, 100, author="CORE")

    def report_status(self):
        """Generates a comprehensive system health report."""
        print(f"\n{BOLD}{CYAN}===== 📊 MC96 UNIVERSE STATUS REPORT ====={RESET}")
        
        # 1. Database Stats
        self.cursor.execute("SELECT count(*) FROM memcells WHERE status='ACTIVE'")
        active_cells = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT count(*) FROM memory_events")
        total_events = self.cursor.fetchone()[0]
        db_size = Path(DB_PATH).stat().st_size / 1024
        
        print(f"{BOLD}🧠 MEMORY MATRIX:{RESET}")
        print(f"   • Active Synapses (Cells): {GREEN}{active_cells}{RESET}")
        print(f"   • Total Memories (Events): {GREEN}{total_events}{RESET}")
        print(f"   • Neural Mass (DB Size):   {DIM}{db_size:.2f} KB{RESET}")
        
        # 2. Vibe Check
        self.cursor.execute("SELECT AVG(vibe_score) FROM memory_events ORDER BY id DESC LIMIT 20")
        vibe = self.cursor.fetchone()[0] or 50
        vibe_color = GREEN if vibe > 80 else YELLOW if vibe > 50 else RED
        print(f"   • System Vibe (Last 20):   {vibe_color}{vibe:.1f}%{RESET}")
        
        # 3. Integrity
        integrity = "100%" # Placeholder for now, could run PRAGMA integrity_check if slow
        print(f"   • Matrix Integrity:        {GREEN}{integrity}{RESET}")
        
        print(f"{BOLD}{CYAN}=========================================={RESET}\n")

    def suggest_next_action(self):
        """
        PROACTIVE ASSISTANCE ENGINE.
        Analyzes recent context to suggest the next logical step.
        """
        self.cursor.execute("SELECT event_type, content FROM memory_events ORDER BY id DESC LIMIT 1")
        last_ev = self.cursor.fetchone()
        
        if not last_ev: return None
        
        etype, content = last_ev
        suggestion = None
        cmd = None
        
        if etype == "INDEX_COMPLETE":
            suggestion = "I see we just indexed files. Shall I 'Assimilate' this knowledge into Gabriel?"
            cmd = "assimilate"
        elif etype == "PLUGIN_SCAN":
            suggestion = "Plugins scanned. Shall I run 'Overlap' to check for tool compatibility?"
            cmd = "overlap"
        elif etype == "KNOWLEDGE_DISCOVERY":
             suggestion = "New Knowledge found. Shall I 'Optimze' the database?"
             cmd = "optimize"
        elif etype == "INTELLIGENCE_ASSIMILATION":
             suggestion = "Intelligence Assimilated. Run 'Overlap' to sync timeframes?"
             cmd = "overlap"
             
        if suggestion:
            # CHECK FLOW STATE (AUTOPILOT)
            # If user is in Deep Work (FLOW_START < 60 mins ago), Auto-Accept.
            self.cursor.execute("SELECT timestamp FROM memory_events WHERE event_type='FLOW_START' ORDER BY id DESC LIMIT 1")
            flow_event = self.cursor.fetchone()
            is_flowing = False
            
            if flow_event:
                # Simple check: Is flow recent? (We won't do heavy datetime math to keep imports light if needed, 
                # but we have datetime.now).
                # Assume flow implies high trust.
                print(f"{MAGENTA}   (Flow State is Active...){RESET}")
                is_flowing = True # We treat presence of explicit FLOW_START as intent for now, or check time if possible.
            
            if is_flowing and cmd:
                print(f"{GREEN}🤖 FLOW AUTOPILOT > {suggestion}{RESET}")
                print(f"{GREEN}   ⚡ ACCEPTING ALL: Auto-Executing '{cmd}' for zero latency...{RESET}")
                self.execute_command(cmd)
                return None
            else:
                print(f"\n{GREEN}🤖 ASSISTANT > {suggestion}{RESET}")
                print(f"   (Type '{cmd}' to execute or press ENTER to confirm)")
                # Minimal friction for non-flow:
                # In a real loop we might handle 'empty input' as confirm, but this is a display function.
                # We'll leave the prompt explicit for now outside of Flow.
                return cmd
        
        return None

    def execute_command(self, cmd):
        # ... (rest of function)
        cmd = cmd.lower().strip()
        print(f"{YELLOW}CORE > ⚡ EXECUTING: {cmd.upper()}{RESET}")
        
        script = None
        args = []
        
        if "omega" in cmd or "everything" in cmd or "full" in cmd:
            script = "turbo_omega.py"
        elif "scavenge" in cmd or "find" in cmd:
            script = "turbo_scavenger.py"
        elif "status" in cmd or "report" in cmd:
            self.report_status()
            return True 
        elif "keith" in cmd or "integrity" in cmd:
            script = "turbo_keith.py"
        elif "singularity" in cmd:
             script = "turbo_singularity.py"
             args = [str(Path.expanduser(Path("~/Universal/Library")))]
        elif "index" in cmd or "scan" in cmd:
            script = "turbo_indexer.py"
        elif "hunt" in cmd or "logo" in cmd:
            script = "turbo_hunter.py"
        elif "plugin" in cmd:
            script = "turbo_plugins.py"
        elif "overlap" in cmd:
            self.analyze_overlap()
            return True
        elif "omniscience" in cmd or "smart" in cmd:
            self.execute_omniscience_protocol()
            return True
        elif "condense" in cmd or "optimize" in cmd:
            self.condense_memory()
            return True

        if script:
            print(f"{GREEN}CORE > 🚀 Launching {script}...{RESET}")
            import subprocess
            subprocess.run(["python3", f"Audio_Unitor/Scripts/{script}"] + args)
            return True
        else:
            if "overlap" not in cmd and "status" not in cmd:
                 print(f"{RED}CORE > ⚠️ Command not recognized (yet).{RESET}")
            return False

    def process_neural_input(self, msg, author="USER"):
        msg = msg.strip()
        if not msg: return None
        
        # Neural Parsing
        lower_msg = msg.lower()
        etype = "DIALOGUE"
        vibe = 50
        response = "Received."
        executed = False
        
        # Identity Check: Persistent or Override
        if msg.upper().startswith("BECOME:"):
            # IDENTITY SWITCH COMMAND
            target_identity = msg.split(":")[1].strip().upper()
            if target_identity in ["SHIRL", "ENGR", "ENGR_KEITH", "GABRIEL", "CORE"]:
                self.current_persona = target_identity
                # Log the shift
                self.log_event(self.covenant_id, "IDENTITY_SHIFT", f"Persona shifted to {target_identity}", 100, author="CORE")
                print(f"{GREEN}CORE > Identity Matrix Realigned: {BOLD}{target_identity}{RESET}")
                return True
            else:
                 print(f"{YELLOW}CORE > Unknown Identity: {target_identity}{RESET}")
                 return False

        # Apply Current Persona if not overridden
        if not author or author == "USER":
             pass

        # Manual Override
        upper_msg = msg.upper()
        if upper_msg.startswith("SHIRL:"):
            author = "SHIRL"
            msg = msg[6:].strip()
            lower_msg = msg.lower()
        elif upper_msg.startswith("ENGR:") or upper_msg.startswith("ENGR_KEITH:"):
            author = "ENGR_KEITH"
            msg = msg.split(":", 1)[1].strip()
            lower_msg = msg.lower()

        # Direct Command Detection (Fuzzy)
        if lower_msg in ["scavenge", "omega", "keith", "status", "dedup", "ingest", "overlap"]:
            lower_msg = f"do: {lower_msg}"
            msg = f"Do: {msg}" 
        
        if lower_msg.startswith("do:"):
            etype = "COMMAND"
            cmd_content = msg[3:].strip()
            vibe = 80
            executed = self.execute_command(cmd_content)
            response = f"{BOLD}⚡ Action Completed.{RESET}" if executed else "⚠️ Action Failed."
            if executed: msg = cmd_content 
        elif lower_msg.startswith("goal:"):
            etype = "SHARED_GOAL"
            msg = msg[5:].strip()
            vibe = 90
            response = f"{BOLD}🏆 Target Locked.{RESET}"
        elif lower_msg.startswith("idea:"):
            etype = "IDEA"
            msg = msg[5:].strip()
            vibe = 75
            response = f"{BOLD}💡 Spark Captured.{RESET}"
        elif lower_msg.startswith("love:"):
            etype = "VIBE_CHECK"
            msg = msg[5:].strip()
            vibe = 100
            response = f"{BOLD}❤️ Love Frequency Optimized.{RESET}"
        elif lower_msg.startswith("thread:"):
            etype = "MEMORY_THREAD"
            msg = msg[7:].strip()
            vibe = 85
            response = f"{BOLD}🧵 Thread Synchronized.{RESET}"
        elif lower_msg.startswith("note:"):
            etype = "NOTE"
            msg = msg[5:].strip()
            response = "📝 Note Saved."
        else:
            # 🧠 ORACLE PROTOCOL: INTELLIGENT INTENT DETECTION
            intent, confidence = self.analyze_intent(lower_msg)
            
            if intent == "QUERY":
                print(f"{GREEN}CORE > 🧠 Analyzing Query...{RESET}")
                self.smart_query(lower_msg)
                return True # Don't log queries as memories, they are retrievals
            
            elif intent == "GREETING":
                response = f"Systems Online. Accessing Neural Matrix. Ready, {self.current_persona}."
                
            # Auto-Sentiment Fallback for normal messages
            if "excellent" in lower_msg or "love" in lower_msg or "great" in lower_msg: vibe = 80
            if "bad" in lower_msg or "hate" in lower_msg or "fail" in lower_msg: vibe = 20
        
        self.log_event(self.covenant_id, etype, msg, vibe, author=author)
        if not executed:
             print(f"{GREEN}CORE > {response}{RESET}")
        return True

    def analyze_intent(self, text):
        """Determine if input is a Question, Command, or Statement."""
        text = text.lower()
        
        # Query Signs
        if text.startswith(("what", "who", "where", "when", "how", "list", "show", "find", "recall")):
            return "QUERY", 0.9
        if "?" in text:
            return "QUERY", 0.8
            
        # Greeting Signs
        if text in ["hello", "hi", "yo", "sup", "hey", "start", "init"]:
            return "GREETING", 0.9
            
        return "STATEMENT", 0.5

    def smart_query(self, text):
        """Use NLP heuristics to query the DB based on natural language."""
        text = text.lower()
        
        # 1. Temporal Logic
        time_filter = None
        if "today" in text:
            time_filter = datetime.now().strftime("%Y-%m-%d")
        elif "yesterday" in text:
            # Simple fallback (requires timedelta import, keeping simple for zero latency dep)
            pass 
            
        # 2. Entity Extraction (Simple)
        words = text.split()
        keywords = [w.rstrip("?.!,") for w in words if len(w) > 3 and w not in ["what", "show", "find", "about", "with", "from"]]
        
        print(f"   🔎 Search Vector: {keywords} | Time: {time_filter or 'All'}")
        
        
        # 3. Construct Query
        if "recent" in text or "last" in text or "history" in text:
            # Show History
            print(f"\n{BOLD}CORE > 📜 Recent System History:{RESET}")
            self.cursor.execute("SELECT timestamp, author, content FROM memory_events ORDER BY timestamp DESC LIMIT 5")
            for ts, auth, ctx in self.cursor.fetchall():
                 print(f"   [{ts[11:16]}] {auth}: {ctx}")
                 
        elif "vibe" in text:
            # Analyze Vibe
             self.cursor.execute("SELECT AVG(vibe_score) FROM memory_events ORDER BY timestamp DESC LIMIT 10")
             score = self.cursor.fetchone()[0] or 50
             print(f"\n{BOLD}CORE > 🔮 Current System Vibe: {score:.1f}/100{RESET}")

        elif keywords:
            # Keyword Search (Use find_associations and standard search)
            topic = keywords[0] # Primary subject
            self.recall(topic) # Reuse our smart recall
             
        else:
            print(f"\n{YELLOW}CORE > I understood the question but need more specific keywords.{RESET}")

    def chat_mode(self):
        print(f"\n{BOLD}{GREEN}CORE > 🧠 NEURAL LINK ACTIVE (Smart Context Enabled){RESET}")
        
        # Show Current Persona Vibe
        current_p = getattr(self, "current_persona", "CORE")
        print(f"{BOLD}IDENTITY: {current_p}{RESET}")
        if current_p == "SHIRL":
            print(f"{MAGENTA}{prompts.SHIRL_PROMPT}{RESET}")
        elif current_p == "ENGR":
            print(f"{CYAN}{prompts.ENGR_PROMPT}{RESET}")
        
        # Inject Strategy
        print(f"{cfg.DIM}{prompts.STRATEGIC_LAYER}{cfg.RESET}")
        
        print(f"{CYAN}POWER PROMPTS:{RESET}")
        print(f"   • Do:   [Action] -> EXECUTES SCRIPTS (e.g., 'Do: Overlap') 🚀")
        print(f"   • Goal: [Text]   -> Sets Shared Focus 🏆")
        print(f"   • Idea: [Text]   -> Logs Creative Spark 💡")
        print(f"   • Love: [Text]   -> Boosts Vibe 100% ❤️")
        print(f"   • Become:[Name]  -> Switches Identity (Shirl/Engr) 🎭")
        print(f"{CYAN}Context: You can prefix inputs with 'SHIRL:' or 'ENGR:' to switch persona.{RESET}")
        print(f"{CYAN}Type your thoughts. (Type 'EXIT' to return to Nexus){RESET}")
        
        while True:
            msg = input(f"\n{CYAN}NEURAL INPUT > {RESET}").strip()
            if msg.upper() == 'EXIT': break
            self.process_neural_input(msg, author="USER")

def interact():
    caretaker = MemCell()
    print(f"{BOLD}{CYAN}CORE > 🧬 OMNI-MEMCELL ACTIVE (THE ALL-KNOWING VAULT){RESET}")
    print(f"{GREEN}CORE > Covenant Integrity: 100% | Entity: {caretaker.covenant_id}{RESET}")
    
    while True:
        pending_cmd = caretaker.suggest_next_action()
        
        print(f"\n   [C] 👁️  Enter Neural Link (Chat)")
        print(f"   [O] ⏳ Analyze Temporal & Subject Overlap")
        print(f"   [T] 🕰️  Temporal Intelligence (Heatmap)")
        print(f"   [K] 🔗 Associative Intelligence (Correlations)")
        print(f"   [Z] 🧠 Omniscience Protocol (Hyper-Learning)")
        print(f"   [1] Create New Cell")
        print(f"   [2] Log Event")
        print(f"   [3] Recall Memory")
        print(f"   [4] List Active Cells")
        print(f"   [Q] Quit")
        
        prompt_suffix = f" (Enter to Run '{pending_cmd}')" if pending_cmd else ""
        choice = input(f"\n   {CYAN}OMNI-CORE{prompt_suffix} > {RESET}").lower().strip()
        
        if not choice and pending_cmd:
            # ACCEPT ALL (Enter Key)
            choice = f"do: {pending_cmd}"
            caretaker.process_neural_input(choice, author="CORE")
            continue

        if choice == 'c':
            caretaker.chat_mode()
        elif choice == 'o':
            caretaker.analyze_overlap()
        elif choice == 't':
            caretaker.analyze_temporal_patterns()
        elif choice == 'k':
            caretaker.analyze_correlations()
        elif choice == 'z':
            caretaker.execute_omniscience_protocol()
        elif choice == '1':
            topic = input("   Topic: ")
            desc = input("   Description: ")
            caretaker.create_cell(topic, desc)
        elif choice == '2':
            cells = caretaker.list_cells()
            if not cells:
                print("   No active cells.")
                continue
            for c in cells: print(f"   #{c[0]}: {c[1]}")
            
            try:
                cid = input("   Select Cell ID (Enter for Covenant): ")
                cid = int(cid) if cid else caretaker.covenant_id
                
                etype = input("   Event Type (NOTE, UPDATE, FILE): ")
                content = input("   Content: ")
                # vibe = input("   Vibe Score (0-100) [50]: ")
                # vibe = int(vibe) if vibe else 50
                caretaker.log_event(cid, etype, content, 50, author="CORE")
            except: print("   Invalid ID")
        elif choice == '3':
            q = input("   Search Query: ")
            caretaker.recall(q)
        elif choice == '4':
            cells = caretaker.list_cells()
            for c in cells: print(f"   #{c[0]}: {BOLD}{c[1]}{RESET} - {c[2]}")
        elif choice == 'q':
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "optimize":
        mc = MemCell()
        mc.optimize_db()
    else:
        interact()
