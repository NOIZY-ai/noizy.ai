import os

ROOT = "/Volumes/JOE/NKI"
PREFIXES = ["turbo_scan_v", "turbo_rebuild_v", "launcher_v"]
KEEP = ["turbo_bfa_god.py", "turbo_backup_v1.py"]

count = 0
for f in os.listdir(ROOT):
    full_path = os.path.join(ROOT, f)
    if f in KEEP: continue
    
    should_delete = False
    for p in PREFIXES:
        if f.startswith(p):
            should_delete = True
            break
            
    if should_delete:
        try:
            os.remove(full_path)
            print(f"Deleted: {f}")
            count += 1
        except Exception as e:
            print(f"Error deleting {f}: {e}")

print(f"Total deleted: {count}")
