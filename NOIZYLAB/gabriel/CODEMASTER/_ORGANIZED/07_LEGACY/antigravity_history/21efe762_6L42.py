import os
import shutil
import re
from pathlib import Path

import argparse
import subprocess
import shutil
import zipfile
import tarfile

# Configuration
# DEFAULT_SOURCE = "/Users/m2ultra/Downloads/Audio_Inbox" 
# DEFAULT_DEST = "/Users/m2ultra/Audio_Unitor/Staging_Area"
PROCESSED_DIR = "/Users/m2ultra/Audio_Unitor/Processed_Archives"



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
    return name

def notify_user(title, message):
    """Sends a native MacOS notification."""
    try:
        script = f'display notification "{message}" with title "{title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", script])
    except Exception as e:
        print(f"Notification Error: {e}")

def get_category(filename):
    """Smartly detects category based on keywords."""
    name = filename.lower()
    if any(x in name for x in ['kick', 'snare', 'hat', 'clap', 'cymbal', 'drum', 'perc']):
        return "Drums"
    if any(x in name for x in ['bass', '808', 'sub']):
        return "Bass"
    if any(x in name for x in ['synth', 'pad', 'lead', 'pluck', 'arp', 'key']):
        return "Synths"
    if any(x in name for x in ['fx', 'riser', 'faller', 'sweep', 'noise']):
        return "FX"
    if any(x in name for x in ['vox', 'vocal', 'acapella', 'adlib']):
        return "Vocals"
    if any(x in name for x in ['loop']):
        return "Loops"
    return "Uncategorized"

def is_audio_file(filename):
    AUDIO_EXT = {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.mid', '.midi'}
    return Path(filename).suffix.lower() in AUDIO_EXT

def is_archive(filename):
    return Path(filename).suffix.lower() in {'.zip', '.rar', '.tar', '.gz'}

def extract_archive(filepath, extract_to):
    """Extracts zip or tar files."""
    try:
        if str(filepath).endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        elif str(filepath).endswith(('.tar', '.gz')):
            with tarfile.open(filepath, 'r') as tar_ref:
                tar_ref.extractall(extract_to)
            return True
    except Exception as e:
        print(f"Extraction Error for {filepath}: {e}")
    return False

def organize_folder(source, destination, dry_run=True, level=0):
    """
    Recursive organizer with auto-unzip and smart sorting.
    """
    source_path = Path(source)
    dest_path = Path(destination)
    
    if level == 0:
        if not source_path.exists():
            print(f"Error: Source directory '{source}' does not exist.")
            return

        print(f"Scanning {source}...")
        mode = "[DRY RUN]" if dry_run else "[LIVE]"
        print(f"Mode: {mode}")
    
    items_moved = 0
    
    # Process Directories (and extracted folders)
    for item in source_path.iterdir():
        if item.name.startswith('.'): continue
        
        # Handle Archives
        if item.is_file() and is_archive(item):
            print(f"📦 Archive found: {item.name}")
            if not dry_run:
                # Create a temp dir for extraction
                temp_extract_dir = source_path / f"_extracted_{item.stem}"
                temp_extract_dir.mkdir(exist_ok=True)
                
                if extract_archive(item, temp_extract_dir):
                    print(f"   ↳ Extracted to {temp_extract_dir.name}")
                    # Recursively organize the extracted content
                    items_moved += organize_folder(temp_extract_dir, destination, dry_run=False, level=level+1)
                    
                    # Cleanup
                    item_dest = Path(PROCESSED_DIR)
                    item_dest.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.move(str(item), str(item_dest / item.name))
                        shutil.rmtree(temp_extract_dir) # Remove temp dir after moving contents
                        print(f"   ↳ Archive archived to {PROCESSED_DIR}")
                    except Exception as e:
                        print(f"   ⚠️ Cleanup warning: {e}")
                else:
                    print(f"   ⚠️ Failed to extract {item.name}")
            continue

        # Handle Directory Recursion
        if item.is_dir():
             items_moved += organize_folder(item, destination, dry_run, level=level+1)
             continue

        # Handle Audio Files
        if item.is_file() and is_audio_file(item):
            category = get_category(item.name)
            
            # Determine 'Like New' path: Destination / Category / ParentFolder / File
            # If we are in the root source, just use Category/File
            
            clean_parent = sanitize_name(item.parent.name)
            if clean_parent.startswith("_Extracted"): # specific handling for our temp dirs
                 clean_parent = sanitize_name(item.parent.name.replace("_Extracted_", ""))

            if item.parent == source_path and level == 0:
                 # File is loose in inbox
                 final_dest_folder = dest_path / category / "Loose_Files"
            else:
                 final_dest_folder = dest_path / category / clean_parent

            final_dest_path = final_dest_folder / item.name
            
            print(f"{'[LIVE]' if not dry_run else '[DRY]'} Move: {item.name} -> {category}/{final_dest_folder.name}/")
            
            if not dry_run:
                try:
                    final_dest_folder.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item), str(final_dest_path))
                    items_moved += 1
                except Exception as e:
                    print(f"Error moving {item.name}: {e}")

    if level == 0 and items_moved > 0 and not dry_run:
        notify_user("Audio Unitor", f"Processed {items_moved} audio files.")
    
    return items_moved


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
