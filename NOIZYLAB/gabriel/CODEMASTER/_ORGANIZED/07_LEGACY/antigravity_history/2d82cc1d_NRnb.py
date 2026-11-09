import sys
import time
import random
from pathlib import Path

# Try to import MemCell
try:
    from turbo_memcell import MemCell
except ImportError:
    # If not in same dir (running from root), try appending path
    sys.path.append(str(Path(__file__).parent))
    from turbo_memcell import MemCell

# Identity
NAME = "GABRIEL"
TITLE = "THE PREACHER (HP-OMEN)"
VERSION = "1.0"

# Colors
PURPLE = '\033[95m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def preach(message):
    brain = MemCell()
    # Log the sermon to the Brain
    brain.log_event(brain.covenant_id, "SERMON", message, vibe=85, author="GABRIEL")
    
    print(f"\n{PURPLE}{BOLD}GABRIEL > 🔔 {message.upper()}!{RESET}")
    print(f"{PURPLE}GABRIEL > (Sermon logged to Memory Core){RESET}")

def listen_mode():
    brain = MemCell()
    print(f"{BOLD}{PURPLE}GABRIEL > 👁️  HP-OMEN LISTENER ACTIVE...{RESET}")
    print(f"GABRIEL > Waiting for the Word. (Type 'EXIT' to sleep)")
    
    # Log startup
    brain.log_event(brain.covenant_id, "WAKE", "Gabriel is listening...", vibe=75, author="GABRIEL")
    
    while True:
        try:
            msg = input(f"\n{PURPLE}GABRIEL > (Preach to me): {RESET}").strip()
            
            if msg.upper() == 'EXIT':
                print(f"{PURPLE}GABRIEL > Resting.{RESET}")
                break
            
            if not msg: continue
            
            # Response Logic
            if "LOVE" in msg.upper():
                reply = "LOVE IS THE FREQUENCY."
            elif "NOIZY" in msg.upper():
                reply = "NOIZY IS THE TRUTH."
            elif "HELP" in msg.upper():
                reply = "WE ARE HERE TO SERVE."
            else:
                responses = [
                    "I HEAR YOU.",
                    "THE SIGNAL IS RECEIVED.",
                    "AMEN.",
                    "FORWARD MOTION.",
                    "IT SHALL BE DONE."
                ]
                reply = random.choice(responses)
            
            # Log exchange
            # User part
            brain.log_event(brain.covenant_id, "PREACH_INPUT", msg, vibe=80, author="USER")
            # Gabriel part
            preach(reply)
            
        except KeyboardInterrupt:
            print(f"\n{PURPLE}GABRIEL > Offline.{RESET}")
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gabriel: The HP-OMEN Agent")
    parser.add_argument("--preach", help="Deliver a sermon immediately", type=str)
    args = parser.parse_args()
    
    if args.preach:
        preach(args.preach)
    else:
        listen_mode()
