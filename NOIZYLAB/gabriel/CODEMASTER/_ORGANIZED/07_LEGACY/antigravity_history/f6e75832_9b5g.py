import os

target = "hello_probe.txt"
try:
    with open(target, "w") as f:
        f.write("Probe Successful")
    print(f"Wrote to {target}")
except Exception as e:
    print(f"Failed to write: {e}")
