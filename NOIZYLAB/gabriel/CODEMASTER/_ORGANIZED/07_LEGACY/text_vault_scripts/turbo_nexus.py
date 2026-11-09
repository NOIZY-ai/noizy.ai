#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import sqlite3
import threading
import json
from pathlib import Path

try:
    import turbo_config as cfg
    import turbo_gabriel # Gabriel Integration
    import turbo_prompts as prompts
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel
    import turbo_prompts as prompts

# Configuration
SCRIPTS_DIR = cfg.SCRIPTS_DIR
DB_PATH = cfg.UNIVERSE_DB_PATH

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
                if DB_PATH.exists():
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
                        
                        if row:
                            focus = row[0]
                            status = "ACTIVE" 
                        
                        data['agents'][agent] = {
                            "status": status,
                            "focus": focus
                        }
                    
                    conn.close()
            except: pass
            
            # Write JSON
            feed_path = SCRIPTS_DIR.parent / "Dashboard" / "team_status.json"
            with open(feed_path, 'w') as f:
                json.dump(data, f)
                
        except Exception: pass
        time.sleep(1)

# Start Pulse
threading.Thread(target=update_dashboard_feed, daemon=True).start()

# Helper for Clear Screen
def clear_screen():
    print(cfg.CLEAR_SCREEN, end="")

def get_heartbeat():
    try:
        if not DB_PATH.exists(): return 50, "System Offline", ""
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
    
    color = cfg.GREEN if vibe > 75 else cfg.YELLOW if vibe > 40 else cfg.RED
    
    # Using 'clear' command or ANSI escape sequence from config? 
    # Let's rely on print call or standard ANSI
    # cfg.CLEAR_SCREEN is not explicitly defined in the file I wrote earlier (oversight). 
    # I'll just use the ANSI code directly or add it to cfg later.
    print("\033[H\033[J", end="") # Direct Clear
    print(f"{cfg.BOLD}{cfg.CYAN}")
    print("   ╔════════════════════════════════════════════╗")
    print("   ║              THE NEXUS CORE                ║")
    print("   ║          (Universal Control v52.0)         ║")
    print("   ╚════════════════════════════════════════════╝")
    
    print(f"\n   {color}❤️  RELATIONSHIP HEALTH: [{bar}] {vibe}%{cfg.RESET}")
    print(f"   {cfg.BOLD}🏆 FOCUS: {goal}{cfg.RESET}")
    
    # Persona Status
    try:
        if DB_PATH.exists():
            conn = sqlite3.connect(str(DB_PATH))
            c = conn.cursor()
            c.execute("SELECT author, MAX(timestamp) FROM memory_events WHERE author IN ('SHIRL', 'ENGR') GROUP BY author")
            active_personas = c.fetchall()
            
            status_line = ""
            for p, ts in active_personas:
                 status_line += f"{cfg.YELLOW}⚡ {p}: ACTIVE {cfg.RESET} "
            
            if status_line:
                 print(f"   {status_line}")
            conn.close()
    except: pass

    if subjects:
         print(f"   {cfg.DIM}🧠 ACTIVE SUBJECTS: {subjects}{cfg.RESET}")
    print(f"{cfg.CYAN}   ──────────────────────────────────────────────{cfg.RESET}")

def run_script(script_name, args=[]):
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        cfg.system_log(f"Script not found: {script_name}", "ERROR")
        time.sleep(2)
        return
    
    cmd = ["python3", str(script_path)] + args
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{cfg.YELLOW}CORE > Interrupted.{cfg.RESET}")
    input(f"\n{cfg.CYAN}CORE > Press Enter to return to Nexus...{cfg.RESET}")

def memory_core_search():
    cfg.print_header("MEMORY CORE SEARCH")
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
            cfg.system_log("No records found.", "WARN")
        else:
            print(f"\nCORE > Found {len(results)} records:")
            for row in results:
                ts, act, orig, final = row
                print(f"[{ts}] {cfg.BOLD}{act}{cfg.RESET}")
                print(f"  From: {orig}")
                print(f"  To:   {final}")
                print("-" * 40)
        conn.close()
    except Exception as e:
        cfg.system_log(f"Database Error: {e}", "ERROR")
    input(f"\n{cfg.CYAN}CORE > Press Enter to return...{cfg.RESET}")

