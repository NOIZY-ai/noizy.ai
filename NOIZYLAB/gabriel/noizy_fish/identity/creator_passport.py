"""
NOIZY Fish — Layer 1: Creator Identity & Consent
=================================================

The Creator Passport is the foundational identity document for every
creator in the NOIZY ecosystem. It captures:

1. WHO the creator is (identity, credentials, linked accounts)
2. WHAT they create (works registered with the system)
3. HOW their work can be used (consent registry)
4. WHEN consent was granted/modified (immutable audit trail)
5. WHERE compensation should flow (payment routing)

This is the "passport" that travels with every piece of content.
When a licensing inquiry comes in, this is what gets queried.

Design Principles:
- Creator-owned: The creator controls their passport
- Privacy-first: Minimal PII, cryptographic protection
- Standards-compatible: Links to ISRC, ISWC, IPI, ISNI, C2PA
- Audit-complete: Every change is logged forever
- Scale-ready: Designed for millions of creators
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
import hashlib
import json

from ..standards import (
    IPI, ISNI, ISRC, ISWC, NoizyID,
    ContributorRole, RightsType, TerritoryCode
)


# ═══════════════════════════════════════════════════════════════════════════
# CREATOR TYPE CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════

class CreatorType(Enum):
    """Types of creators in the NOIZY ecosystem."""
    COMPOSER = "composer"                # Writes music
    LYRICIST = "lyricist"                # Writes words
    SONGWRITER = "songwriter"            # Writes music + words
    PRODUCER = "producer"                # Creates/produces recordings
    PERFORMER = "performer"              # Performs (vocalist, musician)
    VOICE_ACTOR = "voice_actor"          # Voice performance
    SOUND_DESIGNER = "sound_designer"    # Sound effects, ambience
    DJ = "dj"                            # DJ/remix artist
    ENGINEER = "engineer"                # Recording/mixing/mastering
    LABEL = "label"                      # Record label (organization)
    PUBLISHER = "publisher"              # Music publisher (organization)
    COLLECTIVE = "collective"            # Group/band/collective
    AI_ASSISTED = "ai_assisted"          # Human + AI collaboration


class VerificationStatus(Enum):
    """Creator verification levels."""
    UNVERIFIED = "unverified"            # Email only
    EMAIL_VERIFIED = "email_verified"    # Email confirmed
    IDENTITY_VERIFIED = "identity_verified"  # ID check passed
    PRO_VERIFIED = "pro_verified"        # PRO membership confirmed
    FULLY_VERIFIED = "fully_verified"    # All verification complete


# ═══════════════════════════════════════════════════════════════════════════
# CREATOR IDENTITY
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CreatorIdentity:
    """
    Core identity information for a creator.
    This is the "WHO" of the creator passport.
    """
    # Primary identification
    creator_id: str = field(default_factory=lambda: str(uuid4()))
    noizy_id: Optional[NoizyID] = None

    # Display information
    display_name: str = ""               # Public name / artist name
    legal_name: Optional[str] = None     # Real name (private)
    aliases: list[str] = field(default_factory=list)

    # Classification
    creator_types: list[CreatorType] = field(default_factory=list)
    primary_role: Optional[ContributorRole] = None

    # External identifiers (industry standards)
    ipi_number: Optional[IPI] = None     # CISAC IPI
    isni_number: Optional[ISNI] = None   # ISO 27729 ISNI
    pro_membership: Optional[str] = None  # ASCAP, BMI, SESAC, etc.
    pro_member_id: Optional[str] = None

    # Contact (minimal, encrypted in storage)
    email_hash: Optional[str] = None     # SHA-256 of email
    notification_email: Optional[str] = None  # For system notifications

    # Verification
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    verified_at: Optional[datetime] = None
    verification_method: Optional[str] = None

    # Cryptographic identity
    public_key: Optional[str] = None     # For signing claims
    key_fingerprint: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.noizy_id:
            self.noizy_id = NoizyID.generate("CR")
        if self.ipi_number:
            self.noizy_id.ipi = self.ipi_number
        if self.isni_number:
            self.noizy_id.isni = self.isni_number

    def generate_fingerprint(self) -> str:
        """Generate a unique fingerprint for this identity."""
        data = {
            "creator_id": self.creator_id,
            "display_name": self.display_name,
            "ipi": str(self.ipi_number) if self.ipi_number else None,
            "isni": str(self.isni_number) if self.isni_number else None,
            "created_at": self.created_at.isoformat()
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════════════
# CONSENT RULES — The core of the system
# ═══════════════════════════════════════════════════════════════════════════

class UseCategory(Enum):
    """Categories of content use."""
    # Distribution
    STREAMING = "streaming"              # Spotify, Apple Music, etc.
    DOWNLOAD = "download"                # iTunes, Bandcamp, etc.
    PHYSICAL = "physical"                # CD, vinyl, etc.

    # Sync & Media
    SYNC_FILM = "sync_film"              # Feature films
    SYNC_TV = "sync_tv"                  # Television
    SYNC_AD = "sync_ad"                  # Advertising
    SYNC_GAME = "sync_game"              # Video games
    SYNC_TRAILER = "sync_trailer"        # Trailers/promos
    SYNC_SOCIAL = "sync_social"          # Social media content

    # Derivative
    SAMPLE = "sample"                    # Sampling in new work
    REMIX = "remix"                      # Remix/reinterpretation
    COVER = "cover"                      # Cover version
    INTERPOLATION = "interpolation"      # Melodic interpolation
    MASHUP = "mashup"                    # Combined with other works

    # AI & Technology
    AI_TRAINING = "ai_training"          # ML model training data
    AI_GENERATION = "ai_generation"      # AI-generated derivatives
    AI_VOICE_CLONE = "ai_voice_clone"    # Voice cloning
    AI_STYLE_TRANSFER = "ai_style_transfer"  # Style transfer

    # Performance
    LIVE_PERFORMANCE = "live_performance"
    BROADCAST_RADIO = "broadcast_radio"
    BROADCAST_TV = "broadcast_tv"
    PUBLIC_PLACE = "public_place"        # Restaurants, stores, etc.

    # Other
    EDUCATIONAL = "educational"
    NON_PROFIT = "non_profit"
    PERSONAL = "personal"
    MERCHANDISE = "merchandise"
    NFT = "nft"


class ConsentDecision(Enum):
    """Possible consent decisions."""
    ALLOWED = "allowed"                  # Always allowed
    ALLOWED_WITH_TERMS = "allowed_terms" # Allowed if terms met
    REQUIRES_APPROVAL = "requires_approval"  # Case-by-case
    NEGOTIABLE = "negotiable"            # Open to offers
    DENIED = "denied"                    # Never allowed
    NOT_SET = "not_set"                  # No preference


class CompensationType(Enum):
    """How compensation is calculated."""
    FLAT_FEE = "flat_fee"                # One-time payment
    PERCENTAGE = "percentage"            # % of revenue
    PER_USE = "per_use"                  # Per stream/play/view
    ADVANCE_ROYALTY = "advance_royalty"  # Upfront + ongoing
    REVENUE_SHARE = "revenue_share"      # Split proceeds
    FREE = "free"                        # No charge (but track)
    NEGOTIATE = "negotiate"              # Must negotiate


@dataclass
class CompensationTerms:
    """Compensation requirements for a use type."""
    compensation_type: CompensationType
    minimum_amount: Optional[float] = None
    preferred_amount: Optional[float] = None
    percentage_rate: Optional[float] = None  # For percentage-based
    per_use_rate: Optional[float] = None     # For per-use
    currency: str = "USD"
    advance_required: bool = False
    advance_amount: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class ConsentRule:
    """
    A single consent rule for a specific use case.
    This is what gets queried when a licensing inquiry comes in.
    """
    rule_id: str = field(default_factory=lambda: str(uuid4()))

    # What this rule applies to
    use_category: UseCategory = UseCategory.STREAMING
    decision: ConsentDecision = ConsentDecision.NOT_SET

    # Geographic restrictions
    allowed_territories: list[str] = field(default_factory=lambda: ["WW"])
    excluded_territories: list[str] = field(default_factory=list)

    # Duration limits
    duration_limit: Optional[str] = None  # "1 year", "perpetual", etc.
    expiration_date: Optional[datetime] = None

    # Compensation
    compensation: Optional[CompensationTerms] = None

    # Exclusions
    excluded_parties: list[str] = field(default_factory=list)  # Company names
    excluded_contexts: list[str] = field(default_factory=list)  # "political", "tobacco"
    excluded_platforms: list[str] = field(default_factory=list)  # Specific platforms

    # Requirements
    requires_credit: bool = True
    credit_format: Optional[str] = None
    requires_approval_over: Optional[float] = None  # Auto-approve under this amount
    requires_sample_review: bool = False  # Must review how it's used

    # Additional terms
    additional_terms: Optional[str] = None
    contract_template: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None  # Creator ID who set this

    def matches_inquiry(
        self,
        use_category: UseCategory,
        territory: str = "WW",
        requestor: Optional[str] = None,
        context: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Check if this rule matches an inquiry.
        Returns (matches, reason).
        """
        # Check use category
        if self.use_category != use_category:
            return False, "Use category does not match"

        # Check territory
        if territory not in self.allowed_territories and "WW" not in self.allowed_territories:
            return False, f"Territory {territory} not allowed"
        if territory in self.excluded_territories:
            return False, f"Territory {territory} is excluded"

        # Check excluded parties
        if requestor:
            for excluded in self.excluded_parties:
                if excluded.lower() in requestor.lower():
                    return False, f"Requestor matches excluded party: {excluded}"

        # Check excluded contexts
        if context:
            for excluded in self.excluded_contexts:
                if excluded.lower() in context.lower():
                    return False, f"Context matches exclusion: {excluded}"

        # Check expiration
        if self.expiration_date and datetime.utcnow() > self.expiration_date:
            return False, "Rule has expired"

        return True, "Rule matches"


