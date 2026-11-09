#!/usr/bin/env python3
"""
MC96 Network Backup Utility — DGS1210-10 Smart Switch
Author: Rob + MC96 System
Purpose: Auto-pull switch configuration & archive to Gabriel root
"""

import os
import time
import datetime
import requests
from pathlib import Path

# === CONFIG ===
SWITCH_IP = "192.168.0.2"              # Static IP of your DGS1210-10
USERNAME = "admin"                     # Update if changed
PASSWORD = "YOUR_SECURE_PASSWORD"      # Change this before use
DEST_DIR = Path("/GABRIEL/System/NetworkBackups")  # Default destination
LOG_FILE = DEST_DIR / "backup_log.txt"

# === ADVANCED SETTINGS ===
TIMEOUT = 15
BACKUP_PREFIX = "DGS1210_CFG"
DATESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
BACKUP_FILE = DEST_DIR / f"{BACKUP_PREFIX}_{DATESTAMP}.cfg"

# === FUNCTIONS ===
def ensure_paths():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        LOG_FILE.touch()

def log(msg):
    ts = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} {msg}\n")
    print(msg)

def backup_switch():
    """Pull config file via HTTP API (works on firmware 6.10+)."""
    url = f"http://{SWITCH_IP}/cgi-bin/DownloadCfg.cgi"
    auth = (USERNAME, PASSWORD)
    try:
        log(f"Connecting to switch at {SWITCH_IP} ...")
        response = requests.get(url, auth=auth, timeout=TIMEOUT)
        if response.status_code == 200:
            with open(BACKUP_FILE, "wb") as f:
                f.write(response.content)
            log(f"✅ Backup complete → {BACKUP_FILE}")
        else:
            log(f"⚠️  HTTP {response.status_code}: unable to retrieve config")
    except Exception as e:
        log(f"❌ Backup failed: {e}")

def prune_old_backups(keep_last=10):
    """Keep latest n backups, delete older ones."""
    files = sorted(DEST_DIR.glob(f"{BACKUP_PREFIX}_*.cfg"))
    if len(files) > keep_last:
        for old in files[:-keep_last]:
            old.unlink(missing_ok=True)
            log(f"🗑️  Removed old backup: {old.name}")

# === MAIN ===
if __name__ == "__main__":
    ensure_paths()
    backup_switch()
    prune_old_backups()
    log("Backup routine finished.\n")
