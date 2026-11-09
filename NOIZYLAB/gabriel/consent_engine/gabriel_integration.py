"""
Gabriel MCP Integration for Consent Engine
==========================================
Connects the consent engine to Gabriel MCP for:
- Consent registry queries
- Providence chain storage
- Creator notifications
- Email handling
"""

from typing import Optional, Any
from dataclasses import asdict
import json

from .schema import ConsentRegistry, LicensingInquiry, UseType, ConsentStatus, UseRestriction, PricePoint, RoyaltySplit, RoyaltyType


class GabrielConsentTools:
    """
    MCP tools for consent engine operations.
    These get registered with Gabriel MCP server.
    """

    TOOLS = [
        {
            "name": "consent_registry_query",
            "description": "Query a creator's consent registry by work ID",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "work_id": {
                        "type": "string",
                        "description": "The unique ID of the work"
                    }
                },
                "required": ["work_id"]
            }
        },
        {
            "name": "consent_registry_update",
            "description": "Update a creator's consent registry",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "work_id": {"type": "string"},
                    "creator_id": {"type": "string"},
                    "updates": {"type": "object"}
                },
                "required": ["work_id", "updates"]
            }
        },
        {
            "name": "consent_registry_create",
            "description": "Create a new consent registry for a work",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "creator_id": {"type": "string"},
                    "creator_name": {"type": "string"},
                    "creator_email": {"type": "string"},
                    "work_id": {"type": "string"},
                    "work_title": {"type": "string"},
                    "work_type": {"type": "string"}
                },
                "required": ["creator_id", "creator_name", "work_id", "work_title"]
            }
        },
        {
            "name": "licensing_inquiry_process",
            "description": "Process a licensing inquiry against consent registry",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "requestor_name": {"type": "string"},
                    "requestor_email": {"type": "string"},
                    "requestor_company": {"type": "string"},
                    "work_id": {"type": "string"},
                    "use_type": {"type": "string"},
                    "use_description": {"type": "string"},
                    "offered_fee": {"type": "number"}
                },
                "required": ["requestor_name", "requestor_email", "work_id", "use_type"]
            }
        },
        {
            "name": "providence_query",
            "description": "Query the providence chain for a work's history",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "work_id": {"type": "string"},
                    "record_type": {"type": "string"}
                },
                "required": ["work_id"]
            }
        },
        {
            "name": "providence_sync",
            "description": "Sync a providence record to distributed storage",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "record": {"type": "object"}
                },
                "required": ["record"]
            }
        }
    ]

    def __init__(self, storage_backend=None):
        self.storage = storage_backend or InMemoryStorage()

    async def handle_tool_call(self, name: str, arguments: dict) -> Any:
        """Route tool calls to appropriate handlers."""
        handlers = {
            "consent_registry_query": self._query_registry,
            "consent_registry_update": self._update_registry,
            "consent_registry_create": self._create_registry,
            "licensing_inquiry_process": self._process_inquiry,
            "providence_query": self._query_providence,
            "providence_sync": self._sync_providence,
        }

        handler = handlers.get(name)
        if handler:
            return await handler(arguments)
        return {"error": f"Unknown tool: {name}"}

    async def _query_registry(self, args: dict) -> Optional[dict]:
        """Query consent registry by work ID."""
        work_id = args["work_id"]
        registry = await self.storage.get_registry(work_id)
        if registry:
            return asdict(registry)
        return None

    async def _update_registry(self, args: dict) -> dict:
        """Update an existing consent registry."""
        work_id = args["work_id"]
        updates = args["updates"]

        registry = await self.storage.get_registry(work_id)
        if not registry:
            return {"error": "Registry not found"}

        # Apply updates
        for key, value in updates.items():
            if hasattr(registry, key):
                setattr(registry, key, value)

        await self.storage.save_registry(registry)
        return {"success": True, "work_id": work_id}

    async def _create_registry(self, args: dict) -> dict:
        """Create a new consent registry."""
        registry = ConsentRegistry(
            creator_id=args["creator_id"],
            creator_name=args["creator_name"],
            creator_email=args.get("creator_email", ""),
            work_id=args["work_id"],
            work_title=args["work_title"],
            work_type=args.get("work_type", "song")
        )

        await self.storage.save_registry(registry)
        return {"success": True, "registry_id": registry.registry_id}

    async def _process_inquiry(self, args: dict) -> dict:
        """Process a licensing inquiry."""
        from .handlers.licensing_inquiry import LicensingInquiryHandler

        inquiry = LicensingInquiry(
            requestor_name=args["requestor_name"],
            requestor_email=args["requestor_email"],
            requestor_company=args.get("requestor_company"),
            work_id=args["work_id"],
            work_title=args.get("work_title", ""),
            use_type=UseType(args["use_type"]),
            use_description=args.get("use_description", ""),
            offered_fee=args.get("offered_fee")
        )

        handler = LicensingInquiryHandler()
        decision = await handler.handle_inquiry(inquiry)

        return asdict(decision)

    async def _query_providence(self, args: dict) -> list:
        """Query providence chain."""
        work_id = args["work_id"]
        records = await self.storage.get_providence_records(work_id)
        return [r.to_dict() for r in records]

    async def _sync_providence(self, args: dict) -> dict:
        """Sync providence record to storage."""
        record = args["record"]
        await self.storage.save_providence_record(record)
        return {"success": True}


