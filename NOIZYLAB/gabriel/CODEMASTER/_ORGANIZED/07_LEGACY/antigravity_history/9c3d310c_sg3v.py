
import sys
from pathlib import Path
sys.path.append("/Users/m2ultra/.gemini/antigravity/scratch/NOIZYLAB/PROJECTS_MASTER/GABRIEL_CORE/MEMCELL")

from MEMCELL_CORE import MemCellCore

print("🧪 Testing MemCell Integration...")
core = MemCellCore()
print(f"Loaded Core with {len(core.db)} memories.")

if core.graph is None:
    print("❌ GraphRAG NOT loaded.")
    sys.exit(1)

print("✅ GraphRAG loaded.")

# Add a test memory
print("Injecting test memory...")
mem = core.add_memory("The system is crystal smooth.", topic="Optimization", tags=["M2Ultra", "Gabriel"], type="STATUS")
print("Memory added.")

# Check if graph updated
if "ent_" in str(core.graph.graph.nodes):
    print("✅ Graph nodes detected (simplistic check).")
else:
    # Check specific node
    if core.graph.graph.has_node(mem['id']):
         print("✅ Memory Node found in Graph.")
    else:
         print("❌ Memory Node MISSING from Graph.")

print("Test Complete.")
