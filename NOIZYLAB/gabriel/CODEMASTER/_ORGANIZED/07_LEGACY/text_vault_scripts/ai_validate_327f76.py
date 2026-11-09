#!/usr/bin/env python3
"""
ai_validate.py - Claude AI Classification for GitHub Offboarding
NOIZYLAB Production Version

Environment variables:
  CLAUDE_API_URL       Claude endpoint (required unless --force-rules)
  CLAUDE_API_KEY       Claude API key (or ANTHROPIC_API_KEY)
  ALLOW_EMAIL          Allowlist (default: rsplowman@icloud.com)
  CONFIDENCE_THRESHOLD Default: 0.95

Usage:
  python ai_validate.py --inventory artifacts/inventory.json --out artifacts/plan.json
  python ai_validate.py --inventory artifacts/inventory.json --force-rules  # Skip AI
"""

import os
import sys
import json
import time
import argparse
import re
from datetime import datetime, timezone

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from jsonschema import validate, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "remove": {"type": "array", "items": {"type": "object", "required": ["login", "reason", "confidence", "repos", "evidence"]}},
        "review": {"type": "array", "items": {"type": "object", "required": ["login", "reason", "confidence", "repos", "evidence"]}},
        "preserve": {"type": "array", "items": {"type": "object", "required": ["login", "reason", "confidence", "repos", "evidence"]}}
    },
    "required": ["remove", "review", "preserve"]
}

# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE API
# ═══════════════════════════════════════════════════════════════════════════════

def call_claude(api_url: str, api_key: str, payload: dict, max_retries: int = 4, backoff: int = 2):
    """Call Claude API with retries."""
    if not HAS_REQUESTS:
        raise RuntimeError("requests library required for Claude API")
    
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    
    # Also support Anthropic's standard header
    if "anthropic" in api_url.lower():
        headers["anthropic-version"] = "2023-06-01"
    
    attempt = 0
    last_resp = None
    
    while attempt < max_retries:
        try:
            r = requests.post(api_url, headers=headers, json=payload, timeout=90)
            last_resp = r
            if r.status_code == 200:
                return r.json()
            print(f"  Attempt {attempt+1}: status {r.status_code}", file=sys.stderr)
            attempt += 1
            time.sleep(backoff ** attempt)
        except requests.RequestException as e:
            print(f"  Attempt {attempt+1}: {e}", file=sys.stderr)
            attempt += 1
            time.sleep(backoff ** attempt)
    
    status = last_resp.status_code if last_resp else "no response"
    raise RuntimeError(f"Claude API failed after {max_retries} attempts; last status: {status}")


def compact_inventory(inv: dict) -> dict:
    """Compress inventory for Claude (reduce tokens)."""
    members = []
    for m in inv.get("members", []):
        members.append({
            "login": m.get("login"),
            "email": m.get("email") or None,
            "name": m.get("name") or None
        })
    
    # Repo collaborators as dict
    repo_collabs = {}
    rc = inv.get("repo_collaborators", {})
    if isinstance(rc, dict):
        for repo, collabs in rc.items():
            repo_collabs[repo] = [c.get("login") if isinstance(c, dict) else c for c in collabs if c]
    elif isinstance(rc, list):
        # Handle legacy array format
        for item in rc:
            repo = item.get("repo", "unknown")
            login = item.get("login")
            if login:
                repo_collabs.setdefault(repo, []).append(login)
    
    # Invitations
    invitations = []
    for i in inv.get("invitations", []):
        invitations.append({
            "login": i.get("login"),
            "email": i.get("email")
        })
    
    # Outside collaborators
    outside = []
    for o in inv.get("outside_collaborators", []):
        outside.append({
            "login": o.get("login"),
            "email": o.get("email")
        })
    
    return {
        "org": inv.get("org"),
        "members": members,
        "invitations": invitations,
        "outside_collaborators": outside,
        "repo_collaborators": repo_collabs
    }


