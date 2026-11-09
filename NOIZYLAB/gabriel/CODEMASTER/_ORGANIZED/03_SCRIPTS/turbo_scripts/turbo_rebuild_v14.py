import os
import re
import shutil
import sys
import argparse
import time
import mmap
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
DEFAULT_ROOT = "/Volumes/JOE"
MAX_WORKERS = (os.cpu_count() or 4) + 12 # Max Saturation

# MASTER BFA SIGNATURES (V14 SINGULARITY EDITION)
KNOWN_PRODUCTS_OD = {
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

# SINGULARITY OPTIMIZATION: COMPILE ONE MASSIVE REGEX
# We need to map the matched Group back to the Product Name.
# Since python re.match objects usually just give the whole match string, 
# we iterate. But if we want 100% speed, we should rely on the map scan.
# Keeping the iteration for now as the mmap IO is the bottleneck, not the cpu regex.

def log(msg):
    print(msg)
    sys.stdout.flush()

def identify_library_root(filepath, file_binary_header):
    decoded_head = file_binary_header.decode('ascii', errors='ignore')
    signature_product = None
    
    # 1. OPTIMIZED SIG CHECK
    # We could optimize this loop, but iterating 50 strings is fast enough compared to disk IO.
    for pattern, product_folder in KNOWN_PRODUCTS_OD.items():
        if re.search(pattern, decoded_head, re.IGNORECASE):
            signature_product = product_folder
            break
            
    # 2. DEEP CONTEXT CHECK (8 Levels)
    path_product = None
    curr = filepath
    library_root = None
    
    for i in range(8):
        curr = os.path.dirname(curr)
        dirname = os.path.basename(curr)
        if not dirname or dirname == '/': break
        if "Volumes" in dirname: break
        
        for pattern, product_folder in KNOWN_PRODUCTS_OD.items():
            if re.search(pattern, dirname, re.IGNORECASE):
                path_product = product_folder
                library_root = curr 
                break
        if library_root: break

    final_product = signature_product or path_product
    if final_product and library_root:
        return final_product, library_root
    
    if final_product:
        return final_product, os.path.dirname(filepath)
        
    return None, None

def process_discovery(file_info):
    full_path, fname = file_info
    try:
        if os.path.getsize(full_path) == 0: return None
        with open(full_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                head_len = min(len(mm), 200*1024*1024) 
                header = mm[:head_len]
                product, root = identify_library_root(full_path, header)
                if product and root:
                    return (product, root)
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--nuke', action='store_true')
    args = parser.parse_args()

    root_dir = args.root
    execute = args.execute
    nuke = args.nuke

    log(f"TURBO REBUILD V14: THE SINGULARITY")
    log(f"Scanning Universe: {root_dir}")
    log(f"Engine: SHELL VELOCITY + GOD MODE + SWARM")
    if nuke: log("WARNING: NUKE ACTIVE")
    log("-" * 60)

    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME)
    if execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    anchors = []
    log("Initializing Shell-Accelerated Scan (find)...")
    
    try:
        # SUPER FAST SHELL SCAN
        cmd = ["find", root_dir, "-name", "*.nki"]
        # Use subprocess to stream stdout line by line or capture all
        # Capture all is faster for python to parse at once
        find_output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        paths = find_output.decode('utf-8').splitlines()
        
        log(f"Shell returned {len(paths)} potential targets instantly.")
        
        for p in paths:
             if REPAIR_DIR_NAME not in p:
                 anchors.append((p, os.path.basename(p)))
                 
    except Exception as e:
        log(f"Shell scan failed ('{e}'). Fallback to os.walk...")
        for dirpath, _, filenames in os.walk(root_dir):
            if REPAIR_DIR_NAME in dirpath: continue
            for fname in filenames:
                if fname.lower().endswith('.nki'):
                    anchors.append((os.path.join(dirpath, fname), fname))

    log(f"Engaging ID Swarm on {len(anchors)} items...")

    detected_libraries = {} 
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_discovery, f): f for f in anchors}
        
        for future in as_completed(futures):
            res = future.result()
            if res:
                prod, root = res
                detected_libraries[root] = prod

    log(f"Singularity Identified {len(detected_libraries)} unique library roots.")
    log("-" * 60)

    count = 0
    # Re-use Architect Move Logic inline for simplicity
    for source_root, product_name in detected_libraries.items():
        if source_root.startswith(base_repair_dir): continue
        target_path = os.path.join(base_repair_dir, product_name)
        
        log(f"[SINGULARITY] {product_name} :: {source_root} -> {target_path}")
        
        if execute:
            try:
                if not os.path.exists(target_path):
                    if nuke:
                        shutil.move(source_root, target_path)
                    else:
                        shutil.copytree(source_root, target_path, dirs_exist_ok=True)
                    count += 1
                else:
                    log(f"SKIP: Target exists.")
            except Exception as e:
                log(f"ERROR: {e}")
        else:
            count += 1

    log("-" * 60)
    log(f"SINGULARITY COMPLETE. Operations: {count}")

if __name__ == "__main__":
    main()
