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

def build_global_index():
    print("👁️  THE ORACLE IS AWAKENING...")
    start_time = time.time()
    
    volumes_path = Path('/Volumes')
    volumes = [v for v in volumes_path.iterdir() if v.is_dir()]
    
    all_files = []
    
    for vol in volumes:
        if vol.name == 'M2Ultra': continue # Skip boot drive if desired, or keep specific folders
        if vol.name.startswith('com.apple'): continue
        
        print(f"📀 Found Volume: {vol.name}")
        files = scan_volume(str(vol))
        all_files.extend(files)
        print(f"      ↳ Indexed {len(files)} audio files.")

    duration = time.time() - start_time
    
    # Save
    data = {
        "meta": {
            "count": len(all_files),
            "last_scan": str(datetime.now()),
            "scan_duration": f"{duration:.2f}s"
        },
        "files": all_files
    }
    
    save_index(data)
    
    print(f"\n🔮 ORACLE INDEX COMPLETE")
    print(f"   Indexed: {len(all_files):,} sample files")
    print(f"   Time: {duration:.2f} seconds")
    print(f"   Database: {INDEX_PATH}")

if __name__ == "__main__":
    build_global_index()
