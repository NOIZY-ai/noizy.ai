#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

STAGING_AREA = cfg.STAGING_AREA
REMOTE_NAME = cfg.REMOTE_DRIVE_NAME
REMOTE_PATH = cfg.REMOTE_PATH

# 🚀 JUMBO FRAMES MODE (High Performance Rclone)
JUMBO_FLAGS = [
    "--transfers=16",        
    "--checkers=16",         
    "--drive-chunk-size=128M",
    "--pacer-min-sleep=10ms", 
    "--stats=1s",            
    "--progress"             
]

def check_vault_mounted():
    return STAGING_AREA.exists()

def check_rclone_installed():
    try:
        subprocess.run(["rclone", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except:
        return False

def check_remote_exists(remote):
    try:
        result = subprocess.run(["rclone", "listremotes"], capture_output=True, text=True)
        return f"{remote}:" in result.stdout
    except:
        return False

def deploy():
    cfg.print_header("🚀 TURBO DEPLOY", "Syncing to MC96UNIVERSE")
    
    if not check_rclone_installed():
        cfg.system_log("Error: rclone is not installed. Please run: brew install rclone", "ERROR")
        return

    if not check_remote_exists(REMOTE_NAME):
        cfg.system_log(f"Remote '{REMOTE_NAME}' not configured.", "WARN")
        print("CORE > [INSTRUCTION] Run 'rclone config' in terminal to link Google Drive.")
        return

    cfg.system_log(f"Syncing Local Staging Area -> Google Drive/{REMOTE_PATH}...", "INFO")
    print(f"CORE > 📂 Source: {STAGING_AREA}")
    
    cmd = [
        "rclone", "sync", 
        str(STAGING_AREA), 
        f"{REMOTE_NAME}:{REMOTE_PATH}",
        "--create-empty-src-dirs" 
    ] + JUMBO_FLAGS
    
    try:
        subprocess.run(cmd, check=True)
        cfg.system_log(f"SUCCESS! The Universe is synced to {REMOTE_PATH}.", "SUCCESS")
    except subprocess.CalledProcessError as e:
        cfg.system_log(f"Sync Failed: {e}", "ERROR")

if __name__ == "__main__":
    deploy()
