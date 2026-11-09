import os
import sys
import subprocess
import time
import sqlite3
from pathlib import Path

import threading
import json

# Configuration
SCRIPTS_DIR = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Scripts")
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

def update_dashboard_feed():
    """Background thread to update the HTML Dashboard feed."""
    while True:
        try:
            # Gather Data
            data = {
                "system": {
                    "vibe": 100, # dynamic placeholder
                    "focus": "Monitoring",
                    "status": "ONLINE"
                },
                "agents": {}
            }
            
            # Connect to Brain for Real Stats
            try:
                conn = sqlite3.connect(str(DB_PATH))
                c = conn.cursor()
                
                # Vibe Check
                c.execute("SELECT vibe, context, goal FROM memory_events ORDER BY timestamp DESC LIMIT 1")
                latest = c.fetchone()
                if latest:
                    data['system']['vibe'] = latest[0]
                    data['system']['focus'] = latest[2]
                
                # Check Agents
                for agent in ['SHIRL', 'ENGR', 'GABRIEL', 'CORE']:
                    c.execute("SELECT context, timestamp FROM memory_events WHERE author=? ORDER BY timestamp DESC LIMIT 1", (agent,))
                    row = c.fetchone()
                    
                    status = "STANDBY"
                    focus = "Waiting"
                    last_seen = "Never"
                    
                    if row:
                        focus = row[0]
                        # check if active in last 5 min? 
                        # simplicity: just mark active if present
                        status = "ACTIVE" 
                    
                    data['agents'][agent] = {
                        "status": status,
                        "focus": focus
                    }
                
                conn.close()
            except: pass
            
            # Write JSON
            feed_path = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/team_status.json")
            with open(feed_path, 'w') as f:
                json.dump(data, f)
                
        except Exception: pass
        time.sleep(1)

# Start Pulse
threading.Thread(target=update_dashboard_feed, daemon=True).start()


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
        cid = res[0] if res else 0
        
        # Get Latest Vibe
        vibe = 50
        if cid:
            c.execute("SELECT vibe_score FROM memory_events WHERE cell_id = ? AND event_type = 'VIBE_CHECK' ORDER BY timestamp DESC LIMIT 1", (cid,))
            vibe_res = c.fetchone()
            if vibe_res: vibe = vibe_res[0]
        
        # Get Latest Goal
        goal = "Establish Connection"
        if cid:
            c.execute("SELECT content FROM memory_events WHERE cell_id = ? AND event_type = 'SHARED_GOAL' ORDER BY timestamp DESC LIMIT 1", (cid,))
            goal_res = c.fetchone()
            if goal_res: goal = goal_res[0]

        # Get Top Subjects (Tags)
        subjects = ""
        try:
            c.execute("SELECT tags FROM memory_events ORDER BY timestamp DESC LIMIT 20")
            rows = c.fetchall()
            all_tags = []
            for r in rows:
                if r[0]: all_tags.extend([t.strip() for t in r[0].split(',')])
            from collections import Counter
            common = Counter(all_tags).most_common(3)
            subjects = ", ".join([f"#{t[0]}" for t in common])
        except: pass
        
        conn.close()
        return vibe, goal, subjects
    except:
        return 50, "System Offline", ""

def print_banner():
    vibe, goal, subjects = get_heartbeat()
    
    # Visual Bar
    bar_len = 20
    filled = int((vibe / 100) * bar_len)
    bar = "█" * filled + "-" * (bar_len - filled)
    
    color = GREEN if vibe > 75 else YELLOW if vibe > 40 else RED
    
    clear_screen()
    print(f"{BOLD}{CYAN}")
    print("   ╔════════════════════════════════════════════╗")
    print("   ║              THE NEXUS CORE                ║")
    print("   ║          (Universal Control v52.0)         ║")
    print("   ╚════════════════════════════════════════════╝")
    
    print(f"\n   {color}❤️  RELATIONSHIP HEALTH: [{bar}] {vibe}%{RESET}")
    print(f"   {BOLD}🏆 FOCUS: {goal}{RESET}")
    
    # Persona Status
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        # Check last 1 hour
        c.execute("SELECT author, MAX(timestamp) FROM memory_events WHERE author IN ('SHIRL', 'ENGR') GROUP BY author")
        active_personas = c.fetchall()
        
        status_line = ""
        for p, ts in active_personas:
             # simple check if recent (e.g. today or last hour? assume if in DB its relevant context)
             status_line += f"{YELLOW}⚡ {p}: ACTIVE {RESET} "
        
        if status_line:
             print(f"   {status_line}")
        conn.close()
    except: pass

    if subjects:
         print(f"   {DIM}🧠 ACTIVE SUBJECTS: {subjects}{RESET}")
    print(f"{CYAN}   ──────────────────────────────────────────────{RESET}")

