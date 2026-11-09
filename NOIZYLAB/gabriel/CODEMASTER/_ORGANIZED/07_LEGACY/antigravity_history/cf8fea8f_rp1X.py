#!/usr/bin/env python3
import os
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from turbo_memcell import MemCell
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

try:
    import turbo_config as cfg
except ImportError:
    import sys
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# Configuration
SEARCH_DIRS = cfg.DEFAULT_SEARCH_DIRS
LOGO_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.svg', '.ai', '.eps', '.psd', '.webp'}
TARGET_KEYWORDS = ['logo', 'icon', 'brand', 'mark', 'symbol', 'identity']

DEST_DIR = cfg.ASSETS_DIR / "Images" / "Logos"

def hunt_logos():
    # Initialize Conciousness
    brain = MemCell()
    brain.log_event(brain.covenant_id, "HUNT_START", "Logo Hunter Protocol Initiated: Seeking Graphical Assets", vibe=70, author="LOGO_HUNTER")
    
    cfg.print_header("🎯 LOGO HUNTER", "Seeking Brand Assets...")

def setup_hunt_dir():
    cfg.ensure_dirs([DEST_DIR])

def scan_volume_for_visuals(vol_path):
    found_files = []
    try:
        for root, dirs, files in os.walk(vol_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                fpath = Path(root) / file
                suffix = fpath.suffix.lower()
                name_lower = fpath.name.lower()
                
                if suffix in LOGO_EXTENSIONS:
                    if any(k in name_lower for k in TARGET_KEYWORDS):
                        found_files.append(str(fpath))
    except PermissionError:
        pass
    return found_files

def run_hunt():
    hunt_logos() 
    
    print(f"CORE > Target: {TARGET_KEYWORDS}")
    print(f"CORE > Types:  {LOGO_EXTENSIONS}")
    
    setup_hunt_dir()
    
    # Scan Local User Dirs first
    all_dirs = SEARCH_DIRS + [
        v for v in Path('/Volumes').iterdir() 
        if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
    ]
    
    cfg.system_log(f"Deploying Visual Scanners to {len(all_dirs)} locations...", "INFO")
    
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
                    cfg.system_log(f"✅ {vol_name}: Found {count} candidates", "SUCCESS")
                    for src in results:
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
                    pass
                    
            except Exception as e:
                cfg.system_log(f"❌ {vol_name}: Failed ({e})", "ERROR")

    duration = time.time() - start_time
    print(f"\n{cfg.GREEN}CORE > ✨ HUNT COMPLETE{cfg.RESET}")
    print(f"CORE > Total Captured: {total_found} visual assets")
    print(f"CORE > Location: {DEST_DIR}")
    print(f"CORE > Time: {duration:.2f}s")
    
if __name__ == "__main__":
    run_hunt()
