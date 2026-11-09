#!/usr/bin/env python3
"""
NOIZY Fish — Registry Dashboard
=================================

Terminal dashboard for the NOIZY Fish registry.
Displays:
- Registry stats
- Recent creators
- Recent inquiries
- Consent decisions breakdown
- Transaction log status

Run: python -m gabriel.noizy_fish.dashboard
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from .registry import NoizyFishDB
from .mcp_service import NoizyFishMCP


def print_box(title: str, width: int = 70):
    """Print a box header."""
    print(f"\n┌{'─' * (width - 2)}┐")
    print(f"│ {title.ljust(width - 4)} │")
    print(f"├{'─' * (width - 2)}┤")


def print_box_end(width: int = 70):
    """Print a box footer."""
    print(f"└{'─' * (width - 2)}┘")


def format_number(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def truncate(s: str, length: int = 30) -> str:
    """Truncate string."""
    if len(s) <= length:
        return s
    return s[:length - 3] + "..."


async def run_dashboard():
    """Run the registry dashboard."""
    # Get database path
    db_path = os.environ.get("NOIZY_FISH_DB", "noizy_fish.db")

    # Check if DB exists
    if not Path(db_path).exists() and db_path != ":memory:":
        print("\n⚠️  No registry database found.")
        print("   Run the demo first: python -m gabriel.noizy_fish.mcp_service --demo")
        print("   Or start the API: uvicorn gabriel.noizy_fish.api:app --reload")
        return

    db = NoizyFishDB(db_path)

    # Header
    print("\n" + "═" * 70)
    print("  NOIZY FISH — CREATOR CONSENT REGISTRY")
    print("═" * 70)
    print(f"  Database: {db_path}")
    print(f"  Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Get stats
    stats = db.get_stats()
    valid, issues = db.verify_transaction_log()

    # Stats Box
    print_box("REGISTRY STATISTICS")
    print(f"│  Creators:     {format_number(stats['creators']).rjust(12)}          │")
    print(f"│  Works:        {format_number(stats['works']).rjust(12)}          │")
    print(f"│  Consent Rules:{format_number(stats['consent_rules']).rjust(12)}          │")
    print(f"│  Licenses:     {format_number(stats['licenses']).rjust(12)}          │")
    print(f"│  Inquiries:    {format_number(stats['inquiries']).rjust(12)}          │")
    print(f"│  Transactions: {format_number(stats['transaction_log_entries']).rjust(12)}          │")
    print_box_end()

    # Decisions breakdown
    if stats.get('decisions'):
        print_box("DECISION BREAKDOWN")
        total = sum(stats['decisions'].values())
        for decision, count in sorted(stats['decisions'].items()):
            pct = (count / total * 100) if total > 0 else 0
            bar_len = int(pct / 2)
            bar = "█" * bar_len + "░" * (50 - bar_len)
            emoji = "✅" if decision in ["allowed", "allowed_terms"] else "❌" if decision == "denied" else "⏳"
            print(f"│  {emoji} {decision.ljust(18)} {count:4d} ({pct:5.1f}%) │")
        print_box_end()

    # Recent creators
    print_box("RECENT CREATORS")
    creators = db.search_creators(limit=5)
    if creators:
        print(f"│  {'Name'.ljust(25)} {'Type'.ljust(15)} {'Status'.ljust(15)} │")
        print(f"│  {'─' * 25} {'─' * 15} {'─' * 15} │")
        for c in creators:
            types = json.loads(c["creator_types"])
            print(f"│  {truncate(c['display_name'], 25).ljust(25)} {truncate(types[0] if types else '-', 15).ljust(15)} {c['verification_status'].ljust(15)} │")
    else:
        print("│  No creators registered                                        │")
    print_box_end()

    # Recent inquiries
    print_box("RECENT INQUIRIES")
    inquiries = db.get_inquiries(limit=5)
    if inquiries:
        print(f"│  {'Requestor'.ljust(20)} {'Category'.ljust(15)} {'Decision'.ljust(12)} {'Offer'.rjust(10)} │")
        print(f"│  {'─' * 20} {'─' * 15} {'─' * 12} {'─' * 10} │")
        for i in inquiries:
            emoji = "✅" if i["decision"] in ["allowed", "allowed_terms"] else "❌" if i["decision"] == "denied" else "⏳"
            offer = f"${i['offered_amount']:,.0f}" if i['offered_amount'] else "-"
            print(f"│  {truncate(i['requestor_name'], 20).ljust(20)} {truncate(i['use_category'], 15).ljust(15)} {emoji} {i['decision'].ljust(10)} {offer.rjust(10)} │")
    else:
        print("│  No inquiries yet                                               │")
    print_box_end()

    # Transaction log status
    print_box("TRANSACTION LOG INTEGRITY")
    if valid:
        print("│  ✓ Chain integrity: VALID                                       │")
        print(f"│    Entries: {stats['transaction_log_entries']}                                                 │")
    else:
        print("│  ✗ Chain integrity: INVALID                                     │")
        for issue in issues[:3]:
            print(f"│    - {issue.ljust(57)} │")
    print_box_end()

    # Use categories
    print_box("CONSENT CATEGORIES")
    categories = [
        ("streaming", "Standard streaming distribution"),
        ("sync_film", "Film/TV synchronization"),
        ("sync_ad", "Advertising synchronization"),
        ("ai_training", "AI/ML training data"),
        ("ai_voice_clone", "Voice cloning/synthesis"),
        ("sample", "Sampling in new works"),
        ("remix", "Remix/derivative works")
    ]
    for cat, desc in categories:
        print(f"│  • {cat.ljust(15)} — {desc.ljust(40)} │")
    print_box_end()

    # Footer
    print("\n" + "═" * 70)
    print("  NOIZY Fish — Consent as the foundation of creator rights")
    print("═" * 70)
    print("\n  Commands:")
    print("    API:    uvicorn gabriel.noizy_fish.api:app --reload --port 8765")
    print("    Docs:   http://localhost:8765/docs")
    print("    MCP:    python -m gabriel.noizy_fish.mcp_service")
    print()


async def demo_and_dashboard():
    """Run demo to populate data, then show dashboard."""
    from .mcp_service import NoizyFishMCP

    service = NoizyFishMCP(db_path="noizy_fish.db")

    print("\n" + "=" * 70)
    print("  POPULATING DEMO DATA...")
    print("=" * 70)

    # Register creators
    sarah = await service._register_creator({
        "display_name": "Sarah Chen",
        "creator_types": ["composer", "songwriter"],
        "ipi_number": "00123456789",
        "pro_membership": "ASCAP",
        "default_consent": "requires_approval"
    })
    print(f"  ✓ Created: {sarah['display_name']}")

    marcus = await service._register_creator({
        "display_name": "Marcus Reed",
        "creator_types": ["voice_actor"],
        "default_consent": "requires_approval"
    })
    print(f"  ✓ Created: {marcus['display_name']}")

    nova = await service._register_creator({
        "display_name": "DJ Nova",
        "creator_types": ["producer", "dj"],
        "default_consent": "negotiable"
    })
    print(f"  ✓ Created: {nova['display_name']}")

    # Set consent rules
    await service._update_consent_rule({
        "creator_id": sarah["creator_id"],
        "use_category": "ai_training",
        "decision": "denied"
    })
    await service._update_consent_rule({
        "creator_id": sarah["creator_id"],
        "use_category": "sync_film",
        "decision": "allowed_terms",
        "minimum_amount": 10000.00
    })
    await service._update_consent_rule({
        "creator_id": marcus["creator_id"],
        "use_category": "ai_voice_clone",
        "decision": "denied"
    })
    await service._update_consent_rule({
        "creator_id": nova["creator_id"],
        "use_category": "ai_training",
        "decision": "allowed_terms",
        "minimum_amount": 50000.00
    })
    print("  ✓ Consent rules configured")

    # Submit inquiries
    inquiries = [
        {"creator_id": sarah["creator_id"], "requestor_name": "Indie Film Studio", "use_category": "sync_film", "offered_amount": 15000.00},
        {"creator_id": sarah["creator_id"], "requestor_name": "AI Music Corp", "use_category": "ai_training", "offered_amount": 100000.00},
        {"creator_id": marcus["creator_id"], "requestor_name": "VoiceAI Inc", "use_category": "ai_voice_clone", "offered_amount": 50000.00},
        {"creator_id": nova["creator_id"], "requestor_name": "AI Music Lab", "use_category": "ai_training", "offered_amount": 60000.00},
        {"creator_id": nova["creator_id"], "requestor_name": "Remix Producer", "use_category": "sample", "offered_amount": 1000.00},
    ]

    for inq in inquiries:
        await service._submit_inquiry(inq)
    print(f"  ✓ {len(inquiries)} inquiries processed")

    print("  ✓ Demo data ready\n")

    # Now show dashboard
    await run_dashboard()


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        asyncio.run(demo_and_dashboard())
    else:
        asyncio.run(run_dashboard())
