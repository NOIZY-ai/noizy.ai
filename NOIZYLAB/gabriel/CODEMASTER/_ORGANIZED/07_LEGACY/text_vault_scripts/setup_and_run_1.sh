#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# NOIZYLAB OFFBOARDER - COMPLETE SETUP & RUN
# ═══════════════════════════════════════════════════════════════════════════════
# 
# Voice-friendly: Run this ONE script, it does everything.
#
# Usage:
#   chmod +x setup_and_run.sh
#   ./setup_and_run.sh
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

echo "═══════════════════════════════════════════════════════════"
echo "NOIZYLAB OFFBOARDER - COMPLETE SETUP"
echo "═══════════════════════════════════════════════════════════"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 1: CREATE DIRECTORY
# ───────────────────────────────────────────────────────────────────────────────
WORKDIR="$HOME/noizylab-audit"
mkdir -p "$WORKDIR"
cd "$WORKDIR"
echo "✅ Working directory: $WORKDIR"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 2: STORE TOKENS IN MACOS KEYCHAIN
# ───────────────────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "TOKEN SETUP"
echo "═══════════════════════════════════════════════════════════"

# Check if GH token exists in keychain
if ! security find-generic-password -a "noizylab" -s "gh_token" -w &>/dev/null; then
    echo ""
    echo "Enter your GitHub PAT (ghp_...):"
    echo "(Get one at: https://github.com/settings/tokens/new)"
    echo "(Required scopes: admin:org, repo)"
    read -s GH_TOKEN_INPUT
    security add-generic-password -a "noizylab" -s "gh_token" -w "$GH_TOKEN_INPUT"
    echo "✅ GitHub token saved to keychain"
else
    echo "✅ GitHub token found in keychain"
fi

# Check if Anthropic key exists in keychain
if ! security find-generic-password -a "noizylab" -s "anthropic_key" -w &>/dev/null; then
    echo ""
    echo "Enter your Anthropic API key (sk-ant-...):"
    echo "(Optional - press Enter to skip, will use rule-based classification)"
    read -s ANTHROPIC_KEY_INPUT
    if [ -n "$ANTHROPIC_KEY_INPUT" ]; then
        security add-generic-password -a "noizylab" -s "anthropic_key" -w "$ANTHROPIC_KEY_INPUT"
        echo "✅ Anthropic key saved to keychain"
    else
        echo "⏭️  Skipped - will use rule-based classification"
    fi
else
    echo "✅ Anthropic key found in keychain"
fi

# ───────────────────────────────────────────────────────────────────────────────
# STEP 3: LOAD TOKENS FROM KEYCHAIN
# ───────────────────────────────────────────────────────────────────────────────
export GH_TOKEN=$(security find-generic-password -a "noizylab" -s "gh_token" -w)
export ANTHROPIC_API_KEY=$(security find-generic-password -a "noizylab" -s "anthropic_key" -w 2>/dev/null || echo "")
export CLAUDE_API_URL="https://api.anthropic.com/v1/messages"

echo ""
echo "Tokens loaded from keychain"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 4: VERIFY GITHUB ACCESS
# ───────────────────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "VERIFYING GITHUB ACCESS"
echo "═══════════════════════════════════════════════════════════"

USER=$(curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/user | grep -o '"login": *"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$USER" ]; then
    echo "❌ GitHub token invalid"
    exit 1
fi
echo "✅ Logged in as: $USER"

# Check org access
ORG_CHECK=$(curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/orgs/NOIZYLAB/members | head -c 100)
if echo "$ORG_CHECK" | grep -q "Not Found\|Bad credentials"; then
    echo "❌ No access to NOIZYLAB org"
    exit 1
fi
echo "✅ NOIZYLAB org accessible"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 5: CREATE SCRIPTS
# ───────────────────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "CREATING SCRIPTS"
echo "═══════════════════════════════════════════════════════════"

mkdir -p scripts artifacts

# ─────────────────────────────────────────────────────────────
# gather_full_inventory.py
# ─────────────────────────────────────────────────────────────
cat > scripts/gather_full_inventory.py << 'SCRIPT'
#!/usr/bin/env python3
import os, json, subprocess, argparse
from datetime import datetime, timezone

def gh(args):
    try:
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=60, 
                          env={**os.environ, "GH_TOKEN": os.environ.get("GH_TOKEN", "")})
        return r.stdout.strip()
    except:
        return ""