@dataclass
class ConsentRegistry:
    """
    The complete consent registry for a creator.
    Contains all consent rules and default settings.
    """
    registry_id: str = field(default_factory=lambda: str(uuid4()))
    creator_id: str = ""

    # Default consent (applies when no specific rule exists)
    default_decision: ConsentDecision = ConsentDecision.REQUIRES_APPROVAL

    # Rules by use category
    rules: list[ConsentRule] = field(default_factory=list)

    # Global exclusions (apply to ALL use categories)
    global_excluded_parties: list[str] = field(default_factory=list)
    global_excluded_contexts: list[str] = field(default_factory=list)

    # Auto-approval settings
    auto_approve_under: Optional[float] = None  # Auto-approve offers under $X
    auto_approve_categories: list[UseCategory] = field(default_factory=list)

    # Notification preferences
    notify_on_inquiry: bool = True
    notify_on_auto_approval: bool = True
    notify_on_decline: bool = True
    notify_on_violation: bool = True

    # Metadata
    version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def get_rule_for_use(self, use_category: UseCategory) -> Optional[ConsentRule]:
        """Get the consent rule for a specific use category."""
        for rule in self.rules:
            if rule.use_category == use_category:
                return rule
        return None

    def evaluate_inquiry(
        self,
        use_category: UseCategory,
        territory: str = "WW",
        requestor: Optional[str] = None,
        context: Optional[str] = None,
        offered_amount: Optional[float] = None
    ) -> tuple[ConsentDecision, list[str]]:
        """
        Evaluate an inquiry against this registry.
        Returns (decision, list of reasons).
        """
        reasons = []

        # Check global exclusions first
        if requestor:
            for excluded in self.global_excluded_parties:
                if excluded.lower() in requestor.lower():
                    reasons.append(f"Global exclusion: {excluded}")
                    return ConsentDecision.DENIED, reasons

        if context:
            for excluded in self.global_excluded_contexts:
                if excluded.lower() in context.lower():
                    reasons.append(f"Global context exclusion: {excluded}")
                    return ConsentDecision.DENIED, reasons

        # Find matching rule
        rule = self.get_rule_for_use(use_category)

        if not rule:
            reasons.append(f"No rule for {use_category.value}, using default")
            return self.default_decision, reasons

        # Check rule match
        matches, match_reason = rule.matches_inquiry(
            use_category, territory, requestor, context
        )

        if not matches:
            reasons.append(match_reason)
            return ConsentDecision.DENIED, reasons

        # Check compensation
        if rule.decision == ConsentDecision.ALLOWED_WITH_TERMS:
            if rule.compensation and offered_amount:
                if rule.compensation.minimum_amount:
                    if offered_amount < rule.compensation.minimum_amount:
                        reasons.append(
                            f"Offer ${offered_amount} below minimum ${rule.compensation.minimum_amount}"
                        )
                        return ConsentDecision.DENIED, reasons

        # Check auto-approval
        if rule.decision == ConsentDecision.REQUIRES_APPROVAL:
            if self.auto_approve_under and offered_amount:
                if offered_amount >= self.auto_approve_under:
                    reasons.append(f"Auto-approved: offer meets ${self.auto_approve_under} threshold")
                    return ConsentDecision.ALLOWED, reasons

            if use_category in self.auto_approve_categories:
                reasons.append(f"Auto-approved: {use_category.value} is in auto-approve list")
                return ConsentDecision.ALLOWED, reasons

        reasons.append(f"Rule decision: {rule.decision.value}")
        return rule.decision, reasons


