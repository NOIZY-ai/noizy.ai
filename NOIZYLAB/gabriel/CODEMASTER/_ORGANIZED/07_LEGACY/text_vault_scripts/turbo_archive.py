#!/usr/bin/env python3
import time
import subprocess
from pathlib import Path
import turbo_config as cfg

# ------------------------------------------------------------------------------
# 🌙 TURBO ARCHIVE (NIGHTLY BACKUP)
# ------------------------------------------------------------------------------
# Running this script will sync the ACTIVE NVMe drive to the ARCHIVE Cloud/Ext.
# It is designed to run via cron at 3 AM.

def archive_protocol():
    cfg.print_header("🌙 TURBO ARCHIVE", "Nightly Sync Protocol")
    
    source = cfg.STAGING_AREA
    remote_name = cfg.REMOTE_DRIVE_NAME
    remote_path = cfg.REMOTE_PATH
    
    # Safety Check
    if not source.exists():
        cfg.system_log(f"CRITICAL: Active Source {source} not found!", "ERROR")
        return

    cfg.system_log(f"Initiating Sync: {source} -> {remote_name}:{remote_path}", "INFO")
    
    # Rclone Command (Jumbo Frames for Speed)
    cmd = [
        "rclone", "sync", str(source), f"{remote_name}:{remote_path}",
        "--transfers=16",
        "--checkers=16",
        "--drive-chunk-size=128M",
        "--pacer-min-sleep=10ms",
        "--stats=5s",
        "--progress",
        "--create-empty-src-dirs"
    ]
    
    try:
        # Run rclone
        subprocess.run(cmd, check=True)
        cfg.system_log("✅ ARCHIVE SYNC COMPLETE. SLEEP WELL.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        cfg.system_log(f"❌ ARCHIVE FAILED: {e}", "ERROR")
    except FileNotFoundError:
        cfg.system_log("❌ ERROR: rclone not installed.", "ERROR")

if __name__ == "__main__":
    archive_protocol()
