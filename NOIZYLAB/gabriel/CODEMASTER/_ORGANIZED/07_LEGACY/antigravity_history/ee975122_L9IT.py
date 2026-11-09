#!/usr/bin/env python3
"""
turbo_workspace.py
Global Workspace Manager & Template Factory
"""
import os
import json
import subprocess
import sys
import shutil
from pathlib import Path

# Configuration
WORKSPACE_DIR = Path.home() / "Workspaces"
TEMPLATE_DIR = Path.home() / "NOIZYLAB" / "templates"
VSCODE_CMD = "code"

def diff_workspaces():
    """Find all workspace files."""
    WORKSPACE_DIR.mkdir(exist_ok=True)
    found = []
    locations = [
        Path.home(),
        Path.home() / "NOIZYLAB",
        Path.home() / "Documents/PROJECTS",
        Path.home() / "Documents/GABRIEL"
    ]
    for loc in locations:
        if loc.exists():
            found.extend(loc.glob("**/*.code-workspace"))
    return sorted(list(set(found)))

def get_templates():
    """List available templates."""
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    return sorted(list(TEMPLATE_DIR.glob("*.json")))

def create_workspace(template_path):
    """Create a new project from a template."""
    print(f"\n✨ Creating new project from {template_path.stem}...")
    
    try:
        with open(template_path, 'r') as f:
            config = json.load(f)
            
        name = input("Project Name: ").strip()
        if not name: return
        
        # Determine location
        parent = Path.home() / "Documents" / "PROJECTS"
        project_dir = parent / name
        
        if project_dir.exists():
            print("❌ Project directory already exists!")
            return
            
        project_dir.mkdir(parents=True)
        
        # Create structure
        for folder in config.get("folders", []):
            (project_dir / folder).mkdir(parents=True, exist_ok=True)
            
        for file, content in config.get("files", {}).items():
            with open(project_dir / file, 'w') as f:
                f.write(content)
                
        # Create .code-workspace file
        ws_content = {
            "folders": [{"path": "."}],
            "settings": config.get("settings", {})
        }
        ws_file = project_dir / f"{name}.code-workspace"
        with open(ws_file, 'w') as f:
            json.dump(ws_content, f, indent=4)
            
        print(f"✅ Project Created: {project_dir}")
        subprocess.run([VSCODE_CMD, str(ws_file)])
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")

def main():
    print(f"\n🚀 **TURBO WORKSPACE MANAGER** 🚀")
    print("="*40)
    
    # 1. List Templates
    templates = get_templates()
    if templates:
        print("Templates:")
        for i, t in enumerate(templates):
            print(f"  {i+1}. [NEW] {t.stem}")
    
    # 2. List Existing Workspaces
    workspaces = diff_workspaces()
    if workspaces:
        print("\nExisting Workspaces:")
        start_idx = len(templates)
        for i, ws in enumerate(workspaces):
            print(f"  {start_idx + i + 1}. {ws.name} \t({ws.parent.name})")
            
    print("="*40)
    
    choice = input(f"\nSelect option (1-{len(templates) + len(workspaces)}) or 'q': ")
    if choice.lower() == 'q': return
    
    try:
        idx = int(choice) - 1
        # Template Choice
        if 0 <= idx < len(templates):
            create_workspace(templates[idx])
        # Workspace Choice
        elif len(templates) <= idx < len(templates) + len(workspaces):
            ws = workspaces[idx - len(templates)]
            print(f"\n🚀 Launching {ws.name}...")
            subprocess.run([VSCODE_CMD, str(ws)])
        else:
            print("❌ Invalid selection")
            
    except ValueError:
        print("❌ Invalid input")

if __name__ == "__main__":
    main()
