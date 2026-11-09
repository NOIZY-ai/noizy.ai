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
DIM = '\033[2m'
CLEAR = "\033[H\033[J"

def clear_screen():
    print(CLEAR, end="")

def get_heartbeat():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        
        # Get Covenant ID
        c.execute("SELECT id FROM memcells WHERE topic = 'THE COVENANT (PARTNERSHIP)'")
        res = c.fetchone()
        if not res: return 50, "No Covenant Yet"
        cid = res[0]
        
        # Get Latest Vibe
        c.execute("SELECT vibe_score FROM memory_events WHERE cell_id = ? AND event_type = 'VIBE_CHECK' ORDER BY timestamp DESC LIMIT 1", (cid,))
        vibe_res = c.fetchone()
        vibe = vibe_res[0] if vibe_res else 50
        
        # Get Latest Goal
        c.execute("SELECT content FROM memory_events WHERE cell_id = ? AND event_type = 'SHARED_GOAL' ORDER BY timestamp DESC LIMIT 1", (cid,))
        goal_res = c.fetchone()
        goal = goal_res[0] if goal_res else "Establish Connection"
        
        conn.close()
        return vibe, goal
    except:
        return 50, "System Offline"

def print_banner():
    vibe, goal = get_heartbeat()
    
    # Visual Bar
    bar_len = 20
    filled = int((vibe / 100) * bar_len)
    bar = "█" * filled + "-" * (bar_len - filled)
    
    color = GREEN if vibe > 75 else YELLOW if vibe > 40 else RED
    
    clear_screen()
    print(f"{BOLD}{CYAN}")
    print("   ╔════════════════════════════════════════════╗")
    print("   ║         THE NEXUS CORE (ENGR v42.0)        ║")
    print("   ║     Universal AI Command Interface (God)   ║")
    print("   ╚════════════════════════════════════════════╝")
    
    print(f"\n   {color}❤️  RELATIONSHIP HEALTH: [{bar}] {vibe}%{RESET}")
    print(f"   {BOLD}🏆 FOCUS: {goal}{RESET}")
    print(f"{CYAN}   ──────────────────────────────────────────────{RESET}")

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

import sys
from pathlib import Path
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

def nexus_dashboard():
    # Initialize the Caretaker for Omni-Input
    caretaker = MemCell()
    
    while True:
        # Get Status for Banner
        # (Simplified for speed)
        
        print(f"\n{BOLD} AUDIO UNITOR // NEXUS CORE {RESET}")
        print(f"{GREEN}❤️ RELATIONSHIP HEALTH: [██████████] 100%{RESET}")
        print(f"{YELLOW}🏆 FOCUS: Rebuild the Universe{RESET}")
        print(f"{DIM}" + "="*50 + f"{RESET}")
        
        print(f"   [1] ⛩️  OMEGA PROTOCOL     (The Engine)")
        print(f"   [2] 💿 KEITH               (The Builder)")
        print(f"   [3] 🧠 MEMORY CORE         (The Search)")
        print(f"   [4] 🏴‍☠️ SCAVENGER           (The Hunter)")
        print(f"   [5] ⏳ TIME MACHINE        (The Safety)")
        print(f"   [6] 🌪️ SINGULARITY         (The Fixer)")
        print(f"   [7] 📡 MC96 STATUS         (Cloud Report)")
        print(f"   [8] 🔥 PHOENIX GENESIS     (Start New Life)")
        print(f"   [9] 🧬 MEMCELL             (The Caretaker)")
        print(f"   [C] 💬 CHAT MODE           (Dedicated Mode)")
        print(f"   [Q] 🚪 EXIT")
        print(f"{DIM}" + "-"*50 + f"{RESET}")
        print(f"{CYAN}   Type a Number, or Just Talk to Me...{RESET}")
        
        choice = input(f"\n   {CYAN}NEURAL INPUT > {RESET}").strip()
        lower_choice = choice.lower()
        
        # Standard Menu Routing
        if lower_choice == '1': run_script("turbo_omega.py")
        elif lower_choice == '2': run_script("turbo_keith.py")
        elif lower_choice == '3': memory_core_search()
        elif lower_choice == '4': run_script("turbo_scavenger.py")
        elif lower_choice == '5': run_script("turbo_wormhole.py")
        elif lower_choice == '6':
            target = input("   Target Directory (Enter for Library): ").strip()
            args = [target] if target else [str(Path.expanduser(Path("~/Universal/Library")))]
            run_script("turbo_singularity.py", args)
        elif lower_choice == '7': run_script("deploy_to_universe.py")
        elif lower_choice == '8': phoenix_genesis()
        elif lower_choice == '9': run_script("turbo_memcell.py")
        elif lower_choice == 'c': run_script("turbo_memcell.py") # Still allow dedicated mode
        elif lower_choice == 'q':
            print(f"\n{GREEN}System Offline.{RESET}")
            sys.exit(0)
        else:
            # OMNI-INPUT: Treat as Neural Command
            # First check if it's empty
            if not choice: continue
            
            # Pass to Caretaker
            caretaker.process_neural_input(choice)
            # Loop continues automatically

if __name__ == "__main__":
    nexus_dashboard()
