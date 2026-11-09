import os
import shutil
import time
import re
import subprocess
import wave
import struct
import math
import zipfile
import tarfile
import sqlite3
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Configuration
DEST_ROOT = Path.expanduser(Path("~/Universal/Library"))
TIME_MACHINE_ROOT = Path.expanduser(Path("~/Universal/Time_Machine"))
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")
import sys
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
LIBRARY_ROOT = Path.expanduser(Path("~/Universal/Library"))

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def singularity_clean(target_dir):
    # Initialize Conciousness
    brain = MemCell()
    brain.log_event(brain.covenant_id, "SINGULARITY_START", f"Singularity Protocol Initiated: Cleaning {target_dir}", vibe=65, author="SINGULARITY")

    print(f"{BOLD}{CYAN}CORE > 🌪️ SINGULARITY PROTOCOL: Cleaning {target_dir}...{RESET}")

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
    "artist_title": re.compile(r"(.+?)\s+-\s+(.+)")
}

AUDIO_EXTS = {'.wav', '.aif', '.aiff', '.mp3', '.m4a', '.flac', '.ogg'}
ARCHIVE_EXTS = {'.zip', '.tar', '.gz'}
AF_ARGS = ["-f", "WAVE", "-d", "LEI16@44100"]

# --- DATABASE / MEMORY CORE ---
def db_init():
    try:
        if not DB_PATH.parent.exists(): DB_PATH.parent.mkdir(parents=True)
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        c = conn.cursor()
        # Provenance Schema
        c.execute("""CREATE TABLE IF NOT EXISTS provenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            original_path TEXT,
            final_path TEXT,
            file_hash TEXT,
            agent TEXT
        )""")
        # Indexes
        c.execute("""CREATE INDEX IF NOT EXISTS idx_prov_hash ON provenance(file_hash)""")
        c.execute("""CREATE INDEX IF NOT EXISTS idx_prov_final ON provenance(final_path)""")
        return conn
    except: return None

# Global DB Connection (Thread safe via check_same_thread=False or per-thread cursor)
# SQLite is thread-safe for sharing connection in recent python, but cursor per thread is safer.
# We will use a shared connection for simplicity in this script, locking commits if needed.
# Or just open/close per batch. Let's pass `conn` around or use a global.
DB_CONN = db_init()

def log_provenance(action, orig_path, final_path, file_hash=None):
    if not DB_CONN: return
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        DB_CONN.execute("INSERT INTO provenance (timestamp, action, original_path, final_path, file_hash, agent) VALUES (?, ?, ?, ?, ?, ?)",
                       (ts, action, str(orig_path), str(final_path), file_hash, "Singularity v35"))
        DB_CONN.commit()
    except: pass

def fast_hash(path):
    # Minimal hash for provenance (Size+Name enough? No, content for ID)
    # Use DNA logic?
    try:
        h = hashlib.md5()
        with open(path, "rb") as f:
            h.update(f.read(4096)) # Just head for speed log
        return h.hexdigest()
    except: return "unknown"

def create_time_machine_backup(src_path):
    try:
        try:
            rel_path = src_path.relative_to(Path.home())
        except:
            rel_path = Path(str(src_path).lstrip("/"))
            
        backup_path = SESSION_BACKUP_DIR / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        if hasattr(os, 'link'):
            os.link(src_path, backup_path)
        else:
            shutil.copy2(src_path, backup_path)
            
        return True
    except Exception:
        return False

def get_smart_metadata(filename):
    f_lower = filename.lower()
    bpm = None
    key = None
    artist = None
    title = None
    
    bpm_match = META_PATTERNS["bpm"].search(f_lower)
    if bpm_match:
        try: bpm = int(bpm_match.group(1))
        except: pass
    key_match = META_PATTERNS["key"].search(filename)
    if key_match: key = key_match.group(1)
    
    # Try Artist - Title
    at_match = META_PATTERNS["artist_title"].search(Path(filename).stem)
    if at_match:
        artist = at_match.group(1).strip()
        title = at_match.group(2).strip()
        
    return bpm, key, artist, title

def get_semantic_context(fpath):
    tags = set()
    try:
        parents = list(fpath.parents)
        ignored = {'users', 'downloads', 'universal', 'library', 'assets', 'audio', 'image', 'video', 'text', 'desktop', 'documents', 'temp_unpack', 'scavenge_bin'}
        for p in parents[:2]: 
            name = p.name.lower().replace("_", " ").replace("-", " ")
            parts = name.split()
            for part in parts:
                if part not in ignored and len(part) > 2 and not part.isdigit():
                    tags.add(part.title())
    except: pass
    return list(tags)

