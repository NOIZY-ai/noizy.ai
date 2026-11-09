import os
import shutil
import time
import subprocess
from pathlib import Path

# Configuration
WORMHOLE_NAME = "Ω_DROP"
SEARCH_PATHS = [
    Path.expanduser(Path("~/Downloads")),
    Path.expanduser(Path("~/Desktop")),
    Path("/Volumes")
]
SINGULARITY_SCRIPT = "turbo_singularity.py"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def collapse_wormhole(path):
    try:
        # Only remove if empty (Singularity should have consumed everything)
        # Check if empty
        if not any(path.iterdir()):
            path.rmdir()
            print(f"CORE > 💫 Wormhole Collapsed: {path}")
            return True
        else:
            print(f"CORE > ⚠️ Wormhole still active (not empty): {path}")
            return False
    except Exception as e:
        print(f"CORE > ❌ Failed to collapse {path}: {e}")
        return False

def activate_wormhole(path):
    print(f"CORE > 🌌 Wormhole Detected at: {path}")
    print("CORE > Engaging Singularity...")
    
    # Call Singularity on this path
    script_dir = Path(__file__).parent
    singularity_path = script_dir / SINGULARITY_SCRIPT
    
    try:
        subprocess.run(["python3", str(singularity_path), str(path)], check=True)
        # After Singularity returns, try to collapse
        collapse_wormhole(path)
    except subprocess.CalledProcessError:
        print(f"CORE > ❌ Singularity Core Failure at {path}")
    except Exception as e:
        print(f"CORE > ❌ Activation Error: {e}")

def run_wormhole_scanner():
    print(f"{BOLD}{CYAN}CORE > 🔭 WORMHOLE SCANNER INITIATED{RESET}")
    print("CORE > Scanning the Universe for Ω_DROP zones...")
    
    found_count = 0
    
    for base_path in SEARCH_PATHS:
        if not base_path.exists(): continue
        
        # Check root of these paths
        target = base_path / WORMHOLE_NAME
        if target.exists() and target.is_dir():
            activate_wormhole(target)
            found_count += 1
            
        # For /Volumes, check inside each mount
        if base_path == Path("/Volumes"):
            try:
                for mount in base_path.iterdir():
                    # Skip boot volume symlink if present or protected?
                    # Generally safely check subdirs
                    if mount.is_dir():
                        target = mount / WORMHOLE_NAME
                        if target.exists() and target.is_dir():
                            activate_wormhole(target)
                            found_count += 1
            except: pass

    if found_count == 0:
        print(f"CORE > {YELLOW}No active wormholes detected.{RESET}")
    else:
        print(f"\n{GREEN}CORE > ✨ Processed {found_count} Wormholes.{RESET}")

if __name__ == "__main__":
    run_wormhole_scanner()
