import os
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
HOME_DIR = os.path.expanduser("~")
TARGET_DIRS = [
    HOME_DIR,  # Scan the root home directory for loose scripts/text too
    os.path.join(HOME_DIR, "Documents"),
    os.path.join(HOME_DIR, "Downloads"),
    os.path.join(HOME_DIR, "Desktop"),
    os.path.join(HOME_DIR, "NOIZYLAB")
]

# Destination for organized text files
TEXT_VAULT = os.path.join(HOME_DIR, "Documents", "NOIZYLAB_TEXT_VAULT")

def move_worker(args):
    source_path, dest_dir, filename = args
    
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except Exception as e:
            return 0

    base, ext = os.path.splitext(filename)
    dest_path = os.path.join(dest_dir, filename)
    
    # Handle collision
    if os.path.exists(dest_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_path = os.path.join(dest_dir, f"{base}_{timestamp}{ext}")

    try:
        shutil.move(source_path, dest_path)
        return 1
    except Exception:
        return 0

def organize_txt_files():
    print(f"⚡ TURBO-CHARGED TEXT ORGANIZATION INITIATED...")
    
    if not os.path.exists(TEXT_VAULT):
        os.makedirs(TEXT_VAULT)

    move_tasks = []
    
    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
            
        print(f"  🔍 Scanning: {target}")
        
        if target == HOME_DIR:
             scanner = [(target, [], os.listdir(target))]
        else:
             scanner = os.walk(target)

        for root, dirs, files in scanner:
            # Skip the vault itself
            if TEXT_VAULT in root:
                continue
            
            # Skip hidden folders
            if os.path.basename(root).startswith("."):
                continue

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                
                TARGET_EXTENSIONS = [
                    ".txt", ".md", ".log", ".json", ".yaml", ".yml", ".ini", ".cfg", ".toml", ".xml",
                    ".sh", ".zsh", ".bash", ".command", ".csv",
                    ".py", ".js", ".ts", ".html", ".css", ".jsx", ".tsx", ".php", ".rb", ".go", ".rs", ".java", ".cpp", ".c", ".h"
                ]

                if ext in TARGET_EXTENSIONS:
                    if file.startswith("."): continue
                    if file == os.path.basename(__file__): continue
                    
                    source_path = os.path.join(root, file)
                    
                    if target == HOME_DIR:
                         target_name = "HOME_ROOT"
                    else:
                         target_name = os.path.basename(target)

                    rel_path = os.path.relpath(root, start=target)
                    if rel_path == ".": rel_path = ""
                    
                    dest_folder = os.path.join(TEXT_VAULT, target_name, rel_path)
                    
                    move_tasks.append((source_path, dest_folder, file))

    print(f"  📦 Found {len(move_tasks)} items to relocate.")
    print(f"  🚀 EXECUTING CONCURRENT MOVES...")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(move_worker, move_tasks)
        moved_count = sum(results)

    print(f"\n✨ COMPLETE. Moved {moved_count} text files to {TEXT_VAULT}")

if __name__ == "__main__":
    organize_txt_files()
