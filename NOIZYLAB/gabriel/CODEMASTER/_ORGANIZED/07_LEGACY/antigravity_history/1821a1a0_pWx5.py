import time
import os
import sys
import subprocess
from pathlib import Path

# Configuration
WATCH_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.expanduser(Path("~/Downloads"))
INGEST_SCRIPT = Path("Audio_Unitor/Scripts/turbo_ingest.py")
LOG_FILE = Path("sentinel.log")

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{timestamp}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def get_file_stats(directory):
    stats = {}
    try:
        if not directory.exists(): return {}
        for f in directory.iterdir():
            if f.name.startswith('.'): continue
            if f.name.endswith('.download'): continue # Skip partial downloads
            if f.name.endswith('.crdownload'): continue 
            try:
                stats[f.name] = f.stat().st_size
            except: pass
    except: pass
    return stats

def run_sentinel():
    print(f"{BOLD}{CYAN}🛡️  THE SENTINEL IS WATCHING{RESET}")
    print(f"   Target: {WATCH_DIR}")
    print(f"   Action: Trigger Harvester")
    
    log("Sentinel Started.")
    
    # Initialize State
    last_state = get_file_stats(WATCH_DIR)
    
    try:
        while True:
            time.sleep(2) # Poll every 2 seconds
            
            current_state = get_file_stats(WATCH_DIR)
            
            # Detect New Files
            new_files = []
            for name, size in current_state.items():
                if name not in last_state:
                    new_files.append(name)
            
            # Process New Files
            if new_files:
                print(f"\n{YELLOW}👀 Detected {len(new_files)} new files...{RESET}")
                
                # Debounce: Wait for size to settle
                time.sleep(3) 
                stable = True
                check_state = get_file_stats(WATCH_DIR)
                
                for nf in new_files:
                    if nf not in check_state or check_state[nf] != current_state.get(nf, -1):
                        print(f"   ⏳ File {nf} is still growing, waiting...")
                        stable = False
                        break
                
                if stable:
                    log(f"Triggering Harvester for: {', '.join(new_files)}")
                    # Trigger Ingest on the Whole Folder (Simpler for now, Ingest handles filtering)
                    # Or ideally, pass specific file. indexing handles whole folder fast.
                    try:
                        subprocess.run(['python3', str(INGEST_SCRIPT), str(WATCH_DIR)], check=True)
                        log("Harvester Run Complete.")
                        
                        # Update state to avoid re-triggering immediately 
                        # (Though Ingest moves files, so they will disappear from WATCH_DIR)
                        # We just need to refresh last_state after ingest
                        last_state = get_file_stats(WATCH_DIR) 
                        continue 
                        
                    except Exception as e:
                        log(f"Harvester Error: {e}")
            
            # Update State (Handle deletions/moves)
            last_state = get_file_stats(WATCH_DIR)
            
    except KeyboardInterrupt:
        log("Sentinel Stopped.")
        print(f"\n{RED}🛑 Sentinel Offline.{RESET}")

if __name__ == "__main__":
    if not INGEST_SCRIPT.exists():
        print(f"Error: Could not find {INGEST_SCRIPT}")
        sys.exit(1)
        
    run_sentinel()
