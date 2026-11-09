#!/usr/bin/env python3
"""
secrets_audit.py - Scan for user references in secrets/variables/workflows
Usage:
  python secrets_audit.py --plan artifacts/plan.json --inventory artifacts/inventory.json --org NOIZYLAB
Scans:
  - Org secrets (names only - values hidden)
  - Org variables (names + values)
  - Repo secrets
  - Repo variables
  - Workflow files (content)
"""
import os
import sys
import json
import argparse
import subprocess
import re

ORG = os.environ.get("ORG", "NOIZYLAB")


def gh(args: list, timeout: int = 30) -> str:
    """Run gh CLI."""
    try:
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except:
        return ""


def gh_json(args: list) -> list | dict:
    """Run gh CLI, parse JSON."""
    out = gh(args)
    if not out:
        return []
    try:
        return json.loads(out)
    except:
        return []


def get_org_secrets(org: str) -> list:
    """Get org-level secrets (names only)."""
    data = gh_json(["api", f"/orgs/{org}/actions/secrets"])
    return data.get("secrets", []) if isinstance(data, dict) else []


def get_org_variables(org: str) -> list:
    """Get org-level variables (names + values)."""
    data = gh_json(["api", f"/orgs/{org}/actions/variables"])
    return data.get("variables", []) if isinstance(data, dict) else []


def get_repo_secrets(org: str, repo: str) -> list:
    """Get repo secrets."""
    data = gh_json(["api", f"/repos/{org}/{repo}/actions/secrets"])
    return data.get("secrets", []) if isinstance(data, dict) else []


def get_repo_variables(org: str, repo: str) -> list:
    """Get repo variables."""
    data = gh_json(["api", f"/repos/{org}/{repo}/actions/variables"])
    return data.get("variables", []) if isinstance(data, dict) else []


def get_workflow_files(org: str, repo: str) -> list:
    """Get workflow file contents."""
    files = []
    # List workflows
    tree = gh_json(["api", f"/repos/{org}/{repo}/contents/.github/workflows"])
    if not isinstance(tree, list):
        return []
    
    for item in tree:
        if item.get("name", "").endswith((".yml", ".yaml")):
            # Get content
            content_data = gh_json(["api", f"/repos/{org}/{repo}/contents/{item.get('path')}"])
            if isinstance(content_data, dict) and content_data.get("content"):
                import base64
                try:
                    content = base64.b64decode(content_data["content"]).decode("utf-8")
                    files.append({"name": item.get("name"), "path": item.get("path"), "content": content})
                except:
                    pass
    return files


