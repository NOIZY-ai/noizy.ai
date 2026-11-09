import json
import argparse

DB_PATH = "/Users/m2ultra/.gemini/antigravity/playground/infinite-omega/Audio_Unitor/Database/vi_db.json"

CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'

def search_vi(query):
    print(f"\n🔍 Searching VI Database for: {CYAN}{query}{RESET}")
    
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
    except:
        print("❌ Database not found or corrupted.")
        return
    
    results = []
    q = query.lower()
    
    for inst in db.get('instruments', []):
        if (q in inst.get('name', '').lower() or 
            q in inst.get('developer', '').lower() or
            q in inst.get('type', '').lower()):
            results.append(inst)
    
    if not results:
        print("❌ No matches found.")
    else:
        print(f"✅ Found {len(results)} matches:\n")
        for inst in results[:15]:
            print(f"  [{inst.get('type', 'N/A')}] {GREEN}{inst.get('name')}{RESET} by {inst.get('developer')}")
        
        if len(results) > 15:
            print(f"\n  ...and {len(results)-15} more.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search term")
    args = parser.parse_args()
    search_vi(args.query)
