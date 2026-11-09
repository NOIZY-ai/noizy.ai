import os
import shutil
import datetime

# Configuration
SOURCE_VOLUMES = [
    "/Volumes/4TB Blue Fish",
    "/Volumes/JOE",
    "/Volumes/RED DRAGON",
    "/Volumes/4TB BLK",
    "/Volumes/6TB"
]
DEST_BASE = "/Users/m2ultra/NOIZYLAB/Code_Universe"
DOCS_DEST = os.path.join(DEST_BASE, "Documentation/Gathered_MDs")
LOG_FILE = "/Users/m2ultra/code_mining_log.txt"

SOURCE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs', '.c', '.cpp', '.h', '.hpp', 
    '.java', '.swift', '.rb', '.php', '.sh', '.zsh', '.html', '.css'
}

IGNORED_DIRS = {
    '.Spotlight-V100', '.Trashes', '.fseventsd', 'System Volume Information', 
    'node_modules', 'venv', '.venv', '__pycache__', '.git' # .git is handled separately
}

def log(message):
    print(message)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def scan_and_copy():
    ensure_dir(DEST_BASE)
    ensure_dir(DOCS_DEST)
    
    log("Starting deep scan and consolidation...")
    
    for volume in SOURCE_VOLUMES:
        if not os.path.exists(volume):
            log(f"Volume not mounted or not found: {volume}")
            continue
            
        log(f"Scanning volume: {volume}")
        volume_name = os.path.basename(volume)
        repo_dest_base = os.path.join(DEST_BASE, f"Imported_{volume_name.replace(' ', '_')}")
        ensure_dir(repo_dest_base)
        
        for root, dirs, files in os.walk(volume):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            # Check for Git Repo
            if '.git' in os.listdir(root) and os.path.isdir(os.path.join(root, '.git')):
                log(f"Found Git Repository: {root}")
                # Copy entire repo
                rel_path = os.path.relpath(root, volume)
                dest_path = os.path.join(repo_dest_base, rel_path)
                
                if os.path.exists(dest_path):
                    log(f"Skipping existing repo destination: {dest_path}")
                else:
                    try:
                        shutil.copytree(root, dest_path, dirs_exist_ok=True)
                        log(f"Copied repo to: {dest_path}")
                    except Exception as e:
                        log(f"Error copying repo {root}: {e}")
                
                # specific optimization: don't traverse inside the repo looking for more repos 
                # (unless we want submodules, but usually copying the root is enough)
                # But we definitely don't want to scan every file inside as "Loose Code"
                dirs[:] = [] 
                continue

            # Process files in non-repo directories
            for file in files:
                file_path = os.path.join(root, file)
                
                # Markdown
                if file.endswith(".md"):
                    # Handle collision
                    safe_name = f"{volume_name}_{os.path.basename(root)}_{file}".replace(' ', '_').replace('/', '_')
                    dest_md = os.path.join(DOCS_DEST, safe_name)
                    try:
                        shutil.copy2(file_path, dest_md)
                        # log(f"Copied MD: {file}")
                    except Exception as e:
                        log(f"Error copying MD {file}: {e}")
                
                # Loose Source Code (Optional: Enable if needed, currently might match too much junk)
                # ext = os.path.splitext(file)[1]
                # if ext in SOURCE_EXTENSIONS:
                    # Copy to Loose_Code?
                    # pass

    log("Scan and consolidation complete.")

if __name__ == "__main__":
    scan_and_copy()
