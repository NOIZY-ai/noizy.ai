import sqlite3
import argparse
from pathlib import Path

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def search_db(query, limit=50):
    if not DB_PATH.exists():
        print(f"{YELLOW}❌ Universe Database not found. Run Turbo Indexer first.{RESET}")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    print(f"{BOLD}🔎 Searching Universe DB for: {CYAN}{query}{RESET}")
    
    # Try Hash Search first (Exact Dedup)
    if len(query) == 64: # SHA256 length
        print(f"   Detected Hash Query...")
        c.execute("SELECT path, filename, volume, size FROM files WHERE hash=?", (query,))
    else:
        # Wildcard Name Search
        search_term = f"%{query}%"
        c.execute("SELECT path, filename, volume, size FROM files WHERE filename LIKE ? LIMIT ?", (search_term, limit))
        
    results = c.fetchall()
    
    if not results:
        print(f"   ⚪ No matches found.")
        return

    print(f"   ✅ Found {len(results)} matches:\n")
    
    for row in results:
        path, name, vol, size = row
        size_mb = size / (1024*1024)
        print(f"   📂 {GREEN}{vol}{RESET} | {name} ({size_mb:.2f} MB)")
        print(f"      ↳ {path}")
        
    if len(results) == limit:
        print(f"\n   ... (Showing first {limit} results)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_search.py <query>")
    else:
        search_db(sys.argv[1])
