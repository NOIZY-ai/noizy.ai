#!/usr/bin/env python3
"""
Gabriel Doctor: scan + heal + optimize repo hygiene
- Formats/lints (Python via ruff)
- Deletes empty folders
- Creates an asset manifest
- Finds large files + duplicates (by hash)
Safe by default: does NOT delete duplicates unless you pass --dedupe-move
"""

from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
from datetime import datetime

AUDIO_EXT = {".wav", ".aiff", ".aif", ".mp3", ".flac", ".m4a", ".ogg", ".opus"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".gif"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
CODE_EXT  = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md", ".yml", ".yaml", ".toml"}

DEFAULT_IGNORES = {
    ".git", ".DS_Store", "node_modules", ".venv", "dist", "build", ".next",
    "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"
}

def run(cmd: list[str]) -> int:
    print("▶", " ".join(cmd))
    return subprocess.call(cmd)

def sha256_file(p: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def is_ignored(path: Path) -> bool:
    parts = set(path.parts)
    return any(x in parts for x in DEFAULT_IGNORES)

def delete_empty_dirs(root: Path) -> int:
    removed = 0
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        d = Path(dirpath)
        if is_ignored(d):
            continue
        # ignore hidden dirs by default
        if d.name.startswith(".") and d.name not in {".agent"}:
            continue
        if not any((d / f).exists() for f in filenames) and not any((d / sd).exists() for sd in dirnames):
            try:
                d.rmdir()
                removed += 1
            except OSError:
                pass
    return removed

def classify(p: Path) -> str:
    ext = p.suffix.lower()
    if ext in AUDIO_EXT: return "audio"
    if ext in IMAGE_EXT: return "image"
    if ext in VIDEO_EXT: return "video"
    if ext in CODE_EXT:  return "code"
    return "other"

def build_manifest(root: Path, out: Path, min_size_mb: float = 25.0) -> dict:
    items = []
    big = []
    for dirpath, _, filenames in os.walk(root):
        d = Path(dirpath)
        if is_ignored(d):
            continue
        for fn in filenames:
            p = d / fn
            if is_ignored(p):
                continue
            try:
                stat = p.stat()
            except FileNotFoundError:
                continue
            rec = {
                "path": str(p.relative_to(root)),
                "size_bytes": stat.st_size,
                "type": classify(p),
                "ext": p.suffix.lower()
            }
            items.append(rec)
            if stat.st_size >= int(min_size_mb * 1024 * 1024):
                big.append(rec)
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "root": str(root),
        "counts": {
            "total_files": len(items),
            "audio": sum(1 for i in items if i["type"] == "audio"),
            "image": sum(1 for i in items if i["type"] == "image"),
            "video": sum(1 for i in items if i["type"] == "video"),
            "code":  sum(1 for i in items if i["type"] == "code"),
            "other": sum(1 for i in items if i["type"] == "other"),
        },
        "big_files_over_mb": min_size_mb,
        "big_files": sorted(big, key=lambda x: x["size_bytes"], reverse=True)[:250],
        "files": items
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2))
    return manifest

def find_duplicates_by_hash(root: Path, cache_path: Path) -> dict[str, list[str]]:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text())
        except Exception:
            cache = {}

    hashes: dict[str, list[str]] = {}
    for dirpath, _, filenames in os.walk(root):
        d = Path(dirpath)
        if is_ignored(d):
            continue
        for fn in filenames:
            p = d / fn
            if is_ignored(p):
                continue
            # skip tiny files to reduce noise
            try:
                st = p.stat()
            except FileNotFoundError:
                continue
            if st.st_size < 1024:
                continue
            rel = str(p.relative_to(root))
            key = f"{rel}:{st.st_size}:{int(st.st_mtime)}"
            h = cache.get(key)
            if not h:
                h = sha256_file(p)
                cache[key] = h
            hashes.setdefault(h, []).append(rel)

    cache_path.write_text(json.dumps(cache))
    dups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return dups

def move_duplicates(root: Path, dups: dict[str, list[str]], dup_dir: Path) -> int:
    moved = 0
    dup_dir.mkdir(parents=True, exist_ok=True)
    for h, paths in dups.items():
        keep = paths[0]
        for rel in paths[1:]:
            src = root / rel
            if not src.exists():
                continue
            target = dup_dir / Path(rel).name
            # ensure unique name
            if target.exists():
                target = dup_dir / f"{Path(rel).stem}_{h[:8]}{Path(rel).suffix}"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(target))
            moved += 1
    return moved

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo root")
    ap.add_argument("--fix-python", action="store_true", help="Run ruff format + ruff check --fix")
    ap.add_argument("--delete-empty", action="store_true", help="Delete empty folders")
    ap.add_argument("--manifest", action="store_true", help="Write asset manifest")
    ap.add_argument("--dupes", action="store_true", help="Find duplicates by hash")
    ap.add_argument("--dedupe-move", action="store_true", help="Move duplicates (keeps 1 copy)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    report_dir = root / "reports"
    report_dir.mkdir(exist_ok=True)

    exit_code = 0

    if args.fix_python:
        # ruff must be installed (pipx install ruff OR pip install ruff)
        exit_code |= run(["ruff", "format", str(root)])
        exit_code |= run(["ruff", "check", str(root), "--fix", "--unsafe-fixes"])

    if args.delete_empty:
        removed = delete_empty_dirs(root)
        print(f"✅ empty folders removed: {removed}")

    if args.manifest:
        out = report_dir / "asset_manifest.json"
        build_manifest(root, out)
        print(f"✅ Manifest generated: {out}")

    if args.dupes:
        cache = report_dir / "obj_cache.json"
        dups = find_duplicates_by_hash(root, cache)
        print(f"✅ Found {len(dups)} duplicate sets.")
        
        if args.dedupe_move:
            dest = root / "_duplicates"
            count = move_duplicates(root, dups, dest)
            print(f"✅ Moved {count} duplicates to {dest}")
        else:
            for k, v in list(dups.items())[:10]:
                print(f"  Hash {k[:8]} -> {len(v)} copies")
            if len(dups) > 10:
                print(f"  ... and {len(dups)-10} more sets.")

    print("🏁 Gabriel Doctor finished.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
