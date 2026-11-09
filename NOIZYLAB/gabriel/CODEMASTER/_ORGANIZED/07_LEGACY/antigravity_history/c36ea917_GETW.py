import os
import re
import sqlite3
import datetime
from pathlib import Path

import sys

# CONFIG
sys.path.append(str(Path(__file__).parent)) # Scripts dir
try:
    import turbo_config as cfg
    DB_PATH = Path(cfg.UNIVERSE_DB_PATH)
except ImportError:
    # Fallback if config fails
    DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe_db.sqlite")

print(f"DEBUG: Ghost connecting to {DB_PATH}")

class GhostWriter:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH)) # Ensure string for sqlite3
        self.cursor = self.conn.cursor()
        self.patterns = [
            r"#\s*TODO:?(.*)",
            r"#\s*FIXME:?(.*)",
            r"#\s*OPTIMIZE:?(.*)",
            r"#\s*NOTE:?(.*)"
        ]

    def scan(self):
        print("👻 GHOST WRITER: Awakening...")
        tasks = []
        
        for root, dirs, files in os.walk(ROOT_DIR):
            for file in files:
                if file.endswith(".py"):
                    path = Path(root) / file
                    tasks.extend(self.scan_file(path))
                    
        print(f"👻 GHOST WRITER: Found {len(tasks)} Spectral Echoes (Tasks).")
        self.ingest(tasks)

    def scan_file(self, filepath):
        results = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                for pattern in self.patterns:
                    match = re.search(pattern, line)
                    if match:
                        content = match.group(1).strip()
                        tag = "TODO" if "TODO" in pattern else "FIXME" if "FIXME" in pattern else "OPTIMIZE" if "OPTIMIZE" in pattern else "NOTE"
                        if content:
                             results.append({
                                 "file": filepath.name,
                                 "line": i + 1,
                                 "type": tag,
                                 "content": content
                             })
        except Exception as e:
            print(f"⚠️ Error reading {filepath.name}: {e}")
            
        return results

    def ingest(self, tasks):
        new_count = 0
        for task in tasks:
            # Check if exists (Simple dup check based on content string)
            # ideally we'd check file/line but code moves. Content is safer for uniqueness of *idea*.
            task_str = f"{task['type']} [{task['file']}:{task['line']}] {task['content']}"
            
            self.cursor.execute("SELECT id FROM memory_events WHERE content = ? AND event_type='GHOST_TASK'", (task_str,))
            if not self.cursor.fetchone():
                timestamp = datetime.datetime.now().isoformat()
                self.cursor.execute(
                    "INSERT INTO memory_events (timestamp, event_type, content, vibe_score, author, tags) VALUES (?, ?, ?, ?, ?, ?)",
                    (timestamp, "GHOST_TASK", task_str, 50, "GHOST", task['type'])
                )
                new_count += 1
                
        self.conn.commit()
        if new_count > 0:
            print(f"👻 GHOST WRITER: Materialized {new_count} new tasks into MemCell.")
        else:
            print("👻 GHOST WRITER: No new spectral echoes detected.")

if __name__ == "__main__":
    ghost = GhostWriter()
    ghost.scan()
