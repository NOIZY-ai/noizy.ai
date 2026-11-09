"""
GABRIEL NATIVE KERNEL BRIDGE
Shared Library for Portal and Infinity Core
"""
import asyncio
import subprocess
import orjson
from pathlib import Path

class NativeBridge:
    """Interface to C++/Metal Native Modules (Shared)"""
    def __init__(self, use_metal=True):
        self.metal_bin = Path("/Users/m2ultra/NOIZYLAB/bin/gabriel_metal_proto")
        self.sentry_bin = Path("/Users/m2ultra/NOIZYLAB/bin/gabriel_fsevents")
        self.jxa_bridge = Path("/Users/m2ultra/NOIZYLAB/NATIVE/AUTOMATION/gabriel_bridge.js")
        self.use_metal = use_metal and self.metal_bin.exists()

    async def check_metal_status(self) -> bool:
        """Verifies Metal Core availability"""
        if not self.use_metal: return False
        try:
            # We just run it to see if it executes without error for now
            proc = await asyncio.create_subprocess_exec(
                str(self.metal_bin),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            return proc.returncode == 0
        except Exception as e:
            print(f"[NATIVE] Metal Check Failed: {e}")
            return False

    async def run_benchmark(self) -> str:
        """Executes the Metal Benchmark"""
        if not self.use_metal: return "Metal Offline."
        try:
            proc = await asyncio.create_subprocess_exec(
                str(self.metal_bin), "benchmark",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            output = stdout.decode()
            
            # Parse for TFLOPS
            import re
            match = re.search(r"RESULT_TFLOPS: ([\d\.]+)", output)
            if match:
                return f"{match.group(1)} TFLOPS"
            return "Benchmark failed to produce score."
        except Exception as e:
            return f"Benchmark Error: {e}"

    async def run_automation(self, command: str, payload: dict) -> dict:
        """Executes a JXA Automation Command"""
        if not self.jxa_bridge.exists(): return {"status": "error", "message": "Bridge Missing"}
        try:
            proc = await asyncio.create_subprocess_exec(
                "osascript", "-l", "JavaScript", str(self.jxa_bridge), command, orjson.dumps(payload).decode(),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                print(f"JXA Error: {stderr.decode()}")
                return {"status": "error", "message": stderr.decode()}
            return orjson.loads(stdout.decode())
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def stream_sentry_events(self, watch_path: str):
        """Async Generator: Yields real-time file events from the Sentinel"""
        if not self.sentry_bin.exists():
            print("[NATIVE] Sentinel Binary Missing.")
            return

        print(f"[NATIVE] 🛡️ Sentinel Awakening on: {watch_path}")
        
        process = await asyncio.create_subprocess_exec(
            str(self.sentry_bin), watch_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Read stdout line by line
        while True:
            line = await process.stdout.readline()
            if not line: break
            
            line_str = line.decode().strip()
            if not line_str: continue
            
            # Parse JSON
            try:
                if line_str.startswith("{"):
                    yield orjson.loads(line_str)
                else:
                    # Log initialization messages
                    print(line_str) 
            except Exception as e:
                print(f"[NATIVE] Sentinel Parse Error: {e} | Raw: {line_str}")

    def launch_sentry(self, watch_path: str):
        """Legacy: Spawns the monitor (blocking/popen) - Deprecated for async stream"""
        if not self.sentry_bin.exists(): return None
        print(f"[NATIVE] Launching Sentry (Legacy) on {watch_path}")
        return subprocess.Popen(
            [str(self.sentry_bin), watch_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
