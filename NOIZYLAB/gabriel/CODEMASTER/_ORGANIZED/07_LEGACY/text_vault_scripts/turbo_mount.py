#!/usr/bin/env python3
# ==============================================================================
# 🔌 TURBO MOUNT (CONNECTION PROTOCOL)
# ==============================================================================
# Mounts remote volumes from THE_VAULT (Old Mac Pro) via SMB/AFP
# Network Node: 10.90.90.30 (THE_VAULT) via DGS1210-10

import os
import sys
import subprocess
import time
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# CONFIGuration
MOUNT_POINT_ROOT = Path("/Volumes")
SERVER_IP = "10.90.90.30" # From Config
SERVER_NAME = "MacPro12Core"
PROTOCOL = "smb" # or afp

# KNOWN VOLUMES ON MAC PRO (Expand as needed)
# Assuming typical names or asking user. For now, general connect.
SHARES = ["Data", "Backup", "Audio_Archive"] 

def mount_share(share_name):
    mount_point = MOUNT_POINT_ROOT / share_name
    uri = f"{PROTOCOL}://{SERVER_IP}/{share_name}"
    
    if mount_point.exists():
        print(f"CORE > ✅ {share_name} appears to be mounted.")
        return True
        
    print(f"CORE > 🔌 Attempting to mount {share_name} from {SERVER_IP}...")
    
    try:
        # MacOS open command handles authentication dialog if needed, or uses Keychain
        ret = subprocess.run(["open", uri], capture_output=True, text=True)
        if ret.returncode == 0:
            print(f"CORE > ⏳ Connection initiated for {share_name}...")
            time.sleep(2) # Wait for mount
            if mount_point.exists():
                print(f"CORE > ✅ SUCCESS: {share_name} mounted.")
                return True
        else:
            print(f"CORE > ❌ Failed to initiate connection: {ret.stderr}")
            
    except Exception as e:
        print(f"CORE > ❌ Error: {e}")
        
    return False

def main():
    cfg.print_header("🔌 TURBO MOUNT", "QUARANTINED MODE")
    print(f"{cfg.RED}CORE > 🛑 MOUNTING LOGIC IS QUARANTINED.{cfg.RESET}")
    return
    
    print("CORE > 📡 Scanning for known shares...")
    
    mounted_count = 0
    for share in SHARES:
        if mount_share(share):
            mounted_count += 1
            
    if mounted_count > 0:
        cfg.system_log(f"Connected to {mounted_count} remote volumes.", "SUCCESS")
        # Trigger Sentinel Scan of /Volumes immediately
        try:
            print("CORE > 🛡️  Triggering Sentinel Scan on new mounts...")
            subprocess.Popen(["python3", str(cfg.SCRIPTS_DIR / "turbo_sentinel.py"), "/Volumes"])
        except: pass
    else:
        cfg.system_log("No volumes mounted. Check network/auth.", "WARN")

if __name__ == "__main__":
    main()
