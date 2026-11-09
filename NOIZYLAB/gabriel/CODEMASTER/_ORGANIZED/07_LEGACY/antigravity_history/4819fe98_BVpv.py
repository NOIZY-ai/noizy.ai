import os
import shutil
import time
import re
import subprocess
import wave
import zipfile
import tarfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
DEST_ROOT = Path.expanduser(Path("~/Universal/Library"))
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
ARCHIVE_EXTS = {'.zip', '.tar', '.gz'}
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

def get_semantic_context(fpath):
    tags = set()
    try:
        parents = list(fpath.parents)
        ignored = {'users', 'downloads', 'universal', 'library', 'assets', 'audio', 'image', 'video', 'text', 'desktop', 'documents', 'temp_unpack'}
        for p in parents[:2]: 
            name = p.name.lower().replace("_", " ").replace("-", " ")
            parts = name.split()
            for part in parts:
                if part not in ignored and len(part) > 2 and not part.isdigit():
                    tags.add(part.title())
    except: pass
    return list(tags)

def get_duration_class(file_path):
    try:
        with wave.open(str(file_path), 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            duration = frames / float(rate)
            if duration < 2.0: return "One Shot", duration
            if duration >= 2.0 and duration < 30.0: return "Loop", duration
            return "Track", duration
    except:
        try:
            size_kb = file_path.stat().st_size / 1024
            if size_kb < 350: return "One Shot", 0
            if size_kb > 350 and size_kb < 10000: return "Loop", 0
            return "Track", 0
        except: pass
    return "Unknown", 0

def set_xattr(file_path, key, value):
    try:
        subprocess.run(["xattr", "-w", key, str(value), str(file_path)], check=True, stderr=subprocess.DEVNULL)
        return True
    except: return False

def clean_filename(name):
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r'(?u)[^-\w.]', '', s)
    return s.lower()

def classify(fpath):
    name = fpath.name.lower()
    ext = fpath.suffix.lower().replace('.', '')
    modality = "Unsorted"
    
    # Omni-Classification
    if ext in {"png","jpg","jpeg","gif","tif","tiff","svg","psd","ai"}: modality = "Image"
    elif ext in {"wav","aiff","flac","mp3","ogg","m4a"}: modality = "Audio"
    elif ext in {"mp4","mov","mkv","webm"}: modality = "Video"
    elif ext in {"pdf","doc","docx","txt","md"}: modality = "Text"
    elif ext in {"vst", "vst3", "component", "aax", "dpm"}: modality = "Plugins"
    elif ext in {"nki", "fxp", "aupreset", "fxb", "patch"}: modality = "Presets"
    elif ext in {"ttf", "otf", "fnt", "woff"}: modality = "Fonts"
    elif ext in {"logicx", "als", "ptx", "cpr", "flp"}: modality = "Projects"
    
    tag = "General"
    for p_name, p_regex in PATTERNS.items():
        if p_regex.search(name):
            clean_tag = p_name.replace("type_", "").replace("mood_", "").title()
            if "mood" in p_name: clean_tag += "_Mood"
            tag = clean_tag
            break
            
    # Sub-classify Plugins/Presets if possible? 
    # For now, just 'General' or regex match (e.g. 'kick preset' -> Kick).
    return modality, tag

def process_archive(archive_path):
    """
    Explodes the archive, processes contents, then removes archive.
    """
    temp_dir = archive_path.parent / f"{archive_path.stem}_temp_unpack"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        print(f"   📦 Exploding Archive: {archive_path.name}")
        shutil.unpack_archive(str(archive_path), str(temp_dir))
        
        # Recursive Scan of the temp dir
        unpacked_files = []
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                if not f.startswith('.'):
                    unpacked_files.append(Path(root) / f)
        
        # Process each unpacked file
        # We process them sequentially here to assume strict order within archive context?
        # Or parallel? Since this is already running in a thread (process_atom called via ThreadPool?), 
        # we should avoid nesting ThreadPools blindly. Just run sequentially for the archive contents.
        success_count = 0
        for f in unpacked_files:
            # Recursively call logic (but NOT via process_atom which deletes source... wait)
            # process_atom deletes source. That is GOOD for temp unpacked files.
            # We want to consume the temp files.
            res, msg = process_atom(f)
            if res == 1: success_count += 1
            
        print(f"   ✅ Assimilated {success_count} files from {archive_path.name}")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        archive_path.unlink() # Delete the original zip
        return (1, f"Archive/{archive_path.name}")
        
    except Exception as e:
        # Cleanup temp if failed
        if temp_dir.exists(): shutil.rmtree(temp_dir)
        return (-1, f"Archive Fail: {e}")

