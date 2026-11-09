import json
import datetime
import os
import argparse

MEMCELL_DB = "/Users/m2ultra/.gemini/antigravity/brain/7ce086fd-9c9f-435a-9136-8deed85eaf0f/MEMCELL_LOG.jsonl"

def log_memcell(subject, overlap, persona="OMNISCIENT", mode="EXECUTION"):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "subject": subject,
        "overlap": overlap,
        "persona": persona,
        "mode": mode
    }
    
    with open(MEMCELL_DB, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    print(f"MemCell Logged: [{entry['timestamp']}] {subject} | {overlap}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MemCell Logger")
    parser.add_argument("--subject", required=True, help="Core Subject Matter")
    parser.add_argument("--overlap", required=True, help="Overlapping tasks/context")
    parser.add_argument("--persona", default="OMNISCIENT", help="Active Persona (Shirl/Engr)")
    parser.add_argument("--mode", default="EXECUTION", help="Current Mode")
    
    args = parser.parse_args()
    log_memcell(args.subject, args.overlap, args.persona, args.mode)
