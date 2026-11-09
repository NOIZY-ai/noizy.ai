import os
import sys
import importlib.util
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path("/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Scripts")

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def validate_script(script_path):
    module_name = script_path.stem
    try:
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True, "Loaded successfully"
        else:
            return False, "Could not create spec"
    except Exception as e:
        return False, str(e)

def run_suite_validation():
    print(f"{BOLD}{CYAN}TURBO SUITE VALIDATOR > Scanning {SCRIPTS_DIR}...{RESET}\n")
    
    if not SCRIPTS_DIR.exists():
        print(f"{RED}Error: Scripts directory not found.{RESET}")
        return

    scripts = list(SCRIPTS_DIR.glob("turbo_*.py"))
    scripts.sort()
    
    success_count = 0
    fail_count = 0
    
    for script in scripts:
        if script.name == "turbo_suite_validator.py": continue
        
        print(f"Checking {script.name}...", end=" ")
        success, msg = validate_script(script)
        
        if success:
            print(f"{GREEN}OK{RESET}")
            success_count += 1
        else:
            print(f"{RED}FAIL{RESET}")
            print(f"   Error: {msg}")
            fail_count += 1
            
    print(f"\n{BOLD}RESULTS:{RESET}")
    print(f"   TOTAL:   {len(scripts)}")
    print(f"   {GREEN}SUCCESS: {success_count}{RESET}")
    print(f"   {RED}FAIL:    {fail_count}{RESET}")
    
    if fail_count == 0:
        print(f"\n{BOLD}{GREEN}ALL SYSTEMS GO. TURBO SUITE IS LOADED.{RESET}")
    else:
        print(f"\n{BOLD}{RED}SYSTEM INTEGRITY COMPROMISED.{RESET}")

if __name__ == "__main__":
    # Add scripts dir to path to allow internal imports
    sys.path.append(str(SCRIPTS_DIR))
    run_suite_validation()
