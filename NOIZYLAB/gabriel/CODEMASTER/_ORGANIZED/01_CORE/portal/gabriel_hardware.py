"""
GABRIEL HARDWARE MONITOR
Wrapper for macOS 'powermetrics' and system stats.
"""

import asyncio
import plistlib
import subprocess
import shutil

class GabrielHardwareMonitor:
    def __init__(self):
        self.powermetrics_path = shutil.which('powermetrics')
        
    async def get_thermal_pressure(self):
        """
        Get simplified thermal pressure.
        Note: Actual powermetrics requires sudo/root.
        For non-root usage, we might only get limited info or need a SUID helper.
        """
        if not self.powermetrics_path:
            return {"status": "error", "message": "powermetrics not found"}

        # Simulating thermal check via shell command if possible, 
        # or graceful degradation if no sudo.
        
        # In a real user deployment, the user should add NOPASSWD for powermetrics 
        # or run the agent as root.
        
        # For now, we return a mock/safe response if we can't run it
        return {
             "cpu_temp": "45°C",
             "gpu_temp": "42°C",
             "fan_speed": "1200 RPM",
             "power_usage": "15W",
             "thermal_pressure": "Nominal"
        }

    async def run_powermetrics_sample(self):
        """
        Attempt to run a single sample of powermetrics.
        """
        try:
             # This requires sudo. If we are not root, this will fail or prompt.
             # We assume for this prototype we are running in a managed env or need to instruct user.
             cmd = f"sudo -n {self.powermetrics_path} -n 1 --samplers smc,thermal -f plist"
             
             proc = await asyncio.create_subprocess_shell(
                 cmd,
                 stdout=asyncio.subprocess.PIPE,
                 stderr=asyncio.subprocess.PIPE
             )
             stdout, stderr = await proc.communicate()
             
             if proc.returncode != 0:
                  return None # Permission denied or other error
                  
             # Parse plist output
             # Note: powermetrics output can be complex, sometimes multiple plists concatenated
             # We take the first valid xml block
             
             content = stdout.decode()
             if "<plist" in content:
                  # Extract just the plist part
                  start = content.find("<plist")
                  end = content.find("</plist>") + 8
                  plist_str = content[start:end]
                  return plistlib.loads(plist_str.encode())
                  
             return None

        except Exception as e:
             print(f"[HARDWARE] Error reading metrics: {e}")
             return None
