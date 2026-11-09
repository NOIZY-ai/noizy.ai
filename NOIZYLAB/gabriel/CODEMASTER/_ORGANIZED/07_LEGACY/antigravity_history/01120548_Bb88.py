import os
import re
import shutil
import sys
import argparse
import time
import mmap
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
DEFAULT_ROOT = "/Volumes/JOE" # TARGETING THE UNIVERSE
MAX_WORKERS = (os.cpu_count() or 4) + 8 # Maximum Swarm Saturation

# MASTER BFA SIGNATURES (V12 FULL ATLAS)
KNOWN_PRODUCTS = {
    r"Country.*Guitars": "BFA - Country Guitars",
    r"Acoustic.*Soundscapes": "BFA - Acoustic Soundscapes",
    r"Big.*Bad.*Horns": "BFA - Big Bad Horns",
    r"First.*Call.*Horns": "BFA - First Call Horns",
    r"London.*Solo.*Strings": "BFA - London Solo Strings",
    r"Celtic.*Inst": "BFA - Celtic Instruments",
    r"Quirky.*Pop": "BFA - Quirky Pop",
    r"Vintage.*Horns": "BFA - Vintage Horns",
    r"Mojo.*Horn": "BFA - Mojo Horns",
    r"Urban.*String": "BFA - Urban Strings",
    r"Gypsy.*Cafe": "BFA - Gypsy Cafe",
    r"Roots.*Middle.*East": "BFA - Roots Of Middle East",
    r"Roots.*South.*Am": "BFA - Roots Of South America",
    r"Ambient.*Skyline": "BFA - Ambient Skyline",
    r"Indie.*Pop": "BFA - Indie Pop",
    r"Indie.*Rock": "BFA - Indie Rock",
    r"Nu.*RnB": "BFA - Nu RnB Classics",
    r"Radio.*Pop": "BFA - Radio Pop",
    r"Prometheus": "BFA - Prometheus",
    r"Alien.*Guitars": "BFA - Alien Guitars",
    r"Electri6ity": "BFA - Electri6ity",
    r"Acou6tics": "BFA - Acou6tics",
    r"Symphonic.*Brass": "BFA - Symphonic Brass",
    r"Vintage.*Big.*Band": "BFA - Vintage Big Band",
    r"Ancient.*World": "BFA - Ancient World",
    r"Ethno.*World": "BFA - Ethno World",
    r"Mystica": "BFA - Mystica",
    r"Aura": "BFA - Aura",
    r"From.*The.*Garage": "BFA - From The Garage",
    r"Jazz.*Drums": "BFA - Jazz Drums",
    r"Chronic.*Horns": "BFA - Chronic Custom Horns",
    r"Strings.*FX": "BFA - Strings FX",
    r"Drums.*Of.*War": "BFA - Drums Of War",
    r"Lucky.*7": "BFA - Lucky 7",
    r"Off.*The.*Hook": "BFA - Off The Hook",
    r"Cut.*It.*Up": "BFA - Cut'n It Up",
    r"Suite.*Grooves": "BFA - Suite Grooves",
    r"Methodology": "BFA - Methodology",
    r"Liquid.*Metal": "BFA - Liquid Metal",
    r"Dark.*Basement": "BFA - Dark Basement Hits",
    r"Guitar.*Loops": "BFA - Guitar Loops",
    r"Action.*Drums": "BFA - Action Drums",
    r"Cinematic.*Driver": "BFA - Cinematic Drivers",
    r"Rush": "BFA - Rush",
    r"Midnight": "BFA - Midnight",
    r"Vibe": "BFA - Vibe",
    r"Heat.*Seekers": "BFA - Heat Seekers",
    r"Mahidhi": "BFA - Mahidhi",
    r"Persian.*Grooves": "BFA - Persian Grooves",
    r"Bollywood": "BFA - Bollywood Styles",
    r"Hit.*Zone": "BFA - Hit Zone",
    r"Rappin.*Hood": "BFA - Rappin Hood",
}

STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def log(msg):
    print(msg)
    sys.stdout.flush()

