import os
import argparse
from pathlib import Path

STAGING_AREA = "/Users/m2ultra/Audio_Unitor/Staging_Area"

CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'

def search_aliases(query):
    print(f"\n🔍 Searching Library for: {CYAN}{query}{RESET}")
    results = []
    
    root = Path(STAGING_AREA)
    if not root.exists():
        print("Library empty.")
        return

    # Using rglob for recursive search
    # This searches the filenames of the aliases
    for item in root.rglob(f"*{query}*"):
        if item.is_symlink() or item.is_file():
            results.append(item)
            
    if not results:
        print(f"❌ No results found.")
    else:
        print(f"✅ Found {len(results)} matches:\n")
        for i, res in enumerate(results[:20]): # Limit display
            # Show category context (parent folder)
            category = res.parent.name
            print(f" {i+1}. [{category}] {res.name}")
            
        if len(results) > 20:
             print(f"\n...and {len(results)-20} more.")
             
        print(f"\n{GREEN}Tip: Use Option 4 (Fetch) to edit any of these.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search term")
    args = parser.parse_args()
    search_aliases(args.query)
