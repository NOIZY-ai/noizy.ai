import os
import re
import shutil
import sys
import argparse

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"

# MASTER BFA SIGNATURES (Massively Expanded)
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

def log(msg):
    print(msg)
    sys.stdout.flush()

STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def extract_best_name_and_folder(filepath):
    try:
        with open(filepath, 'rb') as f:
            # SUPER DEEP SCAN: 2MB to catch deep tags
            data = f.read(2 * 1024 * 1024) 
            text_data = data.decode('ascii', errors='ignore')

            # 1. PRIORITY: Check for Known Product Signatures FIRST
            for pattern, product_folder in KNOWN_PRODUCTS.items():
                if re.search(pattern, text_data, re.IGNORECASE):
                    internal_name = _heuristic_name(data)
                    return product_folder, internal_name
            
            # 2. CONTEXT AWARENESS (New for V7)
            # If binary fails, check if parent folder matches a known product
            parent_dir = os.path.basename(os.path.dirname(filepath))
            for pattern, product_folder in KNOWN_PRODUCTS.items():
                if re.search(pattern, parent_dir, re.IGNORECASE):
                    internal_name = _heuristic_name(data)
                    return product_folder, internal_name

            # 3. STANDARD HEURISTIC (Fallback)
            internal_name = _heuristic_name(data)
            return None, internal_name

    except Exception as e:
        log(f"Error reading {filepath}: {e}")
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

def process_volume(root_dir, active_execute=False, nuke_mode=False):
    log(f"TURBO SCAN V7: SMARTER & CONTEXT AWARE")
    log(f"Scanning Root: {root_dir}")
    log(f"Active Execute: {active_execute}")
    log(f"NUKE MODE (Delete Original): {nuke_mode}")
    log("-" * 60)

    base_repair_dir = os.path.join(root_dir, REPAIR_DIR_NAME)
    if active_execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)

    count = 0
    sorted_count = 0

    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                
                # V7 Smart Extraction
                product_folder, internal_name = extract_best_name_and_folder(full_path)
                
                if not internal_name:
                    internal_name = os.path.splitext(fname)[0]
                
                clean_name = clean_filename(internal_name) + ".nki"

                if product_folder:
                    dest_dir = os.path.join(base_repair_dir, product_folder)
                    log(f"[SMART SORT] {fname} -> {product_folder}/{clean_name}")
                    sorted_count += 1
                else:
                    dest_dir = os.path.join(base_repair_dir, "00_Unsorted_Misc")
                    log(f"[UNSORTED] {fname} -> {clean_name}")

                if active_execute:
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir, exist_ok=True)

                    dest_path = os.path.join(dest_dir, clean_name)

                    if os.path.exists(dest_path):
                         base, ext = os.path.splitext(clean_name)
                         c = 1
                         while os.path.exists(os.path.join(dest_dir, f"{base}_{c}{ext}")): c += 1
                         dest_path = os.path.join(dest_dir, f"{base}_{c}{ext}")

                    try:
                        if nuke_mode:
                            shutil.move(full_path, dest_path)
                        else:
                            shutil.copy2(full_path, dest_path)
                        count += 1
                    except Exception as e:
                        log(f"FAILED: {e}")

    log("-" * 60)
    log(f"Total Operations: {count}")
    log(f"Smart Sorted: {sorted_count}")

def main():
    root = "/Volumes/JOE/NKI"
    execute = "--execute" in sys.argv
    nuke = "--nuke" in sys.argv
    process_volume(root, active_execute=execute, nuke_mode=nuke)

if __name__ == "__main__":
    main()