def polish_audio(file_path):
    try:
        temp_path = file_path.with_suffix('.tmp.wav')
        modified = False
        
        with wave.open(str(file_path), 'rb') as wav:
            channels = wav.getnchannels()
            width = wav.getsampwidth()
            rate = wav.getframerate()
            frames = wav.getnframes()
            
            if width != 2: return False
            if file_path.stat().st_size > 500 * 1024 * 1024: return False

            raw_data = wav.readframes(frames)
            
            if channels == 2:
                count = len(raw_data) // 2
                fmt = f"<{count}h"
                samples = struct.unpack(fmt, raw_data)
                
                left = samples[0::2]
                right = samples[1::2]
                
                if left == right:
                    with wave.open(str(temp_path), 'wb') as out:
                        out.setnchannels(1)
                        out.setsampwidth(width)
                        out.setframerate(rate)
                        out.writeframes(struct.pack(f"<{len(left)}h", *left))
                    modified = True
                    
        if modified:
            os.replace(temp_path, file_path)
            return True
            
    except Exception:
        pass
    return False

def analyze_timbre(file_path):
    tags = []
    try:
        with wave.open(str(file_path), 'rb') as wav:
            channels = wav.getnchannels()
            width = wav.getsampwidth()
            rate = wav.getframerate()
            frames = wav.getnframes()
            
            if width != 2: return []
            
            read_len = min(rate, frames) 
            start_pos = max(0, (frames // 2) - (read_len // 2))
            
            wav.setpos(start_pos)
            raw_data = wav.readframes(read_len)
            
            count = len(raw_data) // 2
            fmt = f"<{count}h"
            samples = struct.unpack(fmt, raw_data)
            
            if channels == 2:
                samples = samples[::2]
                
            zcr_count = 0
            if len(samples) > 1:
                prev = samples[0]
                for s in samples[1:]:
                    if (s >= 0 and prev < 0) or (s < 0 and prev >= 0):
                        zcr_count += 1
                    prev = s
            
            duration_read = len(samples) / rate
            zcr_rate = zcr_count / duration_read if duration_read > 0 else 0
            
            sum_sq = sum(float(s)*float(s) for s in samples)
            rms_val = math.sqrt(sum_sq / len(samples)) if len(samples) > 0 else 0
            
            db = -96.0
            if rms_val > 0:
                db = 20 * math.log10(rms_val / 32768.0)
                
            if zcr_rate > 1500: tags.append("Bright")
            elif zcr_rate < 300: tags.append("Dark")
            
            if db > -12: tags.append("Heavy")
            elif db < -24: tags.append("Soft")
            
    except Exception:
        pass
    return tags

def get_duration_class(file_path):
    try:
        with wave.open(str(file_path), 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            duration = frames / float(rate)
            if duration < 2.0: return "One Shot", duration
            if duration >= 2.0 and duration < 45.0: return "Loop", duration 
            return "Track", duration
    except:
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
    return modality, tag

def process_archive(archive_path):
    create_time_machine_backup(archive_path)
    temp_dir = archive_path.parent / f"{archive_path.stem}_temp_unpack"
    temp_dir.mkdir(exist_ok=True)
    try:
        shutil.unpack_archive(str(archive_path), str(temp_dir))
        unpacked_files = []
        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                if not f.startswith('.'):
                    unpacked_files.append(Path(root) / f)
        success_count = 0
        for f in unpacked_files:
            res, msg = process_atom(f, backup=False) 
            if res == 1: success_count += 1
        shutil.rmtree(temp_dir)
        archive_path.unlink() 
        return (1, f"Archive/{archive_path.name}")
    except Exception:
        if temp_dir.exists(): shutil.rmtree(temp_dir)
        return (-1, f"Archive Fail")

def process_atom(src_path, backup=True):
    try:
        p = Path(src_path)
        if not p.exists(): return (0, "Skipped")
        
        orig_path = str(p)
        
        if backup: create_time_machine_backup(p)
        if p.suffix.lower() in ARCHIVE_EXTS: return process_archive(p)

        context_tags = get_semantic_context(p)
        modality, tag = classify(p)
        
        dest_base = DEST_ROOT / "Assets" / modality / tag 
        
        is_audio = p.suffix.lower() in AUDIO_EXTS
        bpm, key_sig, artist, title = get_smart_metadata(p.name)
        
        is_music = False
        if is_audio and artist and title: is_music = True
        
        if is_music:
            clean_artist = clean_filename(artist)
            clean_album = "Singles" 
            dest_base = DEST_ROOT / "Music" / clean_artist / clean_album
            dest_name = f"{clean_filename(title)}.wav"
        else:
             clean_stem = clean_filename(p.stem)
             dest_name = f"{clean_stem}.wav" if is_audio else clean_filename(p.name)
             
        dest_base.mkdir(parents=True, exist_ok=True)
        dest_path = dest_base / dest_name
        
        if dest_path.exists():
            ts = int(time.time_ns())
            base_ext = '.wav' if is_audio else p.suffix
            dest_name = f"{clean_filename(p.stem)}_{ts}{base_ext}"
            dest_path = dest_base / dest_name

        action_log = "INGEST"
        
        if is_audio:
            cmd = ["afconvert"] + AF_ARGS + [str(p), str(dest_path)]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                action_log = "CONVERTED"
            except:
                shutil.copy2(str(p), str(dest_path))
                action_log = "COPIED"
            
            if dest_path.exists() and dest_path.stat().st_size > 0:
                was_polished = False
                if not is_music: 
                    was_polished = polish_audio(dest_path)
                    if was_polished: action_log += "+POLISHED"
                
                dur_class, dur_sec = get_duration_class(dest_path)
                
                if not is_music and dur_sec > 60.0:
                    new_base = DEST_ROOT / "Music" / "Unknown_Artist" / "Singles"
                    new_base.mkdir(parents=True, exist_ok=True)
                    new_dest = new_base / dest_path.name
                    os.rename(dest_path, new_dest)
                    dest_path = new_dest
                    dur_class = "Track"
                    action_log += "+REROUTED"
                    
                timbre_tags = analyze_timbre(dest_path)
                
                set_xattr(dest_path, "com.apple.metadata:kMDItemAuthors", "Audio Unitor AI")
                if artist: set_xattr(dest_path, "com.apple.metadata:kMDItemAuthors", artist)
                if title: set_xattr(dest_path, "com.apple.metadata:kMDItemTitle", title)
                    
                set_xattr(dest_path, "com.apple.metadata:kMDItemMusicalGenre", tag)
                if bpm: set_xattr(dest_path, "com.apple.metadata:kMDItemTempo", bpm)
                if key_sig: set_xattr(dest_path, "com.apple.metadata:kMDItemKeySignature", key_sig)
                
                all_keywords = context_tags + [dur_class] + timbre_tags
                if all_keywords:
                    kw_str = ",".join(all_keywords)
                    set_xattr(dest_path, "com.apple.metadata:kMDItemKeywords", kw_str)
                
                desc = f"{dur_class} in {tag} ({', '.join(timbre_tags)})."
                set_xattr(dest_path, "com.apple.metadata:kMDItemDescription", desc)

        else:
             if p.is_dir(): shutil.copytree(str(p), str(dest_path), dirs_exist_ok=True)
             else: shutil.copy2(str(p), str(dest_path))

        if dest_path.exists():
            # MEMORY CORE: LOG PROVENANCE
            final_hash = fast_hash(dest_path)
            log_provenance(action_log, orig_path, dest_path, final_hash)
            
            if p.is_dir(): shutil.rmtree(str(p))
            else: p.unlink()
            return (1, f"{tag}/{dest_path.name}")
        else:
             return (-1, f"Transfer Failed: {p.name}")

    except Exception as e:
        return (-1, f"Error {src_path}")

def run_singularity(source_dir):
    print(f"{BOLD}{CYAN}CORE > 🌌 THE SINGULARITY: MEMORY CORE ACTIVE{RESET}")
    print(f"CORE > Source:  {source_dir}")
    print(f"CORE > Dest:    {DEST_ROOT}")
    files = []
    for root, dirs, filenames in os.walk(source_dir):
        if str(Path(root).resolve()).startswith(str(DEST_ROOT.resolve())): continue
        if str(Path(root).resolve()).startswith(str(TIME_MACHINE_ROOT.resolve())): continue
        for f in filenames:
            if not f.startswith('.'): files.append(Path(root) / f)
                
    print(f"CORE > Engaging Singularity Engine on {len(files)} items...")
    
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
                if errors < 10: print(f"CORE > {RED}Error: {msg}{RESET}")
            if (i+1) % 100 == 0: print(f"CORE > ...processed {i+1}...", end='\r')
                
    duration = time.time() - start_t
    print(f"\n{GREEN}CORE > ✨ SINGULARITY COMPLETE ({duration:.2f}s){RESET}")
    print(f"CORE > Processed: {count} | Errors: {errors}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_singularity.py <source_dir>")
    else:
        run_singularity(sys.argv[1])
