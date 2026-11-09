import os
import shutil
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
HUNT_DIR = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Visual_Hunt")
EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif', '.psd', '.ai', '.eps', '.svg', '.pdf', '.indir', '.indd', '.heic', '.bmp', '.gif'}
KEYWORDS = ['fish', 'noizy', 'logo', 'brand', 'cover', 'art']

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def setup_hunt_dir():
    if not HUNT_DIR.exists():
        HUNT_DIR.mkdir(parents=True)
    # Optional: Clear previous hunt? Maybe not, user said "COLLECT ALL".
    # Let's keep it additive but avoid dupes.

def scan_volume_for_visuals(vol_path):
    found_files = []
    try:
        for root, dirs, files in os.walk(vol_path):
            # Optimization: Skip massive folders that are unlikely to hold logos? 
            # Actually user said "EVERYWHERE SUPER DEEP". We scan all.
            # Just skip hidden.
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                fpath = Path(root) / file
                suffix = fpath.suffix.lower()
                name_lower = fpath.name.lower()
                
                if suffix in EXTENSIONS:
                    # Check keywords
                    if any(k in name_lower for k in KEYWORDS):
                        found_files.append(str(fpath))
    except PermissionError:
        pass
    return found_files

def run_hunt():
    print(f"{BOLD}{CYAN}CORE > 🦅 VISUAL HUNTER INITIALIZED{RESET}")
    print(f"CORE > Target: {KEYWORDS}")
    print(f"CORE > Types:  {EXTENSIONS}")
    
    setup_hunt_dir()
    
    volumes_path = Path('/Volumes')
    volumes = [
        v for v in volumes_path.iterdir() 
        if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
    ]
    
    print(f"CORE > Deploying Visual Scanners to {len(volumes)} Volumes...")
    
    start_time = time.time()
    total_found = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_vol = {executor.submit(scan_volume_for_visuals, str(vol)): vol.name for vol in volumes}
        
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
                        # Create Symlink in Hunt Dir
                        # flatten name: VolName_FileName
                        sanitized_vol = vol_name.replace(" ", "_")
                        fname = Path(src).name
                        link_name = f"{sanitized_vol}___{fname}"
                        dest = HUNT_DIR / link_name
                        
                        try:
                            if not dest.exists():
                                os.symlink(src, dest)
                        except FileExistsError:
                            pass
                        except Exception as e:
                            # print(f"      ⚠️ Failed to link {fname}: {e}")
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
