import os
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
MAP_OUTPUT = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/system_map.json"
HTML_OUTPUT = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/system_map.html"

# Categories
TYPES = {
    'Audio': {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg'},
    'Visual': {'.png', '.jpg', '.jpeg', '.psd', '.ai', '.svg', '.mov', '.mp4'},
    'Project': {'.als', '.logicx', '.ptx', '.cpr', '.flp', '.asd'}
}

CYAN = '\033[96m'
GREEN = '\033[92m'
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
        <style>
            body { background-color: #050505; color: #00ff9d; font-family: 'Courier New', monospace; padding: 40px; }
            h1 { letter-spacing: 5px; text-shadow: 0 0 10px #00ff9d; }
            .hotspot { border: 1px solid #333; margin-bottom: 10px; padding: 10px; background: #0a0a0a; display: flex; justify-content: space-between; }
            .path { color: #fff; font-weight: bold; }
            .stats { display: flex; gap: 20px; }
            .audio { color: #00ffff; }
            .visual { color: #ff00ff; }
            .project { color: #ffff00; }
        </style>
    </head>
    <body>
        <h1>SYSTEM MAP (HIGH DENSITY CLUSTERS)</h1>
    """
    
    for spot in sorted_spots[:500]: # Top 500 hotspots to keep page loadable
        c = spot['counts']
        html += f"""
        <div class="hotspot">
            <div class="path">{spot['path']}</div>
            <div class="stats">
                <span class="audio">Audio: {c['Audio']}</span>
                <span class="visual">Visual: {c['Visual']}</span>
                <span class="project">Proj: {c['Project']}</span>
            </div>
        </div>
        """
        
    html += "</body></html>"
    
    with open(HTML_OUTPUT, 'w') as f:
        f.write(html)
    print(f"🗺️  Map Generated: {HTML_OUTPUT}")

def run_cartography():
    print(f"{BOLD}🗺️  MAPPING THE UNIVERSE (DENSITY SCANNING)...{RESET}")
    start = time.time()
    
    volumes_path = Path('/Volumes')
    volumes = [
        v for v in volumes_path.iterdir() 
        if v.is_dir() and v.name != 'M2Ultra' and not v.name.startswith('com.apple')
    ]
    
    all_hotspots = []
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_vol = {executor.submit(scan_folder_density, str(vol)): vol.name for vol in volumes}
        
        for future in as_completed(future_to_vol):
            vol_name = future_to_vol[future]
            try:
                spots = future.result()
                all_hotspots.extend(spots)
                print(f"   ✅ {vol_name}: Found {len(spots)} density clusters")
            except Exception as e:
                print(f"   ❌ {vol_name}: Failed ({e})")

    # Generate Outputs
    generate_html_map(all_hotspots)
    
    duration = time.time() - start
    print(f"{GREEN}✨ CARTOGRAPHY COMPLETE ({duration:.2f}s){RESET}")

if __name__ == "__main__":
    run_cartography()
