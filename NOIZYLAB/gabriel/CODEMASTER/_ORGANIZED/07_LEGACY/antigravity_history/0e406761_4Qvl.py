#!/usr/bin/env python3
import os
import sys
import sqlite3
import hashlib
import re
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

try:
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
DB_PATH = cfg.UNIVERSE_DB_PATH
cfg.ensure_dirs([DB_PATH.parent])

THREADS = max(4, (os.cpu_count() or 4) * 2)

# Intelligence Heuristics (Neural Core)
PATTERNS = {
    # Musical Metadata
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), 
    
    # Drums & Percussion
    "type_kick": re.compile(r"kick|bd|bassdrum|stomp|808_kick", re.IGNORECASE),
    "type_snare": re.compile(r"snare|sd|rim|clap|snap", re.IGNORECASE),
    "type_hat": re.compile(r"hat|hh|cymbal|ride|crash|shaker|tamb", re.IGNORECASE),
    "type_tom": re.compile(r"tom|timpani|cong|bongo", re.IGNORECASE),
    "type_perc": re.compile(r"perc|hit|impact|metal|wood|click", re.IGNORECASE),
    "type_loop": re.compile(r"loop|drumloop|break|fill", re.IGNORECASE),
    
    # Instruments
    "type_bass": re.compile(r"bass|sub|808|log|reese", re.IGNORECASE),
    "type_synth": re.compile(r"synth|lead|pad|pluck|arp|saw|square", re.IGNORECASE),
    "type_guitar": re.compile(r"guitar|gtr|acoustic|electric|dist", re.IGNORECASE),
    "type_piano": re.compile(r"piano|keys|rhodes|organ", re.IGNORECASE),
    "type_orchestra": re.compile(r"viol|cello|string|brass|horn|trumpet", re.IGNORECASE),
    
    # Vocals
    "type_vocal": re.compile(r"vocal|vox|acapella|chant|choir|adlib|hook|verse", re.IGNORECASE),
    "type_speech": re.compile(r"speech|talk|spoken|podcast", re.IGNORECASE),
    
    # FX & Foley
    "type_fx": re.compile(r"fx|sfx|noise|riser|impact|glass|ping|tink|blow|morse|bottle|pop|purr|sosumi|hero|funk|frog|laser|sweep|trans", re.IGNORECASE),
    "type_atmos": re.compile(r"atmos|texture|drone|ambi|bg|bed", re.IGNORECASE),
    
    # Moods (Experimental)
    "mood_dark": re.compile(r"dark|evil|horror|scary|grim", re.IGNORECASE),
    "mood_happy": re.compile(r"happy|uplifting|major|bright", re.IGNORECASE),
    "mood_aggro": re.compile(r"aggro|hard|punchy|distorted", re.IGNORECASE),
    "mood_chill": re.compile(r"chill|mellow|smooth|lofi|jazz", re.IGNORECASE),
    
    # Business/Visual
    "type_logo": re.compile(r"logo|brand|guideline|brief|contract", re.IGNORECASE),
    "type_doc": re.compile(r"invoice|receipt|tax|legal|license", re.IGNORECASE)
}

