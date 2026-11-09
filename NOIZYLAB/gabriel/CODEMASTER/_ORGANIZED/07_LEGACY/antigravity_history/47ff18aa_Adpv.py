import json
import argparse
import sys

INDEX_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/oracle_index.json"

CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

def search_oracle(query):
    print(f"\n🔮 Consulting The Oracle for: {CYAN}{query}{RESET}")
    
    try:
        with open(INDEX_PATH, 'r') as f:
            data = json.load(f)
    except:
        print("❌ Oracle Database not found. Run Indexer first.")
        return

    files = data.get('files', [])
    count = data.get('meta', {}).get('count', 0)
    print(f"   (Searching {count:,} samples...)")
    
    q_lower = query.lower()
    results = [f for f in files if q_lower in f.lower()]
    
    if not results:
        print("❌ No matches found.")
    else:
        print(f"✅ Found {len(results)} matches:\n")
        for i, path in enumerate(results[:20]):
            print(f"  {path}")
            
        if len(results) > 20:
             print(f"\n...and {len(results)-20} more.")
             
    print(f"\n{GREEN}Tip: Use Option 4 (Fetch) to edit any of these.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search term")
    args = parser.parse_args()
    search_oracle(args.query)
