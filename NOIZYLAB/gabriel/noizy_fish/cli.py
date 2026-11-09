#!/usr/bin/env python3
"""
NOIZY Fish — Command Line Interface
=====================================

CLI tools for managing the creator consent registry.

Usage:
    noizy-fish <command> [options]

Commands:
    status          Show registry status
    creators        List/search creators
    creator         Show creator details
    register        Register a new creator
    consent         Check or update consent
    inquiry         Submit a licensing inquiry
    import          Import from CSV/JSON
    export          Export to CSV/JSON
    analytics       Show analytics
    verify          Verify transaction log
    serve           Start API server

Examples:
    noizy-fish status
    noizy-fish creators --search "Sarah"
    noizy-fish consent check --creator abc123 --use ai_training
    noizy-fish inquiry --creator abc123 --requestor "AI Corp" --use ai_training --offer 100000
    noizy-fish import creators.csv --template standard_artist
    noizy-fish analytics --report summary
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from .registry import NoizyFishDB
from . import NoizyFish
from .bulk_ingestion import (
    import_creators_csv,
    import_works_csv,
    export_creators_csv,
    export_creators_json,
    list_templates
)
from .analytics import AnalyticsEngine


# ═══════════════════════════════════════════════════════════════════════════
# CLI Commands
# ═══════════════════════════════════════════════════════════════════════════

def cmd_status(args):
    """Show registry status."""
    fish = NoizyFish(args.db)
    stats = fish.stats()

    print("\n" + "═" * 50)
    print("  NOIZY FISH REGISTRY STATUS")
    print("═" * 50)
    print(f"  Database: {args.db}")
    print(f"  Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()
    print(f"  Creators:     {stats['creators']:>8}")
    print(f"  Works:        {stats['works']:>8}")
    print(f"  Consent Rules:{stats['consent_rules']:>8}")
    print(f"  Licenses:     {stats['licenses']:>8}")
    print(f"  Inquiries:    {stats['inquiries']:>8}")
    print(f"  Transactions: {stats['transaction_log_entries']:>8}")
    print()
    print(f"  Log Integrity: {'✓ Valid' if stats['transaction_log_valid'] else '✗ Invalid'}")
    print("═" * 50 + "\n")


def cmd_creators(args):
    """List or search creators."""
    db = NoizyFishDB(args.db)
    creators = db.search_creators(
        query=args.search,
        creator_type=args.type,
        limit=args.limit
    )

    print(f"\nFound {len(creators)} creator(s):\n")
    print(f"{'ID':<36} {'Name':<25} {'Type':<15} {'Status':<12}")
    print("-" * 90)

    for c in creators:
        types = json.loads(c["creator_types"])
        print(f"{c['creator_id']:<36} {c['display_name'][:25]:<25} {types[0] if types else '-':<15} {c['verification_status']:<12}")


def cmd_creator(args):
    """Show creator details."""
    fish = NoizyFish(args.db)
    creator = fish.get_creator(args.id)

    if not creator:
        print(f"\n✗ Creator not found: {args.id}")
        sys.exit(1)

    db = NoizyFishDB(args.db)
    rules = db.get_consent_rules(creator["creator_id"])

    print(f"\n{'═' * 50}")
    print(f"  CREATOR: {creator['display_name']}")
    print(f"{'═' * 50}")
    print(f"  ID: {creator['creator_id']}")
    print(f"  NOIZY ID: {creator['noizy_id']}")
    print(f"  Types: {', '.join(creator['creator_types'])}")
    print(f"  Status: {creator['verification_status']}")
    print()
    print(f"  CONSENT RULES ({len(rules)}):")
    print(f"  {'-' * 46}")

    for r in rules:
        min_comp = f"${r['min_compensation']:,.0f}" if r['min_compensation'] else "N/A"
        emoji = "✅" if r['decision'] in ['allowed', 'allowed_terms'] else "❌" if r['decision'] == 'denied' else "⏳"
        print(f"  {emoji} {r['use_category']:<20} {r['decision']:<15} {min_comp}")

    print(f"{'═' * 50}\n")


def cmd_register(args):
    """Register a new creator."""
    fish = NoizyFish(args.db)

    types = args.types.split(",") if args.types else ["performer"]

    result = fish.register_creator(
        display_name=args.name,
        creator_types=types,
        ipi_number=args.ipi,
        isni_number=args.isni,
        pro_membership=args.pro,
        consent_template=args.template,
        default_consent=args.default_consent
    )

    print(f"\n✓ Creator registered:")
    print(f"  ID: {result['creator_id']}")
    print(f"  NOIZY ID: {result['noizy_id']}")
    print(f"  Name: {result['display_name']}")

    if args.template:
        print(f"  Template: {args.template}")


def cmd_consent(args):
    """Check or update consent."""
    fish = NoizyFish(args.db)

    if args.action == "check":
        result = fish.check_consent(
            creator_id=args.creator,
            use_category=args.use,
            requestor=args.requestor,
            context=args.context,
            territory=args.territory or "WW",
            offered_amount=args.offer
        )

        emoji = "✅" if result['decision'] in ['allowed', 'allowed_terms'] else "❌" if result['decision'] == 'denied' else "⏳"

        print(f"\n{emoji} CONSENT CHECK")
        print(f"  Creator: {args.creator}")
        print(f"  Use: {args.use}")
        print(f"  Decision: {result['decision'].upper()}")
        print(f"  Reasons:")
        for reason in result['reasons']:
            print(f"    • {reason}")

    elif args.action == "update":
        result = fish.update_consent(
            creator_id=args.creator,
            use_category=args.use,
            decision=args.decision,
            minimum_amount=args.min_amount
        )

        print(f"\n✓ Consent updated:")
        print(f"  Use: {args.use}")
        print(f"  Decision: {args.decision}")
        if args.min_amount:
            print(f"  Minimum: ${args.min_amount:,.2f}")


def cmd_inquiry(args):
    """Submit a licensing inquiry."""
    fish = NoizyFish(args.db)

    result = fish.submit_inquiry(
        creator_id=args.creator,
        requestor_name=args.requestor,
        use_category=args.use,
        requestor_email=args.email,
        territory=args.territory or "WW",
        context=args.context,
        offered_amount=args.offer
    )

    emoji = "✅" if result['status'] == 'APPROVED' else "❌" if result['status'] == 'DENIED' else "⏳"

    print(f"\n{emoji} INQUIRY SUBMITTED")
    print(f"  ID: {result['inquiry_id']}")
    print(f"  Status: {result['status']}")
    print(f"  Decision: {result['decision']}")
    print(f"  Reasons:")
    for reason in result['reasons']:
        print(f"    • {reason}")


def cmd_import(args):
    """Import from CSV/JSON."""
    db = NoizyFishDB(args.db)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"\n✗ File not found: {args.file}")
        sys.exit(1)

    content = file_path.read_text()

    if args.type == "creators":
        if file_path.suffix == ".json":
            from .bulk_ingestion import import_creators_json
            result = import_creators_json(db, content, args.template)
        else:
            result = import_creators_csv(db, content, args.template)
    else:
        result = import_works_csv(db, content)

    print(f"\n{'✓' if result.failed == 0 else '⚠️'} IMPORT COMPLETE")
    print(f"  Total: {result.total}")
    print(f"  Successful: {result.successful}")
    print(f"  Failed: {result.failed}")

    if result.errors:
        print(f"\n  Errors:")
        for err in result.errors[:5]:
            print(f"    Row {err['row']}: {err['error']}")


def cmd_export(args):
    """Export to CSV/JSON."""
    db = NoizyFishDB(args.db)

    if args.format == "csv":
        content = export_creators_csv(db)
    else:
        content = export_creators_json(db)

    if args.output:
        Path(args.output).write_text(content)
        print(f"\n✓ Exported to: {args.output}")
    else:
        print(content)


def cmd_analytics(args):
    """Show analytics."""
    db = NoizyFishDB(args.db)
    analytics = AnalyticsEngine(db)

    if args.report == "summary":
        report = analytics.generate_report("summary")
        md = analytics.export_report_markdown(report)
        print(md)

    elif args.report == "ai":
        stats = analytics.get_ai_consent_stats()
        print("\n" + "═" * 50)
        print("  AI CONSENT ANALYTICS")
        print("═" * 50)
        print(f"  Total AI Inquiries: {stats['total_ai_inquiries']}")
        print(f"  Approved: {stats['ai_approved']} ({stats['ai_approval_rate']:.1f}%)")
        print(f"  Denied: {stats['ai_denied']}")
        print(f"  Value Denied: ${stats['total_ai_value_denied']:,.2f}")
        print("═" * 50 + "\n")

    elif args.report == "categories":
        categories = analytics.get_category_breakdown()
        print("\n" + "═" * 50)
        print("  CATEGORY ANALYTICS")
        print("═" * 50)
        for cat in categories:
            print(f"  {cat['category']:<20} {cat['total']:>5} inquiries ({cat['approval_rate']:>5.1f}% approved)")
        print("═" * 50 + "\n")


def cmd_verify(args):
    """Verify transaction log integrity."""
    db = NoizyFishDB(args.db)
    valid, issues = db.verify_transaction_log()

    if valid:
        print("\n✓ Transaction log integrity: VALID")
        stats = db.get_stats()
        print(f"  Entries: {stats['transaction_log_entries']}")
    else:
        print("\n✗ Transaction log integrity: INVALID")
        print("  Issues:")
        for issue in issues:
            print(f"    • {issue}")


def cmd_serve(args):
    """Start API server."""
    try:
        import uvicorn
        print(f"\n🚀 Starting NOIZY Fish API server on port {args.port}...")
        uvicorn.run(
            "gabriel.noizy_fish.api:app",
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    except ImportError:
        print("\n✗ uvicorn not installed. Run: pip install uvicorn")
        sys.exit(1)


def cmd_templates(args):
    """List consent templates."""
    templates = list_templates()

    print("\n" + "═" * 50)
    print("  CONSENT TEMPLATES")
    print("═" * 50)

    for tmpl in templates:
        print(f"\n  {tmpl['name']}")
        print(f"    {tmpl['description']}")

    print("\n" + "═" * 50)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="noizy-fish",
        description="NOIZY Fish Creator Consent Registry CLI"
    )
    parser.add_argument("--db", default="noizy_fish.db", help="Database path")

    subparsers = parser.add_subparsers(dest="command", help="Command")

    # status
    subparsers.add_parser("status", help="Show registry status")

    # creators
    p = subparsers.add_parser("creators", help="List/search creators")
    p.add_argument("--search", "-s", help="Search query")
    p.add_argument("--type", "-t", help="Filter by type")
    p.add_argument("--limit", "-n", type=int, default=50, help="Max results")

    # creator
    p = subparsers.add_parser("creator", help="Show creator details")
    p.add_argument("id", help="Creator ID or NOIZY ID")

    # register
    p = subparsers.add_parser("register", help="Register a new creator")
    p.add_argument("name", help="Display name")
    p.add_argument("--types", "-t", help="Creator types (comma-separated)")
    p.add_argument("--ipi", help="IPI number")
    p.add_argument("--isni", help="ISNI number")
    p.add_argument("--pro", help="PRO membership")
    p.add_argument("--template", help="Consent template to apply")
    p.add_argument("--default-consent", default="requires_approval", help="Default consent decision")

    # consent
    p = subparsers.add_parser("consent", help="Check or update consent")
    p.add_argument("action", choices=["check", "update"], help="Action")
    p.add_argument("--creator", "-c", required=True, help="Creator ID")
    p.add_argument("--use", "-u", required=True, help="Use category")
    p.add_argument("--requestor", "-r", help="Requestor name (for check)")
    p.add_argument("--context", help="Context (for check)")
    p.add_argument("--territory", help="Territory code")
    p.add_argument("--offer", type=float, help="Offered amount")
    p.add_argument("--decision", "-d", help="New decision (for update)")
    p.add_argument("--min-amount", type=float, help="Minimum amount (for update)")

    # inquiry
    p = subparsers.add_parser("inquiry", help="Submit a licensing inquiry")
    p.add_argument("--creator", "-c", required=True, help="Creator ID")
    p.add_argument("--requestor", "-r", required=True, help="Requestor name")
    p.add_argument("--use", "-u", required=True, help="Use category")
    p.add_argument("--email", "-e", help="Requestor email")
    p.add_argument("--territory", "-t", help="Territory code")
    p.add_argument("--context", help="Use context")
    p.add_argument("--offer", type=float, help="Offered amount")

    # import
    p = subparsers.add_parser("import", help="Import from CSV/JSON")
    p.add_argument("file", help="File to import")
    p.add_argument("--type", choices=["creators", "works"], default="creators", help="Import type")
    p.add_argument("--template", help="Consent template to apply")

    # export
    p = subparsers.add_parser("export", help="Export to CSV/JSON")
    p.add_argument("--format", "-f", choices=["csv", "json"], default="csv", help="Export format")
    p.add_argument("--output", "-o", help="Output file")

    # analytics
    p = subparsers.add_parser("analytics", help="Show analytics")
    p.add_argument("--report", "-r", choices=["summary", "ai", "categories"], default="summary", help="Report type")

    # verify
    subparsers.add_parser("verify", help="Verify transaction log")

    # serve
    p = subparsers.add_parser("serve", help="Start API server")
    p.add_argument("--host", default="0.0.0.0", help="Host")
    p.add_argument("--port", "-p", type=int, default=8765, help="Port")
    p.add_argument("--reload", action="store_true", help="Enable auto-reload")

    # templates
    subparsers.add_parser("templates", help="List consent templates")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Dispatch
    commands = {
        "status": cmd_status,
        "creators": cmd_creators,
        "creator": cmd_creator,
        "register": cmd_register,
        "consent": cmd_consent,
        "inquiry": cmd_inquiry,
        "import": cmd_import,
        "export": cmd_export,
        "analytics": cmd_analytics,
        "verify": cmd_verify,
        "serve": cmd_serve,
        "templates": cmd_templates
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
