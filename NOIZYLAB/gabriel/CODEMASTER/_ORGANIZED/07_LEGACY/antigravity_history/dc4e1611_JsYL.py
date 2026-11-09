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
    tags_db = data.get('tags', {})
    
    # Check for Semantic Tags (e.g. bpm:128)
    semantic_filter = None
    text_query = query
    
    if ":" in query:
        parts = query.split(":")
        if len(parts) == 2:
            key, val = parts[0].lower(), parts[1].lower()
            semantic_filter = (key, val)
            print(f"   (Semantic Filter: {key}={val})")
            text_query = "" # Pure semantic search if just one tag, or we could handle mixed. 
                            # For now, let's assume if tag is present, that's the search.
    
    count = data.get('meta', {}).get('count', 0)
    print(f"   (Searching {count:,} samples...)")
    
    results = []
    
    if semantic_filter:
        s_key, s_val = semantic_filter
        for fpath in files:
            ftags = tags_db.get(fpath, {})
            # Check match
            if s_key in ftags and str(ftags[s_key]) == s_val:
                results.append(fpath)
            elif s_key == 'type' and s_val in str(ftags.get('type', '')): # Loose match for type
                results.append(fpath)
    else:
        # Standard Text Search
        q_lower = query.lower()
        results = [f for f in files if q_lower in f.lower()]
    
    if not results:
        print("❌ No matches found.")
    else:
        print(f"✅ Found {len(results)} matches:\n")
        for i, path in enumerate(results[:20]):
            ftags = tags_db.get(path)
            meta_str = ""
            if ftags:
                meta_str = f"{YELLOW}[{ftags.get('bpm', '?')}bpm {ftags.get('key', '')} {ftags.get('type', '')}]{RESET} "
            
            print(f"  {meta_str}{path}")
            
        if len(results) > 20:
             print(f"\n...and {len(results)-20} more.")
             
    print(f"\n{GREEN}Tip: Use Option 4 (Fetch) to materialise.{RESET}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Search term")
    args = parser.parse_args()
    search_oracle(args.query)
