import os
import json
import time
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
MAP_FILE = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/volume_map.json")
HTML_MAP = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/volume_map.html")

# Categories
TYPES = {
    'Audio': {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg'},
    'Visual': {'.png', '.jpg', '.jpeg', '.psd', '.ai', '.svg', '.mov', '.mp4'},
    'Project': {'.als', '.logicx', '.ptx', '.cpr', '.flp', '.asd'}
}

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

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
                        
            # Hotspot Threshold
            if has_items:
                # If significant collection, log it
                total = sum(counts.values())
                if total > 20: # Start small to catch more
                    hotspots.append({
                        "path": root,
                        "counts": counts,
                        "total": total
                    })
    except PermissionError:
        pass
        
    return hotspots

def generate_html_map(hotspots):
    # Sort by density
    sorted_spots = sorted(hotspots, key=lambda x: x['total'], reverse=True)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SYSTEM CARTOGRAPHY</title>
        <link rel="stylesheet" href="../../nexus.css">
        <style>
             /* Map-specific overrides */
             body { padding: 20px; background: transparent; }
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
             .hotspot:hover { border-color: var(--main); background: rgba(0, 255, 157, 0.1); }
             .path { color: #fff; font-size: 0.9em; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max_width: 70%; }
             .stats { display: flex; gap: 15px; font-size: 0.8em; }
             .audio { color: #00ffff; }
             .visual { color: #ff00ff; }
             .project { color: #ffff00; }
        </style>
    </head>
    <body>
        <div class="flex-between mb-10">
            <h2 class="mt-0 text-main">DENSITY CLUSTERS</h2>
            <div class="text-small text-dim">TOP 500 HOTSPOTS</div>
        </div>
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
    
    with open(HTML_MAP, 'w') as f:
        f.write(html)
    print(f"CORE > 🗺️  Map Generated: {HTML_MAP}")

def run_cartography(target_dir=None, use_db=False):
    print(f"{BOLD}CORE > 🗺️  MAPPING THE UNIVERSE (DENSITY SCANNING)...{RESET}")
    start = time.time()
    
    all_hotspots = []
    
    if use_db:
        # INSTANT MAP MODE
        print(f"CORE > 🚀 INSTANT MODE: Reading from Universe DB...")
        db_path = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db"
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            # 1. Get all file paths
            c.execute("SELECT path, tags FROM files") # Getting tags too for colored map later?
            rows = c.fetchall()
            conn.close()
            
            # 2. Process in memory
            # Map: Folder -> Counts
            density_map = {} # path -> {audio:0, visual:0, project:0}
            
            for r in rows:
                p = Path(r[0])
                folder = str(p.parent)
                ext = p.suffix.lower()
                
                if folder not in density_map:
                    density_map[folder] = {'Audio':0, 'Visual':0, 'Project':0}
                    
                if ext in {'.wav','.aif','.mp3','.flac','.ogg'}: density_map[folder]['Audio'] += 1
                elif ext in {'.png','.jpg','.psd','.mov','.mp4'}: density_map[folder]['Visual'] += 1
                elif ext in {'.als','.logicx','.ptx','.cpr'}: density_map[folder]['Project'] += 1
            
            # 3. Filter Hotspots
            for folder, counts in density_map.items():
                total = sum(counts.values())
                if total > 5: # Threshold
                    # Determine primary type
                    primary = max(counts, key=counts.get)
                    all_hotspots.append({
                        "path": folder,
                        "total": total, # FIXED: Changed from 'count' to 'total'
                        "type": primary, # 'audio', 'visual', 'project'
                        "counts": counts # FIXED: Changed from 'details' to 'counts'
                    })
            print(f"CORE > ✅ DB Scan Complete. Found {len(all_hotspots)} clusters.")
            
        except Exception as e:
            print(f"CORE > ❌ DB Error: {e}")
            return

    elif target_dir:
         print(f"CORE > 🎯 Targeted Map: {target_dir}")
         all_hotspots.extend(scan_folder_density(target_dir))
    else:
        # ORIGINAL SLOW MODE
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
                    print(f"CORE > ✅ {vol_name}: Found {len(spots)} density clusters")
                except Exception as e:
                    print(f"CORE > ❌ {vol_name}: Failed ({e})")

    # Generate Outputs
    generate_html_map(all_hotspots)
    
    duration = time.time() - start
    print(f"{GREEN}CORE > ✨ CARTOGRAPHY COMPLETE ({duration:.2f}s){RESET}")

if __name__ == "__main__":
    import sys
    import sqlite3 # Need this import locally if not at top
    
    use_db = False
    target = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--db":
            use_db = True
        else:
            target = sys.argv[1]
            
    run_cartography(target, use_db)


