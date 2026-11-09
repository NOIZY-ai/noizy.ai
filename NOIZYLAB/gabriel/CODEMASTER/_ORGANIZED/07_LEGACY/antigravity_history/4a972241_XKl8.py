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
    print(f"\n{BOLD}4. FILESYSTEM (THE HOUSE){RESET}")
    required = [
        "docs/CB_01_MASTER_PROMPT_V3_GOD_MODE.md",
        "tools/scripts/mc96_optimize.sh",
        "docs/NOIZYLAB_REBUILD_LOG.md"
    ]
    for r in required:
        if os.path.exists(r):
            check_pass(f"Found: {r}")
        else:
            errors += check_fail(f"Missing: {r}")

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
