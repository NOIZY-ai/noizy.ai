"""
NOIZY.ai Creator Consent Registry Schema
=========================================
The data structures that protect creator rights.

Every creator has a consent registry that defines:
- What uses are allowed
- What price points apply
- What restrictions exist
- Who gets paid and how much

This is the source of truth. Nothing happens without consent verification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class UseType(Enum):
    """Types of usage that can be licensed."""
    STREAMING = "streaming"              # Spotify, Apple Music, etc.
    SYNC = "sync"                        # Film, TV, ads, games
    SAMPLE = "sample"                    # Used in another work
    REMIX = "remix"                      # Derivative work
    COVER = "cover"                      # Re-recording
    AI_TRAINING = "ai_training"          # ML model training
    AI_GENERATION = "ai_generation"      # AI-generated derivatives
    BROADCAST = "broadcast"              # Radio, TV broadcast
    LIVE_PERFORMANCE = "live_performance"
    MERCHANDISE = "merchandise"          # Physical goods
    NFT = "nft"                          # Blockchain/NFT use
    EDUCATIONAL = "educational"          # Schools, courses
    NON_PROFIT = "non_profit"            # Charity, non-commercial
    PERSONAL = "personal"                # Personal/private use
    COMMERCIAL = "commercial"            # General commercial use


class ConsentStatus(Enum):
    """Consent decision states."""
    ALLOWED = "allowed"                  # Explicitly permitted
    DENIED = "denied"                    # Explicitly forbidden
    REQUIRES_APPROVAL = "requires_approval"  # Human review needed
    NEGOTIABLE = "negotiable"            # Open to discussion
    NOT_SET = "not_set"                  # No preference recorded


class LicenseType(Enum):
    """Types of licenses that can be granted."""
    EXCLUSIVE = "exclusive"              # Only one licensee
    NON_EXCLUSIVE = "non_exclusive"      # Multiple licensees OK
    ONE_TIME = "one_time"                # Single use
    PERPETUAL = "perpetual"              # Forever
    TIME_LIMITED = "time_limited"        # Specific duration
    TERRITORY_LIMITED = "territory"       # Geographic limits


class RoyaltyType(Enum):
    """How royalties are calculated."""
    FLAT_FEE = "flat_fee"                # One-time payment
    PERCENTAGE = "percentage"            # % of revenue
    PER_USE = "per_use"                  # Per stream/play/view
    ADVANCE_PLUS_ROYALTY = "advance_royalty"  # Upfront + ongoing
    REVENUE_SHARE = "revenue_share"      # Split of proceeds


@dataclass
class RoyaltySplit:
    """Who gets paid and how much."""
    recipient_id: str                    # Creator/collaborator ID
    recipient_name: str
    recipient_email: str
    percentage: float                    # Their share (0-100)
    role: str                            # songwriter, producer, etc.
    payment_method: Optional[str] = None # How they get paid


@dataclass
class PricePoint:
    """Pricing for a specific use type."""
    use_type: UseType
    royalty_type: RoyaltyType
    minimum_fee: float                   # Floor price
    preferred_fee: Optional[float] = None
    percentage_rate: Optional[float] = None  # If percentage-based
    per_use_rate: Optional[float] = None     # If per-use
    currency: str = "USD"
    notes: Optional[str] = None


@dataclass
class UseRestriction:
    """Restrictions on how work can be used."""
    use_type: UseType
    status: ConsentStatus
    restrictions: list[str] = field(default_factory=list)  # Specific limits
    excluded_parties: list[str] = field(default_factory=list)  # Banned licensees
    excluded_contexts: list[str] = field(default_factory=list)  # No guns, no politics, etc.
    requires_credit: bool = True
    credit_format: Optional[str] = None  # How to credit
    notes: Optional[str] = None


@dataclass
class ConsentRegistry:
    """
    The Creator's Consent Registry
    ===============================
    This is the complete record of a creator's consent preferences.
    Every licensing decision flows through this.
    """
    # Identity
    registry_id: str = field(default_factory=lambda: str(uuid4()))
    creator_id: str = ""
    creator_name: str = ""
    creator_email: str = ""

    # Work identification
    work_id: str = ""                    # Unique ID for the work
    work_title: str = ""
    work_type: str = ""                  # song, beat, sample, etc.
    isrc: Optional[str] = None           # International Standard Recording Code
    iswc: Optional[str] = None           # International Standard Musical Work Code

    # Ownership & splits
    royalty_splits: list[RoyaltySplit] = field(default_factory=list)

    # Consent settings per use type
    use_restrictions: list[UseRestriction] = field(default_factory=list)

    # Pricing
    price_points: list[PricePoint] = field(default_factory=list)

    # Global settings
    default_consent: ConsentStatus = ConsentStatus.REQUIRES_APPROVAL
    auto_approve_under: Optional[float] = None  # Auto-approve requests under $X
    auto_approve_types: list[UseType] = field(default_factory=list)

    # Notifications
    notify_on_inquiry: bool = True
    notify_on_approval: bool = True
    notify_on_decline: bool = True
    notify_on_violation: bool = True

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def get_consent_for_use(self, use_type: UseType) -> UseRestriction:
        """Get consent settings for a specific use type."""
        for restriction in self.use_restrictions:
            if restriction.use_type == use_type:
                return restriction
        # Return default if not explicitly set
        return UseRestriction(
            use_type=use_type,
            status=self.default_consent
        )

    def get_price_for_use(self, use_type: UseType) -> Optional[PricePoint]:
        """Get pricing for a specific use type."""
        for price in self.price_points:
            if price.use_type == use_type:
                return price
        return None

    def is_party_excluded(self, party_name: str) -> bool:
        """Check if a party is banned from licensing."""
        for restriction in self.use_restrictions:
            if party_name.lower() in [p.lower() for p in restriction.excluded_parties]:
                return True
        return False

    def is_context_excluded(self, context: str) -> bool:
        """Check if a context/use case is banned."""
        for restriction in self.use_restrictions:
            for excluded in restriction.excluded_contexts:
                if excluded.lower() in context.lower():
                    return True
        return False


@dataclass
class LicensingInquiry:
    """
    An incoming licensing request.
    This is what we verify against the consent registry.
    """
    inquiry_id: str = field(default_factory=lambda: str(uuid4()))

    # Who's asking
    requestor_name: str = ""
    requestor_email: str = ""
    requestor_company: Optional[str] = None

    # What they want
    work_id: str = ""
    work_title: str = ""
    use_type: UseType = UseType.COMMERCIAL
    use_description: str = ""            # Plain English description

    # Context
    project_name: Optional[str] = None   # Film title, ad campaign, etc.
    project_description: Optional[str] = None
    territory: str = "worldwide"
    duration: Optional[str] = None       # How long they need it

    # Offer
    offered_fee: Optional[float] = None
    offered_terms: Optional[str] = None

    # Metadata
    received_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "email"                # email, form, api, etc.
    raw_message: Optional[str] = None    # Original inquiry text


@dataclass
class LicensingDecision:
    """
    The result of verifying an inquiry against consent.
    This is what gets communicated back.
    """
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    inquiry_id: str = ""
    registry_id: str = ""

    # Decision
    status: ConsentStatus = ConsentStatus.NOT_SET
    approved: bool = False

    # If approved
    license_type: Optional[LicenseType] = None
    fee: Optional[float] = None
    royalty_terms: Optional[str] = None
    usage_boundaries: list[str] = field(default_factory=list)
    credit_requirements: Optional[str] = None

    # If declined
    decline_reason: Optional[str] = None
    consent_rules_applied: list[str] = field(default_factory=list)

    # If needs review
    review_reason: Optional[str] = None

    # Metadata
    decided_at: datetime = field(default_factory=datetime.utcnow)
    decided_by: str = "automated"        # automated or human

    # Providence chain
    providence_hash: Optional[str] = None


@dataclass
class CreatorReceipt:
    """
    Human-readable record sent to creator.
    Full transparency on what happened.
    """
    receipt_id: str = field(default_factory=lambda: str(uuid4()))

    # Context
    creator_name: str = ""
    creator_email: str = ""
    work_title: str = ""

    # What happened
    inquiry_summary: str = ""            # Plain English: who wanted what
    decision_summary: str = ""           # Plain English: what we decided

    # Details
    requestor_name: str = ""
    requestor_company: Optional[str] = None
    use_type: str = ""
    use_description: str = ""

    # Outcome
    approved: bool = False
    fee_if_approved: Optional[float] = None
    terms_if_approved: Optional[str] = None
    decline_reason_if_declined: Optional[str] = None

    # Consent rules that applied
    consent_rules_applied: list[str] = field(default_factory=list)

    # Transparency
    full_inquiry_text: Optional[str] = None
    full_decision_text: Optional[str] = None

    # Timestamps
    inquiry_received: datetime = field(default_factory=datetime.utcnow)
    decision_made: datetime = field(default_factory=datetime.utcnow)
    receipt_sent: datetime = field(default_factory=datetime.utcnow)

    # Providence
    providence_hash: Optional[str] = None
    providence_link: Optional[str] = None

    def to_email_body(self) -> str:
        """Generate human-readable email content."""
        status = "APPROVED" if self.approved else "DECLINED"

        body = f"""
