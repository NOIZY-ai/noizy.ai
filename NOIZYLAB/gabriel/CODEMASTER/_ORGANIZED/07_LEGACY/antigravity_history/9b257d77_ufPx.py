import os
import shutil
import time
import concurrent.futures
from pathlib import Path

SOURCE_DIR = "/Volumes/4TB Blue Fish"
DEST_DIR = "/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/mined_code/4TB_Blue_Fish"

# EXTENSIONS TO MINE
EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', '.json', 
    '.sh', '.bash', '.zsh', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', 
    '.java', '.kt', '.swift', '.php', '.rb', '.pl', '.md', '.xml', 
    '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.sql'
}

# DIRECTORIES TO IGNORE (HEAVY ASSETS/SAMPLES)
IGNORE_DIRS = {
    'Native Instruments', 'Spectrasonics', 'reFX', 'IK Multimedia', 
    'Samples', 'Audio', 'Music', 'Images', 'Videos', 'STEAM', 'SAGE', 
    'NEXUS library', 'Factory Content', 'Plug-Ins', 'VST', 'Component', 
    'Application Support', 'Cache', 'Caches'
}

def is_ignored(path_part):
    return path_part in IGNORE_DIRS or path_part.startswith('.')

def process_file(file_info):
    src_path, dest_path = file_info
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(src_path, dest_path)
        return 1
    except Exception as e:
        return 0

def hyper_scan():
    print(f"🚀 SYSTEM: HYPER-SPEED ENGAGED.")
    print(f"📂 TARGET: {SOURCE_DIR}")
    print(f"🚫 IGNORING: {len(IGNORE_DIRS)} Heavy Asset Paths")
    
    files_to_copy = []
    
    start_time = time.time()
    scanned_count = 0
    copy_count = 0
    
    # PHASE 1: FAST SCAN
    print("⚡ PHASE 1: SCANNING FILE SYSTEM...")
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        # IN-PLACE Modification of dirs to skip subtrees
        dirs[:] = [d for d in dirs if not is_ignored(d)]
        
        for file in files:
            scanned_count += 1
            if scanned_count % 10000 == 0:
                print(f"   ...scanned {scanned_count} files...")
                
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, SOURCE_DIR)
                dest_path = os.path.join(DEST_DIR, rel_path)
                files_to_copy.append((src_path, dest_path))

    scan_duration = time.time() - start_time
    print(f"⚡ SCAN COMPLETE in {scan_duration:.2f}s. FOUND {len(files_to_copy)} TARGET FILES.")

    # PHASE 2: PARALLEL COPY
    if files_to_copy:
        print(f"⚡ PHASE 2: PARALLEL EXTRACTION ({min(32, os.cpu_count() + 4)} THREADS)...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            futures = [executor.submit(process_file, item) for item in files_to_copy]
            for future in concurrent.futures.as_completed(futures):
                copy_count += future.result()
                if copy_count % 100 == 0:
                    print(f"   ...extracted {copy_count} files...")

    total_duration = time.time() - start_time
    print(f"✅ HYPER MINING FINISHED.")
    print(f"📊 SUMMARY: Scanned {scanned_count} files. Extracted {copy_count} code assets.")
    print(f"⏱ TOTAL TIME: {total_duration:.2f}s")

if __name__ == "__main__":
    hyper_scan()
