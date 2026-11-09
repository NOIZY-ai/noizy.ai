import time
import sys
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from noizy_memcell import memory_core

# NOIZYLAB GUARDIAN v2.0
# "Sentinel" Module: Autonomous Audio Protection & Indexing
# OPTIMIZED: MemCell Integration, Ignore logic for partial downloads

class AudioSentinel(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        
        filename = os.path.basename(event.src_path)
        if filename.endswith(('.wav', '.mp3', '.aif', '.aiff', '.flac')):
            # v2.0 FIX: Ignore partial downloads
            if "download" in filename or "part" in filename: return
            
            overlap = memory_core.analyze_temporal_overlap()
            vibe = overlap["overlap_status"]
            
            print(f"\n>>> [THE SENTINEL v3.0] NEW ASSET DETECTED: {filename}")
            print(f"    -> VIBE CONTEXT: {vibe}")
            memory_core.log_interaction(f"Guardian Detection: {filename} [{vibe}]", "GUARD_ALERT", "SHIRL")
            
            # Trigger Cortex v3.0
            subprocess.run(['python3', 'noizy_cortex.py', event.src_path])
            # Trigger analysis
            subprocess.run(["python3", "noizy_cortex.py", filename])
            print(">>> [THE GUARDIAN] ASSET SECURED & INDEXED.")
            memory_core.log_interaction(f"Secured: {os.path.basename(filename)}", "SUCCESS", "ENGR")

def start_guardian(path):
    print(f"""
    ___________________________________________________________
      T H E   G U A R D I A N   O F   N O I Z Y   L A B
      v2.0 // ZERO LATENCY PROTOCOL // MEMCELL ACTIVE
    ___________________________________________________________
     Watching: {path}
     Protocols: ACTIVE
     Council: KEITH | SHIRL | POPS | ALEX | DREAM
    """)
    
    memory_core.log_interaction(f"Sentinel Watch: {path}", "BOOT", "SHIRL")
    
    event_handler = AudioSentinel()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n>>> THE GUARDIAN STANDS DOWN.")
        memory_core.log_interaction("Sentinel Stand Down", "SHUTDOWN", "SHIRL")
    
    observer.join()

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    start_guardian(target_path)
