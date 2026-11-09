import os
import re
import shutil
import sys
import argparse

# Configuration
LOG_FILE = "scan_log.txt"
REPAIR_DIR_NAME = "_KTK_To_Fix_2026"

def log(msg):
    # Print to stdout for user visibility
    print(msg)
    sys.stdout.flush()

# Heuristic: Common junk strings in NKI headers to ignore
IGNORE_STRINGS = {
    'Konst', 'K4', 'K5', 'NiSound', 'Standard', 'Version', 'Author', 
    'Patch', 'Kontakt', 'Native Instruments', 'Drums', 'Piano', 'Bass', 
    'hsin', 'uacc', 'mod', 'zone', 'group', 's.v.i', 'presets', 'samples',
    'velocity', 'group', 'zone', 'editor', 'joypad', 'normal', 'high', 'low'
}

# Regex for printable ASCII strings (4+ chars)
STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def extract_best_name(filepath):
    try:
        with open(filepath, 'rb') as f:
            # Deep Scan 1MB
            data = f.read(1024 * 1024) 
            
            matches = []
            for match in STRING_RE.finditer(data):
                s = match.group(0).decode('ascii', errors='ignore').strip()
                matches.append(s)

            candidates = []
            for s in matches:
                # Filter junk
                if not s or len(s) < 4 or len(s) > 60: 
                    continue
                if any(x in s for x in ['/', '\\', ':', '.nki', '.wav', '.aif', 'www.', '.com', '.ncw']): 
                    continue
                if any(ignored.lower() == s.lower() for ignored in IGNORE_STRINGS):
                    continue
                
                candidates.append(s)

            # Heuristic: Prefer strings with spaces (Title Case likely)
            title_candidates = [c for c in candidates if ' ' in c]
            if title_candidates:
                return title_candidates[0]
            
            if candidates:
                return candidates[0]

    except Exception as e:
        log(f"Error reading {filepath}: {e}")
    return None

def clean_filename(name):
    # Remove forbidden chars
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip()
    
    # User Request: Cleanup double dashes (never allowed) and multiple spaces
    # matches "--", " - -", "---", etc. and replaces with single " - "
    name = re.sub(r'\s*-{2,}\s*', ' - ', name)
    name = re.sub(r'\s+', ' ', name)

    # User Request: Remove specific trailing lowercase 'a' artifact
    # e.g. "Bass Enda" -> "Bass End"
    if name.endswith('a'):
        name = name[:-1]
        
    return name.strip()

def process_volume(root_dir, active_execute=False):
    log(f"TURBO SCAN V4: Safe Repair Mode")
    log(f"Scanning Root: {root_dir}")
    log(f"Target Directory: {os.path.join(root_dir, REPAIR_DIR_NAME)}")
    log("-" * 60)

    # Ensure target exists
    target_dir = os.path.join(root_dir, REPAIR_DIR_NAME)
    if active_execute:
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
                log(f"Created directory: {target_dir}")
            except Exception as e:
                log(f"CRITICAL: Could not create {target_dir}: {e}")
                return

    processed = 0
    copied = 0

    for dirpath, _, filenames in os.walk(root_dir):
        # Skip the repair directory itself to avoid loops
        if REPAIR_DIR_NAME in dirpath:
            continue

        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                processed += 1
                
                internal_name = extract_best_name(full_path)
                
                if internal_name:
                    clean_name = clean_filename(internal_name) + ".nki"
                    
                    # Logic: Only copy if the name is noticeably different or cleaner?
                    # Actually, for "Reconstruct", we copy EVERYTHING that has a valid internal name.
                    
                    dest_path = os.path.join(target_dir, clean_name)
                    
                    # Handle duplicates in destination
                    if active_execute and os.path.exists(dest_path):
                         base, ext = os.path.splitext(clean_name)
                         counter = 1
                         while os.path.exists(os.path.join(target_dir, f"{base}_{counter}{ext}")):
                             counter += 1
                         dest_path = os.path.join(target_dir, f"{base}_{counter}{ext}")

                    if clean_name != fname:
                        log(f"[FOUND] {fname} -> {os.path.basename(dest_path)} (Internal: {internal_name})")
                    else:
                         log(f"[VERIFIED] {fname} matches internal name.")

                    if active_execute:
                        try:
                            # COPY instead of rename
                            shutil.copy2(full_path, dest_path)
                            copied += 1
                        except Exception as e:
                            log(f"Error copying {fname}: {e}")
                else:
                    log(f"[SKIP] No internal name found in {fname}")

    log("-" * 60)
    log(f"Total Scanned: {processed}")
    log(f"Total Copied to {REPAIR_DIR_NAME}: {copied}")

def main():
    root = "/Volumes/JOE/NKI"
    
    # Check for execute flag or custom root
    execute = False
    if "--execute" in sys.argv:
        execute = True
    
    # Optional root arg
    for arg in sys.argv[1:]:
        if arg != "--execute" and not arg.startswith("-"):
            root = arg

    if not execute:
        log("DRY RUN MODE. Pass --execute to actually copy files.")
    
    process_volume(root, active_execute=execute)

if __name__ == "__main__":
    main()
