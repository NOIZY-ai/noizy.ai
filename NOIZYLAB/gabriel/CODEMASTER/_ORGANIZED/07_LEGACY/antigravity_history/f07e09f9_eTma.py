#!/usr/bin/env python3
import argparse, os, shutil, hashlib, json
from datetime import datetime
from pathlib import Path

ASSET_BUCKETS = {
  "audio": {".wav",".aiff",".aif",".mp3",".flac",".m4a",".ogg"},
  "video": {".mp4",".mov",".mkv",".avi",".webm",".m4v"},
  "images": {".png",".jpg",".jpeg",".webp",".gif",".tif",".tiff",".svg"},
  "3d":    {".glb",".gltf",".vrm",".fbx",".obj",".usdz",".splat",".ply"},
  "docs":  {".pdf",".md",".txt",".rtf",".docx",".pptx",".xlsx",".csv",".json",".yaml",".yml"}
}

IGNORE_DIRS = {".git","node_modules",".venv","venv","__pycache__", ".cache", "gabriel"}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ensure_dir(p: Path): p.mkdir(parents=True, exist_ok=True)

def classify(p: Path):
    ext = p.suffix.lower()
    for bucket, exts in ASSET_BUCKETS.items():
        if ext in exts: return bucket
    return "other"

def delete_empty_dirs(root: Path, dry_run: bool):
    removed = []
    dirs = sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda x: len(str(x)), reverse=True)
    for d in dirs:
        try:
            if any(part in IGNORE_DIRS for part in d.parts): 
                continue
            if d.is_dir() and not any(d.iterdir()):
                removed.append(str(d))
                if not dry_run:
                    d.rmdir()
        except Exception:
            pass
    return removed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Project root to optimize (source tree)")
    ap.add_argument("--gabriel", default="/Volumes/GABRIEL/MC96/GABRIEL_CORE", help="GABRIEL core root")
    ap.add_argument("--author", default="ENGR", help="Rob|Shirl|ENGR|GABRIEL")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--move-other", action="store_true", help="Also move unknown filetypes into vault/assets/other")
    args = ap.parse_args()

    src_root = Path(args.root).expanduser().resolve()
    gab = Path(args.gabriel).expanduser().resolve()

    vault_assets = gab/"vault"/"assets"
    vault_artifacts = gab/"vault"/"artifacts"
    ensure_dir(vault_assets); ensure_dir(vault_artifacts)
    ensure_dir(vault_artifacts/"manifests"); ensure_dir(vault_artifacts/"logs"); ensure_dir(vault_artifacts/"reports")
    ensure_dir(gab/"memcell_db")

    ts = datetime.now().isoformat(timespec="seconds")
    manifest = {
        "run_at": ts,
        "author": args.author,
        "source_root": str(src_root),
        "gabriel_root": str(gab),
        "moves": [],
        "dedupe": [],
        "skipped": [],
        "empty_dirs_deleted": []
    }

    # hash index for dedupe in vault
    vault_hash_index = {}
    for existing in vault_assets.rglob("*"):
        if existing.is_file():
            try:
                h = sha256_file(existing)
                vault_hash_index.setdefault(h, []).append(str(existing))
            except Exception:
                pass

    for p in src_root.rglob("*"):
        if not p.is_file():
            continue

        parts = set([x.lower() for x in p.parts])
        if parts & IGNORE_DIRS:
            continue

        bucket = classify(p)
        if bucket == "other" and not args.move_other:
            continue

        dest_dir = vault_assets/bucket
        ensure_dir(dest_dir)

        try:
            h = sha256_file(p)
        except Exception:
            manifest["skipped"].append({"path": str(p), "reason": "hash_failed"})
            continue

        # dedupe by hash
        if h in vault_hash_index:
            manifest["dedupe"].append({"path": str(p), "duplicate_of": vault_hash_index[h][0]})
            if not args.dry_run:
                p.unlink(missing_ok=True)
            continue

        # move with collision handling
        dest = dest_dir/p.name
        if dest.exists():
            dest = dest_dir/f"{p.stem}_{h[:10]}{p.suffix}"

        manifest["moves"].append({"from": str(p), "to": str(dest), "sha256": h})
        vault_hash_index.setdefault(h, []).append(str(dest))

        if not args.dry_run:
            shutil.move(str(p), str(dest))

    # delete empty folders
    manifest["empty_dirs_deleted"] = delete_empty_dirs(src_root, args.dry_run)

    out = vault_artifacts/"manifests"/f"optimize_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    if not args.dry_run:
        out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\n=== GABRIEL OPTIMIZE ALL COMPLETE ===")
    print("Dry run:", args.dry_run)
    print("Moved:", len(manifest["moves"]))
    print("Deduped (deleted duplicates):", len(manifest["dedupe"]))
    print("Empty dirs deleted:", len(manifest["empty_dirs_deleted"]))
    if not args.dry_run:
        print("Manifest:", out)

if __name__ == "__main__":
    main()