def gh_json(args):
    out = gh(args)
    try:
        return json.loads(out) if out else []
    except:
        return []

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"))
    p.add_argument("--out", default="artifacts/inventory.json")
    args = p.parse_args()
    
    org = args.org
    print(f"Gathering inventory for {org}...")
    
    inv = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "org": org,
        "members": [],
        "invitations": [],
        "repos": [],
        "repo_collaborators": {}
    }
    
    # Members
    members = gh_json(["api", f"/orgs/{org}/members", "--paginate"])
    for m in members if isinstance(members, list) else []:
        user = gh_json(["api", f"/users/{m.get('login')}"])
        inv["members"].append({
            "login": m.get("login"),
            "id": m.get("id"),
            "email": user.get("email") if isinstance(user, dict) else None
        })
    print(f"  Members: {len(inv['members'])}")
    
    # Invitations
    invites = gh_json(["api", f"/orgs/{org}/invitations"])
    for i in invites if isinstance(invites, list) else []:
        inv["invitations"].append({"id": i.get("id"), "login": i.get("login"), "email": i.get("email")})
    print(f"  Invitations: {len(inv['invitations'])}")
    
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(inv, f, indent=2)
    print(f"Wrote: {args.out}")

if __name__ == "__main__":
    main()
SCRIPT

# ─────────────────────────────────────────────────────────────
# ai_validate.py
# ─────────────────────────────────────────────────────────────
cat > scripts/ai_validate.py << 'SCRIPT'
#!/usr/bin/env python3
import os, sys, json, time, argparse, re

try:
    import requests
except ImportError:
    requests = None

def call_claude(url, key, payload, retries=4):
    if not requests:
        return None
    headers = {"Content-Type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"}
    for i in range(retries):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=90)
            if r.status_code == 200:
                return r.json()
        except:
            pass
        time.sleep(2 ** i)
    return None

def extract_json(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except:
        pass
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    return None

def rule_based(inv, allowlist):
    allow_lower = [a.lower() for a in allowlist]
    preserve, remove, review = [], [], []
    
    for m in inv.get("members", []):
        login = m.get("login", "")
        email = m.get("email", "")
        entry = {"login": login, "reason": "", "confidence": 0.95, "repos": [], "evidence": ""}
        
        if login.lower() in allow_lower or (email and email.lower() in allow_lower):
            entry["reason"] = "In allowlist"
            entry["confidence"] = 1.0
            entry["evidence"] = "Matches allowlist"
            preserve.append(entry)
        elif not email:
            entry["reason"] = "Missing email - requires review"
            entry["confidence"] = 0.5
            entry["evidence"] = "No email on record"
            review.append(entry)
        else:
            entry["reason"] = "Not in allowlist"
            entry["evidence"] = "No allowlist match"
            remove.append(entry)
    
    return {"preserve": preserve, "remove": remove, "review": review}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--out", default="artifacts/plan.json")
    args = p.parse_args()
    
    url = os.environ.get("CLAUDE_API_URL", "")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    allow = os.environ.get("ALLOW_EMAIL", "rsplowman@icloud.com")
    threshold = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.95"))
    allowlist = [a.strip() for a in allow.split(",") if a.strip()]
    
    inv = json.load(open(args.inventory))
    
    # AI or fallback
    if not url or not key or not requests:
        print("Using rule-based classification")
        plan = rule_based(inv, allowlist)
    else:
        print("Calling Claude API...")
        prompt = f"Classify GitHub members for offboarding. Allowlist: {allowlist}. Return JSON with remove/review/preserve arrays. Each entry needs: login, reason, confidence (0-1), repos [], evidence."
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": f"{prompt}\n\nInventory:\n{json.dumps(inv, indent=2)}"}]
        }
        raw = call_claude(url, key, payload)
        
        text = ""
        if raw and "content" in raw:
            text = "".join(c.get("text", "") for c in raw["content"] if c.get("type") == "text")
        
        plan = extract_json(text)
        if not plan:
            print("AI failed, using rules")
            plan = rule_based(inv, allowlist)
    
    # CRITICAL: Enforce allowlist
    allow_lower = [a.lower() for a in allowlist]
    for cat in ["remove", "review"]:
        kept, moved = [], []
        for e in plan.get(cat, []):
            login = (e.get("login") or "").lower()
            email = (e.get("email") or "").lower()
            if login in allow_lower or email in allow_lower:
                e["reason"] = f"PROTECTED: {e.get('reason', '')}"
                e["confidence"] = 1.0
                moved.append(e)
            else:
                kept.append(e)
        plan[cat] = kept
        plan["preserve"] = plan.get("preserve", []) + moved
    
    # Apply threshold
    final_remove, to_review = [], []
    for e in plan.get("remove", []):
        if e.get("confidence", 0) < threshold:
            e["reason"] += " (low confidence)"
            to_review.append(e)
        else:
            final_remove.append(e)
    plan["remove"] = final_remove
    plan["review"] = plan.get("review", []) + to_review
    
    # Ensure required keys
    for k in ["preserve", "remove", "review"]:
        if k not in plan:
            plan[k] = []
    
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(plan, f, indent=2)
    
    summary = {"preserve": len(plan["preserve"]), "remove": len(plan["remove"]), "review": len(plan["review"])}
    with open(args.out.replace(".json", ".summary.txt"), "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Plan: {args.out}")
    print(f"Summary: {summary}")

