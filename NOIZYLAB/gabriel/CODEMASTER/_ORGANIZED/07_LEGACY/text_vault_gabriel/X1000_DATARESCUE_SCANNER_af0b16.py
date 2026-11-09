#!/usr/bin/env python3
"""
🚀 X1000 DATARESCUE INTEGRATION 🚀
===================================
Access files outside workspace boundary
Integrate with DataRescue program
"""

import os
import sys
from pathlib import Path
import subprocess

class X1000DataRescueAccess:
    """Access external paths like MissionControl96"""
    
    def __init__(self):
        self.gabriel = Path("/Users/rsp_ms/GABRIEL")
        self.desktop = Path("/Users/rsp_ms/Desktop")
        
    def scan_missioncontrol96(self):
        """Scan MissionControl96 folder"""
        mc96 = self.desktop / "MissionControl96"
        
        print("🚀 X1000 DATARESCUE SCANNER")
        print("=" * 80)
        print(f"📁 Target: {mc96}")
        
        if not mc96.exists():
            print("❌ MissionControl96 not found")
            return []
        
        print("✅ MissionControl96 found!")
        
        # Scan contents
        items = []
        try:
            for item in mc96.rglob("*"):
                if item.is_file():
                    size = item.stat().st_size
                    items.append({
                        "path": str(item),
                        "name": item.name,
                        "size": size,
                        "size_mb": size / 1024 / 1024,
                        "type": item.suffix
                    })
        except Exception as e:
            print(f"⚠️  Scan error: {e}")
        
        print(f"\n📊 Found {len(items)} files:")
        print("-" * 80)
        
        for item in sorted(items, key=lambda x: x['size'], reverse=True):
            print(f"  {item['size_mb']:8.2f} MB | {item['name']}")
        
        return items
    
    def list_directory_tree(self, path: Path, prefix="", max_depth=5, current_depth=0):
        """List directory tree structure"""
        if current_depth >= max_depth:
            return
        
        try:
            entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{entry.name}")
                
                if entry.is_dir():
                    extension_prefix = "    " if is_last else "│   "
                    self.list_directory_tree(entry, prefix + extension_prefix, max_depth, current_depth + 1)
        except PermissionError:
            print(f"{prefix}[Permission Denied]")
        except Exception as e:
            print(f"{prefix}[Error: {e}]")
    
    def scan_with_tree(self):
        """Scan MissionControl96 with tree view"""
        mc96 = self.desktop / "MissionControl96"
        
        print("\n🌳 DIRECTORY TREE:")
        print("=" * 80)
        print(f"📁 {mc96}")
        
        if mc96.exists():
            self.list_directory_tree(mc96)
        else:
            print("❌ Not found")
        
        print("=" * 80)

def main():
    scanner = X1000DataRescueAccess()
    
    print("\n🚀 X1000 DATARESCUE MISSIONCONTROL96 SCANNER")
    print("=" * 80)
    
    # Scan files
    items = scanner.scan_missioncontrol96()
    
    # Show tree
    scanner.scan_with_tree()
    
    print("\n✨ SCAN COMPLETE")
    
    return items

if __name__ == '__main__':
    main()
