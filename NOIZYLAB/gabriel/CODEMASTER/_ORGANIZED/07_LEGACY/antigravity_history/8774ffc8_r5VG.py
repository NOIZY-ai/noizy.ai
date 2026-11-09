import sys
import json
import datetime
from pathlib import Path

# Config
WINDOW_HOURS = 4
NOW = datetime.datetime.now()
WINDOW_START = NOW - datetime.timedelta(hours=WINDOW_HOURS)

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")

def normalize(text):
    return " ".join(text.strip().lower().split())

def main():
    if not DB_PATH.exists():
        print("BLOCKED: DB not found.")
        sys.exit(1)
        
    with open(DB_PATH) as f:
        db = json.load(f)
        
    # 1. Filter Window
    sweep_entries = []
    for m in db:
        try:
            ts = datetime.datetime.fromisoformat(m['timestamp'])
            if ts >= WINDOW_START:
                sweep_entries.append(m)
        except:
            continue
            
    if not sweep_entries:
        print("NO CHANGES DETECTED IN WINDOW")
        return

    # 2. Keying (Dedupe)
    clusters = {}
    
    for m in sweep_entries:
        key = normalize(m['content'])
        # Simple clustering by exact active content match for this speed
        # For "Similarity", we basically just check if key is in clusters
        if key not in clusters:
            clusters[key] = []
        clusters[key].append(m)
        
    # 3. Consolidate to GOLD
    gold_entries = []
    clusters_output = []
    
    for key, members in clusters.items():
        # Sort by timestamp, newest first
        members.sort(key=lambda x: x['timestamp'], reverse=True)
        primary = members[0]
        
        # Provenance: List of IDs
        provenance = [x['id'] for x in members]
        
        gold = {
            "GOLD_ID": f"GOLD_{primary['id'][:8]}",
            "Title": f"[{primary['author']}] {primary['topic']}",
            "Body": primary['content'],
            "Tags": primary['tags'],
            "Provenance": provenance
        }
        
        gold_entries.append(gold)
        
        clusters_output.append({
            "cluster_id": f"CL_{primary['id'][:4]}",
            "representative": primary['content'][:30]+"...",
            "count": len(members),
            "gold_id": gold['GOLD_ID']
        })

    # OUTPUT
    print("\n---------- SUBJECT ----------")
    print(f"MemCell Sweep: {len(sweep_entries)} raw / {len(gold_entries)} consolidated")
    
    print("\n---------- OVERLAP MAP ----------")
    for c in clusters_output:
        print(f"[{c['cluster_id']}] Count: {c['count']} -> {c['gold_id']} | {c['representative']}")
        
    print("\n---------- GOLD ENTRIES ----------")
    print(json.dumps(gold_entries, indent=2))
    
    print("\n---------- CHANGELOG ----------")
    added = len(gold_entries)
    compressed = len(sweep_entries) - added
    print(f"New Gold Entries: {added}")
    print(f"Compressed Duplicates: {compressed}")

if __name__ == "__main__":
    main()
