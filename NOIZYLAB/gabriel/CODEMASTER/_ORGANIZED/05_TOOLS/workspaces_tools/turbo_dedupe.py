#!/usr/bin/env python3
import hashlib, json, shutil
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(".").resolve()
REPORTS = ROOT / "reports"
QUAR = ROOT / "_quarantine_duplicates"
REPORTS.mkdir(exist_ok=True)
QUAR.mkdir(exist_ok=True)

IGNORE = {".git","node_modules",".venv","venv","dist","build",".next","__pycache__","reports", "_quarantine_duplicates"}

def sha256(p: Path, chunk=16*1024*1024):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

def main():
    idx={}
    moved=[]
    scanned=0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if any(x in p.parts for x in IGNORE): continue
        scanned += 1
        try:
            h=sha256(p)
        except Exception:
            continue
        if h in idx:
            target = QUAR / p.name
            if target.exists():
                target = QUAR / f"{p.stem}_{p.stat().st_size}{p.suffix}"
            shutil.move(str(p), str(target))
            moved.append({"dupe_of": idx[h], "from": str(p), "to": str(target), "hash": h})
        else:
            idx[h] = str(p)

    out={
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files_scanned": scanned,
        "unique_hashes": len(idx),
        "duplicates_quarantined": len(moved),
        "moves": moved[:5000],
    }
    (REPORTS/"dedupe_report.json").write_text(json.dumps(out, indent=2))
    print("✅ reports/dedupe_report.json")
    print("✅ quarantined:", len(moved))

if __name__=="__main__":
    main()
