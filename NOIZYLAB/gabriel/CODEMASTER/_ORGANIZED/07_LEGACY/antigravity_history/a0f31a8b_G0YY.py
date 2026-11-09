#!/usr/bin/env python3
import argparse, csv, json, os, re, shutil, unicodedata
from datetime import datetime
from pathlib import Path

AUDIO_EXTS = {".wav",".aiff",".aif",".mp3",".flac",".m4a",".ogg",".aac",".alac",".wma"}
BAD_CHARS = r'<>:"/\\|?*\0'
BAD_RE = re.compile(f"[{re.escape(BAD_CHARS)}]")

def safe_name(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).strip()
    s = BAD_RE.sub("_", s)
    s = re.sub(r"\s+", " ", s)
    s = s.replace("..", ".")
    return s[:240]  # keep paths safe

def classify(p: Path):
    ext = p.suffix.lower()
    if ext in AUDIO_EXTS:
        return "audio"
    if ext == "":
        return "noext"
    return "other"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Source folder containing audio")
    ap.add_argument("--dest", default="/Volumes/GABRIEL/MC96/GABRIEL_CORE/vault/assets/audio", help="Destination audio vault")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.src).expanduser().resolve()
    dest = Path(args.dest).expanduser().resolve()
    dup_dir = dest / "_duplicates"
    unk_dir = dest / "_unknown"
    
    # Ensure dest exists (or log if we can't create it due to missing volume)
    try:
        dest.mkdir(parents=True, exist_ok=True)
        dup_dir.mkdir(parents=True, exist_ok=True)
        unk_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"CRITICAL ERROR: Cannot create destination {dest}. Is the GABRIEL volume mounted?")
        print(f"Error: {e}")
        return

    ts = datetime.now().isoformat(timespec="seconds")
    manifest_rows = []
    seen_fast = {}  # key: (basename_lower, size) -> first path

    def record(action, p, to=None, reason=None):
        manifest_rows.append({
            "time": ts,
            "action": action,
            "from": str(p),
            "to": str(to) if to else "",
            "size": p.stat().st_size if p.exists() else "",
            "reason": reason or ""
        })

    print(f"🚀 STARTING SCAN: {src}")
    print(f"🎯 DESTINATION: {dest}")
    
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        # skip junk
        parts = {x.lower() for x in p.parts}
        if any(x in parts for x in [".git","node_modules","__pycache__", ".ds_store"]):
            continue

        kind = classify(p)
        ext = p.suffix.lower()

        # no extension -> quarantine
        if kind == "noext":
            new_name = safe_name(p.name) + ".unknown"
            to = unk_dir / new_name
            if to.exists():
                to = unk_dir / f"{p.stem}_{p.stat().st_size}.unknown"
            record("MOVE_UNKNOWN", p, to, "no extension")
            if not args.dry_run:
                shutil.move(str(p), str(to))
            continue

        if kind != "audio":
            continue

        # normalize filename
        safe = safe_name(p.stem) + ext
        target = dest / safe
        if target.exists():
            # fast duplicate check (basename + size)
            key = (safe.lower(), p.stat().st_size)
            if key in seen_fast:
                to = dup_dir / safe
                if to.exists():
                    to = dup_dir / f"{p.stem}_{p.stat().st_size}{ext}"
                record("MOVE_DUP_FAST", p, to, f"fast-dup of {seen_fast[key]}")
                if not args.dry_run:
                    shutil.move(str(p), str(to))
                continue
            else:
                # collision but not proven duplicate -> rename
                target = dest / f"{p.stem}_{p.stat().st_size}{ext}"

        key = (safe.lower(), p.stat().st_size)
        seen_fast.setdefault(key, str(target))

        record("MOVE_AUDIO", p, target, "organized")
        if not args.dry_run:
            shutil.move(str(p), str(target))

    # write manifests
    out_dir = Path("/Volumes/GABRIEL/MC96/GABRIEL_CORE/vault/artifacts/manifests")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        csv_path = out_dir / f"audio_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        json_path = out_dir / f"audio_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        if not args.dry_run:
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=["time","action","from","to","size","reason"])
                w.writeheader()
                w.writerows(manifest_rows)
            json_path.write_text(json.dumps(manifest_rows, indent=2), encoding="utf-8")

        print("=== GABRIEL AUDIO ORGANIZE COMPLETE ===")
        print("Dry run:", args.dry_run)
        print("Records:", len(manifest_rows))
        if not args.dry_run:
            print("Manifest CSV:", csv_path)
            print("Manifest JSON:", json_path)
    except Exception as e:
        print(f"Error writing manifest: {e}")

if __name__ == "__main__":
    main()
