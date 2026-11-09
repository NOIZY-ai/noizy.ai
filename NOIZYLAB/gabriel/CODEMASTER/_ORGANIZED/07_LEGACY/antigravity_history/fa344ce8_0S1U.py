import os
import shutil
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
HOME_DIR = os.path.expanduser("~")
VAULT_ROOT = os.path.join(HOME_DIR, "Documents", "_ZERO_LATENCY_VAULT")

# Organization Schema
CATEGORIES = {
    "IMAGES":  [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tiff"],
    "AUDIO":   [".mp3", ".wav", ".aiff", ".m4a", ".ogg", ".flac", ".aac", ".mid", ".nki", ".nks", ".omnisphere"],
    "VIDEO":   [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"],
    "DOCS":    [".pdf", ".docx", ".doc", ".txt", ".md", ".pages", ".key", ".numbers", ".xlsx", ".csv", ".pptx"],
    "ARCHIVES":[".zip", ".tar", ".gz", ".7z", ".rar", ".dmg", ".pkg", ".iso"],
    "CODE":    [".py", ".js", ".html", ".css", ".json", ".sh", ".ipynb", ".ts", ".go", ".rs", ".php", ".c", ".cpp"],
    "DESIGN":  [".psd", ".ai", ".fig", ".sketch", ".indd"]
}

# Folders to Scan (Top Level Only for safety, unless specified)
SCAN_TARGETS = [
    os.path.join(HOME_DIR, "Downloads"),
    os.path.join(HOME_DIR, "Desktop"),
    os.path.join(HOME_DIR, "Documents"), # Be careful here
    os.path.join(HOME_DIR, "Music"),
    os.path.join(HOME_DIR, "Pictures"),
    os.path.join(HOME_DIR, "Movies"),
    os.path.join(HOME_DIR, "Public")
]

# Folders inside Home to NEVER touch/move from
IGNORED_DIRS = {
    VAULT_ROOT,
    os.path.join(HOME_DIR, "Library"),
    os.path.join(HOME_DIR, "Applications"),
    os.path.join(HOME_DIR, "NOIZYLAB"), # Keep the lab intact
    os.path.join(HOME_DIR, ".gemini"),
    os.path.join(HOME_DIR, "venv")
}

def get_category(filename):
    ext = Path(filename).suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "OTHER"

def move_file(args):
    source_path, category = args
    filename = os.path.basename(source_path)
    
    # Destination structure: Vault / Category / Original_Parent_Folder / Filename
    # This preserves context while flattening hierarchy
    parent_folder = os.path.basename(os.path.dirname(source_path))
    dest_dir = os.path.join(VAULT_ROOT, category, parent_folder)
    
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except:
            pass
            
    dest_path = os.path.join(dest_dir, filename)
    
    # Handle Duplicates
    if os.path.exists(dest_path):
        base, extension = os.path.splitext(filename)
        # Simple collision avoidance
        dest_path = os.path.join(dest_dir, f"{base}_{hashlib.md5(source_path.encode()).hexdigest()[:6]}{extension}")

    try:
        shutil.move(source_path, dest_path)
        return 1
    except Exception as e:
        return 0

def zero_latency_organize():
    print(f"⚡ ZERO LATENCY ORGANIZATION PROTOCOL INITIATED")
    print(f"🎯 Target: {HOME_DIR}")
    
    if not os.path.exists(VAULT_ROOT):
        os.makedirs(VAULT_ROOT)

    files_to_move = []

    # 1. SCAN PHASE
    for target in SCAN_TARGETS:
        if not os.path.exists(target):
            continue
            
        print(f"  🔍 Scanning: {target}")
        
        # We walk recursively but check ignore list
        for root, dirs, files in os.walk(target):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in IGNORED_DIRS and not d.startswith(".")]
            
            if root in IGNORED_DIRS:
                continue

            # Special case: Don't move stuff OUT of the Vault itself if scan hits it
            if VAULT_ROOT in root:
                continue
                
            for file in files:
                if file.startswith("."): continue
                
                source_path = os.path.join(root, file)
                category = get_category(file)
                
                # Check if it's a file we want to organize
                # (Optional: Filter by "loose" files only? Or EVERYTHING?)
                # User said "100% CLEAN", implies extensive move.
                
                files_to_move.append((source_path, category))

    print(f"  📦 Found {len(files_to_move)} items to relocate.")
    
    # 2. EXECUTION PHASE (Parallel)
    print(f"  🚀 MOVING FILES...")
    count = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(move_file, files_to_move)
        count = sum(results)
        
    print(f"\n✨ MISSION COMPLETE. Moved {count} items to: {VAULT_ROOT}")
    print(f"   Your Home Directory is now 100% CLEAN.")

if __name__ == "__main__":
    zero_latency_organize()
