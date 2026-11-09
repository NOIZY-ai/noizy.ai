import os
import sys
import time
import subprocess
import json
import shutil
from pathlib import Path

# Add script dir to path to import siblings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from turbo_memcell import MemCell
    from volume_scanner import scan_volume_deep
except ImportError:
    print("CORE > Error: Dependencies (MemCell/VolumeScanner) not found.")
    sys.exit(1)

# Configuration
GHOST_MOUNT_ROOT = Path("/tmp/ghost_mounts")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def get_unmounted_volumes():
    """Finds HFS+/APFS/ExFAT partitions that are NOT currently mounted."""
    print(f"{CYAN}CORE > 👻 Scanning for Ghost Volumes...{RESET}")
    
    # 1. Get all disks
    cmd = ["diskutil", "list", "-plist"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        return []
        
    try:
        import plistlib
        data = plistlib.loads(result.stdout)
    except:
        print(f"{RED}CORE > Failed to parse diskutil output.{RESET}")
        return []

    candidates = []
    
    # Iterate through all disks and partitions
    for disk in data.get('AllDisksAndPartitions', []):
        for partition in disk.get('Partitions', []):
            volume_name = partition.get('VolumeName')
            device_id = partition.get('DeviceIdentifier')
            content = partition.get('Content', '')
            
            # Filter for likely data partitions
            if not volume_name: continue
            if "Recovery" in volume_name: continue
            if "Boot" in volume_name: continue
            
            # Check if mounted
            mount_point = partition.get('MountPoint')
            if not mount_point:
                # Double check with info in case plist is weird
                info = subprocess.run(["diskutil", "info", device_id], capture_output=True, text=True).stdout
                if "Mounted:                 No" in info:
                    candidates.append({
                        'name': volume_name,
                        'id': device_id,
                        'size': partition.get('Size', 0)
                    })
    
    return candidates

def ghost_scan(volume_info):
    name = volume_info['name']
    dev_id = volume_info['id']
    
    print(f"\n{BOLD}{YELLOW}CORE > 👻 FOUND GHOST: {name} ({dev_id}){RESET}")
    print(f"CORE > Initiating Stealth Mount (Read-Only)...")
    
    mount_point = GHOST_MOUNT_ROOT / name
    if not mount_point.exists():
        mount_point.mkdir(parents=True)
        
    # Mount Read-Only
    cmd = ["diskutil", "mount", "readOnly", "-mountPoint", str(mount_point), dev_id]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"{RED}CORE > Mount Failed: {res.stderr}{RESET}")
        return
        
    print(f"{GREEN}CORE > Mounted at {mount_point}. Scanning...{RESET}")
    
    # Log to Brain
    try:
        mc = MemCell()
        mc.log_event(mc.covenant_id, "GHOST_SCAN", f"Ghost Scanned Volume: {name}", vibe=80, author="GHOST_SCANNER")
    except: pass
    
    try:
        # Perform Deep Scan
        scan_volume_deep(str(mount_point))
    except Exception as e:
        print(f"{RED}CORE > Scan Error: {e}{RESET}")
    finally:
        # ALWAYS UNMOUNT
        print(f"CORE > 👻 Vanishing (Unmounting)...")
        subprocess.run(["diskutil", "unmount", "force", dev_id], capture_output=True)
        
        # Cleanup
        try:
            if mount_point.exists():
                mount_point.rmdir()
        except: pass
        
        print(f"{GREEN}CORE > {name} has vanished.{RESET}")

def main():
    if not os.geteuid() == 0:
        # We might need sudo for some mount operations, but diskutil often works for user ownership
        # print(f"{YELLOW}CORE > Note: Ghost Scanner might need sudo for some drives.{RESET}")
        pass

    ghosts = get_unmounted_volumes()
    
    if not ghosts:
        print(f"{GREEN}CORE > No unmounted ghost volumes found.{RESET}")
        return
        
    print(f"{BOLD}CORE > Found {len(ghosts)} unmounted volumes.{RESET}")
    
    for g in ghosts:
        choice = input(f"CORE > Scan ghost volume '{g['name']}'? (y/n/all): ").lower().strip()
        if choice == 'all':
            for remain in ghosts: ghost_scan(remain)
            return
        if choice == 'y':
            ghost_scan(g)

if __name__ == "__main__":
    main()
