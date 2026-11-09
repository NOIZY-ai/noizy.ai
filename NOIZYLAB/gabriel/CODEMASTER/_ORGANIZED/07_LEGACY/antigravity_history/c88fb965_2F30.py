import os
import sys
import time
import subprocess
import argparse
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega")
SCRIPTS_DIR = BASE_DIR / "Audio_Unitor/Scripts"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def run_step(step_name, command):
    print(f"\n{BOLD}🔄 STEP: {step_name}{RESET}")
    print(f"   Cmd: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        print(f"   {GREEN}✅ {step_name} Complete.{RESET}")
    except subprocess.CalledProcessError as e:
        print(f"   {RED}❌ {step_name} Failed: {e}{RESET}")
        sys.exit(1)

def run_harvester(source_dir=None):
    print(f"{BOLD}{CYAN}🌪️  THE HARVESTER: CHAOS INGESTION ENGINE{RESET}")
    
    # 1. Determine Source
    if not source_dir:
        default_dl = Path.home() / "Downloads"
        i = input(f"   🎯 Target Directory [Default: {default_dl}]: ").strip()
        source_dir = i if i else str(default_dl)
        
    src_path = Path(source_dir)
    if not src_path.exists():
        print(f"   {RED}❌ Source not found: {src_path}{RESET}")
        return

    start_time = time.time()

    # 2. Pipeline Execution
    
    # A. ORGANIZE (Sort Chaos -> Vault)
    # python3 turbo_organizer.py <source>
    run_step("SORTING CHAOS", ["python3", str(SCRIPTS_DIR / "turbo_organizer.py"), str(src_path)])
    
    # B. INDEX (Update Universe DB)
    # We index the Vault (Universal) to capture the newly sorted files
    vault_path = Path.home() / "Universal"
    run_step("NEURAL INDEXING", ["python3", str(SCRIPTS_DIR / "turbo_indexer.py"), str(vault_path)])
    
    # C. DEDUP (Check for Waste)
    run_step("CHECKING FOR WASTE", ["python3", str(SCRIPTS_DIR / "turbo_dedup.py")])
    
    duration = time.time() - start_time
    print(f"\n{GREEN}✨ HARVEST COMPLETE ({duration:.2f}s){RESET}")
    print(f"   The Chaos has been consumed, sorted, indexed, and optimized.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Harvester: Chaos Ingestion Pipeline")
    parser.add_argument("source", nargs="?", help="Source directory to ingest")
    args = parser.parse_args()
    
    try:
        run_harvester(args.source)
    except KeyboardInterrupt:
        print("\n⚠️ Ingestion Aborted.")
