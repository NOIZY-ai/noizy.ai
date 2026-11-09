"""
SONIC SEARCH ENGINE v1.0
Hyper-fast Code Indexing using SQLite FTS5
"""

import sqlite3
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging

# CONFIG
DB_PATH = Path("NOIZYLAB_DB/gabriel_index.db")
VAULT_PATH = Path("mined_code")
BATCH_SIZE = 1000

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("SONIC")

class SonicIndex:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # FTS5 Virtual Table for blazing fast text search
        c.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS code_index 
            USING fts5(path, filename, content, tokenize='trigram');
        ''')
        # Metadata table to track modification times for incremental updates
        c.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                path TEXT PRIMARY KEY,
                mtime REAL
            );
        ''')
        conn.commit()
        conn.close()

    def index_vault(self, vault_path=VAULT_PATH, rebuild=False):
        """Crawls and indexes the vault."""
        logger.info(f"🚀 STARTING SONIC INDEX: {vault_path}")
        start_time = time.time()
        
        if rebuild and self.db_path.exists():
            os.remove(self.db_path)
            self._init_db()

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 1. SCAN FILES
        files_to_process = []
        for root, _, files in os.walk(vault_path):
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.html', '.css', '.md', '.sh', '.json', '.txt', '.glsl', '.hlsl', '.c', '.cpp', '.h', '.rs', '.go', '.java')):
                     files_to_process.append(Path(root) / file)
        
        logger.info(f"Found {len(files_to_process)} candidates. Checking diffs...")

        # 2. FILTER CHANGED FILES (Incremental)
        updates = []
        for p in files_to_process:
            try:
                mtime = p.stat().st_mtime
                row = c.execute("SELECT mtime FROM metadata WHERE path = ?", (str(p),)).fetchone()
                if not row or row[0] < mtime:
                    updates.append(p)
            except:
                pass
        
        logger.info(f"Indexing {len(updates)} new/modified files...")

        # 3. BATCH PROCESS
        count = 0
        for i in range(0, len(updates), BATCH_SIZE):
            batch = updates[i:i+BATCH_SIZE]
            data_batch = []
            meta_batch = []
            
            for p in batch:
                try:
                    content = p.read_text(errors='ignore')
                    rel_path = str(p.relative_to(vault_path))
                    data_batch.append((str(p), p.name, content))
                    meta_batch.append((str(p), p.stat().st_mtime))
                except:
                    continue
            
            # Atomic Write
            if data_batch:
                c.executemany("INSERT OR REPLACE INTO code_index (path, filename, content) VALUES (?, ?, ?)", data_batch)
                c.executemany("INSERT OR REPLACE INTO metadata (path, mtime) VALUES (?, ?)", meta_batch)
                conn.commit()
                count += len(data_batch)
                print(f"  [+] Indexed {count}/{len(updates)}")

        duration = time.time() - start_time
        logger.info(f"✅ INDEX COMPLETE in {duration:.2f}s. Total Indexed: {count}")
        conn.close()

    def search(self, query: str, limit=20):
        """Full-text search with snippets."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # FTS5 Rank
        try:
            results = c.execute(f'''
                SELECT path, snippet(code_index, 2, '<b>', '</b>', '...', 64) as snip, rank 
                FROM code_index 
                WHERE code_index MATCH ? 
                ORDER BY rank 
                LIMIT ?
            ''', (query, limit)).fetchall()
        except Exception as e:
            return [("Error", str(e), 0)]
            
        conn.close()
        return results

if __name__ == "__main__":
    import sys
    indexer = SonicIndex()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--build":
            indexer.index_vault(rebuild=True)
        else:
            # Search mode
            query = " ".join(sys.argv[1:])
            print(f"🔎 SEARCHING: {query}")
            hits = indexer.search(query)
            for path, snip, rank in hits:
                print(f"\n📄 {path}\n   {snip}")
    else:
        # Default build if no args
        indexer.index_vault()
