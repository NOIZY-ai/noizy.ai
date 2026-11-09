import os
import sys
import sqlite3
import hashlib
import time
import mmap
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")
# Index everything as requested ("FIND EVERYTHING")
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
    c.execute("""CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        filename TEXT,
        extension TEXT,
        size INTEGER,
        hash TEXT,
        volume TEXT,
        indexed_at TEXT
    )""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_hash ON files(hash)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_volume ON files(volume)""")
    c.execute("""CREATE INDEX IF NOT EXISTS idx_ext ON files(extension)""")

def fast_sha256(path: Path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            if path.stat().st_size == 0:
                return h.hexdigest()
            # 1GB limit for mmap to avoid memory issues on huge files
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

def index_file(fpath, vol_name):
    try:
        path_obj = Path(fpath)
        stat = path_obj.stat()
        size = stat.st_size
        ext = path_obj.suffix.lower()
        file_hash = fast_sha256(path_obj)
        
        return {
            "path": str(fpath),
            "filename": path_obj.name,
            "extension": ext,
            "size": size,
            "hash": file_hash,
            "volume": vol_name,
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

    print(f"      Found {len(files_to_process)} candidates. Hashing...")
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
        INSERT OR REPLACE INTO files (path, filename, extension, size, hash, volume, indexed_at)
        VALUES (:path, :filename, :extension, :size, :hash, :volume, :indexed_at)
    """, batch)
    conn.commit()

def run_turbo_index(target_vol=None):
    print(f"{BOLD}{CYAN}🚀 TURBO-SUPER-SONIC ENGINE INITIALIZED{RESET}")
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
    print(f"\n{GREEN}✨ TURBO INDEX COMPLETE{RESET}")
    print(f"   Total Files: {total_indexed}")
    print(f"   Time: {duration:.2f}s") # Fixed variable name

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        run_turbo_index(target)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted. Database is safe.")
