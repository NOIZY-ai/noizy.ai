import os
import shutil
import struct
import re

# CONFIG
ROOT_DIR = "/Volumes/6TB/Sample_Libraries"
ORGANIZED_ROOT = os.path.join(ROOT_DIR, "_ORGANIZED_WORLDS")

print(f"🌍 WORLD BUILDER ACTIVATED")
print(f"🎯 Making the worlds right in: {ROOT_DIR}")

# UTILS
def sanitize_filename(name):
    # Keep alphanumeric, spaces, hyphens
    clean = re.sub(r'[^a-zA-Z0-9 \-_]', '', name)
    return clean.strip()

def get_aiff_metadata(path):
    # Simple grab of Name/Title
    try:
        with open(path, 'rb') as f:
            header = f.read(12)
            if header[:4] != b'FORM': return None
            size = os.path.getsize(path)
            while f.tell() < size:
                chunk_header = f.read(8)
                if len(chunk_header) < 8: break
                cid = chunk_header[:4]
                csize = struct.unpack('>I', chunk_header[4:])[0]
                
                if cid == b'NAME':
                    return f.read(csize).decode('ascii', errors='ignore').strip()
                else:
                    f.seek(csize, 1)
                    if csize % 2 != 0: f.seek(1, 1)
    except:
        pass
    return None

# EXECUTION
renamed_count = 0
moved_count = 0

for root, dirs, files in os.walk(ROOT_DIR):
    # Skip our own output dir to avoid loops
    if "_ORGANIZED_WORLDS" in root:
        continue
        
    for file in files:
        if file.startswith("."): continue
        
        path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        
        # ACTION 1: HEAL NAMES (Rename cryptic files if they have titles)
        # Focus on the "EL-A..." files found in report
        if ext in ['.aif', '.aiff'] and file.startswith("EL-"):
            title = get_aiff_metadata(path)
            if title and title != os.path.splitext(file)[0]:
                # Construct new name
                new_name = sanitize_filename(title) + ext
                new_path = os.path.join(root, new_name)
                
                # check collision
                if not os.path.exists(new_path):
                    shutil.move(path, new_path)
                    # print(f"✨ Renamed: {file} -> {new_name}")
                    renamed_count += 1
                
        # ACTION 2: ORGANIZE LOOSE/GENERIC ITEMS
        # If we find "Acid" or "Sonic Foundry" loops that are NOT in a specific library folder
        # (Heuristic: path doesn't contain "Sample_Libraries" sub-folders we know are good)
        # Actually, let's just ensure they are grouped.
        
        # For this pass, we stick to "Heal Names" as the primary visible "Righting of the World"
        # and standardizing extensions.
        
        # ACTION 3: LOWERCASE EXTENSIONS (Standardize)
        # .AIF -> .aif
        if ext.isupper():
            new_name = os.path.splitext(file)[0] + ext.lower()
            new_path = os.path.join(root, new_name)
            if not os.path.exists(new_path):
                shutil.move(path, new_path)
                renamed_count += 1

print(f"✨ RENAMING COMPLETE")
print(f"- Files Healed (Renamed/Standardized): {renamed_count}")
print(f"🌍 The naming convention is now righteous.")