def run_script(script_name, args=[]):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"{RED}CORE > Script not found: {script_name}{RESET}")
        time.sleep(2)
        return
    
    cmd = ["python3", str(script_path)] + args
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}CORE > Interrupted.{RESET}")
    input(f"\n{CYAN}CORE > Press Enter to return to Nexus...{RESET}")

def memory_core_search():
    print(f"\n{BOLD}CORE > 🧠 MEMORY CORE SEARCH{RESET}")
    query = input("CORE > Enter search term (filename, hash, path): ").strip()
    if not query: return
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        sql = f"SELECT timestamp, action, original_path, final_path FROM provenance WHERE original_path LIKE ? OR final_path LIKE ? OR file_hash LIKE ? ORDER BY timestamp DESC LIMIT 20"
        wild_query = f"%{query}%"
        c.execute(sql, (wild_query, wild_query, wild_query))
        results = c.fetchall()
        
        if not results:
            print(f"{YELLOW}CORE > No records found.{RESET}")
        else:
            print(f"\nCORE > Found {len(results)} records:")
            for row in results:
                ts, act, orig, final = row
                print(f"[{ts}] {BOLD}{act}{RESET}")
                print(f"  From: {orig}")
                print(f"  To:   {final}")
                print("-" * 40)
        conn.close()
    except Exception as e:
        print(f"{RED}CORE > Database Error: {e}{RESET}")
    input(f"\n{CYAN}CORE > Press Enter to return...{RESET}")

