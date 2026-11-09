import json
import re
import argparse
from pathlib import Path
from collections import defaultdict

INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Intelligence Heuristics
PATTERNS = {
    "bpm": re.compile(r"(\d{2,3})\s?bpm", re.IGNORECASE),
    "key": re.compile(r"\b([A-G][#b]?m?)\b"), # Simple key matcher (e.g. Am, F#)
    "type_kick": re.compile(r"kick|bd|bassdrum", re.IGNORECASE),
    "type_snare": re.compile(r"snare|sd|rim", re.IGNORECASE),
    "type_hat": re.compile(r"hat|hh|cymbal|ride|crash", re.IGNORECASE),
    "type_bass": re.compile(r"bass|sub|808", re.IGNORECASE),
    "type_loop": re.compile(r"loop", re.IGNORECASE),
    "type_vocal": re.compile(r"vocal|vox|acapella", re.IGNORECASE),
    "type_fx": re.compile(r"fx|sfx|noise|riser|impact", re.IGNORECASE),
}

def load_index():
    try:
        with open(INDEX_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

def save_index(data):
    with open(INDEX_PATH, 'w') as f:
        json.dump(data, f) # Save tagging results back

def tag_library():
    data = load_index()
    if not data:
        print("❌ Oracle Database not found.")
        return

    print("🧠 ACTIVATING SMART TAGGER (AI HEURISTICS)...")
    
    files = data.get('files', [])
    tags_db = {} # Maps filepath -> {tags}
    
    tagged_count = 0
    stats = defaultdict(int)
    
    for fpath in files:
        fname = Path(fpath).name
        f_lower = fname.lower()
        
        file_tags = {}
        
        # BPM
        bpm_match = PATTERNS["bpm"].search(f_lower)
        if bpm_match:
            file_tags['bpm'] = int(bpm_match.group(1))
            stats['bpm'] += 1
            
        # Key
        key_match = PATTERNS["key"].search(fname) # Case sensitive for keys usually better
        if key_match:
            file_tags['key'] = key_match.group(1)
            stats['key'] += 1
            
        # Types
        found_type = False
        for p_name, p_regex in PATTERNS.items():
            if p_name.startswith("type_") and p_regex.search(f_lower):
                t_name = p_name.replace("type_", "")
                file_tags['type'] = t_name
                stats[f"type_{t_name}"] += 1
                found_type = True
                break
        
        if file_tags:
            tags_db[fpath] = file_tags
            tagged_count += 1

    # Save enhanced metadata
    # We store it in a new section 'tags' to preserve raw file list speed
    data['tags'] = tags_db
    save_index(data)
    
    print(f"\n✅ SMART TAGGING COMPLETE")
    print(f"   Tagged Files: {tagged_count:,} / {len(files):,}")
    print(f"\n📊 Intelligence Report:")
    print(f"   BPM Detected:  {stats['bpm']:,} files")
    print(f"   Keys Detected: {stats['key']:,} files")
    print(f"   Samples Classified:")
    for k, v in sorted(stats.items()):
        if k.startswith("type_"):
            print(f"     - {k.replace('type_', '').title()}: \t{v:,}")

if __name__ == "__main__":
    tag_library()
