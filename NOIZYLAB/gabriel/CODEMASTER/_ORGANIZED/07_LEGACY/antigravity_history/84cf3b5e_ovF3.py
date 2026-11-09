import os
import shutil
import re
from pathlib import Path

# Configuration
SOURCE_DIR = "/Users/m2ultra/Downloads/Audio_Inbox" # Example
DEST_DIR = "/Users/m2ultra/Audio_Unitor/Staging_Area"

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

def organize_folder(source, destination):
    """
    Walks through the source and moves audio to destination with 'Like New' structure.
    """
    print(f"Scanning {source}...")
    
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
                
                dest_path = dest_folder / file # We warn't renaming files yet, just folders
                
                # Simulation mode print
                print(f"[MOVE] {src_path} -> {dest_path}")
                
                # Uncomment to actually move
                # shutil.move(str(src_path), str(dest_path))

if __name__ == "__main__":
    print("MUSIC UNITOR: AUDIO ORGANIZER ACTIVATED")
    # Ask user for input if running interactively, or use defaults
    # For now, just printing the config
    print(f"Source: {SOURCE_DIR}")
    print(f"Destination: {DEST_DIR}")
    print("Run this script to see the 'Like New' organization plan.")
