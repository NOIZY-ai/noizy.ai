import subprocess
import time
import sys
from datetime import datetime

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

SCRIPTS_DIR = "Audio_Unitor/Scripts"

def run_step(name, script, args=None):
    print(f"\n{BOLD}🔄 STEP: {name}{RESET}")
    start = time.time()
    cmd = ["python3", f"{SCRIPTS_DIR}/{script}"]
    if args:
        cmd.extend(args)
        
    try:
        subprocess.run(cmd, check=True)
        duration = time.time() - start
        print(f"{GREEN}✅ {name} Complete ({duration:.2f}s){RESET}")
        return True
    except subprocess.CalledProcessError:
        print(f"{YELLOW}❌ {name} Failed{RESET}")
        return False

def maintenance_routine():
    print(f"{BOLD}{CYAN}╔════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║    DAILY MAINTENANCE PROTOCOL (AUTO)   ║{RESET}")
    print(f"{BOLD}{CYAN}╚════════════════════════════════════════╝{RESET}")
    print(f"Timestamp: {datetime.now()}")
    
    # 1. Update the Map (Parallel Indexing)
    if not run_step("Global Indexing", "global_indexer.py"):
        return

    # 2. Add Intelligence (Smart Tagging)
    if not run_step("Smart Tagging", "smart_tagger.py"):
        return
        
    # 3. Analyze Health (Sonic Fingerprints)
    if not run_step("Sonic Analysis", "sonic_analyzer.py"):
        return

    # 4. Generate Report (Visuals) - Coming next
    # if not run_step("Visual Report", "universe_report.py"):
    #    return

    print(f"\n{GREEN}✨ SYSTEM MAINTENANCE COMPLETE. ALL SYSTEMS OPTIMAL.{RESET}")

if __name__ == "__main__":
    maintenance_routine()
