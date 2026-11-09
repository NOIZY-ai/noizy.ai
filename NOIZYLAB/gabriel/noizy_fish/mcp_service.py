"""
NOIZY Fish — MCP Service
=========================

Model Context Protocol service for NOIZY Fish.
Exposes tools for:

1. Creator Management
   - register_creator — Create/update creator passport
   - get_creator — Fetch creator by ID
   - search_creators — Search creators

2. Consent Management
   - check_consent — Fast consent lookup (the core query!)
   - get_consent_rules — Get all rules for a creator
   - update_consent_rule — Update a consent rule

3. Work Management
   - register_work — Register a work (recording, composition, voice)
   - get_work — Fetch work by ID
   - get_creator_works — Get all works by a creator

4. Licensing Inquiry
   - submit_inquiry — Submit licensing inquiry (full flow)

5. Registry Stats
   - get_registry_stats — Get registry statistics

Run standalone: python -m gabriel.noizy_fish.mcp_service
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

# MCP imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP not available — running in standalone mode")

from .registry import NoizyFishDB
from .identity.creator_passport import (
    CreatorPassport,
    CreatorIdentity,
    CreatorType,
    VerificationStatus,
    ConsentRegistry,
    ConsentRule,
    UseCategory,
    ConsentDecision,
    CompensationTerms,
    CompensationType
)
from .standards import IPI, ISNI, NoizyID, ContributorRole


class NoizyFishMCP:
    """
    NOIZY Fish MCP Service.
    Handles all MCP tool calls for the registry.
    """

    def __init__(self, db_path: str = "noizy_fish.db"):
        self.db = NoizyFishDB(db_path)
        if MCP_AVAILABLE:
            self.server = Server("noizy-fish")
            self._register_tools()

    def _register_tools(self):
        """Register MCP tools."""
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="register_creator",
                    description="Register a new creator in NOIZY Fish with identity and consent settings",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "display_name": {"type": "string", "description": "Public/artist name"},
                            "creator_types": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Types: composer, lyricist, songwriter, producer, performer, voice_actor, sound_designer, dj, engineer"
                            },
                            "ipi_number": {"type": "string", "description": "IPI number (11 digits)"},
                            "isni_number": {"type": "string", "description": "ISNI number (16 digits)"},
                            "pro_membership": {"type": "string", "description": "PRO: ASCAP, BMI, SESAC, etc."},
                            "default_consent": {
                                "type": "string",
                                "description": "Default consent: allowed, requires_approval, denied, negotiable"
                            }
                        },
                        "required": ["display_name", "creator_types"]
                    }
                ),
                Tool(
                    name="get_creator",
                    description="Get creator passport by creator_id or noizy_id",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creator_id": {"type": "string", "description": "Creator ID or NOIZY ID"}
                        },
                        "required": ["creator_id"]
                    }
                ),
                Tool(
                    name="search_creators",
                    description="Search for creators by name or type",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"},
                            "creator_type": {"type": "string", "description": "Filter by type"},
                            "limit": {"type": "integer", "description": "Max results (default 50)"}
                        }
                    }
                ),
                Tool(
                    name="check_consent",
                    description="Check if a use is allowed for a creator — the core licensing query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creator_id": {"type": "string", "description": "Creator ID"},
                            "use_category": {
                                "type": "string",
                                "description": "Use type: streaming, sync_film, sync_ad, ai_training, ai_voice_clone, sample, remix, etc."
                            },
                            "requestor": {"type": "string", "description": "Name of requesting party"},
                            "context": {"type": "string", "description": "Context/description of use"},
                            "territory": {"type": "string", "description": "ISO territory code (default WW)"},
                            "offered_amount": {"type": "number", "description": "Offered compensation"}
                        },
                        "required": ["creator_id", "use_category"]
                    }
                ),
                Tool(
                    name="update_consent_rule",
                    description="Update consent rule for a specific use category",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creator_id": {"type": "string", "description": "Creator ID"},
                            "use_category": {"type": "string", "description": "Use category"},
                            "decision": {
                                "type": "string",
                                "description": "Decision: allowed, allowed_terms, requires_approval, negotiable, denied"
                            },
                            "minimum_amount": {"type": "number", "description": "Minimum compensation"},
                            "excluded_parties": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Parties to exclude"
                            },
                            "excluded_contexts": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Contexts to exclude (e.g., tobacco, political)"
                            }
                        },
                        "required": ["creator_id", "use_category", "decision"]
                    }
                ),
                Tool(
                    name="register_work",
                    description="Register a work (recording, composition, voice asset)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creator_id": {"type": "string", "description": "Creator ID"},
                            "title": {"type": "string", "description": "Work title"},
                            "work_type": {
                                "type": "string",
                                "description": "Type: recording, composition, voice"
                            },
                            "isrc": {"type": "string", "description": "ISRC code (for recordings)"},
                            "iswc": {"type": "string", "description": "ISWC code (for compositions)"},
                            "format": {"type": "string", "description": "Format: audio/wav, audio/mp3, etc."}
                        },
                        "required": ["creator_id", "title", "work_type"]
                    }
                ),
                Tool(
                    name="get_work",
                    description="Get work by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "work_id": {"type": "string", "description": "Work ID or NOIZY work ID"}
                        },
                        "required": ["work_id"]
                    }
                ),
                Tool(
                    name="submit_inquiry",
                    description="Submit a full licensing inquiry — checks consent and logs result",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creator_id": {"type": "string", "description": "Creator ID"},
                            "requestor_name": {"type": "string", "description": "Requesting party name"},
                            "requestor_email": {"type": "string", "description": "Requesting party email"},
                            "use_category": {"type": "string", "description": "Use category"},
                            "work_id": {"type": "string", "description": "Work ID (optional)"},
                            "territory": {"type": "string", "description": "Territory code"},
                            "context": {"type": "string", "description": "Use context/description"},
                            "offered_amount": {"type": "number", "description": "Offered compensation"}
                        },
                        "required": ["creator_id", "requestor_name", "use_category"]
                    }
                ),
                Tool(
                    name="get_registry_stats",
                    description="Get NOIZY Fish registry statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            try:
                result = await self._handle_tool(name, arguments)
                return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

    async def _handle_tool(self, name: str, args: dict) -> dict:
        """Route tool calls to handlers."""
        handlers = {
            "register_creator": self._register_creator,
            "get_creator": self._get_creator,
            "search_creators": self._search_creators,
            "check_consent": self._check_consent,
            "update_consent_rule": self._update_consent_rule,
            "register_work": self._register_work,
            "get_work": self._get_work,
            "submit_inquiry": self._submit_inquiry,
            "get_registry_stats": self._get_registry_stats
        }

        handler = handlers.get(name)
        if not handler:
            return {"error": f"Unknown tool: {name}"}

        return await handler(args)

    # ═══════════════════════════════════════════════════════════════════
    # Tool Handlers
    # ═══════════════════════════════════════════════════════════════════

    async def _register_creator(self, args: dict) -> dict:
        """Register a new creator."""
        passport = CreatorPassport()

        # Set identity
        passport.identity.display_name = args["display_name"]
        passport.identity.creator_types = [
            CreatorType(t) for t in args.get("creator_types", ["performer"])
        ]

        if args.get("ipi_number"):
            passport.identity.ipi_number = IPI.parse(args["ipi_number"])

        if args.get("isni_number"):
            passport.identity.isni_number = ISNI.parse(args["isni_number"])

        passport.identity.pro_membership = args.get("pro_membership")

        # Set default consent
        default = args.get("default_consent", "requires_approval")
        passport.consent.default_decision = ConsentDecision(default)

        # Save to database
        creator_id = self.db.save_creator(passport)

        # Log transaction
        self.db.log_transaction(
            "creator_registered",
            {
                "creator_id": creator_id,
                "display_name": passport.identity.display_name,
                "types": [t.value for t in passport.identity.creator_types]
            },
            entity_id=creator_id,
            entity_type="creator"
        )

        return {
            "success": True,
            "creator_id": creator_id,
            "noizy_id": str(passport.identity.noizy_id),
            "display_name": passport.identity.display_name,
            "message": f"Creator '{passport.identity.display_name}' registered successfully"
        }

    async def _get_creator(self, args: dict) -> dict:
        """Get creator by ID."""
        creator_id = args["creator_id"]

        # Try by creator_id first
        creator = self.db.get_creator(creator_id)

        # Try by noizy_id if not found
        if not creator:
            creator = self.db.get_creator_by_noizy_id(creator_id)

        if not creator:
            return {"error": f"Creator not found: {creator_id}"}

        # Get consent rules
        rules = self.db.get_consent_rules(creator["creator_id"])

        return {
            "creator_id": creator["creator_id"],
            "noizy_id": creator["noizy_id"],
            "display_name": creator["display_name"],
            "creator_types": json.loads(creator["creator_types"]),
            "ipi_number": creator["ipi_number"],
            "isni_number": creator["isni_number"],
            "pro_membership": creator["pro_membership"],
            "verification_status": creator["verification_status"],
            "consent_rules": [
                {
                    "use_category": r["use_category"],
                    "decision": r["decision"],
                    "min_compensation": r["min_compensation"]
                }
                for r in rules
            ],
            "created_at": creator["created_at"],
            "updated_at": creator["updated_at"]
        }

    async def _search_creators(self, args: dict) -> dict:
        """Search creators."""
        results = self.db.search_creators(
            query=args.get("query"),
            creator_type=args.get("creator_type"),
            limit=args.get("limit", 50)
        )

        return {
            "count": len(results),
            "creators": [
                {
                    "creator_id": c["creator_id"],
                    "noizy_id": c["noizy_id"],
                    "display_name": c["display_name"],
                    "creator_types": json.loads(c["creator_types"]),
                    "verification_status": c["verification_status"]
                }
                for c in results
            ]
        }

    async def _check_consent(self, args: dict) -> dict:
        """Check consent — the core query."""
        result = self.db.check_consent(
            creator_id=args["creator_id"],
            use_category=args["use_category"],
            requestor=args.get("requestor"),
            context=args.get("context"),
            territory=args.get("territory", "WW"),
            offered_amount=args.get("offered_amount")
        )

        return {
            "creator_id": args["creator_id"],
            "use_category": args["use_category"],
            **result
        }

    async def _update_consent_rule(self, args: dict) -> dict:
        """Update a consent rule."""
        # Get existing creator
        creator = self.db.get_creator(args["creator_id"])
        if not creator:
            return {"error": f"Creator not found: {args['creator_id']}"}

        # Parse passport
        passport_data = json.loads(creator["passport_data"])

        # Create new rule
        rule = ConsentRule(
            use_category=UseCategory(args["use_category"]),
            decision=ConsentDecision(args["decision"])
        )

        if args.get("minimum_amount"):
            rule.compensation = CompensationTerms(
                compensation_type=CompensationType.FLAT_FEE,
                minimum_amount=args["minimum_amount"]
            )

        if args.get("excluded_parties"):
            rule.excluded_parties = args["excluded_parties"]

        if args.get("excluded_contexts"):
            rule.excluded_contexts = args["excluded_contexts"]

        # Save rule
        with self.db._get_conn() as conn:
            self.db._save_consent_rule(conn, args["creator_id"], rule)

        # Log transaction
        self.db.log_transaction(
            "consent_rule_updated",
            {
                "creator_id": args["creator_id"],
                "use_category": args["use_category"],
                "decision": args["decision"],
                "minimum_amount": args.get("minimum_amount")
            },
            entity_id=args["creator_id"],
            entity_type="consent_rule"
        )

        return {
            "success": True,
            "creator_id": args["creator_id"],
            "use_category": args["use_category"],
            "decision": args["decision"],
            "message": f"Consent rule updated for {args['use_category']}"
        }

    async def _register_work(self, args: dict) -> dict:
        """Register a work."""
        work_id = str(uuid4())
        work_type = args["work_type"]

        # Generate NOIZY work ID
        type_prefix = {"recording": "REC", "composition": "WK", "voice": "VOC"}.get(work_type, "WK")
        noizy_work_id = f"NZ-{type_prefix}-{datetime.utcnow().strftime('%Y%m%d')}-{work_id[:8].upper()}"

        self.db.save_work(
            work_id=work_id,
            noizy_work_id=noizy_work_id,
            creator_id=args["creator_id"],
            work_type=work_type,
            title=args["title"],
            isrc=args.get("isrc"),
            iswc=args.get("iswc"),
            format=args.get("format")
        )

        # Log transaction
        self.db.log_transaction(
            "work_registered",
            {
                "work_id": work_id,
                "noizy_work_id": noizy_work_id,
                "creator_id": args["creator_id"],
                "title": args["title"],
                "work_type": work_type
            },
            entity_id=work_id,
            entity_type="work"
        )

        return {
            "success": True,
            "work_id": work_id,
            "noizy_work_id": noizy_work_id,
            "title": args["title"],
            "work_type": work_type,
            "message": f"Work '{args['title']}' registered successfully"
        }

    async def _get_work(self, args: dict) -> dict:
        """Get work by ID."""
        work = self.db.get_work(args["work_id"])

        if not work:
            return {"error": f"Work not found: {args['work_id']}"}

        return {
            "work_id": work["work_id"],
            "noizy_work_id": work["noizy_work_id"],
            "creator_id": work["creator_id"],
            "work_type": work["work_type"],
            "title": work["title"],
            "isrc": work["isrc"],
            "iswc": work["iswc"],
            "format": work["format"],
            "created_at": work["created_at"]
        }

    async def _submit_inquiry(self, args: dict) -> dict:
        """Submit a full licensing inquiry."""
        # Check consent
        consent_result = self.db.check_consent(
            creator_id=args["creator_id"],
            use_category=args["use_category"],
            requestor=args.get("requestor_name"),
            context=args.get("context"),
            territory=args.get("territory", "WW"),
            offered_amount=args.get("offered_amount")
        )

        # Log inquiry
        inquiry_id = self.db.log_inquiry(
            creator_id=args["creator_id"],
            requestor_name=args["requestor_name"],
            use_category=args["use_category"],
            decision=consent_result["decision"],
            reasons=consent_result["reasons"],
            work_id=args.get("work_id"),
            requestor_email=args.get("requestor_email"),
            territory=args.get("territory", "WW"),
            context=args.get("context"),
            offered_amount=args.get("offered_amount")
        )

        # Log transaction
        self.db.log_transaction(
            "inquiry_submitted",
            {
                "inquiry_id": inquiry_id,
                "creator_id": args["creator_id"],
                "requestor": args["requestor_name"],
                "use_category": args["use_category"],
                "decision": consent_result["decision"]
            },
            entity_id=inquiry_id,
            entity_type="inquiry"
        )

        # Determine emoji for decision
        decision = consent_result["decision"]
        if decision in ["allowed", "allowed_terms"]:
            emoji = "✅"
            status = "APPROVED"
        elif decision in ["requires_approval", "negotiable"]:
            emoji = "⏳"
            status = "PENDING REVIEW"
        else:
            emoji = "❌"
            status = "DENIED"

        return {
            "inquiry_id": inquiry_id,
            "status": status,
            "decision": decision,
            "emoji": emoji,
            "reasons": consent_result["reasons"],
            "compensation": consent_result.get("compensation"),
            "requestor": args["requestor_name"],
            "use_category": args["use_category"],
            "message": f"{emoji} Inquiry {status}: {consent_result['reasons'][0] if consent_result['reasons'] else decision}"
        }

    async def _get_registry_stats(self, args: dict) -> dict:
        """Get registry statistics."""
        stats = self.db.get_stats()

        # Verify transaction log
        valid, issues = self.db.verify_transaction_log()

        return {
            **stats,
            "transaction_log_valid": valid,
            "transaction_log_issues": issues if not valid else None
        }

    async def run(self):
        """Run the MCP server."""
        if not MCP_AVAILABLE:
            print("MCP not available — cannot run server")
            return

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


# ═══════════════════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════════════════

async def demo():
    """Run a demo of the NOIZY Fish MCP service."""
    print("\n" + "=" * 70)
    print("NOIZY FISH MCP SERVICE — DEMO")
    print("=" * 70)

    service = NoizyFishMCP(db_path=":memory:")

    # Register creators
    print("\n" + "─" * 50)
    print("REGISTERING CREATORS")
    print("─" * 50)

    sarah = await service._register_creator({
        "display_name": "Sarah Chen",
        "creator_types": ["composer", "songwriter"],
        "ipi_number": "00123456789",
        "pro_membership": "ASCAP",
        "default_consent": "requires_approval"
    })
    print(f"✓ {sarah['display_name']}: {sarah['noizy_id']}")

    marcus = await service._register_creator({
        "display_name": "Marcus Reed",
        "creator_types": ["voice_actor", "performer"],
        "default_consent": "requires_approval"
    })
    print(f"✓ {marcus['display_name']}: {marcus['noizy_id']}")

    nova = await service._register_creator({
        "display_name": "DJ Nova",
        "creator_types": ["producer", "dj"],
        "default_consent": "negotiable"
    })
    print(f"✓ {nova['display_name']}: {nova['noizy_id']}")

    # Set consent rules
    print("\n" + "─" * 50)
    print("SETTING CONSENT RULES")
    print("─" * 50)

    # Sarah: AI training denied
    await service._update_consent_rule({
        "creator_id": sarah["creator_id"],
        "use_category": "ai_training",
        "decision": "denied"
    })
    print(f"✓ Sarah: AI training → DENIED")

    # Sarah: Sync film with minimum
    await service._update_consent_rule({
        "creator_id": sarah["creator_id"],
        "use_category": "sync_film",
        "decision": "allowed_terms",
        "minimum_amount": 10000.00
    })
    print(f"✓ Sarah: Sync film → $10K minimum")

    # Marcus: Voice clone denied
    await service._update_consent_rule({
        "creator_id": marcus["creator_id"],
        "use_category": "ai_voice_clone",
        "decision": "denied"
    })
    print(f"✓ Marcus: Voice cloning → DENIED")

    # Nova: AI training allowed at premium
    await service._update_consent_rule({
        "creator_id": nova["creator_id"],
        "use_category": "ai_training",
        "decision": "allowed_terms",
        "minimum_amount": 50000.00
    })
    print(f"✓ Nova: AI training → $50K minimum")

    # Submit inquiries
    print("\n" + "─" * 50)
    print("LICENSING INQUIRIES")
    print("─" * 50)

    inquiries = [
        {
            "creator_id": sarah["creator_id"],
            "requestor_name": "Indie Film Studio",
            "use_category": "sync_film",
            "offered_amount": 15000.00,
            "context": "Documentary score"
        },
        {
            "creator_id": sarah["creator_id"],
            "requestor_name": "AI Music Corp",
            "use_category": "ai_training",
            "offered_amount": 100000.00,
            "context": "Training data for music generation"
        },
        {
            "creator_id": marcus["creator_id"],
            "requestor_name": "VoiceAI Inc",
            "use_category": "ai_voice_clone",
            "offered_amount": 50000.00,
            "context": "Clone voice for AI assistant"
        },
        {
            "creator_id": nova["creator_id"],
            "requestor_name": "AI Music Lab",
            "use_category": "ai_training",
            "offered_amount": 60000.00,
            "context": "Beat generation model training"
        }
    ]

    for inq in inquiries:
        result = await service._submit_inquiry(inq)
        creator = await service._get_creator({"creator_id": inq["creator_id"]})
        print(f"\n{result['emoji']} {creator['display_name']} — {inq['use_category']}")
        print(f"   Requestor: {inq['requestor_name']}")
        print(f"   Offer: ${inq.get('offered_amount', 0):,.2f}")
        print(f"   Decision: {result['status']}")
        print(f"   Reason: {result['reasons'][0]}")

    # Stats
    print("\n" + "─" * 50)
    print("REGISTRY STATS")
    print("─" * 50)

    stats = await service._get_registry_stats({})
    print(f"  Creators: {stats['creators']}")
    print(f"  Works: {stats['works']}")
    print(f"  Consent Rules: {stats['consent_rules']}")
    print(f"  Inquiries: {stats['inquiries']}")
    print(f"  Transaction Log: {stats['transaction_log_entries']} entries")
    print(f"  Log Integrity: {'✓ Valid' if stats['transaction_log_valid'] else '✗ Invalid'}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo())
    elif MCP_AVAILABLE:
        service = NoizyFishMCP()
        asyncio.run(service.run())
    else:
        print("Run with --demo for standalone demo")
        asyncio.run(demo())
