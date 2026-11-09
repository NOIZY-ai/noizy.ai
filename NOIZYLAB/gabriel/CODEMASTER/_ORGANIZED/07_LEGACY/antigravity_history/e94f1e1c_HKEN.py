import os
import shutil
import time
import subprocess
import concurrent.futures
from pathlib import Path

SOURCE_DIR = "/Volumes/4TB Blue Fish"
DEST_DIR = "/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/mined_code/4TB_Blue_Fish"

# RAW FIND COMMAND for maximum speed (macOS optimized)
FIND_CMD = [
    "find", SOURCE_DIR, 
    "-type", "f",
    "(",
    "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.ts", "-o", "-name", "*.tsx", "-o", "-name", "*.jsx",
    "-o", "-name", "*.html", "-o", "-name", "*.css", "-o", "-name", "*.scss", "-o", "-name", "*.json",
    "-o", "-name", "*.sh", "-o", "-name", "*.bash", "-o", "-name", "*.zsh",
    "-o", "-name", "*.c", "-o", "-name", "*.cpp", "-o", "-name", "*.h", "-o", "-name", "*.hpp",
    "-o", "-name", "*.go", "-o", "-name", "*.rs", "-o", "-name", "*.java", "-o", "-name", "*.kt",
    "-o", "-name", "*.swift", "-o", "-name", "*.php", "-o", "-name", "*.rb", "-o", "-name", "*.pl",
    "-o", "-name", "*.md", "-o", "-name", "*.xml", "-o", "-name", "*.yaml", "-o", "-name", "*.yml",
    "-o", "-name", "*.toml", "-o", "-name", "*.ini", "-o", "-name", "*.conf", "-o", "-name", "*.cfg", "-o", "-name", "*.sql",
    ")"
]

def process_file(src_path):
    try:
        # Calculate relative path
        rel_path = os.path.relpath(src_path, SOURCE_DIR)
        dest_path = os.path.join(DEST_DIR, rel_path)
        
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
        return 1
    except Exception:
        return 0

def hyper_scan():
    print(f"🚀 SYSTEM: HYPER-SPEED ENGAGED (v2).")
    print(f"📂 TARGET: {SOURCE_DIR}")
    
    start_time = time.time()
    
    # PHASE 1: NATIVE FIND SCAN
    print("⚡ PHASE 1: NATIVE FILE SYSTEM SCAN...")
    try:
        result = subprocess.run(FIND_CMD, stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)
        files = result.stdout.strip().split('\n')
        files = [f for f in files if f] # Filter empty
    except Exception as e:
        print(f"❌ SCAN ERROR: {e}")
        return

    scan_duration = time.time() - start_time
    print(f"⚡ SCAN COMPLETE in {scan_duration:.2f}s. FOUND {len(files)} TARGET FILES.")

    # PHASE 2: PARALLEL COPY
    copy_count = 0
    if files:
        print(f"⚡ PHASE 2: PARALLEL EXTRACTION ({min(50, os.cpu_count() + 10)} THREADS)...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_file, f) for f in files]
            
            # Monitoring loop
            completed = 0
            total = len(files)
            
            for future in concurrent.futures.as_completed(futures):
                completed += 1
                copy_count += future.result()
                if completed % 100 == 0:
                    print(f"   ...progress: {completed}/{total} files...")

    total_duration = time.time() - start_time
    print(f"✅ HYPER MINING FINISHED.")
    print(f"📊 SUMMARY: Extracted {copy_count} code assets.")
    print(f"⏱ TOTAL TIME: {total_duration:.2f}s")

if __name__ == "__main__":
    hyper_scan()
