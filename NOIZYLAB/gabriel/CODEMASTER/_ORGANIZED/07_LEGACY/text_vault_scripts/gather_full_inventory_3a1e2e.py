#!/usr/bin/env python3
"""
gather_full_inventory.py
Comprehensive GitHub org inventory for offboarding analysis

Collects:
- Org members (with email if available)
- Pending invitations
- Outside collaborators
- Repos and collaborators
- Teams and team members
- Deploy keys

Usage:
  export GH_TOKEN="ghp_..."
  python gather_full_inventory.py --org NOIZYLAB --out artifacts/inventory.json

Requires:
  GH_TOKEN environment variable with admin:org, repo permissions
"""

import os
import sys
import json
import argparse
import subprocess
import time
from datetime import datetime, timezone

ORG = os.environ.get("ORG", "NOIZYLAB")
RATE_LIMIT_DELAY = 0.3  # Seconds between API calls to avoid rate limits


def gh(args: list, timeout: int = 60) -> str:
    """Run gh CLI command."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0 and result.stderr:
            # Only print non-404 errors
            if "404" not in result.stderr:
                print(f"  ⚠️ {result.stderr[:80]}", file=sys.stderr)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  ⚠️ Timeout: gh {' '.join(args[:3])}...", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"  ⚠️ Error: {e}", file=sys.stderr)
        return ""


def gh_json(args: list, timeout: int = 60) -> list | dict:
    """Run gh CLI and parse JSON."""
    output = gh(args, timeout)
    if not output:
        return []
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return []


def gh_paginate(endpoint: str) -> list:
    """Fetch all pages from a paginated endpoint."""
    result = gh_json(["api", endpoint, "--paginate"])
    if isinstance(result, list):
        return result
    return []


def get_user_email(login: str) -> str | None:
    """Get user's public email if available."""
    user = gh_json(["api", f"/users/{login}"])
    if isinstance(user, dict):
        return user.get("email")
    return None


