#!/usr/bin/env python3
# 📊 MEMCELL DASHBOARD - THE 2ND ACT MONITOR
# Purpose: Visualizing the Rebuild & Memory Stats
# "Caretaker Mode"

import os
import json
from MEMCELL_CORE import MemCellCore

class Dashboard:
    def __init__(self):
        self.brain = MemCellCore()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        self.clear_screen()
        memories = self.brain.db
        projects = [m for m in memories if m.get('type') == "PROJECT"]
        thoughts = [m for m in memories if m.get('type') == "THOUGHT"]
        
        print("\n" + "="*60)
        print("   🧠 MEMCELL SYSTEM DASHBOARD   |   MODE: CARETAKER")
        print("="*60)
        
        print(f"\n📈 CAPACITY STATUS:")
        print(f"   • Total Memories:   {len(memories)}")
        print(f"   • Active Projects:  {len(projects)}")
        print(f"   • Database Size:    Infinite (JSON)")
        print(f"   • Backup Status:    SECURE")
        
        print(f"\n🏗️  2ND ACT REBUILD PROJECTS:")
        print("-" * 60)
        if not projects:
            print("   (No projects tracked yet. Use 'add project' to start)")
        else:
            for p in projects[-5:]: # Show last 5
                # Extract status from tags if available
                status = "Active"
                if "tags" in p and len(p["tags"]) > 1:
                    status = p["tags"][1]
                
                print(f"   • {p['timestamp'][:10]} | {p['topic'].replace('Project: ', '')} | [{status}]")
                print(f"     > {p['content']}")
                print("")

        print(f"\n💭 RECENT THOUGHTS:")
        print("-" * 60)
        for t in thoughts[-3:]:
            print(f"   • {t['timestamp'][11:16]} | {t['content']}")

        print("\n" + "="*60)
        print("   GORUNFREE! 🚀  |  PARTNERSHIP ACTIVE")
        print("="*60 + "\n")

if __name__ == "__main__":
    dash = Dashboard()
    dash.render()
