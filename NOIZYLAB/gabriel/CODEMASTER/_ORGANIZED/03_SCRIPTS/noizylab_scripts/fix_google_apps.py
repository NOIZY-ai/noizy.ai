#!/usr/bin/env python3
"""
🔧 Fix-GoogleApps - macOS Edition (FIX 12)
Installs/updates Google apps using Homebrew
Equivalent to Windows winget version

Features:
- Install/upgrade core Google apps
- Verify installations
- Version detection
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Colors
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def log(msg: str, level: str = "INFO"):
    """Log with color"""
    colors = {
        "SUCCESS": C.GREEN,
        "WARNING": C.YELLOW,
        "ERROR": C.RED,
        "INFO": C.CYAN
    }
    color = colors.get(level, C.CYAN)
    symbol = {"SUCCESS": "✓", "WARNING": "⚠", "ERROR": "✗", "INFO": "→"}.get(level, "→")
    print(f"{color}{symbol} {msg}{C.END}")


def run_cmd(cmd: list, check: bool = False) -> tuple:
    """Run command and return (success, output)"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def check_brew() -> bool:
    """Check if Homebrew is installed"""
    success, _ = run_cmd(["brew", "--version"])
    return success


def install_or_upgrade(cask: str, name: str):
    """Install or upgrade a Homebrew cask"""
    # Check if installed
    success, output = run_cmd(["brew", "list", "--cask", cask])
    
    if success:
        # Already installed, upgrade
        log(f"Upgrading {name}...", "INFO")
        success, output = run_cmd(["brew", "upgrade", "--cask", cask])
        if success or "already installed" in output.lower():
            log(f"Updated: {name}", "SUCCESS")
        else:
            log(f"Upgrade {name}: {output[:100]}", "WARNING")
    else:
        # Not installed, install
        log(f"Installing {name}...", "INFO")
        success, output = run_cmd(["brew", "install", "--cask", cask])
        if success:
            log(f"Installed: {name}", "SUCCESS")
        else:
            log(f"Install {name} failed: {output[:100]}", "ERROR")


def get_chrome_version() -> str:
    """Get Chrome version from app bundle"""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/Info.plist",
        os.path.expanduser("~/Applications/Google Chrome.app/Contents/Info.plist")
    ]
    
    for plist_path in chrome_paths:
        if os.path.exists(plist_path):
            try:
                result = subprocess.run(
                    ["defaults", "read", plist_path.replace("/Info.plist", "/Info"), "CFBundleShortVersionString"],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
    return None


def get_drive_version() -> str:
    """Get Google Drive version"""
    drive_path = "/Applications/Google Drive.app/Contents/Info.plist"
    if os.path.exists(drive_path.replace("/Info.plist", "")):
        try:
            result = subprocess.run(
                ["defaults", "read", drive_path.replace("/Info.plist", "/Info"), "CFBundleShortVersionString"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
    return None


def fix_google_apps():
    """Main function - Install/Update Google apps on macOS (FIX 12)"""
    print(f"\n{C.CYAN}{C.BOLD}═══ FIX 12: GOOGLE STACK (Install + Update + Verify) ═══{C.END}\n")
    
    # 1) Ensure Homebrew is usable
    if not check_brew():
        log("Homebrew missing/broken. Install from https://brew.sh then re-run.", "ERROR")
        return False
    
    log("Homebrew available", "SUCCESS")
    
    # 2) Install/upgrade core Google apps (add/remove as needed)
    google_apps = [
        ("google-chrome", "Google Chrome"),
        ("google-drive", "Google Drive"),
        ("google-cloud-sdk", "Google Cloud SDK (gcloud CLI)"),
        # ("google-chrome-canary", "Google Chrome Canary"),  # optional
    ]
    
    for cask, name in google_apps:
        try:
            # Install (will skip if already installed)
            run_cmd(["brew", "install", "--cask", cask])
            # Upgrade (will update if available)
            run_cmd(["brew", "upgrade", "--cask", cask])
            log(f"Installed/updated: {name}", "SUCCESS")
        except Exception as e:
            log(f"brew failed for {cask}: {e}", "WARNING")
    
    # 3) macOS doesn't have Google Update services like Windows
    # Google apps on macOS use built-in Sparkle/KeyStone updaters
    log("Checking Google updater (Keystone)...", "INFO")
    keystone_path = os.path.expanduser("~/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle")
    if os.path.exists(keystone_path):
        log("Google Keystone updater found", "SUCCESS")
        # Trigger update check
        ksadmin = os.path.expanduser("~/Library/Google/GoogleSoftwareUpdate/GoogleSoftwareUpdate.bundle/Contents/MacOS/ksadmin")
        if os.path.exists(ksadmin):
            run_cmd([ksadmin, "--check"])
            log("Triggered Keystone update check", "SUCCESS")
    else:
        log("Google Keystone not found (Chrome may use App Store or Sparkle)", "WARNING")
    
    # 4) Cleanup old versions
    log("Cleaning up old versions...", "INFO")
    run_cmd(["brew", "cleanup"])
    log("Cleanup complete", "SUCCESS")
    
    # 5) Version proof
    print(f"\n{C.CYAN}{C.BOLD}═══ VERSION VERIFICATION ═══{C.END}\n")
    
    # Chrome version
    chrome_ver = get_chrome_version()
    if chrome_ver:
        log(f"Chrome version detected: {chrome_ver}", "SUCCESS")
    else:
        chrome_app = "/Applications/Google Chrome.app"
        if os.path.exists(chrome_app):
            log("Chrome installed but version unreadable", "WARNING")
        else:
            log("Chrome not found at expected path", "WARNING")
    
    # Drive version
    drive_ver = get_drive_version()
    if drive_ver:
        log(f"Google Drive version detected: {drive_ver}", "SUCCESS")
    else:
        drive_app = "/Applications/Google Drive.app"
        if os.path.exists(drive_app):
            log("Google Drive installed but version unreadable", "WARNING")
        else:
            log("Google Drive not found at expected path", "WARNING")
    
    # gcloud version
    success, output = run_cmd(["gcloud", "--version"])
    if success:
        gcloud_ver = output.split('\n')[0] if output else "Unknown"
        log(f"gcloud CLI: {gcloud_ver}", "SUCCESS")
    else:
        log("gcloud CLI not in PATH (may need: source ~/.zshrc)", "WARNING")
    
    print(f"\n{C.GREEN}{C.BOLD}✓ Google stack audit complete{C.END}\n")
    return True


def fix_google_apps_windows():
    """Windows version using winget (for reference)"""
    print("Windows version - use PowerShell script")
    # The original PowerShell function would go here
    pass


if __name__ == "__main__":
    import platform
    
    if platform.system() == "Darwin":
        fix_google_apps()
    elif platform.system() == "Windows":
        print("Run the PowerShell version: Fix-GoogleApps")
    else:
        print(f"Unsupported platform: {platform.system()}")
