#!/usr/bin/env python3
import os, re, json
from datetime import datetime
from collections import defaultdict

NKI_ROOT = "/Volumes/JOE/NKI"
PORTAL_DIR = "/Volumes/JOE/NKI/MC96_MISSION_CONTROL"

SHIRL = ["shirl", "vocal", "voice", "sing", "lyric", "melody"]
ENGR = ["engr", "engineer", "mix", "master", "eq", "compress"]

def classify(filename, path):
    c = (filename + " " + path).lower()
    s = sum(1 for p in SHIRL if p in c)
    e = sum(1 for p in ENGR if p in c)
    return "SHIRL" if s > e else "ENGR" if e > s else "UNKNOWN"

def main():
    print("=" * 60)
    print("MC96 MEMCELL TRACKER")
    print("=" * 60)
    
    buckets = defaultdict(list)
    types = {"SHIRL": 0, "ENGR": 0, "UNKNOWN": 0}
    total = 0
    
    for dp, _, fns in os.walk(NKI_ROOT):
        if any(x in dp for x in ['_KTK', 'MC96_MISSION', '__pycache__']): continue
        for f in fns:
            if f.startswith('.'): continue
            try:
                p = os.path.join(dp, f)
                t = datetime.fromtimestamp(os.stat(p).st_mtime).strftime("%Y-%m-%d %H:%M")
                ty = classify(f, dp)
                types[ty] += 1
                buckets[t].append({"file": f, "type": ty})
                total += 1
            except: pass
    
    overlaps = [{"time": k, "count": len(v), "golden": any(x["type"]=="SHIRL" for x in v) and any(x["type"]=="ENGR" for x in v)} for k, v in buckets.items() if len(v) > 1]
    overlaps.sort(key=lambda x: -x["count"])
    golden = sum(1 for o in overlaps if o["golden"])
    
    report = {"generated": datetime.now().isoformat(), "total": total, "types": types, "overlaps": len(overlaps), "golden": golden, "top": overlaps[:10]}
    
    os.makedirs(PORTAL_DIR, exist_ok=True)
    with open(f"{PORTAL_DIR}/overlap_report.json", 'w') as f: json.dump(report, f, indent=2)
    
    print(f"Total Files: {total}")
    print(f"SHIRL: {types['SHIRL']}, ENGR: {types['ENGR']}")
    print(f"Overlaps: {len(overlaps)}, Golden: {golden}")
    print("=" * 60)

if __name__ == "__main__": main()
