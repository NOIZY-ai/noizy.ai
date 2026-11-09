import time
import sys
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# NOIZYLAB GUARDIAN v1.0
# "Sentinel" Module: Autonomous Audio Protection & indexing
# Dedicated to: Engr_Keith, Shirl, Pops, Alex Ward, Dream

class AudioSentinel(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        filename = event.src_path
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ['.wav', '.mp3', '.aif', '.aiff', '.flac']:
            print(f"\n>>> [THE GUARDIAN] NEW AUDIO DETECTED: {filename}")
            print("    -> Awakening Cortex...")
            # Trigger analysis
            subprocess.run(["python3", "noizy_cortex.py", filename])
            print(">>> [THE GUARDIAN] ASSET SECURED & INDEXED.")

def start_guardian(path):
    print(f"""
    ___________________________________________________________
      T H E   G U A R D I A N   O F   N O I Z Y   L A B
    ___________________________________________________________
     Watching: {path}
     Protocols: ACTIVE
     Council: KEITH | SHIRL | POPS | ALEX | DREAM
    """)
    
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
    
    observer.join()

if __name__ == "__main__":
    target_path = sys.argv[1] if len(sys.argv) > 1 else "."
    start_guardian(target_path)
