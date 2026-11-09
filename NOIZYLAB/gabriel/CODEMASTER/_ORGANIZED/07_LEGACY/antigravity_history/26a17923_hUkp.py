# ==============================================================================
# 🦅 GABRIEL ALLEGIANCE (SYSTEM LEADER)
# ==============================================================================
# This script operates under the command of GABRIEL.
# PROTOCOL: GORUNFREE | LATENCY: ZERO | TRUTH: ONE
# ==============================================================================

import os
import json
import time
import sys
import sqlite3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import turbo_config as cfg
    import turbo_gabriel
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    import turbo_gabriel
    from turbo_memcell import MemCell

# Configuration
MAP_FILE = cfg.DATABASE_DIR / "volume_map.json"
HTML_MAP = cfg.DATABASE_DIR / "volume_map.html"

# Categories
TYPES = {
    'Audio': {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg'},
    'Visual': {'.png', '.jpg', '.jpeg', '.psd', '.ai', '.svg', '.mov', '.mp4'},
    'Project': {'.als', '.logicx', '.ptx', '.cpr', '.flp', '.asd'}
}

def scan_folder_density(vol_path):
    hotspots = []
    try:
        for root, dirs, files in os.walk(vol_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            counts = {'Audio': 0, 'Visual': 0, 'Project': 0}
            has_items = False
            
            for f in files:
                ext = Path(f).suffix.lower()
                for cat, extensions in TYPES.items():
                    if ext in extensions:
                        counts[cat] += 1
                        has_items = True
            
            if has_items:
                total = sum(counts.values())
                if total > 20: 
                    hotspots.append({
                        "path": root,
                        "counts": counts,
                        "total": total
                    })
    except PermissionError: pass
    return hotspots

def generate_html_map(hotspots):
    sorted_spots = sorted(hotspots, key=lambda x: x['total'], reverse=True)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SYSTEM CARTOGRAPHY</title>
        <style>
             body { padding: 20px; background: #050505; color: #fff; font-family: sans-serif; }
             .hotspot { 
                 border: 1px solid #333; 
                 margin-bottom: 5px; 
                 padding: 8px; 
                 background: rgba(10,10,10,0.8); 
                 display: flex; 
                 justify-content: space-between; 
                 align-items: center;
                 font-family: 'Courier New', monospace;
             }
             .hotspot:hover { border-color: #00ff9d; background: rgba(0, 255, 157, 0.1); }
             .path { color: #fff; font-size: 0.9em; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 70%; }
             .stats { display: flex; gap: 15px; font-size: 0.8em; }
             .audio { color: #00ffff; }
             .visual { color: #ff00ff; }
             .project { color: #ffff00; }
        </style>
    </head>
    <body>
        <h2>DENSITY CLUSTERS</h2>
    """
    
    for spot in sorted_spots[:500]: # Top 500 hotspots
        c = spot['counts']
        html += f"""
        <div class="hotspot">
            <div class="path" title="{spot['path']}">{spot['path'].replace('/Users/m2ultra', '~')}</div>
            <div class="stats">
                <span class="audio">A:{c['Audio']}</span>
                <span class="visual">V:{c['Visual']}</span>
                <span class="project">P:{c['Project']}</span>
            </div>
        </div>
        """
        
    html += "</body></html>"
    
    cfg.ensure_dirs([HTML_MAP.parent])
    with open(HTML_MAP, 'w') as f:
        f.write(html)
    cfg.system_log(f"Map Generated: {HTML_MAP}", "SUCCESS")

def run_cartography(target_dir=None, use_db=False):
    cfg.print_header("🗺️  CARTOGRAPHER", "MAPPING THE UNIVERSE")
    start = time.time()
    
    all_hotspots = []
    
    if use_db:
        cfg.system_log("INSTANT MODE: Reading from Universe DB...", "INFO")
        try:
            conn = sqlite3.connect(cfg.UNIVERSE_DB_PATH)
            c = conn.cursor()
            c.execute("SELECT path, tags FROM files") 
            rows = c.fetchall()
            conn.close()
            
            density_map = {} 
            for r in rows:
                p = Path(r[0])
                folder = str(p.parent)
                ext = p.suffix.lower()
                
                if folder not in density_map:
                    density_map[folder] = {'Audio':0, 'Visual':0, 'Project':0}
                    
                if ext in {'.wav','.aif','.mp3','.flac','.ogg'}: density_map[folder]['Audio'] += 1
                elif ext in {'.png','.jpg','.psd','.mov','.mp4'}: density_map[folder]['Visual'] += 1
                elif ext in {'.als','.logicx','.ptx','.cpr'}: density_map[folder]['Project'] += 1
            
            for folder, counts in density_map.items():
                total = sum(counts.values())
                if total > 5: 
                    all_hotspots.append({
                        "path": folder,
                        "total": total,
                        "type": max(counts, key=counts.get),
                        "counts": counts
                    })
            cfg.system_log(f"DB Scan Complete. Found {len(all_hotspots)} clusters.", "SUCCESS")
            
        except Exception as e:
            cfg.system_log(f"DB Error: {e}", "ERROR")
            return

    elif target_dir:
         print(f"CORE > 🎯 Targeted Map: {target_dir}")
         all_hotspots.extend(scan_folder_density(target_dir))
    else:
        volumes_path = Path('/Volumes')
        volumes = [
            v for v in volumes_path.iterdir() 
            if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
        ]
    
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_vol = {executor.submit(scan_folder_density, str(vol)): vol.name for vol in volumes}
            for future in as_completed(future_to_vol):
                vol_name = future_to_vol[future]
                try:
                    spots = future.result()
                    all_hotspots.extend(spots)
                    cfg.system_log(f"{vol_name}: Found {len(spots)} density clusters", "SUCCESS")
                except Exception as e:
                    cfg.system_log(f"{vol_name}: Failed ({e})", "ERROR")

    generate_html_map(all_hotspots)
    
    duration = time.time() - start
    cfg.system_log(f"CARTOGRAPHY COMPLETE ({duration:.2f}s)", "SUCCESS")

if __name__ == "__main__":
    use_db = False
    target = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--db":
            use_db = True
        else:
            target = sys.argv[1]
            
    run_cartography(target, use_db)


