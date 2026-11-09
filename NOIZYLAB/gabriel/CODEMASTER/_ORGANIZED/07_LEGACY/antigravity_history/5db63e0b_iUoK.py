import time
import os
import sys
import subprocess
from pathlib import Path

try:
    import turbo_config as cfg
except ImportError:
    # If config not found in path, try adding current dir
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

# Configuration
WATCH_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else cfg.DEFAULT_SEARCH_DIRS[0]
INGEST_SCRIPT = cfg.SCRIPTS_DIR / "turbo_ingest.py"
LOG_FILE = cfg.SCRIPTS_DIR.parent / "turbo_sentinel.log" # Log in parent for cleanliness

def log_to_file(msg):
    timestamp = time.strftime('%H:%M:%S')
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_file_stats(directory):
    stats = {}
    try:
        if not directory.exists(): return {}
        for f in directory.iterdir():
            if f.name.startswith('.'): continue
            if f.name.endswith('.download'): continue
            if f.name.endswith('.crdownload'): continue 
            try:
                stats[f.name] = f.stat().st_size
            except: pass
    except: pass
    return stats

def run_sentinel():
    cfg.print_header("🛡️  THE SENTINEL", f"Watching: {WATCH_DIR}")
    
    log_to_file("Sentinel Started.")
    
    # Initialize State
    last_state = get_file_stats(WATCH_DIR)
    
    try:
        while True:
            time.sleep(1) # Zero Latency Optimization: Poll every 1s
            
            current_state = get_file_stats(WATCH_DIR)
            
            # Detect New Files
            new_files = []
            for name, size in current_state.items():
                if name not in last_state:
                    new_files.append(name)
            
            # Process New Files
            if new_files:
                cfg.system_log(f"👀 Detected {len(new_files)} new files...", "WARN")
                
                # Debounce: Wait for size to settle
                time.sleep(1) 
                stable = True
                check_state = get_file_stats(WATCH_DIR)
                
                for nf in new_files:
                    if nf not in check_state or check_state[nf] != current_state.get(nf, -1):
                        cfg.system_log(f"⏳ File {nf} is still growing, waiting...", "INFO")
                        stable = False
                        break
                
                if stable:
                    log_to_file(f"Triggering Harvester for: {', '.join(new_files)}")
                    
                    try:
                        cfg.system_log(f"🚀 Triggering Harvester...", "SUCCESS")
                        subprocess.run(['python3', str(INGEST_SCRIPT), str(WATCH_DIR)], check=True)
                        log_to_file("Harvester Run Complete.")
                        
                        last_state = get_file_stats(WATCH_DIR) 
                        continue 
                        
                    except Exception as e:
                        cfg.system_log(f"Harvester Error: {e}", "ERROR")
                        log_to_file(f"Harvester Error: {e}")
            
            # Update State (Handle deletions/moves)
            last_state = get_file_stats(WATCH_DIR)
            
    except KeyboardInterrupt:
        log_to_file("Sentinel Stopped.")
        print(f"\n{cfg.RED}CORE > 🛑 Sentinel Offline.{cfg.RESET}")

if __name__ == "__main__":
    if not INGEST_SCRIPT.exists():
        print(f"{cfg.RED}CORE > Error: Could not find {INGEST_SCRIPT}{cfg.RESET}")
        sys.exit(1)
        
    run_sentinel()

