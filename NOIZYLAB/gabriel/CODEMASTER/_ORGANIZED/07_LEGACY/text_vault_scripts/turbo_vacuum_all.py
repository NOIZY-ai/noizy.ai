#!/usr/bin/env python3
# ==============================================================================
# ⚫ TURBO VACUUM ALL (OMNIVOROUS CLEANER)
# ==============================================================================
# Deletes empty folders and junk files across ALL mounted volumes.
# PROTOCOL: GORUNFREE

import os
import sys
from pathlib import Path

try:
    import turbo_config as cfg
    import turbo_vacuum
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_vacuum

SKIP_VOLUMES = ["M2Ultra", "Recovery", "VM", "Preboot", "Update"]

def vacuum_all():
    cfg.print_header("⚫ OMNI-VACUUM", "Initiating System-Wide Cleanup")
    
    volumes_dir = Path("/Volumes")
    if not volumes_dir.exists():
        print(f"CORE > {cfg.RED}Error: /Volumes not found.{cfg.RESET}")
        return

    targets = [v for v in volumes_dir.iterdir() if v.is_dir()]
    
    print(f"CORE > Found {len(targets)} candidate volumes.")
    
    for vol in targets:
        if vol.name in SKIP_VOLUMES or vol.name.startswith("."):
            print(f"CORE > ⏭️  Skipping {vol.name} (Protected)")
            continue
            
        print(f"\n{cfg.BOLD}{cfg.MAGENTA}CORE > 🌪️  VACUUMING: {vol.name}{cfg.RESET}")
        turbo_vacuum.run_vacuum(vol)
        
    print(f"\n{cfg.BOLD}{cfg.GREEN}CORE > ✨ OMNI-CLEAN COMPLETE.{cfg.RESET}")

if __name__ == "__main__":
    confirm = input("⚠️  WARNING: This will delete ALL empty folders and junk files on ALL drives. Proceed? (y/n): ")
    if confirm.lower() == 'y':
        vacuum_all()
    else:
        print("CORE > Aborted.")
