# 🤖 SYSTEM FILE: demonstrate_god_mode.py
# Optimized by Healer Drone

import sys
import os
sys.path.append(os.getcwd())
from AI_INTEGRATION_SUITE.MEMCELL_CORE import MemCellCore

def demonstrate_god_mode():
    mc = MemCellCore()
    print("\n⚡ EXECUTING GOD MODE TRACKING DEMO...\n")

    # 1. Add a complex memory
    print("[ACTION] Adding Memory with Subject & Overlap...")
    mem_obj = mc.add_memory(
        content="Optimized all 1125 system prompts to Zero Latency Protocols.",
        type="ACTION",
        topic="System Optimization",
        group="God Mode",
        author="ENGR_KEITH",
        subject="Global Prompt Upgrade",
        overlap=["Docs", "Scripts", "Brain"]
    )
    target_id = mem_obj['id']

    # 2. Retrieve and show it
    print(f"\n[SUCCESS] Memory Added. ID: {target_id}")
    print("[VERIFICATION] Retrieving from Database...\n")

    # Force reload to prove persistence
    mc_verify = MemCellCore()
    memories = mc_verify.search_memories("System Optimization")

    for m in memories:
        if m['id'] == target_id:
            print("--------------------------------------------------")
            print(f"🔥 GOD MODE MEMORY DETECTED 🔥")
            print(f"   Shape:    {m['type']} // {m['topic']}")
            print(f"   Author:   {m['author']}")
            print(f"   Subject:  {m['subject']}")
            print(f"   Overlap:  {m['overlap']}")
            print(f"   Content:  {m['content']}")
            print(f"   Time:     {m['timestamp']} (Precision: {m.get('god_mode_timestamp')})")
            print("--------------------------------------------------")

if __name__ == "__main__":
    demonstrate_god_mode()
