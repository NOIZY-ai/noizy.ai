import os
from datetime import datetime

SOURCE_DIR = "/Users/m2ultra/Documents/GABRIEL"
OUTPUT_FILE = os.path.join(SOURCE_DIR, "GABRIEL_COMPLETE_INGESTION.md")

SKIP_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar', '.gz', '.pyc', '.DS_Store'}
SKIP_DIRS = {'.git', '.claude-worktrees', '__pycache__', 'node_modules', 'EXECUTION_REPORTS', 'NOIZYLAB_AGENTS_BRANCH'}

def is_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read(1024)
        return True
    except UnicodeDecodeError:
        return False

def generate_omnibus():
    files_to_ingest = []
    
    # Walk the directory
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for file in files:
            if file.startswith('.'): continue
            
            ext = os.path.splitext(file)[1].lower()
            if ext in SKIP_EXTENSIONS: continue
            
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, SOURCE_DIR)
            
            # Skip the output file itself if it exists
            if filepath == OUTPUT_FILE: continue
            
            files_to_ingest.append((relpath, filepath))
    
    files_to_ingest.sort()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        # Header
        outfile.write(f"# GABRIEL COMPLETE INGESTION\n")
        outfile.write(f"Generated: {datetime.now().isoformat()}\n")
        outfile.write(f"Source: {SOURCE_DIR}\n\n")
        
        # Table of Contents
        outfile.write("## Table of Contents\n")
        for relpath, _ in files_to_ingest:
            anchor = relpath.replace('/', '-').replace('.', '-').replace('_', '-').lower()
            outfile.write(f"- [{relpath}](#{anchor})\n")
        outfile.write("\n---\n\n")
        
        # File Contents
        for relpath, filepath in files_to_ingest:
            if not is_text_file(filepath):
                print(f"Skipping binary file: {relpath}")
                continue
                
            print(f"Ingesting: {relpath}")
            anchor = relpath.replace('/', '-').replace('.', '-').replace('_', '-').lower()
            outfile.write(f"## {relpath} <a name=\"{anchor}\"></a>\n")
            outfile.write(f"**Path**: `{filepath}`\n\n")
            
            ext = os.path.splitext(relpath)[1].lower()
            lang = ext.replace('.', '')
            if lang == 'md': lang = 'markdown'
            if lang == 'py': lang = 'python'
            if lang == 'sh': lang = 'bash'
            if not lang: lang = 'text'
            
            outfile.write(f"```{lang}\n")
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(f"Error reading file: {e}")
            outfile.write("\n```\n\n")
            outfile.write("---\n\n")

if __name__ == "__main__":
    generate_omnibus()
    print(f"Successfully created {OUTPUT_FILE}")
