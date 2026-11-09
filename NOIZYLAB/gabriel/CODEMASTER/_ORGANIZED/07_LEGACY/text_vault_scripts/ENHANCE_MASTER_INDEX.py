#!/usr/bin/env python3
"""
Enhance Master Index with line counts and better descriptions
Also create backup archive
"""

import os
import subprocess
from pathlib import Path

CODE_MASTER = Path("/Users/rsp_ms/CODE_MASTER")
INDEX_FILE = CODE_MASTER / "docs" / "CODE_MASTER_INDEX.md"

def count_lines(file_path):
    """Count lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except:
        return 0

def enhance_index():
    """Add line counts and improve index"""
    if not INDEX_FILE.exists():
        print("Index file not found. Run EXTRACT_MASTER_CODE_LIST.py first.")
        return
    
    print("📊 Enhancing master index with line counts...")
    
    # Read existing index
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all file paths in the index
    import re
    path_pattern = r'Path: `([^`]+)`'
    paths = re.findall(path_pattern, content)
    
    # Add line counts
    enhanced_content = content
    for path_str in paths:
        file_path = CODE_MASTER / path_str
        if file_path.exists():
            lines = count_lines(file_path)
            # Add line count after size if not already present
            if f"Path: `{path_str}`" in enhanced_content and f"Lines: {lines}" not in enhanced_content:
                enhanced_content = enhanced_content.replace(
                    f"Path: `{path_str}`\n- Size:",
                    f"Path: `{path_str}`\n- Lines: {lines}\n- Size:"
                )
    
    # Write enhanced index
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    print(f"✅ Enhanced index saved: {INDEX_FILE}")

def create_backup_archive():
    """Create a backup archive of all CODE_MASTER files"""
    print("💾 Creating backup archive...")
    
    backup_dir = CODE_MASTER.parent / "CODE_MASTER_BACKUP"
    backup_dir.mkdir(exist_ok=True)
    
    # Create tar archive
    archive_name = f"CODE_MASTER_BACKUP_{Path.home().name}_{subprocess.check_output(['date', '+%Y%m%d_%H%M%S']).decode().strip()}.tar.gz"
    archive_path = backup_dir / archive_name
    
    try:
        subprocess.run([
            'tar', '-czf', str(archive_path),
            '-C', str(CODE_MASTER.parent),
            'CODE_MASTER'
        ], check=True, capture_output=True)
        
        size = archive_path.stat().st_size / 1024 / 1024
        print(f"✅ Backup archive created: {archive_path}")
        print(f"📦 Archive size: {size:.2f} MB")
        return archive_path
    except Exception as e:
        print(f"❌ Error creating archive: {e}")
        return None

if __name__ == "__main__":
    enhance_index()
    archive = create_backup_archive()
    if archive:
        print(f"\n✅ All work saved!")
        print(f"📁 Master Index: {INDEX_FILE}")
        print(f"💾 Backup Archive: {archive}")

