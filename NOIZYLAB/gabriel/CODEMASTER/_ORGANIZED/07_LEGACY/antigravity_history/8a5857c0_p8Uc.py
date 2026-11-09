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

    if check_remote_exists(REMOTE_NAME):
         cfg.system_log(f"Syncing Local Staging Area -> Google Drive/{REMOTE_PATH}...", "INFO")
         cmd = ["rclone", "sync", str(STAGING_AREA), f"{REMOTE_NAME}:{REMOTE_PATH}", "--create-empty-src-dirs"] + JUMBO_FLAGS
         try:
             subprocess.run(cmd, check=True)
             cfg.system_log(f"SUCCESS! The Universe is synced to {REMOTE_PATH}.", "SUCCESS")
         except subprocess.CalledProcessError as e:
             cfg.system_log(f"Drive Sync Failed: {e}", "ERROR")

    # 🚀 GIT PUSH (THE ONE TRUTH)
    CODE_ROOT = cfg.SCRIPTS_DIR.parent.parent
    cfg.system_log(f"Deploying Code from {CODE_ROOT} to {cfg.GIT_REMOTE_URL}...", "INFO")
    
    try:
        # Check if remote exists
        check_git = subprocess.run(["git", "remote", "get-url", "origin"], cwd=CODE_ROOT, capture_output=True, text=True)
        if "NOIZYLAB-io" not in check_git.stdout:
           # If origin is wrong or missing, try to fix or warn
           pass 
        
        # Add, Commit, Push
        subprocess.run(["git", "add", "."], cwd=CODE_ROOT, check=True)
        subprocess.run(["git", "commit", "-m", "Gabriel Build: God Mode Active"], cwd=CODE_ROOT)
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=CODE_ROOT, check=True)
        cfg.system_log("GIT DEPLOYMENT SUCCESSFUL. ONE TRUTH.", "SUCCESS")
    except Exception as e:
        cfg.system_log(f"Git Deploy Failed (Check Auth/Path): {e}", "WARN")

if __name__ == "__main__":
    deploy()
