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
    print(f"\n{BOLD}{MAGENTA}⛩️  PHASE: {step_name}{RESET}")
    start_t = time.time()
    
    cmd = ["python3", str(SCRIPTS_DIR / script_name)] + args
    try:
        # Run subprocess and stream output? Or just let it print?
        # Let it print to show progress of each tool
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ {step_name} Failed: {e}{RESET}")
        return False
    except KeyboardInterrupt:
        print(f"\n{YELLOW}⚠️  Interrupted during {step_name}{RESET}")
        return False
        
    duration = time.time() - start_t
    print(f"{GREEN}✅ {step_name} Complete ({duration:.1f}s){RESET}")
    return True

def run_omega(target_dir):
    print(f"{BOLD}{YELLOW}⚡ THE OMEGA PROTOCOL: TOTAL SYSTEM UNIFICATION ⚡{RESET}")
    print(f"   Target: {target_dir}")
    print(f"   Mode:   FULL AUTONOMY")
    
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"   {RED}❌ Target not found.{RESET}")
        return

    # 1. VACUUM (The Black Hole Part 1)
    # Remove junk/empty dirs first to avoid processing them.
    if not run_step("VACUUM (Deep Clean)", "turbo_vacuum.py", [str(target_path)]): return

    # 2. DEDUP (The Black Hole Part 2)
    # Remove duplicates.
    # Note: Dedup scans the DB. We should re-index first?
    # Actually, dedup works on the DB. Vacuum might have deleted things.
    # Ideally we should Index -> Dedup -> Index?
    # But Dedup script runs a query. Let's assume DB is relatively fresh OR run indexer?
    # Let's run a quick index update first to be safe?
    # User wanted "FAST". Dedup might rely on old data if we don't index.
    # But Dedup checks file existence before deleting usually? The script I wrote checks 'copies' from DB.
    # If I vacuuumed, the DB might point to non-existent files.
    # So: VACUUM -> INDEX -> DEDUP -> SANITIZE -> CONVERT -> LIBRARIAN -> FINAL INDEX?
    # That's thorough.
    
    # Let's do:
    # 1. Vacuum
    # 2. Index (Essential for Dedup to be accurate)
    if not run_step("NEURAL INDEX (Pre-Scan)", "turbo_indexer.py", [str(target_path)]): return
    
    # 3. Dedup (Auto-Nuke)
    if not run_step("DEDUP (Auto-Nuke)", "turbo_dedup.py", ["--nuke"]): return

    # 4. SINGULARITY (Atomic Fix)
    # Replaces: Sanitizer, Alchemist, Librarian, Architect
    if not run_step("SINGULARITY (Atomic Unification)", "turbo_singularity.py", [str(target_path)]): return

    # 5. Final Index (Update DB with new structure)
    # Now we must scan the DESTINATION since files moved.
    # The Organizer moves them to ~/Universal/Library
    library_path = Path.expanduser(Path("~/Universal/Library"))
    if not run_step("NEURAL INDEX (Final Update)", "turbo_indexer.py", [str(library_path)]): return

    print(f"\n{BOLD}{GREEN}⛩️  OMEGA PROTOCOL COMPLETE.{RESET}")
    print(f"   The System is Perfection.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_omega.py <target_dir>")
    else:
        run_omega(sys.argv[1])
