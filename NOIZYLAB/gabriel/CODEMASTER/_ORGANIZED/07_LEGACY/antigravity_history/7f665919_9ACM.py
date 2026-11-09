import os
import sys
import re
import subprocess
from pathlib import Path

# Configuration
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Reuse patterns from turbo_indexer (Simplified)
PATTERNS = {
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), 
}

def get_smart_metadata(filename):
    f_lower = filename.lower()
    bpm = None
    key = None
    
    # BPM
    bpm_match = PATTERNS["bpm"].search(f_lower)
    if bpm_match:
        try: bpm = int(bpm_match.group(1))
        except: pass
        
    # Key
    key_match = PATTERNS["key"].search(filename) # Case sensitive for Key often
    if key_match:
        key = key_match.group(1)
        
    return bpm, key

def set_xattr(file_path, key, value):
    try:
        # xattr -w <key> <value> <file>
        # User <value> must be string
        subprocess.run(["xattr", "-w", key, str(value), str(file_path)], check=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def run_librarian(target_dir):
    print(f"{BOLD}{CYAN}📚 TURBO LIBRARIAN: DEEP METADATA INJECTOR{RESET}")
    print(f"   Target: {target_dir}")
    print(f"   Method: MacOS Extended Attributes (Spotlight/Finder Safe)")
    
    root_path = Path(target_dir)
    if not root_path.exists():
        print(f"   {RED}❌ Target not found.{RESET}")
        return

    files_processed = 0
    tags_injected = 0
    
    # Supported Attributes
    # kMDItemTempo (BPM)
    # kMDItemKeySignature (Key)
    # kMDItemMusicalGenre (Tags/Genre)
    # kMDItemAuthors (Artist)
    # kMDItemComment (Comments)
    
    for root, dirs, files in os.walk(root_path):
        for f in files:
            if f.startswith('.'): continue
            
            fpath = Path(root) / f
            bpm, key = get_smart_metadata(f)
            
            injected = False
            
            # AUTHORS
            if set_xattr(fpath, "com.apple.metadata:kMDItemAuthors", "Audio Unitor AI"):
                injected = True
                
            # BPM
            if bpm:
                if set_xattr(fpath, "com.apple.metadata:kMDItemTempo", bpm):
                    # print(f"   Set BPM: {bpm}")
                    injected = True
            
            # KEY
            if key:
                if set_xattr(fpath, "com.apple.metadata:kMDItemKeySignature", key):
                    # print(f"   Set KEY: {key}")
                    injected = True
                    
            if injected:
                # print(f"   ✅ Tagged: {f}")
                tags_injected += 1
                
            files_processed += 1
            if files_processed % 100 == 0:
                print(f"   ...processed {files_processed} files...")

    print(f"\n{GREEN}✨ LIBRARY CATALOGED{RESET}")
    print(f"   Scanned: {files_processed}")
    print(f"   Injected: {tags_injected}")
    print(f"   Note: Tags are visible in Finder & Spotlight.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 turbo_librarian.py <target_dir>")
    else:
        run_librarian(sys.argv[1])
