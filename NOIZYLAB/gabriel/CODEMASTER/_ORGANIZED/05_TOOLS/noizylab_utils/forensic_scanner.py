#!/usr/bin/env python3
"""
FORENSIC CODE RECONSTRUCTOR
Rebuilds code library based on:
1. Modification dates (temporal ordering)
2. Content relevance (keyword scoring)

Creates MemCells for each file with metadata.
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re

# Configuration
SCAN_PATHS = [
    "/Users/m2ultra/AI_COMPLETE_BRAIN",
    "/Volumes/JOE/NKI",
    "/Volumes/6TB/Sample_Libraries",
    "/Volumes/RED DRAGON/noizylab_2026",
]

OUTPUT_DIR = "/Users/m2ultra/m2ultra/noizylab/memcells"
CODE_EXTENSIONS = {'.py', '.ts', '.js', '.sh', '.sql', '.json', '.yaml', '.yml', '.md'}

# Relevance keywords with weights
RELEVANCE_KEYWORDS = {
    'gabriel': 10, 'noizylab': 10, 'turbo': 8, 'mission_control': 8,
    'memcell': 9, 'gorunfree': 9, 'omega': 7, 'god_mode': 7,
    'ai': 5, 'llm': 5, 'prompt': 6, 'agent': 6,
    'streamlit': 4, 'api': 4, 'claude': 5, 'gemini': 5, 'openai': 5,
}

def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]

def score_relevance(content: str, filepath: str) -> float:
    """Score 0.0-1.0 based on keyword presence"""
    text = (content + filepath).lower()
    score = 0
    max_score = sum(RELEVANCE_KEYWORDS.values())
    
    for keyword, weight in RELEVANCE_KEYWORDS.items():
        if keyword in text:
            score += weight
    
    return min(score / max_score, 1.0)

def categorize_file(ext: str) -> str:
    if ext in {'.py', '.ts', '.js', '.sh'}:
        return 'code'
    elif ext in {'.json', '.yaml', '.yml', '.toml'}:
        return 'config'
    elif ext == '.md':
        return 'doc'
    elif ext == '.sql':
        return 'code'
    return 'other'

def extract_tags(content: str, filepath: str) -> list:
    """Extract relevant tags from content"""
    tags = []
    text = (content + filepath).lower()
    
    if 'gabriel' in text: tags.append('gabriel')
    if 'turbo' in text: tags.append('turbo')
    if 'mission_control' in text or 'mission-control' in text: tags.append('mission_control')
    if 'memcell' in text: tags.append('memcell')
    if 'prompt' in text: tags.append('prompt')
    if 'agent' in text: tags.append('agent')
    if 'streamlit' in text: tags.append('streamlit')
    if 'api' in text: tags.append('api')
    
    return tags

def scan_directory(path: str) -> list:
    """Scan directory for code files"""
    memcells = []
    
    if not os.path.exists(path):
        print(f"⚠️ Path not found: {path}")
        return memcells
    
    print(f"📡 Scanning: {path}")
    
    for root, dirs, files in os.walk(path):
        # Skip hidden and cache directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'node_modules' and d != 'venv']
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in CODE_EXTENSIONS:
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                stat = os.stat(filepath)
                mtime = datetime.fromtimestamp(stat.st_mtime)
                
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                if len(content) < 10:  # Skip nearly empty files
                    continue
                
                relevance = score_relevance(content, filepath)
                
                memcell = {
                    'memcell_id': hash_content(filepath + str(stat.st_mtime)),
                    'timestamp': mtime.isoformat(),
                    'source_path': filepath,
                    'filename': file,
                    'category': categorize_file(ext),
                    'extension': ext,
                    'content_hash': hash_content(content),
                    'size_bytes': stat.st_size,
                    'relevance_score': round(relevance, 3),
                    'tags': extract_tags(content, filepath),
                }
                
                memcells.append(memcell)
                
            except Exception as e:
                print(f"  ⚠️ Error reading {filepath}: {e}")
    
    return memcells

def main():
    print("=" * 60)
    print("🔬 FORENSIC CODE RECONSTRUCTOR")
    print("=" * 60)
    
    all_memcells = []
    
    for path in SCAN_PATHS:
        memcells = scan_directory(path)
        all_memcells.extend(memcells)
        print(f"  Found {len(memcells)} files")
    
    # Sort by relevance (high first), then by date (newest first)
    all_memcells.sort(key=lambda x: (-x['relevance_score'], x['timestamp']), reverse=False)
    
    print(f"\n📊 Total files scanned: {len(all_memcells)}")
    
    # Filter high relevance
    high_relevance = [m for m in all_memcells if m['relevance_score'] >= 0.1]
    print(f"📌 High relevance files: {len(high_relevance)}")
    
    # Save to JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    output_file = os.path.join(OUTPUT_DIR, 'memcell_index.json')
    with open(output_file, 'w') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'total_files': len(all_memcells),
            'high_relevance': len(high_relevance),
            'memcells': all_memcells
        }, f, indent=2)
    
    print(f"\n✅ Index saved to: {output_file}")
    
    # Print top 20 most relevant
    print("\n🏆 TOP 20 MOST RELEVANT FILES:")
    print("-" * 60)
    for i, m in enumerate(high_relevance[:20], 1):
        print(f"{i:2}. [{m['relevance_score']:.2f}] {m['filename']}")
        print(f"    {m['source_path']}")
        print(f"    Tags: {', '.join(m['tags']) if m['tags'] else 'none'}")

if __name__ == "__main__":
    main()
