import os
import re
import argparse
from pathlib import Path

AUDITION_STAGE = "/Users/m2ultra/Audio_Unitor/Audition_Stage"

CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def batch_rename(pattern, replacement, dry_run=True):
    """Batch rename files in Audition Stage using regex."""
    stage = Path(AUDITION_STAGE)
    
    if not stage.exists():
        print("❌ Audition Stage not found.")
        return
    
    files = list(stage.iterdir())
    if not files:
        print("❌ Audition Stage is empty.")
        return
    
    print(f"🔄 Batch Rename in Audition Stage")
    print(f"   Pattern: {CYAN}{pattern}{RESET}")
    print(f"   Replace: {GREEN}{replacement}{RESET}")
    print(f"   Mode: {'[DRY RUN]' if dry_run else '[LIVE]'}")
    print("-" * 40)
    
    count = 0
    for f in files:
        if f.is_file():
            new_name = re.sub(pattern, replacement, f.name)
            if new_name != f.name:
                print(f"   {f.name} -> {new_name}")
                if not dry_run:
                    f.rename(stage / new_name)
                count += 1
    
    if count == 0:
        print("No matches found.")
    else:
        print(f"\n{'Would rename' if dry_run else 'Renamed'} {count} files.")
        if dry_run:
            print(f"{YELLOW}Run with --live to apply.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Rename files in Audition Stage")
    parser.add_argument("pattern", help="Regex pattern to match")
    parser.add_argument("replacement", help="Replacement string")
    parser.add_argument("--live", action="store_true", help="Actually rename files")
    
    args = parser.parse_args()
    batch_rename(args.pattern, args.replacement, dry_run=not args.live)
