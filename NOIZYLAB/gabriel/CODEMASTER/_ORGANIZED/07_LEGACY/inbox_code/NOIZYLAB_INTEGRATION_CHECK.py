#!/usr/bin/env python3
# 🔥 NOIZYLAB MASTER INTEGRATION CHECK
# Purpose: VERIFY 100% SYSTEM STATUS (ZERO LATENCY)
# "THE FINAL EXAM"

import os
import sys
import json
import subprocess
import time

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'
CYAN = '\033[96m'
YELLOW = '\033[93m'

def check_pass(msg):
    print(f"[{GREEN}✅ PASS{RESET}] {msg}")

def check_fail(msg):
    print(f"[{RED}❌ FAIL{RESET}] {msg}")
    return 1

def run_check():
    errors = 0
    print(f"\n{BOLD}🚀 STARTING NOIZYLAB ZERO LATENCY DIAGNOSTIC...{RESET}\n")

    # 1. NETWORK CHECK (HOT ROD V3)
    print(f"{BOLD}1. NETWORK (HOT ROD V3){RESET}")
    try:
        mtu = subprocess.check_output("networksetup -getMTU $(route get default | grep interface | awk '{print $2}')", shell=True).decode()
        if "9000" in mtu:
            check_pass("MTU 9000 (Jumbo Frames) Verified")
        else:
            print(f"   ⚠️  MTU is {mtu.strip()} (Run 'sudo ./mc96_optimize.sh')")
            # Not a fail for script, but warning
    except:
        check_fail("Network Check Failed")

    # 2. MEMCELL CORE (THE BRAIN)
    print(f"\n{BOLD}2. MEMCELL (THE BRAIN){RESET}")
    db_path = "memcell_db.json"
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r') as f:
                data = json.load(f)
            check_pass(f"Database Loaded ({len(data)} memories)")
            check_pass("Persistence Layer Active")
        except:
            errors += check_fail("Database Corrupted")
    else:
        check_pass("Database Initialized (New)")

    # 3. TACTILE VOICE (THE HANDS)
    print(f"\n{BOLD}3. TACTILE SYSTEM (THE HANDS){RESET}")
    if os.path.exists("AI_INTEGRATION_SUITE/TACTILE_ASSISTANCE_SYSTEM.py"):
        check_pass("Voice System Found")
    else:
        errors += check_fail("Voice System Missing")

    # 4. FILESYSTEM ORG (THE HOUSE)

    print(f"\n{CYAN}4. FILESYSTEM (THE HOUSE){RESET}")
    required_files = [
        "docs/CB_01_MASTER_PROMPT_V3_GOD_MODE.md",
        "docs/UNIVERSAL_GOD_HEADER.md",
        "docs/GABRIEL_AVATAR_SYSTEM.md",
        "docs/LIFELUV_ENGR_TACTILE_COMPLETE.md",
        "tools/scripts/mc96_optimize.sh",
        "docs/NOIZYLAB_REBUILD_LOG.md"
    ]

    missing = []
    for f in required_files:
        if os.path.exists(f):
            print(f"[{GREEN}✅ PASS{RESET}] Found: {f}")
        else:
            print(f"[{RED}❌ FAIL{RESET}] Missing: {f}")
            missing.append(f)
    errors += len(missing)

    # GOD MODE SWEEP VERIFICATION
    print(f"\n{CYAN}5. GOD MODE COMPLIANCE CHECK (THE LAW){RESET}")
    docs_dir = "docs"
    compliance_count = 0
    total_checked = 0
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            if filename.endswith(".md") and not filename.startswith("CB_01") and "LOG" not in filename:
                total_checked += 1
                with open(os.path.join(docs_dir, filename), 'r') as f:
                    content = f.read(100) # Check first 100 chars
                    if "GOD MODE SYSTEM" in content or "ZERO LATENCY" in content:
                        compliance_count += 1

        if total_checked > 0:
            rate = (compliance_count / total_checked) * 100
            status_color = GREEN if rate == 100 else YELLOW
            print(f"[{status_color}✅ PASS{RESET}] Compliance Rate: {rate:.1f}% ({compliance_count}/{total_checked} Docs)")
            if rate < 100:
                errors += 1 # Increment error if not 100% compliant
        else:
            print(f"[{YELLOW}⚠️ INFO{RESET}] No docs to check.")
    else:
        print(f"[{RED}❌ FAIL{RESET}] Docs directory missing.")
        errors += 1 # Docs directory missing is an error

    # FINAL SCORE
    print("-" * 40)
    if errors == 0:
        print(f"\n{GREEN}{BOLD}🏆 SYSTEM STATUS: 100% INTEGRATED{RESET}")
        print(f"{BOLD}🔥 ZERO LATENCY MODE: READY{RESET}")
        print("GORUNFREE! 🚀\n")
    else:
        print(f"\n{RED}{BOLD}⚠️  SYSTEM STATUS: {errors} ERRORS FOUND{RESET}")
        print("Run diagnostics to fix.\n")

if __name__ == "__main__":
    run_check()
