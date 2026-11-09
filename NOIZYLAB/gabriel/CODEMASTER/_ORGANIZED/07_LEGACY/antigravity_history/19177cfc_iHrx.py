import os
import sys

LOG_PATH = "/Users/m2ultra/Desktop/HEALTH_REPORT.txt"

def log(msg):
    # Print to console and file
    print(msg)
    try:
        with open(LOG_PATH, 'a') as f:
            f.write(msg + "\n")
    except: pass

def check_file_header(filepath):
    try:
        size = os.path.getsize(filepath)
        log(f"  SIZE: {size} bytes")
        
        if size == 0:
            log("  [ALERT] FILE IS EMPTY (0 KB). This is why it is 'Wrong'.")
            return

        with open(filepath, 'rb') as f:
            header = f.read(16)
            log(f"  HEADER HEX: {header.hex()}")
            try:
                text = header.decode('ascii', errors='ignore')
                log(f"  HEADER TEXT: {text}")
            except: pass
            
            # Known Kontakt magic bytes often appear near start or it sends a snippet.
            # BFA files usually are valid NKI.
            
    except Exception as e:
        log(f"  [ERROR] Cannot read file: {e}")

def main():
    if os.path.exists(LOG_PATH): os.remove(LOG_PATH)
    
    log("=== TURBO HEALTH CHECK ===")
    
    # 1. Check Mount
    mount = "/Volumes/JOE"
    if os.path.exists(mount):
        log(f"[OK] Mount '{mount}' exists.")
        try:
            items = os.listdir(mount)
            log(f"     Contains: {len(items)} items.")
        except Exception as e:
            log(f"[ERROR] Cannot list mount: {e}")
    else:
        log(f"[CRITICAL] Mount '{mount}' is MISSING.")
        return

    # 2. Check NKI Folder
    nki_dir = os.path.join(mount, "NKI")
    if os.path.exists(nki_dir):
        log(f"[OK] NKI Folder exists.")
        
        # 3. Check specific files
        sample_count = 0
        for f in os.listdir(nki_dir):
            if f.lower().endswith('.nki'):
                log(f"- Inspecting: {f}")
                check_file_header(os.path.join(nki_dir, f))
                sample_count += 1
                if sample_count >= 3: break
    else:
        log(f"[ERROR] NKI folder not found.")

if __name__ == "__main__":
    main()
