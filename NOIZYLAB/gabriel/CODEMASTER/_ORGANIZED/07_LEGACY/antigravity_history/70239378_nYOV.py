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

    def scan_universe(self):
        """Parallel Scan of All Volumes + HP-OMEN"""
        logger.info("🚀 LAUNCHING FISHNET GLOBAL SCAN")
        start = time.time()
        
        # 1. Standard Volumes
        targets = [p for p in VOLUMES_ROOT.iterdir() if p.is_dir() and not p.name.startswith('.')]
        
        # 2. HP-OMEN Targeting
        pc_bridge = Path(os.path.expanduser("~/Mounts/PC_Bridge"))
        if pc_bridge.exists() and pc_bridge not in targets:
            targets.append(pc_bridge)
            logger.info("✅ HP-OMEN DETECTED (PC_Bridge)")
        elif not pc_bridge.exists():
            logger.warning("⚠️ HP-OMEN OFFLINE (PC_Bridge not found). Trying mount...")
            # Optional: auto-trigger mount here if python permissions allow, 
            # but usually better handled by bridge script.
            
        logger.info(f"Detected {len(targets)} Fishing Grounds: {[t.name for t in targets]}")
        
        total_loot = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = executor.map(self.scan_volume, targets)
            total_loot = sum(results)

        duration = time.time() - start
        logger.info(f"🏁 FISHNET COMPLETE in {duration:.2f}s. Total Catch: {total_loot}")

if __name__ == "__main__":
    scanner = FishnetIndex()
    scanner.scan_universe()
