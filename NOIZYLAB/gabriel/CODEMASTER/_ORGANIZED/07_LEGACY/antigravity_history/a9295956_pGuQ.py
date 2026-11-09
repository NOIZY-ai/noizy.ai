#!/usr/bin/env python3
"""
================================================================================
█▀▀█ █░░█ █▀▀█ █▀▀▄ █▀▀█   █░░█ █░░ ▀▀█▀▀ ░▀░ █▀▄▀█ █▀▀█ ▀▀█▀▀ █▀▀
█░░█ █░░█ █▄▄▀ █▀▀▄ █░░█   █░░█ █░░ ░░█░░ ▀█▀ █░▀░█ █▄▄█ ░░█░░ █▀▀
▀▀▀▀ ░▀▀▀ ▀░▀▀ ▀▀▀░ ▀▀▀▀   ░▀▀▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀░░░▀ ▀░░▀ ░░▀░░ ▀▀▀
================================================================================
TURBO ULTIMATE v1.0 - THE OMEGA SINGULARITY
================================================================================
CONSOLIDATION: All turbo_* scripts unified into ONE.
FEATURES:
  ◆ OMEGA REGEX: O(1) BFA Product Identification
  ◆ DEEP MMAP:   500MB binary scan depth
  ◆ ARCHITECT:   Moves library trees to central hub
  ◆ HEALER:      Renames NKIs to true internal names
  ◆ CLEANER:     Nukes empty folders
  ◆ CACHE CLEAR: Removes .DS_Store and cache junk
  ◆ PERM FIX:    Repairs file permissions
  ◆ CENTRALIZE:  Moves ALL scripts to central location
  ◆ DATE TRACK:  Tracks overlapping modification times
================================================================================
USAGE:
  python3 TURBO_ULTIMATE.py                    # Dry Run (Safe Preview)
  python3 TURBO_ULTIMATE.py --execute          # Execute (Copy Mode)
  python3 TURBO_ULTIMATE.py --execute --nuke   # Execute (Move Mode)
  python3 TURBO_ULTIMATE.py --centralize       # Centralize all scripts
  python3 TURBO_ULTIMATE.py --clean            # Clean cache + empty dirs
  python3 TURBO_ULTIMATE.py --all              # FULL OPTIMIZATION
================================================================================
"""

import os
import re
import sys
import shutil
import mmap
import argparse
import hashlib
import time
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict

# ==============================================================================
# CONFIGURATION
# ==============================================================================
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"
DEFAULT_ROOT = "/Volumes/JOE"
NKI_ROOT = "/Volumes/JOE/NKI"
CENTRAL_SCRIPTS_DIR = "/Volumes/JOE/NKI/_TURBO_SCRIPTS"
LOG_FILE = "/Volumes/JOE/NKI/turbo_ultimate_log.txt"
DATE_OVERLAP_FILE = "/Volumes/JOE/NKI/date_overlaps.json"
MAX_WORKERS = min((os.cpu_count() or 4) + 8, 24)  # Capped for stability

# Cache patterns to nuke
CACHE_PATTERNS = [
    ".DS_Store", "Thumbs.db", "desktop.ini", ".Spotlight-V100",
    ".fseventsd", ".Trashes", "__pycache__", "*.pyc", ".AppleDouble"
]

