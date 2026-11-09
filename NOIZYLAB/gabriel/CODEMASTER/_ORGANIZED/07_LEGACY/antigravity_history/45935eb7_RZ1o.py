import os
import shutil
import struct
import re
import sys
from datetime import datetime

# INTELLIGENCE INTEGRATION
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from memcell_core import MemCellCore
except ImportError:
    MemCellCore = None # Fallback

# CONFIG
ROOT_DIR = "/Volumes/6TB/Sample_Libraries"
ORGANIZED_ROOT = os.path.join(ROOT_DIR, "_ORGANIZED_WORLDS")

class TurboWorldHealer:
    def __init__(self):
        self.memcell = MemCellCore() if MemCellCore else None
        self.renamed_count = 0
        self.scanned_count = 0
        self.logs = []

    def log(self, msg):
        print(msg)
        self.logs.append(msg)
        if self.memcell and "Renamed" in msg:
            self.memcell.collect(subject=msg, context={"tool": "TurboWorldHealer"})

    def sanitize_filename(self, name):
        # Keep alphanumeric, spaces, hyphens
        clean = re.sub(r'[^a-zA-Z0-9 \-_]', '', name)
        return clean.strip()

    def get_aiff_metadata(self, path):
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

    def heal_world(self):
        self.log(f"🌍 WORLD BUILDER ACTIVATED")
        self.log(f"🎯 Healing filenames in: {ROOT_DIR}")
        
        for root, dirs, files in os.walk(ROOT_DIR):
            # Skip our own output dir to avoid loops
            if "_ORGANIZED_WORLDS" in root:
                continue
                
            for file in files:
                if file.startswith("."): continue
                self.scanned_count += 1
                
                path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                # ACTION 1: HEAL NAMES (Rename cryptic files if they have titles)
                # Focus on the "EL-A..." files found in report
                if ext in ['.aif', '.aiff'] and file.startswith("EL-"):
                    title = self.get_aiff_metadata(path)
                    if title and title != os.path.splitext(file)[0]:
                        # Construct new name
                        new_name = self.sanitize_filename(title) + ext
                        new_path = os.path.join(root, new_name)
                        
                        # check collision
                        if not os.path.exists(new_path):
                            shutil.move(path, new_path)
                            self.log(f"✨ Renamed: {file} -> {new_name}")
                            self.renamed_count += 1
                        
                # ACTION 2: LOWERCASE EXTENSIONS (Standardize)
                # .AIF -> .aif
                if ext.isupper():
                    new_name = os.path.splitext(file)[0] + ext.lower()
                    new_path = os.path.join(root, new_name)
                    if not os.path.exists(new_path):
                        shutil.move(path, new_path)
                        self.renamed_count += 1

        self.log(f"✨ RENAMING COMPLETE")
        self.log(f"- Files Scanned: {self.scanned_count}")
        self.log(f"- Files Healed: {self.renamed_count}")
        self.log(f"🌍 The naming convention is now righteous.")
        return {"renamed": self.renamed_count, "logs": self.logs}

if __name__ == "__main__":
    healer = TurboWorldHealer()
    healer.heal_world()
