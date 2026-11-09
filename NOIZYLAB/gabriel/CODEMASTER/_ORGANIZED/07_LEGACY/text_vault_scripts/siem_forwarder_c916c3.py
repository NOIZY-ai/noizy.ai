#!/usr/bin/env python3
"""
siem_forwarder.py
Forward audit events to SIEM endpoint with signing and checksums
"""

import json
import os
import argparse
import requests
import hashlib
import hmac
import sys
from datetime import datetime, timezone
from pathlib import Path

SIEM_ENDPOINT = os.environ.get("SIEM_ENDPOINT")
SIEM_API_KEY = os.environ.get("SIEM_API_KEY")
SIGNING_KEY = os.environ.get("AUDIT_SIGNING_KEY", "")

def compute_checksum(data: bytes) -> str:
    """Compute SHA256 checksum."""
    return hashlib.sha256(data).hexdigest()

def sign_payload(payload: bytes, key: str) -> str:
    """Sign payload with HMAC-SHA256."""
    if not key:
        return ""
    return hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()

def create_audit_event(event_type: str, data: dict, org: str) -> dict:
    """Create a structured audit event."""
    return {
        "event_id": hashlib.sha256(f"{datetime.now().isoformat()}{event_type}".encode()).hexdigest()[:16],
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "organization": org,
        "source": "noizylab-offboarder",
        "version": "1.0.0",
        "data": data
    }

def forward_to_siem(event: dict) -> tuple[bool, str]:
    """Forward event to SIEM endpoint."""
    if not SIEM_ENDPOINT:
        return False, "SIEM_ENDPOINT not configured"
    
    payload = json.dumps(event).encode()
    checksum = compute_checksum(payload)
    signature = sign_payload(payload, SIGNING_KEY)
    
    headers = {
        "Content-Type": "application/json",
        "X-Checksum-SHA256": checksum,
        "X-Signature-HMAC": signature,
        "X-Event-Type": event.get("event_type", "unknown"),
        "X-Source": "noizylab-offboarder"
    }
    
    if SIEM_API_KEY:
        headers["Authorization"] = f"Bearer {SIEM_API_KEY}"
    
    try:
        r = requests.post(SIEM_ENDPOINT, headers=headers, data=payload, timeout=30)
        return r.status_code in [200, 201, 202], r.text
    except Exception as e:
        return False, str(e)

def process_audit_file(filepath: str, org: str) -> list:
    """Process an audit file and create events."""
    with open(filepath) as f:
        data = json.load(f)
    
    events = []
    
    # Determine event type from filename
    filename = Path(filepath).stem
    
    if "execution" in filename or "audit" in filename:
        # Execution log - create events for each action
        for action in data.get("actions", []):
            event = create_audit_event(
                event_type="github.offboard.action",
                data={
                    "action_type": action.get("type") or action.get("action"),
                    "target_user": action.get("user"),
                    "target_resource": action.get("target"),
                    "result": action.get("status") or action.get("result"),
                    "timestamp": action.get("timestamp")
                },
                org=org
            )
            events.append(event)
        
        # Summary event
        if data.get("summary"):
            events.append(create_audit_event(
                event_type="github.offboard.summary",
                data=data["summary"],
                org=org
            ))
    
    elif "plan" in filename:
        # Plan created event
        events.append(create_audit_event(
            event_type="github.offboard.plan_created",
            data={
                "preserve_count": len(data.get("preserve", [])),
                "remove_count": len(data.get("remove", [])),
                "review_count": len(data.get("review", [])),
                "action_count": len(data.get("actions", []))
            },
            org=org
        ))
    
    elif "inventory" in filename:
        # Inventory collected event
        events.append(create_audit_event(
            event_type="github.offboard.inventory_collected",
            data=data.get("summary", {}),
            org=org
        ))
    
    return events

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--files", nargs="+", required=True, help="Audit files to forward")
    p.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"))
    p.add_argument("--out", default="artifacts/siem_forward_log.json")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    
    print("═" * 60)
    print("SIEM FORWARDER")
    print(f"Endpoint: {SIEM_ENDPOINT or 'NOT CONFIGURED'}")
    print(f"Files: {len(args.files)}")
    print(f"Mode: {'🔵 DRY RUN' if args.dry_run else '🟢 LIVE'}")
    print("═" * 60)
    
    log = {
        "forwarded_at": datetime.now(timezone.utc).isoformat(),
        "org": args.org,
        "dry_run": args.dry_run,
        "files_processed": [],
        "events_created": 0,
        "events_forwarded": 0,
        "events_failed": 0,
        "events": []
    }
    
    for filepath in args.files:
        if not Path(filepath).exists():
            print(f"⚠️ File not found: {filepath}")
            continue
        
        print(f"\nProcessing: {filepath}")
        events = process_audit_file(filepath, args.org)
        log["files_processed"].append(filepath)
        log["events_created"] += len(events)
        
        for event in events:
            # Compute checksum
            payload = json.dumps(event).encode()
            event["_checksum"] = compute_checksum(payload)
            event["_signature"] = sign_payload(payload, SIGNING_KEY)
            
            if args.dry_run:
                print(f"  [DRY RUN] Would forward: {event['event_type']}")
                log["events"].append({**event, "forward_status": "dry_run"})
            else:
                success, msg = forward_to_siem(event)
                status = "success" if success else "failed"
                print(f"  {'✅' if success else '❌'} {event['event_type']}: {status}")
                
                log["events"].append({**event, "forward_status": status, "forward_message": msg if not success else None})
                
                if success:
                    log["events_forwarded"] += 1
                else:
                    log["events_failed"] += 1
    
    # Save log
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(log, f, indent=2)
    
    print("\n" + "═" * 60)
    print(f"Files processed: {len(log['files_processed'])}")
    print(f"Events created: {log['events_created']}")
    print(f"Events forwarded: {log['events_forwarded']}")
    print(f"Events failed: {log['events_failed']}")
    print(f"Log: {args.out}")

if __name__ == "__main__":
    main()
