#!/usr/bin/env python3
"""
GABRIEL BRAIN - GOD MODE MUSIC KNOWLEDGE INTERFACE
Protocol: ZERO LATENCY
Created by: CB_01
Date: December 2025
"""

import argparse
import re
import sys
import random
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
            print(f"CRITICAL ERROR: Knowledge Base not found at {self.path}")
            sys.exit(1)
        
        with open(self.path, "r", encoding="utf-8") as f:
            self.raw_content = f.read()
            
        self.parse_entries()
        self.parse_recipes()

    def parse_entries(self):
        # Regex to find major timeline entries
        # Looks for "### **YEAR - Title**" blocks
        entry_pattern = r"### \*\*(.*?)\*\*(.*?)(?=###|\Z)"
        matches = re.finditer(entry_pattern, self.raw_content, re.DOTALL)
        
        for match in matches:
            header = match.group(1).strip()
            body = match.group(2).strip()
            
            # Extract God Mode Mapping
            mapping_match = re.search(r"\*\*GOD MODE MAPPING:\*\*\s*(.*)", body)
            mapping = mapping_match.group(1).strip() if mapping_match else None
            
            self.entries.append({
                "header": header,
                "body": body,
                "mapping": mapping
            })

    def parse_recipes(self):
        # Extract God Mode Recipes
        recipe_pattern = r"### \*\*RECIPE(.*?)\*\*(.*?)(?=###|\Z)"
        matches = re.finditer(recipe_pattern, self.raw_content.split("GOD MODE RECIPES")[1] if "GOD MODE RECIPES" in self.raw_content else "", re.DOTALL)
        
        for match in matches:
            title = match.group(1).strip()
            body = match.group(2).strip()
            self.recipes.append({
                "title": title,
                "body": body
            })

    def search(self, query):
        print(f"\n🧠 GABRIEL SEARCH: '{query}'\n" + "="*40)
        hits = 0
        for entry in self.entries:
            if query.lower() in entry["header"].lower() or query.lower() in entry["body"].lower():
                print(f"\n🔍 FOUND: {entry['header']}")
                
                # Highlight Mapping
                if entry["mapping"]:
                    print(f"⚡ ZERO LATENCY MAPPING: {entry['mapping']}")
                
                # Show key stats if relevant
                if "Core Tech" in entry["body"]:
                    tech = re.search(r"\*\*Core Tech:\*\*\s*(.*)", entry["body"])
                    if tech: print(f"🛠️  TECH: {tech.group(1)}")
                
                if "Sonic Signature" in entry["body"]:
                    sig = re.search(r"\*\*Sonic Signature:\*\*\s*(.*)", entry["body"])
                    if sig: print(f"🔊 SIGNATURE: {sig.group(1)}")
                    
                hits += 1
        
        if hits == 0:
            print("No matches found in God Mode Database.")
        else:
            print(f"\nTotal Hits: {hits}")

    def get_recipe(self, query):
        print(f"\n🧪 GOD MODE RECIPES MATCHING: '{query}'\n" + "="*40)
        hits = 0
        for recipe in self.recipes:
            if query.lower() in recipe["title"].lower() or query.lower() in recipe["body"].lower():
                print(f"\n📜 RECIPE{recipe['title']}")
                print("-" * 20)
                print(recipe["body"])
                hits += 1
        
        if hits == 0:
            print("No recipes found.")

    def random_insight(self):
        if not self.entries:
            return
        entry = random.choice(self.entries)
        print(f"\n🎲 RANDOM GOD MODE INSIGHT:\n" + "="*40)
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
        brain.search(args.mapping) # Search covers mapping
    elif args.recipe:
        brain.get_recipe(args.recipe)
    elif args.random:
        brain.random_insight()
    else:
        # Default to random if no args
        print("Usage: gabriel_brain.py [--search term] [--recipe era] [--random]")
        brain.random_insight()

if __name__ == "__main__":
    main()