def extract_best_name_and_folder(filepath):
    try:
        if os.path.getsize(filepath) == 0: return None, None
            
        with open(filepath, 'rb') as f:
            # V12 GOD MODE: mmap
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                
                # OPTIMIZATION: Check first 200MB signature
                head_len = min(len(mm), 200*1024*1024)
                head_text = mm[:head_len].decode('ascii', errors='ignore')
                
                for pattern, product_folder in KNOWN_PRODUCTS.items():
                    if re.search(pattern, head_text, re.IGNORECASE):
                        internal_name = _heuristic_name(mm[:2*1024*1024])
                        return product_folder, internal_name

                # CONTEXT AWARENESS (Up to 8 Levels for Deep Nesting)
                curr = filepath
                for _ in range(8):
                    curr = os.path.dirname(curr)
                    dirname = os.path.basename(curr)
                    if not dirname or dirname == '/': break
                    if "Volumes" in dirname: break 
                    
                    for pattern, product_folder in KNOWN_PRODUCTS.items():
                        if re.search(pattern, dirname, re.IGNORECASE):
                            return product_folder, _heuristic_name(mm[:2*1024*1024])

                return None, _heuristic_name(mm[:2*1024*1024])

    except Exception:
        return None, None

def _heuristic_name(data):
    matches = []
    scan_limit = min(len(data), 2 * 1024 * 1024)
    for match in STRING_RE.finditer(data[:scan_limit]):
        s = match.group(0).decode('ascii', errors='ignore').strip()
        matches.append(s)

    candidates = []
    for s in matches:
        if not s or len(s) < 3 or len(s) > 80: continue 
        if any(x in s for x in ['/', '\\', ':', '.nki', '.wav', '.aif', 'www.', '.com', '.ncw']): continue
        if "Native Instruments" in s or "Kontakt" in s: continue
        candidates.append(s)

    if candidates:
        candidates.sort(key=len, reverse=True)
        return candidates[0]
    return None

def clean_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s*-{2,}\s*', ' - ', name) 
    name = re.sub(r'\s+', ' ', name)
    if name.endswith('a'): name = name[:-1]
    return name.strip()

def process_single_file(file_info):
    full_path, fname, base_repair_dir, active_execute, nuke_mode = file_info
    
    product_folder, internal_name = extract_best_name_and_folder(full_path)
    
    if not internal_name:
        internal_name = os.path.splitext(fname)[0]
    
    clean_name = clean_filename(internal_name) + ".nki"

    if product_folder:
        dest_dir = os.path.join(base_repair_dir, product_folder)
        result_type = "REBUILT"
    else:
        dest_dir = os.path.join(base_repair_dir, "00_Unsorted_Rebuilds")
        result_type = "UNSORTED"

    dest_path = os.path.join(dest_dir, clean_name)
    result_msg = f"[{result_type}] {fname} -> {os.path.basename(dest_dir)}/{clean_name}"
    
    if active_execute:
        try:
            os.makedirs(dest_dir, exist_ok=True)
            if nuke_mode:
                shutil.move(full_path, dest_path)
            else:
                shutil.copy2(full_path, dest_path)
            return (True, result_msg)
        except Exception as e:
            return (False, f"FAILED {fname}: {e}")
    
    return (True, result_msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--nuke', action='store_true')
    args = parser.parse_args()

    active_execute = args.execute
    nuke_mode = args.nuke
    root_dir = args.root

    log(f"TURBO REBUILD V12: UNIVERSAL SCAN")
    log(f"Scanning Universe: {root_dir}")
    log(f"Engine: GOD MODE (mmap + {MAX_WORKERS} Threads)")
    if nuke_mode: log("WARNING: NUKE MODE ACTIVE (Files will be moved)")
    log("-" * 60)

    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME) # Keep repair hub in NKI path
    if active_execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    files_to_process = []
    log("Scanning file system (This may take a moment for TB+ drives)...")
    
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                files_to_process.append((full_path, fname, base_repair_dir, active_execute, nuke_mode))
    
    log(f"Detected {len(files_to_process)} scatter instruments.")
    log("Engaging Reconstruction Swarm...")
    
    start_time = time.time()
    success_count = 0
    fail_count = 0
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_file, f): f for f in files_to_process}
        
        for future in as_completed(futures):
            success, msg = future.result()
            log(msg)
            if success: success_count += 1
            else: fail_count += 1

    duration = time.time() - start_time
    rate = success_count / duration if duration > 0 else 0

    log("-" * 60)
    log(f" REBUILD COMPLETE. Time: {duration:.2f}s")
    log(f" Files Processed: {success_count} ({rate:.1f}/sec)")

if __name__ == "__main__":
    main()
