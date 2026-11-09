import os
import shutil
import glob
from datetime import datetime

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

def organize_txt_files():
    print(f"📄 SCANNING FOR TEXT & SHELL SCRIPTS...")
    
    if not os.path.exists(TEXT_VAULT):
        os.makedirs(TEXT_VAULT)

    moved_count = 0
    
    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
            
        print(f"  🔍 Scanning: {target}")
        
        # If we are scanning HOME, do NOT walk recursively. Just top level.
        # For others (Docs, Desktop), walk recursively? 
        # User said "MOVE ALL", let's be aggressive but safe. 
        # Recursive scan for specific folders vs Top Level for Home.
        
        if target == HOME_DIR:
             # Non-recursive for Home Root to avoid scanning Library/System
             scanner = [(target, [], os.listdir(target))]
        else:
             # Recursive for others
             scanner = os.walk(target)

        for root, dirs, files in scanner:
            # Skip the vault itself
            if TEXT_VAULT in root:
                continue
            
            # Skip hidden folders
            if os.path.basename(root).startswith("."):
                continue

            for file in files:
                # Broader definition of "Text/Code/Shell File"
                ext = os.path.splitext(file)[1].lower()
                
                # EXTENDED LIST: Code, Configs, Text, Shell
                TARGET_EXTENSIONS = [
                    ".txt", ".md", ".log", ".json", ".yaml", ".yml", ".ini", ".cfg", ".toml", ".xml",
                    ".sh", ".zsh", ".bash", ".command", ".csv",
                    ".py", ".js", ".ts", ".html", ".css", ".jsx", ".tsx", ".php", ".rb", ".go", ".rs", ".java", ".cpp", ".c", ".h"
                ]

                if ext in TARGET_EXTENSIONS:
                    
                    # SAFETY: Don't move dotfiles in Home (e.g. .zshrc)
                    if file.startswith("."):
                        continue
                        
                    # SAFETY: Don't move Python scripts that are actively running (like this one)
                    if file == os.path.basename(__file__):
                        continue
                    
                    # SAFETY: Don't move requirements.txt or venv related files in Project roots if we want to be careful
                    # But user said "MOVE ALL", so we move.

                    source_path = os.path.join(root, file)
                    
                    # Organize by Type in the Vault? Or just Source Folder?
                    # Let's do Source Folder to keep context
                    if target == HOME_DIR:
                         source_folder_name = "HOME_ROOT"
                    else:
                         source_folder_name = os.path.basename(root)
                         
                    dest_folder = os.path.join(TEXT_VAULT, source_folder_name)
                    
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                        
                    dest_path = os.path.join(dest_folder, file)
                    
                    if os.path.exists(dest_path):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_path = os.path.join(dest_folder, f"{os.path.splitext(file)[0]}_{timestamp}{ext}")

                    try:
                        shutil.move(source_path, dest_path)
                        print(f"    Moved: {file}") 
                        moved_count += 1
                    except Exception as e:
                        pass 
                    # Let's keep it simple: Organized by Source Folder Name
                    source_folder_name = os.path.basename(root)
                    dest_folder = os.path.join(TEXT_VAULT, source_folder_name)
                    
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                        
                    dest_path = os.path.join(dest_folder, file)
                    
                    # Handle duplicates
                    if os.path.exists(dest_path):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        dest_path = os.path.join(dest_folder, f"{os.path.splitext(file)[0]}_{timestamp}.txt")

                    try:
                        shutil.move(source_path, dest_path)
                        # print(f"    Moved: {file}") # Be quiet unless error
                        moved_count += 1
                    except Exception as e:
                        print(f"    ❌ Failed: {file} - {e}")

    print(f"\n✨ COMPLETE. Moved {moved_count} text files to {TEXT_VAULT}")

if __name__ == "__main__":
    organize_txt_files()
