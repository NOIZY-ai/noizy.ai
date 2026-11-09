#!/usr/bin/env python3
"""
GABRIEL File Suite - Complete Workflow Example
Demonstrates full pipeline: Scan → Classify → Organize → Report
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from deepscan import DeepScan
from sensemaker import SenseMaker
from hivesort import HiveSort, OrganizeMode
import json


def main():
    # Configuration
    VOLUME_PATH = "/Volumes/GABRIEL"
    DB_PATH = "gabriel_demo.db"
    OUTPUT_PATH = "/Volumes/GABRIEL/Organized_Demo"
    
    print("=" * 60)
    print("GABRIEL File Suite - Complete Workflow Demo")
    print("=" * 60)
    
    # Step 1: Deep Scan
    print("\n📡 Step 1/5: Deep Scan")
    print("-" * 60)
    scanner = DeepScan(DB_PATH, max_workers=8)
    
    def progress(current, total):
        pct = 100 * current // total
        print(f"Progress: {current}/{total} ({pct}%)", end='\r')
    
    scan_stats = scanner.scan_volume(VOLUME_PATH, progress_callback=progress)
    print(f"\n✅ Scanned {scan_stats['total_files']} files")
    print(f"   Total size: {scan_stats['total_size_gb']} GB")
    print(f"   Errors: {scan_stats['errors']}")
    
    # Step 2: Find Duplicates
    print("\n🔍 Step 2/5: Duplicate Detection")
    print("-" * 60)
    duplicates = scanner.find_duplicates()
    
    if duplicates:
        total_wasted = sum(d['wasted_space'] for d in duplicates)
        wasted_gb = round(total_wasted / (1024**3), 2)
        print(f"✅ Found {len(duplicates)} duplicate groups")
        print(f"   Wasted space: {wasted_gb} GB")
        print(f"\n   Top 5 duplicate groups:")
        for i, dup in enumerate(duplicates[:5], 1):
            wasted_mb = round(dup['wasted_space'] / (1024**2), 2)
            print(f"   {i}. {dup['count']} copies - {wasted_mb} MB wasted")
    else:
        print("✅ No duplicates found!")
    
    # Step 3: AI Classification
    print("\n🧠 Step 3/5: AI Classification")
    print("-" * 60)
    classifier = SenseMaker(DB_PATH)
    
    # Classify first 100 files (change to higher number for full classification)
    results = classifier.classify_batch(limit=100, use_ai=False)
    print(f"✅ Classified {len(results)} files")
    
    # Show category breakdown
    cat_stats = classifier.get_category_stats()
    print(f"\n   Categories:")
    for cat in cat_stats['categories']:
        print(f"   - {cat['category']}: {cat['count']} files ({cat['size_gb']} GB)")
    
    # Step 4: Smart Organization
    print("\n📁 Step 4/5: Smart Organization")
    print("-" * 60)
    organizer = HiveSort(DB_PATH)
    
    # Dry-run first (safe)
    print("   Running dry-run (no changes)...")
    org_stats = organizer.organize_by_category(
        OUTPUT_PATH,
        mode=OrganizeMode.SYMLINK,
        dry_run=True
    )
    
    print(f"✅ Organization plan:")
    print(f"   Total files: {org_stats['total']}")
    print(f"   Would organize: {org_stats['organized']}")
    print(f"   Mode: {org_stats['mode']}")
    print(f"\n   Categories:")
    for cat, stats in org_stats['categories'].items():
        print(f"   - {cat}: {stats['count']} files ({stats['size_gb']} GB)")
    
    # Step 5: Generate Reports
    print("\n📊 Step 5/5: Generate Reports")
    print("-" * 60)
    
    # Export category map
    category_map_file = "category_map.json"
    classifier.export_category_map(category_map_file)
    print(f"✅ Category map: {category_map_file}")
    
    # Create organization manifest
    manifest_file = "organization_manifest.json"
    organizer.create_manifest(manifest_file)
    print(f"✅ Manifest: {manifest_file}")
    
    # Database statistics
    db_stats = scanner.get_stats()
    print(f"\n📈 Final Statistics:")
    print(f"   Total files: {db_stats['total_files']:,}")
    print(f"   Total size: {db_stats['total_size_gb']} GB")
    print(f"   Database: {DB_PATH}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Workflow Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review category_map.json")
    print("2. Review organization_manifest.json")
    print("3. If satisfied, organize for real:")
    print(f"   ./gabriel.py organize {DB_PATH} {OUTPUT_PATH} --mode symlink")
    print("\n4. Start dashboard to explore:")
    print("   python dashboard/api.py")
    print("   streamlit run dashboard/streamlit_app.py")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
