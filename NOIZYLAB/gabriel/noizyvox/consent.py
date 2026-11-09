"""
NOIZYVOX Consent Engine
=======================

Voice consent management integrated with NOIZYFISH.

Your consent is your power. No means no. Forever.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import hashlib
import json


class ConsentType(Enum):
    """Types of consent for voice use."""
    # AI Training
    AI_TRAINING_GENERAL = "ai_training_general"
    AI_TRAINING_SPECIFIC = "ai_training_specific"
    AI_TRAINING_NEVER = "ai_training_never"

    # Synthetic Voice
    SYNTHETIC_CLONE_FULL = "synthetic_clone_full"
    SYNTHETIC_CLONE_LIMITED = "synthetic_clone_limited"
    SYNTHETIC_CLONE_NEVER = "synthetic_clone_never"

    # Commercial Use
    COMMERCIAL_EXCLUSIVE = "commercial_exclusive"
    COMMERCIAL_NON_EXCLUSIVE = "commercial_non_exclusive"
    COMMERCIAL_BUYOUT = "commercial_buyout"

    # Modifications
    MODIFICATION_ALLOWED = "modification_allowed"
    MODIFICATION_APPROVAL = "modification_approval"
    MODIFICATION_NEVER = "modification_never"

    # Distribution
    DISTRIBUTION_WORLDWIDE = "distribution_worldwide"
    DISTRIBUTION_REGIONAL = "distribution_regional"
    DISTRIBUTION_SINGLE_USE = "distribution_single_use"


class UsageRights(Enum):
    """Specific usage rights that can be granted."""
    BROADCAST_TV = "broadcast_tv"
    BROADCAST_RADIO = "broadcast_radio"
    STREAMING = "streaming"
    THEATRICAL = "theatrical"
    INTERNET = "internet"
    SOCIAL_MEDIA = "social_media"
    IN_STORE = "in_store"
    TRADE_SHOW = "trade_show"
    EDUCATIONAL = "educational"
    INTERNAL = "internal"
    ALL_MEDIA = "all_media"


class ConsentStatus(Enum):
    """Status of a consent record."""
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    DISPUTED = "disputed"


class ConsentTerm(Enum):
    """Duration terms for consent."""
    ONE_YEAR = "one_year"
    TWO_YEARS = "two_years"
    FIVE_YEARS = "five_years"
    TEN_YEARS = "ten_years"
    PERPETUAL = "perpetual"
    PROJECT_BASED = "project_based"

    @property
    def days(self) -> Optional[int]:
        return {
            ConsentTerm.ONE_YEAR: 365,
            ConsentTerm.TWO_YEARS: 730,
            ConsentTerm.FIVE_YEARS: 1825,
            ConsentTerm.TEN_YEARS: 3650,
            ConsentTerm.PERPETUAL: None,
            ConsentTerm.PROJECT_BASED: None
        }[self]


@dataclass
class VoiceConsent:
    """
    A consent record for voice usage.

    Immutable once active. Integrates with NOIZYFISH.
    """
    consent_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    grantor_id: str = ""           # Voice owner (guild member)
    grantor_name: str = ""
    grantee_id: str = ""           # Entity receiving consent
    grantee_name: str = ""

    # Voice reference
    voice_print_id: str = ""
    project_id: Optional[str] = None

    # Status
    status: ConsentStatus = ConsentStatus.DRAFT

    # Consent details
    consent_types: List[ConsentType] = field(default_factory=list)
    usage_rights: List[UsageRights] = field(default_factory=list)
    term: ConsentTerm = ConsentTerm.ONE_YEAR

    # Restrictions
    excluded_uses: List[str] = field(default_factory=list)
    geographic_restrictions: List[str] = field(default_factory=list)
    language_restrictions: List[str] = field(default_factory=list)

    # Compensation
    compensation_type: str = "flat_fee"  # flat_fee, royalty, hybrid
    flat_fee_amount: float = 0.0
    royalty_percentage: float = 0.0
    minimum_guarantee: float = 0.0

    # Dates
    created_date: datetime = field(default_factory=datetime.utcnow)
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    revoked_date: Optional[datetime] = None

    # Verification
    consent_hash: str = ""
    grantor_signature: Optional[str] = None
    grantee_signature: Optional[str] = None

    # NOIZYFISH integration
    noizyfish_registry_id: Optional[str] = None
    blockchain_tx_id: Optional[str] = None

    # Metadata
    notes: str = ""
    attachments: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize consent hash."""
        if not self.consent_hash:
            self.compute_hash()

    def compute_hash(self) -> str:
        """Compute consent record hash."""
        data = {
            "consent_id": self.consent_id,
            "grantor_id": self.grantor_id,
            "grantee_id": self.grantee_id,
            "voice_print_id": self.voice_print_id,
            "consent_types": [c.value for c in self.consent_types],
            "usage_rights": [u.value for u in self.usage_rights],
            "term": self.term.value,
            "created_date": self.created_date.isoformat()
        }
        self.consent_hash = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
        return self.consent_hash

    @property
    def is_active(self) -> bool:
        """Check if consent is currently active."""
        if self.status != ConsentStatus.ACTIVE:
            return False
        if self.expiration_date and datetime.utcnow() > self.expiration_date:
            return False
        return True

    @property
    def days_remaining(self) -> Optional[int]:
        """Days until expiration."""
        if not self.expiration_date:
            return None
        delta = self.expiration_date - datetime.utcnow()
        return max(0, delta.days)

    def activate(self) -> bool:
        """Activate the consent."""
        if not self.grantor_signature or not self.grantee_signature:
            return False

        self.status = ConsentStatus.ACTIVE
        self.effective_date = datetime.utcnow()

        if self.term.days:
            self.expiration_date = self.effective_date + timedelta(days=self.term.days)

        return True

    def revoke(self, reason: str = "") -> bool:
        """Revoke the consent."""
        if self.status not in [ConsentStatus.ACTIVE, ConsentStatus.PENDING]:
            return False

        self.status = ConsentStatus.REVOKED
        self.revoked_date = datetime.utcnow()
        self.notes += f"\nRevoked: {reason}" if reason else ""
        return True

    def sign_grantor(self, signature: str):
        """Sign as grantor (voice owner)."""
        self.grantor_signature = signature

    def sign_grantee(self, signature: str):
        """Sign as grantee."""
        self.grantee_signature = signature

    def allows_use(self, consent_type: ConsentType) -> bool:
        """Check if a specific use is allowed."""
        return consent_type in self.consent_types and self.is_active

    def allows_ai_training(self) -> bool:
        """Check if AI training is allowed."""
        return (
            ConsentType.AI_TRAINING_GENERAL in self.consent_types or
            ConsentType.AI_TRAINING_SPECIFIC in self.consent_types
        ) and self.is_active

    def allows_synthetic_clone(self) -> bool:
        """Check if synthetic voice cloning is allowed."""
        return (
            ConsentType.SYNTHETIC_CLONE_FULL in self.consent_types or
            ConsentType.SYNTHETIC_CLONE_LIMITED in self.consent_types
        ) and self.is_active

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "consent_id": self.consent_id,
            "grantor_name": self.grantor_name,
            "grantee_name": self.grantee_name,
            "status": self.status.value,
            "consent_types": [c.value for c in self.consent_types],
            "usage_rights": [u.value for u in self.usage_rights],
            "term": self.term.value,
            "is_active": self.is_active,
            "days_remaining": self.days_remaining,
            "allows_ai_training": self.allows_ai_training(),
            "allows_synthetic_clone": self.allows_synthetic_clone(),
            "compensation": {
                "type": self.compensation_type,
                "flat_fee": self.flat_fee_amount,
                "royalty_percentage": self.royalty_percentage
            },
            "consent_hash": self.consent_hash[:16] + "...",
            "noizyfish_id": self.noizyfish_registry_id
        }


