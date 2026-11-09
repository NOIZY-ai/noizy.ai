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
MAX_WORKERS = (os.cpu_count() or 4) + 16
LOG_FILE = "/Volumes/JOE/NKI/omega_log.txt"

# MASTER BFA SIGNATURES (V15 OMEGA EDITION)
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

regex_parts = []
for key, val in RAW_SIGS.items():
    pattern = val[0]
    regex_parts.append(f"(?P<{key}>{pattern})")
    
FULL_PATTERN_STR = "|".join(regex_parts)
OMEGA_REGEX = re.compile(FULL_PATTERN_STR.encode('ascii'), re.IGNORECASE)

def log(msg):
    print(msg)
    sys.stdout.flush()
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(msg + "\n")
    except: pass

def identify_library_root(filepath, file_binary_header):
    match = OMEGA_REGEX.search(file_binary_header)
    signature_product = None
    if match:
        group_name = match.lastgroup
        if group_name and group_name in RAW_SIGS:
            signature_product = RAW_SIGS[group_name][1]
            
    path_product = None
    curr = filepath
    library_root = None
    
    for i in range(8):
        curr = os.path.dirname(curr)
        dirname = os.path.basename(curr)
        if not dirname or dirname == '/': break
        if "Volumes" in dirname: break
        
        try:
            d_bytes = dirname.encode('ascii', errors='ignore')
            m_path = OMEGA_REGEX.search(d_bytes)
            if m_path:
                g_name = m_path.lastgroup
                if g_name in RAW_SIGS:
                    path_product = RAW_SIGS[g_name][1]
                    library_root = curr
                    break
        except: pass
            
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

    sys.setrecursionlimit(2000)

    # Clean log
    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)

    root_dir = args.root
    execute = args.execute
    nuke = args.nuke

    log(f"TURBO REBUILD V16: OMEGA LOGGING EDITION")
    log(f"Root: {root_dir}")
    log(f"Mode: {'EXECUTE' if execute else 'DRY RUN'}")
    log("-" * 60)

    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME)
    if execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    anchors = []
    log("Checking Shell Acceleration...")
    
    try:
        cmd = ["find", root_dir, "-name", "*.nki"]
        find_output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        paths = find_output.decode('utf-8').splitlines()
        log(f"Shell returned {len(paths)} targets.")
        for p in paths:
             if REPAIR_DIR_NAME not in p:
                 anchors.append((p, os.path.basename(p)))
    except Exception as e:
        log(f"Shell failed ({e}). using os.walk...")
        for dirpath, _, filenames in os.walk(root_dir):
            if REPAIR_DIR_NAME in dirpath: continue
            for fname in filenames:
                if fname.lower().endswith('.nki'):
                    anchors.append((os.path.join(dirpath, fname), fname))

    log(f"Engaging Omega Swarm on {len(anchors)} items...")
    
    detected_libraries = {} 
    
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_discovery, f): f for f in anchors}
        
        for future in as_completed(futures):
            res = future.result()
            if res:
                prod, root = res
                detected_libraries[root] = prod

    log(f"Identified {len(detected_libraries)} libraries.")
    log("-" * 60)

    count = 0
    for source_root, product_name in detected_libraries.items():
        if source_root.startswith(base_repair_dir): continue
        target_path = os.path.join(base_repair_dir, product_name)
        
        log(f"[REBUILDING] {product_name} :: {source_root} -> {target_path}")
        
        if execute:
            try:
                if not os.path.exists(target_path):
                    if nuke:
                        shutil.move(source_root, target_path)
                    else:
                        shutil.copytree(source_root, target_path, dirs_exist_ok=True)
                    count += 1
                else:
                    log(f"SKIP: Target Exists.")
            except Exception as e:
                log(f"ERROR: {e}")
        else:
            count += 1

    log("-" * 60)
    log(f"DONE. Rebuilt {count} libraries.")

if __name__ == "__main__":
    main()
