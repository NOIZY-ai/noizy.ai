import os
import re
import argparse
import sys
import shutil

# Heuristic: Common junk strings in NKI headers to ignore
IGNORE_STRINGS = {
    'Konst', 'K4', 'K5', 'NiSound', 'Standard', 'Version', 'Author', 
    'Patch', 'Kontakt', 'Native Instruments', 'Drums', 'Piano', 'Bass' # Generic terms might be dangerous to ignore if they ARE the name, but usually they are metadata keys.
    # We will refine to be permissive but prefer longer, specific strings.
}

# Regex for printable ASCII strings (4+ chars)
STRING_RE = re.compile(rb'([\x20-\x7E]{4,})')

def extract_best_name(filepath):
    """
    Attempts to find the internal instrument name.
    Strategy: Return the FIRST string that:
    1. Is not in IGNORE_STRINGS
    2. Doesn't look like a file path (contains / or \)
    3. Is 4-50 chars long
    """
    try:
        with open(filepath, 'rb') as f:
            # Read first 4KB - header usually contains the name early on
            data = f.read(4096)
            
            for match in STRING_RE.finditer(data):
                s = match.group(0).decode('ascii', errors='ignore').strip()
                
                # Filter junk
                if not s or len(s) < 4 or len(s) > 60:
                    continue
                if any(x in s for x in ['/', '\\', ':', '.nki', '.wav', '.aif']): # internal paths/extensions
                    continue
                if s in IGNORE_STRINGS:
                    continue
                
                # Heuristic: The name often appears early. 
                # If we passed filters, this is our best guess.
                return s
    except Exception as e:
        pass
    return None

def clean_filename(name):
    # Remove characters forbidden in filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip()

def process_volume(root_dir, dry_run=True):
    renamed_count = 0
    errors = 0
    
    print(f"Scanning {root_dir}...")
    print(f"Mode: {'DRY RUN (No changes)' if dry_run else 'EXECUTE (Renaming files)'}")
    print("-" * 60)

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.lower().endswith('.nki'):
                full_path = os.path.join(dirpath, fname)
                
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

                    print(f"[RENAME] '{fname}' -> '{new_fname}'")
                    # print(f"         (Found internal name: '{internal_name}')")

                    if not dry_run:
                        try:
                            os.rename(full_path, new_full_path)
                            renamed_count += 1
                        except Exception as e:
                            print(f"[ERROR] Failed to rename {full_path}: {e}")
                            errors += 1
                    else:
                        renamed_count += 1
                else:
                    # Optional: Print files where no name was found
                    # print(f"[SKIP] No suitable name found for '{fname}'")
                    pass

    print("-" * 60)
    print(f"Total processed: {renamed_count}")
    print(f"Errors: {errors}")

def main():
    parser = argparse.ArgumentParser(description="Rename NKI files to their internal original names.")
    parser.add_argument('root', help="Root directory to scan (e.g. /Volumes/JOE)")
    parser.add_argument('--execute', action='store_true', help="Actually rename files. Default is DRY RUN.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.root):
        print(f"Error: Path {args.root} does not exist.")
        sys.exit(1)
        
    process_volume(args.root, dry_run=not args.execute)

if __name__ == "__main__":
    main()