def db_connect(db_path: Path):
    cfg.ensure_dirs([db_path.parent])
    conn = sqlite3.connect(str(db_path), isolation_level=None, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("PRAGMA mmap_size=134217728")
    return conn

def db_init(conn):
    c = conn.cursor()
    # Neural Schema Upgrade: Added bpm, key, tags
    c.execute("""CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        filename TEXT,
        extension TEXT,
        size INTEGER,
        hash TEXT,
        volume TEXT,
        bpm INTEGER,
        key TEXT,
        tags TEXT,
        indexed_at TEXT
    )""")
    # Run migration if needed (Handle existing tables)
    try: c.execute("ALTER TABLE files ADD COLUMN bpm INTEGER")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE files ADD COLUMN key TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE files ADD COLUMN tags TEXT")
    except sqlite3.OperationalError: pass

    # Indexes
    c.execute("""CREATE INDEX IF NOT EXISTS idx_hash ON files(hash)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_volume ON files(volume)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_tags ON files(tags)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_bpm ON files(bpm)""")


def fast_sha256(path: Path):
    """
    DNA Scanner: Smart Partial Hashing for Jumbogrames Speed.
    - Small files (< 1MB): Full Hash.
    - Large files: Hash (Head + Tail + Size).
    """
    h = hashlib.sha256()
    try:
        size = path.stat().st_size
        if size == 0:
            return h.hexdigest()
        
        # DNA Optimization: Partial Hash for large files
        if size > 1024 * 1024: # 1MB cutoff
            with open(path, "rb") as f:
                # Head
                h.update(f.read(65536))
                # Tail
                f.seek(max(0, size - 65536))
                h.update(f.read(65536))
            # Mix in size to avoid collision on partial content match
            h.update(str(size).encode())
        else:
            # Full Hash for small files (Fast enough)
            with open(path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
                    
    except (ValueError, OSError):
        return None
    return h.hexdigest()

def get_smart_tags(filename):
    f_lower = filename.lower()
    bpm = None
    key = None
    tags = []
    
    # BPM
    bpm_match = PATTERNS["bpm"].search(f_lower)
    if bpm_match:
        bpm = int(bpm_match.group(1))
        
    # Key
    key_match = PATTERNS["key"].search(filename)
    if key_match:
        key = key_match.group(1)
        
    # Types
    for p_name, p_regex in PATTERNS.items():
        if p_name.startswith("type_") and p_regex.search(f_lower):
            t_name = p_name.replace("type_", "")
            tags.append(t_name)
    # Moods
    for p_name, p_regex in PATTERNS.items():
        if p_name.startswith("mood_") and p_regex.search(f_lower):
            t_name = p_name.replace("mood_", "") + "_mood"
            tags.append(t_name)
            
    return bpm, key, ",".join(tags) if tags else None

def index_file(fpath, vol_name):
    try:
        path_obj = Path(fpath)
        if path_obj.name.startswith('.'): return None

        stat = path_obj.stat()
        size = stat.st_size
        ext = path_obj.suffix.lower()
        file_hash = fast_sha256(path_obj)
        
        # Neural Tagging
        bpm, key, tags = get_smart_tags(path_obj.name)
        
        return {
            "path": str(fpath),
            "filename": path_obj.name,
            "extension": ext,
            "size": size,
            "hash": file_hash,
            "volume": vol_name,
            "bpm": bpm,
            "key": key,
            "tags": tags,
            "indexed_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception:
        return None

def scan_volume(vol_path: Path):
    cfg.system_log(f"Scanning {vol_path.name}...", "INFO")
    files_to_index = []
    for root, dirs, files in os.walk(vol_path):
        # Optimization: Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for f in files:
            if not f.startswith('.'):
                 files_to_index.append(Path(root) / f)
                 
    cfg.system_log(f"Found {len(files_to_index)} candidates in {vol_path.name}.", "INFO")
    
    results = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        # Pass volume name clearly
        future_to_file = {executor.submit(index_file, f, vol_path.name): f for f in files_to_index}
        
        completed = 0
        for future in as_completed(future_to_file):
            res = future.result()
            if res:
                results.append(res)
            completed += 1
            if completed % 1000 == 0:
                print(f"CORE >    Indexed {completed}/{len(files_to_index)}...", end='\r')
                
    cfg.system_log(f"{vol_path.name}: Processed {len(results)} valid files.", "SUCCESS")
    return results

def bulk_insert(conn, batch):
    c = conn.cursor()
    c.executemany("""
        INSERT OR REPLACE INTO files (path, filename, extension, size, hash, volume, bpm, key, tags, indexed_at)
        VALUES (:path, :filename, :extension, :size, :hash, :volume, :bpm, :key, :tags, :indexed_at)
    """, batch)
    conn.commit()

def run_turbo_index(target=None):
    cfg.print_header("📡 INDEXER PROTOCOL", "NEURAL SCANNING ONLINE")
    print(f"CORE > Database: {DB_PATH}")
    
    # Initialize Conciousness
    try:
        brain = MemCell()
        brain.log_event(brain.covenant_id, "INDEX_START", f"Indexer Protocol Initiated", vibe=80, author="INDEXER")
    except: pass
    
    conn = db_connect(DB_PATH)
    db_init(conn)
    start_time = time.time()
    
    all_results = []
    
    if target:
        vol_path = Path(target)
        if vol_path.exists():
            print(f"CORE > 🎯 Targeted Scan: {vol_path}")
            all_results.extend(scan_volume(vol_path))
    else:
        # Auto-detect volumes
        volumes_dir = Path('/Volumes')
        if volumes_dir.exists():
            volumes = [v for v in volumes_dir.iterdir() if v.is_dir() and not v.name.startswith('.')]
            if Path(cfg.STAGING_AREA).exists(): volumes.append(Path(cfg.STAGING_AREA)) # Add Staging
            
            for vol in volumes:
                if vol.name == 'M2Ultra' or vol.name.startswith('com.apple'): continue 
                all_results.extend(scan_volume(vol))
        
        # Also index local vault?
        local_vault = Path.home() / "Universal"
        if local_vault.exists():
             all_results.extend(scan_volume(local_vault))

    # Bulk Insert
    if all_results:
        cfg.system_log(f"Committing {len(all_results)} records to Universe DB...", "WARN")
        
        # Batching for massive inserts
        batch_size = 5000
        for i in range(0, len(all_results), batch_size):
            batch = all_results[i:i+batch_size]
            bulk_insert(conn, batch)
            print(f"CORE >    Committed batch {i // batch_size + 1}...", end='\r')
            
        cfg.system_log("Commit Complete.", "SUCCESS")
            
    conn.close()
    duration = time.time() - start_time
    
    # MemCell Update
    try:
        brain.log_event(brain.covenant_id, "INDEX_COMPLETE", f"Indexed {len(all_results)} files", vibe=100, author="INDEXER")
    except: pass
    
    cfg.system_log("NEURAL INDEX COMPLETE", "SUCCESS")
    print(f"CORE > Total Files: {len(all_results)}")
    print(f"CORE > Time: {duration:.2f}s")
    
if __name__ == "__main__":
    target_vol = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        run_turbo_index(target_vol)
    except KeyboardInterrupt:
        print(f"\n{cfg.RED}CORE > ⚠️ Interrupted. Database is safe.{cfg.RESET}")
