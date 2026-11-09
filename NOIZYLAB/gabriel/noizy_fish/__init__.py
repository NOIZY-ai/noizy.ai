"""
NOIZY Fish — Creator Consent Registry
======================================

A three-layer architecture for creator rights management:

LAYER 1: IDENTITY & CONSENT
  - Creator passports with cryptographic identity
  - Consent rules per use category
  - Geographic/party/context exclusions
  - Audit trail for every change

LAYER 2: PROVIDENCE (C2PA)
  - Tamper-evident content credentials
  - Chain of custody tracking
  - AI involvement disclosure
  - Links to consent registry

LAYER 3: TRACKING & ROYALTIES
  - License execution
  - Usage event tracking
  - Automated royalty distribution
  - Immutable transaction log

Quick Start:
-----------
    from gabriel.noizy_fish import NoizyFish

    # Initialize
    fish = NoizyFish()

    # Register creator
    creator = fish.register_creator(
        display_name="Sarah Chen",
        creator_types=["composer", "songwriter"],
        consent_template="composer_premium"
    )

    # Check consent
    result = fish.check_consent(
        creator_id=creator["creator_id"],
        use_category="ai_training",
        requestor="AI Corp",
        offered_amount=100000
    )
    # → {"decision": "denied", "reasons": [...]}

    # Submit inquiry
    inquiry = fish.submit_inquiry(
        creator_id=creator["creator_id"],
        requestor_name="Indie Film Studio",
        use_category="sync_film",
        offered_amount=15000
    )
    # → {"status": "APPROVED", ...}

API Server:
-----------
    uvicorn gabriel.noizy_fish.api:app --reload --port 8765

Dashboard:
----------
    python -m gabriel.noizy_fish.dashboard --demo

MCP Service:
------------
    python -m gabriel.noizy_fish.mcp_service --demo

Standards Supported:
-------------------
  - ISRC (ISO 3901:2019) — Sound recording codes
  - ISWC (ISO 15707:2022) — Musical work codes
  - IPI (CISAC) — Creator identification
  - ISNI (ISO 27729) — Name identifiers
  - C2PA — Content provenance manifests
  - DDEX/RIN — Recording information notification
"""

__version__ = "1.0.0"
__author__ = "NOIZYLAB"

# Core imports
from .registry import NoizyFishDB
from .standards import ISRC, ISWC, IPI, ISNI, NoizyID, ContributorRole

# Identity
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

# Providence
from .providence.c2pa_manifest import (
    C2PAManifest,
    Claim,
    Action,
    ActionType,
    CreatorAssertion,
    AIAssertion,
    AIDisclosure
)

# Tracking
from .tracking.royalty_engine import (
    RoyaltyEngine,
    License,
    LicenseStatus,
    RoyaltySplit,
    UsageEvent,
    UsageEventType,
    TransactionLog
)

# Notifications
from .notifications import (
    NotificationService,
    Event,
    EventType,
    WebhookConfig,
    get_notification_service,
    emit_event,
    emit_event_sync
)

# Bulk operations
from .bulk_ingestion import (
    import_creators_csv,
    import_creators_json,
    import_works_csv,
    export_creators_csv,
    export_creators_json,
    CONSENT_TEMPLATES,
    list_templates,
    apply_template
)

# Verification
from .verification import (
    VerificationService,
    VerificationStep,
    VerificationCode,
    VerificationRecord
)

# Smart licenses
from .smart_licenses import (
    LicenseTemplate,
    LicenseType,
    LicenseCondition,
    LicenseAction,
    LicenseExecutor,
    SMART_LICENSE_TEMPLATES,
    get_license_template,
    list_license_templates
)

# Crypto
from .crypto import (
    KeyPair,
    SignedClaim,
    HashChain,
    create_consent_claim,
    create_identity_claim,
    create_license_claim,
    hash_data
)

# Advanced 2056 Systems
from .ai_fingerprint import (
    AIFingerprintRegistry,
    AIModelIdentity,
    TrainingAttestation,
    OutputAttribution,
    AICapability,
    ModelType,
    TrainingStatus
)

from .federated_identity import (
    FederatedIdentityManager,
    IdentityClaim,
    VerifiableCredential,
    IdentityDelegation,
    IdentityProvider,
    ClaimStatus,
    DelegationType
)

from .voice_biometrics import (
    VoiceBiometricsEngine,
    VocalFingerprint,
    VoiceSample,
    CloneDetectionReport,
    VoiceType,
    DetectionResult
)

from .rights_dna import (
    RightsDNAEngine,
    RightsDNA,
    ContentFingerprint,
    DerivativeRelation,
    RightsConflict,
    WorkType as RightsDNAWorkType,
    DerivativeType,
    RightsConflictType
)

from .consent_propagation import (
    ConsentPropagationEngine,
    PropagatedConsent,
    ConsentChain,
    ConsentOverride,
    PropagationPolicy,
    ConflictResolution
)

from .advanced_licenses import (
    AdvancedLicenseManager,
    TimeLockedLicense,
    UsageBasedLicense,
    FractionalWork,
    FractionalShare,
    LicenseOption,
    LicenseState,
    RenewalPolicy
)


