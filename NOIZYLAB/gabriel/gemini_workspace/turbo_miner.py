#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           TURBO MINER - MULTI-VOLUME PARALLEL SCANNER                        ║
║           ZERO LATENCY | 100% OPTIMIZED                                      ║
║           GABRIEL SYSTEM OMEGA - NOIZYLAB                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Scans ALL mounted volumes in parallel for maximum throughput.
"""
import os
import subprocess
import concurrent.futures
import time
from pathlib import Path
from datetime import datetime

# Volumes to scan
VOLUMES = [
    "/Volumes/4TB Blue Fish",
    "/Volumes/12TB",
    "/Volumes/6TB Plata",
    "/Volumes/2TB Backup"
]

WORKSPACE = Path("/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL")
HYPER_MINER = WORKSPACE / "hyper_miner.py"

def scan_volume(volume):
    """Launch hyper_miner for a specific volume."""
    if not os.path.exists(volume):
        return (volume, "NOT_MOUNTED", 0)
    
    start = time.time()
    try:
        result = subprocess.run(
            ["python3", str(HYPER_MINER), volume],
            capture_output=True,
            text=True,
            timeout=1800  # 30 min max per volume
        )
        duration = time.time() - start
        status = "SUCCESS" if result.returncode == 0 else "ERROR"
        return (volume, status, duration)
    except subprocess.TimeoutExpired:
        return (volume, "TIMEOUT", 1800)
    except Exception as e:
        return (volume, f"FAILED: {e}", 0)

def turbo_scan():
    """Scan all volumes in parallel."""
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🌊 TURBO MINER - MULTI-VOLUME PARALLEL SCANNER                  ║")
    print("║  ⚡ ZERO LATENCY EDITION                                         ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    # Check which volumes are mounted
    available = [v for v in VOLUMES if os.path.exists(v)]
    print(f"📂 DETECTED VOLUMES: {len(available)}/{len(VOLUMES)}")
    for v in available:
        print(f"   ✅ {v}")
    print()
    
    if not available:
        print("❌ No volumes mounted. Nothing to scan.")
        return
    
    start_time = time.time()
    
    # Scan all volumes in parallel
    print("🚀 LAUNCHING PARALLEL SCANNERS...")
    print()
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(available)) as executor:
        futures = {executor.submit(scan_volume, v): v for v in available}
        for future in concurrent.futures.as_completed(futures):
            vol, status, duration = future.result()
            results.append((vol, status, duration))
            print(f"   {'✅' if status == 'SUCCESS' else '❌'} {os.path.basename(vol)}: {status} ({duration:.1f}s)")
    
    total_time = time.time() - start_time
    
    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  ✅ TURBO SCAN COMPLETE                                          ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"   ⏱️  TOTAL TIME: {total_time:.1f}s")
    print(f"   📊 VOLUMES PROCESSED: {len(results)}")
    print()

if __name__ == "__main__":
    turbo_scan()
