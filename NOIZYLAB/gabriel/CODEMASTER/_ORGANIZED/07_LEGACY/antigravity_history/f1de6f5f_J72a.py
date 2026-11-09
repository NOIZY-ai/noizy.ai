import os
import shutil

def nuke_empty_folders(root_path):
    print(f"🚀 Scanning: {root_path}")
    deleted_count = 0
    
    # Walk bottom-up so we can delete nested empty folders
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Skip system areas if we accidentally wander there (sanity check)
        if "/Library/" in dirpath or "/.Trashes" in dirpath:
            continue
            
        try:
            # If directory is empty (no files and no subdirectories)
            if not os.listdir(dirpath):
                # Double check it's not a mount point
                if not os.path.ismount(dirpath):
                    os.rmdir(dirpath)
                    print(f"💥 Nuked: {dirpath}")
                    deleted_count += 1
        except Exception as e:
            # Ignore permission errors, just keep moving
            pass
            
    return deleted_count

if __name__ == "__main__":
    targets = [
        "/Users/m2ultra/Documents",
        "/Users/m2ultra/Downloads",
        "/Users/m2ultra/Desktop",
        "/Users/m2ultra/Music",
        "/Users/m2ultra/Pictures",
        "/Users/m2ultra/NOIZYLAB" 
    ]
    
    # Add all external volumes
    volumes_dir = "/Volumes"
    if os.path.exists(volumes_dir):
        for vol in os.listdir(volumes_dir):
            full_path = os.path.join(volumes_dir, vol)
            # Skip the startup disk link if it's just a symlink or the root itself to prevent loops
            if os.path.islink(full_path): 
                continue
            targets.append(full_path)

    total_nuked = 0
    for target in targets:
        if os.path.exists(target):
            total_nuked += nuke_empty_folders(target)

    print(f"\n💀 TOTAL DESTRUCTION COMPLETE. {total_nuked} empty folders obliterated.")
