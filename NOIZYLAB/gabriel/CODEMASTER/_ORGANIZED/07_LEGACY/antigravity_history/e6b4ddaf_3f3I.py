#!/usr/bin/env python3
# 🧠 KNOWLEDGE CONDENSER (MC96 INTELLIGENCE LAYER)
# Purpose: "Learn everything and condense it into bullet points!"

import json
import datetime
from pathlib import Path
from collections import defaultdict

# CONFIG
BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "memcell_db.json"
OUTPUT_MD = BASE_DIR / "CONDENSED_WISDOM.md"
OUTPUT_JSON = BASE_DIR / "knowledge_core.json"

class KnowledgeCondenser:
    def __init__(self):
        self.db = []
        self.wisdom = defaultdict(list)
        
    def load_db(self):
        if not DB_PATH.exists():
            print("❌ No Brain Found.")
            return False
            
        with open(DB_PATH, 'r') as f:
            self.db = json.load(f)
        return True
        
    def condense(self):
        print(f"🧠 CONDENSER: Processing {len(self.db)} raw thoughts...")
        
        # 1. Group by Subject
        for m in self.db:
            subj = m.get('subject', 'General')
            content = m.get('content', '').strip()
            reinforce = m.get('reinforcement', 1)
            
            # Simple heuristic: Only keep "worthy" thoughts
            # (In a real system, we'd use embedding similarity here)
            # For now: We keep everything but sort by strength
            self.wisdom[subj].append({
                'content': content,
                'score': reinforce,
                'id': m['id']
            })
            
        # 2. Sort & Filter
        final_wisdom = {}
        for subj, items in self.wisdom.items():
            # Sort by Score (Desc)
            items.sort(key=lambda x: x['score'], reverse=True)
            # Remove exact duplicates
            seen = set()
            unique_items = []
            for i in items:
                if i['content'] not in seen:
                    unique_items.append(i)
                    seen.add(i['content'])
            final_wisdom[subj] = unique_items
            
        self.wisdom = final_wisdom
        
    def publish(self):
        print("📝 PUBLISHING WISDOM...")
        
        # MD Output
        with open(OUTPUT_MD, 'w') as f:
            f.write("# 🧠 MC96 CONDENSED WISDOM\n")
            f.write(f"> **GENERATED**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("> **DIRECTIVE**: Condensed, Bullet-Point Intelligence.\n\n")
            
            for subj, items in sorted(self.wisdom.items()):
                f.write(f"## 🔹 {subj.upper()}\n")
                for i in items:
                    icon = "🔥" if i['score'] > 5 else "🔸" if i['score'] > 2 else "•"
                    f.write(f"{icon} {i['content']}\n")
                f.write("\n")
                
        # JSON Output (For AI RAG)
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(self.wisdom, f, indent=2)
            
        print(f"✅ WISDOM SECURED: {OUTPUT_MD}")

if __name__ == "__main__":
    kc = KnowledgeCondenser()
    if kc.load_db():
        kc.condense()
        kc.publish()