# ═══════════════════════════════════════════════════════════════════════════
# High-Level API
# ═══════════════════════════════════════════════════════════════════════════

class NoizyFish:
    """
    High-level API for NOIZY Fish.
    Combines all subsystems into a simple interface.
    """

    def __init__(self, db_path: str = "noizy_fish.db"):
        """Initialize NOIZY Fish."""
        self.db = NoizyFishDB(db_path)
        self.notifications = get_notification_service()
        self.verification = VerificationService(self.db)
        self.licenses = LicenseExecutor()

    # ─────────────────────────────────────────────────────────────────────────
    # Creator Operations
    # ─────────────────────────────────────────────────────────────────────────

    def register_creator(
        self,
        display_name: str,
        creator_types: list[str] = None,
        ipi_number: str = None,
        isni_number: str = None,
        pro_membership: str = None,
        consent_template: str = None,
        default_consent: str = "requires_approval"
    ) -> dict:
        """Register a new creator."""
        passport = CreatorPassport()
        passport.identity.display_name = display_name

        if creator_types:
            passport.identity.creator_types = [
                CreatorType(t) for t in creator_types
            ]

        if ipi_number:
            passport.identity.ipi_number = IPI.parse(ipi_number)

        if isni_number:
            passport.identity.isni_number = ISNI.parse(isni_number)

        passport.identity.pro_membership = pro_membership
        passport.consent.default_decision = ConsentDecision(default_consent)

        if consent_template:
            apply_template(passport, consent_template)

        creator_id = self.db.save_creator(passport)

        return {
            "creator_id": creator_id,
            "noizy_id": str(passport.identity.noizy_id),
            "display_name": display_name
        }

    def get_creator(self, creator_id: str) -> dict:
        """Get creator by ID."""
        import json
        creator = self.db.get_creator(creator_id)
        if not creator:
            creator = self.db.get_creator_by_noizy_id(creator_id)
        if not creator:
            return None

        rules = self.db.get_consent_rules(creator["creator_id"])
        return {
            "creator_id": creator["creator_id"],
            "noizy_id": creator["noizy_id"],
            "display_name": creator["display_name"],
            "creator_types": json.loads(creator["creator_types"]),
            "verification_status": creator["verification_status"],
            "consent_rules": len(rules)
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Consent Operations
    # ─────────────────────────────────────────────────────────────────────────

    def check_consent(
        self,
        creator_id: str,
        use_category: str,
        requestor: str = None,
        context: str = None,
        territory: str = "WW",
        offered_amount: float = None
    ) -> dict:
        """
        Check consent — THE CORE QUERY.
        Returns {"decision": "...", "reasons": [...]}
        """
        return self.db.check_consent(
            creator_id=creator_id,
            use_category=use_category,
            requestor=requestor,
            context=context,
            territory=territory,
            offered_amount=offered_amount
        )

    def update_consent(
        self,
        creator_id: str,
        use_category: str,
        decision: str,
        minimum_amount: float = None,
        excluded_parties: list[str] = None,
        excluded_contexts: list[str] = None
    ) -> dict:
        """Update a consent rule."""
        rule = ConsentRule(
            use_category=UseCategory(use_category),
            decision=ConsentDecision(decision)
        )

        if minimum_amount:
            rule.compensation = CompensationTerms(
                compensation_type=CompensationType.FLAT_FEE,
                minimum_amount=minimum_amount
            )

        if excluded_parties:
            rule.excluded_parties = excluded_parties

        if excluded_contexts:
            rule.excluded_contexts = excluded_contexts

        with self.db._get_conn() as conn:
            self.db._save_consent_rule(conn, creator_id, rule)

        return {"success": True, "use_category": use_category, "decision": decision}

    # ─────────────────────────────────────────────────────────────────────────
    # Inquiry Operations
    # ─────────────────────────────────────────────────────────────────────────

    def submit_inquiry(
        self,
        creator_id: str,
        requestor_name: str,
        use_category: str,
        requestor_email: str = None,
        work_id: str = None,
        territory: str = "WW",
        context: str = None,
        offered_amount: float = None
    ) -> dict:
        """Submit a licensing inquiry."""
        # Check consent
        result = self.check_consent(
            creator_id=creator_id,
            use_category=use_category,
            requestor=requestor_name,
            context=context,
            territory=territory,
            offered_amount=offered_amount
        )

        # Log inquiry
        inquiry_id = self.db.log_inquiry(
            creator_id=creator_id,
            requestor_name=requestor_name,
            use_category=use_category,
            decision=result["decision"],
            reasons=result["reasons"],
            work_id=work_id,
            requestor_email=requestor_email,
            territory=territory,
            context=context,
            offered_amount=offered_amount
        )

        # Determine status
        decision = result["decision"]
        if decision in ["allowed", "allowed_terms"]:
            status = "APPROVED"
        elif decision in ["requires_approval", "negotiable"]:
            status = "PENDING_REVIEW"
        else:
            status = "DENIED"

        return {
            "inquiry_id": inquiry_id,
            "status": status,
            "decision": decision,
            "reasons": result["reasons"]
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Work Operations
    # ─────────────────────────────────────────────────────────────────────────

    def register_work(
        self,
        creator_id: str,
        title: str,
        work_type: str = "recording",
        isrc: str = None,
        iswc: str = None,
        format: str = None
    ) -> dict:
        """Register a work."""
        from uuid import uuid4
        from datetime import datetime

        work_id = str(uuid4())
        type_prefix = {"recording": "REC", "composition": "WK", "voice": "VOC"}.get(work_type, "WK")
        noizy_work_id = f"NZ-{type_prefix}-{datetime.utcnow().strftime('%Y%m%d')}-{work_id[:8].upper()}"

        self.db.save_work(
            work_id=work_id,
            noizy_work_id=noizy_work_id,
            creator_id=creator_id,
            work_type=work_type,
            title=title,
            isrc=isrc,
            iswc=iswc,
            format=format
        )

        return {
            "work_id": work_id,
            "noizy_work_id": noizy_work_id,
            "title": title
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Stats
    # ─────────────────────────────────────────────────────────────────────────

    def stats(self) -> dict:
        """Get registry statistics."""
        stats = self.db.get_stats()
        valid, _ = self.db.verify_transaction_log()
        stats["transaction_log_valid"] = valid
        return stats


# ═══════════════════════════════════════════════════════════════════════════
# Module-level convenience
# ═══════════════════════════════════════════════════════════════════════════

_default_instance: NoizyFish = None


def init(db_path: str = "noizy_fish.db") -> NoizyFish:
    """Initialize the default NoizyFish instance."""
    global _default_instance
    _default_instance = NoizyFish(db_path)
    return _default_instance


def get_instance() -> NoizyFish:
    """Get the default NoizyFish instance."""
    global _default_instance
    if _default_instance is None:
        _default_instance = NoizyFish()
    return _default_instance


# Export all
__all__ = [
    # Main class
    "NoizyFish",
    "init",
    "get_instance",

    # Database
    "NoizyFishDB",

    # Standards
    "ISRC", "ISWC", "IPI", "ISNI", "NoizyID", "ContributorRole",

    # Identity
    "CreatorPassport", "CreatorIdentity", "CreatorType", "VerificationStatus",
    "ConsentRegistry", "ConsentRule", "UseCategory", "ConsentDecision",
    "CompensationTerms", "CompensationType",

    # Providence
    "C2PAManifest", "Claim", "Action", "ActionType",
    "CreatorAssertion", "AIAssertion", "AIDisclosure",

    # Tracking
    "RoyaltyEngine", "License", "LicenseStatus", "RoyaltySplit",
    "UsageEvent", "UsageEventType", "TransactionLog",

    # Notifications
    "NotificationService", "Event", "EventType", "WebhookConfig",
    "get_notification_service", "emit_event", "emit_event_sync",

    # Bulk
    "import_creators_csv", "import_creators_json", "import_works_csv",
    "export_creators_csv", "export_creators_json",
    "CONSENT_TEMPLATES", "list_templates", "apply_template",

    # Verification
    "VerificationService", "VerificationStep", "VerificationCode", "VerificationRecord",

    # Smart Licenses
    "LicenseTemplate", "LicenseType", "LicenseCondition", "LicenseAction",
    "LicenseExecutor", "SMART_LICENSE_TEMPLATES",
    "get_license_template", "list_license_templates",

    # Crypto
    "KeyPair", "SignedClaim", "HashChain",
    "create_consent_claim", "create_identity_claim", "create_license_claim",
    "hash_data",

    # 2056 VALUE: AI Fingerprinting
    "AIFingerprintRegistry", "AIModelIdentity", "TrainingAttestation",
    "OutputAttribution", "AICapability", "ModelType", "TrainingStatus",

    # 2056 VALUE: Federated Identity
    "FederatedIdentityManager", "IdentityClaim", "VerifiableCredential",
    "IdentityDelegation", "IdentityProvider", "ClaimStatus", "DelegationType",

    # 2056 VALUE: Voice Biometrics
    "VoiceBiometricsEngine", "VocalFingerprint", "VoiceSample",
    "CloneDetectionReport", "VoiceType", "DetectionResult",

    # 2056 VALUE: Rights DNA
    "RightsDNAEngine", "RightsDNA", "ContentFingerprint",
    "DerivativeRelation", "RightsConflict", "RightsDNAWorkType",
    "DerivativeType", "RightsConflictType",

    # 2056 VALUE: Consent Propagation
    "ConsentPropagationEngine", "PropagatedConsent", "ConsentChain",
    "ConsentOverride", "PropagationPolicy", "ConflictResolution",

    # 2056 VALUE: Advanced Licenses
    "AdvancedLicenseManager", "TimeLockedLicense", "UsageBasedLicense",
    "FractionalWork", "FractionalShare", "LicenseOption",
    "LicenseState", "RenewalPolicy"
]
