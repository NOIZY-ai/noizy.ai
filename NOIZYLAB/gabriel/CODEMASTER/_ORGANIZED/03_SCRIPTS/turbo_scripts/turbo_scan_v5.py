import os
import re
import shutil
import sys
import argparse

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"

# MASTER BFA SIGNATURES (Sourced from Research)
# Maps a regex pattern found in the binary to the CLEAN Official Product Name
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
}

def log(msg):
    print(msg)
    sys.stdout.flush()

STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def extract_best_name(filepath):
    try:
        with open(filepath, 'rb') as f:
            # SUPER DEEP SCAN: 2MB to catch deep tags
            data = f.read(2 * 1024 * 1024) 
            text_data = data.decode('ascii', errors='ignore')

            # 1. PRIORITY: Check for Known Product Signatures FIRST
            for pattern, official_name in KNOWN_PRODUCTS.items():
                if re.search(pattern, text_data, re.IGNORECASE):
                    # We found a verified BFA signature!
                    # Now try to find the specific patch name near it, OR just return the product
                    # For now, let's grab the specific string match if it looks like a filename
                    return official_name # Strategy: Group into Product Folders? Or rename file? 
                    # User wants NAMES. Let's try to find the specific patch name.
            
            # 2. STANDARD HEURISTIC (Fallback)
            matches = []
            for match in STRING_RE.finditer(data):
                s = match.group(0).decode('ascii', errors='ignore').strip()
                matches.append(s)

            candidates = []
            for s in matches:
                if not s or len(s) < 3 or len(s) > 80: continue # Looser constraints
                if any(x in s for x in ['/', '\\', ':', '.nki', '.wav', '.aif', 'www.', '.com', '.ncw']): continue
                if "Native Instruments" in s or "Kontakt" in s: continue
                candidates.append(s)

            if candidates:
                # Heuristic: Valid names usually have spaces and Capital Letters
                # Return the longest string that looks like a title
                candidates.sort(key=len, reverse=True)
                return candidates[0]

    except Exception as e:
        log(f"Error reading {filepath}: {e}")
    return None

def clean_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s*-{2,}\s*', ' - ', name) # Double dash fix
    name = re.sub(r'\s+', ' ', name)
    if name.endswith('a'): name = name[:-1] # Trailing 'a' fix
    return name.strip()

def process_volume(root_dir, active_execute=False, nuke_mode=False):
    log(f"TURBO SCAN V5: NUCLEAR OPTION")
    log(f"Scanning Root: {root_dir}")
    log(f"Active Execute: {active_execute}")
    log(f"NUKE MODE (Delete Original): {nuke_mode}")
    log("-" * 60)

    target_dir = os.path.join(root_dir, REPAIR_DIR_NAME)
    if active_execute and not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                
                # Try to get a name
                internal_name = extract_best_name(full_path)
                
                # NUCLEAR FALLBACK: If no name, keep original name but CLEAN it
                if not internal_name:
                    internal_name = os.path.splitext(fname)[0] 
                
                # Check if it matches a KNOWN PRODUCT to add a folder prefix?
                # For now, just rename the file cleanly.
                
                clean_name = clean_filename(internal_name) + ".nki"
                dest_path = os.path.join(target_dir, clean_name)

                # Handle duplicates
                if active_execute and os.path.exists(dest_path):
                     base, ext = os.path.splitext(clean_name)
                     c = 1
                     while os.path.exists(os.path.join(target_dir, f"{base}_{c}{ext}")): c += 1
                     dest_path = os.path.join(target_dir, f"{base}_{c}{ext}")

                log(f"[NUCLEAR FIX] {fname} -> {os.path.basename(dest_path)}")

                if active_execute:
                    try:
                        if nuke_mode:
                            # MOVE (Delete source)
                            shutil.move(full_path, dest_path)
                        else:
                            # COPY (Safe)
                            shutil.copy2(full_path, dest_path)
                        count += 1
                    except Exception as e:
                        log(f"FAILED: {e}")

    log("-" * 60)
    log(f"Total Operations: {count}")

def main():
    root = "/Volumes/JOE/NKI"
    execute = "--execute" in sys.argv
    nuke = "--nuke" in sys.argv
    process_volume(root, active_execute=execute, nuke_mode=nuke)

if __name__ == "__main__":
    main()
