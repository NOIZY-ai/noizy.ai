import sys
import os
import json
import argparse
from noizy_memcell import memory_core

# NOIZYLAB SEARCH v3.0
# "The Librarian" Module: Search Database
# OPTIMIZED: MemCell v3.0 Logging, Zero Latency

print(">>> [NOIZYLAB LIBRARIAN v3.0] INITIALIZING...")

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

def search_library(bpm_range=None, key=None, min_energy=None):
    print("\n>>> [NOIZY LIBRARIAN] SEARCHING ARCHIVES...")
    memory_core.log_interaction("Search Query Initiated", "QUERY_START", "DIRECTOR")
    
    data = load_db()
    if not data:
        print("!!! LIBRARY IS EMPTY.")
        return

    # Optimized Filtering
    results = data
    
    if bpm_range:
        results = [t for t in results if bpm_range[0] <= t.get("bpm", 0) <= bpm_range[1]]
        
    if key:
        k_lower = key.lower()
        results = [t for t in results if k_lower in t.get("key", "").lower()]
        
    if min_energy:
        results = [t for t in results if t.get("energy_db", -100) >= min_energy]

    print(f"    -> FOUND {len(results)} MATCHES.")
    memory_core.log_interaction(f"Found {len(results)} matches", "QUERY_SUCCESS", "SHIRL")
    
    print("----------------------------------------------------------------")
    print(f"{'FILENAME':<40} | {'BPM':<6} | {'KEY':<4} | {'ENERGY':<6}")
    print("----------------------------------------------------------------")
    for r in results[:20]: # Show top 20
        print(f"{r.get('file', 'Unknown')[-40:]:<40} | {r.get('bpm', 0):<6.1f} | {r.get('key', '-'):<4} | {r.get('energy_db', 0):<6.1f}")
        
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
