import os
import shutil

source_root = "/Users/m2ultra"
dest_root = "/Volumes/12TB/Audio_Evacuation_M2Ultra"
list_file = "/Users/m2ultra/audio_files_to_move.txt"

with open(list_file, 'r') as f:
    files = [line.strip() for line in f if line.strip()]

print(f"Moving {len(files)} files from {source_root} to {dest_root}...")

count = 0
for src_path in files:
    if not os.path.exists(src_path):
        print(f"Skipping missing file: {src_path}")
        continue
        
    # Calculate relative path
    if src_path.startswith(source_root):
        rel_path = os.path.relpath(src_path, source_root)
        dest_path = os.path.join(dest_root, rel_path)
        
        # Create dest dir
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Move
        try:
            shutil.move(src_path, dest_path)
            print(f"Moved: {rel_path}")
            count += 1
        except Exception as e:
            print(f"Error moving {src_path}: {e}")

print(f"Completed. Moved {count} files.")
