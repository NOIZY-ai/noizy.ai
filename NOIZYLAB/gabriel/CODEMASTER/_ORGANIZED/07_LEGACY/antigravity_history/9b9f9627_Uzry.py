import os
import sys
import time
import subprocess
from pathlib import Path
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Configuration
VOLUME_ROOT = Path("/Volumes")
DB_PATH = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/universe.db")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

AUDIO_KEYWORDS = ['audio', 'sample', 'music', 'sound', 'plugin', 'vst', 'kontakt', 
                  'drum', 'synth', 'loop', 'preset', 'instrument', 'fx', 'wav', 'aiff']

def get_disk_usage(path):
    """Get disk usage for a volume."""
    try:
        result = subprocess.run(['df', '-h', path], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            return {'total': parts[1], 'used': parts[2], 'percent': parts[4]}
    except:
        pass
    return None

def find_audio_folders(volume, max_depth=3, limit=5):
    """Find audio-related folders in a volume."""
    results = []
    try:
        for root, dirs, files in os.walk(volume):
            depth = root.replace(volume, '').count(os.sep)
            if depth >= max_depth:
                dirs[:] = []  # Don't go deeper
                continue
            
            folder_name = os.path.basename(root).lower()
            if any(kw in folder_name for kw in AUDIO_KEYWORDS):
                results.append(root)
                if len(results) >= limit:
                    break
    except PermissionError:
        pass
    return results

def scan_all_volumes():
    # Initialize Conciousness
    try:
        brain = MemCell()
        brain.log_event(brain.covenant_id, "SCAN_START", "Volume Scanner: Initiating System-Wide Scan", vibe=60, author="TURBO_SCANNER")
    except: pass

    print(f"\n{BOLD}{CYAN}CORE > ╔═══════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}CORE > ║       V O L U M E   S C A N N E R     ║{RESET}")
    print(f"{BOLD}{CYAN}CORE > ╚═══════════════════════════════════════╝{RESET}\n")
    
    volumes_path = Path('/Volumes')
    volumes = [v for v in volumes_path.iterdir() if v.is_dir() or v.is_symlink()]
    
    print(f"CORE > Found {BOLD}{len(volumes)}{RESET} mounted volumes.\n")
    
    for vol in sorted(volumes):
        vol_name = vol.name
        
        # Skip M2Ultra (boot drive symlink)
        if vol_name == 'M2Ultra':
            print(f"CORE > 📀 {BOLD}{vol_name}{RESET} (Boot Drive - Skipped)")
            continue
        
        usage = get_disk_usage(str(vol))
        
        if usage:
            pct = int(usage['percent'].replace('%', ''))
            color = GREEN if pct < 70 else YELLOW if pct < 90 else RED
            print(f"CORE > 📀 {BOLD}{vol_name}{RESET}")
            print(f"CORE >    {color}Used: {usage['used']} / {usage['total']} ({usage['percent']}){RESET}")
        else:
            print(f"CORE > 📀 {BOLD}{vol_name}{RESET}")
        
        # Find audio folders
        audio_folders = find_audio_folders(str(vol))
        for folder in audio_folders:
            rel_path = folder.replace(str(vol), '')
            print(f"CORE >    🎵 {rel_path}")
        
        print()

def scan_volume_deep(volume_path, extensions=None):
    """Deep scan a specific volume for audio files."""
    if extensions is None:
        extensions = {'.wav', '.aif', '.aiff', '.mp3', '.flac', '.ogg', '.mid', '.midi'}
    
    print(f"\n{BOLD}CORE > Deep Scanning: {volume_path}{RESET}\n")
    
    file_count = 0
    folder_stats = {}
    
    try:
        for root, dirs, files in os.walk(volume_path):
            audio_files = [f for f in files if Path(f).suffix.lower() in extensions]
            if audio_files:
                folder_stats[root] = len(audio_files)
                file_count += len(audio_files)
    except PermissionError:
        print(f"CORE > {RED}Permission denied for some folders.{RESET}")
    
    # Top 10 folders by audio file count
    top_folders = sorted(folder_stats.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"CORE > Total Audio Files: {BOLD}{file_count:,}{RESET}\n")
    print(f"CORE > {BOLD}Top 10 Audio Hotspots:{RESET}")
    for folder, count in top_folders:
        print(f"CORE >   {count:5d} files - {folder}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Audio Volume Scanner")
    parser.add_argument("--deep", help="Deep scan a specific volume path")
    args = parser.parse_args()
    
    if args.deep:
        scan_volume_deep(args.deep)
    else:
        scan_all_volumes()
