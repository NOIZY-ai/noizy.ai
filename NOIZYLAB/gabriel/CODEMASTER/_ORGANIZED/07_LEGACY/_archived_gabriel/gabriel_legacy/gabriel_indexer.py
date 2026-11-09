import os
import json
import time
from concurrent.futures import ThreadPoolExecutor

ROOT_DIR = "/Users/m2ultra/NOIZYLAB"
OUTPUT_FILE = "/Users/m2ultra/NOIZYLAB/GABRIEL/gabriel_index.json"
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.env', '.vscode', 'dist', 'build'}
IGNORE_EXTS = {'.pyc', '.DS_Store', '.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov', '.mp3', '.wav', '.zip', '.tar.gz', '.pkl', '.bin', '.exe', '.dll', '.so', '.dylib'}

def get_file_info(filepath):
    try:
        stat = os.stat(filepath)
        return {
            "path": filepath,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "name": os.path.basename(filepath),
            "ext": os.path.splitext(filepath)[1]
        }
    except Exception:
        return None

def scan_directory(root_path):
    print(f"Scanning {root_path}...")
    file_list = []
    
    for root, dirs, files in os.walk(root_path):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in IGNORE_EXTS):
                continue
                
            filepath = os.path.join(root, file)
            info = get_file_info(filepath)
            if info:
                file_list.append(info)
                
    return file_list

def main():
    start_time = time.time()
    print("🚀 GABRIEL FAST INDEXER INITIALIZED")
    
    # Scan in parallel if we had multiple roots, but for now just one fast scan
    all_files = scan_directory(ROOT_DIR)
    
    index_data = {
        "timestamp": time.time(),
        "total_files": len(all_files),
        "root": ROOT_DIR,
        "files": all_files
    }
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(index_data, f, indent=2)
        
    duration = time.time() - start_time
    print(f"✅ Indexing complete in {duration:.2f}s")
    print(f"📂 Indexed {len(all_files)} files")
    print(f"💾 Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
