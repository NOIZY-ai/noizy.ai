import sqlite3
import json
import time
from pathlib import Path
from datetime import datetime

# Identity
NAME = "THE CARETAKER (MEMCELL)"
VERSION = "40.0"

# Configuration
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

class MemCell:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self.init_db()
        self.init_covenant()

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
        
        # Schema Migration: Add tags and author if missing
        try:
            self.cursor.execute("SELECT tags FROM memory_events LIMIT 1")
        except:
            try:
                self.cursor.execute("ALTER TABLE memory_events ADD COLUMN tags TEXT")
                print(f"{GREEN}CORE > Schema Upgraded: Added 'tags' column.{RESET}")
            except: pass
            
        try:
            self.cursor.execute("SELECT author FROM memory_events LIMIT 1")
        except:
            try:
                self.cursor.execute("ALTER TABLE memory_events ADD COLUMN author TEXT DEFAULT 'CORE'")
                print(f"{GREEN}CORE > Schema Upgraded: Added 'author' column.{RESET}")
            except: pass
            
        self.conn.commit()

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
        # Enhanced Subject Matter Extractor (Chronos Upgrade)
        stop_words = {
            "the", "and", "is", "at", "which", "on", "for", "to", "a", "an", "in", "of", "with",
            "from", "by", "that", "this", "it", "as", "are", "was", "were", "be", "has", "have",
            "but", "or", "so", "if", "then", "not", "just", "can", "will", "do", "did"
        }
        
        # 1. Prioritize Capitalized Words (Proper Nouns/Projects) - likely Subject Matter
        words = content.replace(".", "").replace(",", "").replace(":", "").replace("!", "").split()
        capitalized = [w for w in words if w[0].isupper() and w.lower() not in stop_words and len(w) > 2]
        
        # 2. General Frequency
        clean_words = [w.lower() for w in words if w.lower() not in stop_words and len(w) > 3]
        
        # Merge lists, prioritizing capitalized
        all_candidates = capitalized + clean_words
        
        # Deduplicate while preserving order
        seen = set()
        final_tags = []
        for tag in all_candidates:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                final_tags.append(tag)
                
        return ", ".join(final_tags[:6]) # Top 6 unique tags

    def log_event(self, cell_id, event_type, content, vibe=50, author="CORE"):
        ts = datetime.now().isoformat()
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
        
        if not cells:
            print(f"{YELLOW}CORE > No Cells found matching '{query}'.{RESET}")
            # Fallback: Search individual events directly?
            # self.cursor.execute("SELECT * FROM memory_events WHERE content LIKE ?", (wild,))
            return

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

    def analyze_overlap(self):
        print(f"\n{BOLD}{CYAN}CORE > ⏳ CHRONOS ENGINE: CALCULATING TEMPORAL & SUBJECT OVERLAP...{RESET}")
        
        # 1. Temporal Heatmap (Activity by Hour)
        print(f"\n{BOLD}CORE > 🕰️  Temporal Heatmap (Peak Activity):{RESET}")
        # Extract hour from ISO timestamps: T14:20:00 -> 14
        self.cursor.execute("SELECT substr(timestamp, 12, 2) as hour, COUNT(*) FROM memory_events GROUP BY hour ORDER BY hour")
        hours = self.cursor.fetchall()
        
        # Visualize 24h clock
        if not hours:
            print("   (No temporal data yet)")
        else:
            max_hits = max(h[1] for h in hours) if hours else 1
            for h, count in hours:
                bar = "█" * int((count / max_hits) * 20)
                print(f"   [{h}:00] {bar} {count}")

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

    def list_cells(self):
        self.cursor.execute("SELECT id, topic, description, status FROM memcells WHERE status='ACTIVE'")
        return self.cursor.fetchall()
        
    # Relationship Specifics
    def log_vibe(self, score, note):
        self.log_event(self.covenant_id, "VIBE_CHECK", note, score, author="CORE")
        
    def add_goal(self, goal):
        self.log_event(self.covenant_id, "SHARED_GOAL", goal, 90, author="CORE")
        
    def add_milestone(self, milestone):
        self.log_event(self.covenant_id, "MILESTONE", milestone, 100, author="CORE")

    def execute_command(self, cmd):
        cmd = cmd.lower().strip()
        print(f"{YELLOW}CORE > ⚡ EXECUTING: {cmd.upper()}{RESET}")
        
        script = None
        args = []
        
        if "omega" in cmd or "everything" in cmd or "full" in cmd:
            script = "turbo_omega.py"
        elif "scavenge" in cmd or "find" in cmd:
            script = "turbo_scavenger.py"
        elif "status" in cmd or "report" in cmd:
            script = None # TODO: Add status reporter
            print(f"CORE > System appears functional.")
            pass 
        elif "keith" in cmd or "integrity" in cmd:
            script = "turbo_keith.py"
        elif "singularity" in cmd:
             script = "turbo_singularity.py"
             args = [str(Path.expanduser(Path("~/Universal/Library")))]
        elif "overlap" in cmd:
            self.analyze_overlap()
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
        
        # Identity Check: Did user explicitly type "SHIRL:" or "ENGR:"?
        if msg.upper().startswith("SHIRL:"):
            author = "SHIRL"
            msg = msg[6:].strip()
            lower_msg = msg.lower()
        elif msg.upper().startswith("ENGR:"):
            author = "ENGR"
            msg = msg[5:].strip()
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
        elif lower_msg.startswith("note:"):
            etype = "NOTE"
            msg = msg[5:].strip()
            response = "📝 Note Saved."
        else:
            # Auto-Sentiment Fallback
            if "excellent" in lower_msg or "love" in lower_msg or "great" in lower_msg: vibe = 80
            if "bad" in lower_msg or "hate" in lower_msg or "fail" in lower_msg: vibe = 20
        
        self.log_event(self.covenant_id, etype, msg, vibe, author=author)
        if not executed:
             print(f"{GREEN}CORE > {response}{RESET}")
        return True

    def chat_mode(self):
        print(f"\n{BOLD}{GREEN}CORE > 🧠 NEURAL LINK ACTIVE (Smart Context Enabled){RESET}")
        print(f"{CYAN}POWER PROMPTS:{RESET}")
        print(f"   • Do:   [Action] -> EXECUTES SCRIPTS (e.g., 'Do: Overlap') 🚀")
        print(f"   • Goal: [Text]   -> Sets Shared Focus 🏆")
        print(f"   • Idea: [Text]   -> Logs Creative Spark 💡")
        print(f"   • Love: [Text]   -> Boosts Vibe 100% ❤️")
        print(f"{CYAN}Context: You can prefix inputs with 'SHIRL:' or 'ENGR:' to switch persona.{RESET}")
        print(f"{CYAN}Type your thoughts. (Type 'EXIT' to return to Nexus){RESET}")
        
        while True:
            msg = input(f"\n{CYAN}NEURAL INPUT > {RESET}").strip()
            if msg.upper() == 'EXIT': break
            self.process_neural_input(msg, author="USER")

def interact():
    caretaker = MemCell()
    print(f"{BOLD}{CYAN}CORE > 🧬 MEMCELL INTERFACE (THE MUTUAL VAULT){RESET}")
    print(f"{GREEN}CORE > Covenant Active: {caretaker.covenant_id}{RESET}")
    
    while True:
        print(f"\n   [C] 💬 Enter Chat Mode (Neural Link)")
        print(f"   [O] ⏳ Analyze Overlap (Subject & Time)")
        print(f"   [1] Create New Cell (Project)")
        print(f"   [2] Log Event to Cell")
        print(f"   [3] Recall Memory")
        print(f"   [4] List Active Cells")
        print(f"   [Q] Quit")
        
        choice = input(f"\n   {CYAN}CORE > {RESET}").lower().strip()
        
        if choice == 'c':
            caretaker.chat_mode()
        elif choice == 'o':
            caretaker.analyze_overlap()
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
    interact()
