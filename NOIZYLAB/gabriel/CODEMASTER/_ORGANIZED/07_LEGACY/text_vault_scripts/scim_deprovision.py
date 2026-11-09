#!/usr/bin/env python3
"""
scim_deprovision.py
Deprovision users in IdP via SCIM before GitHub removal
"""

import json
import os
import argparse
import requests
import sys
from datetime import datetime, timezone

SCIM_ENDPOINT = os.environ.get("SCIM_ENDPOINT")
SCIM_TOKEN = os.environ.get("SCIM_TOKEN")
IDP_WEBHOOK = os.environ.get("IDP_WEBHOOK")
IDP_WEBHOOK_SECRET = os.environ.get("IDP_WEBHOOK_SECRET")

def scim_get_user(email: str) -> dict | None:
    """Get user from SCIM directory."""
    if not SCIM_ENDPOINT or not SCIM_TOKEN:
        return None
    
    headers = {
        "Authorization": f"Bearer {SCIM_TOKEN}",
        "Content-Type": "application/scim+json"
    }
    
    # SCIM filter query
    filter_query = f'emails[value eq "{email}"]'
    
    try:
        r = requests.get(
            f"{SCIM_ENDPOINT}/Users",
            headers=headers,
            params={"filter": filter_query},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            resources = data.get("Resources", [])
            return resources[0] if resources else None
    except:
        pass
    
    return None

def scim_deactivate_user(user_id: str) -> tuple[bool, str]:
    """Deactivate user via SCIM PATCH."""
    if not SCIM_ENDPOINT or not SCIM_TOKEN:
        return False, "SCIM not configured"
    
    headers = {
        "Authorization": f"Bearer {SCIM_TOKEN}",
        "Content-Type": "application/scim+json"
    }
    
    payload = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [
            {
                "op": "replace",
                "path": "active",
                "value": False
            }
        ]
    }
    
    try:
        r = requests.patch(
            f"{SCIM_ENDPOINT}/Users/{user_id}",
            headers=headers,
            json=payload,
            timeout=30
        )
        return r.status_code in [200, 204], r.text
    except Exception as e:
        return False, str(e)

def send_idp_webhook(action: str, user: dict) -> tuple[bool, str]:
    """Send webhook to IdP for custom processing."""
    if not IDP_WEBHOOK:
        return False, "IDP_WEBHOOK not configured"
    
    import hmac
    import hashlib
    
    payload = {
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "source": "noizylab-offboarder"
    }
    
    payload_bytes = json.dumps(payload).encode()
    
    headers = {"Content-Type": "application/json"}
    
    if IDP_WEBHOOK_SECRET:
        signature = hmac.new(
            IDP_WEBHOOK_SECRET.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()
        headers["X-Signature-SHA256"] = signature
    
    try:
        r = requests.post(IDP_WEBHOOK, headers=headers, data=payload_bytes, timeout=30)
        return r.status_code in [200, 201, 202], r.text
    except Exception as e:
        return False, str(e)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True, help="Removal plan JSON")
    p.add_argument("--out", default="artifacts/scim_deprovision_log.json")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--webhook-only", action="store_true", help="Only send webhook, no SCIM")
    args = p.parse_args()
    
    plan = json.load(open(args.plan))
    
    print("═" * 60)
    print("SCIM/IDP DEPROVISIONING")
    print(f"SCIM Endpoint: {SCIM_ENDPOINT or 'NOT CONFIGURED'}")
    print(f"IDP Webhook: {IDP_WEBHOOK or 'NOT CONFIGURED'}")
    print(f"Mode: {'🔵 DRY RUN' if args.dry_run else '🟢 LIVE'}")
    print("═" * 60)
    
    log = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "scim_actions": [],
        "webhook_actions": []
    }
    
    for entry in plan.get("remove", []):
        login = entry.get("login")
        email = entry.get("email")
        
        print(f"\nProcessing: {login} ({email or 'no email'})")
        
        # SCIM deprovisioning
        if not args.webhook_only and email and SCIM_ENDPOINT:
            if args.dry_run:
                print(f"  [DRY RUN] Would deactivate in SCIM")
                log["scim_actions"].append({
                    "user": login,
                    "email": email,
                    "status": "dry_run"
                })
            else:
                scim_user = scim_get_user(email)
                if scim_user:
                    user_id = scim_user.get("id")
                    success, msg = scim_deactivate_user(user_id)
                    status = "success" if success else "failed"
                    print(f"  SCIM deactivate: {'✅' if success else '❌'}")
                    log["scim_actions"].append({
                        "user": login,
                        "email": email,
                        "scim_id": user_id,
                        "status": status,
                        "message": msg if not success else None
                    })
                else:
                    print(f"  SCIM: User not found")
                    log["scim_actions"].append({
                        "user": login,
                        "email": email,
                        "status": "not_found"
                    })
        
        # IDP Webhook
        if IDP_WEBHOOK:
            user_data = {"login": login, "email": email}
            
            if args.dry_run:
                print(f"  [DRY RUN] Would send webhook")
                log["webhook_actions"].append({
                    "user": login,
                    "status": "dry_run"
                })
            else:
                success, msg = send_idp_webhook("deprovision", user_data)
                status = "success" if success else "failed"
                print(f"  Webhook: {'✅' if success else '❌'}")
                log["webhook_actions"].append({
                    "user": login,
                    "status": status,
                    "message": msg if not success else None
                })
    
    # Summary
    scim_success = len([a for a in log["scim_actions"] if a["status"] == "success"])
    webhook_success = len([a for a in log["webhook_actions"] if a["status"] == "success"])
    
    log["summary"] = {
        "scim_deactivated": scim_success,
        "webhooks_sent": webhook_success
    }
    
    # Save
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(log, f, indent=2)
    
    print("\n" + "═" * 60)
    print(f"SCIM deactivated: {scim_success}")
    print(f"Webhooks sent: {webhook_success}")
    print(f"Log: {args.out}")

if __name__ == "__main__":
    main()
