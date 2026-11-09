#!/usr/bin/env python3
"""
NUCLEAR MODE — PHASE 1A
Build cryptographic truth index (sha256)
READ-ONLY. SAFE. REVERSIBLE.
(Localized to NOIZYLAB due to missing External Volume)
"""

import hashlib, json
from pathlib import Path
from datetime import datetime
import sys

# ADJUSTED PATHS FOR LOCAL EXECUTION
AUDIO_ROOT = Path("/Users/m2ultra/NOIZYLAB/archives/root_sweep_20251214/Universal/Library/Assets/Audio")
REPORTS = Path("/Users/m2ultra/NOIZYLAB/reports")
REPORTS.mkdir(parents=True, exist_ok=True)

AUDIO_EXT = {
    ".wav",".aiff",".aif",".mp3",".flac",
    ".m4a",".ogg",".aac",".alac"
}

def sha256_file(p, chunk=16*1024*1024):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

def main():
    if not AUDIO_ROOT.exists():
        print(f"❌ CRITICAL: Audio Root not found: {AUDIO_ROOT}")
        sys.exit(1)

    index = {}
    count = 0

    print(f"☢️  NUCLEAR PHASE 1A — HASHING START")
    print(f"📂 Target: {AUDIO_ROOT}")

    for p in AUDIO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in AUDIO_EXT:
            continue

        try:
            h = sha256_file(p)
        except Exception as e:
            print("⚠️  Failed:", p, e)
            continue

        index.setdefault(h, []).append({
            "path": str(p),
            "size": p.stat().st_size
        })

        count += 1
        if count % 100 == 0:
            print(f"… hashed {count} files")

    out = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_files": count,
        "unique_hashes": len(index),
        "hash_index": index
    }

    out_path = REPORTS / "audio_hash_index.json"
    out_path.write_text(json.dumps(out, indent=2))

    print("\n✅ PHASE 1A COMPLETE")
    print(f"📄 Truth index: {out_path}")
    print("🔒 No files touched")

if __name__ == "__main__":
    main()