def phoenix_genesis():
    print(f"\n{BOLD}{CYAN}CORE > 🔊 AUDIO UNITOR: SYSTEM ONLINE (v{VERSION}){RESET}")
    # Removed artificial sleep for Zero Latency
    # time.sleep(2)
    print(f"{YELLOW}WARNING: This will ARCHIVE your entire current Library and start a NEW ONE.")
    print("Your old files will be moved to 'Archive_Old_World' safely.")
    print(f"This is for a 'Brand New Life'.{RESET}")
    
    confirm = input(f"\nCORE > Are you ready for the Second Act? (Type 'BURN IT DOWN'): ")
    if confirm != "BURN IT DOWN":
        print("CORE > Aborted.")
        return

    lib_path = Path.expanduser(Path("~/Universal/Library"))
    if not lib_path.exists():
        print("CORE > Library does not exist yet. Creating new one...")
    else:
        ts = time.strftime("%Y-%m-%d_%H%M%S")
        archive_name = f"Archive_Old_World_{ts}"
        archive_path = lib_path.parent / archive_name
        
        print(f"CORE > Moving Old World to {archive_path}...")
        try:
            os.rename(lib_path, archive_path)
            print(f"   {GREEN}Archive Successful.{RESET}")
        except Exception as e:
            print(f"   {RED}Failed to move library: {e}{RESET}")
            return

    # Genesis
    print("CORE > Creating New World...")
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
    
    input(f"\n{CYAN}CORE > Press Enter to return...{RESET}")

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
        print_banner()
        
        print(f"   [1] ⛩️  OMEGA PROTOCOL     (The Engine)")
        print(f"   [2] 💿 KEITH               (The Builder)")
        print(f"   [3] 🧠 MEMORY CORE         (The Search)")
        print(f"   [4] 🏴‍☠️ SCAVENGER           (The Hunter)")
        print(f"   [5] ⏳ TIME MACHINE        (The Safety)")
        print(f"   [6] 🌪️ SINGULARITY         (The Fixer)")
        print(f"   [7] 📡 MC96 STATUS         (Cloud Report)")
        print(f"   [8] 🔥 PHOENIX GENESIS     (Start New Life)")
        print(f"   [9] 🧬 MEMCELL             (The Caretaker)")
        print(f"   [T] 👥 NOIZY TEAM          (Conference Room)")
        print(f"   [G] 👁️ GABRIEL             (The Preacher)")
        print(f"   [O] ⏳ ANALYZE OVERLAP     (Temporal Intelligence)")
        print(f"   [C] 💬 CHAT MODE           (Neural Link)")
        print(f"{DIM}" + "-"*50 + f"{RESET}")
        print(f"   {BOLD}NEW TOOLS:{RESET}")
        print(f"   [V] 📊 VISUALIZER          (Generate Report)")
        print(f"   [M] 🗺️ CARTOGRAPHER        (Map Density)")
        print(f"   [H] 👻 GHOST HUNTER        (Scan Mounts)")
        print(f"   [D] 🎹 VI DATABASE         (Plugin Tools)")
        print(f"   [S] 🌐 START SERVER        (Nexus API)")
        print(f"   [W] 🛡️ SENTINEL            (Watchdog)")
        print(f"{DIM}" + "-"*50 + f"{RESET}")
        print(f"   [Q] 🚪 EXIT")
        print(f"{DIM}" + "-"*50 + f"{RESET}")
        print(f"{CYAN}   Type a Number, or Just Talk to Me...{RESET}")
        
        choice = input(f"\n   {CYAN}CORE > {RESET}").strip()
        lower_choice = choice.lower()
        
        # Standard Menu Routing
        if lower_choice == '1': run_script("turbo_omega.py")
        elif lower_choice == '2': run_script("turbo_keith.py")
        elif lower_choice == '3': memory_core_search()
        elif lower_choice == '4': run_script("turbo_scavenger.py")
        elif lower_choice == '5': run_script("turbo_wormhole.py")
        elif lower_choice == '6':
            target = input("CORE > Target Directory (Enter for Library): ").strip()
            args = [target] if target else [str(Path.expanduser(Path("~/Universal/Library")))]
            run_script("turbo_singularity.py", args)
        elif lower_choice == '7': run_script("deploy_to_universe.py")
        elif lower_choice == '8': phoenix_genesis()
        elif lower_choice == '9': run_script("turbo_memcell.py")
        elif lower_choice == 't':
             print(f"{GREEN}CORE > 👥 Opening Conference Room...{RESET}")
             subprocess.run(["open", "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/noizy_team.html"])
        elif lower_choice == 'g': run_script("turbo_gabriel.py")
        elif lower_choice == 'o': 
             caretaker.analyze_overlap()
             input(f"\n{CYAN}CORE > Press Enter to return...{RESET}")
        elif lower_choice == 'c': run_script("turbo_memcell.py") # Still allow dedicated mode
        # New Tools
        elif lower_choice == 'v': run_script("turbo_vis.py")
        elif lower_choice == 'm': run_script("turbo_cartographer.py")
        elif lower_choice == 'h': run_script("turbo_ghost.py")
        elif lower_choice == 'd': run_script("turbo_vi.py")
        elif lower_choice == 's': run_script("turbo_server.py")
        elif lower_choice == 'w': run_script("turbo_sentinel.py")
        elif lower_choice == 'q':
            print(f"\n{GREEN}CORE > System Offline.{RESET}")
            sys.exit(0)
        else:
            # OMNI-INPUT: Treat as Neural Command
            # First check if it's empty
            if not choice: continue
            
            # Pass to Caretaker
            caretaker.process_neural_input(choice, author="USER")
            # input(f"\n{CYAN}CORE > Press Enter to continue...{RESET}") # Optional pause



if __name__ == "__main__":
    nexus_dashboard()
