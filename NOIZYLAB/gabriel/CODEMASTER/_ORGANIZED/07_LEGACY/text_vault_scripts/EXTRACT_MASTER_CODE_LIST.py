#!/usr/bin/env python3
"""
Extract Complete Master Code List from CODE_MASTER
Generates comprehensive catalog of all code files
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

CODE_MASTER = Path("/Users/rsp_ms/CODE_MASTER")
OUTPUT_FILE = CODE_MASTER / "docs" / "CODE_MASTER_INDEX.md"

# Categories mapping
CATEGORIES = {
    'GABRIEL': ['gabriel', 'GABRIEL', 'X1000'],
    'MC96': ['mc96', 'MC96', 'missioncontrol', 'fishnet'],
    'EMAIL_SETUP': ['email', 'gmail', 'improvmx', 'cloudflare', 'alias'],
    'BEATS': ['beats', 'mic', 'voice', 'audio'],
    'AGENTS': ['agent', 'LUCY', 'POPS', 'KEITH', 'DREAM', 'WARD', 'FLEET'],
    'SYSTEM_FIXES': ['fix', 'repair', 'bootstrap', 'corruption', 'shell'],
    'AUTOMATION': ['auto', 'setup', 'install', 'launch', 'organize'],
    'NETWORK': ['network', 'backup', 'distribute', 'drive', 'scan'],
    'UTILITIES': ['git', 'cleanup', 'optimize', 'health', 'monitor'],
}

def extract_description(file_path):
    """Extract description from file header/comments"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[:50]  # Read first 50 lines
            
            # Look for common header patterns
            for i, line in enumerate(lines):
                # Python docstrings
                if '"""' in line or "'''" in line:
                    desc = []
                    quote = '"""' if '"""' in line else "'''"
                    for j in range(i, min(i+10, len(lines))):
                        desc.append(lines[j].strip())
                        if quote in lines[j] and j > i:
                            return ' '.join(desc).replace(quote, '').strip()
                
                # Shell script comments
                if line.strip().startswith('#') and len(line.strip()) > 5:
                    if any(keyword in line.lower() for keyword in ['purpose', 'description', 'what', 'this']):
                        return line.strip('#').strip()
                
                # Markdown headers
                if line.startswith('#') and i < 5:
                    return line.strip('#').strip()
            
            # Fallback: first meaningful comment
            for line in lines[:20]:
                if line.strip().startswith('#') and len(line.strip()) > 10:
                    return line.strip('#').strip()[:100]
    except:
        pass
    
    return "No description available"

def categorize_file(file_path, filename):
    """Categorize file by name and path"""
    path_str = str(file_path).lower()
    name_lower = filename.lower()
    
    categories = []
    for cat, keywords in CATEGORIES.items():
        if any(kw.lower() in path_str or kw.lower() in name_lower for kw in keywords):
            categories.append(cat)
    
    if not categories:
        return 'UTILITIES'
    
    # Priority order for multiple matches
    priority = ['GABRIEL', 'MC96', 'AGENTS', 'EMAIL_SETUP', 'BEATS', 'SYSTEM_FIXES', 'AUTOMATION', 'NETWORK', 'UTILITIES']
    for pcat in priority:
        if pcat in categories:
            return pcat
    
    return categories[0]

def get_file_type(file_path):
    """Get file type from extension"""
    ext = file_path.suffix.lower()
    type_map = {
        '.sh': 'Shell Script',
        '.ps1': 'PowerShell Script',
        '.py': 'Python Script',
        '.js': 'JavaScript',
        '.md': 'Markdown',
        '.txt': 'Text File',
        '.json': 'JSON Config',
    }
    return type_map.get(ext, 'Other')

def scan_all_files():
    """Scan all code files in CODE_MASTER"""
    files_data = defaultdict(lambda: defaultdict(list))
    stats = defaultdict(int)
    total_size = 0
    
    # File extensions to include
    extensions = {'.sh', '.ps1', '.py', '.js', '.md', '.txt', '.json'}
    
    for root, dirs, files in os.walk(CODE_MASTER):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = Path(root) / file
            ext = file_path.suffix.lower()
            
            if ext in extensions:
                try:
                    size = file_path.stat().st_size
                    total_size += size
                    
                    file_type = get_file_type(file_path)
                    category = categorize_file(file_path, file)
                    description = extract_description(file_path)
                    
                    rel_path = file_path.relative_to(CODE_MASTER)
                    
                    file_info = {
                        'name': file,
                        'path': str(rel_path),
                        'full_path': str(file_path),
                        'type': file_type,
                        'category': category,
                        'size': size,
                        'description': description,
                    }
                    
                    files_data[category][file_type].append(file_info)
                    stats[file_type] += 1
                    stats['total'] += 1
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    return files_data, stats, total_size

def generate_master_index(files_data, stats, total_size):
    """Generate the master index markdown document"""
    
    output = []
    output.append("# CODE_MASTER - COMPLETE MASTER CODE INDEX")
    output.append("")
    output.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"**Total Files:** {stats['total']}")
    output.append(f"**Total Size:** {total_size / 1024 / 1024:.2f} MB")
    output.append("")
    output.append("---")
    output.append("")
    
    # Statistics section
    output.append("## 📊 STATISTICS")
    output.append("")
    output.append("### File Count by Type:")
    for file_type, count in sorted(stats.items()):
        if file_type != 'total':
            output.append(f"- **{file_type}:** {count}")
    output.append("")
    output.append("---")
    output.append("")
    
    # Files organized by category
    output.append("## 📁 FILES BY CATEGORY")
    output.append("")
    
    for category in sorted(files_data.keys()):
        output.append(f"### {category}")
        output.append("")
        
        for file_type in sorted(files_data[category].keys()):
            files = files_data[category][file_type]
            output.append(f"#### {file_type} ({len(files)} files)")
            output.append("")
            
            for file_info in sorted(files, key=lambda x: x['name']):
                output.append(f"**{file_info['name']}**")
                output.append(f"- Path: `{file_info['path']}`")
                output.append(f"- Size: {file_info['size'] / 1024:.1f} KB")
                output.append(f"- Description: {file_info['description'][:150]}")
                output.append("")
        
        output.append("---")
        output.append("")
    
    # Quick reference by file type
    output.append("## 🔍 QUICK REFERENCE BY FILE TYPE")
    output.append("")
    
    type_files = defaultdict(list)
    for category in files_data.values():
        for file_type, files in category.items():
            type_files[file_type].extend(files)
    
    for file_type in sorted(type_files.keys()):
        output.append(f"### {file_type}")
        output.append("")
        for file_info in sorted(type_files[file_type], key=lambda x: x['name']):
            output.append(f"- `{file_info['path']}` - {file_info['description'][:80]}")
        output.append("")
    
    return '\n'.join(output)

def main():
    """Main execution"""
    print("🔍 Scanning CODE_MASTER directory...")
    files_data, stats, total_size = scan_all_files()
    
    print(f"✅ Found {stats['total']} files")
    print("📝 Generating master index...")
    
    # Ensure docs directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate index
    index_content = generate_master_index(files_data, stats, total_size)
    
    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Master index created: {OUTPUT_FILE}")
    print(f"📊 Total files cataloged: {stats['total']}")
    print(f"💾 Total size: {total_size / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    main()

