#!/usr/bin/env python3
"""
Gabriel Turbo Mode V1.0 - MIACLE BULLETS Implementation
All-in-one system hygiene and optimization tool.

Operations:
1. Scan everything → inventory + biggest offenders
2. Heal code → format/lint/fix
3. Unify directory → move manifest + dry-run
4. Delete empty → safe cleanup
5. Deduplicate → hash index + quarantine
6. Turbo runtime → warm caches
7. Reports → structured JSON for Gemini
"""

import os
import sys
import json
import hashlib
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_ROOT = Path.home() / "NOIZYLAB" / "PROJECTS" / "GABRIEL"
QUARANTINE_DIR = DEFAULT_ROOT / "archive" / "quarantine"
REPORT_DIR = DEFAULT_ROOT / "reports"

IGNORE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".ruff_cache", "gabriel_venv"}
CODE_EXTENSIONS = {".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml", ".md", ".sh"}
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp3", ".wav", ".aiff", ".mp4"}


# ============================================================================
# 1️⃣ SCAN EVERYTHING
# ============================================================================

def scan_directory(root: Path) -> dict:
    """Full inventory scan with size analysis."""
    inventory = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size_mb": 0,
        "by_extension": defaultdict(lambda: {"count": 0, "size": 0}),
        "empty_dirs": [],
        "largest_files": [],
        "code_files": [],
        "asset_files": [],
    }
    
    all_files = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip ignored dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        path = Path(dirpath)
        inventory["total_dirs"] += 1
        
        # Check for empty
        if not filenames and not dirnames:
            inventory["empty_dirs"].append(str(path.relative_to(root)))
        
        for filename in filenames:
            filepath = path / filename
            try:
                size = filepath.stat().st_size
            except OSError:
                continue
            
            ext = filepath.suffix.lower()
            inventory["total_files"] += 1
            inventory["total_size_mb"] += size
            inventory["by_extension"][ext]["count"] += 1
            inventory["by_extension"][ext]["size"] += size
            
            all_files.append((str(filepath.relative_to(root)), size, ext))
            
            if ext in CODE_EXTENSIONS:
                inventory["code_files"].append(str(filepath.relative_to(root)))
            elif ext in ASSET_EXTENSIONS:
                inventory["asset_files"].append(str(filepath.relative_to(root)))
    
    # Convert bytes to MB
    inventory["total_size_mb"] = round(inventory["total_size_mb"] / (1024 * 1024), 2)
    
    # Top 20 largest files
    all_files.sort(key=lambda x: -x[1])
    inventory["largest_files"] = [
        {"path": f[0], "size_mb": round(f[1] / (1024 * 1024), 2)}
        for f in all_files[:20]
    ]
    
    # Convert defaultdict
    inventory["by_extension"] = dict(inventory["by_extension"])
    
    return inventory


# ============================================================================
# 2️⃣ HEAL CODE (FORMAT/LINT/FIX)
# ============================================================================

