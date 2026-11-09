import os
import sys
import re
import shutil
import subprocess
from pathlib import Path

# Configuration
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

MIME_MAP = {
    'audio/wav': '.wav', 'audio/x-wav': '.wav', 'audio/mpeg': '.mp3', 'audio/x-aiff': '.aif',
    'image/jpeg': '.jpg', 'image/png': '.png', 'application/pdf': '.pdf', 'text/plain': '.txt',
    'video/mp4': '.mp4', 'video/quicktime': '.mov', 'application/zip': '.zip',
    'application/x-gzip': '.gz', 'application/json': '.json'
}

def detect_extension(file_path):
    try:
        result = subprocess.run(['file', '--mime-type', '-b', str(file_path)], capture_output=True, text=True)
        mime = result.stdout.strip()
        return MIME_MAP.get(mime, "")
    except: return ""

def clean_filename(name):
    # Remove extension for processing
    stem = Path(name).stem
    ext = Path(name).suffix
    
    # Replace non-alphanumeric with underscore
    clean = re.sub(r'[^a-zA-Z0-9]', '_', stem)
    # Collapse multiple underscores
    clean = re.sub(r'_+', '_', clean)
    # Strip leading/trailing underscores
    clean = clean.strip('_')
    # Lowercase (Optional, maybe keep Case for readability? User likes "Cyberpunk" so maybe Caps is okay? 
    # Let's go snake_case as planned for "Detox")
    clean = clean.lower()
    
    return f"{clean}{ext}"

def run_sanitizer(target_dir):
    print(f"{BOLD}{CYAN}CORE > ☢️  TURBO SANITIZER INITIALIZED{RESET}")
    print(f"CORE > Target: {target_dir}")
    
    root_path = Path(target_dir)
    if not root_path.exists():
        print("CORE > ❌ Target not found.")
        return
    
    files_processed = 0
    files_fixed = 0
    files_renamed = 0
    
    # Collect all files first to avoid iterator issues while renaming
    all_files = []
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if not f.startswith('.'):
                all_files.append(Path(root) / f)
                
    print(f"CORE > Scanning {len(all_files)} files...")
    
    for fpath in all_files:
        if not fpath.exists(): continue 
        
        original_name = fpath.name
        parent = fpath.parent
        new_name = original_name
        renamed = False
        
        # 1. MAGIC EYE (Fix Extension)
        if not fpath.suffix or fpath.suffix == ".":
            detected_ext = detect_extension(fpath)
            if detected_ext:
                print(f"CORE > 👁️  Magic Eye: {original_name} -> {detected_ext}")
                new_name = f"{fpath.stem}{detected_ext}"
                renamed = True
                files_fixed += 1
                
        # 2. FILENAME DETOX (Snake Case)
        # Apply cleaning to the current 'new_name'
        cleaned = clean_filename(new_name)
        if cleaned != new_name:
            # print(f"   🧼 Detox: {new_name} -> {cleaned}")
            new_name = cleaned
            renamed = True
            
        # Execute Rename if needed
        if renamed and new_name != original_name:
            dest_path = parent / new_name
            if dest_path.exists():
                # Collision handling
                ts = int(os.path.getmtime(fpath))
                dest_path = parent / f"{Path(new_name).stem}_{ts}{Path(new_name).suffix}"
            
            try:
                fpath.rename(dest_path)
                print(f"CORE > ✅ Fixed: {original_name} -> {GREEN}{dest_path.name}{RESET}")
                files_renamed += 1
            except Exception as e:
                print(f"CORE > ❌ Failed to rename {fpath}: {e}")
                
        files_processed += 1
        
    print(f"\n{GREEN}CORE > ✨ SANITIZATION COMPLETE{RESET}")
    print(f"CORE > Scanned: {files_processed}")
    print(f"CORE > Fixed Exts: {files_fixed}")
    print(f"CORE > Renamed:    {files_renamed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_sanitizer.py <target_dir>")
    else:
        run_sanitizer(sys.argv[1])
