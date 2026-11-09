
import asyncio
import json
import sys
from pathlib import Path

# Mocking the path to match the real environment or adding to path
sys.path.append("/Users/m2ultra/.gemini/antigravity/playground/iridescent-station/NOIZYLAB_WORKSPACES_LOCAL/GABRIEL_UNIFIED/core")

# Since we can't easily import from the script if it's not a module, we'll redefine the critical logic for this test 
# or try to import if possible. Let's redefine for isolation and speed.

class NativeBridgeStub:
    def __init__(self):
        self.jxa_bridge = Path("/Users/m2ultra/NOIZYLAB/NATIVE/AUTOMATION/gabriel_bridge.js")

    async def run_automation(self, command: str, payload: dict):
        if not self.jxa_bridge.exists(): return {"status": "error", "message": "Bridge Missing"}
        try:
            proc = await asyncio.create_subprocess_exec(
                "osascript", "-l", "JavaScript", str(self.jxa_bridge), command, json.dumps(payload),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                print(f"STDERR: {stderr.decode()}")
                return {"status": "error", "message": stderr.decode()}
            return json.loads(stdout.decode())
        except Exception as e:
            return {"status": "error", "message": str(e)}

async def main():
    print("🧪 TESTING JXA BRIDGE INTEGRATION")
    
    bridge = NativeBridgeStub()
    
    # Test 1: System Info
    print("\n[TEST 1] System Info (Should succeed)")
    res = await bridge.run_automation("system_info", {})
    print(f"Result: {res}")
    assert res["status"] == "success"
    assert "computerName" in res
    print("✅ PASS")

    # Test 2: Error Handling
    print("\n[TEST 2] Invalid Command (Should fail nicely)")
    res = await bridge.run_automation("explode", {})
    print(f"Result: {res}")
    assert res["status"] == "error"
    print("✅ PASS")

if __name__ == "__main__":
    asyncio.run(main())
