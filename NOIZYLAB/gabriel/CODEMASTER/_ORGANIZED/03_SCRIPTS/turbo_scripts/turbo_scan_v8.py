import os
import re
import shutil
import sys
import argparse
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
MAX_WORKERS = os.cpu_count() or 4  # Use all available cores

# MASTER BFA SIGNATURES (V7 Expanded Intelligence)
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
}

STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def log(msg):
    print(msg)
    sys.stdout.flush()

def extract_best_name_and_folder(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read(1 * 1024 * 1024) # 1MB is usually sufficient for signature
            text_data = data.decode('ascii', errors='ignore')

            # 1. KNOWN PRODUCTS
            for pattern, product_folder in KNOWN_PRODUCTS.items():
                if re.search(pattern, text_data, re.IGNORECASE):
                    internal_name = _heuristic_name(data)
                    return product_folder, internal_name
            
            # 2. CONTEXT AWARENESS
            parent_dir = os.path.basename(os.path.dirname(filepath))
            for pattern, product_folder in KNOWN_PRODUCTS.items():
                if re.search(pattern, parent_dir, re.IGNORECASE):
                    internal_name = _heuristic_name(data)
                    return product_folder, internal_name

            # 3. FALLBACK
            internal_name = _heuristic_name(data)
            return None, internal_name

    except Exception:
        return None, None

def _heuristic_name(data):
    matches = []
    for match in STRING_RE.finditer(data):
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
    """
    Worker function for parallel processing.
    """
    full_path, fname, base_repair_dir, active_execute, nuke_mode = file_info
    
    product_folder, internal_name = extract_best_name_and_folder(full_path)
    
    if not internal_name:
        internal_name = os.path.splitext(fname)[0]
    
    clean_name = clean_filename(internal_name) + ".nki"

    if product_folder:
        dest_dir = os.path.join(base_repair_dir, product_folder)
        result_type = "SORTED"
    else:
        dest_dir = os.path.join(base_repair_dir, "00_Unsorted_Misc")
        result_type = "UNSORTED"

    dest_path = os.path.join(dest_dir, clean_name)
    
    # Don't actually move/copy in the worker if we want to avoid race conditions with directory creation?
    # Actually, worst case dir exists. os.makedirs is safe with exist_ok.
    # But print statements might interleave.
    
    result_msg = f"[{result_type}] {fname} -> {os.path.basename(dest_dir)}/{clean_name}"
    
    if active_execute:
        try:
            os.makedirs(dest_dir, exist_ok=True)
            
            if os.path.exists(dest_path):
                 base, ext = os.path.splitext(clean_name)
                 c = 1
                 while os.path.exists(os.path.join(dest_dir, f"{base}_{c}{ext}")): c += 1
                 dest_path = os.path.join(dest_dir, f"{base}_{c}{ext}")

            if nuke_mode:
                shutil.move(full_path, dest_path)
            else:
                shutil.copy2(full_path, dest_path)
            
            return (True, result_msg)
        except Exception as e:
            return (False, f"FAILED {fname}: {e}")
    
    return (True, result_msg)

def process_volume_parallel(root_dir, active_execute=False, nuke_mode=False):
    log(f"TURBO SCAN V8: PARALLEL SWARM (CPUs: {MAX_WORKERS})")
    log(f"Scanning Root: {root_dir}")
    log("-" * 60)

    base_repair_dir = os.path.join(root_dir, REPAIR_DIR_NAME)
    if active_execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    # 1. Collect all files FIRST
    files_to_process = []
    log("Gathering file list...")
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                files_to_process.append((full_path, fname, base_repair_dir, active_execute, nuke_mode))
    
    log(f"Found {len(files_to_process)} NKI files. Engaging Swarm.")
    
    start_time = time.time()
    success_count = 0
    fail_count = 0
    
    # 2. Parallel Execution
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_single_file, f): f for f in files_to_process}
        
        for future in as_completed(futures):
            success, msg = future.result()
            log(msg)
            if success:
                success_count += 1
            else:
                fail_count += 1

    duration = time.time() - start_time
    rate = success_count / duration if duration > 0 else 0

    log("-" * 60)
    log(f"SWARM COMPLETE in {duration:.2f} seconds.")
    log(f"Processed: {success_count} ({rate:.1f} files/sec)")
    log(f"Failures: {fail_count}")

def main():
    root = "/Volumes/JOE/NKI"
    execute = "--execute" in sys.argv
    nuke = "--nuke" in sys.argv
    process_volume_parallel(root, active_execute=execute, nuke_mode=nuke)

if __name__ == "__main__":
    main()