# ==============================================================================
# OMEGA SIGNATURES: O(1) PRODUCT IDENTIFICATION
# ==============================================================================
RAW_SIGS: Dict[str, Tuple[str, str]] = {
    "CountryGuitars":    (r"Country.*Guitars",        "BFA - Country Guitars"),
    "AcousticSounds":    (r"Acoustic.*Soundscapes",   "BFA - Acoustic Soundscapes"),
    "BigBadHorns":       (r"Big.*Bad.*Horns",         "BFA - Big Bad Horns"),
    "FirstCall":         (r"First.*Call.*Horns",      "BFA - First Call Horns"),
    "LondonStrings":     (r"London.*Solo.*Strings",   "BFA - London Solo Strings"),
    "CelticInst":        (r"Celtic.*Inst",            "BFA - Celtic Instruments"),
    "QuirkyPop":         (r"Quirky.*Pop",             "BFA - Quirky Pop"),
    "VintageHorns":      (r"Vintage.*Horns",          "BFA - Vintage Horns"),
    "MojoHorn":          (r"Mojo.*Horn",              "BFA - Mojo Horns"),
    "UrbanString":       (r"Urban.*String",           "BFA - Urban Strings"),
    "GypsyCafe":         (r"Gypsy.*Cafe",             "BFA - Gypsy Cafe"),
    "RootsMidEast":      (r"Roots.*Middle.*East",     "BFA - Roots Of Middle East"),
    "RootsSouthAm":      (r"Roots.*South.*Am",        "BFA - Roots Of South America"),
    "AmbientSky":        (r"Ambient.*Skyline",        "BFA - Ambient Skyline"),
    "IndiePop":          (r"Indie.*Pop",              "BFA - Indie Pop"),
    "IndieRock":         (r"Indie.*Rock",             "BFA - Indie Rock"),
    "NuRnB":             (r"Nu.*RnB",                 "BFA - Nu RnB Classics"),
    "RadioPop":          (r"Radio.*Pop",              "BFA - Radio Pop"),
    "Prometheus":        (r"Prometheus",              "BFA - Prometheus"),
    "AlienGuitars":      (r"Alien.*Guitars",          "BFA - Alien Guitars"),
    "Electri6ity":       (r"Electri6ity",             "BFA - Electri6ity"),
    "Acou6tics":         (r"Acou6tics",               "BFA - Acou6tics"),
    "SymBrass":          (r"Symphonic.*Brass",        "BFA - Symphonic Brass"),
    "VintageBigBand":    (r"Vintage.*Big.*Band",      "BFA - Vintage Big Band"),
    "AncientWorld":      (r"Ancient.*World",          "BFA - Ancient World"),
    "EthnoWorld":        (r"Ethno.*World",            "BFA - Ethno World"),
    "Mystica":           (r"Mystica",                 "BFA - Mystica"),
    "Aura":              (r"Aura",                    "BFA - Aura"),
    "Garage":            (r"From.*The.*Garage",       "BFA - From The Garage"),
    "JazzDrums":         (r"Jazz.*Drums",             "BFA - Jazz Drums"),
    "ChronicHorns":      (r"Chronic.*Horns",          "BFA - Chronic Custom Horns"),
    "StringsFX":         (r"Strings.*FX",             "BFA - Strings FX"),
    "DrumsOfWar":        (r"Drums.*Of.*War",          "BFA - Drums Of War"),
    "Lucky7":            (r"Lucky.*7",                "BFA - Lucky 7"),
    "OffTheHook":        (r"Off.*The.*Hook",          "BFA - Off The Hook"),
    "CutItUp":           (r"Cut.*It.*Up",             "BFA - Cut'n It Up"),
    "SuiteGrooves":      (r"Suite.*Grooves",          "BFA - Suite Grooves"),
    "Methodology":       (r"Methodology",             "BFA - Methodology"),
    "LiquidMetal":       (r"Liquid.*Metal",           "BFA - Liquid Metal"),
    "DarkBasement":      (r"Dark.*Basement",          "BFA - Dark Basement Hits"),
    "GuitarLoops":       (r"Guitar.*Loops",           "BFA - Guitar Loops"),
    "ActionDrums":       (r"Action.*Drums",           "BFA - Action Drums"),
    "CinematicDriver":   (r"Cinematic.*Driver",       "BFA - Cinematic Drivers"),
    "Rush":              (r"Rush",                    "BFA - Rush"),
    "Midnight":          (r"Midnight",                "BFA - Midnight"),
    "Vibe":              (r"Vibe",                    "BFA - Vibe"),
    "HeatSeekers":       (r"Heat.*Seekers",           "BFA - Heat Seekers"),
    "Mahidhi":           (r"Mahidhi",                 "BFA - Mahidhi"),
    "PersianGrooves":    (r"Persian.*Grooves",        "BFA - Persian Grooves"),
    "Bollywood":         (r"Bollywood",               "BFA - Bollywood Styles"),
    "HitZone":           (r"Hit.*Zone",               "BFA - Hit Zone"),
    "RappinHood":        (r"Rappin.*Hood",            "BFA - Rappin Hood"),
}

