#!/usr/bin/env python3
"""
feedback_loop.py
Record owner decisions to improve AI classification over time
"""

import json
import os
import argparse
from datetime import datetime, timezone
from pathlib import Path

FEEDBACK_DIR = os.environ.get("FEEDBACK_DIR", "artifacts/feedback")

def load_feedback_history() -> list:
    """Load existing feedback history."""
    history_path = Path(FEEDBACK_DIR) / "feedback_history.json"
    if history_path.exists():
        with open(history_path) as f:
            return json.load(f)
    return []

def save_feedback_history(history: list):
    """Save feedback history."""
    os.makedirs(FEEDBACK_DIR, exist_ok=True)
    history_path = Path(FEEDBACK_DIR) / "feedback_history.json"
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

def record_decision(plan: dict, execution_log: dict, decisions: dict) -> dict:
    """Record owner decisions on AI classifications."""
    feedback = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "plan_summary": {
            "preserve_count": len(plan.get("preserve", [])),
            "remove_count": len(plan.get("remove", [])),
            "review_count": len(plan.get("review", []))
        },
        "decisions": [],
        "corrections": []
    }
    
    # Record decisions on review items
    for entry in plan.get("review", []):
        login = entry.get("login")
        ai_reason = entry.get("reason")
        ai_confidence = entry.get("confidence")
        
        decision = decisions.get(login, {})
        owner_action = decision.get("action", "pending")  # approve_remove, approve_keep, pending
        owner_reason = decision.get("reason", "")
        
        feedback["decisions"].append({
            "login": login,
            "ai_classification": "review",
            "ai_reason": ai_reason,
            "ai_confidence": ai_confidence,
            "owner_action": owner_action,
            "owner_reason": owner_reason
        })
    
    # Record corrections (AI said remove but owner kept, or vice versa)
    executed_users = set()
    for action in execution_log.get("actions", []):
        if action.get("status") == "success":
            executed_users.add(action.get("user"))
    
    for entry in plan.get("remove", []):
        login = entry.get("login")
        if login not in executed_users:
            # AI said remove but wasn't executed (owner override)
            feedback["corrections"].append({
                "login": login,
                "ai_classification": "remove",
                "ai_confidence": entry.get("confidence"),
                "actual_outcome": "kept",
                "correction_type": "false_positive"
            })
    
    return feedback

def generate_training_prompt(history: list, limit: int = 50) -> str:
    """Generate training context from feedback history."""
    recent = history[-limit:] if len(history) > limit else history
    
    examples = []
    
    for feedback in recent:
        for decision in feedback.get("decisions", []):
            if decision.get("owner_action") in ["approve_remove", "approve_keep"]:
                examples.append({
                    "user": decision.get("login"),
                    "ai_said": decision.get("ai_classification"),
                    "owner_decided": decision.get("owner_action"),
                    "reason": decision.get("owner_reason")
                })
        
        for correction in feedback.get("corrections", []):
            examples.append({
                "user": correction.get("login"),
                "ai_said": correction.get("ai_classification"),
                "actual": correction.get("actual_outcome"),
                "type": correction.get("correction_type")
            })
    
    if not examples:
        return ""
    
    prompt_addition = """
LEARNING FROM PAST DECISIONS:
The following are owner decisions that corrected or confirmed AI classifications.
Use these to improve your accuracy:

"""
    
    for ex in examples[:20]:  # Limit to 20 examples
        if ex.get("type") == "false_positive":
            prompt_addition += f"- {ex['user']}: AI classified as REMOVE but owner KEPT (false positive)\n"
        elif ex.get("owner_decided") == "approve_remove":
            prompt_addition += f"- {ex['user']}: AI flagged for review, owner REMOVED\n"
        elif ex.get("owner_decided") == "approve_keep":
            prompt_addition += f"- {ex['user']}: AI flagged for review, owner KEPT\n"
    
    prompt_addition += "\nApply these learnings to improve classification accuracy.\n"
    
    return prompt_addition

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plan", help="Original plan JSON")
    p.add_argument("--execution-log", help="Execution log JSON")
    p.add_argument("--decisions", help="Owner decisions JSON file")
    p.add_argument("--generate-prompt", action="store_true", help="Generate training prompt")
    p.add_argument("--out", default="artifacts/feedback/latest.json")
    args = p.parse_args()
    
    if args.generate_prompt:
        history = load_feedback_history()
        prompt = generate_training_prompt(history)
        print(prompt if prompt else "No feedback history available")
        return
    
    if not args.plan or not args.execution_log:
        print("Provide --plan and --execution-log, or use --generate-prompt")
        return
    
    plan = json.load(open(args.plan))
    execution_log = json.load(open(args.execution_log))
    
    # Load decisions if provided
    decisions = {}
    if args.decisions and Path(args.decisions).exists():
        decisions = json.load(open(args.decisions))
    
    print("═" * 60)
    print("FEEDBACK LOOP - RECORDING DECISIONS")
    print("═" * 60)
    
    feedback = record_decision(plan, execution_log, decisions)
    
    # Save to history
    history = load_feedback_history()
    history.append(feedback)
    save_feedback_history(history)
    
    # Save latest
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(feedback, f, indent=2)
    
    print(f"Decisions recorded: {len(feedback['decisions'])}")
    print(f"Corrections recorded: {len(feedback['corrections'])}")
    print(f"Saved: {args.out}")
    print(f"History: {len(history)} total feedback entries")

if __name__ == "__main__":
    main()
