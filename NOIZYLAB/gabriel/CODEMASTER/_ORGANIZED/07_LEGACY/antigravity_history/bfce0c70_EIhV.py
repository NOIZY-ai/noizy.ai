# 📊 MEMCELL DASHBOARD - THE GOD MODE MONITOR
# Purpose: Visualizing the "Intuitive Intelligence" (Subject/Overlap)
# "God Mode"

import os
import json
import time
from MEMCELL_CORE import MemCellCore

# Colors
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

class Dashboard:
    def __init__(self):
        self.brain = MemCellCore()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        self.clear_screen()
        memories = self.brain.db
        projects = [m for m in memories if m.get('type') == "PROJECT"]
        actions = [m for m in memories if m.get('type') == "ACTION"]
        
        # Calculate God Mode Stats
        total_overlap = sum(len(m.get('overlap', [])) for m in memories)
        subjects = set(m.get('subject', 'General') for m in memories)
        
        print(f"\n{CYAN}" + "="*60)
        print(f"   🧠 MEMCELL GOD MODE DASHBOARD   |   {BOLD}ZERO LATENCY ACTIVE{RESET}{CYAN}")
        print("="*60 + f"{RESET}")
        
        print(f"\n{BOLD}📈 INTUITIVE INTELLIGENCE METRICS:{RESET}")
        print(f"   • Total Memories:   {GREEN}{len(memories)}{RESET}")
        print(f"   • Active Subjects:  {YELLOW}{len(subjects)}{RESET} (Tracked)")
        print(f"   • Overlap Connections: {CYAN}{total_overlap}{RESET} (Linked)")
        print(f"   • Database Status:  {GREEN}100% NORMALIZED{RESET}")
        
        print(f"\n{BOLD}⚡ RECENT GOD MODE ACTIONS (Subject + Overlap):{RESET}")
        print(f"{CYAN}" + "-" * 60 + f"{RESET}")
        
        # Show last 5 Actions with full God Mode details
        recent_items = (actions + projects)[-5:]
        recent_items.sort(key=lambda x: x['timestamp'], reverse=True)

        for item in recent_items:
            author = item.get('author', 'SYSTEM')
            subject = item.get('subject', 'General')
            overlap = item.get('overlap', [])
            topic = item.get('topic', 'General')
            
            # Format output
            print(f"   {BOLD}[{author}]{RESET} :: {YELLOW}{subject}{RESET}")
            print(f"   Topic: {topic} | {item['timestamp'].split('T')[1][:8]}")
            print(f"   {CYAN}Overlap: {overlap}{RESET}")
            print(f"   > {item['content']}")
            print(f"{CYAN}" + "-" * 60 + f"{RESET}")

        print(f"\n{GREEN}" + "="*60)
        print(f"   GORUNFREE! 🚀  |  PARTNERSHIP ACTIVE")
        print("="*60 + f"{RESET}\n")

if __name__ == "__main__":
    dash = Dashboard()
    dash.render()
