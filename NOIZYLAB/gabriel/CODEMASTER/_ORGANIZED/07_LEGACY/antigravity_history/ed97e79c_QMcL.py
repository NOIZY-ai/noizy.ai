import os
import sys
import shutil
from pathlib import Path

# Configuration
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

JUNK_FILES = {'.DS_Store', 'Thumbs.db', 'desktop.ini', '__MACOSX'}

def run_vacuum(target_dir):
    print(f"{BOLD}{CYAN}⚫  TURBO VACUUM: THE VOID{RESET}")
    print(f"   Target: {target_dir}")
    
    root_path = Path(target_dir)
    if not root_path.exists():
        print(f"   {RED}❌ Target not found.{RESET}")
        return

    files_removed = 0
    dirs_removed = 0
    bytes_freed = 0
    
    # 1. Remove Junk Files & Ghost Files (Bottom-Up)
    print("   Consumer of Worlds (Files)...")
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            fpath = Path(root) / name
            remove = False
            reason = ""
            
            # Check Junk List
            if name in JUNK_FILES or name.startswith("._"):
                remove = True
                reason = "System Junk"
                
            # Check Ghost Files (0 bytes)
            # Note: Verify it's not a special marker file? 
            # In audio world, 0 byte usually means failed copy or corruption.
            elif fpath.stat().st_size == 0:
                remove = True
                reason = "Ghost File (0B)"
            
            if remove:
                try:
                    fpath.unlink()
                    # print(f"      Consumed: {name} ({reason})")
                    files_removed += 1
                except Exception as e:
                    print(f"      {RED}Failed to consume {name}: {e}{RESET}")

    # 2. Remove Empty Directories (Bottom-Up)
    print("   Collapsing Dimensions (Empty Folders)...")
    # Walk again or reuse? Walk again to ensure we catch dirs emptied by file removal
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in dirs:
            dpath = Path(root) / name
            try:
                # rmdir only works if empty, so it's safe
                dpath.rmdir()
                # print(f"      Collapsed: {name}")
                dirs_removed += 1
            except OSError:
                # Not empty, ignore
                pass
                
    print(f"\n{GREEN}✨ SINGULARITY COMPLETE{RESET}")
    print(f"   Files Consumed: {files_removed}")
    print(f"   Dims Collapsed: {dirs_removed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_vacuum.py <target_dir>")
    else:
        run_vacuum(sys.argv[1])
