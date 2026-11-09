import os
import shutil
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

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
MAX_SIZE = 100 * 1024 * 1024 # 100MB (Avoid huge scores)

THREADS = max(4, (os.cpu_count() or 4) * 2)

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

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
        # Try to find which App it belongs to
        parts = p.parts
        app_name = "System"
        for part in reversed(parts):
            if part.endswith(".app"):
                app_name = part.replace(".app", "")
                break
                
        safe_name = f"{app_name}_{p.name}"
        dest_path = DEST_DIR / safe_name
        
        if dest_path.exists():
            return (0, "Exists")
            
        shutil.copy2(p, dest_path)
        return (1, dest_path.name)
        
    except Exception as e:
        return (-1, str(e))

def run_scavenger():
    print(f"{BOLD}{CYAN}CORE > 🏴‍☠️ THE SCAVENGER: HUNTING FOR ASSETS...{RESET}")
    print(f"CORE > Targets: {', '.join([str(t) for t in SCAVENGE_TARGETS])}")
    
    # Use a temp staging area so Singularity definitely sees it as external
    STAGING_DIR = Path.expanduser(Path("~/Universal/_Wormhole_Ingest/Scavenged"))
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    candidates = []
    print("CORE > Scanning directories...")
    
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
        
    print(f"CORE > Found {len(candidates)} potential assets. Extracting to Staging...")
    
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
    print(f"\n{GREEN}CORE > ✨ SCAVENGE COMPLETE ({duration:.2f}s){RESET}")
    print(f"CORE > Looted: {count} new assets")
    
    if count > 0:
        print(f"\n{BOLD}CORE > 🌌 FEEDING LOOT TO SINGULARITY...{RESET}")
        script_dir = Path(__file__).parent
        singularity_path = script_dir / SINGULARITY_SCRIPT
        try:
            # Point Singularity at the Staging Dir
            subprocess.run(["python3", str(singularity_path), str(STAGING_DIR)], check=True)
            # Cleanup Staging
            shutil.rmtree(STAGING_DIR)
            print(f"CORE > 🧹 Staging Area Cleared.")
        except Exception as e:
            print(f"CORE > ❌ Singularity Failed: {e}")

if __name__ == "__main__":
    run_scavenger()
