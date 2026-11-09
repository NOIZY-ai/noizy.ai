import os
import shutil
import time
import subprocess
import concurrent.futures
import sys
from pathlib import Path

# Get source from Args or default
if len(sys.argv) > 1:
    SOURCE_DIR = sys.argv[1]
else:
    SOURCE_DIR = "/Volumes/4TB Blue Fish"

# Sanitize volume name for destination
vol_name = os.path.basename(SOURCE_DIR.rstrip('/'))
DEST_DIR = f"/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/mined_code/{vol_name}"

# RAW FIND COMMAND for maximum speed
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
        rel_path = os.path.relpath(src_path, SOURCE_DIR)
        dest_path = os.path.join(DEST_DIR, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
        return 1
    except Exception:
        return 0

def hyper_scan():
    print(f"🚀 MINING: {vol_name}")
    start_time = time.time()
    
    # PHASE 1: NATIVE FIND SCAN
    try:
        result = subprocess.run(FIND_CMD, stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)
        files = result.stdout.strip().split('\n')
        files = [f for f in files if f]
    except Exception as e:
        print(f"❌ ERROR {vol_name}: {e}")
        return

    scan_duration = time.time() - start_time
    print(f"⚡ {vol_name} SCANNED: {len(files)} files in {scan_duration:.2f}s")

    # PHASE 2: PARALLEL COPY
    copy_count = 0
    if files:
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(process_file, f) for f in files]
            for future in concurrent.futures.as_completed(futures):
                copy_count += future.result()

    total_duration = time.time() - start_time
    print(f"✅ {vol_name} COMPLETE. Extracted {copy_count} assets in {total_duration:.2f}s")

if __name__ == "__main__":
    hyper_scan()
