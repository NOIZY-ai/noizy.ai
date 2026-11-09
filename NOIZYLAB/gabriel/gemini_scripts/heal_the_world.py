import os
import shutil
import time

# CONFIGURATION
TARGET_ROOT = "/Volumes/6TB/Sample_Libraries"
TRASH_DIR = os.path.join(TARGET_ROOT, "_MC96_QUALITY_UPGRADE_TRASH")

# JUNK DEFINITIONS
JUNK_FILES = [".DS_Store", "Thumbs.db", "Desktop.ini"]
JUNK_PREFIXES = ["._"] # AppleDouble

stats = {
    "junk_files_removed": 0,
    "trash_bytes_cleared": 0,
    "empty_dirs_removed": 0
}

print(f"🌍 HEAL THE WORLD PROTOCOL ACTIVATED")
print(f"🎯 Target Sector: {TARGET_ROOT}")

# 1. EMPTY THE SPECIFIC TRASH (The "Shitty Files" from previous step)
if os.path.exists(TRASH_DIR):
    print(f"🗑️ Emptying Quality Upgrade Trash: {TRASH_DIR}...")
    try:
        # Calculate size for stats
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(TRASH_DIR):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        
        shutil.rmtree(TRASH_DIR)
        stats["trash_bytes_cleared"] += total_size
        print(f"   ✅ Deleted {total_size / (1024*1024):.2f} MB of trash.")
    except Exception as e:
        print(f"   ❌ Error deleting trash: {e}")
else:
    print("   ✅ Trash already empty.")

# 2. GLOBAL JUNK CLEANUP
print("🧹 Sweeping for System Junk (.DS_Store, ._*) ...")
for root, dirs, files in os.walk(TARGET_ROOT):
    for file in files:
        file_path = os.path.join(root, file)
        
        should_delete = False
        if file in JUNK_FILES:
            should_delete = True
        elif any(file.startswith(p) for p in JUNK_PREFIXES):
            should_delete = True
            
        if should_delete:
            try:
                os.remove(file_path)
                stats["junk_files_removed"] += 1
                # print(f"   Removed: {file}")
            except OSError:
                pass

# 3. FINAL EMPTY DIRECTORY SWEEP
print("✨ Finalizing Structure (Removing Empty Folders)...")
for root, dirs, files in os.walk(TARGET_ROOT, topdown=False):
    if not files and not dirs:
        try:
            os.rmdir(root)
            stats["empty_dirs_removed"] += 1
        except OSError:
            pass

print(f"\n🌍 HEALING COMPLETE.")
print(f"- Trash Emptied: {stats['trash_bytes_cleared'] / (1024*1024):.2f} MB")
print(f"- System Junk Files Removed: {stats['junk_files_removed']}")
print(f"- Empty Folders Dissolved: {stats['empty_dirs_removed']}")
print("The Universe is cleaner. 🕊️")
