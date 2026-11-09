"""
VISUAL VAULT SCANNER
Indexes all .png assets across the Gabriel Universe (External Volumes)
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("VISUAL_SCAN")

class VisualIndex:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS images (
                path TEXT PRIMARY KEY,
                filename TEXT,
                volume TEXT,
                size INTEGER,
                mtime REAL
            );
        ''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_filename ON images(filename);')
        c.execute('CREATE INDEX IF NOT EXISTS idx_volume ON images(volume);')
        conn.commit()
        conn.close()

    def scan_volume(self, vol_path: Path):
        """Scans a single volume for PNGs"""
        logger.info(f"Scanning Volume: {vol_path.name}...")
        count = 0
        batch = []
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        for root, dirs, files in os.walk(vol_path):
            # Skip system dirs
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
            
            for file in files:
                if file.lower().endswith('.png'):
                    full_path = Path(root) / file
                    try:
                        stat = full_path.stat()
                        batch.append((
                            str(full_path),
                            file,
                            vol_path.name,
                            stat.st_size,
                            stat.st_mtime
                        ))
                        count += 1
                    except:
                        continue
                        
                    if len(batch) >= 1000:
                        c.executemany("INSERT OR REPLACE INTO images VALUES (?,?,?,?,?)", batch)
                        conn.commit()
                        batch = []
                        print(f"  [{vol_path.name}] Found {count} images...", end='\r')

        if batch:
            c.executemany("INSERT OR REPLACE INTO images VALUES (?,?,?,?,?)", batch)
            conn.commit()
        
        conn.close()
        logger.info(f"✅ {vol_path.name} Complete. Total: {count}")
        return count

    def scan_universe(self):
        """Scans all available volumes in parallel"""
        logger.info("🚀 STARTING GLOBAL VISUAL SCAN")
        start = time.time()
        
        # Identify Targets
        targets = [p for p in VOLUMES_ROOT.iterdir() if p.is_dir() and not p.name.startswith('.')]
        logger.info(f"Detected {len(targets)} Volumes: {[t.name for t in targets]}")
        
        total_images = 0
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(self.scan_volume, targets)
            total_images = sum(results)

        duration = time.time() - start
        logger.info(f"🏁 SCAN COMPLETE in {duration:.2f}s. Total Images: {total_images}")

if __name__ == "__main__":
    scanner = VisualIndex()
    scanner.scan_universe()
