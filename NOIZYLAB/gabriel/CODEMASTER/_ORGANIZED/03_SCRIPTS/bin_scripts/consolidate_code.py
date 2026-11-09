import os
import shutil
import datetime
import subprocess

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

IGNORED_DIRS = {
    '.Spotlight-V100', '.Trashes', '.fseventsd', 'System Volume Information', 
    'node_modules', 'venv', '.venv', '__pycache__', '.git', 'vendor', 'Pods'
}

def log(message):
    print(message)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{datetime.datetime.now()} - {message}\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

def ensure_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            log(f"Created directory: {path}")
        except Exception as e:
            log(f"Error creating directory {path}: {e}")

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command, 
            cwd=cwd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            log(f"Command failed: {command}\nStderr: {result.stderr}")
            return False
        return True
    except Exception as e:
        log(f"Command execution error: {command}\nException: {e}")
        return False

def scan_and_copy():
    ensure_dir(DEST_BASE)
    ensure_dir(DOCS_DEST)
    
    log("Starting SUPER-SONIC deep scan and consolidation...")
    
    for volume in SOURCE_VOLUMES:
        if not os.path.exists(volume):
            log(f"Skipping unmounted volume: {volume}")
            continue
            
        log(f"Scanning volume: {volume}")
        volume_name = os.path.basename(volume)
        repo_dest_base = os.path.join(DEST_BASE, f"Imported_{volume_name.replace(' ', '_')}")
        ensure_dir(repo_dest_base)
        
        for root, dirs, files in os.walk(volume):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            # 1. Handle Git Repositories
            if '.git' in os.listdir(root) and os.path.isdir(os.path.join(root, '.git')):
                log(f"FOUND REPO: {root}")
                rel_path = os.path.relpath(root, volume)
                dest_path = os.path.join(repo_dest_base, rel_path)
                
                if os.path.exists(dest_path):
                    log(f"  Skipping existing: {dest_path}")
                else:
                    try:
                        shutil.copytree(root, dest_path, dirs_exist_ok=True)
                        log(f"  COPIED to: {dest_path}")
                    except Exception as e:
                        log(f"  ERROR copying repo {root}: {e}")
                
                dirs[:] = [] # Stop recursing into this repo
                continue

            # 2. Handle Markdown Files
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    safe_name = f"{volume_name}_{os.path.basename(root)}_{file}".replace(' ', '_').replace('/', '_')
                    dest_md = os.path.join(DOCS_DEST, safe_name)
                    if not os.path.exists(dest_md):
                        try:
                            shutil.copy2(file_path, dest_md)
                            # log(f"  Gathered MD: {file}")
                        except Exception as e:
                            log(f"  Error copying MD {file}: {e}")

    log("Scan complete. Initializing Git...")
    
    # Git Integration
    if not os.path.exists(os.path.join(DEST_BASE, ".git")):
        run_command("git init", cwd=DEST_BASE)
        run_command("git remote add origin https://github.com/NOIZYLAB-io/Code_Universe.git", cwd=DEST_BASE)
    
    run_command("git add .", cwd=DEST_BASE)
    run_command('git commit -m "Auto-consolidated code from external volumes"', cwd=DEST_BASE)
    
    log("Attempting GitHub push...")
    # Attempt simple push, assuming auth is configured
    if run_command("git push -u origin main", cwd=DEST_BASE):
        log("PUSH SUCCESSFUL!")
    else:
        log("Push failed. You may need to run 'gh auth login' or check remote manually.")

if __name__ == "__main__":
    scan_and_copy()
