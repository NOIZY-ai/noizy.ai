import os

DOCS_DIR = "docs"
HEADER = """# ⚡ NOIZYLAB GOD MODE SYSTEM
**PROTOCOL:** ZERO LATENCY | **AUTHORITY:** SHIRL & ENGR

> [!IMPORTANT]
> **SYSTEM STATUS:** GOD MODE ACTIVE.
> **INSTRUCTION:** ADHERE TO ZERO LATENCY & PREDICTIVE ACTIONS.

"""

def is_relevant(filename):
    # Filter for markdown files, excluding those we've already handled manually or are effectively receipts/logs
    if not filename.endswith(".md"):
        return False
    if filename.startswith("CB_01_MASTER"): return False # Already done
    if filename.startswith("UNIVERSAL_GOD"): return False # Is the header
    if filename.startswith("GABRIEL"): return False # Already done
    if filename.startswith("LIFELUV"): return False # Already done
    if "LOG" in filename: return False
    return True

count = 0
for filename in os.listdir(DOCS_DIR):
    if is_relevant(filename):
        path = os.path.join(DOCS_DIR, filename)
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            # Check if already upgraded to avoid duplication
            if "GOD MODE SYSTEM" in content or "ZERO LATENCY" in content[:200]:
                continue
                
            new_content = HEADER + content
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"⚡ Upgraded: {filename}")
            count += 1
        except Exception as e:
            print(f"❌ Failed: {filename} - {e}")

print(f"✅ GOD MODE SWEEP COMPLETE. Upgraded {count} files.")
