#!/usr/bin/env python3
"""
Quick cleanup script for absorbed folders
"""

from pathlib import Path
import shutil

print("🗑️  CLEANUP: Removing absorbed folders")
print("=" * 80)

folders = [
    '/Volumes/RED DRAGON/noizylab_rescue',
    '/Users/rsp_ms/Desktop/THE CLEANER'
]

for folder in folders:
    path = Path(folder)
    if path.exists():
        try:
            shutil.rmtree(path)
            print(f"✅ Deleted: {folder}")
        except Exception as e:
            print(f"❌ Error: {folder} - {e}")
    else:
        print(f"⚠️  Not found: {folder}")

print("\n✅ Cleanup complete!")
