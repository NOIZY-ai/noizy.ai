import os
import shutil
import sys

# We report back to the volume we can read
REPORT_FILE = "/Volumes/JOE/NKI/probe_result.txt"
SOURCE_DIR = "/Volumes/JOE/NKI"
LOCAL_TEST_DIR = os.path.expanduser("~/Desktop/TURBO_LOCAL_TEST")

def report(msg):
    print(msg)
    try:
        with open(REPORT_FILE, "a") as f:
            f.write(msg + "\n")
    except: pass

def main():
    try:
        if os.path.exists(REPORT_FILE): os.remove(REPORT_FILE)
    except: pass

    report("--- TURBO LOCAL PROBE ---")
    
    # 1. Create Local Dir
    try:
        report(f"1. Creating {LOCAL_TEST_DIR}...")
        if os.path.exists(LOCAL_TEST_DIR):
            shutil.rmtree(LOCAL_TEST_DIR)
        os.makedirs(LOCAL_TEST_DIR, exist_ok=True)
        report("   [OK] Directory Created.")
    except Exception as e:
        report(f"   [FAIL] Mkdir failed: {e}")
        return

    # 2. Copy a file
    try:
        # Find a .nki to copy
        candidate = None
        for f in os.listdir(SOURCE_DIR):
            if f.endswith('.nki'):
                candidate = os.path.join(SOURCE_DIR, f)
                break
        
        if not candidate:
            report("   [FAIL] No NKI file found to test copy.")
            return

        report(f"2. Copying {os.path.basename(candidate)}...")
        dst = os.path.join(LOCAL_TEST_DIR, "test_file.nki")
        shutil.copy2(candidate, dst)
        report("   [OK] Copy successful.")
        
    except Exception as e:
        report(f"   [FAIL] Copy failed: {e}")
        return

    # 3. Modify (Rename) - The Test of Execution
    try:
        report(f"3. Testing Modification (Rename)...")
        dst_renamed = os.path.join(LOCAL_TEST_DIR, "renamed_successful.nki")
        os.rename(dst, dst_renamed)
        report("   [OK] Rename successful.")
    except Exception as e:
        report(f"   [FAIL] Rename failed: {e}")
        return

    report("--- RESULT: LOCAL EXECUTION IS VIABLE ---")

if __name__ == "__main__":
    main()