def main():
    parser = argparse.ArgumentParser(description="Audit secrets for user references")
    parser.add_argument("--plan", default="artifacts/plan.json", help="Path to plan.json")
    parser.add_argument("--inventory", default="artifacts/inventory.json", help="Path to inventory.json")
    parser.add_argument("--org", default=ORG, help="GitHub org")
    parser.add_argument("--out", default="artifacts/secrets_audit.json", help="Output file")
    parser.add_argument("--scan-workflows", action="store_true", help="Also scan workflow files")
    args = parser.parse_args()

    print("═" * 60)
    print("SECRETS AUDIT")
    print("═" * 60)

    # Load plan
    if not os.path.exists(args.plan):
        print(f"Missing {args.plan}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.plan) as f:
        plan = json.load(f)

    # Get users to check
    users_to_check = []
    for entry in plan.get("remove", []):
        login = entry.get("login", "")
        email = entry.get("email", "")
        if login and login != "(pending)":
            users_to_check.append(login.lower())
        if email:
            # Add email parts
            users_to_check.append(email.lower())
            users_to_check.append(email.split("@")[0].lower())

    users_to_check = list(set(users_to_check))
    print(f"Checking for references to: {users_to_check}")

    # Load inventory for repo list
    repos = []
    if os.path.exists(args.inventory):
        with open(args.inventory) as f:
            inv = json.load(f)
            repos = inv.get("repos", [])
    
    if not repos:
        print("No repos in inventory, scanning org-level only")

    findings = []
    org = args.org

    # ═══════════════════════════════════════════════════════════════════════
    # ORG-LEVEL
    # ═══════════════════════════════════════════════════════════════════════
    print(f"\n📥 Scanning org secrets...")
    org_secrets = get_org_secrets(org)
    for s in org_secrets:
        name = s.get("name", "")
        for user in users_to_check:
            if user in name.lower():
                findings.append({
                    "type": "org_secret_name",
                    "name": name,
                    "matched_user": user,
                    "severity": "medium",
                    "note": "Secret name contains user reference"
                })

    print(f"   Found {len(org_secrets)} org secrets")

    print(f"📥 Scanning org variables...")
    org_vars = get_org_variables(org)
    for v in org_vars:
        name = v.get("name", "")
        value = v.get("value", "")
        for user in users_to_check:
            if user in name.lower():
                findings.append({
                    "type": "org_variable_name",
                    "name": name,
                    "matched_user": user,
                    "severity": "medium"
                })
            if user in value.lower():
                findings.append({
                    "type": "org_variable_value",
                    "name": name,
                    "matched_user": user,
                    "severity": "high",
                    "note": "Variable VALUE contains user reference"
                })

    print(f"   Found {len(org_vars)} org variables")

    # ═══════════════════════════════════════════════════════════════════════
    # REPO-LEVEL
    # ═══════════════════════════════════════════════════════════════════════
    print(f"\n📥 Scanning {len(repos)} repos...")
    
    for i, repo in enumerate(repos):
        if (i + 1) % 10 == 0:
            print(f"   {i + 1}/{len(repos)}...")

        # Repo secrets
        repo_secrets = get_repo_secrets(org, repo)
        for s in repo_secrets:
            name = s.get("name", "")
            for user in users_to_check:
                if user in name.lower():
                    findings.append({
                        "type": "repo_secret_name",
                        "repo": repo,
                        "name": name,
                        "matched_user": user,
                        "severity": "medium"
                    })

        # Repo variables
        repo_vars = get_repo_variables(org, repo)
        for v in repo_vars:
            name = v.get("name", "")
            value = v.get("value", "")
            for user in users_to_check:
                if user in name.lower():
                    findings.append({
                        "type": "repo_variable_name",
                        "repo": repo,
                        "name": name,
                        "matched_user": user,
                        "severity": "medium"
                    })
                if user in value.lower():
                    findings.append({
                        "type": "repo_variable_value",
                        "repo": repo,
                        "name": name,
                        "matched_user": user,
                        "severity": "high"
                    })

        # Workflow files (optional, slower)
        if args.scan_workflows:
            workflows = get_workflow_files(org, repo)
            for wf in workflows:
                content = wf.get("content", "")
                for user in users_to_check:
                    # Find line numbers
                    for line_num, line in enumerate(content.split("\n"), 1):
                        if user in line.lower():
                            findings.append({
                                "type": "workflow_content",
                                "repo": repo,
                                "file": wf.get("path"),
                                "line": line_num,
                                "matched_user": user,
                                "severity": "high",
                                "snippet": line.strip()[:100]
                            })

    # ═══════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════════
    summary = {
        "total_findings": len(findings),
        "high_severity": len([f for f in findings if f.get("severity") == "high"]),
        "medium_severity": len([f for f in findings if f.get("severity") == "medium"]),
        "low_severity": len([f for f in findings if f.get("severity") == "low"])
    }

    output = {
        "audited_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "org": org,
        "users_checked": users_to_check,
        "findings": findings,
        "summary": summary
    }

    # Save
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    with open(args.out, "w") as f:
        json.dump(output, f, indent=2)

    print("\n" + "═" * 60)
    print(f"✅ Wrote: {args.out}")
    print(f"   Total findings: {summary['total_findings']}")
    print(f"   High severity:  {summary['high_severity']}")
    print(f"   Medium severity: {summary['medium_severity']}")
    print("═" * 60)

    if summary["high_severity"] > 0:
        print("\n⚠️  HIGH SEVERITY FINDINGS - Review before proceeding!")
        for f in findings:
            if f.get("severity") == "high":
                print(f"   - {f.get('type')}: {f.get('name', f.get('file'))} ({f.get('matched_user')})")


if __name__ == "__main__":
    main()
