#!/usr/bin/env python3
"""Quick MissionControl96 scanner"""
import os
from pathlib import Path

mc96 = Path("/Users/rsp_ms/Desktop/MissionControl96")

print("🚀 MISSIONCONTROL96 QUICK SCAN")
print("=" * 80)

try:
    if not mc96.exists():
        print("❌ Not found")
    else:
        print(f"✅ Found: {mc96}\n")
        
        for root, dirs, files in os.walk(mc96):
            root_path = Path(root)
            level = len(root_path.relative_to(mc96).parts)
            indent = "  " * level
            
            print(f"{indent}📁 {root_path.name}/")
            
            for f in files:
                file_path = root_path / f
                size = file_path.stat().st_size
                print(f"{indent}  📄 {f} ({size:,} bytes)")
            
            if not files and not dirs:
                print(f"{indent}  (empty)")

except Exception as e:
    print(f"⚠️ Error: {e}")

print("=" * 80)
