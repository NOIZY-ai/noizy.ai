#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run(
    ["ls", "-laR", "/Users/rsp_ms/Desktop/MissionControl96"],
    capture_output=True,
    text=True
)

print("📁 MISSIONCONTROL96 CONTENTS:")
print("=" * 80)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("=" * 80)
