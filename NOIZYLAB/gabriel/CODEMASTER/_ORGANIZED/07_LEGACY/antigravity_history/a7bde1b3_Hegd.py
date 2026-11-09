import os
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    import sys
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
SEARCH_DIRS = [
    Path.expanduser(Path("~/Downloads")),
    Path.expanduser(Path("~/Desktop")),
    Path.expanduser(Path("~/Documents"))
]

LOGO_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.svg', '.ai', '.eps', '.psd', '.webp'}
TARGET_KEYWORDS = ['logo', 'icon', 'brand', 'mark', 'symbol', 'identity']

DEST_DIR = Path.expanduser(Path("~/Universal/Library/Assets/Images/Logos"))

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


def hunt_logos():
    # Initialize Conciousness
    brain = MemCell()
    brain.log_event(brain.covenant_id, "HUNT_START", "Logo Hunter Protocol Initiated: Seeking Graphical Assets", vibe=70, author="LOGO_HUNTER")
    
    print(f"{BOLD}{CYAN}CORE > 🎯 LOGO HUNTER INITIATED (Seeking Brand Assets...){RESET}")

def setup_hunt_dir():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    # Optional: Clear previous hunt? Maybe not, user said "COLLECT ALL".
    # Let's keep it additive but avoid dupes.

def scan_volume_for_visuals(vol_path):
    found_files = []
    try:
        for root, dirs, files in os.walk(vol_path):
            # Optimization: Skip hidden
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                fpath = Path(root) / file
                suffix = fpath.suffix.lower()
                name_lower = fpath.name.lower()
                
                if suffix in LOGO_EXTENSIONS:
                    # Check keywords
                    if any(k in name_lower for k in TARGET_KEYWORDS):
                        found_files.append(str(fpath))
    except PermissionError:
        pass
    return found_files

def run_hunt():
    hunt_logos() # Call the MemCell integration function
    
    print(f"CORE > Target: {TARGET_KEYWORDS}")
    print(f"CORE > Types:  {LOGO_EXTENSIONS}")
    
    setup_hunt_dir()
    
    # Scan Local User Dirs first
    all_dirs = SEARCH_DIRS + [
        v for v in Path('/Volumes').iterdir() 
        if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
    ]
    
    print(f"CORE > Deploying Visual Scanners to {len(all_dirs)} locations...")
    
    start_time = time.time()
    total_found = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_vol = {executor.submit(scan_volume_for_visuals, str(d)): d.name for d in all_dirs}
        
        for future in as_completed(future_to_vol):
            vol_name = future_to_vol[future]
            try:
                results = future.result()
                count = len(results)
                total_found += count
                
                if count > 0:
                    print(f"CORE > ✅ {vol_name}: Found {count} candidates")
                    # Process results immediately to save memory
                    for src in results:
                        # Create Symlink or Copy
                        # flatten name: VolName_FileName
                        sanitized_vol = vol_name.replace(" ", "_")
                        fname = Path(src).name
                        link_name = f"{sanitized_vol}___{fname}"
                        dest = DEST_DIR / link_name
                        
                        try:
                            if not dest.exists():
                                os.symlink(src, dest)
                        except Exception as e:
                            pass


                else:
                    # print(f"   ⚪ {vol_name}: No matches")
                    pass
                    
            except Exception as e:
                print(f"CORE > ❌ {vol_name}: Failed ({e})")

    duration = time.time() - start_time
    print(f"\n{GREEN}CORE > ✨ HUNT COMPLETE{RESET}")
    print(f"CORE > Total Captured: {total_found} visual assets")
    print(f"CORE > Location: {HUNT_DIR}")
    print(f"CORE > Time: {duration:.2f}s")
    
    # Generate an HTML gallery? user didn't ask but would be cool.
    # For now, just the folder.

if __name__ == "__main__":
    run_hunt()