# Compile MEGA REGEX for O(1) matching
regex_parts = [f"(?P<{k}>{v[0]})" for k, v in RAW_SIGS.items()]
OMEGA_REGEX = re.compile("|".join(regex_parts).encode('ascii'), re.IGNORECASE)
STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

# ==============================================================================
# LOGGING
# ==============================================================================
class Logger:
    """Dual-output logger with timestamps."""
    
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.start_time = time.time()
        
    def clear(self):
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
            
    def __call__(self, msg: str, level: str = "INFO"):
        elapsed = time.time() - self.start_time
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}][{elapsed:7.2f}s][{level:5}] {msg}"
        print(formatted)
        sys.stdout.flush()
        try:
            with open(self.log_path, 'a') as f:
                f.write(formatted + "\n")
        except:
            pass

log = Logger(LOG_FILE)

# ==============================================================================
# UTILITIES
# ==============================================================================
def clean_filename(name: str) -> str:
    """Sanitize filename for cross-platform compatibility."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s*-{2,}\s*', ' - ', name)
    name = re.sub(r'\s+', ' ', name)
    # Remove trailing 'a' artifact from some NKI names
    if name.endswith('a') and len(name) > 3:
        name = name[:-1]
    return name.strip()

def get_file_hash(path: str, chunk_size: int = 65536) -> str:
    """Get SHA256 hash of a file for deduplication."""
    hasher = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()[:16]
    except:
        return ""

def get_mod_time(path: str) -> Optional[datetime]:
    """Get modification time of a file."""
    try:
        return datetime.fromtimestamp(os.path.getmtime(path))
    except:
        return None

# ==============================================================================
# CORE: OMEGA IDENTIFICATION ENGINE
# ==============================================================================
def extract_internal_name(mm_data: bytes, scan_limit: int = 500*1024*1024) -> Optional[str]:
    """Deep scan binary for internal instrument name."""
    limit = min(len(mm_data), scan_limit)
    data = mm_data[:limit]
    
    candidates = []
    for match in STRING_RE.finditer(data):
        s = match.group(0).decode('ascii', errors='ignore').strip()
        if not s or len(s) < 3 or len(s) > 80:
            continue
        if any(x in s for x in ['/', '\\', ':', '.nki', '.wav', '.aif', 'www.', '.com', '.ncw']):
            continue
        if "Native Instruments" in s or "Kontakt" in s:
            continue
        candidates.append(s)
    
    if candidates:
        # Heuristic: longest clean string is usually the title
        candidates.sort(key=len, reverse=True)
        return candidates[0]
    return None

def identify_library(filepath: str, mm: mmap.mmap, header: bytes) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Identify library product, root path, and internal name.
    Returns: (product_name, library_root, internal_name)
    """
    # 1. Binary signature match (O(1) via Omega Regex)
    match = OMEGA_REGEX.search(header)
    product_name = None
    if match and match.lastgroup in RAW_SIGS:
        product_name = RAW_SIGS[match.lastgroup][1]
    
    # 2. Path context scan (climb directory tree)
    path_product = None
    library_root = None
    curr = filepath
    
    if not product_name:
        for _ in range(8):  # Scan up to 8 levels
            curr = os.path.dirname(curr)
            dirname = os.path.basename(curr)
            if not dirname or dirname == '/' or "Volumes" in dirname:
                break
            try:
                m = OMEGA_REGEX.search(dirname.encode('ascii', errors='ignore'))
                if m and m.lastgroup in RAW_SIGS:
                    path_product = RAW_SIGS[m.lastgroup][1]
                    library_root = curr
                    break
            except:
                pass
    
    final_product = product_name or path_product
    internal_name = extract_internal_name(mm[:])
    
    # Determine root if not found
    if not library_root:
        curr = filepath
        candidate_root = os.path.dirname(filepath)
        for _ in range(5):
            curr = os.path.dirname(curr)
            if os.path.basename(curr) == "Volumes":
                break
            if os.path.exists(os.path.join(curr, "Documentation")) or \
               os.path.exists(os.path.join(curr, "Samples")):
                candidate_root = curr
                break
        library_root = candidate_root
    
    return final_product, library_root, internal_name

