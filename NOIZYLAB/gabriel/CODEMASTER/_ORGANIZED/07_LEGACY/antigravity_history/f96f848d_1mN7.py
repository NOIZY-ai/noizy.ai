import os
import glob
import stat

ROOT = "/Volumes/JOE/NKI"

def log(msg):
    print(msg)
    # Try to write to a log file that we KNOW we can write to (chmod might allow it?)
    # But we found we can write files.
    try:
        with open(os.path.join(ROOT, "perm_log.txt"), "a") as f:
            f.write(msg + "\n")
    except: pass

def main():
    log("=== PERMISSION REPAIR ===")
    
    files = glob.glob(os.path.join(ROOT, "*.py"))
    files.append(os.path.join(ROOT, "launcher_v15.sh"))
    
    count = 0
    for f in files:
        try:
            # Grant Read/Write/Execute to Everyone (777)
            os.chmod(f, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            log(f"[OK] 777 -> {os.path.basename(f)}")
            count += 1
        except Exception as e:
            log(f"[FAIL] {os.path.basename(f)}: {e}")

    log(f"Attempted {len(files)} files. Fixed {count}.")

if __name__ == "__main__":
    main()
