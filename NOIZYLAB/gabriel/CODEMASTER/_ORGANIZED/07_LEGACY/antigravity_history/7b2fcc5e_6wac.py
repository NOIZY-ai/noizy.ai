import os
import re
import shutil
import sys
import argparse
import time
import mmap
import hashlib

# ==============================================================================
# TURBO BFA GOD MODE V2: THE DEEP TUNNEL EDITION
# ==============================================================================
# "DEEPER, NO EXCUSES!"
# - Scan Depth: Increased to 500MB (effectively infinite for NKI).
# - Velocity: O(1) Regex optimized.
# - Rebuild: Move + Rename.
# ==============================================================================

REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
DEFAULT_ROOT = "/Volumes/JOE"
LOG_FILE = "/Volumes/JOE/NKI/turbo_god_v2_log.txt"

# --- OMEGA SIGNATURES V2 ---
RAW_SIGS = {
    "CountryGuitars": (r"Country.*Guitars", "BFA - Country Guitars"),
    "AcousticSounds": (r"Acoustic.*Soundscapes", "BFA - Acoustic Soundscapes"),
    "BigBadHorns": (r"Big.*Bad.*Horns", "BFA - Big Bad Horns"),
    "FirstCall": (r"First.*Call.*Horns", "BFA - First Call Horns"),
    "LondonStrings": (r"London.*Solo.*Strings", "BFA - London Solo Strings"),
    "CelticInst": (r"Celtic.*Inst", "BFA - Celtic Instruments"),
    "QuirkyPop": (r"Quirky.*Pop", "BFA - Quirky Pop"),
    "VintageHorns": (r"Vintage.*Horns", "BFA - Vintage Horns"),
    "MojoHorn": (r"Mojo.*Horn", "BFA - Mojo Horns"),
    "UrbanString": (r"Urban.*String", "BFA - Urban Strings"),
    "GypsyCafe": (r"Gypsy.*Cafe", "BFA - Gypsy Cafe"),
    "RootsMidEast": (r"Roots.*Middle.*East", "BFA - Roots Of Middle East"),
    "RootsSouthAm": (r"Roots.*South.*Am", "BFA - Roots Of South America"),
    "AmbientSky": (r"Ambient.*Skyline", "BFA - Ambient Skyline"),
    "IndiePop": (r"Indie.*Pop", "BFA - Indie Pop"),
    "IndieRock": (r"Indie.*Rock", "BFA - Indie Rock"),
    "NuRnB": (r"Nu.*RnB", "BFA - Nu RnB Classics"),
    "RadioPop": (r"Radio.*Pop", "BFA - Radio Pop"),
    "Prometheus": (r"Prometheus", "BFA - Prometheus"),
    "AlienGuitars": (r"Alien.*Guitars", "BFA - Alien Guitars"),
    "Electri6ity": (r"Electri6ity", "BFA - Electri6ity"),
    "Acou6tics": (r"Acou6tics", "BFA - Acou6tics"),
    "SymBrass": (r"Symphonic.*Brass", "BFA - Symphonic Brass"),
    "VintageBigBand": (r"Vintage.*Big.*Band", "BFA - Vintage Big Band"),
    "AncientWorld": (r"Ancient.*World", "BFA - Ancient World"),
    "EthnoWorld": (r"Ethno.*World", "BFA - Ethno World"),
    "Mystica": (r"Mystica", "BFA - Mystica"),
    "Aura": (r"Aura", "BFA - Aura"),
    "Garage": (r"From.*The.*Garage", "BFA - From The Garage"),
    "JazzDrums": (r"Jazz.*Drums", "BFA - Jazz Drums"),
    "ChronicHorns": (r"Chronic.*Horns", "BFA - Chronic Custom Horns"),
    "StringsFX": (r"Strings.*FX", "BFA - Strings FX"),
    "DrumsOfWar": (r"Drums.*Of.*War", "BFA - Drums Of War"),
    "Lucky7": (r"Lucky.*7", "BFA - Lucky 7"),
    "OffTheHook": (r"Off.*The.*Hook", "BFA - Off The Hook"),
    "CutItUp": (r"Cut.*It.*Up", "BFA - Cut'n It Up"),
    "SuiteGrooves": (r"Suite.*Grooves", "BFA - Suite Grooves"),
    "Methodology": (r"Methodology", "BFA - Methodology"),
    "LiquidMetal": (r"Liquid.*Metal", "BFA - Liquid Metal"),
    "DarkBasement": (r"Dark.*Basement", "BFA - Dark Basement Hits"),
    "GuitarLoops": (r"Guitar.*Loops", "BFA - Guitar Loops"),
    "ActionDrums": (r"Action.*Drums", "BFA - Action Drums"),
    "CinematicDriver": (r"Cinematic.*Driver", "BFA - Cinematic Drivers"),
    "Rush": (r"Rush", "BFA - Rush"),
    "Midnight": (r"Midnight", "BFA - Midnight"),
    "Vibe": (r"Vibe", "BFA - Vibe"),
    "HeatSeekers": (r"Heat.*Seekers", "BFA - Heat Seekers"),
    "Mahidhi": (r"Mahidhi", "BFA - Mahidhi"),
    "PersianGrooves": (r"Persian.*Grooves", "BFA - Persian Grooves"),
    "Bollywood": (r"Bollywood", "BFA - Bollywood Styles"),
    "HitZone": (r"Hit.*Zone", "BFA - Hit Zone"),
    "RappinHood": (r"Rappin.*Hood", "BFA - Rappin Hood"),
}

