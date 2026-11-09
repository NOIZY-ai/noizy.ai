import os
import shutil
import argparse
from pathlib import Path

# Configuration
AUDITION_STAGE = "/Users/m2ultra/Audio_Unitor/Audition_Stage"
STAGING_AREA = "/Users/m2ultra/Audio_Unitor/Staging_Area"

def fetch_file(alias_path):
    alias = Path(alias_path)
    
    if not alias.exists():
        print(f"❌ Error: File not found: {alias_path}")
        return

    if not alias.is_symlink():
        # Might be a regular file if they put it there manually
        print(f"⚠️  Note: {alias.name} is not an alias. Copying anyway.")
        real_path = alias
    else:
        # Resolve the symlink to the Vault
        real_path = alias.resolve()
        print(f"🔗 Resolved Alias -> Vault: {real_path}")

    if not real_path.exists():
        print(f"❌ Error: Vault file missing! Is the drive plugged in? ({real_path})")
        return

    # Destination
    dest_path = Path(AUDITION_STAGE) / alias.name
    
    print(f"⚡️ Materializing to NVMe Stage...")
    try:
        shutil.copy2(real_path, dest_path)
        print(f"✅ Success: {dest_path}")
        print("   Ready for surgery.")
    except Exception as e:
        print(f"❌ Error copying: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Unitor: Materialize Alias to Stage")
    parser.add_argument("file", help="Path to the alias you want to edit")
    args = parser.parse_args()
    
    fetch_file(args.file)
