import sys
import os
import json
import argparse

# NOIZYLAB LIBRARIAN v1.0
# "Source" Module: Intelligent Asset Retrieval
# Purpose: Find the perfect sound for the "Flow".

# Database file (populated by The Guardian / deep_audio_scan)
DB_FILE = "noizylab_library.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def search_library(bpm_range=None, key=None, min_energy=None, mood=None):
    print("\n>>> [NOIZY LIBRARIAN] SEARCHING ARCHIVES...")
    data = load_db()
    if not data:
        print("!!! LIBRARY IS EMPTY.")
        print("    -> Run 'deep_audio_scan.py' or 'the_guardian.py' first to build the index.")
        return

    results = []
    
    for track in data:
        # Check BPM
        if bpm_range:
            t_bpm = track.get("bpm", 0)
            if not (bpm_range[0] <= t_bpm <= bpm_range[1]):
                continue
                
        # Check Key
        if key:
            t_key = track.get("key", "").lower()
            if key.lower() not in t_key:
                continue
                
        # Check Energy
        if min_energy:
            t_eng = track.get("energy_db", -100)
            if t_eng < min_energy:
                continue

        results.append(track)
        
    # Sort by relevance? Or just list
    print(f"    -> FOUND {len(results)} MATCHES.")
    print("----------------------------------------------------------------")
    print(f"{'FILENAME':<40} | {'BPM':<6} | {'KEY':<4} | {'ENERGY':<6}")
    print("----------------------------------------------------------------")
    for r in results[:20]: # Show top 20
        print(f"{r.get('file', 'Unknown'):<40} | {r.get('bpm', 0):<6.1f} | {r.get('key', '-'):<4} | {r.get('energy_db', 0):<6.1f}")
    if len(results) > 20:
        print(f"... and {len(results)-20} more.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NoizyLab Intelligent Search")
    parser.add_argument("--bpm", help="BPM range (e.g. 120-130)", type=str)
    parser.add_argument("--key", help="Musical Key (e.g. 'C', 'F#', 'Am')", type=str)
    parser.add_argument("--energy", help="Minimum Energy dB (e.g. -20)", type=float)
    
    args = parser.parse_args()
    
    bpm_r = None
    if args.bpm:
        parts = args.bpm.split('-')
        bpm_r = (float(parts[0]), float(parts[1]))
        
    search_library(bpm_range=bpm_r, key=args.key, min_energy=args.energy)
