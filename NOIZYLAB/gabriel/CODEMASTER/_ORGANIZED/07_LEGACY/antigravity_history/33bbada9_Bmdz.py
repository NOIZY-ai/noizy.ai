import os
import sys
import re
import subprocess
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Reuse patterns from turbo_indexer (Simplified)
PATTERNS = {
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), 
}

THREADS = max(4, (os.cpu_count() or 4) * 2)

def get_smart_metadata(filename):
    f_lower = filename.lower()
    bpm = None
    key = None
    
    # BPM
    bpm_match = PATTERNS["bpm"].search(f_lower)
    if bpm_match:
        try: bpm = int(bpm_match.group(1))
        except: pass
        
    # Key
    key_match = PATTERNS["key"].search(filename) # Case sensitive for Key often
    if key_match:
        key = key_match.group(1)
        
    return bpm, key

def set_xattr(file_path, key, value):
    try:
        # xattr -w <key> <value> <file>
        # User <value> must be string
        subprocess.run(["xattr", "-w", key, str(value), str(file_path)], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def process_file(fpath):
    try:
        bpm, key = get_smart_metadata(fpath.name)
        injected = False
        
        # AUTHORS
        if set_xattr(fpath, "com.apple.metadata:kMDItemAuthors", "Audio Unitor AI"):
            injected = True
            
        # BPM
        if bpm:
            if set_xattr(fpath, "com.apple.metadata:kMDItemTempo", bpm):
                injected = True
        
        # KEY
        if key:
            if set_xattr(fpath, "com.apple.metadata:kMDItemKeySignature", key):
                injected = True
                
        if injected:
            return (1, fpath.name)
        return (0, None)
        
    except Exception:
        return (-1, fpath.name)

def run_librarian(target_dir):
    print(f"{BOLD}{CYAN}CORE > 📚 TURBO LIBRARIAN: HYPER-SPEED METADATA INJECTOR{RESET}")
    print(f"CORE > Target: {target_dir}")
    print(f"CORE > Method: MacOS Extended Attributes (Parallelized)")
    
    root_path = Path(target_dir)
    if not root_path.exists():
        print(f"CORE > {RED}❌ Target not found.{RESET}")
        return

    files_to_process = []
    print("CORE > Scanning universe...")
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.startswith('.'): continue
            files_to_process.append(Path(root) / f)
            
    print(f"CORE > Found {len(files_to_process)} candidates. Engaging Juggernaut Drive...")
    
    start_time = time.time()
    processed = 0
    injected_count = 0
    errors = 0
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(process_file, f): f for f in files_to_process}
        
        for i, future in enumerate(as_completed(future_to_file)):
            status, name = future.result()
            processed += 1
            if status == 1:
                injected_count += 1
            elif status == -1:
                errors += 1
                
            if processed % 100 == 0:
                print(f"CORE > ...injected {processed}/{len(files_to_process)}...", end='\r')

    duration = time.time() - start_time
    rate = processed / duration if duration > 0 else 0
    
    print(f"\n{GREEN}CORE > ✨ LIBRARY CATALOGED IN {duration:.2f}s{RESET}")
    print(f"CORE > Rate:     {rate:.1f} files/sec")
    print(f"CORE > Scanned:  {processed}")
    print(f"CORE > Injected: {injected_count}")
    print(f"CORE > Errors:   {errors}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_librarian.py <target_dir>")
    else:
        run_librarian(sys.argv[1])
