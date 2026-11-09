import os
import shutil
import re
from pathlib import Path

import argparse

# Configuration
# DEFAULT_SOURCE = "/Users/m2ultra/Downloads/Audio_Inbox" 
# DEFAULT_DEST = "/Users/m2ultra/Audio_Unitor/Staging_Area"


def sanitize_name(name):
    """
    Cleans up folder/file names to be 'Like New'.
    - Title Case
    - Replaces underscores with spaces (optional preference)
    - Removes weird characters
    """
    # Remove leading/trailing whitespace
    name = name.strip()
    
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    
    # Optional: Title Case
    name = name.title()
    
    return name

def is_audio_file(filename):
    AUDIO_EXT = {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.mid', '.midi'}
    return Path(filename).suffix.lower() in AUDIO_EXT

def organize_folder(source, destination, dry_run=True):
    """
    Walks through the source and moves audio to destination with 'Like New' structure.
    """
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source}' does not exist.")
        return

    print(f"Scanning {source}...")
    print(f"Target: {destination}")
    mode = "[DRY RUN]" if dry_run else "[LIVE]"
    print(f"Mode: {mode}")
    print("-" * 40)
    
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.startswith('.'): continue # Skip hidden files
            
            src_path = Path(root) / file
            
            if is_audio_file(file):
                # Determine 'Like New' path
                # For now, we preserve the parent folder name but clean it up
                parent_folder = Path(root).name
                clean_folder_name = sanitize_name(parent_folder)
                
                # If the parent folder is generic like "Samples", go up one level
                if clean_folder_name.lower() in ['samples', 'audio', 'bounce']:
                    parent_parent = Path(root).parent.name
                    clean_folder_name = f"{sanitize_name(parent_parent)}_{clean_folder_name}"

                dest_folder = Path(destination) / clean_folder_name
                dest_folder.mkdir(parents=True, exist_ok=True)
                
                dest_path = dest_folder / file 
                
                print(f"{mode} Move: {file} -> {clean_folder_name}/")
                
                if not dry_run:
                    try:
                        shutil.move(str(src_path), str(dest_path))
                    except Exception as e:
                        print(f"Error moving {file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Unitor: Organize Audio Files")
    parser.add_argument("--source", "-s", help="Source directory to scan")
    parser.add_argument("--dest", "-d", default="/Users/m2ultra/Audio_Unitor/Staging_Area", help="Destination directory")
    parser.add_argument("--live", action="store_true", help="Actually move files (disable simulation)")
    
    args = parser.parse_args()
    
    print("MUSIC UNITOR: AUDIO ORGANIZER ACTIVATED")
    
    if not args.source:
        print("Please provide a source directory using --source")
    else:
        organize_folder(args.source, args.dest, dry_run=not args.live)