if __name__ == "__main__":
    main()
SCRIPT

# ─────────────────────────────────────────────────────────────
# execute_plan.py
# ─────────────────────────────────────────────────────────────
cat > scripts/execute_plan.py << 'SCRIPT'
#!/usr/bin/env python3
import json, os, sys, argparse, time

try:
    import requests
except ImportError:
    requests = None

def get_token():
    return os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

def gh_delete(url, token):
    h = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    try:
        return requests.delete(url, headers=h, timeout=30).status_code
    except:
        return 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plan", required=True)
    p.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"))
    p.add_argument("--out", default="artifacts/execution_log.json")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    
    token = get_token()
    if not token and not args.dry_run:
        print("Set GH_TOKEN", file=sys.stderr)
        sys.exit(1)
    
    plan = json.load(open(args.plan))
    org = args.org
    log = {"actions": [], "summary": {"success": 0, "failed": 0}}
    
    for entry in plan.get("remove", []):
        user = entry.get("login", "")
        if not user or user == "(pending)":
            continue
        
        if args.dry_run:
            print(f"[DRY] Would remove: {user}")
            continue
        
        status = gh_delete(f"https://api.github.com/orgs/{org}/members/{user}", token)
        log["actions"].append({"type": "remove_member", "user": user, "status": status})
        
        if status in [204, 404]:
            log["summary"]["success"] += 1
        else:
            log["summary"]["failed"] += 1
        
        print(f"{'✅' if status in [204,404] else '❌'} {user}: {status}")
        time.sleep(1)
    
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(log, f, indent=2)
    print(f"Log: {args.out}")

if __name__ == "__main__":
    main()
SCRIPT

# ─────────────────────────────────────────────────────────────
# generate_rollback.py
# ─────────────────────────────────────────────────────────────
cat > scripts/generate_rollback.py << 'SCRIPT'
#!/usr/bin/env python3
import json, os, argparse
from datetime import datetime, timezone

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--audit", required=True)
    p.add_argument("--org", default=os.environ.get("ORG", "NOIZYLAB"))
    p.add_argument("--out", default="artifacts/rollback.sh")
    args = p.parse_args()
    
    log = json.load(open(args.audit))
    org = args.org
    
    removed = set()
    for a in log.get("actions", []):
        if a.get("type") == "remove_member" and a.get("status") in [204, 200]:
            removed.add(a.get("user"))
    
    script = f'''#!/usr/bin/env bash
# ROLLBACK - Generated {datetime.now(timezone.utc).isoformat()}
set -euo pipefail
ORG="${{ORG:-{org}}}"
TOKEN="${{GH_TOKEN:-$GITHUB_TOKEN}}"
[ -z "$TOKEN" ] && echo "Set GH_TOKEN" && exit 1
echo "Reinstating {len(removed)} members..."
'''
    
    for user in sorted(removed):
        script += f'''
curl -s -X PUT -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" \\
  -d '{{"role":"member"}}' "https://api.github.com/orgs/$ORG/memberships/{user}"
echo "  ✅ {user}"
'''
    
    script += '\necho "Rollback complete"\n'
    
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(script)
    os.chmod(args.out, 0o755)
    print(f"Wrote: {args.out}")

