import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
TARGET_DIRS = [
    "/Users/m2ultra/Downloads",
    "/Users/m2ultra/Desktop"
]

# Destination for organized files (relative to the target dir, or absolute)
# Strategy: Create a "_NOIZY_CLEANUP" folder in each target directory to keep it safe but clean.
CLEANUP_DIR_NAME = "_NOIZY_CLEANUP"

FILE_TYPES = {
    "IMAGES":  [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tiff"],
    "AUDIO":   [".mp3", ".wav", ".aiff", ".m4a", ".ogg", ".flac", ".aac", ".mid"],
    "VIDEO":   [".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"],
    "DOCS":    [".pdf", ".docx", ".doc", ".txt", ".md", ".pages", ".key", ".numbers", ".xlsx", ".csv", ".pptx"],
    "ARCHIVES":[".zip", ".tar", ".gz", ".7z", ".rar"],
    "INSTALL": [".dmg", ".pkg", ".iso"],
    "CODE":    [".py", ".js", ".html", ".css", ".json", ".sh", ".ipynb", ".ts", ".go", ".rs", ".php", ".c", ".cpp"],
    "DESIGN":  [".psd", ".ai", ".fig", ".sketch", ".indd"]
}

def organize_directory(path):
    print(f"🧹 Organizing: {path}")
    if not os.path.exists(path):
        print(f"⚠️ Path not found: {path}")
        return

    # Create the cleanup root in this directory
    cleanup_root = os.path.join(path, CLEANUP_DIR_NAME)
    
    # Files to ignore
    ignored_filenames = [".DS_Store", "desktop.ini", CLEANUP_DIR_NAME, "nuke_folders.py", "organize_folders.py"]

    # Iterate over files in the directory
    # We only take the top-level files to avoid messing up existing folder structures
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        # Skip directories (we only organize loose files)
        if os.path.isdir(item_path):
            continue
            
        if item in ignored_filenames or item.startswith("."):
            continue

        # Determine category
        file_ext = Path(item).suffix.lower()
        category = "OTHER"
        for cat, exts in FILE_TYPES.items():
            if file_ext in exts:
                category = cat
                break
        
        # Move file
        target_folder = os.path.join(cleanup_root, category)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            
        try:
            shutil.move(item_path, os.path.join(target_folder, item))
            print(f"Moved {item} -> {category}")
        except Exception as e:
            print(f"❌ Error moving {item}: {e}")

if __name__ == "__main__":
    print("🚀 NOIZYLAB CLEANUP PROTOCOL STARTED")
    for d in TARGET_DIRS:
        organize_directory(d)
    print("✨ ORGANIZATION COMPLETE")
