"""
FISHNET MEDIA SCANNER
Indexes ALL visual assets (Video + Image) across the Gabriel Universe.
"""

import sqlite3
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import logging

# CONFIG
DB_PATH = Path("NOIZYLAB_DB/visual_index.db")
VOLUMES_ROOT = Path("/Volumes")
SKIP_DIRS = {".Trashes", ".Spotlight-V100", "Time Machine Backups", "Backups.backupdb"}

# DEFINITIONS
VIDEO_EXTS = {'.mp4', '.mov', '.mkv', '.avi', '.webm', '.m4v'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
AUDIO_EXTS = {'.wav', '.mp3', '.aif', '.aiff', '.flac', '.ogg', '.m4a', '.mid', '.midi'}
DAW_EXTS = {'.als', '.logicx', '.ptx', '.flp'} 
FONT_EXTS = {'.ttf', '.otf', '.woff', '.woff2'}
MODEL_EXTS = {'.obj', '.fbx', '.blend', '.c4d', '.stl', '.gltf', '.glb'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("FISHNET")

class FishnetIndex:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Schema V2: Added media_type
        # Schema V3: No change needed, just new types in text column
        c.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                path TEXT PRIMARY KEY,
                filename TEXT,
                volume TEXT,
                size INTEGER,
                mtime REAL,
                media_type TEXT
            );
        ''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_filename ON assets(filename);')
        c.execute('CREATE INDEX IF NOT EXISTS idx_type ON assets(media_type);')
        conn.commit()
        conn.close()

    def scan_volume(self, vol_path: Path):
        """Scans a volume for Media Assets"""
        logger.info(f"🕸️ Casting Net: {vol_path.name}...")
        count = 0
        batch = []
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        for root, dirs, files in os.walk(vol_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            
            for file in files:
                ext = Path(file).suffix.lower()
                m_type = None
                
                if ext in VIDEO_EXTS:
                    m_type = 'video'
                elif ext in IMAGE_EXTS:
                    m_type = 'image'
                elif ext in AUDIO_EXTS:
                    m_type = 'audio'
                elif ext in DAW_EXTS:
                    m_type = 'project'
                elif ext in FONT_EXTS:
                    m_type = 'font'
                elif ext in MODEL_EXTS:
                    m_type = 'model_3d'
                
                if m_type:
                    full_path = Path(root) / file
                    try:
                        stat = full_path.stat()
                        batch.append((
                            str(full_path),
                            file,
                            vol_path.name,
                            stat.st_size,
                            stat.st_mtime,
                            m_type
                        ))
                        count += 1
                    except:
                        continue
                        
                    if len(batch) >= 1000:
                        c.executemany("INSERT OR REPLACE INTO assets VALUES (?,?,?,?,?,?)", batch)
                        conn.commit()
                        batch = []
                        print(f"  [{vol_path.name}] Caught {count} items...", end='\r')

        if batch:
            c.executemany("INSERT OR REPLACE INTO assets VALUES (?,?,?,?,?,?)", batch)
            conn.commit()
        
        conn.close()
        logger.info(f"✅ {vol_path.name} Haul: {count} Items")
        return count

    def scan_network(self, watch_mode=False):
        """Main entry point for scanning all targets."""
        print(f"\n🚀 LAUNCHING FISHNET GLOBAL SCAN (Watch Mode: {watch_mode})")
        
        while True:
            # The following lines refer to methods not present in the original class.
            # They are kept as per instruction to make the change faithfully.
            # conn = self.get_db_connection() 
            # if not conn: return
            # self.setup_db(conn)
            # conn.close() # Close for now, workers open their own or we batch insert? 
            # Actually scan_volume handles its own connection or passing data back?
            # scan_volume currently writes to DB? No, scan_volume returns loot list.
            
            # Re-detect volumes every loop in watch mode
            targets = [Path(f"/Volumes/{v}") for v in os.listdir("/Volumes") if not v.startswith('.')]
            if Path(f"/Users/{os.environ.get('USER', 'm2ultra')}").exists():
                 targets.append(Path(f"/Users/{os.environ.get('USER', 'm2ultra')}"))
                 
            # PC Bridge Check
            pc_bridge = Path(f"/Users/{os.environ.get('USER', 'm2ultra')}/Mounts/PC_Bridge")
            if pc_bridge.exists():
                logger.info("✅ HP-OMEN DETECTED (PC_Bridge)")
                targets.append(pc_bridge)
                
            logger.info(f"Detected {len(targets)} Fishing Grounds: {[t.name for t in targets]}")
            
            # DYNAMIC LOAD BALANCING
            worker_count = len(targets) if targets else 1
            if watch_mode: logger.info("🌊 UNIVERSE FLOW: Scanning...")
            
            total_loot = 0
            with ThreadPoolExecutor(max_workers=worker_count) as executor:
                results = executor.map(self.scan_volume, targets)
                total_loot = sum(results)
                
            logger.info(f"🏁 SCAN COMPLETE. Total Loot: {total_loot} Items.")
            
            if not watch_mode:
                break
                
            logger.info("💤 Flowing... (Sleeping 60s)")
            time.sleep(60)

if __name__ == "__main__":
    watch = False
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch = True
    
    scanner = FishnetIndex()
    scanner.scan_network(watch_mode=watch)
