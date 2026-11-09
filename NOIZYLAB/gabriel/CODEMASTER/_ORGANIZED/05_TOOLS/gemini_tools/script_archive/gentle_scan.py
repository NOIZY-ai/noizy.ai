import os
import time
import sys

root_dir = "/Volumes/6TB/Sample_Libraries"
file_count = 0
dir_count = 0
start_time = time.time()

print(f"Starting Low-Voltage Scan of {root_dir}...")
print("Ramping up gently... 🟢")

try:
    for root, dirs, files in os.walk(root_dir):
        # Go easy
        time.sleep(0.005) 
        
        dir_count += 1
        file_count += len(files)
        
        # Periodic update
        if dir_count % 100 == 0:
            elapsed = time.time() - start_time
            sys.stdout.write(f"\rScanned {dir_count} folders, {file_count} files... ({elapsed:.1f}s)")
            sys.stdout.flush()
            
except KeyboardInterrupt:
    print("\nScan interrupted by user.")

end_time = time.time()
duration = end_time - start_time

print(f"\n\n✅ Scan Complete (or stopped).")
print(f"Total Folders: {dir_count}")
print(f"Total Files: {file_count}")
print(f"Time Taken: {duration:.2f} seconds")
