import sqlite3
import argparse
from pathlib import Path

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def run_dedup_report():
    if not DB_PATH.exists():
        print(f"{RED}❌ Universe Database not found.{RESET}")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    print(f"{BOLD}🧬 SCANNING FOR EXACT DUPLICATES (Turbo Engine)...{RESET}")
    
    # Check total files first
    c.execute("SELECT count(*) FROM files")
    total_files = c.fetchone()[0]
    
    # Find hashes that appear more than once
    query = """
        SELECT hash, count(*) as count, sum(size) as total_size, size 
        FROM files 
        GROUP BY hash 
        HAVING count > 1
        ORDER BY total_size DESC
        LIMIT 50
    """
    
    c.execute(query)
    results = c.fetchall()
    
    if not results:
        print(f"   {GREEN}✅ No duplicates found! The Universe is unique.{RESET}")
        return
        
    print(f"   {YELLOW}⚠️  Found massive duplication!{RESET}\n")
    
    wasted_total = 0
    
    for row in results:
        file_hash, count, total_vol, single_size = row
        wasted_bytes = total_vol - single_size # Keep one copy
        wasted_total += wasted_bytes
        
        # Get one filename for context
        c.execute("SELECT filename, path FROM files WHERE hash=? LIMIT 1", (file_hash,))
        sample = c.fetchone()
        name = sample[0]
        
        print(f"   {BOLD}{name}{RESET}")
        print(f"      Hash: {file_hash[:16]}...")
        print(f"      Copies: {count}")
        print(f"      Wasted: {format_size(wasted_bytes)}")
        
        # List paths? Maybe too verbose if 50 copies. Just top 3.
        c.execute("SELECT path, volume FROM files WHERE hash=? LIMIT 3", (file_hash,))
        paths = c.fetchall()
        for p in paths:
             print(f"         - {p[1]}: {p[0]}")
        if count > 3:
            print(f"         ... and {count-3} more locations.")
        print("")
        
    print(f"{BOLD}📊 DUPLICATION SUMMARY:{RESET}")
    print(f"   Files Scanned: {total_files}")
    print(f"   Top 50 Dupes Wasted Space: {RED}{format_size(wasted_total)}{RESET}")
    
    # Calculate Total Wasted in DB
    c.execute("""
        SELECT sum(size * (count - 1)) 
        FROM (SELECT size, count(*) as count FROM files GROUP BY hash HAVING count > 1)
    """)
    grand_total_wasted = c.fetchone()[0] or 0
    print(f"   TOTAL UNIVERSE WASTE: {RED}{format_size(grand_total_wasted)}{RESET}")

if __name__ == "__main__":
    run_dedup_report()
