#!/usr/bin/env python3
"""
generate_rollback.py - Generate rollback script from execution log
Usage:
  python generate_rollback.py --audit artifacts/execution_log.json --org NOIZYLAB --out artifacts/rollback.sh
Creates:
  - rollback.sh (bash script)
  - rollback_snapshot.json (for rollback_executor.py)
"""
import json
import os
import sys
import argparse
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description="Generate rollback script")
    parser.add_argument("--audit", required=True, help="Path to execution_log.json")
    parser.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"), help="GitHub org")
    parser.add_argument("--out", default="artifacts/rollback.sh", help="Output script")
    args = parser.parse_args()

    if not os.path.exists(args.audit):
        print(f"Missing: {args.audit}", file=sys.stderr)
        sys.exit(1)

    with open(args.audit) as f:
        log = json.load(f)

    org = args.org
    actions = log.get("actions", [])

    # Extract removed users
    removed_members = []
    cancelled_invitations = []

    for action in actions:
        atype = action.get("type", "")
        status = action.get("status", 0)

        # Only include successful removals
        if status not in [204, 200]:
            continue

        if atype == "remove_org_member":
            user = action.get("user")
            if user:
                removed_members.append(user)

        if atype == "cancel_invitation":
            email = action.get("email")
            if email:
                cancelled_invitations.append(email)

    # Remove duplicates
    removed_members = list(set(removed_members))
    cancelled_invitations = list(set(cancelled_invitations))

    print("═" * 60)
    print("GENERATE ROLLBACK")
    print("═" * 60)
    print(f"Removed members: {len(removed_members)}")
    print(f"Cancelled invitations: {len(cancelled_invitations)}")

    # Generate bash script
    script_lines = [
        "#!/usr/bin/env bash",
        "# ROLLBACK SCRIPT - Generated from execution log",
        f"# Generated: {datetime.now(timezone.utc).isoformat()}",
        f"# Org: {org}",
        "#",
        "# This script will reinstate removed members.",
        "# Review carefully before running!",
        "#",
        "# Usage: GH_TOKEN=ghp_... ./rollback.sh",
        "",
        "set -euo pipefail",
        "",
        f'ORG="${{ORG:-{org}}}"',
        'TOKEN="${GH_TOKEN:-$GITHUB_TOKEN}"',
        "",
        'if [ -z "$TOKEN" ]; then',
        '    echo "ERROR: Set GH_TOKEN or GITHUB_TOKEN"',
        '    exit 1',
        'fi',
        "",
        'AUTH="Authorization: token $TOKEN"',
        'ACCEPT="Accept: application/vnd.github+json"',
        "",
        "echo '═══════════════════════════════════════════════════════════'",
        "echo 'ROLLBACK - REINSTATING MEMBERS'",
        "echo '═══════════════════════════════════════════════════════════'",
        "",
    ]

    # Add member reinstatement commands
    if removed_members:
        script_lines.append("# Reinstate org members")
        for user in removed_members:
            script_lines.append(f'echo "Reinstating {user}..."')
            script_lines.append(
                f'curl -s -X PUT -H "$AUTH" -H "$ACCEPT" '
                f'-d \'{{"role":"member"}}\' '
                f'"https://api.github.com/orgs/$ORG/memberships/{user}" | jq -r \'.state // "error"\''
            )
            script_lines.append("")
    else:
        script_lines.append("# No members to reinstate")
        script_lines.append("")

    # Add invitation recreation commands
    if cancelled_invitations:
        script_lines.append("# Re-invite cancelled invitations")
        script_lines.append("# NOTE: Cannot recreate invitations via API easily")
        script_lines.append("# Manual action required for:")
        for email in cancelled_invitations:
            script_lines.append(f"#   - {email}")
        script_lines.append("")
    
    script_lines.extend([
        "echo ''",
        "echo '═══════════════════════════════════════════════════════════'",
        "echo 'ROLLBACK COMPLETE'",
        "echo '═══════════════════════════════════════════════════════════'",
    ])

    # Write bash script
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(args.out, "w") as f:
        f.write("\n".join(script_lines))
    
    os.chmod(args.out, 0o755)
    print(f"\n✅ Wrote: {args.out}")

    # Write JSON snapshot for rollback_executor.py
    snapshot_path = args.out.replace(".sh", "_snapshot.json")
    snapshot = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "org": org,
        "source_audit": args.audit,
        "members_snapshot": [{"login": u} for u in removed_members],
        "invitations_snapshot": [{"email": e} for e in cancelled_invitations]
    }

    with open(snapshot_path, "w") as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"✅ Wrote: {snapshot_path}")
    print("═" * 60)


if __name__ == "__main__":
    main()
