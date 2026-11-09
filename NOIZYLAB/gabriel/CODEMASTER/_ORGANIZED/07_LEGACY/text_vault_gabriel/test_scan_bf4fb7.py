#!/usr/bin/env python3
"""
Quick test of the file organization system
"""

import sys
from pathlib import Path

# Test if file_organizer is working
try:
    from file_organizer import quick_scan, FileOrganizer
    print("✅ file_organizer module loaded successfully")
    
    # Test scan
    test_path = "/Volumes/RED DRAGON/_To Sort"
    
    if Path(test_path).exists():
        print(f"\n🔍 Scanning: {test_path}")
        print("="*70)
        
        result = quick_scan(test_path)
        
        print(f"\n📊 RESULTS:")
        print(f"   Audio Files: {result['audio_files']}")
        print(f"   Drum Kits: {result['kits']}")
        print(f"   Instruments: {result['instruments']}")
        print(f"   Total Size: {FileOrganizer.human_readable_size(result['total_size'])}")
        
        if result['formats']:
            print(f"\n   Formats:")
            for fmt, count in sorted(result['formats'].items(), key=lambda x: x[1], reverse=True):
                print(f"      {fmt}: {count} files")
        
        if result['bpm_distribution']:
            print(f"\n   BPM Distribution:")
            bpm_list = sorted(result['bpm_distribution'].items(), key=lambda x: int(x[0]))
            for bpm, count in bpm_list:
                print(f"      {bpm} BPM: {count} files")
        
        print("\n" + "="*70)
        print("✅ SCAN COMPLETE!")
        
    else:
        print(f"⚠️  Path not found: {test_path}")
        print("\nAvailable volumes:")
        volumes = Path("/Volumes").glob("*")
        for vol in volumes:
            if vol.is_dir() and not vol.name.startswith('.'):
                print(f"   - {vol}")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nMake sure you're running from /Users/rsp_ms/GABRIEL")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
