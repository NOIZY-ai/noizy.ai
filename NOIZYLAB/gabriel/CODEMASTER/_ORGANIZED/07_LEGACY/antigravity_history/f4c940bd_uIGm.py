import os
import shutil
import time
import re
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
DEST_ROOT = Path.expanduser(Path("~/Universal/Library")) # Centralized Library
THREADS = max(4, (os.cpu_count() or 4) * 2)

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Reuse patterns for fallback
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

def get_xattr(file_path, key):
    try:
        res = subprocess.run(["xattr", "-p", key, str(file_path)], capture_output=True, text=True, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            return res.stdout.strip()
    except: pass
    return None

def classify(fpath):
    name = fpath.name.lower()
    ext = fpath.suffix.lower().replace('.', '')
    
    # 1. Check Metadata (Librarian Injection)
    # Note: We didn't inject Genre explicitly in Librarian yet (we did Authors/Tempo/Key), 
    # but let's support reading it if present OR key off filename regex if metadata missing.
    # Actually, Librarian v1 didn't put Type in xattr yet. 
    # So we mainly use Regex for Type, but could use Key for subfolder?
    
    # Modality
    modality = "Unsorted"
    if ext in {"png","jpg","jpeg","gif","tif","tiff","svg","psd","ai"}: modality = "Image"
    elif ext in {"wav","aiff","flac","mp3","ogg"}: modality = "Audio"
    elif ext in {"mp4","mov","mkv","webm"}: modality = "Video"
    elif ext in {"pdf","doc","docx","txt","md"}: modality = "Text"
    
    # Context Tags (Prioritized)
    tag = "General"
    
    # Check Patterns
    for p_name, p_regex in PATTERNS.items():
        if p_regex.search(name):
            clean_tag = p_name.replace("type_", "").replace("mood_", "").title()
            if "mood" in p_name: clean_tag += "_Mood"
            tag = clean_tag
            break
            
    return modality, tag

def organize_file(src_path):
    try:
        path_obj = Path(src_path)
        if not path_obj.exists(): return (0, "Missing")
        
        # Don't move files that are ALREADY in the library to avoid loops if source == dest root
        # Check if absolute path starts with DEST_ROOT
        try:
             if str(path_obj.resolve()).startswith(str(DEST_ROOT.resolve())):
                 return (0, "Already in Library")
        except: pass

        modality, tag = classify(path_obj)
        
        # Structure: ~/Universal/Library/Assets/[Modality]/[Tag]
        dest_dir = DEST_ROOT / "Assets" / modality / tag
        
        # Create dir safely (race condition possible with threads, ok to fail exists check)
        dest_dir.mkdir(parents=True, exist_ok=True)
            
        dest_path = dest_dir / path_obj.name
        
        # Handle Collision
        if dest_path.exists():
            ts = int(time.time_ns()) # Nanoseconds for safer threading collision avoidance
            stem = path_obj.stem
            new_name = f"{stem}_{ts}{path_obj.suffix}"
            dest_path = dest_dir / new_name
            
        shutil.move(str(src_path), str(dest_path))
        return (1, f"{tag}/{dest_path.name}")
        
    except Exception as e:
        return (-1, f"{src_path.name}: {e}")

def run_organizer(source_dir):
    print(f"{BOLD}CORE > 🏛️  TURBO ORGANIZER: THE ARCHITECT{RESET}")
    print(f"CORE > Source: {source_dir}")
    print(f"CORE > Dest:   {DEST_ROOT}")
    
    src = Path(source_dir)
    if not src.exists():
        print(f"CORE > {RED}❌ Source not found.{RESET}")
        return

    files_to_move = []
    print("CORE > Scanning chaos...")
    for root, dirs, files in os.walk(src):
        # SKIP if currently walking the Library itself
        if str(Path(root).resolve()).startswith(str(DEST_ROOT.resolve())):
            continue
            
        for f in files:
            if not f.startswith('.'):
                files_to_move.append(Path(root) / f)
                
    print(f"CORE > Found {len(files_to_move)} items. Constructing Order...")
    
    start_time = time.time()
    moved_count = 0
    errors = 0
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(organize_file, f): f for f in files_to_move}
        
        for i, future in enumerate(as_completed(future_to_file)):
            status, msg = future.result()
            if status == 1:
                moved_count += 1
            elif status == -1:
                errors += 1
                # print(f"   {RED}Error: {msg}{RESET}")
            
            if (i+1) % 100 == 0:
                print(f"CORE > ...sorted {i+1}/{len(files_to_move)}...", end='\r')

    duration = time.time() - start_time
    rate = moved_count / duration if duration > 0 else 0
    
    print(f"\n{GREEN}CORE > ✨ ARCHITECTURE COMPLETE ({duration:.2f}s){RESET}")
    print(f"CORE > Rate:   {rate:.1f} files/sec")
    print(f"CORE > Sorted: {moved_count}")
    print(f"CORE > Errors: {errors}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_organizer.py <source_path>")
    else:
        run_organizer(sys.argv[1])