# ═══════════════════════════════════════════════════════════════════════════
# CREATOR PASSPORT — The complete document
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CreatorPassport:
    """
    The Creator Passport — Complete identity and consent document.

    This is the foundational record for every creator in NOIZY Fish.
    It combines:
    - Identity (who they are)
    - Consent (how their work can be used)
    - Works (what they've created)
    - Audit (history of all changes)

    When a licensing inquiry comes in, this passport is queried
    to determine if the use is allowed.
    """
    # Identity
    identity: CreatorIdentity = field(default_factory=CreatorIdentity)

    # Consent registry
    consent: ConsentRegistry = field(default_factory=ConsentRegistry)

    # Works registered (ISRC/ISWC references)
    registered_works: list[str] = field(default_factory=list)  # Work IDs
    registered_recordings: list[str] = field(default_factory=list)  # Recording IDs

    # Payment routing
    payment_method: Optional[str] = None  # stripe, paypal, wire, crypto
    payment_details_hash: Optional[str] = None  # Encrypted payment info

    # Audit trail
    audit_log: list[dict] = field(default_factory=list)

    # C2PA compatibility
    c2pa_actor_id: Optional[str] = None  # For C2PA named actor assertion

    # Passport metadata
    passport_version: int = 1
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_consent_update: Optional[datetime] = None

    def __post_init__(self):
        self.consent.creator_id = self.identity.creator_id

    def log_change(self, action: str, details: dict, by: Optional[str] = None):
        """Log a change to the audit trail."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details,
            "by": by or self.identity.creator_id,
            "passport_version": self.passport_version
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()[:16]

        self.audit_log.append(entry)
        self.updated_at = datetime.utcnow()

    def update_consent_rule(self, rule: ConsentRule, by: Optional[str] = None):
        """Update a consent rule and log the change."""
        # Find existing rule
        existing_idx = None
        for i, r in enumerate(self.consent.rules):
            if r.use_category == rule.use_category:
                existing_idx = i
                break

        if existing_idx is not None:
            old_rule = self.consent.rules[existing_idx]
            self.consent.rules[existing_idx] = rule
            action = "consent_rule_updated"
            details = {
                "use_category": rule.use_category.value,
                "old_decision": old_rule.decision.value,
                "new_decision": rule.decision.value
            }
        else:
            self.consent.rules.append(rule)
            action = "consent_rule_created"
            details = {
                "use_category": rule.use_category.value,
                "decision": rule.decision.value
            }

        self.log_change(action, details, by)
        self.last_consent_update = datetime.utcnow()
        self.consent.version += 1

    def generate_passport_hash(self) -> str:
        """Generate a cryptographic hash of the entire passport."""
        data = {
            "identity": {
                "creator_id": self.identity.creator_id,
                "display_name": self.identity.display_name,
                "noizy_id": str(self.identity.noizy_id)
            },
            "consent_version": self.consent.version,
            "works_count": len(self.registered_works),
            "audit_count": len(self.audit_log),
            "updated_at": self.updated_at.isoformat()
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def to_c2pa_actor(self) -> dict:
        """Export identity for C2PA named actor assertion."""
        return {
            "@context": "https://c2pa.org/assertions/identity/1",
            "type": "CreatorIdentity",
            "name": self.identity.display_name,
            "identifier": [
                {
                    "type": "NoizyID",
                    "value": str(self.identity.noizy_id)
                }
            ] + ([{
                "type": "IPI",
                "value": str(self.identity.ipi_number)
            }] if self.identity.ipi_number else []) + ([{
                "type": "ISNI",
                "value": str(self.identity.isni_number)
            }] if self.identity.isni_number else []),
            "role": self.identity.primary_role.value if self.identity.primary_role else "Creator",
            "verificationStatus": self.identity.verification_status.value
        }

    def to_dict(self) -> dict:
        """Export passport as dictionary."""
        return {
            "passport_version": self.passport_version,
            "identity": {
                "creator_id": self.identity.creator_id,
                "noizy_id": str(self.identity.noizy_id),
                "display_name": self.identity.display_name,
                "creator_types": [t.value for t in self.identity.creator_types],
                "ipi": str(self.identity.ipi_number) if self.identity.ipi_number else None,
                "isni": str(self.identity.isni_number) if self.identity.isni_number else None,
                "verification_status": self.identity.verification_status.value
            },
            "consent": {
                "registry_id": self.consent.registry_id,
                "default_decision": self.consent.default_decision.value,
                "rules_count": len(self.consent.rules),
                "version": self.consent.version
            },
            "works": {
                "registered_works": len(self.registered_works),
                "registered_recordings": len(self.registered_recordings)
            },
            "audit": {
                "entries": len(self.audit_log),
                "last_change": self.audit_log[-1]["timestamp"] if self.audit_log else None
            },
            "passport_hash": self.generate_passport_hash(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
