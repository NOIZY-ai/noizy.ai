import os
import shutil
import time
import re
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
DEST_ROOT = Path.expanduser(Path("~/Universal/Library"))
BACKUP_ROOT = Path.expanduser(Path("~/Universal/Backups/Singularity_Trash"))
THREADS = max(4, (os.cpu_count() or 4) * 2)

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Reuse patterns
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

META_PATTERNS = {
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), 
}

AUDIO_EXTS = {'.wav', '.aif', '.aiff', '.mp3', '.m4a', '.flac', '.ogg'}

# Alchemist Args (44.1kHz 16-bit WAV)
AF_ARGS = ["-f", "WAVE", "-d", "LEI16@44100"]

def get_smart_metadata(filename):
    f_lower = filename.lower()
    bpm = None
    key = None
    bpm_match = META_PATTERNS["bpm"].search(f_lower)
    if bpm_match:
        try: bpm = int(bpm_match.group(1))
        except: pass
    key_match = META_PATTERNS["key"].search(filename)
    if key_match: key = key_match.group(1)
    return bpm, key

def set_xattr(file_path, key, value):
    try:
        subprocess.run(["xattr", "-w", key, str(value), str(file_path)], check=True, stderr=subprocess.DEVNULL)
        return True
    except: return False

def classify(fpath):
    name = fpath.name.lower()
    ext = fpath.suffix.lower().replace('.', '')
    modality = "Unsorted"
    if ext in {"png","jpg","jpeg","gif","tif","tiff","svg","psd","ai"}: modality = "Image"
    elif ext in {"wav","aiff","flac","mp3","ogg","m4a"}: modality = "Audio"
    elif ext in {"mp4","mov","mkv","webm"}: modality = "Video"
    elif ext in {"pdf","doc","docx","txt","md"}: modality = "Text"
    tag = "General"
    for p_name, p_regex in PATTERNS.items():
        if p_regex.search(name):
            clean_tag = p_name.replace("type_", "").replace("mood_", "").title()
            if "mood" in p_name: clean_tag += "_Mood"
            tag = clean_tag
            break
    return modality, tag

def clean_filename(name):
    # Basic Detox (Snake Case)
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r'(?u)[^-\w.]', '', s)
    return s.lower()

def process_atom(src_path):
    # 1. READ & CLASSIFY
    try:
        p = Path(src_path)
        if not p.exists(): return (0, "Skipped")
        
        modality, tag = classify(p)
        
        # Structure: ~/Universal/Library/Assets/[Modality]/[Tag]
        dest_dir = DEST_ROOT / "Assets" / modality / tag
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Name handling (Force .wav for Audio, keep others) + SANITIZE
        is_audio = p.suffix.lower() in AUDIO_EXTS
        clean_stem = clean_filename(p.stem)
        dest_name = f"{clean_stem}.wav" if is_audio else clean_filename(p.name)
        
        dest_path = dest_dir / dest_name
        
        # Collision
        if dest_path.exists():
            ts = int(time.time_ns())
            base_ext = '.wav' if is_audio else p.suffix
            dest_name = f"{clean_stem}_{ts}{base_ext}"
            dest_path = dest_dir / dest_name

        # 2. CONVERT / MOVE (Atomic Action)
        converted = False
        if is_audio:
            # ALCHEMIST + ARCHITECT: Convert DIRECTLY to destination
            cmd = ["afconvert"] + AF_ARGS + [str(p), str(dest_path)]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                converted = True
            except:
                # Fallback: Just copy if conversion fails (or plain move)
                shutil.copy2(str(p), str(dest_path))
        else:
            # Non-audio: Just move/copy
            shutil.copy2(str(p), str(dest_path))

        # 3. INJECT METADATA (Librarian)
        if is_audio and dest_path.exists():
            bpm, key_sig = get_smart_metadata(p.name)
            set_xattr(dest_path, "com.apple.metadata:kMDItemAuthors", "Audio Unitor AI")
            set_xattr(dest_path, "com.apple.metadata:kMDItemMusicalGenre", tag) # New: Inject Tag!
            if bpm: set_xattr(dest_path, "com.apple.metadata:kMDItemTempo", bpm)
            if key_sig: set_xattr(dest_path, "com.apple.metadata:kMDItemKeySignature", key_sig)

        # 4. DELETE SOURCE (Complete the Move)
        # Verify valid dest first
        if dest_path.exists() and dest_path.stat().st_size > 0:
            p.unlink()
            return (1, f"{tag}/{dest_path.name}")
        else:
             return (-1, f"Transfer Failed: {p.name} -> {dest_path} (Exists: {dest_path.exists()})")

    except Exception as e:
        return (-1, f"Error {src_path}: {e}")

def run_singularity(source_dir):
    print(f"{BOLD}{CYAN}🌌 THE SINGULARITY: TYPE-IV CIVILIZATION PIPELINE{RESET}")
    print(f"   Source: {source_dir}")
    print(f"   Dest:   {DEST_ROOT}")
    print(f"   Mode:   Atomic (Read -> Convert -> Tag -> Move -> Delete)")

    files = []
    for root, dirs, filenames in os.walk(source_dir):
        # Skip Library itself
        if str(Path(root).resolve()).startswith(str(DEST_ROOT.resolve())): continue
        for f in filenames:
            if not f.startswith('.'):
                files.append(Path(root) / f)
                
    print(f"   Engaging Singularity Engine on {len(files)} files...")
    
    count = 0
    errors = 0
    start_t = time.time()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(process_atom, f): f for f in files}
        for i, future in enumerate(as_completed(future_to_file)):
            status, msg = future.result()
            if status == 1: count += 1
            elif status == -1: 
                errors += 1
                print(f"   {RED}Error: {msg}{RESET}")
            
            if (i+1) % 100 == 0:
                print(f"   ...processed {i+1}/{len(files)}...", end='\r')
                
    duration = time.time() - start_t
    rate = count / duration if duration > 0 else 0
    print(f"\n{GREEN}✨ SINGULARITY COMPLETE ({duration:.2f}s){RESET}")
    print(f"   Rate: {rate:.1f} files/sec")
    print(f"   Total: {count}")
    print(f"   Errors: {errors}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_singularity.py <source_dir>")
    else:
        run_singularity(sys.argv[1])
