#!/usr/bin/env python3
"""
🔗 GABRIEL MASTER CHAIN - DRIVE DISTRIBUTION SYSTEM 🔗
=====================================================

Intelligently distributes autonomous learning content across
connected drives in the master chain for optimal redundancy
and performance.

Master Chain Strategy:
- 12TB 1: Primary music library + learning resources
- 12TB 2: Backup + extended learning datasets
- RED DRAGON: High-speed cache + active learning sessions
- Additional drives: Distributed storage by domain
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import json

class DriveDistributor:
    """Distribute GABRIEL content across master chain drives."""
    
    def __init__(self):
        # Define master chain drives
        self.drives = {
            '12TB_1': {
                'path': Path('/Volumes/12TB 1'),
                'capacity_gb': 12000,
                'purpose': 'Primary storage - Music + Learning Resources',
                'priority': 1
            },
            '12TB_2': {
                'path': Path('/Volumes/12TB'),
                'capacity_gb': 12000,
                'purpose': 'Backup + Extended datasets',
                'priority': 2
            },
            'RED_DRAGON': {
                'path': Path('/Volumes/RED DRAGON'),
                'capacity_gb': 2000,
                'purpose': 'High-speed cache + Active sessions',
                'priority': 3
            },
            'GABRIEL_MOUNT': {
                'path': Path('/Users/rsp_ms/GABRIEL/GABRIEL_MOUNT'),
                'capacity_gb': 500,
                'purpose': 'Local workspace mount point',
                'priority': 4
            }
        }
        
        # Content distribution strategy
        self.distribution_plan = {
            'learning_data': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': 'Learner profiles, sessions, analytics',
                'path': 'GABRIEL_LEARNING/data'
            },
            'knowledge_graph': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'cache': 'RED_DRAGON',
                'description': '10,000+ concept nodes + embeddings',
                'path': 'GABRIEL_LEARNING/knowledge_graph'
            },
            'skill_trees': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': '1,000+ skills across 50+ domains',
                'path': 'GABRIEL_LEARNING/skill_trees'
            },
            'ai_tutor_sessions': {
                'primary': 'RED_DRAGON',
                'backup': '12TB_1',
                'description': 'Active GPT-4o conversation histories',
                'path': 'GABRIEL_LEARNING/ai_tutor'
            },
            'achievements': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': 'Gamification data + leaderboards',
                'path': 'GABRIEL_LEARNING/achievements'
            },
            'cohorts': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': 'Collaborative learning groups',
                'path': 'GABRIEL_LEARNING/cohorts'
            },
            'analytics_cache': {
                'primary': 'RED_DRAGON',
                'backup': '12TB_1',
                'description': 'Real-time performance metrics',
                'path': 'GABRIEL_LEARNING/analytics'
            },
            'career_data': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': 'Job market analysis + roadmaps',
                'path': 'GABRIEL_LEARNING/career'
            },
            'resources': {
                'primary': '12TB_1',
                'backup': '12TB_2',
                'description': 'Learning materials database',
                'path': 'GABRIEL_LEARNING/resources'
            },
            'ml_models': {
                'primary': '12TB_1',
                'cache': 'RED_DRAGON',
                'description': 'Trained models + embeddings',
                'path': 'GABRIEL_LEARNING/models'
            }
        }
        
        self.stats = {
            'directories_created': 0,
            'files_copied': 0,
            'symlinks_created': 0,
            'total_size_mb': 0,
            'drives_used': set()
        }
    
    def check_drives(self) -> Dict[str, bool]:
        """Check which drives are currently mounted."""
        print("\n🔍 SCANNING MASTER CHAIN DRIVES...")
        print("=" * 80)
        
        available = {}
        for drive_id, drive_info in self.drives.items():
            path = drive_info['path']
            is_available = path.exists()
            available[drive_id] = is_available
            
            status = "✅ ONLINE" if is_available else "❌ OFFLINE"
            print(f"\n{drive_id:15s} {status}")
            print(f"   Path: {path}")
            print(f"   Purpose: {drive_info['purpose']}")
            print(f"   Priority: {drive_info['priority']}")
            
            if is_available:
                self.stats['drives_used'].add(drive_id)
        
        return available
    
    def create_structure(self, dry_run: bool = True) -> Dict[str, Any]:
        """Create directory structure on drives."""
        print("\n\n📂 CREATING DISTRIBUTION STRUCTURE...")
        print("=" * 80)
        
        if dry_run:
            print("\n⚠️  DRY RUN MODE - No actual changes will be made\n")
        
        available_drives = self.check_drives()
        created = []
        
        for content_type, config in self.distribution_plan.items():
            print(f"\n📦 {content_type.upper().replace('_', ' ')}")
            print(f"   Description: {config['description']}")
            
            # Create on primary drive
            if config['primary'] in available_drives and available_drives[config['primary']]:
                primary_path = self.drives[config['primary']]['path'] / config['path']
                print(f"   Primary: {config['primary']} → {primary_path}")
                
                if not dry_run:
                    primary_path.mkdir(parents=True, exist_ok=True)
                    self.stats['directories_created'] += 1
                
                created.append({
                    'content_type': content_type,
                    'drive': config['primary'],
                    'path': str(primary_path),
                    'role': 'primary'
                })
            
            # Create on backup drive
            if 'backup' in config:
                backup_id = config['backup']
                if backup_id in available_drives and available_drives[backup_id]:
                    backup_path = self.drives[backup_id]['path'] / config['path']
                    print(f"   Backup:  {backup_id} → {backup_path}")
                    
                    if not dry_run:
                        backup_path.mkdir(parents=True, exist_ok=True)
                        self.stats['directories_created'] += 1
                    
                    created.append({
                        'content_type': content_type,
                        'drive': backup_id,
                        'path': str(backup_path),
                        'role': 'backup'
                    })
            
            # Create on cache drive
            if 'cache' in config:
                cache_id = config['cache']
                if cache_id in available_drives and available_drives[cache_id]:
                    cache_path = self.drives[cache_id]['path'] / config['path']
                    print(f"   Cache:   {cache_id} → {cache_path}")
                    
                    if not dry_run:
                        cache_path.mkdir(parents=True, exist_ok=True)
                        self.stats['directories_created'] += 1
                    
                    created.append({
                        'content_type': content_type,
                        'drive': cache_id,
                        'path': str(cache_path),
                        'role': 'cache'
                    })
        
        return {
            'created': created,
            'stats': self.stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def distribute_autonomous_learning(self, source_dir: Path, dry_run: bool = True) -> Dict[str, Any]:
        """Distribute autonomous learning system files."""
        print("\n\n🚀 DISTRIBUTING AUTONOMOUS LEARNING SYSTEM...")
        print("=" * 80)
        
        if not source_dir.exists():
            print(f"❌ Source directory not found: {source_dir}")
            return {'error': 'Source not found'}
        
        available_drives = self.check_drives()
        
        # Distribution map
        file_distribution = {
            'autonomous_learning.py': {
                'drives': ['12TB_1', '12TB_2', 'RED_DRAGON'],
                'description': 'Core system (1621 lines)'
            },
            'RUN_X1000_DEMO.py': {
                'drives': ['12TB_1', 'RED_DRAGON'],
                'description': 'Demo script'
            },
            '.gabriel_learning_x1000/': {
                'drives': ['12TB_1', '12TB_2'],
                'description': 'Learning data directory'
            }
        }
        
        results = []
        
        for filename, config in file_distribution.items():
            source_path = source_dir / filename
            
            if not source_path.exists():
                print(f"\n⚠️  Skipping {filename} (not found)")
                continue
            
            print(f"\n📄 {filename}")
            print(f"   {config['description']}")
            
            for drive_id in config['drives']:
                if drive_id not in available_drives or not available_drives[drive_id]:
                    print(f"   ⚠️  {drive_id} offline - skipping")
                    continue
                
                dest_base = self.drives[drive_id]['path'] / 'GABRIEL_LEARNING'
                dest_path = dest_base / filename
                
                print(f"   → {drive_id}: {dest_path}")
                
                if not dry_run:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if source_path.is_file():
                        shutil.copy2(source_path, dest_path)
                        self.stats['files_copied'] += 1
                        file_size = source_path.stat().st_size / (1024 * 1024)  # MB
                        self.stats['total_size_mb'] += file_size
                    elif source_path.is_dir():
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                
                results.append({
                    'file': filename,
                    'drive': drive_id,
                    'destination': str(dest_path),
                    'status': 'copied' if not dry_run else 'planned'
                })
        
        return {
            'results': results,
            'stats': self.stats
        }
    
    def create_symlinks(self, dry_run: bool = True) -> Dict[str, Any]:
        """Create symbolic links for quick access."""
        print("\n\n🔗 CREATING SYMLINK NETWORK...")
        print("=" * 80)
        
        available_drives = self.check_drives()
        
        # Define symlink strategy
        symlinks = []
        
        # Link primary to backup
        if available_drives.get('12TB_1') and available_drives.get('12TB_2'):
            for content_type, config in self.distribution_plan.items():
                if 'backup' in config and config['backup'] == '12TB_2':
                    primary_path = self.drives['12TB_1']['path'] / config['path']
                    backup_path = self.drives['12TB_2']['path'] / config['path']
                    
                    link_name = backup_path.parent / f"{backup_path.name}_PRIMARY_LINK"
                    
                    print(f"\n🔗 {content_type}")
                    print(f"   Link: {link_name}")
                    print(f"   Target: {primary_path}")
                    
                    if not dry_run and primary_path.exists():
                        if link_name.exists() or link_name.is_symlink():
                            link_name.unlink()
                        link_name.symlink_to(primary_path)
                        self.stats['symlinks_created'] += 1
                    
                    symlinks.append({
                        'link': str(link_name),
                        'target': str(primary_path),
                        'content_type': content_type
                    })
        
        return {
            'symlinks': symlinks,
            'stats': self.stats
        }
    
    def generate_report(self) -> str:
        """Generate distribution report."""
        report = f"""
╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║  🔗 GABRIEL MASTER CHAIN - DISTRIBUTION REPORT                                ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 STATISTICS
═══════════════════════════════════════════════════════════════════════════════

Drives Used:        {len(self.stats['drives_used'])}
Directories:        {self.stats['directories_created']}
Files Copied:       {self.stats['files_copied']}
Symlinks Created:   {self.stats['symlinks_created']}
Total Size:         {self.stats['total_size_mb']:.2f} MB

🗺️ DISTRIBUTION MAP
═══════════════════════════════════════════════════════════════════════════════

"""
        
        for content_type, config in self.distribution_plan.items():
            report += f"\n{content_type.upper().replace('_', ' ')}\n"
            report += f"  Description: {config['description']}\n"
            report += f"  Primary:     {config.get('primary', 'N/A')}\n"
            if 'backup' in config:
                report += f"  Backup:      {config['backup']}\n"
            if 'cache' in config:
                report += f"  Cache:       {config['cache']}\n"
            report += f"  Path:        {config['path']}\n"
        
        return report


def main():
    """Execute drive distribution."""
    print("\n" + "="*80)
    print("🔗 GABRIEL MASTER CHAIN - DRIVE DISTRIBUTION SYSTEM")
    print("="*80)
    
    distributor = DriveDistributor()
    
    # Check drives
    available = distributor.check_drives()
    online_count = sum(1 for v in available.values() if v)
    
    print(f"\n📊 Summary: {online_count}/{len(available)} drives online")
    
    if online_count == 0:
        print("\n❌ No drives available! Cannot proceed.")
        return
    
    # Menu
    print("\n\n📋 DISTRIBUTION OPTIONS")
    print("="*80)
    print("1. Create directory structure (DRY RUN)")
    print("2. Create directory structure (EXECUTE)")
    print("3. Distribute autonomous learning system (DRY RUN)")
    print("4. Distribute autonomous learning system (EXECUTE)")
    print("5. Create symlink network (DRY RUN)")
    print("6. Create symlink network (EXECUTE)")
    print("7. Full distribution (DRY RUN)")
    print("8. Full distribution (EXECUTE)")
    print("9. Generate report")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == '1':
        result = distributor.create_structure(dry_run=True)
        print(f"\n✅ Dry run complete: {result['stats']['directories_created']} directories planned")
    
    elif choice == '2':
        confirm = input("\n⚠️  Execute structure creation? (yes/no): ").lower()
        if confirm == 'yes':
            result = distributor.create_structure(dry_run=False)
            print(f"\n✅ Created {result['stats']['directories_created']} directories")
    
    elif choice == '3':
        source = Path('/Users/rsp_ms/GABRIEL')
        result = distributor.distribute_autonomous_learning(source, dry_run=True)
        print(f"\n✅ Dry run complete: {len(result.get('results', []))} operations planned")
    
    elif choice == '4':
        source = Path('/Users/rsp_ms/GABRIEL')
        confirm = input("\n⚠️  Execute file distribution? (yes/no): ").lower()
        if confirm == 'yes':
            result = distributor.distribute_autonomous_learning(source, dry_run=False)
            print(f"\n✅ Distributed {result['stats']['files_copied']} files")
    
    elif choice == '5':
        result = distributor.create_symlinks(dry_run=True)
        print(f"\n✅ Dry run complete: {len(result['symlinks'])} symlinks planned")
    
    elif choice == '6':
        confirm = input("\n⚠️  Execute symlink creation? (yes/no): ").lower()
        if confirm == 'yes':
            result = distributor.create_symlinks(dry_run=False)
            print(f"\n✅ Created {result['stats']['symlinks_created']} symlinks")
    
    elif choice == '7':
        print("\n🚀 FULL DISTRIBUTION (DRY RUN)...")
        distributor.create_structure(dry_run=True)
        source = Path('/Users/rsp_ms/GABRIEL')
        distributor.distribute_autonomous_learning(source, dry_run=True)
        distributor.create_symlinks(dry_run=True)
        print("\n✅ Dry run complete!")
        print(distributor.generate_report())
    
    elif choice == '8':
        confirm = input("\n⚠️  Execute FULL distribution? (yes/no): ").lower()
        if confirm == 'yes':
            print("\n🚀 EXECUTING FULL DISTRIBUTION...")
            distributor.create_structure(dry_run=False)
            source = Path('/Users/rsp_ms/GABRIEL')
            distributor.distribute_autonomous_learning(source, dry_run=False)
            distributor.create_symlinks(dry_run=False)
            print("\n✅ Distribution complete!")
            print(distributor.generate_report())
            
            # Save report
            report_path = Path('/Users/rsp_ms/GABRIEL/distribution_report.txt')
            report_path.write_text(distributor.generate_report())
            print(f"\n📄 Report saved: {report_path}")
    
    elif choice == '9':
        print(distributor.generate_report())
    
    else:
        print("\n👋 Exiting...")


if __name__ == "__main__":
    main()
