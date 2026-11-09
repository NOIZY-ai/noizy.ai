import os
import sys
import argparse
import subprocess
from pathlib import Path

# ANSI Colors for that Cyberpunk feel
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'

VAULT_ROOT = "/Volumes/6TB/Audio_Universe"
INBOX = "/Users/m2ultra/Downloads/Audio_Inbox"
AUDITION = "/Users/m2ultra/Audio_Unitor/Audition_Stage"
STAGING = "/Users/m2ultra/Audio_Unitor/Staging_Area"

def print_banner():
    banner = f"""
{CYAN}{BOLD}
    ╔════════════════════════════════════════╗
    ║       A U D I O   U N I T O R          ║
    ║      MISSION CONTROL INTERFACE         ║
    ╚════════════════════════════════════════╝
{RESET}"""
    print(banner)

def check_status():
    print(f"{BOLD}SYSTEM STATUS:{RESET}")
    
    # Check Vault
    if Path(VAULT_ROOT).exists():
        print(f"[{GREEN}ONLINE{RESET}]  Vault (6TB) Connected")
    else:
        print(f"[{RED}OFFLINE{RESET}] Vault Disconnected! Check Cable.")

    # Check Hyper-Drive
    # Simple check for process name
    try:
        # pgrep -f hyper_drive_watcher.py
        p = subprocess.run(["pgrep", "-f", "hyper_drive_watcher.py"], capture_output=True)
        if p.returncode == 0:
             print(f"[{GREEN}ACTIVE{RESET}]  Hyper-Drive Engine")
        else:
             print(f"[{YELLOW}IDLE{RESET}]    Hyper-Drive Engine")
    except:
        pass

    # Check Staging Stats
    files = list(Path(STAGING).rglob('*'))
    file_count = len([f for f in files if f.is_file()]) # These are mostly symlinks
    print(f"[{CYAN}INFO{RESET}]    Library Index: {file_count} items")
    
    # Check Audition Stage
    audition_files = list(Path(AUDITION).iterdir())
    if len(audition_files) > 0:
        print(f"[{YELLOW}ALERT{RESET}]   {len(audition_files)} items on Audition Stage (NVMe)")
    else:
        print(f"[{GREEN}CLEAN{RESET}]   Audition Stage Empty")

    print("-" * 40)

def main_menu():
    print_banner()
    check_status()
    
    print(f"{BOLD}COMMANDS:{RESET}")
    print("0. [Oracle] Global Search (All Volumes) 👁️")
    print("1. [Cloud]  Sync Vault to Google Drive (MC96UNIVERSE)")

    print("2. [Tool]   Add to VI Database")
    print("3. [Stage]  Flush Audition Stage -> Vault")
    print("4. [Fetch]  Materialize Alias -> Audition Stage")
    print("5. [Find]   Search Alias Library")
    print("6. [VI]     Search VI Database")
    print("7. [Rename] Batch Rename (Audition Stage)")
    print("8. [Scan]   Auto-Discover Plugins (System)")
    print("9. [Index]  Re-Build Global Oracle Index")
    print("10.[Deep]   Analyze Sonic Fingerprints (Dedup)")
    print("11.[Auto]   Run Daily Maintenance Protocol")
    print("12.[Visual] Generate Universe Status Report")
    print("13.[Drive]  Restart Hyper-Drive Engine")
    print("Q. Quit")
    
    choice = input(f"\n{CYAN}Awaiting Command > {RESET}").lower()




    
    if choice == '0':
        query = input(f"🔮 Oracle Search > ").strip()
        subprocess.run(["python3", "Audio_Unitor/Scripts/search_oracle.py", query])
    elif choice == '1':
        subprocess.run(["python3", "Audio_Unitor/Scripts/deploy_to_universe.py"])

    elif choice == '2':
        subprocess.run(["python3", "Audio_Unitor/Scripts/vi_db_tool.py"])
    elif choice == '3':
        subprocess.run(["python3", "Audio_Unitor/Scripts/archive_audition.py"])
    elif choice == '4':
        print(f"{YELLOW}Drag and Drop the Alias file here and press Enter:{RESET}")
        path = input("> ").strip().replace("\\ ", " ").strip("'").strip('"')
        if path:
            subprocess.run(["python3", "Audio_Unitor/Scripts/fetch_to_stage.py", path])
    elif choice == '5':
        query = input(f"Search Query > ").strip()
        subprocess.run(["python3", "Audio_Unitor/Scripts/search_aliases.py", query])
    elif choice == '6':
        query = input(f"VI Search > ").strip()
        subprocess.run(["python3", "Audio_Unitor/Scripts/search_vi_db.py", query])
    elif choice == '7':
        print(f"{YELLOW}Batch Rename in Audition Stage{RESET}")
        pattern = input("Regex Pattern: ").strip()
        replacement = input("Replacement: ").strip()
        confirm = input("Apply for real? (y/n): ").strip().lower()
        if confirm == 'y':
            subprocess.run(["python3", "Audio_Unitor/Scripts/batch_rename.py", pattern, replacement, "--live"])
        else:
            subprocess.run(["python3", "Audio_Unitor/Scripts/batch_rename.py", pattern, replacement])
    elif choice == '8':
        subprocess.run(["python3", "Audio_Unitor/Scripts/plugin_scanner.py"])
    elif choice == '9':
        subprocess.run(["python3", "Audio_Unitor/Scripts/global_indexer.py"])
    elif choice == '10':
        subprocess.run(["python3", "Audio_Unitor/Scripts/sonic_analyzer.py"])
    elif choice == '11':
        subprocess.run(["python3", "Audio_Unitor/Scripts/daily_maintenance.py"])
    elif choice == '12':
        subprocess.run(["python3", "Audio_Unitor/Scripts/universe_report.py"])
        print(f"{GREEN}Opening Report...{RESET}")
        subprocess.run(["open", "universe_status.html"])
    elif choice == '13':
        print("Restarting Engine...")
        subprocess.run(["pkill", "-f", "hyper_drive_watcher.py"])

        subprocess.Popen(["python3", "Audio_Unitor/Scripts/hyper_drive_watcher.py"])
        print(f"{GREEN}Engine Restarted.{RESET}")
    elif choice == 'q':

        sys.exit()
    else:
        print("Invalid Command.")

if __name__ == "__main__":
    while True:
        try:
            main_menu()
            input(f"\n{CYAN}Press Enter to continue...{RESET}")
            print("\n" * 2)
        except KeyboardInterrupt:
            print("\nTerminated.")
            sys.exit()
