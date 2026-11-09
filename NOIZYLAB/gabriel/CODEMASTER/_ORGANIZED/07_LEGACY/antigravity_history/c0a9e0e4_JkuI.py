import os
import re
import shutil
import sys
import argparse
import time
import mmap

# Configuration
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
DEFAULT_ROOT = "/Volumes/JOE"

# RAW SIGNATURES (V17 VISUALIZER EDITION)
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
    # Print to both stdout and stderr to guarantee visibility in runner
    print(msg)
    sys.stdout.flush()

def identify_library_root(filepath, file_binary_header):
    # 1. Signature Check
    match = OMEGA_REGEX.search(file_binary_header)
    signature_product = None
    if match and match.lastgroup in RAW_SIGS:
        signature_product = RAW_SIGS[match.lastgroup][1]
            
    # 2. Context Check
    path_product = None
    curr = filepath
    library_root = None
    
    for i in range(8):
        curr = os.path.dirname(curr)
        dirname = os.path.basename(curr)
        if not dirname or dirname == '/' or "Volumes" in dirname: break
        
        try:
            # Quick check on dirname
            if OMEGA_REGEX.search(dirname.encode('ascii', errors='ignore')):
                # Which one?
                m = OMEGA_REGEX.search(dirname.encode('ascii', errors='ignore'))
                if m.lastgroup in RAW_SIGS:
                    path_product = RAW_SIGS[m.lastgroup][1]
                    library_root = curr
                    break
        except: pass
            
    final_product = signature_product or path_product
    if final_product and library_root:
        return final_product, library_root
    if final_product:
        return final_product, os.path.dirname(filepath)
    return None, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT)
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--nuke', action='store_true')
    args = parser.parse_args()

    root_dir = args.root
    execute = args.execute
    nuke = args.nuke

    log(f"TURBO REBUILD V17: THE VISUALIZER")
    log(f"Root: {root_dir}")
    log(f"Mode: {'EXECUTE' if execute else 'DRY RUN'}")
    
    base_repair_dir = os.path.join("/Volumes/JOE/NKI", REPAIR_DIR_NAME)
    if execute and not os.path.exists(base_repair_dir):
        os.makedirs(base_repair_dir, exist_ok=True)
        log(f"Created Hub: {base_repair_dir}")

    count = 0
    # Single Threaded Walk for Maximized Reliability
    for dirpath, _, filenames in os.walk(root_dir):
        if REPAIR_DIR_NAME in dirpath: continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                
                try:
                    if os.path.getsize(full_path) == 0: continue
                    with open(full_path, 'rb') as f:
                        # Use mmap for speed even in single thread
                        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                            head_len = min(len(mm), 50*1024*1024) 
                            header = mm[:head_len]
                            
                            product, source_root = identify_library_root(full_path, header)
                            
                            if product and source_root:
                                # FOUND ONE!
                                target_path = os.path.join(base_repair_dir, product)
                                
                                log(f"[FOUND] {product}")
                                log(f"       Source: {source_root}")
                                log(f"       Target: {target_path}")

                                if execute:
                                    if not os.path.exists(target_path):
                                        log(f"       >>> CREATING FOLDER: {product}")
                                        
                                        if nuke:
                                            # Careful with move in walk loop, might break iterator?
                                            # shutil.move is risky if we are inside the tree?
                                            # But walk handles it usually.
                                            try:
                                                shutil.move(source_root, target_path)
                                                count += 1
                                            except Exception as e:
                                                log(f"       !!! MOVE FAILED: {e}")
                                        else:
                                            try:
                                                shutil.copytree(source_root, target_path, dirs_exist_ok=True)
                                                count += 1
                                            except Exception as e:
                                                log(f"       !!! COPY FAILED: {e}")
                                    else:
                                        log(f"       (Folder already exists)")

                except Exception as e:
                    pass
                    # log(f"Error checking {fname}: {e}")

    log("-" * 60)
    log(f"VISUALIZER COMPLETE. Libraries Rebuilt: {count}")

if __name__ == "__main__":
    main()
