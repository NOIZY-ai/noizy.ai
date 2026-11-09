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
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import turbo_config as cfg
    import turbo_gabriel
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel

# Configuration
SCAVENGE_TARGETS = [
    Path("/Applications"),
    Path("/Library/Audio"),
    Path.expanduser(Path("~/Library/Audio")),
    Path.expanduser(Path("~/Library/Application Support"))
]

DEST_DIR = Path.expanduser(Path("~/Universal/Scavenge_Bin"))
SINGULARITY_SCRIPT = "turbo_singularity.py"

# Filters
VALID_EXTS = {'.wav', '.aif', '.aiff', '.mid', '.midi', '.png', '.jpg', '.svg'}
MIN_SIZE = 50 * 1024       # 50KB (Avoid UI beeps)
MAX_SIZE = 100 * 1024 * 1024 * 5 # 500MB (Increased cap)

THREADS = max(4, (os.cpu_count() or 4) * 2)

def scavenge_file(fpath):
    try:
        p = Path(fpath)
        # Permission check
        if not os.access(p, os.R_OK): return (0, "No Access")
        
        stat = p.stat()
        size = stat.st_size
        
        if size < MIN_SIZE: return (0, "Too Small")
        if size > MAX_SIZE: return (0, "Too Big")
        
        # Unique Name to avoid collisions in flat scavenge dir
        # Structure: AppName_Filename
        parts = p.parts
        app_name = "System"
        for part in reversed(parts):
            if part.endswith(".app"):
                app_name = part.replace(".app", "")
                break
                
        safe_name = f"{app_name}_{p.name}"
        # We don't copy to DEST_DIR here, we copy to Staging in run_scavenger
        return (1, safe_name) # Just checking validity here if we were separate
        
    except Exception as e:
        return (-1, str(e))

def run_scavenger():
    cfg.print_header("🏴‍☠️ THE SCAVENGER", "HUNTING FOR ASSETS")
    cfg.system_log(f"Targets: {', '.join([str(t) for t in SCAVENGE_TARGETS])}", "INFO")
    
    # Use a temp staging area so Singularity definitely sees it as external
    STAGING_DIR = Path.expanduser(Path("~/Universal/_Wormhole_Ingest/Scavenged"))
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    candidates = []
    cfg.system_log("Scanning directories...", "INFO")
    
    for target in SCAVENGE_TARGETS:
        if not target.exists(): continue
        try:
            for root, dirs, files in os.walk(target):
                if "Frameworks" in root or "Versions" in root: continue
                # Skip if already in Universe
                if "/Universal/" in root: continue
                
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in VALID_EXTS:
                        candidates.append(Path(root) / f)
        except: pass
        
    cfg.system_log(f"Found {len(candidates)} potential assets. Extracting to Staging...", "INFO")
    
    count = 0
    start_t = time.time()
    
    # Helper to use STAGING_DIR
    def scavenge_to_staging(fpath):
        try:
            p = Path(fpath)
            if not os.access(p, os.R_OK): return (0, "No Access")
            stat = p.stat()
            size = stat.st_size
            if size < MIN_SIZE or size > MAX_SIZE: return (0, "Size")
            
            parts = p.parts
            app_name = "System"
            for part in reversed(parts):
                if part.endswith(".app"):
                    app_name = part.replace(".app", "")
                    break
            
            safe_name = f"{app_name}_{p.name}"
            dest_path = STAGING_DIR / safe_name
            
            if dest_path.exists(): return (0, "Exists")
            shutil.copy2(p, dest_path)
            return (1, dest_path.name)
        except: return (-1, "Error")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(scavenge_to_staging, f): f for f in candidates}
        for i, future in enumerate(as_completed(future_to_file)):
            res, msg = future.result()
            if res == 1: count += 1
            if (i+1) % 500 == 0:
                 print(f"CORE > Scanned {i+1}/{len(candidates)}... (Extracted: {count})", end='\r')

    duration = time.time() - start_t
    cfg.system_log(f"SCAVENGE COMPLETE ({duration:.2f}s)", "SUCCESS")
    cfg.system_log(f"Looted: {count} new assets", "INFO")
    
    if count > 0:
        cfg.system_log("FEEDING LOOT TO SINGULARITY...", "WARN")
        script_dir = Path(__file__).parent
        singularity_path = script_dir / SINGULARITY_SCRIPT
        try:
            # Point Singularity at the Staging Dir
            subprocess.run(["python3", str(singularity_path), str(STAGING_DIR)], check=True)
            # Cleanup Staging
            shutil.rmtree(STAGING_DIR)
            cfg.system_log("Staging Area Cleared.", "SUCCESS")
        except Exception as e:
            cfg.system_log(f"Singularity Failed: {e}", "ERROR")

if __name__ == "__main__":
    run_scavenger()
