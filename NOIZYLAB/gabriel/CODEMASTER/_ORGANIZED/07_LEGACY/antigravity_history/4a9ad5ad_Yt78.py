import sys
import importlib

print(">>> VERIFYING NOIZYLAB ENVIRONMENT...")
print(f"Python: {sys.version}")

libraries = [
    "anthropic", 
    "librosa", 
    "spleeter", 
    "whisper", 
    "numpy", 
    "pandas",
    "moviepy"
]

failed = []

for lib in libraries:
    try:
        module = importlib.import_module(lib)
        version = getattr(module, "__version__", "unknown")
        print(f"  [OK] {lib} ({version})")
    except ImportError as e:
        print(f"  [ERROR] {lib}: {e}")
        failed.append(lib)
    except Exception as e:
        print(f"  [ERROR] {lib}: {e}")
        failed.append(lib)

if failed:
    print(f"\n>>> VERIFICATION FAILED. Issues with: {', '.join(failed)}")
    sys.exit(1)
else:
    print("\n>>> ENVIRONMENT VERIFIED. ALL SYSTEMS GO.")
    sys.exit(0)