# ==============================================================================
# MODULE: CACHE CLEANER
# ==============================================================================
def clean_cache(root: str, execute: bool = False) -> int:
    """Remove all cache files and system junk."""
    log("=" * 60)
    log("MODULE: CACHE CLEANER")
    log("=" * 60)
    
    count = 0
    for pattern in CACHE_PATTERNS:
        for dirpath, dirnames, filenames in os.walk(root):
            # Clean files
            for fname in filenames:
                if fname == pattern or (pattern.startswith("*.") and fname.endswith(pattern[1:])):
                    full_path = os.path.join(dirpath, fname)
                    if execute:
                        try:
                            os.remove(full_path)
                            log(f"  [NUKED] {full_path}")
                            count += 1
                        except:
                            pass
                    else:
                        log(f"  [DRY] {full_path}")
                        count += 1
            
            # Clean directories
            for dname in dirnames[:]:  # Copy to allow modification
                if dname == pattern:
                    full_path = os.path.join(dirpath, dname)
                    if execute:
                        try:
                            shutil.rmtree(full_path)
                            log(f"  [NUKED DIR] {full_path}")
                            count += 1
                            dirnames.remove(dname)
                        except:
                            pass
                    else:
                        log(f"  [DRY DIR] {full_path}")
                        count += 1
    
    log(f"CACHE CLEANER: {count} items processed")
    return count

# ==============================================================================
# MODULE: EMPTY FOLDER NUKER
# ==============================================================================
def nuke_empty_folders(root: str, execute: bool = False) -> int:
    """Remove all empty directories recursively."""
    log("=" * 60)
    log("MODULE: EMPTY FOLDER NUKER")
    log("=" * 60)
    
    count = 0
    # Walk bottom-up to handle nested empties
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        if not dirnames and not filenames:
            # Skip important directories
            if any(x in dirpath for x in ['.git', 'node_modules', '__pycache__']):
                continue
            if execute:
                try:
                    os.rmdir(dirpath)
                    log(f"  [NUKED] {dirpath}")
                    count += 1
                except:
                    pass
            else:
                log(f"  [DRY] {dirpath}")
                count += 1
    
    log(f"EMPTY FOLDER NUKER: {count} folders processed")
    return count

