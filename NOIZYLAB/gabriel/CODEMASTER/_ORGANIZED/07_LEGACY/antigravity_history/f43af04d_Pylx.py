import os

DOCS_DIR = "docs"
HEADER = """# ⚡ NOIZYLAB GOD MODE SYSTEM
**PROTOCOL:** ZERO LATENCY | **AUTHORITY:** SHIRL & ENGR

> [!IMPORTANT]
> **SYSTEM STATUS:** GOD MODE ACTIVE.
> **INSTRUCTION:** ADHERE TO ZERO LATENCY & PREDICTIVE ACTIONS.

"""

TARGETS = [
    "GABRIEL_PYTHON_SETUP.md",
    "LIFELUV_MASTER_PLAN.md",
    "LIFELUV-Flow-Engine.md",
    "GABRIEL_AVATAR_SYSTEM.md",
    "LIFELUV_ENGR_TACTILE_COMPLETE.md"
]

print("⚡ INJECTING FINAL GOD MODE HEADERS...")

for filename in TARGETS:
    path = os.path.join(DOCS_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        
        # Avoid double header if it exists but wasn't detected due to whitespace or something
        if "GOD MODE SYSTEM" in content[:200]:
            print(f"⚠️  Skipping {filename} (Header seems present)")
            continue
            
        new_content = HEADER + content
        with open(path, 'w') as f:
            f.write(new_content)
        print(f"✅ Fixed: {filename}")
    else:
        print(f"❌ File not found: {filename}")

print("🔥 FINAL SWEEP COMPLETE.")
