import os
import json
import time
from pathlib import Path
from datetime import datetime

# Configuration
INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"
EXTENSIONS = {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.mid', '.midi', '.m4a'}

def load_index():
    try:
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"meta": {"count": 0, "last_scan": None}, "files": []}

def save_index(data):
    with open(INDEX_PATH, 'w') as f:
        json.dump(data, f) # No indent to save space for massive index

def scan_volume(vol_path):
    print(f"   Scanning {vol_path}...")
    results = []
    
    try:
        for root, dirs, files in os.walk(vol_path):
            # Skip hidden folders
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if Path(file).suffix.lower() in EXTENSIONS:
                    full_path = str(Path(root) / file)
                    results.append(full_path)
    except PermissionError:
        pass # Skip locked folders
    
    return results

def build_global_index(target_dir=None):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import sys
    
    print(f"\n{BOLD}{CYAN}CORE > 🔮 ORACLE INDEXER INITIALIZED (PARALLEL MODE){RESET}")
    print(f"CORE > Database: {INDEX_PATH}")

    # Initialize Database
    init_db()
    
    # Discovery Phase
    target_dir = None
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
        print(f"CORE > 🎯 Targeted Scan: {target_dir}")
        volumes = [target_dir]
    else:
        # Scan /Volumes
        volumes_path = Path('/Volumes')
        volumes = [
            v for v in volumes_path.iterdir() 
            if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
        ]
        
    print(f"CORE > Deploying Scanners to {len(volumes)} Volumes...")
    
    start_time = time.time()
    total_indexed = 0
    all_files = []
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_vol = {executor.submit(scan_volume, str(vol)): vol.name for vol in volumes}
        
        for future in as_completed(future_to_vol):
            vol_name = future_to_vol[future]
            try:
                files = future.result()
                all_files.extend(files)
                print(f"CORE > ✅ {vol_name}: Indexed {len(files)} files")
            except Exception as e:
                print(f"CORE > ❌ {vol_name}: Failed ({e})")

    # Batch Insert (Hyper-Speed)
    if all_files:
        print(f"CORE > Registering {len(all_files)} artifacts to Oracle...")
        # Chunking for SQLite safety
        CHUNK_SIZE = 900
        for i in range(0, len(all_files), CHUNK_SIZE):
            chunk = all_files[i:i + CHUNK_SIZE]
            verify_and_store(chunk)
            
    duration = time.time() - start_time
    print(f"\n{GREEN}CORE > ✨ ORACLE INDEX COMPLETE{RESET}")
    print(f"CORE > Indexed: {len(all_files):,} sample files")
    print(f"CORE > Time: {duration:.2f} seconds")
    print(f"CORE > Database: {INDEX_PATH}")

if __name__ == "__main__":
    import sys
        build_global_index(target)
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan Interrupted. Saving progress (if implemented)...")

        # We need to save whatever 'all_files' we have. 
        # But 'all_files' is local to the function. 
        # Quick fix: Just let it run fast or accept partial re-run.
        # Actually, let's just make it robust.