# ==============================================================================
# MODULE: SCRIPT CENTRALIZER
# ==============================================================================
def centralize_scripts(root: str, execute: bool = False) -> int:
    """Move all turbo_* scripts to central location."""
    log("=" * 60)
    log("MODULE: SCRIPT CENTRALIZER")
    log(f"Target: {CENTRAL_SCRIPTS_DIR}")
    log("=" * 60)
    
    if execute:
        os.makedirs(CENTRAL_SCRIPTS_DIR, exist_ok=True)
    
    count = 0
    script_patterns = ["turbo_*.py", "turbo_*.sh", "cleanup.py", "micro_*.py", "launcher_*.sh"]
    
    for dirpath, _, filenames in os.walk(root):
        if CENTRAL_SCRIPTS_DIR in dirpath:
            continue
        if REPAIR_DIR_NAME in dirpath:
            continue
            
        for fname in filenames:
            for pattern in script_patterns:
                # Simple glob match
                if pattern.startswith("*"):
                    if fname.endswith(pattern[1:]):
                        match = True
                    else:
                        match = False
                elif "*" in pattern:
                    prefix, suffix = pattern.split("*")
                    match = fname.startswith(prefix) and fname.endswith(suffix)
                else:
                    match = fname == pattern
                
                if match:
                    full_path = os.path.join(dirpath, fname)
                    target_path = os.path.join(CENTRAL_SCRIPTS_DIR, fname)
                    
                    # Handle duplicates
                    if os.path.exists(target_path) and full_path != target_path:
                        base, ext = os.path.splitext(fname)
                        c = 1
                        while os.path.exists(os.path.join(CENTRAL_SCRIPTS_DIR, f"{base}_{c}{ext}")):
                            c += 1
                        target_path = os.path.join(CENTRAL_SCRIPTS_DIR, f"{base}_{c}{ext}")
                    
                    if full_path != target_path:
                        if execute:
                            try:
                                shutil.move(full_path, target_path)
                                log(f"  [CENTRALIZED] {fname}")
                                count += 1
                            except Exception as e:
                                log(f"  [ERROR] {fname}: {e}", "ERROR")
                        else:
                            log(f"  [DRY] {fname} -> {target_path}")
                            count += 1
                    break
    
    log(f"SCRIPT CENTRALIZER: {count} scripts processed")
    return count

# ==============================================================================
# MODULE: DATE/TIME OVERLAP TRACKER
# ==============================================================================
def track_date_overlaps(root: str) -> Dict:
    """Track files with overlapping modification times."""
    log("=" * 60)
    log("MODULE: DATE/TIME OVERLAP TRACKER")
    log("=" * 60)
    
    time_buckets: Dict[str, List[str]] = defaultdict(list)
    
    for dirpath, _, filenames in os.walk(root):
        if REPAIR_DIR_NAME in dirpath:
            continue
        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                mod_time = get_mod_time(full_path)
                if mod_time:
                    # Bucket by minute
                    time_key = mod_time.strftime("%Y-%m-%d %H:%M")
                    time_buckets[time_key].append(full_path)
    
    # Find overlaps (same minute)
    overlaps = {k: v for k, v in time_buckets.items() if len(v) > 1}
    
    log(f"Found {len(overlaps)} time buckets with overlapping files")
    for time_key, files in list(overlaps.items())[:5]:  # Show first 5
        log(f"  [{time_key}] {len(files)} files")
    
    # Save to JSON
    import json
    try:
        with open(DATE_OVERLAP_FILE, 'w') as f:
            json.dump({
                "generated": datetime.now().isoformat(),
                "total_overlaps": len(overlaps),
                "overlaps": overlaps
            }, f, indent=2)
        log(f"Saved overlap data to: {DATE_OVERLAP_FILE}")
    except Exception as e:
        log(f"Failed to save overlap data: {e}", "ERROR")
    
    return overlaps

