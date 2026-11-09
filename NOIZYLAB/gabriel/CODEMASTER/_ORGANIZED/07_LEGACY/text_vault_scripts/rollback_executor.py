#!/usr/bin/env python3
"""
rollback_executor.py - Reinstate removed members from snapshot
Usage:
  python rollback_executor.py --snapshot artifacts/rollback_snapshot.json
Requires: GH_TOKEN or GITHUB_TOKEN
"""
import json
import os
import sys
import argparse
import time

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def get_token():
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")


def add_org_member(org: str, user: str, token: str, role: str = "member") -> tuple:
    """Reinstate member to org."""
    url = f"https://api.github.com/orgs/{org}/memberships/{user}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    try:
        r = requests.put(url, headers=headers, json={"role": role}, timeout=30)
        return r.status_code, r.json() if r.status_code == 200 else r.text
    except Exception as e:
        return 0, str(e)


def main():
    parser = argparse.ArgumentParser(description="Execute rollback from snapshot")
    parser.add_argument("--snapshot", required=True, help="Path to rollback_snapshot.json")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    if not HAS_REQUESTS:
        print("ERROR: requests library required", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    if not token and not args.dry_run:
        print("ERROR: Set GH_TOKEN or GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)

    with open(args.snapshot) as f:
        snapshot = json.load(f)

    org = snapshot.get("org", os.environ.get("ORG", "NOIZYLAB"))
    members = snapshot.get("members_snapshot", [])
    invitations = snapshot.get("invitations_snapshot", [])

    print("═" * 60)
    print(f"ROLLBACK {'(DRY RUN)' if args.dry_run else ''}")
    print("═" * 60)
    print(f"Org: {org}")
    print(f"Members to reinstate: {len(members)}")
    print(f"Invitations (manual): {len(invitations)}")

    success = 0
    failed = 0

    for m in members:
        user = m.get("login")
        if not user:
            continue

        if args.dry_run:
            print(f"  [DRY] Would reinstate: {user}")
            continue

        status, response = add_org_member(org, user, token)
        
        if status == 200:
            state = response.get("state", "unknown") if isinstance(response, dict) else "unknown"
            print(f"  ✅ Reinstated {user} ({state})")
            success += 1
        else:
            print(f"  ❌ Failed {user}: {status}")
            failed += 1
        
        time.sleep(1)  # Rate limiting

    # Note about invitations
    if invitations:
        print("\n⚠️  Manual invitation required for:")
        for inv in invitations:
            print(f"     - {inv.get('email')}")

    print("\n" + "═" * 60)
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print("═" * 60)


if __name__ == "__main__":
    main()