def build_claude_payload(inv_summary: dict, allowlist: list, max_tokens: int = 4000) -> dict:
    """Build Claude API payload."""
    instruction = f"""You are an automated GitHub access auditor. Classify each account into remove, review, or preserve.

CRITICAL ALLOWLIST - These users must ALWAYS be in preserve, never remove:
{chr(10).join(f'- {a}' for a in allowlist)}

RULES:
1. Allowlist matches → preserve with confidence 1.0
2. Missing email → review (never auto-remove)
3. High confidence (>=0.95) and not in allowlist → remove
4. Any uncertainty → review

Return ONLY valid JSON with this exact structure:
{{
  "preserve": [{{ "login": "...", "reason": "...", "confidence": 0.0-1.0, "repos": [...], "evidence": "..." }}],
  "remove": [{{ "login": "...", "reason": "...", "confidence": 0.0-1.0, "repos": [...], "evidence": "..." }}],
  "review": [{{ "login": "...", "reason": "...", "confidence": 0.0-1.0, "repos": [...], "evidence": "..." }}]
}}

No commentary outside the JSON."""

    return {
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": json.dumps(inv_summary)}
        ],
        "max_tokens_to_sample": max_tokens,
        "max_tokens": max_tokens,  # Anthropic format
        "temperature": 0.0
    }