def heal_code(root: Path, dry_run: bool = True) -> dict:
    """Format and lint Python code using ruff."""
    results = {"fixed": [], "errors": [], "dry_run": dry_run}
    
    python_files = list(root.rglob("*.py"))
    python_files = [f for f in python_files if not any(p in str(f) for p in IGNORE_DIRS)]
    
    if not python_files:
        results["message"] = "No Python files found"
        return results
    
    # Check if ruff is available
    try:
        subprocess.run(["ruff", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        results["errors"].append("ruff not installed. Run: pip install ruff")
        return results
    
    for filepath in python_files:
        rel_path = str(filepath.relative_to(root))
        try:
            if dry_run:
                # Check only
                result = subprocess.run(
                    ["ruff", "check", str(filepath)],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    results["fixed"].append({"path": rel_path, "issues": result.stdout.count("\n")})
            else:
                # Fix
                subprocess.run(["ruff", "check", "--fix", str(filepath)], capture_output=True)
                subprocess.run(["ruff", "format", str(filepath)], capture_output=True)
                results["fixed"].append(rel_path)
        except Exception as e:
            results["errors"].append(f"{rel_path}: {e}")
    
    return results


# ============================================================================
# 3️⃣ DELETE EMPTY FOLDERS
# ============================================================================

def delete_empty_dirs(root: Path, dry_run: bool = True) -> dict:
    """Safely remove empty directories."""
    results = {"deleted": [], "dry_run": dry_run}
    
    # Walk bottom-up to handle nested empty dirs
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        path = Path(dirpath)
        
        # Skip root and ignored
        if path == root or any(p in str(path) for p in IGNORE_DIRS):
            continue
        
        # Check if truly empty (after processing children)
        try:
            contents = list(path.iterdir())
            if not contents:
                rel_path = str(path.relative_to(root))
                if dry_run:
                    results["deleted"].append(rel_path)
                else:
                    path.rmdir()
                    results["deleted"].append(rel_path)
        except OSError:
            pass
    
    return results


# ============================================================================
# 4️⃣ DEDUPLICATE ASSETS
# ============================================================================

def find_duplicates(root: Path) -> dict:
    """Find duplicate files by content hash."""
    hash_map = defaultdict(list)
    results = {"duplicates": [], "total_wasted_mb": 0}
    
    for filepath in root.rglob("*"):
        if filepath.is_dir() or any(p in str(filepath) for p in IGNORE_DIRS):
            continue
        
        try:
            # Hash file content
            with open(filepath, "rb") as f:
                content_hash = hashlib.sha256(f.read()).hexdigest()[:16]
            
            hash_map[content_hash].append({
                "path": str(filepath.relative_to(root)),
                "size": filepath.stat().st_size,
            })
        except (OSError, IOError):
            pass
    
    # Find groups with more than one file
    for h, files in hash_map.items():
        if len(files) > 1:
            # Sort by path length (keep shortest)
            files.sort(key=lambda x: len(x["path"]))
            original = files[0]
            duplicates = files[1:]
            
            wasted = sum(d["size"] for d in duplicates)
            results["total_wasted_mb"] += wasted
            results["duplicates"].append({
                "hash": h,
                "original": original["path"],
                "duplicates": [d["path"] for d in duplicates],
                "wasted_mb": round(wasted / (1024 * 1024), 2),
            })
    
    results["total_wasted_mb"] = round(results["total_wasted_mb"] / (1024 * 1024), 2)
    return results


def quarantine_duplicates(root: Path, duplicates: list, dry_run: bool = True) -> dict:
    """Move duplicates to quarantine."""
    results = {"moved": [], "dry_run": dry_run}
    
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    
    for dup_group in duplicates:
        for dup_path in dup_group["duplicates"]:
            src = root / dup_path
            dst = QUARANTINE_DIR / dup_path
            
            if dry_run:
                results["moved"].append(dup_path)
            else:
                try:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    results["moved"].append(dup_path)
                except Exception as e:
                    results["moved"].append(f"ERROR: {dup_path} - {e}")
    
    return results


# ============================================================================
# 5️⃣ WARM CACHES (TURBO RUNTIME)
# ============================================================================

def warm_caches() -> dict:
    """Pre-warm Gabriel caches for zero-latency responses."""
    results = {"warmed": []}
    
    try:
        sys.path.insert(0, str(DEFAULT_ROOT / "core"))
        from speed_core import speed_core
        
        # Warm common queries
        common = ["status", "who are you", "help", "optimize", "time"]
        for q in common:
            speed_core.precompute.set(q, f"cached_response_for_{q}")
            results["warmed"].append(q)
        
        # Warm predictor with common patterns
        for action in ["status", "optimize", "status", "memory"]:
            speed_core.predictor.record(action)
        
        results["predictions"] = speed_core.predictor.predict_next()
        results["stats"] = speed_core.all_stats()
        
    except ImportError as e:
        results["error"] = f"Could not import speed_core: {e}"
    
    return results


# ============================================================================
# 6️⃣ GENERATE REPORT
# ============================================================================

def generate_report(root: Path, output: Optional[Path] = None) -> dict:
    """Generate comprehensive system report for Gemini."""
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "root": str(root),
        "scan": scan_directory(root),
        "duplicates": find_duplicates(root),
        "empty_dirs": delete_empty_dirs(root, dry_run=True),
        "code_health": heal_code(root, dry_run=True),
    }
    
    # Summary
    report["summary"] = {
        "total_files": report["scan"]["total_files"],
        "total_size_mb": report["scan"]["total_size_mb"],
        "empty_dirs_count": len(report["empty_dirs"]["deleted"]),
        "duplicate_groups": len(report["duplicates"]["duplicates"]),
        "wasted_space_mb": report["duplicates"]["total_wasted_mb"],
        "code_issues": len(report["code_health"].get("fixed", [])),
    }
    
    # Save if output specified
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2))
    
    return report


