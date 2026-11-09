# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

#!/usr/bin/env python3
import sqlite3
import argparse
import os
import sys
from pathlib import Path

try:
    import turbo_config as cfg
    import turbo_gabriel
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel

DB_PATH = cfg.UNIVERSE_DB_PATH

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def run_dedup_report(nuke=False):
    cfg.ensure_dirs([DB_PATH.parent])
    if not DB_PATH.exists():
        cfg.system_log("Universe Database not found.", "ERROR")
        return

    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    cfg.print_header("🧬 TURBO DEDUP", "ZERO REDUNDANCY PROTOCOL")
    
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
        cfg.system_log("No duplicates found! The Universe is unique.", "SUCCESS")
        return
        
    cfg.system_log("Found massive duplication!", "WARN")
    
    wasted_total = 0
    
    for row in results:
        file_hash, count, total_vol, single_size = row
        wasted_bytes = total_vol - single_size # Keep one copy
        wasted_total += wasted_bytes
        
        # Get one filename for context
        c.execute("SELECT filename, path FROM files WHERE hash=? LIMIT 1", (file_hash,))
        sample = c.fetchone()
        name = sample[0]
        
        print(f"   {cfg.BOLD}{name}{cfg.RESET}")
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
        
    print(f"{cfg.BOLD}CORE > 📊 DUPLICATION SUMMARY:{cfg.RESET}")
    print(f"CORE > Files Scanned: {total_files}")
    print(f"CORE > Top 50 Dupes Wasted Space: {cfg.RED}{format_size(wasted_total)}{cfg.RESET}")
    
    # Calculate Total Wasted in DB
    c.execute("""
        SELECT sum(size * (count - 1)) 
        FROM (SELECT size, count(*) as count FROM files GROUP BY hash HAVING count > 1)
    """)
    grand_total_wasted = c.fetchone()[0] or 0
    print(f"CORE > TOTAL UNIVERSE WASTE: {cfg.RED}{format_size(grand_total_wasted)}{cfg.RESET}")

    # Generate Cleanup Script
    print(f"\n{cfg.BOLD}CORE > 🧹 GENERATING CLEANUP SCRIPT...{cfg.RESET}")
    script_path = "clean_duplicates.sh"
    
    # Get ALL duplicates
    c.execute("""
        SELECT hash, count(*) as count 
        FROM files 
        GROUP BY hash 
        HAVING count > 1
    """)
    all_dupes = c.fetchall()
    
    nuke_commands = []

    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n# AUTO GENERATED CLEANUP SCRIPT\n")
        f.write("# REVIEW BEFORE RUNNING!\n\n")
        
        for row in all_dupes:
            file_hash = row[0]
            # Get all paths for this hash
            c.execute("SELECT path FROM files WHERE hash=?", (file_hash,))
            paths = [r[0] for r in c.fetchall()]
            
            # Smart Keep: Keep the shortest path (likely the "cleanest" location)
            paths.sort(key=len)
            best_copy = paths[0]
            to_delete = paths[1:]

            f.write(f"# Keeping: {best_copy}\n")
            for kill in to_delete:
                safe_path = kill.replace('"', '\\"') # Escape quotes
                cmd = f'rm "{safe_path}"'
                f.write(cmd + "\n")
                nuke_commands.append(kill)
            f.write("\n")
            
    os.chmod(script_path, 0o755)
    print(f"CORE > ✨ Script Generated: {cfg.GREEN}{script_path}{cfg.RESET}")
    
    if nuke:
        print(f"\n{cfg.BOLD}{cfg.RED}CORE > ☢️  AUTO-NUKE INITIATED ☢️{cfg.RESET}")
        print(f"CORE > Deleting {len(nuke_commands)} redundant files...")
        deleted_count = 0
        for fpath in nuke_commands:
            try:
                os.remove(fpath)
                deleted_count += 1
            except Exception as e:
                print(f"CORE > Failed to delete {fpath}: {e}")
        print(f"CORE > {cfg.GREEN}✅ NUKE COMPLETE. Deleted {deleted_count} files.{cfg.RESET}")
    else:
        print(f"CORE > 👉 Review it, then run: {cfg.CYAN}./{script_path}{cfg.RESET}")
        print(f"CORE > (Or run with --nuke to auto-delete)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turbo Dedup: Find and Destroy Duplicates")
    parser.add_argument("--nuke", action="store_true", help="Automatically delete duplicates (Dangerous!)")
    args = parser.parse_args()
    
    run_dedup_report(args.nuke)
