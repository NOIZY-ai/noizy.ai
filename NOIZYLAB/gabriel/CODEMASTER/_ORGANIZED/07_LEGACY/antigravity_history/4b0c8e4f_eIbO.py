import os
import sys
import subprocess
import time
from pathlib import Path

# Configuration
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
MAGENTA = '\033[95m'

SCRIPTS_DIR = Path(__file__).parent

def run_step(step_name, script_name, args=[]):
    print(f"\n{BOLD}{MAGENTA}CORE > ⛩️  PHASE: {step_name}{RESET}")
    start_t = time.time()
    
    cmd = ["python3", str(SCRIPTS_DIR / script_name)] + args
    try:
        # Run subprocess and stream output? Or just let it print?
        # Let it print to show progress of each tool
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}CORE > ⚠️ {step_name} Failed: {e}{RESET}")
        return False
    except KeyboardInterrupt:
        print(f"\n{YELLOW}CORE > ⚠️  Interrupted: {step_name}{RESET}")
        return False
        
    duration = time.time() - start_t
    print(f"{GREEN}CORE > ✅ {step_name} Complete ({duration:.1f}s){RESET}")
    return True

def run_omega(target_dir):
    print(f"{BOLD}{YELLOW}CORE > ⚡ THE OMEGA PROTOCOL: TOTAL SYSTEM UNIFICATION ⚡{RESET}")
    print(f"CORE > Target: {target_dir}")
    print(f"CORE > Mode:   FULL AUTONOMY (Zero Latency)")
    
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"CORE > {RED}❌ Target not found.{RESET}")
        return

    # 1. VACUUM (The Black Hole Part 1)
    # Remove junk/empty dirs first to avoid processing them.
    if not run_step("VACUUM (Deep Clean)", "turbo_vacuum.py", [str(target_path)]): return
    
    print(f"\n{BOLD}CORE > ⚠️  WARNING: SINGULARITY EVENT IMMINENT.{RESET}")

    # 2. WORMHOLE SCANNER (Universal Ingestion)
    # Bring external matter into the Universe first.
    if not run_step("WORMHOLE (External Ingestion)", "turbo_wormhole.py", []): return

    # 3. VACUUM (Black Hole Part 2)
    if not run_step("VACUUM (Black Hole)", "turbo_vacuum.py", [str(target_path)]): return

    # 4. NEURAL INDEX (Genesis Scan)
    if not run_step("NEURAL INDEX (Genesis Scan)", "turbo_indexer.py", [str(target_path)]): return

    # 5. SINGULARITY (Atomic Fix)
    # Replaces: Sanitizer, Alchemist, Librarian, Architect
    if not run_step("SINGULARITY (Atomic Unification)", "turbo_singularity.py", [str(target_path)]): return

    # 6. FINAL INDEX
    # Now we must scan the DESTINATION since files moved.
    # The Organizer moves them to ~/Universal/Library
    library_path = Path.expanduser(Path("~/Universal/Library"))
    if not run_step("NEURAL INDEX (Final Update)", "turbo_indexer.py", [str(library_path)]): return

    print(f"\n{BOLD}{GREEN}CORE > ⛩️  OMEGA PROTOCOL COMPLETE.{RESET}")
    print(f"CORE > The System is Perfection.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_omega.py <target_dir>")
    else:
        run_omega(sys.argv[1])