# ============================================================================
# CLI
# ============================================================================

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              🚀 GABRIEL TURBO MODE V1.0                       ║
║                    MIACLE BULLETS                              ║
╚═══════════════════════════════════════════════════════════════╝
""")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Gabriel Turbo Mode - MIACLE Operations")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Root directory")
    parser.add_argument("--scan", action="store_true", help="Scan and inventory")
    parser.add_argument("--heal", action="store_true", help="Format/lint Python code")
    parser.add_argument("--empty", action="store_true", help="Delete empty directories")
    parser.add_argument("--dedup", action="store_true", help="Find duplicates")
    parser.add_argument("--quarantine", action="store_true", help="Move duplicates to quarantine")
    parser.add_argument("--warm", action="store_true", help="Warm caches")
    parser.add_argument("--report", action="store_true", help="Generate full report")
    parser.add_argument("--all", action="store_true", help="Run all operations")
    parser.add_argument("--fix", action="store_true", help="Actually apply changes (not dry-run)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if not any([args.scan, args.heal, args.empty, args.dedup, args.quarantine, 
                args.warm, args.report, args.all]):
        parser.print_help()
        return
    
    dry_run = not args.fix
    root = args.root
    
    if not args.json:
        print_banner()
        print(f"📁 Root: {root}")
        print(f"🔒 Mode: {'DRY RUN' if dry_run else '⚠️  LIVE (changes will be applied)'}\n")
    
    results = {}
    
    if args.scan or args.all or args.report:
        results["scan"] = scan_directory(root)
        if not args.json:
            s = results["scan"]
            print(f"📊 SCAN: {s['total_files']} files, {s['total_size_mb']} MB, {len(s['empty_dirs'])} empty dirs")
    
    if args.heal or args.all:
        results["heal"] = heal_code(root, dry_run=dry_run)
        if not args.json:
            h = results["heal"]
            print(f"🔧 HEAL: {len(h.get('fixed', []))} files {'would be' if dry_run else ''} fixed")
    
    if args.empty or args.all:
        results["empty"] = delete_empty_dirs(root, dry_run=dry_run)
        if not args.json:
            e = results["empty"]
            print(f"🗑️  EMPTY: {len(e['deleted'])} dirs {'would be' if dry_run else ''} deleted")
    
    if args.dedup or args.all:
        results["dedup"] = find_duplicates(root)
        if not args.json:
            d = results["dedup"]
            print(f"🔍 DEDUP: {len(d['duplicates'])} duplicate groups, {d['total_wasted_mb']} MB wasted")
    
    if args.quarantine:
        if "dedup" not in results:
            results["dedup"] = find_duplicates(root)
        results["quarantine"] = quarantine_duplicates(root, results["dedup"]["duplicates"], dry_run=dry_run)
        if not args.json:
            q = results["quarantine"]
            print(f"📦 QUARANTINE: {len(q['moved'])} files {'would be' if dry_run else ''} moved")
    
    if args.warm or args.all:
        results["warm"] = warm_caches()
        if not args.json:
            w = results["warm"]
            print(f"🔥 WARM: {len(w.get('warmed', []))} caches warmed")
    
    if args.report or args.all:
        report_path = REPORT_DIR / f"turbo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results["report"] = generate_report(root, report_path)
        if not args.json:
            print(f"📄 REPORT: Saved to {report_path}")
    
    if args.json:
        print(json.dumps(results, indent=2, default=str))
    elif not args.report:
        print("\n✅ Turbo Mode complete. Use --fix to apply changes.")


if __name__ == "__main__":
    main()
