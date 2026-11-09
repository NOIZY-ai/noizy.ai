import os
import json
import time
import argparse
from datetime import datetime
import sys

# GENIUS LINK: Add local path to allow MemCell import
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gabriel.memcell_engine import MemCell, OverlapEngine, Evidence

class Fishnet:
    def __init__(self):
        self.mem_engine = OverlapEngine() # Link to Brain
        self.manifest = {
            "timestamp": datetime.now().isoformat(),
            "volumes": {},
            "total_files": 0,
            "total_size_bytes": 0,
            "errors": []
        }
        self.ignore_list = {
            '.DS_Store', '.Trash', '.Trashes', 'Spotlight-V100', '.fseventsd', 
            'System Volume Information', '$RECYCLE.BIN', 'Thumbs.db'
        }
        self.ignore_ext = {'.tmp', '.lock'}

    def is_ignored(self, name):
        if name in self.ignore_list: return True
        if name.startswith("._"): return True
        _, ext = os.path.splitext(name)
        if ext.lower() in self.ignore_ext: return True
        return False

    def scan_path(self, root_path, volume_name):
        print(f"Scanning Volume: {volume_name} ({root_path})...")
        files_list = []
        vol_size = 0
        vol_count = 0
        
        try:
            for root, dirs, files in os.walk(root_path, topdown=True):
                # Filter directories in-place
                dirs[:] = [d for d in dirs if not self.is_ignored(d)]
                
                for f in files:
                    if self.is_ignored(f): continue
                    
                    try:
                        full_path = os.path.join(root, f)
                        stats = os.stat(full_path)
                        
                        entry = {
                            "p": full_path, # Path
                            "s": stats.st_size, # Size
                            "m": int(stats.st_mtime) # Modified
                        }
                        
                        files_list.append(entry)
                        vol_size += stats.st_size
                        vol_count += 1
                        
                    except Exception as e:
                        self.manifest['errors'].append(f"Error reading {f}: {str(e)}")
                        
        except Exception as e:
            self.manifest['errors'].append(f"Critical error scanning {root_path}: {str(e)}")
            return

        self.manifest['volumes'][volume_name] = {
            "root": root_path,
            "files_count": vol_count,
            "size_bytes": vol_size,
            "files": files_list
        }
        
        self.manifest['total_files'] += vol_count
        self.manifest['total_size_bytes'] += vol_size
        print(f" >> Finished {volume_name}: {vol_count} files ({vol_size/1024/1024:.2f} MB)")

    def run(self, mock=False):
        # 1. Scan User Home (Targeted)
        self.scan_path("/Users/m2ultra/NOIZYLAB", "NOIZYLAB_MAIN")
        
        # 2. Scan External Volumes
        if os.path.exists("/Volumes"):
            for vol in os.listdir("/Volumes"):
                if vol.startswith("."): continue # fast skip
                path = os.path.join("/Volumes", vol)
                if os.path.isdir(path) and not os.path.islink(path):
                    self.scan_path(path, vol)

        # 3. Save Manifest
        if not mock:
            out_path = "FISHNET_MANIFEST.json"
            with open(out_path, 'w') as f:
                json.dump(self.manifest, f, indent=2)
            print(f"\n[FISHNET COMPLETE] Manifest saved to {os.path.abspath(out_path)}")
            print(f"Total Files: {self.manifest['total_files']}")
            print(f"Total Size: {self.manifest['total_size_bytes']/1024/1024/1024:.2f} GB")
            
            # GENIUS: NEURAL INJECTION
            self.feed_memory()
        else:
            print("\n[DRY RUN COMPLETE] No manifest saved.")

    def feed_memory(self):
        """Injects volume stats into MemCell via Overlap Engine."""
        print(">> HYPER-LINK: Injecting Scan Data into MemCell...")
        
        # 1. Volume Stats MemCell
        ev = Evidence(source_id="fishnet_scanner", locator="FISHNET_MANIFEST.json", quote="Global Scan Complete")
        
        claim = f"Fishnet Indexed {self.manifest['total_files']} files ({self.manifest['total_size_bytes']/1024/1024/1024:.2f} GB) across {len(self.manifest['volumes'])} volumes."
        
        cell = MemCell(
            id=f"fishnet_scan_{int(time.time())}",
            type="DATA_SNAPSHOT",
            claim=claim,
            evidence=[ev],
            confidence=1.0
        )
        self.mem_engine.ingest(cell)
        print(f"   + Upserted Memory: {cell.id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry", action="store_true", help="Run without saving")
    args = parser.parse_args()
    
    net = Fishnet()
    net.run(mock=args.dry)
