import time
import sys
from pathlib import Path
from organize_audio import organize_folder

# Configuration
INBOX = "/Users/m2ultra/Downloads/Audio_Inbox"
STAGING = "/Users/m2ultra/Audio_Unitor/Staging_Area"
POLL_INTERVAL = 1.0 # Check every second

def hyper_drive_loop():
    print(f"{BOLD}{CYAN}CORE > 🚀 HYPER-DRIVE ACTIVATED 🚀{RESET}")
    print(f"CORE > Watching: {INBOX}")
    print(f"CORE > Target: {STAGING}")
    print(f"{YELLOW}CORE > Drop files in the Inbox. They will disappear and reappear organized Instantly.{RESET}")
    print(f"{DIM}CORE > Press Ctrl+C to stop.{RESET}")
    
    inbox_path = Path(INBOX)
    if not inbox_path.exists():
        inbox_path.mkdir(parents=True)
    
    try:
        while True:
            # Check if directory is not empty
            if any(inbox_path.iterdir()):
                # Run the organizer in LIVE mode
                # We suppress standard output to keep it clean, or maybe we want to see it?
                # Let's see the speed.
                organize_folder(INBOX, STAGING, dry_run=False)
            
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n🛑 Hyper-Drive Deactivated.")
        sys.exit(0)

if __name__ == "__main__":
    hyper_drive_loop()
