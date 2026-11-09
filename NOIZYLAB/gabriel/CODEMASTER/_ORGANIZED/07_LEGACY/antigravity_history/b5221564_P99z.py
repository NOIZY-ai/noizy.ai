import os
import sys
import sqlite3
import hashlib
import time
import mmap
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

# Intelligence Heuristics (Neural Core)
PATTERNS = {
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), 
    "type_kick": re.compile(r"kick|bd|bassdrum|stomp", re.IGNORECASE),
    "type_snare": re.compile(r"snare|sd|rim|clap", re.IGNORECASE),
    "type_hat": re.compile(r"hat|hh|cymbal|ride|crash", re.IGNORECASE),
    "type_bass": re.compile(r"bass|sub|808|log", re.IGNORECASE),
    "type_loop": re.compile(r"loop|drumloop|break", re.IGNORECASE),
    "type_vocal": re.compile(r"vocal|vox|acapella|chant", re.IGNORECASE),
    "type_fx": re.compile(r"fx|sfx|noise|riser|impact|glass|ping|tink|blow|morse|bottle|pop|purr|sosumi|hero|funk|frog", re.IGNORECASE),
    "type_logo": re.compile(r"logo|brand|guideline|brief|contract", re.IGNORECASE)
}

# Index everything ("FIND EVERYTHING")
EXTENSIONS = {
    # Audio
    '.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.m4a', '.wma', '.mid',
    # Visual
    '.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.psd', '.ai', '.svg', '.bmp', '.heic',
    # Video
    '.mov', '.mp4', '.m4v', '.avi', '.mkv', '.webm',
    # Projects/Docs
    '.als', '.logicx', '.ptx', '.cpr', '.flp', '.asd', '.pdf', '.txt', '.md', '.json', '.xml', '.zip', '.dmg', '.iso'
}

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

THREADS = max(4, os.cpu_count() or 4) * 2 

def db_connect(db_path: Path):
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True)
        
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
    c.execute("""CREATE INDEX IF NOT EXISTS idx_hash ON files(hash)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_volume ON files(volume)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_tags ON files(tags)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_bpm ON files(bpm)""")
    
    # Run migration if needed (Handle existing tables)
    try:
        c.execute("ALTER TABLE files ADD COLUMN bpm INTEGER")
        c.execute("ALTER TABLE files ADD COLUMN key TEXT")
        c.execute("ALTER TABLE files ADD COLUMN tags TEXT")
    except sqlite3.OperationalError:
        pass # Columns already exist

def fast_sha256(path: Path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            if path.stat().st_size == 0:
                return h.hexdigest()
            if path.stat().st_size > 1024 * 1024 * 1024:
                while chunk := f.read(1024 * 1024):
                    h.update(chunk)
            else:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    h.update(mm)
    except (ValueError, OSError):
        try:
            with open(path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
        except:
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
            
    return bpm, key, ",".join(tags) if tags else None

def index_file(fpath, vol_name):
    try:
        path_obj = Path(fpath)
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

def scan_volume(vol_path, conn):
    print(f"   Scanning {vol_path}...")
    vol_name = Path(vol_path).name
    files_to_process = []
    
    try:
        for root, dirs, files in os.walk(vol_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if Path(file).suffix.lower() in EXTENSIONS:
                    files_to_process.append(os.path.join(root, file))
    except PermissionError:
        print(f"      {RED}Permission Denied: {vol_path}{RESET}")
        return 0

    print(f"      Found {len(files_to_process)} candidates. Neural Indexing...")
    batch = []
    processed = 0
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_file = {executor.submit(index_file, f, vol_name): f for f in files_to_process}
        for future in as_completed(future_to_file):
            data = future.result()
            if data:
                batch.append(data)
            if len(batch) >= 1000:
                insert_batch(conn, batch)
                processed += len(batch)
                batch = []
                print(f"      Indexed {processed}/{len(files_to_process)}...", end='\r')
                
    if batch:
        insert_batch(conn, batch)
        processed += len(batch)
        
    print(f"      ✅ Indexed {processed} files in {vol_name}")
    return processed

def insert_batch(conn, batch):
    c = conn.cursor()
    c.executemany("""
        INSERT OR REPLACE INTO files (path, filename, extension, size, hash, volume, bpm, key, tags, indexed_at)
        VALUES (:path, :filename, :extension, :size, :hash, :volume, :bpm, :key, :tags, :indexed_at)
    """, batch)
    conn.commit()

def run_turbo_index(target_vol=None):
    print(f"{BOLD}{CYAN}🧠 NEURAL INDEXER INITIALIZED (Turbo+AI){RESET}")
    print(f"   Database: {DB_PATH}")
    
    conn = db_connect(DB_PATH)
    db_init(conn)
    start_time = time.time()
    total_indexed = 0
    
    if target_vol:
        vol_path = Path(target_vol)
        if vol_path.exists():
            total_indexed += scan_volume(vol_path, conn)
    else:
        volumes = [v for v in Path('/Volumes').iterdir() if v.is_dir() and not v.name.startswith('.')]
        for vol in volumes:
            if vol.name == 'M2Ultra': continue 
            total_indexed += scan_volume(vol, conn)
            
    conn.close()
    duration = time.time() - start_time
    print(f"\n{GREEN}✨ NEURAL INDEX COMPLETE{RESET}")
    print(f"   Total Files: {total_indexed}")
    print(f"   Time: {duration:.2f}s")
    
if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        run_turbo_index(target)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted. Database is safe.")