def extract_json(text: str) -> dict | None:
    """Extract JSON from Claude response."""
    if not text:
        return None
    
    # Try direct parse
    try:
        return json.loads(text)
    except:
        pass
    
    # Try extracting from markdown code block
    patterns = [
        r'```json\s*([\s\S]*?)\s*```',
        r'```\s*([\s\S]*?)\s*```',
        r'\{[\s\S]*\}'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                candidate = match.group(1) if '```' in pattern else match.group(0)
                return json.loads(candidate)
            except:
                continue
    
    # Last resort: find { to }
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except:
        return None


def extract_response_text(raw: dict) -> str:
    """Extract text from various Claude response formats."""
    if isinstance(raw, str):
        return raw
    
    if not isinstance(raw, dict):
        return str(raw)
    
    # Anthropic Messages API format
    if "content" in raw and isinstance(raw["content"], list):
        texts = [c.get("text", "") for c in raw["content"] if c.get("type") == "text"]
        return "\n".join(texts)
    
    # Legacy formats
    if "completion" in raw:
        comp = raw["completion"]
        if isinstance(comp, dict):
            return comp.get("content", "")
        return str(comp)
    
    if "output" in raw:
        return raw["output"]
    
    if "choices" in raw and isinstance(raw["choices"], list):
        choice = raw["choices"][0]
        if isinstance(choice, dict):
            msg = choice.get("message", {})
            if isinstance(msg, dict):
                return msg.get("content", "")
            return choice.get("text", str(msg))
    
    return json.dumps(raw)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_plan(plan: dict) -> tuple:
    """Validate plan against schema."""
    if HAS_JSONSCHEMA:
        try:
            validate(instance=plan, schema=PLAN_SCHEMA)
            return True, None
        except ValidationError as e:
            return False, str(e)
    
    # Manual validation
    errors = []
    for key in ["remove", "review", "preserve"]:
        if key not in plan:
            errors.append(f"Missing '{key}'")
        elif not isinstance(plan[key], list):
            errors.append(f"'{key}' must be array")
    
    return len(errors) == 0, "; ".join(errors) if errors else None


def fix_plan(plan: dict) -> dict:
    """Auto-fix common issues."""
    for key in ["remove", "review", "preserve"]:
        if key not in plan:
            plan[key] = []
    
    for category in ["remove", "review", "preserve"]:
        for entry in plan.get(category, []):
            if "repos" not in entry:
                entry["repos"] = []
            if "evidence" not in entry:
                entry["evidence"] = f"Classified as {category}"
            if "confidence" not in entry:
                entry["confidence"] = 0.5
            else:
                try:
                    entry["confidence"] = max(0.0, min(1.0, float(entry["confidence"])))
                except:
                    entry["confidence"] = 0.5
    
    return plan


# ═══════════════════════════════════════════════════════════════════════════════
# RULE-BASED FALLBACK
# ═══════════════════════════════════════════════════════════════════════════════

def rule_based_classify(inventory: dict, allowlist: list) -> dict:
    """Classify using rules when AI is unavailable."""
    org = inventory.get("org", "UNKNOWN")
    allowlist_lower = [a.lower().strip() for a in allowlist if a]
    
    preserve = []
    remove = []
    review = []
    
    def is_allowed(login: str, email: str) -> tuple:
        """Check allowlist. Returns (matched, evidence)."""
        login_l = (login or "").lower()
        email_l = (email or "").lower()
        
        if login_l in allowlist_lower:
            return True, f"Login '{login}' in allowlist"
        if email_l in allowlist_lower:
            return True, f"Email '{email}' in allowlist"
        
        # Partial match
        for allowed in allowlist_lower:
            if allowed and email_l and (allowed in email_l or email_l in allowed):
                return True, f"Email '{email}' matches '{allowed}'"
        
        return False, f"Not in allowlist"
    
    def get_repos(login: str) -> list:
        """Get repos for user."""
        repos = []
        rc = inventory.get("repo_collaborators", {})
        if isinstance(rc, dict):
            for repo, collabs in rc.items():
                for c in collabs:
                    c_login = c.get("login") if isinstance(c, dict) else c
                    if c_login and c_login.lower() == login.lower():
                        repos.append(repo)
        return repos
    
    # Process members
    for m in inventory.get("members", []):
        login = m.get("login", "")
        email = m.get("email", "")
        repos = get_repos(login)
        allowed, evidence = is_allowed(login, email)
        
        if allowed:
            preserve.append({
                "login": login, "email": email,
                "reason": "In allowlist",
                "confidence": 1.0, "repos": repos, "evidence": evidence
            })
        elif not email:
            review.append({
                "login": login, "email": email,
                "reason": "Missing email - requires review",
                "confidence": 0.5, "repos": repos, "evidence": "No email on record"
            })
        else:
            remove.append({
                "login": login, "email": email,
                "reason": "Not in allowlist",
                "confidence": 0.95, "repos": repos, "evidence": evidence
            })
    
    # Process invitations
    for i in inventory.get("invitations", []):
        login = i.get("login", "")
        email = i.get("email", "")
        allowed, evidence = is_allowed(login, email)
        
        if allowed:
            preserve.append({
                "login": login or "(pending)", "email": email,
                "reason": "Invitation in allowlist",
                "confidence": 1.0, "repos": [], "evidence": evidence
            })
        else:
            remove.append({
                "login": login or "(pending)", "email": email,
                "reason": "Pending invitation not in allowlist",
                "confidence": 0.95, "repos": [], "evidence": evidence
            })
    
    # Process outside collaborators
    for o in inventory.get("outside_collaborators", []):
        login = o.get("login", "")
        email = o.get("email", "")
        repos = get_repos(login)
        allowed, evidence = is_allowed(login, email)
        
        if allowed:
            preserve.append({
                "login": login, "email": email,
                "reason": "Outside collaborator in allowlist",
                "confidence": 1.0, "repos": repos, "evidence": evidence
            })
        else:
            remove.append({
                "login": login, "email": email,
                "reason": "Outside collaborator not in allowlist",
                "confidence": 0.95, "repos": repos, "evidence": evidence
            })
    
    return {
        "preserve": preserve,
        "remove": remove,
        "review": review,
        "metadata": {
            "method": "rule_based",
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "org": org,
            "allowlist": allowlist
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="AI classification for GitHub offboarding")
    parser.add_argument("--inventory", required=True, help="Path to inventory.json")
    parser.add_argument("--out", default="artifacts/plan.json", help="Output plan.json")
    parser.add_argument("--force-rules", action="store_true", help="Skip AI, use rule-based")
    args = parser.parse_args()
    
    # Config from environment
    claude_url = os.environ.get("CLAUDE_API_URL", "")
    claude_key = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
    allow_email = os.environ.get("ALLOW_EMAIL", "rsplowman@icloud.com")
    confidence_threshold = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.95"))
    
    # Parse allowlist
    allowlist = [a.strip() for a in allow_email.split(",") if a.strip()]
    
    # Load inventory
    print("═" * 60)
    print("AI CLASSIFICATION")
    print("═" * 60)
    
    with open(args.inventory) as f:
        inv = json.load(f)
    
    org = inv.get("org", "UNKNOWN")
    print(f"Org: {org}")
    print(f"Allowlist: {allowlist}")
    print(f"Threshold: {confidence_threshold}")
    
    # Ensure output directory
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    # Classify
    plan = None
    
    if args.force_rules:
        print("\n🔧 Using rule-based classification (--force-rules)")
        plan = rule_based_classify(inv, allowlist)
    elif not claude_url or not claude_key:
        print("\n⚠️ No CLAUDE_API_URL/CLAUDE_API_KEY - using rule-based fallback")
        plan = rule_based_classify(inv, allowlist)
    else:
        print(f"\n🤖 Calling Claude API...")
        try:
            inv_summary = compact_inventory(inv)
            payload = build_claude_payload(inv_summary, allowlist)
            
            raw = call_claude(claude_url, claude_key, payload)
            text = extract_response_text(raw)
            plan = extract_json(text)
            
            if not plan:
                print("  ⚠️ Failed to parse Claude response", file=sys.stderr)
                with open("artifacts/claude_raw.json", "w") as f:
                    json.dump({"raw": raw, "text": text}, f, indent=2)
                print("  Saved raw response to artifacts/claude_raw.json")
                print("  Falling back to rule-based...")
                plan = rule_based_classify(inv, allowlist)
            else:
                valid, err = validate_plan(plan)
                if not valid:
                    print(f"  ⚠️ Schema validation failed: {err}", file=sys.stderr)
                    plan = fix_plan(plan)
                    valid, err = validate_plan(plan)
                    if not valid:
                        print("  Falling back to rule-based...")
                        plan = rule_based_classify(inv, allowlist)
                    else:
                        print("  ✅ Auto-fixed plan")
                
                # Add metadata
                if "metadata" not in plan:
                    plan["metadata"] = {}
                plan["metadata"]["method"] = "claude_ai"
                plan["metadata"]["analyzed_at"] = datetime.now(timezone.utc).isoformat()
                plan["metadata"]["org"] = org
        
        except Exception as e:
            print(f"  ⚠️ Claude error: {e}", file=sys.stderr)
            print("  Falling back to rule-based...")
            plan = rule_based_classify(inv, allowlist)
    
    # ═══════════════════════════════════════════════════════════════════════
    # CRITICAL: Enforce allowlist (override AI if needed)
    # ═══════════════════════════════════════════════════════════════════════
    print("\n🔒 Enforcing allowlist...")
    allowlist_lower = [a.lower() for a in allowlist]
    
    # Move any allowlisted users from remove/review to preserve
    for category in ["remove", "review"]:
        moved = []
        remaining = []
        for entry in plan.get(category, []):
            login = (entry.get("login") or "").lower()
            email = (entry.get("email") or "").lower()
            
            if login in allowlist_lower or email in allowlist_lower:
                entry["reason"] = f"PROTECTED: {entry.get('reason', '')} (moved from {category})"
                entry["confidence"] = 1.0
                moved.append(entry)
            else:
                remaining.append(entry)
        
        plan[category] = remaining
        plan["preserve"] = plan.get("preserve", []) + moved
        
        if moved:
            print(f"  Moved {len(moved)} from {category} to preserve: {[e['login'] for e in moved]}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Apply confidence threshold
    # ═══════════════════════════════════════════════════════════════════════
    adjusted_remove = []
    moved_to_review = []
    
    for entry in plan.get("remove", []):
        if entry.get("confidence", 0) < confidence_threshold:
            entry["reason"] = f"{entry.get('reason', '')} (moved to review: confidence {entry.get('confidence', 0)} < {confidence_threshold})"
            moved_to_review.append(entry)
        else:
            adjusted_remove.append(entry)
    
    plan["remove"] = adjusted_remove
    plan["review"] = plan.get("review", []) + moved_to_review
    
    if moved_to_review:
        print(f"  Moved {len(moved_to_review)} to review (low confidence)")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Save outputs
    # ═══════════════════════════════════════════════════════════════════════
    with open(args.out, "w") as f:
        json.dump(plan, f, indent=2)
    
    summary = {
        "org": org,
        "method": plan.get("metadata", {}).get("method", "unknown"),
        "counts": {
            "preserve": len(plan.get("preserve", [])),
            "remove": len(plan.get("remove", [])),
            "review": len(plan.get("review", []))
        },
        "confidence_threshold": confidence_threshold,
        "allowlist": allowlist
    }
    
    summary_path = args.out.replace(".json", ".summary.txt")
    with open(summary_path, "w") as f:
        f.write(json.dumps(summary, indent=2))
    
    print(f"\n✅ Wrote: {args.out}")
    print(f"✅ Wrote: {summary_path}")
    print("\n" + "═" * 60)
    print(f"PRESERVE: {summary['counts']['preserve']}")
    print(f"REMOVE:   {summary['counts']['remove']}")
    print(f"REVIEW:   {summary['counts']['review']}")
    print("═" * 60)
    
    # List preserved
    print("\nPreserved users:")
    for p in plan.get("preserve", []):
        print(f"  ✅ {p.get('login')}")


if __name__ == "__main__":
    main()
