import os
import sys

# Output to current directory (workspace)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "probe_results.txt")

def log(msg):
    try:
        with open(OUTPUT_FILE, "a") as f:
            f.write(str(msg) + "\n")
    except Exception as e:
        pass # Can't log if logging fails

def extract_strings(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read(16000) # Read first 16kb
            
        # Extract ASCII sequences > 4 chars
        result = []
        current = ""
        for b in data:
            if 32 <= b <= 126:
                current += chr(b)
            else:
                if len(current) > 4:
                    # Filter basic noise
                    if "Native Instruments" not in current and "Kontakt" not in current:
                        result.append(current)
                current = ""
        return result[:20] # Return top 20
    except Exception as e:
        return [f"Error: {e}"]

def main():
    if os.path.exists(OUTPUT_FILE):
        try:
            os.remove(OUTPUT_FILE)
        except:
            pass

    log("Probe V2 Starting...")
    root_dir = os.path.dirname(__file__)
    log(f"Scanning root: {root_dir}")
    
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(".nki"):
                full_path = os.path.join(root, file)
                log(f"Inspecting: {file}")
                strings = extract_strings(full_path)
                log(f"Strings found: {strings}")
                count += 1
                if count >= 5:
                    log("Limit 5 reached.")
                    return

if __name__ == "__main__":
    main()
