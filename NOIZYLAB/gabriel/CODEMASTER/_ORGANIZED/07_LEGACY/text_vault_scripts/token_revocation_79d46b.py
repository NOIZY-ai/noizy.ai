#!/usr/bin/env python3
"""
token_revocation.py
Revoke OAuth tokens and authorizations for removed users
"""

import json
import os
import argparse
import requests
import time
import sys
from datetime import datetime, timezone

ORG = os.environ.get("ORG", "NOIZYLAB")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

def api_get(endpoint: str) -> list | dict:
    """GET request with error handling."""
    url = f"https://api.github.com{endpoint}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            return r.json()
        return []
    except:
        return []

def api_delete(endpoint: str) -> tuple[int, str]:
    """DELETE request."""
    url = f"https://api.github.com{endpoint}"
    try:
        r = requests.delete(url, headers=HEADERS, timeout=30)
        return r.status_code, r.text
    except Exception as e:
        return 0, str(e)

def get_oauth_authorizations(org: str) -> list:
    """Get OAuth app authorizations (requires org owner)."""
    # Note: This endpoint may require specific permissions
    grants = api_get(f"/orgs/{org}/credential-authorizations")
    return grants if isinstance(grants, list) else []

def get_user_installations(user: str) -> list:
    """Get user's app installations."""
    # This requires user context, limited in org context
    return []

def revoke_credential(org: str, credential_id: int) -> tuple[bool, str]:
    """Revoke a credential authorization."""
    status, text = api_delete(f"/orgs/{org}/credential-authorizations/{credential_id}")
    return status in [200, 204], text

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True, help="Removal plan JSON")
    p.add_argument("--org", default=ORG)
    p.add_argument("--out", default="artifacts/token_revocation_log.json")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    
    if not TOKEN:
        print("❌ Set GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)
    
    org = args.org
    plan = json.load(open(args.plan))
    
    # Get users to remove
    users_to_remove = set()
    for entry in plan.get("remove", []):
        users_to_remove.add(entry.get("login", "").lower())
    
    print("═" * 60)
    print(f"TOKEN REVOCATION FOR {org}")
    print(f"Users to check: {len(users_to_remove)}")
    print(f"Mode: {'🔵 DRY RUN' if args.dry_run else '🔴 LIVE'}")
    print("═" * 60)
    
    log = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "org": org,
        "dry_run": args.dry_run,
        "credential_authorizations": [],
        "revocations": []
    }
    
    # Get OAuth authorizations
    print("\nFetching credential authorizations...")
    credentials = get_oauth_authorizations(org)
    log["credential_authorizations"] = credentials
    
    print(f"Found {len(credentials)} credential authorizations")
    
    # Check for matching users
    for cred in credentials:
        login = (cred.get("login") or "").lower()
        cred_id = cred.get("credential_id")
        
        if login in users_to_remove:
            print(f"  Found credential for removed user: {login}")
            
            if args.dry_run:
                log["revocations"].append({
                    "user": login,
                    "credential_id": cred_id,
                    "status": "dry_run"
                })
            else:
                success, text = revoke_credential(org, cred_id)
                log["revocations"].append({
                    "user": login,
                    "credential_id": cred_id,
                    "status": "success" if success else "failed",
                    "message": text if not success else None
                })
                time.sleep(0.5)
    
    # Summary
    revoked = len([r for r in log["revocations"] if r["status"] == "success"])
    failed = len([r for r in log["revocations"] if r["status"] == "failed"])
    
    log["summary"] = {
        "credentials_checked": len(credentials),
        "revoked": revoked,
        "failed": failed
    }
    
    # Save
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(log, f, indent=2)
    
    print("\n" + "═" * 60)
    print(f"Credentials checked: {len(credentials)}")
    print(f"Revoked: {revoked}")
    print(f"Failed: {failed}")
    print(f"Log: {args.out}")
    
    # Manual steps reminder
    print("\n⚠️ Manual verification required:")
    print(f"  OAuth Apps: https://github.com/orgs/{org}/settings/applications")
    print(f"  GitHub Apps: https://github.com/orgs/{org}/settings/installations")

if __name__ == "__main__":
    main()