# ==============================================================================
# MODULE: BFA LIBRARY ARCHITECT (Main Rebuild Engine)
# ==============================================================================
def rebuild_libraries(root: str, execute: bool = False, nuke: bool = False) -> Dict:
    """Main BFA library identification and rebuild engine."""
    log("=" * 60)
    log("MODULE: BFA LIBRARY ARCHITECT")
    log(f"Mode: {'EXECUTE' if execute else 'DRY RUN'} | Nuke: {nuke}")
    log("=" * 60)
    
    base_repair_dir = os.path.join(NKI_ROOT, REPAIR_DIR_NAME)
    if execute:
        os.makedirs(base_repair_dir, exist_ok=True)
    
    stats = {'lib_moves': 0, 'file_renames': 0, 'errors': 0, 'scanned': 0}
    detected_libraries: Dict[str, str] = {}
    
    # Fast file discovery via shell
    log("Initializing shell-accelerated scan...")
    try:
        cmd = ["find", root, "-name", "*.nki", "-type", "f"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        nki_files = [p.strip() for p in result.stdout.splitlines() if p.strip()]
        log(f"Shell scan found {len(nki_files)} NKI files")
    except:
        log("Shell scan failed, falling back to os.walk...", "WARN")
        nki_files = []
        for dirpath, _, filenames in os.walk(root):
            if REPAIR_DIR_NAME in dirpath:
                continue
            for fname in filenames:
                if fname.lower().endswith('.nki'):
                    nki_files.append(os.path.join(dirpath, fname))
    
    # Process each NKI
    for full_path in nki_files:
        if REPAIR_DIR_NAME in full_path:
            continue
            
        stats['scanned'] += 1
        fname = os.path.basename(full_path)
        dirpath = os.path.dirname(full_path)
        
        try:
            if os.path.getsize(full_path) == 0:
                continue
            
            with open(full_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    head_len = min(len(mm), 500*1024*1024)
                    header = mm[:head_len]
                    
                    product, lib_root, internal_name = identify_library(full_path, mm, header)
                    
                    # RENAME LOGIC
                    if internal_name:
                        clean_n = clean_filename(internal_name) + ".nki"
                        if clean_n != fname and len(clean_n) > 4:
                            if execute:
                                new_path = os.path.join(dirpath, clean_n)
                                if os.path.exists(new_path):
                                    base, ext = os.path.splitext(clean_n)
                                    c = 1
                                    while os.path.exists(os.path.join(dirpath, f"{base}_{c}{ext}")):
                                        c += 1
                                    clean_n = f"{base}_{c}{ext}"
                                    new_path = os.path.join(dirpath, clean_n)
                                
                                os.rename(full_path, new_path)
                                full_path = new_path
                                stats['file_renames'] += 1
                                log(f"  [RENAME] {fname} -> {clean_n}")
                            else:
                                log(f"  [DRY-RENAME] {fname} -> {clean_n}")
                    
                    # LIBRARY REBUILD LOGIC
                    if product and lib_root:
                        target_lib_path = os.path.join(base_repair_dir, product)
                        
                        if os.path.abspath(lib_root) != os.path.abspath(target_lib_path):
                            if lib_root not in detected_libraries:
                                detected_libraries[lib_root] = product
                                
                                if execute:
                                    if not os.path.exists(target_lib_path):
                                        log(f"  [REBUILD] {product}")
                                        log(f"    Src: {lib_root}")
                                        log(f"    Dst: {target_lib_path}")
                                        
                                        try:
                                            if nuke:
                                                shutil.move(lib_root, target_lib_path)
                                            else:
                                                shutil.copytree(lib_root, target_lib_path, dirs_exist_ok=True)
                                            stats['lib_moves'] += 1
                                        except Exception as e:
                                            log(f"    [ERROR] {e}", "ERROR")
                                            stats['errors'] += 1
                                else:
                                    log(f"  [DRY-REBUILD] {product}: {lib_root}")
                                    stats['lib_moves'] += 1
                                    
        except Exception as e:
            stats['errors'] += 1
    
    log("-" * 60)
    log(f"ARCHITECT COMPLETE:")
    log(f"  Scanned:  {stats['scanned']}")
    log(f"  Renamed:  {stats['file_renames']}")
    log(f"  Rebuilt:  {stats['lib_moves']}")
    log(f"  Errors:   {stats['errors']}")
    
    return stats

# ==============================================================================
# MODULE: PERMISSION FIXER
# ==============================================================================
def fix_permissions(root: str, execute: bool = False) -> int:
    """Fix file permissions for all files."""
    log("=" * 60)
    log("MODULE: PERMISSION FIXER")
    log("=" * 60)
    
    if not execute:
        log("DRY RUN: Would fix permissions on all files")
        return 0
    
    count = 0
    try:
        # Use shell for speed
        subprocess.run(["chmod", "-R", "755", root], check=True, capture_output=True)
        log(f"  Fixed permissions on: {root}")
        count = 1
    except Exception as e:
        log(f"  Permission fix failed: {e}", "ERROR")
    
    # Clear quarantine attributes
    try:
        subprocess.run(["xattr", "-rc", root], capture_output=True)
        log(f"  Cleared quarantine attributes")
    except:
        pass
    
    return count

# ==============================================================================
# MAIN ORCHESTRATOR
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="TURBO ULTIMATE - The Omega Singularity Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('root', nargs='?', default=DEFAULT_ROOT,
                        help="Root directory to scan")
    parser.add_argument('--execute', action='store_true',
                        help="Execute operations (default: dry run)")
    parser.add_argument('--nuke', action='store_true',
                        help="Move instead of copy (destructive)")
    parser.add_argument('--clean', action='store_true',
                        help="Clean cache and empty folders only")
    parser.add_argument('--centralize', action='store_true',
                        help="Centralize all scripts only")
    parser.add_argument('--overlaps', action='store_true',
                        help="Track date/time overlaps only")
    parser.add_argument('--permissions', action='store_true',
                        help="Fix permissions only")
    parser.add_argument('--all', action='store_true',
                        help="Run ALL optimization modules")
    
    args = parser.parse_args()
    
    # Initialize
    log.clear()
    start_time = time.time()
    
    log("=" * 60)
    log("█▀▀█ █░░█ █▀▀█ █▀▀▄ █▀▀█   █░░█ █░░ ▀▀█▀▀ ░▀░ █▀▄▀█ █▀▀█ ▀▀█▀▀ █▀▀")
    log("█░░█ █░░█ █▄▄▀ █▀▀▄ █░░█   █░░█ █░░ ░░█░░ ▀█▀ █░▀░█ █▄▄█ ░░█░░ █▀▀")
    log("▀▀▀▀ ░▀▀▀ ▀░▀▀ ▀▀▀░ ▀▀▀▀   ░▀▀▀ ▀▀▀ ░░▀░░ ▀▀▀ ▀░░░▀ ▀░░▀ ░░▀░░ ▀▀▀")
    log("=" * 60)
    log(f"Root:     {args.root}")
    log(f"Execute:  {args.execute}")
    log(f"Nuke:     {args.nuke}")
    log(f"Workers:  {MAX_WORKERS}")
    log(f"Started:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=" * 60)
    
    total_ops = 0
    
    # Execute requested modules
    if args.all or args.clean:
        total_ops += clean_cache(args.root, args.execute)
        total_ops += nuke_empty_folders(args.root, args.execute)
    
    if args.all or args.centralize:
        total_ops += centralize_scripts(args.root, args.execute)
    
    if args.all or args.overlaps:
        track_date_overlaps(args.root)
    
    if args.all or args.permissions:
        total_ops += fix_permissions(args.root, args.execute)
    
    # Default: rebuild libraries if no specific module requested
    if not any([args.clean, args.centralize, args.overlaps, args.permissions]) or args.all:
        stats = rebuild_libraries(args.root, args.execute, args.nuke)
        total_ops += stats['lib_moves'] + stats['file_renames']
    
    # Summary
    elapsed = time.time() - start_time
    log("=" * 60)
    log("█▀▀ █▀▀█ █▀▄▀█ █▀▀█ █░░ █▀▀ ▀▀█▀▀ █▀▀")
    log("█░░ █░░█ █░▀░█ █▄▄█ █░░ █▀▀ ░░█░░ █▀▀")
    log("▀▀▀ ▀▀▀▀ ▀░░░▀ ▀░░▀ ▀▀▀ ▀▀▀ ░░▀░░ ▀▀▀")
    log("=" * 60)
    log(f"Total Operations: {total_ops}")
    log(f"Elapsed Time:     {elapsed:.2f}s")
    log(f"Log File:         {LOG_FILE}")
    log("=" * 60)
    
    if not args.execute:
        log("")
        log("⚠️  DRY RUN COMPLETE - No changes made!")
        log("    Add --execute to apply changes")
        log("    Add --execute --nuke for destructive mode")

if __name__ == "__main__":
    main()
