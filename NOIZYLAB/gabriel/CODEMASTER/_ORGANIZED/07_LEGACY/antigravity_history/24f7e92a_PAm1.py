import os
import json
import datetime
import argparse
from pathlib import Path
from openai import OpenAI

# CONFIG
MEMCELL_PATH = Path("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL/memcell_db.json")
API_KEY = os.getenv("OPENAI_API_KEY") # User must set this

def load_memcell():
    if not MEMCELL_PATH.exists(): return []
    with open(MEMCELL_PATH) as f:
        return json.load(f)

def find_similar_memcells(query, db, top_n=3):
    # Simple Jaccard/Keyword similarity for local prototype
    # In production, use Vector DB (e.g., Chroma/FAISS)
    query_words = set(query.lower().split())
    
    scored = []
    for entry in db:
        content = (entry.get('title', '') + " " + entry.get('body', '')).lower()
        content_words = set(content.split())
        if not content_words: continue
        
        score = len(query_words.intersection(content_words)) / len(query_words.union(content_words))
        scored.append((score, entry))
        
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scored[:top_n]]

def scan_intel(intel_text):
    print("👁️ SENTINEL: Scanning Intel...")
    
    # 1. RAG
    db = load_memcell()
    context_docs = find_similar_memcells(intel_text, db)
    context_str = "\n".join([f"- [{doc['id']}] {doc['title']}: {doc['body'][:100]}..." for doc in context_docs])
    
    # 2. AI Analysis
    client = OpenAI(api_key=API_KEY)
    
    system_prompt = """You are GABRIEL:SENTINEL.
Input: raw intel.
Task:
1. Extract signals (threats/opportunities) and rank by impact x urgency.
2. Compare to memory context provided.
3. Output JSON only.

Rules:
* No speculation without labeling UNVERIFIED.
* If input is noisy, summarize only evidence.
* Return strict JSON format."""

    user_prompt = f"""
MEMORY CONTEXT:
{context_str}

RAW INTEL:
{intel_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    
    # 3. Output
    print(json.dumps(result, indent=2))
    
    # 4. Upsert Logic (Mocked)
    if result.get('memcell_upserts'):
        print(f"\n>> SENTINEL: Proposing {len(result['memcell_upserts'])} new MemCells to Ingest Queue.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_source", help="Text string or file path")
    args = parser.parse_args()
    
    content = args.input_source
    if os.path.exists(content):
        with open(content) as f:
            content = f.read()
            
    scan_intel(content)
