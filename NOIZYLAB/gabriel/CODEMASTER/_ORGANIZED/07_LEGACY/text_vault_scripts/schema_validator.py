#!/usr/bin/env python3
"""
schema_validator.py - Validate plan.json against schema
Usage:
  python schema_validator.py --plan artifacts/plan.json
  python schema_validator.py --plan artifacts/plan.json --fix
Exit codes: 0=valid, 1=fixed, 2=invalid
"""
import json
import sys
import argparse

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCHEMA = {
    "type": "object",
    "properties": {
        "remove": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["login", "reason", "confidence", "repos", "evidence"]
            }
        },
        "review": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["login", "reason", "confidence", "repos", "evidence"]
            }
        },
        "preserve": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["login", "reason", "confidence", "repos", "evidence"]
            }
        }
    },
    "required": ["remove", "review", "preserve"]
}


def fix_plan(plan: dict) -> dict:
    """Auto-fix common issues."""
    # Ensure required keys
    for key in ["remove", "review", "preserve"]:
        if key not in plan:
            plan[key] = []
    
    # Fix each entry
    for category in ["remove", "review", "preserve"]:
        for entry in plan.get(category, []):
            if "login" not in entry:
                entry["login"] = "unknown"
            if "reason" not in entry:
                entry["reason"] = f"Classified as {category}"
            if "confidence" not in entry:
                entry["confidence"] = 0.5
            else:
                try:
                    entry["confidence"] = max(0.0, min(1.0, float(entry["confidence"])))
                except:
                    entry["confidence"] = 0.5
            if "repos" not in entry:
                entry["repos"] = []
            if "evidence" not in entry:
                entry["evidence"] = "Auto-generated"
    
    return plan


def validate(plan: dict) -> tuple:
    """Validate plan. Returns (valid, error)."""
    if HAS_JSONSCHEMA:
        try:
            jsonschema.validate(instance=plan, schema=SCHEMA)
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e.message)
    
    # Manual validation
    errors = []
    for key in ["remove", "review", "preserve"]:
        if key not in plan:
            errors.append(f"Missing '{key}'")
        elif not isinstance(plan[key], list):
            errors.append(f"'{key}' must be array")
    
    return len(errors) == 0, "; ".join(errors) if errors else None


def main():
    parser = argparse.ArgumentParser(description="Validate plan.json schema")
    parser.add_argument("--plan", required=True, help="Path to plan.json")
    parser.add_argument("--fix", action="store_true", help="Auto-fix and save")
    args = parser.parse_args()
    
    with open(args.plan) as f:
        plan = json.load(f)
    
    valid, error = validate(plan)
    
    if valid:
        print("✅ VALID")
        sys.exit(0)
    
    print(f"❌ INVALID: {error}")
    
    if args.fix:
        print("🔧 Attempting auto-fix...")
        plan = fix_plan(plan)
        valid, error = validate(plan)
        
        if valid:
            with open(args.plan, "w") as f:
                json.dump(plan, f, indent=2)
            print("✅ FIXED and saved")
            sys.exit(1)  # Fixed = exit 1
        else:
            print(f"❌ Could not fix: {error}")
            sys.exit(2)
    
    sys.exit(2)


if __name__ == "__main__":
    main()
