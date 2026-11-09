#!/usr/bin/env python3
# ==============================================================================
# 🧠 TURBO CORTEX FEED (KNOWLEDGE INGESTION)
# ==============================================================================
# "Inhales" knowledge to turn the user into an Audio Beast.
# PROTOCOL: GORUNFREE

import os
import sys
import glob
from pathlib import Path

try:
    import turbo_config as cfg
    from turbo_memcell import MemCell
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    import turbo_config as cfg
    from turbo_memcell import MemCell

# CONFIG
KNOWLEDGE_DIR = cfg.ASSETS_DIR / "Knowledge"
BRAIN = MemCell()

def setup_knowledge_base():
    if not KNOWLEDGE_DIR.exists():
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"CORE > Created Knowledge Base: {KNOWLEDGE_DIR}")
        
    # Create a README
    readme = KNOWLEDGE_DIR / "README.txt"
    if not readme.exists():
        with open(readme, "w") as f:
            f.write("DROP TEXT FILES AND PDFS HERE TO FEED THE CORTEX.\n")
            f.write("Topics: Audio Engineering, Mixing, Mastering, Python, etc.\n")

def ingest_file(filepath):
    path = Path(filepath)
    print(f"CORE > 🧠 Inhaling: {path.name}...")
    
    content = ""
    try:
        # Text Files
        if path.suffix in ['.txt', '.md', '.py', '.json']:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
        # PDF (Simple text extraction if simple)
        # For now, placeholder or needs 'pypdf'
        elif path.suffix == '.pdf':
            print("CORE > PDF detected. Text extraction required (Install pypdf). Skipping content for now.")
            content = f"PDF File: {path.name} (Content index pending)"
            
        if content:
            # Chunking could be added here
            # For now, log as a high-value memory
            BRAIN.log_event(0, "KNOWLEDGE_INGEST", f"Source: {path.name}\n{content[:500]}...", vibe=90, author="CORTEX_FEED")
            print(f"CORE > ✅ {path.name} assimilated.")
            
    except Exception as e:
        print(f"CORE > ❌ Failed to ingest {path.name}: {e}")

def run_feed():
    cfg.print_header("🧠 CORTEX FEED", "Knowledge Assimilation Protocol")
    setup_knowledge_base()
    
    files = []
    for ext in ['*.txt', '*.md', '*.pdf']:
        files.extend(list(KNOWLEDGE_DIR.glob(ext)))
        
    if not files:
        print(f"CORE > Knowledge Base is empty. Drop files in: {KNOWLEDGE_DIR}")
        return
        
    for f in files:
        ingest_file(f)
        
    print(f"\n{cfg.BOLD}{cfg.GREEN}CORE > Assimilation Complete.{cfg.RESET}")

if __name__ == "__main__":
    run_feed()
