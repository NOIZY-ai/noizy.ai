import os
import re
import argparse
import sys
import datetime

# Setup logging
def log(msg):
    print(msg)
    sys.stdout.flush()

# Heuristic: Common junk strings in NKI headers to ignore
IGNORE_STRINGS = {
    'Konst', 'K4', 'K5', 'NiSound', 'Standard', 'Version', 'Author', 
    'Patch', 'Kontakt', 'Native Instruments', 'Drums', 'Piano', 'Bass', 
    'hsin', 'uacc', 'mod', 'zone', 'group', 's.v.i', 'presets', 'samples',
    'velocity', 'group', 'zone', 'editor'
}

# Regex for printable ASCII strings (4+ chars)
STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def extract_best_name(filepath):
    """
    Attempts to find the internal instrument name.
    Now scans deeper (up to 1MB) as per 'Deep Tunnel' request.
    """
    try:
        with open(filepath, 'rb') as f:
            # Read larger chunk to skip headers - TUNNEL DEEP
            data = f.read(1024 * 1024) # 1MB scan
            
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
                
                # Heuristic: Prefer strings with spaces (likely a title) vs code (CamelCase/underscores)
                candidates.append(s)

            # Log candidates for debugging "Tunnel In"
            if candidates:
                log(f"DEBUG: Candidates for {os.path.basename(filepath)}: {candidates[:10]}...")

            # Simple selection heuristic (can be improved)
            # Find the longest candidates that look like titles (contain spaces)
            title_candidates = [c for c in candidates if ' ' in c]
            if title_candidates:
                return title_candidates[0] # Return first "title-like" string
            
            if candidates:
                return candidates[0] # Fallback

    except Exception as e:
        log(f"Error reading {filepath}: {e}")
        pass
    return None

def clean_filename(name):
    # Remove characters forbidden in filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip()

def process_volume(root_dir, dry_run=True):
    renamed_count = 0
    errors = 0
    
    # Initialize log
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except:
            pass
            
    log(f"Scanning {root_dir}...")
    log(f"Mode: {'DRY RUN (No changes)' if dry_run else 'EXECUTE (Renaming files)'}")
    log("-" * 60)

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                
                # Log that we are touching this file
                # log(f"Processing {fname}...")
                
                internal_name = extract_best_name(full_path)
                
                if internal_name:
                    new_fname = clean_filename(internal_name) + ".nki"
                    
                    # Skip if already correct
                    if new_fname == fname:
                        continue
                        
                    new_full_path = os.path.join(dirpath, new_fname)
                    
                    # Handle duplicates
                    if os.path.exists(new_full_path) and new_fname != fname:
                        # Append counter
                        base, ext = os.path.splitext(new_fname)
                        counter = 1
                        while os.path.exists(os.path.join(dirpath, f"{base}_{counter}{ext}")):
                            counter += 1
                        new_fname = f"{base}_{counter}{ext}"
                        new_full_path = os.path.join(dirpath, new_fname)

                    log(f"[RENAME] '{fname}' -> '{new_fname}'")
                    # log(f"         (Found internal name: '{internal_name}')")

                    if not dry_run:
                        try:
                            os.rename(full_path, new_full_path)
                            renamed_count += 1
                        except Exception as e:
                            log(f"[ERROR] Failed to rename {full_path}: {e}")
                            errors += 1
                    else:
                        renamed_count += 1
                else:
                    # Optional: Print files where no name was found
                    log(f"[SKIP] No suitable name found for '{fname}'")
                    pass

    log("-" * 60)
    log(f"Total processed: {renamed_count}")
    log(f"Errors: {errors}")

def main():
    # Force the root to be the current directory if not provided, or specifically /Volumes/JOE/NKI
    root = "/Volumes/JOE/NKI"
    
    # Simple args handling to avoid complexity in this copy
    # Defaulting to dry run (modify source to enable execute if needed, but safe is better)
    execute = False # Start safely
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--execute":
            execute = True
        elif sys.argv[1] != "":
             root = sys.argv[1]
             
    process_volume(root, dry_run=not execute)

if __name__ == "__main__":
    main()
