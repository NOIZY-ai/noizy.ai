# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

import os
import shutil
import time
import subprocess
import sys
from pathlib import Path

try:
    import turbo_config as cfg
    import turbo_gabriel
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel

# Configuration
WORMHOLE_NAME = "Ω_DROP"
SEARCH_PATHS = [
    Path.expanduser(Path("~/Downloads")),
    Path.expanduser(Path("~/Desktop")),
    Path("/Volumes")
]
SINGULARITY_SCRIPT = "turbo_singularity.py"

# Colors
CYAN = cfg.CYAN
GREEN = cfg.GREEN
YELLOW = cfg.YELLOW
RED = cfg.RED
RESET = cfg.RESET
BOLD = cfg.BOLD

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
