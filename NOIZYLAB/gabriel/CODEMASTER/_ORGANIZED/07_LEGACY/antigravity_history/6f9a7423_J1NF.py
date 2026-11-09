#!/usr/bin/env python3
import os
import sys
import shutil
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import turbo_config as cfg
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg

try:
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
CODE_EXTS = {
    '.py', '.js', '.html', '.css', '.java', '.c', '.cpp', '.h', '.hpp', 
    '.go', '.rs', '.swift', '.ts', '.tsx', '.jsx', '.php', '.rb', '.sh', 
    '.bash', '.zsh', '.md', '.json', '.xml', '.yml', '.yaml', '.sql'
}

# Ignore these
IGNORE_DIRS = {
    'node_modules', 'venv', '.git', '.idea', '__pycache__', 'build', 'dist', 
    'target', 'vendor', 'Pods', '.gradle', 'System', 'Library', 'Applications'
}

# Destination
CODE_VAULT = Path.expanduser(Path("~/Universal/Code_Universe"))

def is_safe_path(p):
    parts = p.parts
    for part in parts:
        if part in IGNORE_DIRS: return False
        if part.startswith('.'): return False # Hidden dirs
    return True

def collect_file(fpath, vault_root):
    try:
        p = Path(fpath)
        # Size sanity check (skip huge files)
        if p.stat().st_size > 5 * 1024 * 1024: return (0, "Too Big") # 5MB limit for source code
        
        # Calculate Dest Path
        # We want to preserve structure: Vault / VolumeName / ...path...
        # If /Users/m2ultra/... -> Vault / Macintosh HD / Users / m2ultra ...
        
        # Get volume and relative path
        parts = p.parts
        if parts[1] == 'Volumes':
            vol_name = parts[2]
            rel_path = Path(*parts[3:])
        else:
            vol_name = "Macintosh_HD" # Boot drive
            rel_path = Path(*parts[1:]) # Skip root /
            
        dest_path = vault_root / vol_name / rel_path
        
        if dest_path.exists():
            # Check if identical? For now, skip if exists to save time/churn
            if dest_path.stat().st_size == p.stat().st_size:
                return (0, "Exists")
        
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest_path)
        
        return (1, str(dest_path))
        
    except Exception as e:
        return (-1, str(e))

def run_collector():
    cfg.print_header("📦 TURBO COLLECTOR", "Harvesting All Code from Every Volume")
    
    brain = MemCell()
    brain.log_event(brain.covenant_id, "COLLECTOR_START", "Code Collection Protocol Initiated", vibe=80, author="TURBO_COLLECTOR")
    
    if not CODE_VAULT.exists():
        CODE_VAULT.mkdir(parents=True)
        # Init Git
        subprocess.run(["git", "init"], cwd=CODE_VAULT, check=True)
        cfg.system_log("Initialized Code Universe Git Repo.", "SUCCESS")

    volumes_path = Path('/Volumes')
    volumes = [v for v in volumes_path.iterdir() if v.is_dir() and not v.name.startswith('.')]
    # Add root drive
    volumes.append(Path('/Users/m2ultra')) # Scan home dir specifically instead of full root to be safe/faster
    
    all_files = []
    
    print(f"CORE > Scanning {len(volumes)} Roots for Code...")
    
    for vol in volumes:
        cfg.system_log(f"Scanning {vol}...", "INFO")
        try:
            for root, dirs, files in os.walk(vol):
                # Prune ignores
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
                
                # Safety check for root paths (don't scan deep system folders if we hit them)
                if str(root).startswith("/System") or str(root).startswith("/Library"): continue
                
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in CODE_EXTS:
                        all_files.append(Path(root) / f)
        except Exception as e:
            cfg.system_log(f"Error scanning {vol}: {e}", "WARN")

    print(f"CORE > Found {len(all_files):,} candidate files.")
    # No confirmation needed for this run to avoid blocking if unsupervised, OR prompt user.
    # User said "IF WE COLLECT...". I will assume they want it available.
    # But for safety, I will keep the confirmation input commented out or default YES if auto.
    # But since this is run interactively via Nexus, input is fine.
    
    confirm = input(f"{cfg.YELLOW}CORE > Ready to Ingest to {CODE_VAULT}? [Y/n] {cfg.RESET}")
    if confirm.lower() == 'n': return

    count = 0
    errors = 0
    start_t = time.time()
    
    cfg.system_log("Ingesting...", "INFO")
    
    with ThreadPoolExecutor(max_workers=16) as executor:
        future_to_file = {executor.submit(collect_file, f, CODE_VAULT): f for f in all_files}
        
        for i, future in enumerate(as_completed(future_to_file)):
            res, msg = future.result()
            if res == 1: count += 1
            elif res == -1: errors += 1
            
            if (i+1) % 100 == 0:
                print(f"CORE > Progress: {i+1}/{len(all_files)} | Collected: {count} | Errors: {errors}", end='\r')

    print(f"\n{cfg.GREEN}CORE > Collection Complete.{cfg.RESET}")
    
    # GIT COMMIT
    cfg.system_log("Committing to Git...", "INFO")
    try:
        subprocess.run(["git", "add", "."], cwd=CODE_VAULT, check=True)
        subprocess.run(["git", "commit", "-m", f"Turbo Collection: {count} files ingested."], cwd=CODE_VAULT)
        cfg.system_log("Git Commit Successful.", "SUCCESS")
    except Exception as e:
        cfg.system_log(f"Git Error: {e}", "ERROR")

    # MEMCELL LOGGING
    brain.log_event(brain.covenant_id, "COLLECTION_COMPLETE", f"Ingested {count} code files into Code Universe.", vibe=90, author="TURBO_COLLECTOR")

if __name__ == "__main__":
    run_collector()