def process_atom(src_path):
    try:
        p = Path(src_path)
        if not p.exists(): return (0, "Skipped")
        
        # 0. ARCHIVE CHECK
        if p.suffix.lower() in ARCHIVE_EXTS:
            return process_archive(p)

        # 1. SEMANTIC CONTEXT
        context_tags = get_semantic_context(p)
        
        modality, tag = classify(p)
        dest_dir = DEST_ROOT / "Assets" / modality / tag
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        is_audio = p.suffix.lower() in AUDIO_EXTS
        clean_stem = clean_filename(p.stem)
        dest_name = f"{clean_stem}.wav" if is_audio else clean_filename(p.name)
        dest_path = dest_dir / dest_name
        
        if dest_path.exists():
            ts = int(time.time_ns())
            base_ext = '.wav' if is_audio else p.suffix
            dest_name = f"{clean_stem}_{ts}{base_ext}"
            dest_path = dest_dir / dest_name

        # 2. CONVERT / MOVE
        if is_audio:
            cmd = ["afconvert"] + AF_ARGS + [str(p), str(dest_path)]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            except:
                shutil.copy2(str(p), str(dest_path))
        else:
            # Just Copy/Move
             # If it's a folder (e.g. .logicx package), copytree?
             # Classify treats extensions provided as files mainly. 
             # LogicX is a dir on macOS but treated as file. shutil.move handles it.
             # copy2 might fail on dir.
             if p.is_dir():
                 shutil.copytree(str(p), str(dest_path), dirs_exist_ok=True)
             else:
                 shutil.copy2(str(p), str(dest_path))

        # 3. INJECT METADATA
        if is_audio and dest_path.exists() and dest_path.stat().st_size > 0:
            bpm, key_sig = get_smart_metadata(p.name)
            dur_class, dur_sec = get_duration_class(dest_path)
            
            set_xattr(dest_path, "com.apple.metadata:kMDItemAuthors", "Audio Unitor AI")
            set_xattr(dest_path, "com.apple.metadata:kMDItemMusicalGenre", tag)
            if bpm: set_xattr(dest_path, "com.apple.metadata:kMDItemTempo", bpm)
            if key_sig: set_xattr(dest_path, "com.apple.metadata:kMDItemKeySignature", key_sig)
            
            keywords = context_tags + [dur_class]
            if keywords:
                kw_str = ",".join(keywords)
                set_xattr(dest_path, "com.apple.metadata:kMDItemKeywords", kw_str)
            
            desc = f"{dur_class} in {tag}. Context: {', '.join(context_tags)}"
            set_xattr(dest_path, "com.apple.metadata:kMDItemDescription", desc)

        # 4. DELETE SOURCE
        if dest_path.exists() and (dest_path.is_dir() or dest_path.stat().st_size > 0):
            if p.is_dir(): shutil.rmtree(str(p))
            else: p.unlink()
            return (1, f"{tag}/{dest_path.name}")
        else:
             return (-1, f"Transfer Failed: {p.name}")

    except Exception as e:
        return (-1, f"Error {src_path}: {e}")

def run_singularity(source_dir):
    print(f"{BOLD}{CYAN}🌌 THE SINGULARITY: EVENT HORIZON ACTIVE{RESET}")
    print(f"   Source: {source_dir}")
    print(f"   Dest:   {DEST_ROOT}")
    print(f"   Mode:   Archives + Omni-Types + Atomic")

    files = []
    # Use os.scandir or walk, but be careful of changing dir structure during walk (Archives exploding)
    # Better to collect top-level first? Or just walk.
    # Note: process_archive handles its own recursion on the temp dir.
    # So we just need to find the Archives in the source walk.
    
    for root, dirs, filenames in os.walk(source_dir):
        if str(Path(root).resolve()).startswith(str(DEST_ROOT.resolve())): continue
        for f in filenames:
            if not f.startswith('.'):
                files.append(Path(root) / f)
                
    print(f"   Engaging Singularity Engine on {len(files)} items...")
    
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
    print(f"   Rate: {rate:.1f} items/sec")
    print(f"   Total: {count}")
    print(f"   Errors: {errors}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_singularity.py <source_dir>")
    else:
        run_singularity(sys.argv[1])