def main():
    parser = argparse.ArgumentParser(description="Gather GitHub org inventory")
    parser.add_argument("--org", default=ORG, help="GitHub organization")
    parser.add_argument("--out", default="artifacts/inventory.json", help="Output file")
    parser.add_argument("--skip-emails", action="store_true", help="Skip fetching user emails")
    parser.add_argument("--skip-deploy-keys", action="store_true", help="Skip deploy keys")
    args = parser.parse_args()

    org = args.org

    print("═" * 60)
    print(f"GATHERING INVENTORY FOR {org}")
    print("═" * 60)

    inventory = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "org": org,
        "members": [],
        "invitations": [],
        "outside_collaborators": [],
        "repos": [],
        "repo_collaborators": {},  # Dict: repo -> [collaborators]
        "teams": [],
        "team_members": {},  # Dict: team -> [members]
        "deploy_keys": {},  # Dict: repo -> [keys]
        "summary": {}
    }

    # ═══════════════════════════════════════════════════════════════════════
    # MEMBERS
    # ═══════════════════════════════════════════════════════════════════════
    print("\n📥 Collecting members...")
    members = gh_paginate(f"/orgs/{org}/members?per_page=100")

    for member in members:
        login = member.get("login", "")
        email = None

        # Optionally fetch email (slower but more complete)
        if not args.skip_emails:
            email = get_user_email(login)
            time.sleep(RATE_LIMIT_DELAY)

        inventory["members"].append({
            "login": login,
            "id": member.get("id"),
            "email": email,
            "avatar_url": member.get("avatar_url"),
            "type": member.get("type", "User")
        })

    print(f"  Found {len(inventory['members'])} members")

    # ═══════════════════════════════════════════════════════════════════════
    # INVITATIONS
    # ═══════════════════════════════════════════════════════════════════════
    print("\n📥 Collecting pending invitations...")
    invitations = gh_json(["api", f"/orgs/{org}/invitations"])

    if isinstance(invitations, list):
        for inv in invitations:
            inventory["invitations"].append({
                "id": inv.get("id"),
                "login": inv.get("login"),
                "email": inv.get("email"),
                "role": inv.get("role"),
                "created_at": inv.get("created_at"),
                "inviter": inv.get("inviter", {}).get("login")
            })

    print(f"  Found {len(inventory['invitations'])} invitations")

    # ═══════════════════════════════════════════════════════════════════════
    # OUTSIDE COLLABORATORS
    # ═══════════════════════════════════════════════════════════════════════
    print("\n📥 Collecting outside collaborators...")
    outside = gh_paginate(f"/orgs/{org}/outside_collaborators?per_page=100")

    for collab in outside:
        login = collab.get("login", "")
        email = None

        if not args.skip_emails:
            email = get_user_email(login)
            time.sleep(RATE_LIMIT_DELAY)

        inventory["outside_collaborators"].append({
            "login": login,
            "id": collab.get("id"),
            "email": email
        })

    print(f"  Found {len(inventory['outside_collaborators'])} outside collaborators")

    # ═══════════════════════════════════════════════════════════════════════
    # TEAMS
    # ═══════════════════════════════════════════════════════════════════════
    print("\n📥 Collecting teams...")
    teams = gh_json(["api", f"/orgs/{org}/teams"])

    if isinstance(teams, list):
        for team in teams:
            slug = team.get("slug", "")
            inventory["teams"].append({
                "slug": slug,
                "name": team.get("name"),
                "id": team.get("id"),
                "privacy": team.get("privacy")
            })

            # Team members
            team_members = gh_json(["api", f"/orgs/{org}/teams/{slug}/members"])
            if isinstance(team_members, list):
                inventory["team_members"][slug] = [
                    {"login": m.get("login"), "id": m.get("id")}
                    for m in team_members
                ]
            else:
                inventory["team_members"][slug] = []

            time.sleep(RATE_LIMIT_DELAY)

    print(f"  Found {len(inventory['teams'])} teams")

    # ═══════════════════════════════════════════════════════════════════════
    # REPOS
    # ═══════════════════════════════════════════════════════════════════════
    print("\n📥 Collecting repos...")
    repos_output = gh(["repo", "list", org, "--limit", "500", "--json", "name,visibility,isArchived"])

    try:
        repos = json.loads(repos_output) if repos_output else []
    except json.JSONDecodeError:
        repos = []

    for repo_info in repos:
        repo_name = repo_info.get("name", "")
        if not repo_name:
            continue

        inventory["repos"].append(repo_name)

        # Collaborators
        print(f"    {repo_name}...", end=" ", flush=True)
        collaborators = gh_json(["api", f"/repos/{org}/{repo_name}/collaborators?per_page=100"])

        if isinstance(collaborators, list):
            inventory["repo_collaborators"][repo_name] = [
                {
                    "login": c.get("login"),
                    "id": c.get("id"),
                    "permissions": c.get("permissions", {})
                }
                for c in collaborators
            ]
        else:
            inventory["repo_collaborators"][repo_name] = []

        # Deploy keys (optional)
        if not args.skip_deploy_keys:
            keys = gh_json(["api", f"/repos/{org}/{repo_name}/keys"])
            if isinstance(keys, list) and keys:
                inventory["deploy_keys"][repo_name] = [
                    {
                        "id": k.get("id"),
                        "title": k.get("title"),
                        "read_only": k.get("read_only"),
                        "created_at": k.get("created_at")
                    }
                    for k in keys
                ]

        print(f"{len(inventory['repo_collaborators'].get(repo_name, []))} collaborators")
        time.sleep(RATE_LIMIT_DELAY)

    print(f"\n  Found {len(inventory['repos'])} repos")

    # ═══════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════════
    total_repo_collaborators = sum(len(c) for c in inventory["repo_collaborators"].values())
    total_team_members = sum(len(m) for m in inventory["team_members"].values())
    total_deploy_keys = sum(len(k) for k in inventory["deploy_keys"].values())

    inventory["summary"] = {
        "members": len(inventory["members"]),
        "invitations": len(inventory["invitations"]),
        "outside_collaborators": len(inventory["outside_collaborators"]),
        "teams": len(inventory["teams"]),
        "team_memberships": total_team_members,
        "repos": len(inventory["repos"]),
        "repo_collaborators": total_repo_collaborators,
        "deploy_keys": total_deploy_keys
    }

    # ═══════════════════════════════════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════════════════════════════════
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w") as f:
        json.dump(inventory, f, indent=2)

    print("\n" + "═" * 60)
    print(f"✅ Inventory saved to {args.out}")
    print("═" * 60)
    print(f"  Members:               {inventory['summary']['members']}")
    print(f"  Invitations:           {inventory['summary']['invitations']}")
    print(f"  Outside collaborators: {inventory['summary']['outside_collaborators']}")
    print(f"  Teams:                 {inventory['summary']['teams']}")
    print(f"  Repos:                 {inventory['summary']['repos']}")
    print(f"  Deploy keys:           {inventory['summary']['deploy_keys']}")
    print("═" * 60)


if __name__ == "__main__":
    main()
