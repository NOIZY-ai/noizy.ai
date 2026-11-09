import sys
import json
import datetime
import hashlib
import re
from pathlib import Path
from collections import defaultdict

# --- CONFIGURATION ---
WINDOW_HOURS = 4
WINDOW_BUFFER_MIN = 15
NOW = datetime.datetime.now()
WINDOW_START = NOW - datetime.timedelta(hours=WINDOW_HOURS, minutes=WINDOW_BUFFER_MIN)

DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")

# --- UTILS ---

def compute_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def normalize_text(text):
    """
    Remove boilerplate, standardize whitespace, lowercase.
    For this specific environment, we strip common headers if they existed.
    """
    text = text.lower().strip()
    text = " ".join(text.split()) # Normalize whitespace
    return text

def usage_fingerprint(text):
    """
    Soft fingerprint: sorted unique words > 3 chars.
    """
    words = set(re.findall(r'\b\w{4,}\b', text.lower()))
    return sorted(list(words))

def calculate_jaccard(fp1, fp2):
    if not fp1 or not fp2: return 0.0
    s1 = set(fp1)
    s2 = set(fp2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

# --- CORE LOGIC ---

def main():
    # 1. WINDOWING
    if not DB_PATH.exists():
        print("BLOCKED: DB not found.")
        sys.exit(1)
        
    with open(DB_PATH) as f:
        raw_db = json.load(f)
    
    # Ingest & Parse
    ingest_pool = []
    skipped_count = 0
    
    for entry in raw_db:
        try:
            ts_str = entry.get('timestamp')
            if not ts_str: continue
            ts = datetime.datetime.fromisoformat(ts_str)
            
            if ts >= WINDOW_START:
                # Parse into standard record
                record = {
                    'id': entry.get('id'),
                    'source': 'MEMCELL_CORE', # Single source for now
                    'created_at': ts,
                    'title': f"[{entry.get('author', 'UNKNOWN')}] {entry.get('topic', 'General')}",
                    'body': entry.get('content', ''),
                    'tags': entry.get('tags', []),
                    'raw': entry
                }
                ingest_pool.append(record)
            else:
                skipped_count += 1
        except Exception:
            skipped_count += 1
            continue

    if not ingest_pool:
        print(f"Subject: MemCell Sweep: 0 new, 0 clusters, 0 gold updates (window {WINDOW_START.isoformat()} to {NOW.isoformat()})")
        print("NO DATA IN WINDOW")
        return

    # 2. CANONICALIZATION & FINGERPRINTING
    for r in ingest_pool:
        comp_text = normalize_text(r['body'])
        r['comp_text'] = comp_text
        r['exact_fp'] = compute_sha256(comp_text)
        r['soft_fp'] = usage_fingerprint(comp_text)
        r['cluster_id'] = None

    # 3. OVERLAP DETECTION & CLUSTERING
    clusters = {} # cluster_id -> list of records
    cluster_counter = 0

    # Sort by length descending (longest usually best anchor candidate)
    ingest_pool.sort(key=lambda x: len(x['body']), reverse=True)

    for r in ingest_pool:
        if r['cluster_id']: continue # Already clustered
        
        # New Cluster
        cluster_id = f"CL_{cluster_counter:04d}"
        cluster_counter += 1
        clusters[cluster_id] = [r]
        r['cluster_id'] = cluster_id
        
        # Look for matches in remaining unclustered
        for candidate in ingest_pool:
            if candidate['cluster_id']: continue # Already clustered
            if candidate['id'] == r['id']: continue
            
            match_type = None
            
            # Exact Match
            if candidate['exact_fp'] == r['exact_fp']:
                match_type = "EXACT"
            
            # Strong Match
            elif calculate_jaccard(r['soft_fp'], candidate['soft_fp']) >= 0.88:
                match_type = "STRONG"
            
            # Weak Match (We log it but maybe enforce clustering for this exercise on strong only)
            # Logic: If >0.75 we treat as weak overlap, maybe merge if author same? 
            # For this simplified "Enterprise" run, we'll merge > 0.75 as "WEAK_MERGE"
            elif calculate_jaccard(r['soft_fp'], candidate['soft_fp']) >= 0.75:
                match_type = "WEAK"

            if match_type:
                clusters[cluster_id].append(candidate)
                candidate['cluster_id'] = cluster_id
                candidate['match_reason'] = match_type

    # 4. CONSOLIDATION STRATEGY
    gold_corpus = []
    changelog = {
        'created_gold': [],
        'updated_gold': [],
        'deprecated': [],
        'held_for_review': []
    }
    
    overlap_map = []

    for cid, members in clusters.items():
        # Pick anchor: Most recent timestamp usually preferred for "latest state", 
        # OR longest body. Prompt says: "most complete + most recent".
        # Let's sort by length (completeness) then recency.
        # Actually, python sort is stable.
        
        # Sort by timestamp (newest first)
        members.sort(key=lambda x: x['created_at'], reverse=True)
        # Sort by length (longest first) - this takes precedence if we do it last
        members.sort(key=lambda x: len(x['body']), reverse=True)
        
        anchor = members[0]
        
        # Merge Facts
        # In this simple text DB, merging means taking the anchor's body + union of tags
        all_tags = set()
        provenance = []
        
        for m in members:
            all_tags.update(m['tags'])
            provenance.append({
                'id': m['id'],
                'source': m['source'],
                'timestamp': m['created_at'].isoformat()
            })
            if m['id'] != anchor['id']:
                changelog['deprecated'].append(m['id'])
        
        gold_id = f"GOLD_{anchor['exact_fp'][:8]}"
        
        gold_entry = {
            'GOLD_ID': gold_id,
            'Title': anchor['title'],
            'Body': anchor['body'],
            'Tags': sorted(list(all_tags)),
            'Provenance': provenance
        }
        gold_corpus.append(gold_entry)
        changelog['created_gold'].append(gold_id)
        
        # Overlap Map Entry
        classification = "EXACT" 
        # If any member was STRONG or WEAK, upgrade classification
        types = [m.get('match_reason', 'ANCHOR') for m in members]
        if "WEAK" in types: classification = "WEAK_OVERLAP"
        elif "STRONG" in types: classification = "STRONG_OVERLAP"
        elif len(members) > 1: classification = "EXACT_DUPE"
        else: classification = "UNIQUE"

        overlap_map.append({
            'cluster_id': cid,
            'members': [m['id'] for m in members],
            'classification': classification,
            'merge_action': 'MERGED',
            'gold_id': gold_id
        })

    # --- OUTPUT ---
    
    # A) Subject
    print(f"Subject: MemCell Sweep: {len(ingest_pool)} new, {len(clusters)} clusters, {len(gold_corpus)} gold updates (window {WINDOW_START.strftime('%H:%M')} to {NOW.strftime('%H:%M')})")
    print("-" * 80)
    
    # B) Overlap Map
    print("OVERLAP MAP")
    print("-" * 80)
    print(f"{'CLUSTER':<10} | {'CLASS':<15} | {'ACTION':<10} | {'MEMBERS'}")
    for item in overlap_map:
        m_str = ", ".join([m[:8] for m in item['members']])
        print(f"{item['cluster_id']:<10} | {item['classification']:<15} | {item['merge_action']:<10} | {m_str}")
    print("-" * 80)

    # C) GOLD Entries
    print("GOLD ENTRIES")
    print("-" * 80)
    print(json.dumps(gold_corpus, indent=2))
    print("-" * 80)

    # D) ChangeLog
    print("CHANGELOG")
    print("-" * 80)
    print(json.dumps(changelog, indent=2))
    print("-" * 80)
    
    # Save to file per "Truth Ledger" standard?
    # For now, just stdout as requested.

if __name__ == "__main__":
    main()
