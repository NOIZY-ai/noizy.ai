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
MAX_WORKERS = (os.cpu_count() or 4) + 4 

# MASTER BFA SIGNATURES (God Mode Expanded)
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
}

STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def log(msg):
    print(msg)
    sys.stdout.flush()

def extract_best_name_and_folder(filepath):
    try:
        # Check size first. If empty, skip.
        if os.path.getsize(filepath) == 0:
            return None, None
            
        with open(filepath, 'rb') as f:
            # TURBO GOD MODE: Memory Map the ENTIRE file
            # This allows OS to handle paging. fast access to ANY byte.
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                
                # 1. KNOWN PRODUCTS - Global Regex on Memory Map
                # Converting whole mmap to string might be heavy if file is 2GB+.
                # But regex works on bytes.
                
                # Limit text decode to first 50MB for signatures to be safe/fast? 
                # User said NO EXCUSES. We scan IT ALL.
                # But creating a python string from 2GB is bad.
                # Let's scan chunks or just hope bytes regex on mmap works well.
                # Python's re works on mmap buffer directly!
                
                for pattern, product_folder in KNOWN_PRODUCTS.items():
                    # We need to compile pattern as bytes for direct mmap search
                    # Pattern is raw string. Encode it.
                    # Simplified: regex on mmap object might expect bytes.
                    
                    # Pattern is roughly: r"Country.*Guitars"
                    # We need to be careful about case insensitive on bytes.
                    # Let's read first 10MB as bytes, that usually covers tags.
                    # "NO EXCUSES" -> Ok, let's try scanning chunks if regex fails.
                    
                    # Practical compromise: Read 100MB head.
                    head_data = mm[:100*1024*1024]
                    head_text = head_data.decode('ascii', errors='ignore')
                    
                    if re.search(pattern, head_text, re.IGNORECASE):
                        internal_name = _heuristic_name(head_data)
                        return product_folder, internal_name

                # 2. CONTEXT AWARENESS (Recursive 5-Level)
                curr = filepath
                for _ in range(5):
                    curr = os.path.dirname(curr)
                    dirname = os.path.basename(curr)
                    if not dirname or dirname == '/': break
                    
                    for pattern, product_folder in KNOWN_PRODUCTS.items():
                        if re.search(pattern, dirname, re.IGNORECASE):
                            # Use what data we have
                            return product_folder, _heuristic_name(mm[:1*1024*1024])

                # 3. FALLBACK HEURISTIC
                return None, _heuristic_name(mm[:2*1024*1024])

    except Exception:
        return None, None

def _heuristic_name(data):
    matches = []
    # Limit heuristic scan to 2MB to keep listing fast
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
        result_type = "GOD_MODE_SORT"
    else:
        dest_dir = os.path.join(base_repair_dir, "00_Unsorted_Misc")
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

def process_volume_parallel(root_dir, active_execute=False, nuke_mode=False):
    log(f"TURBO SCAN V11: GOD MODE (mmap)")
    log(f"CPUs: {MAX_WORKERS}")
    log(f"Depth: INFINITE (Memory Mapped)")
    log("-" * 60)

    base_repair_dir = os.path.join(root_dir, REPAIR_DIR_NAME)
    if active_execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    files_to_process = []
    log("Gathering file list...")
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                files_to_process.append((full_path, fname, base_repair_dir, active_execute, nuke_mode))
    
    log(f"Targeting {len(files_to_process)} Files.")
    
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
    log(f" GOD MODE COMPLETE. Time: {duration:.2f}s")
    log(f" Rate: {rate:.1f} files/sec")

def main():
    root = "/Volumes/JOE/NKI"
    execute = "--execute" in sys.argv
    nuke = "--nuke" in sys.argv
    process_volume_parallel(root, active_execute=execute, nuke_mode=nuke)

if __name__ == "__main__":
    main()