class InMemoryStorage:
    """In-memory storage for testing."""

    def __init__(self):
        self.registries: dict[str, ConsentRegistry] = {}
        self.providence_records: list[dict] = []

    async def get_registry(self, work_id: str) -> Optional[ConsentRegistry]:
        return self.registries.get(work_id)

    async def save_registry(self, registry: ConsentRegistry):
        self.registries[registry.work_id] = registry

    async def get_providence_records(self, work_id: str) -> list:
        return [r for r in self.providence_records if r.get("work_id") == work_id]

    async def save_providence_record(self, record: dict):
        self.providence_records.append(record)


def create_test_registry() -> ConsentRegistry:
    """Create a test consent registry for demo purposes."""
    return ConsentRegistry(
        creator_id="creator_001",
        creator_name="MC96",
        creator_email="mc96@noizy.ai",
        work_id="work_001",
        work_title="Midnight Protocol",
        work_type="song",
        royalty_splits=[
            RoyaltySplit(
                recipient_id="creator_001",
                recipient_name="MC96",
                recipient_email="mc96@noizy.ai",
                percentage=100.0,
                role="artist"
            )
        ],
        use_restrictions=[
            UseRestriction(
                use_type=UseType.STREAMING,
                status=ConsentStatus.ALLOWED,
                requires_credit=True,
                credit_format="Music by MC96"
            ),
            UseRestriction(
                use_type=UseType.SYNC,
                status=ConsentStatus.ALLOWED,
                restrictions=["No political ads", "No tobacco/alcohol"],
                excluded_contexts=["political", "tobacco", "vape", "gambling"],
                requires_credit=True
            ),
            UseRestriction(
                use_type=UseType.AI_TRAINING,
                status=ConsentStatus.DENIED,
                notes="Never allow AI training on my voice/music"
            ),
            UseRestriction(
                use_type=UseType.SAMPLE,
                status=ConsentStatus.REQUIRES_APPROVAL,
                notes="Review all sample requests"
            ),
            UseRestriction(
                use_type=UseType.COMMERCIAL,
                status=ConsentStatus.ALLOWED,
                restrictions=["Must credit artist", "No edits without approval"]
            )
        ],
        price_points=[
            PricePoint(
                use_type=UseType.SYNC,
                royalty_type=RoyaltyType.FLAT_FEE,
                minimum_fee=5000.00,
                preferred_fee=10000.00,
                notes="Sync licensing - film/TV/ads"
            ),
            PricePoint(
                use_type=UseType.SAMPLE,
                royalty_type=RoyaltyType.ADVANCE_PLUS_ROYALTY,
                minimum_fee=2500.00,
                percentage_rate=3.0,
                notes="Sample clearance"
            ),
            PricePoint(
                use_type=UseType.COMMERCIAL,
                royalty_type=RoyaltyType.FLAT_FEE,
                minimum_fee=1000.00
            )
        ],
        default_consent=ConsentStatus.REQUIRES_APPROVAL,
        auto_approve_under=None,  # No auto-approve
        notify_on_inquiry=True,
        notify_on_approval=True,
        notify_on_decline=True,
        notify_on_violation=True
    )
