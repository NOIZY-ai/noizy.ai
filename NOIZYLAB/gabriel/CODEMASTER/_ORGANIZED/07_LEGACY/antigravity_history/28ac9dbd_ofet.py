import asyncio
import sys
import os

sys.path.append("/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_UNIFIED/core")
from gabriel_infinity import NativeBridge

async def run_test():
    print("🧪 TESTING METAL BENCHMARK...")
    bridge = NativeBridge()
    if not bridge.use_metal:
        print("❌ Metal Bridge Offline")
        return

    print("   Running Matrix Multiplication (4096 x 4096)...")
    result = await bridge.run_benchmark()
    print(f"   📊 SCORE: {result}")
    
    if "TFLOPS" in result:
        print("\n✅ BENCHMARK PASSED. M2 ULTRA IS SCREAMING.")
    else:
        print("\n❌ BENCHMARK FAILED.")

if __name__ == "__main__":
    asyncio.run(run_test())