if __name__ == "__main__":
    main()
SCRIPT

# ─────────────────────────────────────────────────────────────
# run_offboard.sh (main runner)
# ─────────────────────────────────────────────────────────────
cat > scripts/run_offboard.sh << 'RUNNER'
#!/usr/bin/env bash
set -euo pipefail

DRY_RUN="${DRY_RUN:-true}"
export ORG="${ORG:-NOIZYLAB}"
export ALLOW_EMAIL="${ALLOW_EMAIL:-rsplowman@icloud.com}"

echo "═══════════════════════════════════════════════════════════"
echo "NOIZYLAB OFFBOARDING"
echo "═══════════════════════════════════════════════════════════"
echo "Org: $ORG | Allowlist: $ALLOW_EMAIL | Dry run: $DRY_RUN"

mkdir -p artifacts

echo -e "\n[1/3] Gathering inventory..."
python3 scripts/gather_full_inventory.py --org "$ORG" --out artifacts/inventory.json

echo -e "\n[2/3] AI classification..."
python3 scripts/ai_validate.py --inventory artifacts/inventory.json --out artifacts/plan.json

echo -e "\n[3/3] Verifying..."

# Verify rsplowman protected
if command -v jq &>/dev/null; then
    if jq -e '.remove[] | select(.login | ascii_downcase == "rsplowman")' artifacts/plan.json &>/dev/null; then
        echo "❌ CRITICAL: rsplowman in remove list!"
        exit 1
    fi
    echo "✅ rsplowman protected"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "RESULTS"
    echo "═══════════════════════════════════════════════════════════"
    echo "Preserve: $(jq '.preserve | length' artifacts/plan.json)"
    echo "Remove:   $(jq '.remove | length' artifacts/plan.json)"
    echo "Review:   $(jq '.review | length' artifacts/plan.json)"
    echo ""
    echo "Preserve list:"
    jq -r '.preserve[] | "  ✅ \(.login)"' artifacts/plan.json 2>/dev/null || echo "  (none)"
    echo ""
    echo "Remove list:"
    jq -r '.remove[] | "  ❌ \(.login)"' artifacts/plan.json 2>/dev/null || echo "  (none)"
fi

if [ "$DRY_RUN" = "true" ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "✅ DRY RUN COMPLETE - No changes made"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "To execute: DRY_RUN=false ./scripts/run_offboard.sh"
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "⚠️  EXECUTING REMOVALS"
echo "═══════════════════════════════════════════════════════════"
read -p "Type 'EXECUTE' to proceed: " CONFIRM
[ "$CONFIRM" != "EXECUTE" ] && echo "Aborted" && exit 0

python3 scripts/execute_plan.py --plan artifacts/plan.json --org "$ORG" --out artifacts/execution_log.json
python3 scripts/generate_rollback.py --audit artifacts/execution_log.json --org "$ORG" --out artifacts/rollback.sh

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "⚠️  ROTATE YOUR PAT NOW!"
echo ""
echo "Verify: https://github.com/orgs/$ORG/people"
echo "Rollback: ./artifacts/rollback.sh"
RUNNER

chmod +x scripts/*.sh scripts/*.py

echo "✅ Scripts created"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 6: INSTALL PYTHON DEPS
# ───────────────────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "INSTALLING DEPENDENCIES"
echo "═══════════════════════════════════════════════════════════"

pip3 install requests --quiet 2>/dev/null || pip install requests --quiet || echo "⚠️ Install requests manually: pip install requests"
echo "✅ Dependencies ready"

# ───────────────────────────────────────────────────────────────────────────────
# STEP 7: RUN OFFBOARDER (DRY RUN)
# ───────────────────────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "RUNNING OFFBOARDER (DRY RUN)"
echo "═══════════════════════════════════════════════════════════"

./scripts/run_offboard.sh

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "SETUP COMPLETE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Files created in: $WORKDIR"
echo ""
echo "To execute for real:"
echo "  cd $WORKDIR"
echo "  DRY_RUN=false ./scripts/run_offboard.sh"
echo ""
