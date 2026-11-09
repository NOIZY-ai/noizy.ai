"""
NOIZY Fish — Smart License Contracts
=====================================

Programmable license templates with:
- Automatic term enforcement
- Royalty split calculation
- Geographic restrictions
- Time-based conditions
- Usage limits
- Auto-renewal/termination

Think of these as "smart contracts" for music licensing —
executable rules that fire automatically based on conditions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable
from uuid import uuid4
import json
import hashlib

from .tracking.royalty_engine import (
    License, LicenseStatus, RoyaltySplit,
    RoyaltyEngine, UsageEvent, UsageEventType
)


# ═══════════════════════════════════════════════════════════════════════════
# License Template Types
# ═══════════════════════════════════════════════════════════════════════════

class LicenseType(Enum):
    """Types of licenses."""
    SYNC_STANDARD = "sync_standard"          # Standard sync license
    SYNC_MICRO = "sync_micro"                # Micro-budget sync
    SYNC_BLANKET = "sync_blanket"            # Blanket/catalog license
    SAMPLE_CLEAR = "sample_clear"            # Sample clearance
    REMIX_OFFICIAL = "remix_official"        # Official remix
    STREAMING_DISTRO = "streaming_distro"    # Streaming distribution
    AI_TRAINING = "ai_training"              # AI training license
    VOICE_SESSION = "voice_session"          # Voice actor session
    BUYOUT = "buyout"                        # Full rights buyout


# ═══════════════════════════════════════════════════════════════════════════
# License Template
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class LicenseCondition:
    """A condition that must be met for the license to be valid."""
    condition_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    condition_type: str = ""  # territory, time, usage_count, payment, etc.
    operator: str = "=="     # ==, !=, <, >, <=, >=, in, not_in
    value: any = None
    description: str = ""

    def evaluate(self, context: dict) -> tuple[bool, str]:
        """Evaluate condition against context."""
        actual = context.get(self.condition_type)

        if self.operator == "==":
            result = actual == self.value
        elif self.operator == "!=":
            result = actual != self.value
        elif self.operator == "<":
            result = actual < self.value
        elif self.operator == ">":
            result = actual > self.value
        elif self.operator == "<=":
            result = actual <= self.value
        elif self.operator == ">=":
            result = actual >= self.value
        elif self.operator == "in":
            result = actual in self.value
        elif self.operator == "not_in":
            result = actual not in self.value
        else:
            return False, f"Unknown operator: {self.operator}"

        message = f"{self.name}: {'passed' if result else 'failed'}"
        return result, message


@dataclass
class LicenseAction:
    """An action triggered by the license."""
    action_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    action_type: str = ""  # notify, terminate, renew, pay, restrict
    parameters: dict = field(default_factory=dict)
    trigger: str = ""      # on_start, on_use, on_expiry, on_violation

    def execute(self, context: dict) -> dict:
        """Execute the action."""
        result = {
            "action": self.name,
            "type": self.action_type,
            "trigger": self.trigger,
            "executed_at": datetime.utcnow().isoformat()
        }

        if self.action_type == "notify":
            result["notification"] = self.parameters.get("message", "License notification")
            result["recipient"] = self.parameters.get("recipient")

        elif self.action_type == "pay":
            result["amount"] = self.parameters.get("amount", 0)
            result["recipient"] = self.parameters.get("recipient")

        elif self.action_type == "terminate":
            result["reason"] = self.parameters.get("reason", "Condition not met")

        return result


@dataclass
class LicenseTemplate:
    """
    A reusable license template.
    Contains standard terms, conditions, splits, and actions.
    """
    template_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    license_type: LicenseType = LicenseType.SYNC_STANDARD

    # Terms
    default_fee: float = 0.0
    fee_type: str = "flat_fee"  # flat_fee, percentage, per_use
    percentage_rate: Optional[float] = None
    per_use_rate: Optional[float] = None

    # Duration
    default_duration_days: int = 365
    perpetual: bool = False
    auto_renew: bool = False

    # Geographic
    default_territories: list[str] = field(default_factory=lambda: ["WW"])
    excluded_territories: list[str] = field(default_factory=list)

    # Usage
    usage_limit: Optional[int] = None  # Max number of uses
    media_types: list[str] = field(default_factory=list)  # film, tv, web, etc.

    # Splits
    default_splits: list[dict] = field(default_factory=list)

    # Conditions
    conditions: list[LicenseCondition] = field(default_factory=list)

    # Actions
    actions: list[LicenseAction] = field(default_factory=list)

    # Credit
    requires_credit: bool = True
    credit_format: str = "{artist_name}"

    # Legal
    legal_template: Optional[str] = None

    def create_license(
        self,
        work_id: str,
        work_title: str,
        licensor_id: str,
        licensee_name: str,
        licensee_email: str,
        fee_override: Optional[float] = None,
        duration_override: Optional[int] = None,
        territories_override: Optional[list[str]] = None,
        splits_override: Optional[list[dict]] = None
    ) -> License:
        """Create a license from this template."""
        # Calculate dates
        start_date = datetime.utcnow()
        duration = duration_override or self.default_duration_days
        end_date = start_date + timedelta(days=duration) if not self.perpetual else None

        # Build splits
        splits_data = splits_override or self.default_splits
        royalty_splits = [
            RoyaltySplit(
                recipient_id=s.get("recipient_id", licensor_id),
                recipient_name=s.get("recipient_name", ""),
                recipient_email=s.get("recipient_email", ""),
                percentage=s.get("percentage", 100),
                role=s.get("role", "licensor")
            )
            for s in splits_data
        ]

        # If no splits defined, 100% to licensor
        if not royalty_splits:
            royalty_splits = [
                RoyaltySplit(
                    recipient_id=licensor_id,
                    recipient_name="",
                    recipient_email="",
                    percentage=100.0,
                    role="licensor"
                )
            ]

        license = License(
            work_id=work_id,
            work_title=work_title,
            licensor_id=licensor_id,
            licensee_name=licensee_name,
            licensee_email=licensee_email,
            use_type=self.license_type.value,
            use_description=self.description,
            territory=",".join(territories_override or self.default_territories),
            start_date=start_date,
            end_date=end_date,
            perpetual=self.perpetual,
            fee_type=self.fee_type,
            fee_amount=fee_override or self.default_fee,
            percentage_rate=self.percentage_rate,
            per_use_rate=self.per_use_rate,
            credit_required=self.requires_credit,
            credit_format=self.credit_format,
            royalty_splits=royalty_splits,
            status=LicenseStatus.PENDING
        )

        return license

    def validate_use(self, context: dict) -> tuple[bool, list[str]]:
        """Validate a use against license conditions."""
        passed = []
        failed = []

        for condition in self.conditions:
            result, message = condition.evaluate(context)
            if result:
                passed.append(message)
            else:
                failed.append(message)

        return len(failed) == 0, failed if failed else passed


# ═══════════════════════════════════════════════════════════════════════════
# Pre-built Templates
# ═══════════════════════════════════════════════════════════════════════════

SMART_LICENSE_TEMPLATES = {
    "sync_standard": LicenseTemplate(
        name="Standard Sync License",
        description="Standard synchronization license for film/TV/web",
        license_type=LicenseType.SYNC_STANDARD,
        default_fee=5000.0,
        fee_type="flat_fee",
        default_duration_days=365 * 5,  # 5 years
        default_territories=["WW"],
        media_types=["film", "television", "web"],
        requires_credit=True,
        credit_format="Music: {artist_name}",
        conditions=[
            LicenseCondition(
                name="Territory Check",
                condition_type="territory",
                operator="in",
                value=["WW", "US", "CA", "GB", "EU"],
                description="Must be in approved territories"
            )
        ],
        actions=[
            LicenseAction(
                name="Notify on Use",
                action_type="notify",
                trigger="on_use",
                parameters={"message": "Your sync has been used"}
            )
        ]
    ),

    "sync_micro": LicenseTemplate(
        name="Micro-Budget Sync License",
        description="Sync license for indie/micro-budget productions (<$100K budget)",
        license_type=LicenseType.SYNC_MICRO,
        default_fee=500.0,
        fee_type="flat_fee",
        default_duration_days=365 * 3,  # 3 years
        default_territories=["WW"],
        media_types=["film", "web", "student"],
        requires_credit=True,
        credit_format="Music by {artist_name}",
        conditions=[
            LicenseCondition(
                name="Budget Check",
                condition_type="budget",
                operator="<",
                value=100000,
                description="Budget must be under $100K"
            )
        ]
    ),

    "sync_blanket": LicenseTemplate(
        name="Blanket/Catalog License",
        description="Annual blanket license for entire catalog",
        license_type=LicenseType.SYNC_BLANKET,
        default_fee=25000.0,
        fee_type="flat_fee",
        default_duration_days=365,
        auto_renew=True,
        default_territories=["WW"],
        media_types=["all"],
        usage_limit=None,  # Unlimited
        requires_credit=True,
        actions=[
            LicenseAction(
                name="Renewal Notice",
                action_type="notify",
                trigger="on_expiry",
                parameters={"message": "Blanket license expires in 30 days", "days_before": 30}
            )
        ]
    ),

    "sample_clearance": LicenseTemplate(
        name="Sample Clearance License",
        description="Clearance for using a sample in a new work",
        license_type=LicenseType.SAMPLE_CLEAR,
        default_fee=2500.0,
        fee_type="advance_royalty",
        percentage_rate=2.0,  # 2% of revenue
        perpetual=True,
        default_territories=["WW"],
        requires_credit=True,
        credit_format="Contains sample from {artist_name}",
        conditions=[
            LicenseCondition(
                name="Sample Duration",
                condition_type="sample_seconds",
                operator="<=",
                value=30,
                description="Sample must be 30 seconds or less"
            )
        ]
    ),

    "remix_official": LicenseTemplate(
        name="Official Remix License",
        description="License for creating an official remix",
        license_type=LicenseType.REMIX_OFFICIAL,
        default_fee=1000.0,
        fee_type="revenue_share",
        percentage_rate=50.0,  # 50/50 split
        perpetual=True,
        default_territories=["WW"],
        requires_credit=True,
        credit_format="{artist_name} ({remixer_name} Remix)",
        default_splits=[
            {"recipient_role": "original", "percentage": 50},
            {"recipient_role": "remixer", "percentage": 50}
        ]
    ),

    "streaming_distro": LicenseTemplate(
        name="Streaming Distribution License",
        description="License for digital streaming distribution",
        license_type=LicenseType.STREAMING_DISTRO,
        default_fee=0.0,
        fee_type="percentage",
        percentage_rate=70.0,  # 70% artist share
        perpetual=True,
        default_territories=["WW"],
        requires_credit=False,
        actions=[
            LicenseAction(
                name="Monthly Report",
                action_type="notify",
                trigger="monthly",
                parameters={"message": "Monthly streaming report available"}
            )
        ]
    ),

    "ai_training": LicenseTemplate(
        name="AI Training Data License",
        description="License for using work as AI training data",
        license_type=LicenseType.AI_TRAINING,
        default_fee=50000.0,
        fee_type="flat_fee",
        default_duration_days=365 * 3,
        default_territories=["WW"],
        requires_credit=False,
        conditions=[
            LicenseCondition(
                name="Disclosure Required",
                condition_type="ai_disclosure",
                operator="==",
                value=True,
                description="Must disclose use of training data"
            ),
            LicenseCondition(
                name="No Voice Cloning",
                condition_type="use_type",
                operator="not_in",
                value=["voice_clone", "voice_synthesis"],
                description="Cannot be used for voice cloning"
            )
        ]
    ),

    "voice_session": LicenseTemplate(
        name="Voice Session License",
        description="License for voice acting session",
        license_type=LicenseType.VOICE_SESSION,
        default_fee=500.0,
        fee_type="flat_fee",
        perpetual=True,  # Buyout common in games
        default_territories=["WW"],
        media_types=["game", "app", "web"],
        requires_credit=True,
        credit_format="Voice: {artist_name}",
        conditions=[
            LicenseCondition(
                name="No AI Cloning",
                condition_type="ai_use",
                operator="==",
                value=False,
                description="Voice cannot be used for AI cloning"
            )
        ]
    ),

    "buyout": LicenseTemplate(
        name="Full Buyout License",
        description="Complete transfer of rights",
        license_type=LicenseType.BUYOUT,
        default_fee=100000.0,
        fee_type="flat_fee",
        perpetual=True,
        default_territories=["WW"],
        media_types=["all"],
        usage_limit=None,
        requires_credit=False,
        actions=[
            LicenseAction(
                name="Rights Transfer",
                action_type="transfer",
                trigger="on_start",
                parameters={"transfer_type": "full"}
            )
        ]
    )
}


def get_license_template(template_name: str) -> Optional[LicenseTemplate]:
    """Get a license template by name."""
    return SMART_LICENSE_TEMPLATES.get(template_name)


def list_license_templates() -> list[dict]:
    """List all available license templates."""
    return [
        {
            "name": name,
            "display_name": tmpl.name,
            "description": tmpl.description,
            "default_fee": tmpl.default_fee,
            "fee_type": tmpl.fee_type
        }
        for name, tmpl in SMART_LICENSE_TEMPLATES.items()
    ]


# ═══════════════════════════════════════════════════════════════════════════
# License Executor
# ═══════════════════════════════════════════════════════════════════════════

class LicenseExecutor:
    """
    Executes smart license logic.
    Validates conditions, triggers actions, tracks usage.
    """

    def __init__(self, royalty_engine: Optional[RoyaltyEngine] = None):
        self.engine = royalty_engine or RoyaltyEngine()
        self.active_licenses: dict[str, License] = {}
        self.templates: dict[str, LicenseTemplate] = {}

    def create_from_template(
        self,
        template_name: str,
        **kwargs
    ) -> Optional[License]:
        """Create a license from a template."""
        template = SMART_LICENSE_TEMPLATES.get(template_name)
        if not template:
            return None

        license = template.create_license(**kwargs)
        return license

    def activate(self, license: License) -> tuple[bool, str]:
        """Activate a license."""
        if license.status != LicenseStatus.PENDING:
            return False, "License not in pending status"

        license.status = LicenseStatus.ACTIVE
        license.activated_at = datetime.utcnow()

        self.active_licenses[license.license_id] = license
        self.engine.register_license(license)

        return True, "License activated"

    def validate_use(
        self,
        license_id: str,
        context: dict
    ) -> tuple[bool, list[str]]:
        """Validate a use against license terms."""
        license = self.active_licenses.get(license_id)
        if not license:
            return False, ["License not found"]

        if not license.is_active():
            return False, ["License not active"]

        # Check usage limit
        if hasattr(license, 'usage_limit') and license.usage_limit:
            if license.total_uses >= license.usage_limit:
                return False, ["Usage limit reached"]

        # Check territory
        if context.get("territory"):
            allowed = license.territory.split(",")
            if "WW" not in allowed and context["territory"] not in allowed:
                return False, [f"Territory {context['territory']} not licensed"]

        return True, ["Use validated"]

    def record_use(
        self,
        license_id: str,
        event_type: UsageEventType = UsageEventType.SYNC_USE,
        **kwargs
    ) -> Optional[float]:
        """Record a usage event and calculate royalty."""
        event = UsageEvent(
            license_id=license_id,
            event_type=event_type,
            **kwargs
        )
        return self.engine.record_usage(event)

    def check_expiration(self) -> list[str]:
        """Check for expiring licenses."""
        expiring = []
        now = datetime.utcnow()
        warning_period = timedelta(days=30)

        for license_id, license in self.active_licenses.items():
            if license.end_date:
                if license.end_date < now:
                    license.status = LicenseStatus.EXPIRED
                    expiring.append(f"{license_id}: EXPIRED")
                elif license.end_date < now + warning_period:
                    days_left = (license.end_date - now).days
                    expiring.append(f"{license_id}: expires in {days_left} days")

        return expiring


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate smart licenses."""
    print("\n" + "=" * 70)
    print("NOIZY FISH SMART LICENSES — DEMO")
    print("=" * 70)

    executor = LicenseExecutor()

    # List available templates
    print("\n" + "─" * 50)
    print("AVAILABLE LICENSE TEMPLATES")
    print("─" * 50)

    for tmpl in list_license_templates():
        print(f"  • {tmpl['name']}: {tmpl['display_name']}")
        print(f"    Default fee: ${tmpl['default_fee']:,.0f} ({tmpl['fee_type']})")

    # Create licenses from templates
    print("\n" + "─" * 50)
    print("CREATING LICENSES FROM TEMPLATES")
    print("─" * 50)

    # Sync license
    sync_license = executor.create_from_template(
        "sync_standard",
        work_id="work-001",
        work_title="Midnight Sonata",
        licensor_id="creator-001",
        licensee_name="Indie Film Productions",
        licensee_email="licensing@indiefilm.com",
        fee_override=7500.0
    )
    print(f"  ✓ Created: {sync_license.use_type}")
    print(f"    Fee: ${sync_license.fee_amount:,.0f}")
    print(f"    Duration: {(sync_license.end_date - sync_license.start_date).days} days")

    # Sample clearance
    sample_license = executor.create_from_template(
        "sample_clearance",
        work_id="work-002",
        work_title="Classic Funk Loop",
        licensor_id="creator-002",
        licensee_name="Rising Hip-Hop Artist",
        licensee_email="artist@music.com"
    )
    print(f"  ✓ Created: {sample_license.use_type}")
    print(f"    Advance: ${sample_license.fee_amount:,.0f}")
    print(f"    Royalty: {sample_license.percentage_rate}%")

    # Voice session
    voice_license = executor.create_from_template(
        "voice_session",
        work_id="work-003",
        work_title="Commander Rex Voice Pack",
        licensor_id="creator-003",
        licensee_name="GameDev Studios",
        licensee_email="audio@gamedev.com",
        fee_override=2000.0
    )
    print(f"  ✓ Created: {voice_license.use_type}")
    print(f"    Fee: ${voice_license.fee_amount:,.0f}")
    print(f"    Perpetual: {voice_license.perpetual}")

    # Activate and validate
    print("\n" + "─" * 50)
    print("LICENSE ACTIVATION & VALIDATION")
    print("─" * 50)

    success, message = executor.activate(sync_license)
    print(f"  Sync license: {message}")

    # Validate use in US
    valid, reasons = executor.validate_use(
        sync_license.license_id,
        {"territory": "US"}
    )
    print(f"  Use in US: {'✓ Valid' if valid else '✗ Invalid'}")

    # Validate use in excluded territory
    valid, reasons = executor.validate_use(
        sync_license.license_id,
        {"territory": "CN"}
    )
    print(f"  Use in CN: {'✓ Valid' if valid else '✗ Invalid'} ({reasons[0] if reasons else ''})")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
