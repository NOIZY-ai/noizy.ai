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
DEFAULT_ROOT = "/Volumes/JOE"
MAX_WORKERS = (os.cpu_count() or 4) + 8 

# MASTER BFA SIGNATURES (V13 ARCHITECT EDITION)
# Maps Regex -> Official Folder Name
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

def log(msg):
    print(msg)
    sys.stdout.flush()

def identify_library_root(filepath, file_binary_header):
    """
    Identifies if a file belongs to a known BFA library and returns:
    1. The Official Product Name
    2. The PROBABLE ROOT of the library (e.g., the parent folder containing Instruments/Samples)
    """
    
    # 1. Check Binary Signature
    decoded_head = file_binary_header.decode('ascii', errors='ignore')
    signature_product = None
    
    for pattern, product_folder in KNOWN_PRODUCTS.items():
        if re.search(pattern, decoded_head, re.IGNORECASE):
            signature_product = product_folder
            break
            
    # 2. Check Path Context (Parent/Grandparent)
    path_product = None
    curr = filepath
    library_root = None
    
    # Climb up 4 levels to find a folder that matches a Product Name OR looks like a Root
    # "Public Knowledge": BFA roots usually contain "Instruments" or "Samples" or "Documentation"
    
    for i in range(4):
        curr = os.path.dirname(curr)
        dirname = os.path.basename(curr)
        if not dirname or dirname == '/': break
        if "Volumes" in dirname: break
        
        # Does this folder match a product?
        for pattern, product_folder in KNOWN_PRODUCTS.items():
            if re.search(pattern, dirname, re.IGNORECASE):
                path_product = product_folder
                library_root = curr # This folder IS the library root candidate
                break
        if library_root: break
        
        # Secondary Heuristic: Does this folder contain 'Instruments' and 'Samples'?
        # We can't check siblings easily in parallel without os.listdir, which is slow.
        # Stick to Name Matching for speed.

    final_product = signature_product or path_product
    
    # Heuristic: If we found a product signature in the file, but no folder match,
    # assume the immediate parent is likely a subfolder, and grandparent might be root.
    # But for "Rebuild", we safer moving the FOLDER that matched.
    
    if final_product and library_root:
        return final_product, library_root
    
    # If we have signature but no path match, return immediate parent as root?
    if final_product:
        return final_product, os.path.dirname(filepath)
        
    return None, None

def process_discovery(file_info):
    full_path, fname = file_info
    
    try:
        if os.path.getsize(full_path) == 0: return None
        
        with open(full_path, 'rb') as f:
            # Read header for sig
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                head_len = min(len(mm), 50*1024*1024) 
                header = mm[:head_len]
                
                product, root = identify_library_root(full_path, header)
                if product and root:
                    return (product, root)
    except Exception:
        pass
    return None

def move_library(source_root, dest_root, product_name, execute, nuke):
    # Ensure we don't move inside ourselves
    if source_root.startswith(dest_root): return False
    
    target_path = os.path.join(dest_root, product_name)
    
    # Avoid duplicate moves
    if os.path.exists(target_path) and nuke:
        # If target exists and we are nuking, we might want to merge?
        # Merging dirs is complex. safe shutil.move might fail.
        # Let's perform a rename if target doesn't exist.
        pass

    log(f"[ARCHITECT] Rebuilding: {source_root} -> {target_path}")
    
    if execute:
        try:
            if not os.path.exists(target_path):
                # If nuke, move entire tree
                if nuke:
                    shutil.move(source_root, target_path)
                else:
                    shutil.copytree(source_root, target_path, dirs_exist_ok=True)
                return True
            else:
                log(f"SKIPPING: Target {target_path} already exists.")
                return False
        except Exception as e:
            log(f"ERROR Moving {source_root}: {e}")
            return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--nuke', action='store_true')
    args = parser.parse_args()

    root_dir = args.root
    execute = args.execute
    nuke = args.nuke

    log(f"TURBO REBUILD V13: THE ARCHITECT")
    log(f"Scanning Universe: {root_dir}")
    log(f"Mode: {'EXECUTE' if execute else 'DRY RUN'} | Nuke: {nuke}")
    log("-" * 60)

    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME)
    if execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    # 1. FIND ANCHORS (NKIs)
    anchors = []
    log("Scanning for Library Anchors...")
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue
        for fname in filenames:
            if fname.lower().endswith('.nki'):
                anchors.append((os.path.join(dirpath, fname), fname))

    log(f"Found {len(anchors)} potential anchors.")

    # 2. IDENTIFY ROOTS (Parallel)
    detected_libraries = {} # Map RootPath -> ProductName
    
    log("Identifying Library Roots...")
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_discovery, f): f for f in anchors}
        
        for future in as_completed(futures):
            res = future.result()
            if res:
                prod, root = res
                # Keep the shortest root path for a product? Or longest?
                # Usually we want the highest level folder that matches.
                # If we have multiple hits for same root, verify product consistency.
                detected_libraries[root] = prod

    log(f"Identified {len(detected_libraries)} unique library folders to rebuild.")
    log("-" * 60)

    # 3. REBUILD (Move/Copy Trees)
    # Sort by length of path desc to handle nested moves correctly? 
    # Actually, we want to move top level components.
    
    count = 0
    for root_path, product_name in detected_libraries.items():
        if move_library(root_path, base_repair_dir, product_name, execute, nuke):
            count += 1

    log("-" * 60)
    log(f"ARCHITECT COMPLETE. Rebuilt {count} Libraries.")

if __name__ == "__main__":
    main()
