import asyncio
import sys
import os

# Add the core directory to sys.path so we can import gabriel_infinity
sys.path.append("/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_UNIFIED/core")

from gabriel_infinity import NativeBridge

async def test():
    print("🧪 TESTING NATIVE BRIDGE INTEGRATION...")
    bridge = NativeBridge()
    
    print(f"Target Metal Bin: {bridge.metal_bin}")
    print(f"Target Sentry Bin: {bridge.sentry_bin}")
    
    # Check Metal
    metal_status = await bridge.check_metal_status()
    print(f"Metal Status: {'✅ ONLINE' if metal_status else '❌ OFFLINE'}")
    
    # Check Sentry (We just check existence here as launching it is blocking/long-running)
    sentry_exists = bridge.sentry_bin.exists()
    print(f"Sentry Binary: {'✅ FOUND' if sentry_exists else '❌ MISSING'}")

    if metal_status and sentry_exists:
        print("\n🎉 INTEGRATION VERIFIED. SYSTEM IS GO.")
    else:
        print("\n⚠️ INTEGRATION ISSUES DETECTED.")

if __name__ == "__main__":
    asyncio.run(test())
