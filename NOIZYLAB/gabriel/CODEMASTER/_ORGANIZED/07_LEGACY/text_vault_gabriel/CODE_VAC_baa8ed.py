#!/usr/bin/env python3
"""
🌪️ CODE_VAC - GABRIEL's Code Vacuum Cleaner
Sucks up, analyzes, organizes, and cleans ALL code across the MC96ECOUNIVERSE
NO CODE LEFT BEHIND!
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import hashlib
import shutil
import json
from datetime import datetime
import re
from collections import defaultdict

class CodeVac:
    """
    🌪️ CODE_VAC - The Ultimate Code Vacuum
    Sucks up ALL code files, removes duplicates, organizes by type, cleans junk
    """
    
    def __init__(self, workspace: Path = None):
        self.workspace = workspace or Path.cwd()
        self.vacuum_dir = self.workspace / "CODE_VAC_STORAGE"
        
        # Code file extensions to vacuum
        self.code_extensions = {
            # Programming languages
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.java', '.c', '.cpp', '.h', '.hpp',
            '.cs', '.go', '.rs', '.swift', '.kt',
            '.rb', '.php', '.pl', '.lua', '.r',
            '.m', '.mm', '.scala', '.clj', '.ex',
            '.elixir', '.erl', '.hs', '.ml', '.fs',
            
            # Web
            '.html', '.htm', '.css', '.scss', '.sass',
            '.less', '.vue', '.svelte',
            
            # Shells
            '.sh', '.bash', '.zsh', '.fish', '.ps1',
            
            # Config/Data
            '.json', '.yaml', '.yml', '.toml', '.xml',
            '.ini', '.conf', '.cfg', '.env',
            
            # Documentation
            '.md', '.rst', '.txt', '.adoc',
            
            # SQL
            '.sql', '.psql', '.mysql',
            
            # Other
            '.vim', '.el', '.gradle', '.cmake',
            '.make', '.dockerfile', '.dockerignore'
        }
        
        self.vacuumed_files = []
        self.duplicates = []
        self.junk_files = []
        self.file_hashes = {}
        self.stats = defaultdict(int)
        
        print("\n" + "=" * 80)
        print("🌪️ CODE_VAC - Ultimate Code Vacuum Cleaner")
        print("   Sucking up ALL code across the MC96ECOUNIVERSE")
        print("=" * 80)
    
    def vacuum_all_drives(self, drives: List[str] = None):
        """Vacuum code from all specified drives."""
        if drives is None:
            # Auto-detect all drives
            drives = self._detect_all_drives()
        
        print(f"\n🌪️ VACUUMING {len(drives)} DRIVES...")
        print("=" * 80)
        
        for drive in drives:
            drive_path = Path(drive)
            if drive_path.exists():
                print(f"\n🔍 Vacuuming: {drive}")
                self._vacuum_directory(drive_path, max_depth=10)
            else:
                print(f"⚠️  Skipped: {drive} (not accessible)")
        
        print("\n" + "=" * 80)
        print(f"🌪️ VACUUM COMPLETE!")
        print(f"   Files found: {self.stats['files_found']}")
        print(f"   Files vacuumed: {self.stats['files_vacuumed']}")
        print(f"   Duplicates: {self.stats['duplicates']}")
        print(f"   Junk removed: {self.stats['junk_removed']}")
        print("=" * 80)
    
    def _detect_all_drives(self) -> List[str]:
        """Detect all mounted drives."""
        drives = [str(self.workspace)]
        
        # Add /Volumes drives
        volumes_path = Path('/Volumes')
        if volumes_path.exists():
            for volume in volumes_path.iterdir():
                if volume.is_dir() and not volume.name.startswith('.'):
                    drives.append(str(volume))
        
        return drives
    
    def _vacuum_directory(self, directory: Path, max_depth: int = 10, current_depth: int = 0):
        """Recursively vacuum code files from directory."""
        if current_depth > max_depth:
            return
        
        # Skip certain directories
        skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'env', '.env', 'build', 'dist', '.cache', 'cache',
            'Library', 'Applications', 'System', '.Trash',
            'logs', 'log', 'tmp', 'temp'
        }
        
        try:
            for item in directory.iterdir():
                # Skip hidden and system items
                if item.name.startswith('.') and item.name not in ['.env', '.gitignore']:
                    continue
                
                if item.is_dir():
                    # Skip banned directories
                    if item.name in skip_dirs:
                        continue
                    
                    # Recurse
                    self._vacuum_directory(item, max_depth, current_depth + 1)
                
                elif item.is_file():
                    self.stats['files_found'] += 1
                    
                    # Check if it's a code file
                    if item.suffix.lower() in self.code_extensions:
                        self._vacuum_file(item)
        
        except PermissionError:
            pass
        except Exception as e:
            pass
    
    def _vacuum_file(self, file_path: Path):
        """Vacuum a single code file."""
        try:
            # Skip large files (>10MB)
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return
            
            # Calculate hash
            file_hash = self._calculate_hash(file_path)
            
            # Check for duplicates
            if file_hash in self.file_hashes:
                self.duplicates.append({
                    'file': str(file_path),
                    'duplicate_of': self.file_hashes[file_hash],
                    'hash': file_hash
                })
                self.stats['duplicates'] += 1
                return
            
            # Check if it's junk
            if self._is_junk(file_path):
                self.junk_files.append(str(file_path))
                self.stats['junk_removed'] += 1
                return
            
            # Vacuum the file
            file_info = {
                'path': str(file_path),
                'name': file_path.name,
                'extension': file_path.suffix,
                'size': file_path.stat().st_size,
                'hash': file_hash,
                'lines': self._count_lines(file_path),
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            
            self.vacuumed_files.append(file_info)
            self.file_hashes[file_hash] = str(file_path)
            self.stats['files_vacuumed'] += 1
            
            # Update extension stats
            ext = file_path.suffix.lower()
            self.stats[f'ext_{ext}'] += 1
        
        except Exception:
            pass
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate file hash."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ''
    
    def _count_lines(self, file_path: Path) -> int:
        """Count lines in file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.readlines())
        except:
            return 0
    
    def _is_junk(self, file_path: Path) -> bool:
        """Check if file is junk."""
        junk_patterns = [
            r'test\.py$',
            r'temp\..*$',
            r'tmp\..*$',
            r'\.backup$',
            r'\.old$',
            r'\.bak$',
            r'~$'
        ]
        
        name = file_path.name.lower()
        
        for pattern in junk_patterns:
            if re.search(pattern, name):
                return True
        
        # Check if file is empty or nearly empty
        try:
            if file_path.stat().st_size < 10:
                return True
            
            # Check if file has no real content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
                if len(content) < 10:
                    return True
        except:
            pass
        
        return False
    
    def organize_by_language(self):
        """Organize vacuumed files by programming language."""
        print("\n📁 ORGANIZING BY LANGUAGE...")
        print("=" * 80)
        
        organized = defaultdict(list)
        
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React-TypeScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.swift': 'Swift',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.md': 'Markdown',
            '.sql': 'SQL'
        }
        
        for file_info in self.vacuumed_files:
            ext = file_info['extension'].lower()
            language = language_map.get(ext, 'Other')
            organized[language].append(file_info)
        
        # Display organization
        for language in sorted(organized.keys()):
            files = organized[language]
            total_lines = sum(f['lines'] for f in files)
            print(f"\n{language:20s} : {len(files):5d} files, {total_lines:8d} lines")
        
        print("=" * 80)
        
        return organized
    
    def find_largest_files(self, top_n: int = 20):
        """Find largest code files."""
        print(f"\n📊 TOP {top_n} LARGEST FILES:")
        print("=" * 80)
        
        sorted_files = sorted(self.vacuumed_files, 
                            key=lambda x: x['lines'], 
                            reverse=True)[:top_n]
        
        for i, file_info in enumerate(sorted_files, 1):
            name = Path(file_info['path']).name
            print(f"{i:2d}. {file_info['lines']:6d} lines : {name:40s} ({file_info['extension']})")
        
        print("=" * 80)
    
    def find_oldest_files(self, top_n: int = 20):
        """Find oldest code files."""
        print(f"\n📅 TOP {top_n} OLDEST FILES:")
        print("=" * 80)
        
        sorted_files = sorted(self.vacuumed_files, 
                            key=lambda x: x['modified'])[:top_n]
        
        for i, file_info in enumerate(sorted_files, 1):
            name = Path(file_info['path']).name
            date = file_info['modified'][:10]
            print(f"{i:2d}. {date} : {name:50s}")
        
        print("=" * 80)
    
    def find_duplicates(self):
        """Show duplicate files."""
        print(f"\n🔍 DUPLICATE FILES ({len(self.duplicates)}):")
        print("=" * 80)
        
        for dup in self.duplicates[:50]:
            print(f"\n❌ DUPLICATE:")
            print(f"   Original: {dup['duplicate_of']}")
            print(f"   Copy:     {dup['file']}")
        
        if len(self.duplicates) > 50:
            print(f"\n... and {len(self.duplicates) - 50} more")
        
        print("=" * 80)
    
    def search_content(self, pattern: str):
        """Search for pattern in vacuumed files."""
        print(f"\n🔎 SEARCHING FOR: '{pattern}'")
        print("=" * 80)
        
        matches = []
        
        for file_info in self.vacuumed_files:
            try:
                with open(file_info['path'], 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if re.search(pattern, content, re.IGNORECASE):
                        matches.append(file_info)
            except:
                pass
        
        print(f"\n✅ Found {len(matches)} files containing '{pattern}':")
        for match in matches[:30]:
            print(f"   • {Path(match['path']).name:40s} : {match['path']}")
        
        if len(matches) > 30:
            print(f"\n... and {len(matches) - 30} more")
        
        print("=" * 80)
        
        return matches
    
    def export_inventory(self, filename: str = "CODE_INVENTORY.json"):
        """Export complete code inventory."""
        inventory = {
            'timestamp': datetime.now().isoformat(),
            'total_files': len(self.vacuumed_files),
            'total_duplicates': len(self.duplicates),
            'total_junk': len(self.junk_files),
            'stats': dict(self.stats),
            'files': self.vacuumed_files,
            'duplicates': self.duplicates,
            'junk': self.junk_files
        }
        
        output_path = self.workspace / filename
        with open(output_path, 'w') as f:
            json.dump(inventory, f, indent=2)
        
        print(f"\n💾 Inventory exported to: {output_path}")
        print(f"   {len(self.vacuumed_files)} files catalogued")
        
        return output_path
    
    def create_backup(self, backup_dir: str = "CODE_BACKUP"):
        """Create organized backup of all code."""
        backup_path = self.workspace / backup_dir
        backup_path.mkdir(exist_ok=True)
        
        print(f"\n💾 CREATING BACKUP: {backup_path}")
        print("=" * 80)
        
        organized = self.organize_by_language()
        
        for language, files in organized.items():
            lang_dir = backup_path / language
            lang_dir.mkdir(exist_ok=True)
            
            print(f"\n📁 Backing up {language}... ({len(files)} files)")
            
            for file_info in files:
                try:
                    src = Path(file_info['path'])
                    dst = lang_dir / src.name
                    
                    # Handle name collisions
                    counter = 1
                    while dst.exists():
                        dst = lang_dir / f"{src.stem}_{counter}{src.suffix}"
                        counter += 1
                    
                    shutil.copy2(src, dst)
                except Exception as e:
                    pass
        
        print("\n" + "=" * 80)
        print(f"✅ Backup complete: {backup_path}")
        print("=" * 80)
    
    def generate_report(self):
        """Generate comprehensive CODE_VAC report."""
        print("\n" + "=" * 80)
        print("🌪️ CODE_VAC COMPREHENSIVE REPORT")
        print("=" * 80)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total files scanned:  {self.stats['files_found']:,}")
        print(f"   Code files vacuumed:  {self.stats['files_vacuumed']:,}")
        print(f"   Duplicate files:      {self.stats['duplicates']:,}")
        print(f"   Junk files removed:   {self.stats['junk_removed']:,}")
        
        total_lines = sum(f['lines'] for f in self.vacuumed_files)
        total_size = sum(f['size'] for f in self.vacuumed_files)
        
        print(f"\n   Total lines of code:  {total_lines:,}")
        print(f"   Total size:           {total_size / (1024*1024):.2f} MB")
        
        # Language breakdown
        print(f"\n📊 BY LANGUAGE:")
        ext_stats = {k: v for k, v in self.stats.items() if k.startswith('ext_')}
        sorted_exts = sorted(ext_stats.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for ext, count in sorted_exts:
            ext_name = ext.replace('ext_', '')
            print(f"   {ext_name:15s} : {count:5d} files")
        
        print("=" * 80)


def main():
    """Main CODE_VAC interface."""
    vac = CodeVac()
    
    while True:
        print("\n" + "=" * 80)
        print("🌪️ CODE_VAC - Code Vacuum Cleaner")
        print("=" * 80)
        
        print("\n📋 OPERATIONS:")
        print("  1. 🌪️  Vacuum all drives (auto-detect)")
        print("  2. 🌪️  Vacuum specific directory")
        print("  3. 📁 Organize by language")
        print("  4. 📊 Show largest files")
        print("  5. 📅 Show oldest files")
        print("  6. 🔍 Show duplicates")
        print("  7. 🔎 Search content")
        print("  8. 💾 Export inventory")
        print("  9. 💾 Create organized backup")
        print(" 10. 📊 Generate full report")
        print("  0. Exit")
        
        choice = input("\n🌪️  Select operation: ").strip()
        
        if choice == '1':
            vac.vacuum_all_drives()
            
        elif choice == '2':
            path = input("Enter directory path: ").strip()
            if path:
                vac._vacuum_directory(Path(path))
            
        elif choice == '3':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.organize_by_language()
            
        elif choice == '4':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.find_largest_files()
            
        elif choice == '5':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.find_oldest_files()
            
        elif choice == '6':
            if not vac.duplicates:
                print("⚠️  No duplicates found.")
            else:
                vac.find_duplicates()
            
        elif choice == '7':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                pattern = input("Enter search pattern: ").strip()
                if pattern:
                    vac.search_content(pattern)
        
        elif choice == '8':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.export_inventory()
        
        elif choice == '9':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.create_backup()
        
        elif choice == '10':
            if not vac.vacuumed_files:
                print("⚠️  No files vacuumed yet. Run vacuum first.")
            else:
                vac.generate_report()
        
        elif choice == '0':
            print("\n🌪️  CODE_VAC shutting down. All clean!")
            break
        
        else:
            print("❌ Invalid option")
        
        input("\n⏸️  Press Enter to continue...")


if __name__ == "__main__":
    main()