class ConsentEngine:
    """
    The Consent Engine.

    Manages all voice consent records.
    Integrates with NOIZYFISH for immutable recording.
    """

    def __init__(self):
        self.engine_id = str(uuid4())
        self.consents: Dict[str, VoiceConsent] = {}
        self.created = datetime.utcnow()

    # ─────────────────────────────────────────────────────────────────────────
    # Create & Manage
    # ─────────────────────────────────────────────────────────────────────────

    def create_consent(
        self,
        grantor_id: str,
        grantor_name: str,
        grantee_id: str,
        grantee_name: str,
        voice_print_id: str,
        consent_types: List[ConsentType],
        usage_rights: List[UsageRights] = None,
        term: ConsentTerm = ConsentTerm.ONE_YEAR
    ) -> VoiceConsent:
        """Create a new consent record."""
        consent = VoiceConsent(
            grantor_id=grantor_id,
            grantor_name=grantor_name,
            grantee_id=grantee_id,
            grantee_name=grantee_name,
            voice_print_id=voice_print_id,
            consent_types=consent_types,
            usage_rights=usage_rights or [UsageRights.ALL_MEDIA],
            term=term
        )
        self.consents[consent.consent_id] = consent
        return consent

    def activate_consent(self, consent_id: str) -> bool:
        """Activate a consent record."""
        consent = self.consents.get(consent_id)
        if not consent:
            return False
        return consent.activate()

    def revoke_consent(self, consent_id: str, reason: str = "") -> bool:
        """Revoke a consent record."""
        consent = self.consents.get(consent_id)
        if not consent:
            return False
        return consent.revoke(reason)

    def get_consent(self, consent_id: str) -> Optional[VoiceConsent]:
        """Get a consent record."""
        return self.consents.get(consent_id)

    # ─────────────────────────────────────────────────────────────────────────
    # Queries
    # ─────────────────────────────────────────────────────────────────────────

    def get_consents_by_grantor(self, grantor_id: str) -> List[VoiceConsent]:
        """Get all consents granted by a member."""
        return [c for c in self.consents.values() if c.grantor_id == grantor_id]

    def get_consents_by_grantee(self, grantee_id: str) -> List[VoiceConsent]:
        """Get all consents received by an entity."""
        return [c for c in self.consents.values() if c.grantee_id == grantee_id]

    def get_active_consents(self, voice_print_id: str) -> List[VoiceConsent]:
        """Get all active consents for a voice print."""
        return [
            c for c in self.consents.values()
            if c.voice_print_id == voice_print_id and c.is_active
        ]

    def check_authorization(
        self,
        voice_print_id: str,
        grantee_id: str,
        consent_type: ConsentType
    ) -> Optional[VoiceConsent]:
        """Check if a specific use is authorized."""
        for consent in self.get_active_consents(voice_print_id):
            if consent.grantee_id == grantee_id and consent.allows_use(consent_type):
                return consent
        return None

    def get_expiring_soon(self, days: int = 30) -> List[VoiceConsent]:
        """Get consents expiring within N days."""
        cutoff = datetime.utcnow() + timedelta(days=days)
        return [
            c for c in self.consents.values()
            if c.is_active and c.expiration_date and c.expiration_date <= cutoff
        ]

    # ─────────────────────────────────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get consent engine statistics."""
        active = [c for c in self.consents.values() if c.is_active]

        return {
            "total_consents": len(self.consents),
            "active_consents": len(active),
            "pending_consents": len([c for c in self.consents.values()
                                     if c.status == ConsentStatus.PENDING]),
            "revoked_consents": len([c for c in self.consents.values()
                                     if c.status == ConsentStatus.REVOKED]),
            "expiring_30_days": len(self.get_expiring_soon(30)),
            "ai_training_allowed": len([c for c in active if c.allows_ai_training()]),
            "synthetic_clone_allowed": len([c for c in active if c.allows_synthetic_clone()])
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Consent Engine."""
    print("\n" + "=" * 70)
    print("NOIZYVOX CONSENT ENGINE — DEMO")
    print("Your consent is your power")
    print("=" * 70)

    engine = ConsentEngine()

    # Create consent
    print("\n" + "─" * 50)
    print("  CREATING CONSENT RECORD")
    print("─" * 50)

    consent = engine.create_consent(
        grantor_id="member_123",
        grantor_name="Marcus Williams",
        grantee_id="studio_456",
        grantee_name="Big Audio Productions",
        voice_print_id="vp_789",
        consent_types=[
            ConsentType.COMMERCIAL_NON_EXCLUSIVE,
            ConsentType.MODIFICATION_APPROVAL,
            ConsentType.AI_TRAINING_NEVER  # Explicitly NO AI training
        ],
        usage_rights=[
            UsageRights.BROADCAST_TV,
            UsageRights.STREAMING,
            UsageRights.INTERNET
        ],
        term=ConsentTerm.TWO_YEARS
    )

    consent.flat_fee_amount = 5000.0
    consent.royalty_percentage = 0.0
    consent.excluded_uses = ["Political advertising", "Tobacco", "Gambling"]

    print(f"  Consent ID: {consent.consent_id[:8]}...")
    print(f"  Grantor: {consent.grantor_name}")
    print(f"  Grantee: {consent.grantee_name}")
    print(f"  Term: {consent.term.value}")
    print(f"  Status: {consent.status.value}")

    # Sign and activate
    print("\n" + "─" * 50)
    print("  SIGNING & ACTIVATING")
    print("─" * 50)

    consent.sign_grantor("marcus_williams_sig_" + str(uuid4())[:8])
    consent.sign_grantee("big_audio_sig_" + str(uuid4())[:8])

    print(f"  ✓ Grantor signed")
    print(f"  ✓ Grantee signed")

    if engine.activate_consent(consent.consent_id):
        print(f"  ✓ Consent activated")
        print(f"  Effective: {consent.effective_date}")
        print(f"  Expires: {consent.expiration_date}")
        print(f"  Days remaining: {consent.days_remaining}")

    # Check permissions
    print("\n" + "─" * 50)
    print("  CHECKING PERMISSIONS")
    print("─" * 50)

    print(f"  AI Training allowed: {consent.allows_ai_training()}")
    print(f"  Synthetic Clone allowed: {consent.allows_synthetic_clone()}")
    print(f"  Commercial use: {consent.allows_use(ConsentType.COMMERCIAL_NON_EXCLUSIVE)}")

    # Authorization check
    print("\n" + "─" * 50)
    print("  AUTHORIZATION CHECK")
    print("─" * 50)

    auth = engine.check_authorization(
        voice_print_id="vp_789",
        grantee_id="studio_456",
        consent_type=ConsentType.COMMERCIAL_NON_EXCLUSIVE
    )

    if auth:
        print(f"  ✓ AUTHORIZED for commercial use")
        print(f"    Consent: {auth.consent_id[:8]}...")
    else:
        print("  ✗ NOT AUTHORIZED")

    # Check AI training (should fail)
    auth_ai = engine.check_authorization(
        voice_print_id="vp_789",
        grantee_id="studio_456",
        consent_type=ConsentType.AI_TRAINING_GENERAL
    )

    if auth_ai:
        print(f"  ✓ AUTHORIZED for AI training")
    else:
        print("  ✗ NOT AUTHORIZED for AI training (correct!)")

    # Stats
    print("\n" + "─" * 50)
    print("  ENGINE STATISTICS")
    print("─" * 50)

    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print("No means no. Forever.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
