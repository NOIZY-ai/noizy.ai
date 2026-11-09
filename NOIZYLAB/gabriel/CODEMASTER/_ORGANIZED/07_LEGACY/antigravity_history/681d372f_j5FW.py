import os
import datetime

inventory_root = "/Volumes/12TB/Volume_Inventory"
os.makedirs(inventory_root, exist_ok=True)

volumes_dir = "/Volumes"
volumes = [v for v in os.listdir(volumes_dir) if not v.startswith('.')]

print(f"Found {len(volumes)} volumes to scan.")

for vol in volumes:
    vol_path = os.path.join(volumes_dir, vol)
    if os.path.islink(vol_path):
        continue
        
    print(f"Scanning {vol}...")
    report_file = os.path.join(inventory_root, f"Inventory_{vol}.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"Inventory of {vol}\n")
        f.write(f"Date: {datetime.datetime.now()}\n")
        f.write("-" * 50 + "\n")
        
        file_count = 0
        try:
            for root, dirs, files in os.walk(vol_path):
                # Optional: Skip system/hidden folders if needed?
                # For now, scan everything to be complete
                for name in files:
                    try:
                        path = os.path.join(root, name)
                        size = os.path.getsize(path)
                        f.write(f"{size}\t{path}\n")
                        file_count += 1
                    except OSError:
                        pass
        except Exception as e:
            f.write(f"Error scanning: {e}\n")
            
        f.write(f"\nTotal Files: {file_count}\n")
    print(f"Finished {vol}: {file_count} files.")
