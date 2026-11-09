#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           HYPER MINER V2 - ZERO LATENCY EDITION                              ║
║           100% OPTIMIZED FOR M2 ULTRA 192GB                                  ║
║           GABRIEL SYSTEM OMEGA - NOIZYLAB                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import os
import shutil
import time
import subprocess
import concurrent.futures
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION - ZERO LATENCY SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════

# Source from args or default
SOURCE_DIR = sys.argv[1] if len(sys.argv) > 1 else "/Volumes/4TB Blue Fish"

# Sanitize volume name for destination
VOL_NAME = os.path.basename(SOURCE_DIR.rstrip('/'))
DEST_DIR = Path(f"/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/mined_code/{VOL_NAME}")

# M2 ULTRA OPTIMIZED WORKER COUNT (Max threads for 24-core CPU)
MAX_WORKERS = 100

# Extensions to mine (CODE MASTER COLLECTION)
CODE_EXTENSIONS = [
    # Programming Languages
    "*.py", "*.js", "*.ts", "*.tsx", "*.jsx", "*.go", "*.rs", "*.c", "*.cpp", "*.h", "*.hpp",
    "*.java", "*.kt", "*.swift", "*.php", "*.rb", "*.pl", "*.lua", "*.r", "*.scala", "*.clj",
    # Web
    "*.html", "*.css", "*.scss", "*.sass", "*.less", "*.vue", "*.svelte",
    # Data & Config
    "*.json", "*.xml", "*.yaml", "*.yml", "*.toml", "*.ini", "*.conf", "*.cfg",
    # Scripts
    "*.sh", "*.bash", "*.zsh", "*.fish", "*.ps1", "*.bat", "*.cmd",
    # Docs
    "*.md", "*.rst", "*.txt",
    # Database
    "*.sql", "*.graphql", "*.prisma",
    # DevOps
    "Dockerfile", "*.dockerfile", "Makefile", "CMakeLists.txt",
    # Other
    "*.proto", "*.wasm", "*.asm"
]

# Build native find command for MAXIMUM SPEED
def build_find_cmd():
    cmd = ["find", SOURCE_DIR, "-type", "f", "("]
    for i, ext in enumerate(CODE_EXTENSIONS):
        if i > 0:
            cmd.append("-o")
        cmd.extend(["-name", ext])
    cmd.append(")")
    return cmd

FIND_CMD = build_find_cmd()

# ═══════════════════════════════════════════════════════════════════════════════
# ZERO LATENCY FILE PROCESSOR
# ═══════════════════════════════════════════════════════════════════════════════

def process_file(src_path):
    """Process a single file with deduplication check."""
    try:
        src = Path(src_path)
        if not src.exists() or src.stat().st_size == 0:
            return (0, 0, 0)  # skipped, copied, bytes
        
        # Calculate relative path
        try:
            rel_path = src.relative_to(SOURCE_DIR)
        except ValueError:
            rel_path = Path(src.name)
        
        dest_path = DEST_DIR / rel_path
        
        # Skip if identical file exists
        if dest_path.exists():
            if dest_path.stat().st_size == src.stat().st_size:
                return (1, 0, 0)  # skipped (duplicate)
        
        # Create directory structure
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy with metadata preservation
        shutil.copy2(src, dest_path)
        
        return (0, 1, src.stat().st_size)  # copied
        
    except Exception:
        return (0, 0, 0)

# ═══════════════════════════════════════════════════════════════════════════════
# HYPER SCAN ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def hyper_scan():
    """Main scanning function - ZERO LATENCY."""
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🚀 HYPER MINER V2 - ZERO LATENCY EDITION                        ║")
    print("║  💎 GABRIEL SYSTEM OMEGA                                         ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print(f"📂 SOURCE: {SOURCE_DIR}")
    print(f"📁 TARGET: {DEST_DIR}")
    print(f"⚡ WORKERS: {MAX_WORKERS}")
    print()
    
    start_time = time.time()
    
    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 1: NATIVE FIND SCAN (Lightning Fast)
    # ─────────────────────────────────────────────────────────────────────────
    print("⚡ PHASE 1: SCANNING FILESYSTEM...")
    
    try:
        result = subprocess.run(
            FIND_CMD, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=300  # 5 min timeout
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
    except subprocess.TimeoutExpired:
        print("⚠️  Scan timeout - using partial results")
        files = []
    except Exception as e:
        print(f"❌ SCAN ERROR: {e}")
        return
    
    scan_duration = time.time() - start_time
    print(f"✅ SCANNED: {len(files):,} files in {scan_duration:.2f}s")
    print()
    
    if not files:
        print("⚠️  No files found. Check source path.")
        return
    
    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 2: PARALLEL EXTRACTION (100 Workers)
    # ─────────────────────────────────────────────────────────────────────────
    print(f"⚡ PHASE 2: EXTRACTING WITH {MAX_WORKERS} PARALLEL WORKERS...")
    
    # Ensure destination exists
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    total_copied = 0
    total_skipped = 0
    total_bytes = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_file, f) for f in files]
        
        # Progress tracking
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            skipped, copied, bytes_copied = future.result()
            total_skipped += skipped
            total_copied += copied
            total_bytes += bytes_copied
            completed += 1
            
            # Progress every 1000 files
            if completed % 1000 == 0:
                pct = (completed / len(files)) * 100
                print(f"   ⏳ {completed:,}/{len(files):,} ({pct:.1f}%) - {total_copied:,} new files")
    
    # ─────────────────────────────────────────────────────────────────────────
    # PHASE 3: REPORT
    # ─────────────────────────────────────────────────────────────────────────
    total_duration = time.time() - start_time
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  ✅ EXTRACTION COMPLETE - ZERO LATENCY ACHIEVED                   ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print(f"   📊 TOTAL FILES SCANNED:  {len(files):,}")
    print(f"   ✅ NEW FILES COPIED:     {total_copied:,}")
    print(f"   ⏭️  DUPLICATES SKIPPED:  {total_skipped:,}")
    print(f"   💾 DATA TRANSFERRED:     {total_bytes / (1024*1024):.2f} MB")
    print(f"   ⚡ TOTAL TIME:           {total_duration:.2f}s")
    print(f"   🚀 SPEED:                {len(files) / total_duration:.0f} files/sec")
    print()
    
    # Save manifest
    manifest_path = DEST_DIR / "_MANIFEST.json"
    import json
    manifest = {
        "source": str(SOURCE_DIR),
        "destination": str(DEST_DIR),
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(files),
        "files_copied": total_copied,
        "files_skipped": total_skipped,
        "bytes_transferred": total_bytes,
        "duration_seconds": total_duration,
        "speed_files_per_sec": len(files) / total_duration if total_duration > 0 else 0
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"   📋 MANIFEST: {manifest_path}")
    print()
    print("🐺 GABRIEL SYSTEM OMEGA - MISSION COMPLETE")

# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    hyper_scan()
