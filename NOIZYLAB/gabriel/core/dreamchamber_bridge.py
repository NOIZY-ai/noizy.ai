import os
import time
import subprocess
import logging
from pathlib import Path

# --- CONFIGURATION ---
PC_IP = "10.90.90.20"
CHECK_INTERVAL = 10  # Seconds
MOUNT_SCRIPT = Path(__file__).parent / "mount_pc_shares.sh"
LOG_FILE = Path(__file__).parent.parent / "logs" / "dreamchamber.log"

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ping_pc(ip):
    """Returns True if PC is responsive."""
    try:
        # Ping with loose timeout (1s)
        subprocess.check_call(
            ['ping', '-c', '1', '-W', '1000', ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False

def is_mounted(mount_point="/Volumes/PC_Bridge"):
    return os.path.ismount(mount_point)

def trigger_mount():
    """Executes the shell script to mount shares."""
    logging.info("Attempting to mount PC Shares...")
    try:
        result = subprocess.run(
            [str(MOUNT_SCRIPT)], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            logging.info(f"MOUNT SUCCESS: {result.stdout.strip()}")
            return True
        else:
            logging.error(f"MOUNT FAILED: {result.stderr.strip()}")
            return False
    except Exception as e:
        logging.error(f"EXECUTION ERROR: {e}")
        return False

def main():
    logging.info("BRIDGE STARTED: Monitoring Link...")
    print(f"🌉 DREAMCHAMBER BRIDGE: ACTIVE (Target: {PC_IP})")
    
    was_online = False
    
    while True:
        online = ping_pc(PC_IP)
        
        if online:
            if not was_online:
                logging.info("PC ONLINE detected.")
                print("🟢 PC ONLINE")
            
            # Check if we need to mount
            if not is_mounted():
                logging.warning("Shares not mounted. Triggering auto-mount...")
                trigger_mount()
            
            was_online = True
        else:
            if was_online:
                logging.warning("PC went OFFLINE.")
                print("🔴 PC OFFLINE")
            was_online = False
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