def phoenix_genesis():
    cfg.print_header("PHOENIX GENESIS", f"SYSTEM ONLINE (v{cfg.VERSION})")
    print(f"{cfg.YELLOW}WARNING: This will ARCHIVE your entire current Library and start a NEW ONE.")
    print("Your old files will be moved to 'Archive_Old_World' safely.")
    print(f"This is for a 'Brand New Life'.{cfg.RESET}")
    
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
        
        cfg.system_log(f"Moving Old World to {archive_path}...", "INFO")
        try:
            os.rename(lib_path, archive_path)
            cfg.system_log("Archive Successful.", "SUCCESS")
        except Exception as e:
            cfg.system_log(f"Failed to move library: {e}", "ERROR")
            return

    # Genesis
    print("CORE > Creating New World...")
    try:
        (lib_path / "Music").mkdir(parents=True)
        (lib_path / "Assets" / "Audio").mkdir(parents=True)
        (lib_path / "Assets" / "Images").mkdir(parents=True)
        (lib_path / "Assets" / "Docs").mkdir(parents=True)
        (lib_path / "Docs").mkdir(parents=True)
        
        cfg.system_log("✨ WELCOME TO THE NEW WORLD.", "SUCCESS")
        print(f"   Now run [1] OMEGA PROTOCOL on the Archive to import your best assets.")
    except Exception as e:
         cfg.system_log(f"Genesis Failed: {e}", "ERROR")
    
    input(f"\n{cfg.CYAN}CORE > Press Enter to return...{cfg.RESET}")

def nexus_dashboard():
    # Initialize the Caretaker for Omni-Input
    try:
        from turbo_memcell import MemCell
        caretaker = MemCell()
    except ImportError:
        caretaker = None
    
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
        print(f"{cfg.DIM}" + "-"*50 + f"{cfg.RESET}")
        print(f"   {cfg.BOLD}NEW TOOLS:{cfg.RESET}")
        print(f"   [V] 📊 VISUALIZER          (Generate Report)")
        print(f"   [M] 🗺️ CARTOGRAPHER        (Map Density)")
        print(f"   [H] 👻 GHOST HUNTER        (QUARANTINED)")
        print(f"   [D] 🎹 VI DATABASE         (Plugin Tools)")
        print(f"   [S] 🌐 START SERVER        (Nexus API)")
        print(f"   [W] 🛡️ SENTINEL            (Watchdog)")
        print(f"   [P] 🔌 PLUGINS             (Scan VST/AU)")
        print(f"   [A] 🌊 SONIC               (Audio Analysis)")
        print(f"   [L] 🎨 LOGOS               (Visual Hunter)")
        print(f"   [K] 📦 COLLECTOR           (Harvest Code)")
        print(f"   [U] ☁️  UPLOAD             (Deploy to Cloud)")
        print(f"{cfg.DIM}" + "-"*50 + f"{cfg.RESET}")
        print(f"   [Q] 🚪 EXIT")
        print(f"{cfg.DIM}" + "-"*50 + f"{cfg.RESET}")
        print(f"{cfg.CYAN}   Type a Number, or Just Talk to Me...{cfg.RESET}")
        
        choice = input(f"\n   {cfg.CYAN}CORE > {cfg.RESET}").strip()
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
        elif lower_choice == '7': run_script("turbo_deploy.py") # Updated
        elif lower_choice == '8': phoenix_genesis()
        elif lower_choice == '9': run_script("turbo_memcell.py")
        elif lower_choice == 't':
             cfg.system_log("Opening Conference Room...", "SUCCESS")
             subprocess.run(["open", str(SCRIPTS_DIR.parent / "Dashboard" / "noizy_team.html")])
        elif lower_choice == 'g': run_script("turbo_gabriel.py")
        elif lower_choice == 'o': 
             if caretaker:
                 caretaker.analyze_overlap()
                 input(f"\n{cfg.CYAN}CORE > Press Enter to return...{cfg.RESET}")
        elif lower_choice == 'c': run_script("turbo_memcell.py") 
        # New Tools
        elif lower_choice == 'v': run_script("turbo_vis.py")
        elif lower_choice == 'm': run_script("turbo_cartographer.py")
        elif lower_choice == 'h': 
             # run_script("turbo_ghost.py")
             print(f"{cfg.RED}   👻 GHOST HUNTER IS QUARANTINED.{cfg.RESET}")
             time.sleep(1)
        elif lower_choice == 'd': run_script("turbo_vi.py")
        elif lower_choice == 's': run_script("turbo_server.py")
        elif lower_choice == 'w': run_script("turbo_sentinel.py")
        elif lower_choice == 'p': run_script("turbo_plugins.py") # Updated
        elif lower_choice == 'a': run_script("turbo_sonic.py")   # Updated
        elif lower_choice == 'l': run_script("turbo_hunter.py")  # Updated
        elif lower_choice == 'k': run_script("turbo_collector.py") # New Collector
        elif lower_choice == 'u': run_script("turbo_deploy.py")  # Updated
        elif lower_choice == 'q':
            print(f"\n{cfg.GREEN}CORE > System Offline.{cfg.RESET}")
            sys.exit(0)
        else:
            if not choice: continue
            if caretaker:
                # Pass to Caretaker
                caretaker.process_neural_input(choice, author="USER")

if __name__ == "__main__":
    nexus_dashboard()
