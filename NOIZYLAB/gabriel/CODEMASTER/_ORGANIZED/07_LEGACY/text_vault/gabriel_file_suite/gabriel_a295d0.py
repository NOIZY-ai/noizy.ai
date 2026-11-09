#!/usr/bin/env python3
"""
GABRIEL File Suite - Main CLI Interface
Command-line interface for DeepScan, SenseMaker, and HiveSort
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from deepscan import DeepScan
from sensemaker import SenseMaker
from hivesort import HiveSort, OrganizeMode


def cmd_scan(args):
    """Run DeepScan on volume"""
    scanner = DeepScan(args.database, max_workers=args.workers)
    
    def progress(current, total):
        if args.verbose:
            print(f"Progress: {current}/{total} ({100*current//total}%)", end='\r')
    
    stats = scanner.scan_volume(args.volume, progress_callback=progress)
    
    print(f"\n✅ Scan Complete!")
    print(f"Files indexed: {stats['total_files']}")
    print(f"Total size: {stats['total_size_gb']} GB")
    print(f"Errors: {stats['errors']}")
    
    if args.find_duplicates:
        duplicates = scanner.find_duplicates()
        print(f"\n🔍 Found {len(duplicates)} duplicate groups")
        total_wasted = sum(d['wasted_space'] for d in duplicates)
        print(f"Wasted space: {round(total_wasted / (1024**3), 2)} GB")


def cmd_classify(args):
    """Run SenseMaker classification"""
    classifier = SenseMaker(args.database)
    
    print(f"🧠 Classifying files (AI: {args.use_ai})...")
    results = classifier.classify_batch(limit=args.batch, use_ai=args.use_ai)
    
    print(f"✅ Classified {len(results)} files")
    
    stats = classifier.get_category_stats()
    print(f"\n📊 Category Statistics:")
    for cat in stats['categories']:
        print(f"  {cat['category']}: {cat['count']} files ({cat['size_gb']} GB)")
    print(f"  Unclassified: {stats['unclassified']} files")
    
    if args.export:
        classifier.export_category_map(args.export)
        print(f"\n💾 Category map exported to {args.export}")


def cmd_organize(args):
    """Run HiveSort organization"""
    organizer = HiveSort(args.database)
    
    mode = OrganizeMode(args.mode)
    
    print(f"📁 Organizing files (mode: {mode.value}, dry_run: {args.dry_run})...")
    
    if args.by_extension:
        stats = organizer.organize_by_extension(args.output, mode=mode, dry_run=args.dry_run)
    else:
        stats = organizer.organize_by_category(
            args.output, 
            mode=mode, 
            preserve_structure=args.preserve_structure,
            dry_run=args.dry_run
        )
    
    print(f"\n✅ Organization Complete!")
    print(f"Total files: {stats['total']}")
    print(f"Organized: {stats['organized']}")
    print(f"Failed: {stats['failed']}")
    
    if args.manifest:
        organizer.create_manifest(args.manifest)
        print(f"\n📋 Manifest saved to {args.manifest}")


def cmd_duplicates(args):
    """Handle duplicate files"""
    organizer = HiveSort(args.database)
    
    stats = organizer.handle_duplicates(
        action=args.action,
        dry_run=args.dry_run
    )
    
    print(f"\n🔍 Duplicate Handling Results:")
    print(f"Duplicate groups: {stats['duplicate_groups']}")
    print(f"Files removed: {stats['files_removed']}")
    print(f"Space freed: {stats['space_freed_gb']} GB")


def cmd_stats(args):
    """Show database statistics"""
    scanner = DeepScan(args.database)
    stats = scanner.get_stats()
    
    print(f"\n📊 Database Statistics:")
    print(f"Total files: {stats['total_files']}")
    print(f"Total size: {stats['total_size_gb']} GB")
    
    print(f"\n📁 Top File Types:")
    for ext_stats in stats['top_extensions']:
        ext = ext_stats['ext'] or '(no extension)'
        print(f"  {ext}: {ext_stats['count']} files ({round(ext_stats['size'] / (1024**3), 2)} GB)")
    
    # Category stats if available
    classifier = SenseMaker(args.database)
    cat_stats = classifier.get_category_stats()
    
    if cat_stats['categories']:
        print(f"\n🏷️  Categories:")
        for cat in cat_stats['categories']:
            print(f"  {cat['category']}: {cat['count']} files ({cat['size_gb']} GB, conf: {cat['avg_confidence']})")


def main():
    parser = argparse.ArgumentParser(
        description='GABRIEL File Suite - Intelligent File Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Scan a volume
  gabriel.py scan /Volumes/GABRIEL --database gabriel.db
  
  # Classify files with AI
  gabriel.py classify gabriel.db --use-ai --batch 500
  
  # Organize files (symlink mode - no space used)
  gabriel.py organize gabriel.db /Volumes/GABRIEL/Organized --mode symlink
  
  # Find and handle duplicates
  gabriel.py duplicates gabriel.db --action list
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan volume and extract metadata')
    scan_parser.add_argument('volume', help='Path to volume to scan')
    scan_parser.add_argument('--database', '-d', required=True, help='Database file path')
    scan_parser.add_argument('--workers', '-w', type=int, default=8, help='Number of worker threads')
    scan_parser.add_argument('--find-duplicates', action='store_true', help='Find duplicates after scan')
    scan_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Classify command
    classify_parser = subparsers.add_parser('classify', help='Classify files with AI')
    classify_parser.add_argument('database', help='Database file path')
    classify_parser.add_argument('--use-ai', action='store_true', help='Use Claude AI for classification')
    classify_parser.add_argument('--batch', '-b', type=int, default=100, help='Number of files to classify')
    classify_parser.add_argument('--export', '-e', help='Export category map to JSON file')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organize files into structure')
    organize_parser.add_argument('database', help='Database file path')
    organize_parser.add_argument('output', help='Output directory for organized files')
    organize_parser.add_argument('--mode', '-m', choices=['move', 'copy', 'symlink', 'hardlink'], 
                                  default='symlink', help='Organization mode')
    organize_parser.add_argument('--preserve-structure', action='store_true', 
                                  help='Preserve original directory structure')
    organize_parser.add_argument('--by-extension', action='store_true', 
                                  help='Organize by file extension instead of category')
    organize_parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    organize_parser.add_argument('--manifest', '-f', help='Create organization manifest file')
    
    # Duplicates command
    dup_parser = subparsers.add_parser('duplicates', help='Handle duplicate files')
    dup_parser.add_argument('database', help='Database file path')
    dup_parser.add_argument('--action', '-a', 
                            choices=['list', 'keep_newest', 'keep_largest', 'delete_all_but_one'],
                            default='list', help='Action to perform on duplicates')
    dup_parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.add_argument('database', help='Database file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Route to command handler
    if args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'classify':
        cmd_classify(args)
    elif args.command == 'organize':
        cmd_organize(args)
    elif args.command == 'duplicates':
        cmd_duplicates(args)
    elif args.command == 'stats':
        cmd_stats(args)


if __name__ == '__main__':
    main()
