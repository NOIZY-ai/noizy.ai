import os
import re
import json
import time
from pathlib import Path
from datetime import datetime

# Identity
NAME = "THE ARCHAEOLOGIST"
VERSION = "38.0"

# Configuration
LIBRARY_ROOT = Path.expanduser(Path("~/Universal/Library/Music"))

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def parse_nfo(nfo_path):
    data = {"year": None, "genre": None, "source": None}
    try:
        with open(nfo_path, 'r', errors='ignore') as f:
            content = f.read()
            
            # Year Regex (Simple 4 digit year, usually surrounded by spacing or brackets)
            year_match = re.search(r'\b(19|20)\d{2}\b', content)
            if year_match: data["year"] = int(year_match.group(0))
            
            # Genre
            genre_match = re.search(r'Genre\s*[:\.]\s*([A-Za-z &]+)', content, re.IGNORECASE)
            if genre_match: data["genre"] = genre_match.group(1).strip()
            
            # Source
            if "FLAC" in content: data["source"] = "FLAC"
            elif "320kbps" in content: data["source"] = "MP3-320"
            elif "V0" in content: data["source"] = "MP3-V0"
            
    except: pass
    return data

def parse_log(log_path):
    data = {"verified": False, "score": 0}
    try:
        with open(log_path, 'r', errors='ignore') as f:
            content = f.read()
            if "No errors occurred" in content:
                data["verified"] = True
                data["score"] = 100
            elif "Test & Copy OK" in content:
                data["verified"] = True
                data["score"] = 100
            
            match = re.search(r'Score\s+(\d+)%', content)
            if match: data["score"] = int(match.group(1))
            
    except: pass
    return data

def parse_cue(cue_path):
    tracks = []
    try:
        current_track = {}
        with open(cue_path, 'r', errors='ignore') as f:
            lines = f.readlines()
            
        album_performer = None
        album_title = None
        
        for line in lines:
            line = line.strip()
            if line.startswith("PERFORMER") and not album_performer:
                album_performer = re.search(r'"(.*)"', line).group(1)
            elif line.startswith("TITLE") and not album_title:
                album_title = re.search(r'"(.*)"', line).group(1)
            
            elif line.startswith("TRACK"):
                if current_track: tracks.append(current_track)
                current_track = {"num": re.search(r'\d+', line).group(0)}
            
            elif line.startswith("TITLE") and current_track:
                current_track["title"] = re.search(r'"(.*)"', line).group(1)
            
            elif line.startswith("PERFORMER") and current_track:
                current_track["artist"] = re.search(r'"(.*)"', line).group(1)
            
            elif line.startswith("INDEX 01") and current_track:
                current_track["start_time"] = re.search(r'\d{2}:\d{2}:\d{2}', line).group(0)

        if current_track: tracks.append(current_track)
        
    except: pass
    return {"performer": album_performer, "title": album_title, "tracks": tracks}

def run_archaeologist(root_dir):
    print(f"{BOLD}{CYAN}🏺 THE ARCHAEOLOGIST: DIGGING FOR ARTIFACTS...{RESET}")
    print(f"   Root: {root_dir}")
    
    artifacts = []
    for root, dirs, files in os.walk(root_dir):
        # Look for Sidecars
        cue_files = [f for f in files if f.endswith('.cue')]
        log_files = [f for f in files if f.endswith('.log')]
        nfo_files = [f for f in files if f.endswith('.nfo')]
        
        if cue_files or log_files or nfo_files:
            folder_info = {
                "path": root,
                "nfo_data": {},
                "log_data": {},
                "cue_data": {}
            }
            
            for nfo in nfo_files:
                folder_info["nfo_data"] = parse_nfo(Path(root) / nfo)
            for log in log_files:
                folder_info["log_data"] = parse_log(Path(root) / log)
            for cue in cue_files:
                folder_info["cue_data"] = parse_cue(Path(root) / cue)
            
            artifacts.append(folder_info)

    print(f"   Found {len(artifacts)} Sites with Artifacts.")
    
    for site in artifacts:
        nfo = site["nfo_data"]
        log = site["log_data"]
        cue = site["cue_data"]
        
        info_str = []
        if nfo.get("year"): info_str.append(f"Year: {nfo['year']}")
        if nfo.get("genre"): info_str.append(f"Genre: {nfo['genre']}")
        if log.get("verified"): info_str.append(f"{GREEN}VERIFIED RIP (100%){RESET}")
        elif log: info_str.append(f"{YELLOW}Log Score: {log.get('score')}%{RESET}")
        if cue.get("tracks"): info_str.append(f"Cue: {len(cue['tracks'])} Tracks")
        
        if info_str:
            print(f"   📍 {Path(site['path']).name}: {', '.join(info_str)}")

    # Integration: Write to a specialized JSON for Keith to consume?
    # Or just print for now as User Verification.
    
    return artifacts

if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else LIBRARY_ROOT
    if target.exists():
        run_archaeologist(target)
    else:
         print(f"{RED}Library not found at {target}{RESET}")