# Compile Omega Regex
regex_parts = [f"(?P<{k}>{v[0]})" for k, v in RAW_SIGS.items()]
FULL_PATTERN_STR = "|".join(regex_parts)
OMEGA_REGEX = re.compile(FULL_PATTERN_STR.encode('ascii'), re.IGNORECASE)
# Aggressive String extraction
STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def log(msg):
    # Dual logging: Console + File
    print(msg)
    sys.stdout.flush()
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(msg + "\n")
    except: pass

def clean_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s*-{2,}\s*', ' - ', name) 
    name = re.sub(r'\s+', ' ', name)
    if name.endswith('a'): name = name[:-1]
    return name.strip()

def extract_internal_name(mm_data):
    # DEEP SCAN: 500MB (Basically the whole file usually)
    scan_limit = min(len(mm_data), 500 * 1024 * 1024) 
    data = mm_data[:scan_limit]
    
    matches = []
    # Find all ASCII strings > 4 chars
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
        # Heuristic: Longest string is often the best description? 
        # Or most "Title Case" one?
        # Let's stick to Longest first.
        candidates.sort(key=len, reverse=True)
        return candidates[0]
    return None

def identify_library_root_and_name(filepath, mm, header):
    # 1. Product ID (Omega Regex)
    match = OMEGA_REGEX.search(header)
    product_name = None
    if match and match.lastgroup in RAW_SIGS:
        product_name = RAW_SIGS[match.lastgroup][1]

    # 2. Context ID (Path Analysis)
    path_product = None
    library_root = None
    curr = filepath
    
    if not product_name:
        for i in range(6): # Scan up 6 levels now
            curr = os.path.dirname(curr)
            dirname = os.path.basename(curr)
            if not dirname or dirname == '/' or "Volumes" in dirname: break
            try:
                m = OMEGA_REGEX.search(dirname.encode('ascii', errors='ignore'))
                if m and m.lastgroup in RAW_SIGS:
                    path_product = RAW_SIGS[m.lastgroup][1]
                    library_root = curr
                    break
            except: pass
    
    final_product = product_name or path_product
    internal_name = extract_internal_name(mm)
    
    if not library_root:
        # Heuristic Root Finding
        curr = filepath
        candidate_root = os.path.dirname(filepath)
        for i in range(5):
            curr = os.path.dirname(curr)
            if os.path.basename(curr) == "Volumes": break
            # Stop if we see common root markers
            if os.path.exists(os.path.join(curr, "Documentation")) or os.path.exists(os.path.join(curr, "Samples")):
                candidate_root = curr
                break
        library_root = candidate_root

    return final_product, library_root, internal_name

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT)
    parser.add_argument('--execute', action='store_true', help="Perform actions")
    parser.add_argument('--nuke', action='store_true', help="Move files (delete source)")
    args = parser.parse_args()

    # Clear log
    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)

    log("=== TURBO BFA GOD MODE v2.0 (DEEP TUNNEL) ===")
    log("Status: HEALING & OPTIMIZING")
    log(f"Root: {args.root}")
    log(f"Execute: {args.execute} | Nuke: {args.nuke}")
    log("-" * 60)

    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME)
    if args.execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    root_dir = args.root
    stats = {'lib_moves': 0, 'file_renames': 0}

    # Robust Single-Thread Walk
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue 

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                try:
                    if os.path.getsize(full_path) == 0: continue
                    
                    with open(full_path, 'rb') as f:
                        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                            # 500MB Scan
                            head_len = min(len(mm), 500*1024*1024)
                            header = mm[:head_len]
                            
                            product, lib_root, internal_name = identify_library_root_and_name(full_path, mm, header)

                            # RENAME LOGIC
                            target_fname = fname
                            if internal_name:
                                clean_n = clean_filename(internal_name) + ".nki"
                                if clean_n != fname:
                                    target_fname = clean_n
                                    if args.execute:
                                        new_full_path = os.path.join(dirpath, target_fname)
                                        # Handle collision
                                        if os.path.exists(new_full_path):
                                             base, ext = os.path.splitext(target_fname)
                                             c = 1
                                             while os.path.exists(os.path.join(dirpath, f"{base}_{c}{ext}")): c += 1
                                             target_fname = f"{base}_{c}{ext}"
                                             new_full_path = os.path.join(dirpath, target_fname)
                                        
                                        os.rename(full_path, new_full_path)
                                        full_path = new_full_path 
                                        stats['file_renames'] += 1
                                        log(f"[RENAME] {fname} -> {target_fname}")
                                    else:
                                        log(f"[DRY-RENAME] {fname} -> {target_fname}")

                            # REBUILD LOGIC
                            if product and lib_root:
                                target_lib_path = os.path.join(base_repair_dir, product)
                                
                                if os.path.abspath(lib_root) != os.path.abspath(target_lib_path):
                                    if args.execute:
                                        if not os.path.exists(target_lib_path):
                                            log(f"[MOVING LIB] {product}")
                                            log(f"  Src: {lib_root}")
                                            
                                            if args.nuke:
                                                shutil.move(lib_root, target_lib_path)
                                            else:
                                                shutil.copytree(lib_root, target_lib_path, dirs_exist_ok=True)
                                            stats['lib_moves'] += 1
                                        else:
                                            # Target exists. 
                                            pass
                except Exception as e:
                    pass

    log("-" * 60)
    log(f"DONE. Renamed: {stats['file_renames']} | Moved Libs: {stats['lib_moves']}")

if __name__ == "__main__":
    main()
