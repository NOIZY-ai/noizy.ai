import os
import shutil

ROOT = "/Volumes/JOE/NKI"

def log(msg):
    print(msg)

def main():
    log("=== TURBO CACHE CLEANER ===")
    
    deleted_files = 0
    deleted_dirs = 0
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # 1. Remove __pycache__ directories
        if "__pycache__" in dirnames:
            p = os.path.join(dirpath, "__pycache__")
            try:
                shutil.rmtree(p)
                log(f"[DEL DIR] {p}")
                deleted_dirs += 1
            except Exception as e:
                log(f"[FAIL] {p}: {e}")
            dirnames.remove("__pycache__") # Don't traverse

        # 2. Remove files
        for f in filenames:
            if f == ".DS_Store" or f.endswith(".pyc") or f == "probe_result.txt" or f == "omega_log.txt" or f == "rebuild_log.txt":
                p = os.path.join(dirpath, f)
                try:
                    os.remove(p)
                    log(f"[DEL FILE] {p}")
                    deleted_files += 1
                except Exception as e:
                    log(f"[FAIL] {p}: {e}")

    log("-" * 40)
    log(f"Cleaned {deleted_files} files and {deleted_dirs} folders.")

if __name__ == "__main__":
    main()
