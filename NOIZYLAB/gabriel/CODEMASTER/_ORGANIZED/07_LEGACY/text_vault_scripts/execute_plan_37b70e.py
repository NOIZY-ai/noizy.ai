#!/usr/bin/env python3
"""
execute_plan.py - Execute offboarding plan
Usage:
  python execute_plan.py --plan artifacts/plan.json --org NOIZYLAB --out artifacts/execution_log.json
  python execute_plan.py --plan artifacts/plan.json --org NOIZYLAB --dry-run
Requires: GH_TOKEN or GITHUB_TOKEN environment variable
"""
import json
import os
import sys
import argparse
import time
from datetime import datetime, timezone

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Rate limiting
BATCH_SIZE = 5
DELAY_BETWEEN = 1  # seconds
DELAY_BETWEEN_BATCHES = 2


def get_token():
    """Get GitHub token from environment."""
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")


def gh_delete(url: str, token: str) -> tuple:
    """DELETE request to GitHub API."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    try:
        r = requests.delete(url, headers=headers, timeout=30)
        return r.status_code, r.text
    except Exception as e:
        return 0, str(e)


def delete_org_member(org: str, user: str, token: str) -> tuple:
    """Remove member from org."""
    url = f"https://api.github.com/orgs/{org}/members/{user}"
    return gh_delete(url, token)


def cancel_invitation(org: str, invitation_id: int, token: str) -> tuple:
    """Cancel pending invitation."""
    url = f"https://api.github.com/orgs/{org}/invitations/{invitation_id}"
    return gh_delete(url, token)


def remove_outside_collaborator(org: str, user: str, token: str) -> tuple:
    """Remove outside collaborator from org."""
    url = f"https://api.github.com/orgs/{org}/outside_collaborators/{user}"
    return gh_delete(url, token)


def remove_repo_collaborator(org: str, repo: str, user: str, token: str) -> tuple:
    """Remove collaborator from repo."""
    url = f"https://api.github.com/repos/{org}/{repo}/collaborators/{user}"
    return gh_delete(url, token)


def main():
    parser = argparse.ArgumentParser(description="Execute offboarding plan")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    parser.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"), help="GitHub org")
    parser.add_argument("--out", default="artifacts/execution_log.json", help="Output log")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    args = parser.parse_args()

    if not HAS_REQUESTS:
        print("ERROR: requests library required", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    if not token and not args.dry_run:
        print("ERROR: Set GH_TOKEN or GITHUB_TOKEN", file=sys.stderr)
        sys.exit(1)

    with open(args.plan) as f:
        plan = json.load(f)

    org = args.org
    
    print("═" * 60)
    print(f"EXECUTE PLAN {'(DRY RUN)' if args.dry_run else ''}")
    print("═" * 60)
    print(f"Org: {org}")
    print(f"Remove: {len(plan.get('remove', []))} users")
    
    log = {
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "org": org,
        "dry_run": args.dry_run,
        "actions": [],
        "summary": {"success": 0, "failed": 0, "skipped": 0}
    }

    remove_list = plan.get("remove", [])
    
    for i, entry in enumerate(remove_list):
        user = entry.get("login", "")
        if not user or user == "(pending)":
            # Handle invitation
            inv_id = entry.get("invitation_id")
            if inv_id:
                action = {
                    "type": "cancel_invitation",
                    "invitation_id": inv_id,
                    "email": entry.get("email"),
                    "dry_run": args.dry_run
                }
                
                if args.dry_run:
                    action["status"] = "would_cancel"
                    log["summary"]["skipped"] += 1
                else:
                    status, text = cancel_invitation(org, inv_id, token)
                    action["status"] = status
                    action["response"] = text[:200] if text else ""
                    if status in [204, 404]:  # 404 = already cancelled
                        log["summary"]["success"] += 1
                    else:
                        log["summary"]["failed"] += 1
                    time.sleep(DELAY_BETWEEN)
                
                log["actions"].append(action)
                print(f"  {'[DRY]' if args.dry_run else '🔴'} Cancel invitation: {entry.get('email')}")
            continue
        
        # Remove org member
        action = {
            "type": "remove_org_member",
            "user": user,
            "dry_run": args.dry_run
        }
        
        if args.dry_run:
            action["status"] = "would_remove"
            log["summary"]["skipped"] += 1
        else:
            status, text = delete_org_member(org, user, token)
            action["status"] = status
            action["response"] = text[:200] if text else ""
            if status in [204, 404]:  # 404 = already removed
                log["summary"]["success"] += 1
            else:
                log["summary"]["failed"] += 1
            time.sleep(DELAY_BETWEEN)
        
        log["actions"].append(action)
        print(f"  {'[DRY]' if args.dry_run else '🔴'} Remove member: {user}")
        
        # Remove from repos (cleanup)
        for repo in entry.get("repos", [])[:10]:  # Limit repos per user
            repo_action = {
                "type": "remove_repo_collaborator",
                "user": user,
                "repo": repo,
                "dry_run": args.dry_run
            }
            
            if args.dry_run:
                repo_action["status"] = "would_remove"
            else:
                status, text = remove_repo_collaborator(org, repo, user, token)
                repo_action["status"] = status
                time.sleep(DELAY_BETWEEN)
            
            log["actions"].append(repo_action)
        
        # Batch delay
        if (i + 1) % BATCH_SIZE == 0:
            if not args.dry_run:
                time.sleep(DELAY_BETWEEN_BATCHES)

    # Save log
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    with open(args.out, "w") as f:
        json.dump(log, f, indent=2)

    print("\n" + "═" * 60)
    print(f"✅ Complete: {args.out}")
    print(f"   Success: {log['summary']['success']}")
    print(f"   Failed:  {log['summary']['failed']}")
    print(f"   Skipped: {log['summary']['skipped']}")
    print("═" * 60)


if __name__ == "__main__":
    main()
