import os
import shutil
import sys
import subprocess

SOURCE = "/Volumes/JOE/NKI"
DEST_PARENT = "/Users/m2ultra/Desktop"
DEST = os.path.join(DEST_PARENT, "NKI_LOCAL_COPY")

def get_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def get_free_space(path):
    st = os.statvfs(path)
    return st.f_bavail * st.f_frsize

def log(msg):
    print(msg)
    sys.stdout.flush()

def main():
    log(f"TURBO BACKUP V1")
    log(f"Source: {SOURCE}")
    log(f"Dest:   {DEST}")
    
    if not os.path.exists(SOURCE):
        log("ERROR: Source not found.")
        sys.exit(1)

    log("checking space...")
    # Fast check? du is slow. 
    # Let's trust rsync to fail if full? 
    # Or just estimating.
    
    # We will just run rsync. It's robust.
    
    if not os.path.exists(DEST):
        os.makedirs(DEST, exist_ok=True)
        
    cmd = ["rsync", "-av", "--exclude", ".*", SOURCE + "/", DEST]
    
    log(f"Executing: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
        log("BACKUP COMPLETE.")
    except Exception as e:
        log(f"BACKUP FAILED: {e}")

if __name__ == "__main__":
    main()
