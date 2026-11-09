import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
HOME_DIR = os.path.expanduser("~")
CLEANUP_DIR = os.path.join(HOME_DIR, "Documents", "_HOME_ROOT_CLEANUP")

# Folders to NEVER touch in the User's Home Directory
IGNORED_SYSTEM_FOLDERS = {
    "Applications", "Desktop", "Documents", "Downloads", 
    "Library", "Movies", "Music", "Pictures", "Public", "Sites", 
    "NOIZYLAB", ".Trash", ".gemini", "venv", "__pycache__"
}

FILE_TYPES = {
    "IMAGES":  [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tiff"],
    "AUDIO":   [".mp3", ".wav", ".aiff", ".m4a", ".ogg", ".flac", ".aac", ".mid"],
    "VIDEO":   [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"],
    "DOCS":    [".pdf", ".docx", ".doc", ".txt", ".md", ".pages", ".key", ".numbers", ".xlsx", ".csv", ".pptx"],
    "ARCHIVES":[".zip", ".tar", ".gz", ".7z", ".rar", ".dmg", ".pkg", ".iso"],
    "CODE":    [".py", ".js", ".html", ".css", ".json", ".sh", ".ipynb", ".ts", ".go", ".rs", ".php", ".c", ".cpp"],
    "DESIGN":  [".psd", ".ai", ".fig", ".sketch", ".indd"]
}

def clean_home_root():
    print(f"🧹 Scanning User Home Root: {HOME_DIR}")
    
    if not os.path.exists(CLEANUP_DIR):
        os.makedirs(CLEANUP_DIR)
        print(f"Created Cleanup Vault: {CLEANUP_DIR}")

    moved_count = 0

    # Scan only the top level of the home directory
    # We DO NOT walk recursively into subfolders of Home (that would be disastrous)
    for item in os.listdir(HOME_DIR):
        item_path = os.path.join(HOME_DIR, item)
        
        # SKIP if it's one of the system folders or hidden files
        if item in IGNORED_SYSTEM_FOLDERS or item.startswith("."):
            continue
            
        # If it's a directory that is NOT in the ignore list, we might want to move it too if it looks like clutter
        # But for safety, let's stick to FILES only for now, unless it's clearly a temp folder.
        # User said "ORGANIZE & MOVE", so let's move loose files first.
        
        if os.path.isfile(item_path):
            # Determine category
            file_ext = Path(item).suffix.lower()
            category = "OTHER_FILES"
            for cat, exts in FILE_TYPES.items():
                if file_ext in exts:
                    category = cat
                    break
            
            target_folder = os.path.join(CLEANUP_DIR, category)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                
            try:
                shutil.move(item_path, os.path.join(target_folder, item))
                print(f"  Moved: {item} -> {category}")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Error moving {item}: {e}")

    print(f"\n✨ HOME ROOT CLEANUP COMPLETE. Moved {moved_count} items to {CLEANUP_DIR}")

if __name__ == "__main__":
    clean_home_root()
