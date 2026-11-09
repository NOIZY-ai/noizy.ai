#!/usr/bin/env python3
"""
GABRIEL BRAIN - GOD MODE MUSIC KNOWLEDGE INTERFACE
Protocol: ZERO LATENCY | AI: ENHANCED (NLP/FUZZY DETECT)
Created by: CB_01
Date: December 2025
"""

import argparse
import re
import sys
import random
import difflib
from pathlib import Path

# Configuration
KNOWLEDGE_BASE_PATH = Path("CB_01_COMPLETE_MUSIC_PRODUCTION_KNOWLEDGE_GOD_MODE.md")

class GabrielBrain:
    def __init__(self, path):
        self.path = path
        self.raw_content = ""
        self.entries = []
        self.recipes = []
        self.load_knowledge()

    def load_knowledge(self):
        if not self.path.exists():
            # Fallback for when running from different relative paths in the unified structure
            if (Path("../MUSIC_INTELLIGENCE") / self.path.name).exists():
                self.path = Path("../MUSIC_INTELLIGENCE") / self.path.name
            elif (Path("PROJECTS_MASTER/MUSIC_INTELLIGENCE") / self.path.name).exists():
                self.path = Path("PROJECTS_MASTER/MUSIC_INTELLIGENCE") / self.path.name
            else:
                print(f"CRITICAL ERROR: Knowledge Base not found at {self.path}")
                sys.exit(1)
        
        with open(self.path, "r", encoding="utf-8") as f:
            self.raw_content = f.read()
            
        self.parse_entries()
        self.parse_recipes()

    def parse_entries(self):
        # Regex to find major timeline entries
        entry_pattern = r"### \*\*(.*?)\*\*(.*?)(?=###|\Z)"
        matches = re.finditer(entry_pattern, self.raw_content, re.DOTALL)
        
        for match in matches:
            header = match.group(1).strip()
            body = match.group(2).strip()
            
            # Extract God Mode Mapping
            mapping_match = re.search(r"\*\*GOD MODE MAPPING:\*\*\s*(.*)", body)
            mapping = mapping_match.group(1).strip() if mapping_match else None
            
            # Extract Year for context
            year_match = re.search(r"\d{4}", header)
            year = int(year_match.group(0)) if year_match else 0

            self.entries.append({
                "header": header,
                "body": body,
                "mapping": mapping,
                "year": year,
                "search_text": f"{header} {body}".lower()
            })

    def parse_recipes(self):
        # Extract God Mode Recipes
        if "GOD MODE RECIPES" in self.raw_content:
            recipe_section = self.raw_content.split("GOD MODE RECIPES")[1]
            recipe_pattern = r"### \*\*RECIPE(.*?)\*\*(.*?)(?=###|\Z)"
            matches = re.finditer(recipe_pattern, recipe_section, re.DOTALL)
            
            for match in matches:
                title = match.group(1).strip()
                body = match.group(2).strip()
                self.recipes.append({
                    "title": title,
                    "body": body,
                    "search_text": f"{title} {body}".lower()
                })

    def fuzzy_match(self, query, text_list, cutoff=0.6):
        """Find close matches using difflib."""
        return difflib.get_close_matches(query.lower(), text_list, n=3, cutoff=cutoff)

    def analyze_intent(self, query):
        """Determine what the user is looking for (NLP-lite)."""
        query = query.lower()
        if any(w in query for w in ["how to", "make like", "sound like", "recipe", "style of"]):
            return "RECIPE"
        if any(w in query for w in ["replace", "modern", "vst", "plugin", "mapping", "equivalent"]):
            return "MAPPING"
        return "GENERAL"

    def search(self, query):
        intent = self.analyze_intent(query)
        print(f"\n🧠 GABRIEL INTELLIGENCE | DETECTED INTENT: {intent} | QUERY: '{query}'\n" + "="*60)
        
        if intent == "RECIPE":
            self.get_recipe(query)
            return

        hits = 0
        # 1. Exact/Partial Match
        results = [e for e in self.entries if query.lower() in e['search_text']]
        
        # 2. Fuzzy Match logic if no exact results
        if not results:
            all_headers = [e['header'] for e in self.entries]
            fuzzy_hits = self.fuzzy_match(query, all_headers)
            if fuzzy_hits:
                print(f"🤔 Did you mean: {', '.join(fuzzy_hits)}?")
                # Auto-search the best fuzzy match
                results = [e for e in self.entries if fuzzy_hits[0] in e['header'].lower()]

        for entry in results:
            print(f"\n🔍 FOUND: {entry['header']}")
            
            if intent == "MAPPING" or entry["mapping"]:
                print(f"⚡ ZERO LATENCY MAPPING: {entry['mapping'] or 'No direct mapping available'}")
            
            if "Core Tech" in entry["body"]:
                tech = re.search(r"\*\*Core Tech:\*\*\s*(.*)", entry["body"])
                if tech: print(f"🛠️  TECH: {tech.group(1)}")
            
            if "Sonic Signature" in entry["body"]:
                sig = re.search(r"\*\*Sonic Signature:\*\*\s*(.*)", entry["body"])
                if sig: print(f"🔊 SIGNATURE: {sig.group(1)}")
                
            hits += 1
        
        if hits == 0:
            print("No matches found in God Mode Database. Try broadening your term.")
        else:
            print(f"\nTotal Hits: {hits}")

    def get_recipe(self, query):
        print(f"\n🧪 GOD MODE RECIPES MATCHING: '{query}'\n" + "="*60)
        hits = 0
        for recipe in self.recipes:
            if query.lower() in recipe["search_text"]:
                print(f"\n📜 RECIPE{recipe['title']}")
                print("-" * 20)
                print(recipe["body"])
                hits += 1
        
        if hits == 0:
            print("No exact recipe found.")
            # Suggest close recipes?
            print("Tip: Try years like 1982, 1993, 1997, 2012, 2024.")

    def random_insight(self):
        if not self.entries:
            return
        entry = random.choice(self.entries)
        print(f"\n🎲 RANDOM GOD MODE INSIGHT:\n" + "="*60)
        print(f"OBJ: {entry['header']}")
        print(entry['body'].strip())

def main():
    parser = argparse.ArgumentParser(description="Gabriel Brain - God Mode Music Knowledge Interface")
    parser.add_argument("--search", "-s", help="Search the knowledge base")
    parser.add_argument("--recipe", "-r", help="Find a production recipe")
    parser.add_argument("--mapping", "-m", help="Find Modern Mapping for vintage fear")
    parser.add_argument("--random", action="store_true", help="Get a random insight")
    
    args = parser.parse_args()
    
    brain = GabrielBrain(KNOWLEDGE_BASE_PATH)
    
    if args.search:
        brain.search(args.search)
    elif args.mapping:
        # Force mapping intent
        print(f"\n🧠 GABRIEL INTELLIGENCE | MODE: MAPPING ONLY")
        brain.search(f"{args.mapping} mapping") 
    elif args.recipe:
        brain.get_recipe(args.recipe)
    elif args.random:
        brain.random_insight()
    else:
        # Interactive mode if run without args (for the System Core)
        print("Usage: gabriel_brain.py [--search term] [--recipe era] [--random]")
        brain.random_insight()

if __name__ == "__main__":
    main()
