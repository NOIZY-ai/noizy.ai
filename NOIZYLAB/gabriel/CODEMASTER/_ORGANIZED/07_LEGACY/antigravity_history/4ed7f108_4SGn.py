import os
import argparse
from pathlib import Path
from organize_audio import organize_folder

# Re-use the smart organization logic, but point source to Audition Stage
# ANSI escape codes for colors and styles
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

AUDITION_STAGE = "/Users/m2ultra/Audio_Unitor/Audition_Stage"
VAULT_ROOT = "/Volumes/6TB/Audio_Universe"
STAGING_AREA = "/Users/m2ultra/Audio_Unitor/Staging_Area" # Defined based on context

# Re-use the smart organization logic, but point source to Audition Stage
# organize_audio already handles "VAULT -> ALIAS" logic if destination is ignored/vault is hardcoded.

def run_archiver():
    print(f"\n{BOLD}{CYAN}CORE > 🎬 AUDITION STAGE ARCHIVER{RESET}")
    print(f"CORE > Source: {AUDITION_STAGE}")
    print(f"CORE > Target: {VAULT_ROOT} (with Local Aliases)")
    
    source_path = Path(AUDITION_STAGE) # Convert to Path for iterdir()
    if not source_path.exists() or not any(source_path.iterdir()):
        print(f"{YELLOW}CORE > Stage is empty.{RESET}")
        return

    # run organize_audio logic
    # This will:
    # 1. Scan Audition Stage
    # 2. Key identify category
    # 3. Move to Vault
    # 4. Create Alias in Staging_Area (NOT back in Audition Stage, usually? 
    #    Actually, user might want the alias back in Audition Stage? 
    #    No, standard behavior is fine: move to Staging Area.
    #    If user wants it in Audition Stage, that's complex logic.
    #    Let's stick to: Audition -> Vault -> Staging Area Aliases.
    #    User works in Audition, when done, it gets filed away.
    
    organize_folder(AUDITION_STAGE, VAULT_ROOT, dry_run=False)
    
    print("\n✅ Stage Cleared. Files are safe in the Vault.")
    print("   Find your Aliases in Audio_Unitor/Staging_Area")

if __name__ == "__main__":
    archive_stage()
