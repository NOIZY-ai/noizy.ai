import os
import sys
import json
import time
from datetime import datetime
from noizy_memcell import memory_core

# NOIZYLAB REPATRIATOR v2.0
# "The Collector" Module: Instrument & Plugin Indexing
# OPTIMIZED: MemCell Integration

# Signatures of "Valuable Instruments"
TARGET_EXTENSIONS = {
    # Plugins
    '.vst': 'VST Plugin',
    '.vst3': 'VST3 Plugin',
    '.component': 'Audio Unit (AU)',
    '.aaxplugin': 'Pro Tools AAX',
    
    # Sampler Formats
    '.nki': 'Kontakt Instrument',
    '.nicnt': 'Kontakt Library Info',
    '.exs': 'Logic Sampler',
    '.adg': 'Ableton Device',
    '.sfz': 'SFZ Instrument',
    '.sf2': 'SoundFont',
    '.fxp': 'VST Preset',
    
    # Project Files (to find where instruments are USED)
    '.logicx': 'Logic Project',
    '.als': 'Ableton Live Set',
    '.ptx': 'Pro Tools Session'
}

DEFAULT_ROOTS = [
    "/Library/Audio/Plug-Ins",
    "/Users/Shared",
    "/Volumes"
]

def repatriate_assets(scan_roots):
    print(f"NOIZY REPATRIATOR v2.0: Scanning {len(scan_roots)} roots...")
    memory_core.log_interaction("Repatriator Initialized", "BOOT", "SHIRL")
    
    manifest = {
        "scan_date": str(datetime.now()),
        "counts": {k: 0 for k in TARGET_EXTENSIONS.values()},
        "locations": {k: [] for k in TARGET_EXTENSIONS.values()},
        "libraries_detected": []
    }
    
    start_time = time.time()
    files_scanned = 0
    
    for root_dir in scan_roots:
        if not os.path.exists(root_dir): continue
        print(f"Scanning: {root_dir}")
        memory_core.log_interaction(f"Crawling: {root_dir}", "SCAN_START", "ENGR")
        
        try:
            for current_root, dirs, files in os.walk(root_dir):
                for f in files:
                    files_scanned += 1
                    ext = os.path.splitext(f)[1].lower()
                    
                    if ext == '.nicnt':
                        lib_path = current_root
                        manifest["libraries_detected"].append(lib_path)
                        print(f"FOUND LIBRARY: {os.path.basename(lib_path)}")
                        
                    if ext in TARGET_EXTENSIONS:
                        category = TARGET_EXTENSIONS[ext]
                        manifest["counts"][category] += 1
                        manifest["locations"][category].append(os.path.join(current_root, f))
                        
                    if files_scanned % 5000 == 0:
                        sys.stdout.write(f"\rScanned {files_scanned} artifacts...")
                        sys.stdout.flush()
                        
        except PermissionError:
            pass
        except KeyboardInterrupt:
            print("\nAborted.")
            memory_core.log_interaction("Repatriation Aborted", "CANCEL", "SHIRL")
            return

    duration = time.time() - start_time
    
    # Reporting
    print(f"\nScanning Complete in {duration:.2f}s")
    for cat, count in manifest["counts"].items():
        if count > 0:
            print(f"  {cat}: {count}")
            
    out_file = "noizy_repatriation_manifest.json"
    with open(out_file, "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"Saved manifest to {out_file}")
    memory_core.log_interaction(f"Repatriation Complete. {files_scanned} files scanned.", "SUCCESS", "ENGR")

if __name__ == "__main__":
    roots = sys.argv[1:]
    if not roots:
        user_music = os.path.expanduser("~/Music")
        roots = DEFAULT_ROOTS + [user_music]
    
    repatriate_assets(roots)
