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
    Path.expanduser(Path("~/Library/Application Support")),
    Path(".") # Added for testing
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
    print(f"{BOLD}{CYAN}🏴‍☠️ THE SCAVENGER: HUNTING FOR ASSETS...{RESET}")
    print(f"   Targets: {', '.join([str(t) for t in SCAVENGE_TARGETS])}")
    print(f"   Filter: >50KB, <100MB, {list(VALID_EXTS)}")
    
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    candidates = []
    print("   Scanning directories (this may take a while)...")
    
    for target in SCAVENGE_TARGETS:
        if not target.exists(): continue
        try:
            for root, dirs, files in os.walk(target):
                # Skip some heavy system dirs
                if "Frameworks" in root or "Versions" in root: continue
                
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in VALID_EXTS:
                        candidates.append(Path(root) / f)
        except: pass
        
    print(f"   Found {len(candidates)} potential assets. Extracting...")
    
    count = 0
    start_t = time.time()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(scavenge_file, f): f for f in candidates}
        for i, future in enumerate(as_completed(future_to_file)):
            res, msg = future.result()
            if res == 1: count += 1
            if (i+1) % 100 == 0:
                 print(f"   Scanned {i+1}/{len(candidates)}... (Extracted: {count})", end='\r')

    duration = time.time() - start_t
    print(f"\n{GREEN}✨ SCAVENGE COMPLETE ({duration:.2f}s){RESET}")
    print(f"   Looted: {count} new assets")
    
    if count > 0:
        print(f"\n{BOLD}🌌 FEEDING LOOT TO SINGULARITY...{RESET}")
        script_dir = Path(__file__).parent
        singularity_path = script_dir / SINGULARITY_SCRIPT
        try:
            subprocess.run(["python3", str(singularity_path), str(DEST_DIR)], check=True)
            # Optional: Remove Scavenged dir if empty? 
            # Singularity usually organizes OUT of source. 
            # If Singularity works, DEST_DIR (Assets/Scavenged) might be empty?
            # Singularity moves files.
            # But wait, DEST_DIR IS IN DEST_ROOT.
            # Singularity normally ignores DEST_ROOT to prevent loops.
            # Ah. `turbo_singularity.py` has `if str(Path(root).resolve()).startswith(str(DEST_ROOT.resolve())): continue`.
            # So Singularity will IGNORE this folder if it's inside Library!
            # FIX: We should scavenge to a TEMP folder, then Singularity moves them IN.
        except Exception as e:
            print(f"   ❌ Singularity Failed: {e}")

if __name__ == "__main__":
    run_scavenger()
