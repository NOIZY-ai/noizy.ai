#!/usr/bin/env python3
# 🔥 MC96 AUTO-HEAL - SELF-DOCTOR
# Version 2.0 (Rebuilt by CB_01)
#
# Purpose: Continuous network health monitoring & diagnostics
# Specs: 0-100 Score, 5 Checks, Auto-Fix Recommendations

import subprocess
import time
import argparse
import sys
import platform

# Spec Constants
TARGET_MTU = 9000
TARGET_BUFFER = 16777216  # 16 MB
GATEWAY_IP = "10.0.0.1"  # Default gateway assumption

class ANSI:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    except:
        return ""

def get_active_interface():
    # macOS specific: get default interface
    try:
        return run_cmd("route get default | grep interface | awk '{print $2}'")
    except:
        print(f"{ANSI.RED}No active interface found.{ANSI.RESET}")
        sys.exit(1)

def check_mtu(interface):
    try:
        out = run_cmd(f"networksetup -getMTU {interface}")
        mtu = int(out.split()[-1])
        if mtu >= TARGET_MTU:
            return 20, f"MTU {mtu} (Jumbo Frames Active)"
        else:
            return 0, f"MTU {mtu} (Target: {TARGET_MTU})"
    except:
        return 0, "MTU Check Failed"

def check_buffers():
    try:
        out = run_cmd("sysctl kern.ipc.maxsockbuf")
        val = int(out.split()[-1])
        if val >= TARGET_BUFFER:
            return 20, f"Buffers {val/1024/1024:.0f}MB (Optimized)"
        else:
            return 5, f"Buffers {val} (Standard)"
    except:
        return 0, "Buffer Check Failed"

def check_gateway():
    try:
        out = run_cmd(f"ping -c 1 -W 500 {GATEWAY_IP}")
        if "1 packets received" in out:
            return 20, "Gateway Reachable"
        else:
            return 0, "Gateway Unreachable"
    except:
        return 0, "Gateway Check Failed"

def check_errors(interface):
    try:
        # macOS netstat for I/O errors (simplified)
        out = run_cmd(f"netstat -I {interface} | grep {interface} | awk '{{print $6}}'") # Input errors
        errs = int(out) if out.isdigit() else 0
        if errs == 0:
            return 20, "Zero Packet Errors"
        elif errs < 100:
            return 10, f"{errs} Errors (Minor)"
        else:
            return 0, f"{errs} Errors (CRITICAL)"
    except:
        return 0, "Error Check Failed"

def check_status(interface):
    try:
        out = run_cmd(f"ifconfig {interface}")
        if "status: active" in out:
             return 20, "Interface Active"
        else:
             return 0, "Interface Inactive"
    except:
        return 0, "Status Check Failed"

def run_diagnostics():
    iface = get_active_interface()

    print(f"\n{ANSI.BOLD}🔥 MC96 AUTO-HEAL DIAGNOSTICS{ANSI.RESET}")
    print(f"Interface: {iface}\n")

    score = 0
    checks = []

    # 1. Status
    s_score, s_msg = check_status(iface)
    score += s_score
    print(f"[{'✅' if s_score==20 else '❌'}] Status: {s_msg}")

    # 2. MTU
    m_score, m_msg = check_mtu(iface)
    score += m_score
    print(f"[{'✅' if m_score==20 else '⚠️'}] MTU:    {m_msg}")

    # 3. Buffers
    b_score, b_msg = check_buffers()
    score += b_score
    print(f"[{'✅' if b_score==20 else '⚠️'}] TCP:    {b_msg}")

    # 4. Gateway
    g_score, g_msg = check_gateway()
    score += g_score
    print(f"[{'✅' if g_score==20 else '❌'}] Ping:   {g_msg}")

    # 5. Errors
    e_score, e_msg = check_errors(iface)
    score += e_score
    print(f"[{'✅' if e_score==20 else '❌'}] Health: {e_msg}")

    print("-" * 30)

    # Score Color
    color = ANSI.GREEN
    if score < 80: color = ANSI.YELLOW
    if score < 50: color = ANSI.RED

    print(f"{ANSI.BOLD}🏆 FINAL HEALTH SCORE: {color}{score}/100{ANSI.RESET}\n")

    if score < 100:
        print(f"{ANSI.YELLOW}⚠️ RECOMMENDATION: Run 'sudo ./mc96_optimize.sh' to fix issues.{ANSI.RESET}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MC96 Auto-Healing System")
    parser.add_argument("--service", action="store_true", help="Run continuously")
    args = parser.parse_args()

    if args.service:
        print("Starting continuous monitoring... (Press Ctrl+C to stop)")
        while True:
            run_diagnostics()
            time.sleep(10)
    else:
        run_diagnostics()
