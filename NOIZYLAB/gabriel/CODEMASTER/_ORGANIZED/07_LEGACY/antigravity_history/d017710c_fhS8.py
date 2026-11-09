import os
import shutil
import time
from pathlib import Path

# Configuration
DEST_ROOT = Path.expanduser(Path("~/Universal"))
PROJECT_NAME = "NOIZYai"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def classify(name, ext):
    n = name.lower()
    e = ext.lower().replace('.', '')
    
    # Modality
    modality = "Unsorted"
    if e in {"png","jpg","jpeg","gif","tif","tiff","svg","psd","ai"}: modality = "Image"
    elif e in {"wav","aiff","flac","mp3","ogg"}: modality = "Audio"
    elif e in {"mp4","mov","mkv","webm"}: modality = "Video"
    elif e in {"pdf","doc","docx","txt","md"}: modality = "Text"
    
    # Context Tags
    tag = "General"
    if "logo" in n: tag = "Logo"
    elif "motion" in n: tag = "Motion"
    elif "voice" in n: tag = "Voice"
    elif "shimmer" in n: tag = "Shimmer"
    elif "contract" in n: tag = "Contracts"
    elif "brief" in n: tag = "Creative"
    elif "kick" in n or "snare" in n or "drum" in n: tag = "Drums"
    
    return modality, tag

def organize_file(src_path):
    try:
        path_obj = Path(src_path)
        if not path_obj.exists(): return False
        
        name = path_obj.name
        ext = path_obj.suffix
        
        modality, tag = classify(name, ext)
        
        # Structure: Universal / Projects / NOIZYai / Assets / [Modality] / [Tag]
        # Or user script: Projects / Project / Assets / Tags
        # Let's stick to User Script logic: Assets / Tags
        # But separating by Modality is cleaner. Let's do Assets / Tag
        
        dest_dir = DEST_ROOT / "Projects" / PROJECT_NAME / "Assets" / tag
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True)
            
        dest_path = dest_dir / name
        
        # Handle Collision
        if dest_path.exists():
            # append timestamp
            ts = int(time.time())
            stem = path_obj.stem
            new_name = f"{stem}_{ts}{ext}"
            dest_path = dest_dir / new_name
            
        print(f"   📦 Moving {name} -> {tag}/")
        shutil.move(str(src_path), str(dest_path))
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to move {src_path}: {e}")
        return False

def run_organizer(source_dir):
    print(f"{BOLD}🗄️  TURBO ORGANIZER INITIALIZED{RESET}")
    print(f"   Source: {source_dir}")
    print(f"   Dest:   {DEST_ROOT}")
    
    src = Path(source_dir)
    if not src.exists():
        print("   ❌ Source not found.")
        return

    count = 0
    # Walk and move
    # Careful: iterating while modifying.
    # Collect list first.
    files_to_move = []
    
    for root, dirs, files in os.walk(src):
        for f in files:
            if not f.startswith('.'):
                files_to_move.append(os.path.join(root, f))
                
    print(f"   Found {len(files_to_move)} items. sorting...")
    
    for f in files_to_move:
        if organize_file(f):
            count += 1
            
    print(f"\n{GREEN}✨ ORGANIZATION COMPLETE{RESET}")
    print(f"   Sorted {count} files into {DEST_ROOT}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_organizer.py <source_path>")
    else:
        run_organizer(sys.argv[1])
