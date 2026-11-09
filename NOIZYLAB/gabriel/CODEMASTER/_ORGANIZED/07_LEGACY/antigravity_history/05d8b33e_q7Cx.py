import os

ROOT_DIR = "/Volumes/6TB/Sample_Libraries"
TRASH_DIR = "/Volumes/6TB/Sample_Libraries/_MC96_QUALITY_UPGRADE_TRASH"

removed = 0

print(f"🧹 CLEANING EMPTY DIRECTORIES in {ROOT_DIR}")

# Walk bottom-up
for root, dirs, files in os.walk(ROOT_DIR, topdown=False):
    if root == TRASH_DIR:
        continue
    if not files and not dirs:
        try:
            os.rmdir(root)
            removed += 1
            # print(f"Removed empty: {root}")
        except:
            pass

print(f"✅ Removed {removed} empty folders.")
