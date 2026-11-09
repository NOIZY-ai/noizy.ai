#!/usr/bin/env python3
"""
📊 DISTRIBUTION STATUS - Check Master Chain Drive Status
"""

from pathlib import Path
from datetime import datetime
import shutil

def check_drive_status():
    """Check status of all drives in master chain."""
    
    print("\n" + "="*80)
    print("📊 GABRIEL MASTER CHAIN - DRIVE STATUS")
    print("="*80)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    drives = {
        '12TB 1': Path('/Volumes/12TB 1'),
        '12TB 2': Path('/Volumes/12TB'),
        'RED DRAGON': Path('/Volumes/RED DRAGON'),
        'GABRIEL_MOUNT': Path('/Users/rsp_ms/GABRIEL/GABRIEL_MOUNT'),
        'GABRIEL_LEARNING': Path('/Users/rsp_ms/GABRIEL/.gabriel_learning_x1000')
    }
    
    online_count = 0
    total_size_gb = 0
    
    for name, path in drives.items():
        print(f"\n{'='*80}")
        print(f"📂 {name}")
        print(f"{'='*80}")
        print(f"Path: {path}")
        
        if path.exists():
            online_count += 1
            print("Status: ✅ ONLINE")
            
            # Get disk usage
            try:
                if path.is_mount() or str(path).startswith('/Volumes'):
                    usage = shutil.disk_usage(path)
                    total_gb = usage.total / (1024**3)
                    used_gb = usage.used / (1024**3)
                    free_gb = usage.free / (1024**3)
                    percent = (used_gb / total_gb) * 100 if total_gb > 0 else 0
                    
                    print(f"\nCapacity:")
                    print(f"  Total: {total_gb:,.1f} GB")
                    print(f"  Used:  {used_gb:,.1f} GB ({percent:.1f}%)")
                    print(f"  Free:  {free_gb:,.1f} GB")
                    
                    total_size_gb += used_gb
            except Exception as e:
                print(f"  (Could not get disk usage: {e})")
            
            # Check for GABRIEL content
            gabriel_learning = path / 'GABRIEL_LEARNING'
            if gabriel_learning.exists():
                print(f"\n✅ GABRIEL_LEARNING directory found")
                
                # Count subdirectories
                try:
                    subdirs = [d for d in gabriel_learning.iterdir() if d.is_dir()]
                    files = [f for f in gabriel_learning.iterdir() if f.is_file()]
                    print(f"   Subdirectories: {len(subdirs)}")
                    print(f"   Files: {len(files)}")
                    
                    # List main content
                    if subdirs or files:
                        print(f"\n   Contents:")
                        for item in list(subdirs)[:5] + list(files)[:5]:
                            item_type = "📁" if item.is_dir() else "📄"
                            print(f"     {item_type} {item.name}")
                        if len(subdirs) + len(files) > 10:
                            print(f"     ... and {len(subdirs) + len(files) - 10} more")
                except Exception as e:
                    print(f"   (Could not list contents: {e})")
            else:
                print(f"\n⚠️  GABRIEL_LEARNING directory not found")
                print(f"   Run QUICK_DISTRIBUTE.py to create structure")
            
            # Check for autonomous_learning.py
            al_file = gabriel_learning / 'autonomous_learning.py' if gabriel_learning.exists() else None
            if al_file and al_file.exists():
                size_kb = al_file.stat().st_size / 1024
                print(f"\n✅ autonomous_learning.py found ({size_kb:.1f} KB)")
            
        else:
            print("Status: ❌ OFFLINE")
            print("  Drive not mounted or path does not exist")
    
    # Summary
    print(f"\n\n{'='*80}")
    print("📊 SUMMARY")
    print(f"{'='*80}\n")
    print(f"Drives Online:    {online_count}/{len(drives)}")
    print(f"Total Data:       {total_size_gb:,.1f} GB")
    print(f"Distribution:     {'✅ Active' if online_count >= 2 else '⚠️  Limited'}")
    
    if online_count == 0:
        print("\n❌ No drives online! Check connections.")
    elif online_count == 1:
        print("\n⚠️  Only 1 drive online. Distribution limited.")
        print("   Connect additional drives for full redundancy.")
    else:
        print(f"\n✅ {online_count} drives online - Good redundancy!")
    
    print("\n" + "="*80)
    print("🔗 NEXT STEPS:")
    print("="*80)
    print("\n1. Run: python3 QUICK_DISTRIBUTE.py")
    print("   → Distribute content across all online drives")
    print("\n2. Run: python3 autonomous_learning.py")
    print("   → Test the learning system")
    print("\n3. Run: python3 distribute_to_drives.py")
    print("   → Advanced distribution options")
    print()


if __name__ == "__main__":
    check_drive_status()
