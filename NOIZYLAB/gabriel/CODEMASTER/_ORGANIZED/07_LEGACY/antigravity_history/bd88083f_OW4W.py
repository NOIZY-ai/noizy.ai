import os
import sys
import subprocess
import time
import sqlite3
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Scripts")
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
CLEAR = "\033[H\033[J"

def clear_screen():
    print(CLEAR, end="")

def print_banner():
    clear_screen()
    print(f"{BOLD}{CYAN}")
    print("   ╔════════════════════════════════════════════╗")
    print("   ║         THE NEXUS CORE (ENGR v37.0)        ║")
    print("   ║     Universal AI Command Interface (God)   ║")
    print("   ╚════════════════════════════════════════════╝")
    print(f"{RESET}")

def run_script(script_name, args=[]):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"{RED}Script not found: {script_name}{RESET}")
        time.sleep(2)
        return
    
    cmd = ["python3", str(script_path)] + args
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted.{RESET}")
    input(f"\n{CYAN}Press Enter to return to Nexus...{RESET}")

def memory_core_search():
    print(f"\n{BOLD}🧠 MEMORY CORE SEARCH{RESET}")
    query = input("Enter search term (filename, hash, path): ").strip()
    if not query: return
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        sql = f"SELECT timestamp, action, original_path, final_path FROM provenance WHERE original_path LIKE ? OR final_path LIKE ? OR file_hash LIKE ? ORDER BY timestamp DESC LIMIT 20"
        wild_query = f"%{query}%"
        c.execute(sql, (wild_query, wild_query, wild_query))
        results = c.fetchall()
        
        if not results:
            print(f"{YELLOW}No records found.{RESET}")
        else:
            print(f"\nFound {len(results)} records:")
            for row in results:
                ts, act, orig, final = row
                print(f"[{ts}] {BOLD}{act}{RESET}")
                print(f"  From: {orig}")
                print(f"  To:   {final}")
                print("-" * 40)
        conn.close()
    except Exception as e:
        print(f"{RED}Database Error: {e}{RESET}")
    input(f"\n{CYAN}Press Enter to return...{RESET}")

def phoenix_genesis():
    print(f"\n{BOLD}{RED}🔥 THE PHOENIX PROTOCOL (GENESIS MODE){RESET}")
    print(f"{YELLOW}WARNING: This will ARCHIVE your entire current Library and start a NEW ONE.")
    print("Your old files will be moved to 'Archive_Old_World' safely.")
    print(f"This is for a 'Brand New Life'.{RESET}")
    
    confirm = input(f"\nAre you ready for the Second Act? (Type 'BURN IT DOWN'): ")
    if confirm != "BURN IT DOWN":
        print("Aborted.")
        return

    lib_path = Path.expanduser(Path("~/Universal/Library"))
    if not lib_path.exists():
        print("Library does not exist yet. Creating new one...")
    else:
        ts = time.strftime("%Y-%m-%d_%H%M%S")
        archive_name = f"Archive_Old_World_{ts}"
        archive_path = lib_path.parent / archive_name
        
        print(f"   Moving Old World to {archive_path}...")
        try:
            os.rename(lib_path, archive_path)
            print(f"   {GREEN}Archive Successful.{RESET}")
        except Exception as e:
            print(f"   {RED}Failed to move library: {e}{RESET}")
            return

    # Genesis
    print("   Creating New World...")
    try:
        (lib_path / "Music").mkdir(parents=True)
        (lib_path / "Assets" / "Audio").mkdir(parents=True)
        (lib_path / "Assets" / "Images").mkdir(parents=True)
        (lib_path / "Assets" / "Docs").mkdir(parents=True)
        (lib_path / "Docs").mkdir(parents=True)
        print(f"   {GREEN}✨ WELCOME TO THE NEW WORLD.{RESET}")
        print(f"   Now run [1] OMEGA PROTOCOL on the Archive to import your best assets.")
    except Exception as e:
         print(f"   {RED}Genesis Failed: {e}{RESET}")
    
    input(f"\n{CYAN}Press Enter to return...{RESET}")

def main_menu():
    while True:
        print_banner()
        print(f"   {BOLD}Select Module:{RESET}")
        print(f"   [1] 🚀 OMEGA PROTOCOL    (Full System Run)")
        print(f"   [2] 👷 ENGR_KEITH        (Integrity Scan)")
        print(f"   [3] 🧠 MEMORY CORE       (Audit Search)")
        print(f"   [4] 🏴‍☠️ SCAVENGER         (Find Assets)")
        print(f"   [5] 🌀 WORMHOLE          (Ingest External)")
        print(f"   [6] 👁️ SONIC EYE         (Run Singularity)")
        print(f"   [7] 📡 MC96 STATUS       (Cloud Report)")
        print(f"   [8] 🔥 PHOENIX GENESIS   (Start New Life)")
        print(f"   [Q] 🚪 EXIT")
        
        choice = input(f"\n   {CYAN}COMMAND > {RESET}").lower().strip()
        
        if choice == '1': run_script("turbo_omega.py")
        elif choice == '2': run_script("turbo_keith.py")
        elif choice == '3': memory_core_search()
        elif choice == '4': run_script("turbo_scavenger.py")
        elif choice == '5': run_script("turbo_wormhole.py")
        elif choice == '6':
            target = input("   Target Directory (Enter for Library): ").strip()
            args = [target] if target else [str(Path.expanduser(Path("~/Universal/Library")))]
            run_script("turbo_singularity.py", args)
        elif choice == '7': run_script("deploy_to_universe.py")
        elif choice == '8': phoenix_genesis()
        elif choice == 'q':
            print(f"\n{GREEN}System Offline.{RESET}")
            sys.exit(0)
        else:
            print("Invalid Command.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit(0)
