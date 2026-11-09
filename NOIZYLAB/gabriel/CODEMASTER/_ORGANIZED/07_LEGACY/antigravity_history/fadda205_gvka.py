import os
import sys
import datetime

OUTPUT_FILE = "/Users/m2ultra/NOIZYLAB/probe_results.txt"

def log(msg):
    with open(OUTPUT_FILE, "a") as f:
        f.write(msg + "\n")

def string_extraction(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read(4000) # Read header
            # Simple simulation of 'strings' - valid ASCII, length > 4
            result = ""
            current_string = ""
            for byte in data:
                char = chr(byte)
                if 32 <= byte <= 126: # Printable
                    current_string += char
                else:
                    if len(current_string) >= 4:
                        result += current_string + " | "
                    current_string = ""
            return result[:500] # Return first 500 chars of strings
    except Exception as e:
        return f"Error reading: {e}"

def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    log(f"Probe started at {datetime.datetime.now()}")
    log(f"CWD: {os.getcwd()}")
    
    target_dir = "/Volumes/JOE/NKI"
    if not os.path.exists(target_dir):
        log(f"Target dir {target_dir} NOT FOUND")
        return

    log(f"Scanning {target_dir}...")
    
    count = 0
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            if name.endswith(".nki"):
                path = os.path.join(root, name)
                log(f"Checking: {path}")
                strings_found = string_extraction(path)
                log(f"Strings: {strings_found}")
                count += 1
                if count >= 5: # Just check 5 files
                    log("Limit reached. Exiting.")
                    return

if __name__ == "__main__":
    main()
