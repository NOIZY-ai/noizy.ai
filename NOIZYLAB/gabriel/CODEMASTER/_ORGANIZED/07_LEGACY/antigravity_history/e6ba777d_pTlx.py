#!/usr/bin/env python3
import os
import json
import subprocess
import sys
from pathlib import Path

# Configuration
WORKSPACE_DIR = Path.home() / "Workspaces"
VSCODE_CMD = "code"

def diff_workspaces():
    """Find all workspace files and ensure they are tracked."""
    # Create dir if not exists
    WORKSPACE_DIR.mkdir(exist_ok=True)
    
    found = []
    # Scan common locations
    locations = [
        Path.home(),
        Path.home() / "NOIZYLAB",
        Path.home() / "Documents/PROJECTS",
        Path.home() / "Documents/GABRIEL"
    ]
    
    print("\n🔍 Scanning for workspaces...")
    for loc in locations:
        if loc.exists():
            found.extend(loc.glob("**/*.code-workspace"))
            
    return sorted(list(set(found)))

def list_and_choose():
    workspaces = diff_workspaces()
    
    if not workspaces:
        print("❌ No workspaces found!")
        return
        
    print(f"\n🚀 **MC96 WORKSPACE LAUNCHER** 🚀")
    print("="*40)
    
    for i, ws in enumerate(workspaces):
        print(f"{i+1}. {ws.name} \t({ws.parent})")
        
    print("="*40)
    
    try:
        choice = input(f"\nSelect workspace (1-{len(workspaces)}) or 'q' to quit: ")
        if choice.lower() == 'q':
            return
            
        idx = int(choice) - 1
        if 0 <= idx < len(workspaces):
            ws_path = workspaces[idx]
            print(f"\n🚀 Launching {ws_path.name}...")
            subprocess.run([VSCODE_CMD, str(ws_path)])
        else:
            print("❌ Invalid selection")
            
    except ValueError:
        print("❌ Invalid input")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        diff_workspaces()
    else:
        list_and_choose()
