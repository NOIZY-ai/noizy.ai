import os
import shutil
import time
import re
import subprocess
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

import re

# Intelligence Heuristics (Shared with Neural Indexer)
PATTERNS = {
    "type_kick": re.compile(r"kick|bd|bassdrum|stomp|808_kick", re.IGNORECASE),
    "type_snare": re.compile(r"snare|sd|rim|clap|snap", re.IGNORECASE),
    "type_hat": re.compile(r"hat|hh|cymbal|ride|crash|shaker|tamb", re.IGNORECASE),
    "type_tom": re.compile(r"tom|timpani|cong|bongo", re.IGNORECASE),
    "type_perc": re.compile(r"perc|hit|impact|metal|wood|click", re.IGNORECASE),
    "type_loop": re.compile(r"loop|drumloop|break|fill", re.IGNORECASE),
    "type_bass": re.compile(r"bass|sub|808|log|reese", re.IGNORECASE),
    "type_synth": re.compile(r"synth|lead|pad|pluck|arp|saw|square", re.IGNORECASE),
    "type_guitar": re.compile(r"guitar|gtr|acoustic|electric|dist", re.IGNORECASE),
    "type_piano": re.compile(r"piano|keys|rhodes|organ", re.IGNORECASE),
    "type_orchestra": re.compile(r"viol|cello|string|brass|horn|trumpet", re.IGNORECASE),
    "type_vocal": re.compile(r"vocal|vox|acapella|chant|choir|adlib|hook|verse", re.IGNORECASE),
    "type_speech": re.compile(r"speech|talk|spoken|podcast", re.IGNORECASE),
    "type_fx": re.compile(r"fx|sfx|noise|riser|impact|glass|ping|tink|blow|morse|bottle|pop|purr|sosumi|hero|funk|frog|laser|sweep|trans", re.IGNORECASE),
    "type_atmos": re.compile(r"atmos|texture|drone|ambi|bg|bed", re.IGNORECASE),
    "mood_dark": re.compile(r"dark|evil|horror|scary|grim", re.IGNORECASE),
    "mood_happy": re.compile(r"happy|uplifting|major|bright", re.IGNORECASE),
    "type_logo": re.compile(r"logo|brand|guideline|brief|contract", re.IGNORECASE),
    "type_doc": re.compile(r"invoice|receipt|tax|legal|license", re.IGNORECASE)
}

MIME_MAP = {
    'audio/wav': '.wav',
    'audio/x-wav': '.wav',
    'audio/mpeg': '.mp3',
    'audio/x-aiff': '.aif',
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'application/pdf': '.pdf',
    'text/plain': '.txt',
    'video/mp4': '.mp4',
    'video/quicktime': '.mov'
}

def detect_extension(file_path):
    try:
        # Magic Eye: Use system 'file' command
        result = subprocess.run(
            ['file', '--mime-type', '-b', str(file_path)], 
            capture_output=True, text=True, check=True
        )
        mime = result.stdout.strip()
        print(f"   👁️  Magic Eye detected: {mime}")
        return MIME_MAP.get(mime, "")
    except Exception as e:
        print(f"   ⚠️ Magic Eye failed: {e}")
        return ""

def classify(name, ext):
    n = name.lower()
    e = ext.lower().replace('.', '')
    
    # Modality
    modality = "Unsorted"
    if e in {"png","jpg","jpeg","gif","tif","tiff","svg","psd","ai"}: modality = "Image"
    elif e in {"wav","aiff","flac","mp3","ogg"}: modality = "Audio"
    elif e in {"mp4","mov","mkv","webm"}: modality = "Video"
    elif e in {"pdf","doc","docx","txt","md"}: modality = "Text"
    
    # Context Tags (Prioritized)
    tag = "General"
    
    # Check Patterns
    for p_name, p_regex in PATTERNS.items():
        if p_regex.search(n):
            # Clean tag name (type_kick -> Kick, mood_dark -> Dark_Mood)
            clean_tag = p_name.replace("type_", "").replace("mood_", "").title()
            if "mood" in p_name: clean_tag += "_Mood"
            return modality, clean_tag
            
    return modality, tag

def organize_file(src_path):
    try:
        path_obj = Path(src_path)
        if not path_obj.exists(): return False
        
        name = path_obj.name
        ext = path_obj.suffix
        
        # MAGIC EYE: Fix missing extension
        if not ext or ext == ".":
            print(f"   🔍 Mystery File Found: {name}")
            detected_ext = detect_extension(src_path)
            if detected_ext:
                print(f"   ✨ Auto-Fixing: {name} -> {name}{detected_ext}")
                ext = detected_ext
                name = f"{name}{ext}" # Update name for classification
                # We don't rename source yet, we rename at destination
            else:
                 print(f"   🤷 Could not identify: {name}")

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
