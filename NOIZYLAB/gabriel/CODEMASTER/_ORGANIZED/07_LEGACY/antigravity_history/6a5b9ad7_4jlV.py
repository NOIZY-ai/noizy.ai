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
    print("🚀 DEPLOY TO MC96UNIVERSE 🚀")
    
    if not check_rclone_installed():
        print("❌ Error: rclone is not installed. Please run: brew install rclone")
        return

    if not check_remote_exists(REMOTE_NAME):
        print(f"⚠️  Remote '{REMOTE_NAME}' not configured.")
        print("---------------------------------------------------")
        print("You need to link your Google Drive.")
        print("RUN THIS COMMAND IN TERMINAL:  rclone config")
        print("  1. Press 'n' (New Remote)")
        print(f"  2. Name it: {REMOTE_NAME}")
        print("  3. Select 'Google Drive' (number varies, usually ~18)")
        print("  4. Follow the browser login steps.")
        print("---------------------------------------------------")
        return

    print(f"Syncing Local Staging Area -> Google Drive/{REMOTE_PATH}...")
    print(f"Source: {STAGING_AREA}")
    
    # Using --dry-run first? No, user said "LETS ROCK". But let's be safe.
    # Actually, let's just do it with progress.
    
    cmd = [
        "rclone", "sync", 
        STAGING_AREA, 
        f"{REMOTE_NAME}:{REMOTE_PATH}",
        "--create-empty-src-dirs" 
    ] + JUMBO_FLAGS
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ SUCCESS! The Universe is synced.")
        print(f"Check your Google Drive folder: {REMOTE_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Sync Failed: {e}")

if __name__ == "__main__":
    deploy()
