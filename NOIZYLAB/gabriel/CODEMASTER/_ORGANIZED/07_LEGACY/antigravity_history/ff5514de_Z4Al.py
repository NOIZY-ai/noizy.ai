#!/usr/bin/env python3
import subprocess
import os
import sys

STAGING_AREA = "/Volumes/6TB/Audio_Universe"
REMOTE_NAME = "FISHMUSIC_MASTERS" # User must name it this, or we ask
REMOTE_PATH = "MC96UNIVERSE" # The cloud folder

# 🚀 JUMBO FRAMES MODE (High Performance Rclone)
# We treat files like Jumbo Frames: Big Chunks, Parallel Streams.
JUMBO_FLAGS = [
    "--transfers=16",        # Parallel files
    "--checkers=16",         # Parallel checks
    "--drive-chunk-size=128M", # "Jumbo Frame" equivalent for GDrive
    "--pacer-min-sleep=10ms",  # Aggressive API calls
    "--stats=1s",            # Update often
    "--progress"             # Show the bar
]

def check_vault_mounted():
    return os.path.exists(STAGING_AREA)

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
    print("CORE > 🚀 DEPLOYING TO MC96UNIVERSE...")
    
    if not check_rclone_installed():
        print("CORE > ❌ Error: rclone is not installed. Please run: brew install rclone")
        return

    if not check_remote_exists(REMOTE_NAME):
        print(f"CORE > ⚠️  Remote '{REMOTE_NAME}' not configured.")
        print("CORE > [INSTRUCTION] Run 'rclone config' in terminal to link Google Drive.")
        return

    print(f"CORE > 📡 Syncing Local Staging Area -> Google Drive/{REMOTE_PATH}...")
    print(f"CORE > 📂 Source: {STAGING_AREA}")
    
    cmd = [
        "rclone", "sync", 
        STAGING_AREA, 
        f"{REMOTE_NAME}:{REMOTE_PATH}",
        "--create-empty-src-dirs" 
    ] + JUMBO_FLAGS
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\nCORE > ✅ SUCCESS! The Universe is synced to {REMOTE_PATH}.")
    except subprocess.CalledProcessError as e:
        print(f"\nCORE > ❌ Sync Failed: {e}")

if __name__ == "__main__":
    deploy()
