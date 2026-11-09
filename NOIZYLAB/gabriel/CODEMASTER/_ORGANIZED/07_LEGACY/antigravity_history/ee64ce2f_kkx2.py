#!/usr/bin/env python3
"""
🧹 NOIZYLAB CLEANER & ASSET SORTER
Aggressively collects code, moves assets, and deletes empty folders.
Ensures PROJECTS_MASTER is the only source of truth.
"""

import os
import shutil
from pathlib import Path

# Config
ROOT_DIR = Path("..").resolve() # NOIZYLAB Root
MASTER_DIR = ROOT_DIR / "PROJECTS_MASTER"
INBOX_DIR = MASTER_DIR / "INBOX"
ASSETS_DIR = MASTER_DIR / "ASSETS"

SORTING_RULES = {
    'IMAGES': {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.bmp', '.tiff', '.psd', '.ai'},
    'AUDIO': {'.wav', '.mp3', '.aif', '.aiff', '.flac', '.ogg', '.m4a'},
    'CODE': {'.py', '.js', '.ts', '.html', '.css', '.c', '.cpp', '.h', '.java', '.cs', '.sh', '.md', '.json', '.xml', '.yml', '.yaml'},
    'DOCS': {'.pdf', '.doc', '.docx', '.txt', '.rtf'},
    'ARCHIVES': {'.zip', '.tar', '.gz', '.rar', '.7z'}
}

IGNORED_DIRS = {
    'PROJECTS_MASTER', 
    '.git', 
    '.DS_Store', 
    '__pycache__',
    'node_modules'
}

class NoizyCleaner:
    def __init__(self):
        self.moved_count = 0
        self.deleted_dirs = 0
        
        # Ensure destinations exist
        for subdir in SORTING_RULES.keys():
            (ASSETS_DIR / subdir).mkdir(parents=True, exist_ok=True)
        (INBOX_DIR / "MISC").mkdir(parents=True, exist_ok=True)

    def sort_file(self, file_path):
        """Move file to appropriate folder in PROJECTS_MASTER."""
        # Skip files already in MASTER_DIR
        if MASTER_DIR in file_path.parents:
            return

        ext = file_path.suffix.lower()
        dest_category = "MISC"
        is_asset = False

        for category, extensions in SORTING_RULES.items():
            if ext in extensions:
                dest_category = category
                # distinct logic: Code/Docs go to INBOX usually unless part of a project, 
                # but "Images/Audio" are Assets.
                if category in ['IMAGES', 'AUDIO']:
                    is_asset = True
                break
        
        if is_asset:
            target_folder = ASSETS_DIR / dest_category
        else:
            # Code/Docs from root that aren't in a project go to INBOX
            target_folder = INBOX_DIR / dest_category

        target_path = target_folder / file_path.name
        
        # Handle duplicates
        counter = 1
        while target_path.exists():
            target_path = target_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        try:
            print(f"  📦 Moving {file_path.name} -> {target_folder.name}/")
            shutil.move(str(file_path), str(target_path))
            self.moved_count += 1
        except Exception as e:
            print(f"  ❌ Error moving {file_path}: {e}")

    def clean_empty_dirs(self, directory):
        """Recursively delete empty directories."""
        # Don't delete MASTER_DIR
        if directory == MASTER_DIR:
            return

        # Walk bottom-up
        for root, dirs, files in os.walk(directory, topdown=False):
            current_path = Path(root)
            
            # Skip if inside MASTER_DIR
            if MASTER_DIR in current_path.parents or current_path == MASTER_DIR:
                continue
                
            try:
                # Refresh status
                if not any(current_path.iterdir()):
                    print(f"  🗑️  Deleting empty: {current_path.relative_to(ROOT_DIR)}")
                    current_path.rmdir()
                    self.deleted_dirs += 1
            except Exception as e:
                pass # Directory likely not empty or permission issue

    def execute(self):
        print(f"🧹 STARTING AGGRESSIVE CLEANUP: {ROOT_DIR}")
        print("="*60)

        # 1. Move Files
        for file_path in ROOT_DIR.rglob("*"):
            if file_path.is_file():
                # Skip if ignored or in MASTER path
                if MASTER_DIR in file_path.parents:
                    continue
                if any(p in file_path.parts for p in IGNORED_DIRS):
                    continue
                if file_path.name == ".DS_Store":
                    continue
                    
                self.sort_file(file_path)

        # 2. Delete Empty Dirs
        self.clean_empty_dirs(ROOT_DIR)

        print("="*60)
        print(f"✅ CLEANUP COMPLETE.")
        print(f"   📦 Files Sorted: {self.moved_count}")
        print(f"   🗑️  Empty Folders Removed: {self.deleted_dirs}")

if __name__ == "__main__":
    cleaner = NoizyCleaner()
    cleaner.execute()