═══════════════════════════════════════════════════════════════
LICENSING INQUIRY RECEIPT — {self.work_title}
═══════════════════════════════════════════════════════════════

Hi {self.creator_name},

Here's what just happened with your work:

WHO ASKED:
  • Name: {self.requestor_name}
  • Company: {self.requestor_company or 'Not specified'}
  • Email: (on file)

WHAT THEY WANTED:
  • Work: "{self.work_title}"
  • Use Type: {self.use_type}
  • Description: {self.use_description}

OUR DECISION: {status}
"""

        if self.approved:
            body += f"""
TERMS:
  • Fee: ${self.fee_if_approved:,.2f} USD
  • Terms: {self.terms_if_approved}

YOUR CONSENT RULES THAT APPLIED:
"""
        else:
            body += f"""
REASON:
  {self.decline_reason_if_declined}

YOUR CONSENT RULES THAT PROTECTED YOU:
"""

        for rule in self.consent_rules_applied:
            body += f"  • {rule}\n"

        body += f"""
───────────────────────────────────────────────────────────────
TRANSPARENCY RECORD
───────────────────────────────────────────────────────────────

This decision was made based entirely on YOUR consent settings.
No hidden negotiations. No mystery deals.

Providence Record: {self.providence_hash or 'Pending'}
View Full Record: {self.providence_link or 'Link pending'}

Questions? Reply to this email.

— NOIZY.ai Consent Protection System
═══════════════════════════════════════════════════════════════
"""
        return body
