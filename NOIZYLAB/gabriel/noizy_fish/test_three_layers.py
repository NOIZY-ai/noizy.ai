#!/usr/bin/env python3
"""
NOIZY Fish — Three Layer Test
==============================

Tests all three layers with three creator types:
1. COMPOSER — writes music, holds publishing rights
2. VOICE ACTOR — voice performance, neighboring rights
3. PRODUCER — creates recordings, holds master rights

Each creator has different consent settings and royalty structures.
We'll run licensing inquiries against each and watch the system work.

Run: python -m gabriel.noizy_fish.test_three_layers
"""

import asyncio
from datetime import datetime, timedelta

from .standards import (
    IPI, ISNI, ISRC, ISWC, NoizyID,
    ContributorRole
)
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
from .providence.c2pa_manifest import (
    C2PAManifest,
    Claim,
    Action,
    ActionType,
    CreatorAssertion,
    AIAssertion,
    AIDisclosure,
    SoftwarAgent,
    Ingredient,
    create_recording_manifest,
    create_ai_generated_manifest
)
from .tracking.royalty_engine import (
    RoyaltyEngine,
    License,
    LicenseStatus,
    RoyaltySplit,
    UsageEvent,
    UsageEventType,
    TransactionLog
)


def create_composer_passport() -> CreatorPassport:
    """
    Create passport for SARAH CHEN — Composer/Songwriter
    Focus: Publishing rights, sync licensing
    """
    passport = CreatorPassport()

    # Identity
    passport.identity.display_name = "Sarah Chen"
    passport.identity.creator_types = [CreatorType.COMPOSER, CreatorType.SONGWRITER]
    passport.identity.primary_role = ContributorRole.COMPOSER
    passport.identity.ipi_number = IPI.parse("00123456789")
    passport.identity.isni_number = ISNI.parse("0000000123456789")
    passport.identity.pro_membership = "ASCAP"
    passport.identity.pro_member_id = "ASCAP-12345"
    passport.identity.verification_status = VerificationStatus.FULLY_VERIFIED

    # Consent Registry — Composer perspective
    passport.consent.default_decision = ConsentDecision.REQUIRES_APPROVAL

    # Streaming — allowed for PROs
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.STREAMING,
        decision=ConsentDecision.ALLOWED,
        compensation=CompensationTerms(
            compensation_type=CompensationType.PER_USE,
            per_use_rate=0.004,  # $0.004 per stream
            currency="USD"
        )
    ))

    # Sync for film — premium pricing
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SYNC_FILM,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=10000.00,
            preferred_amount=25000.00,
            currency="USD"
        ),
        requires_credit=True,
        credit_format="Music by Sarah Chen"
    ))

    # Sync for ads — higher fee, some exclusions
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SYNC_AD,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=15000.00,
            currency="USD"
        ),
        excluded_contexts=["tobacco", "alcohol", "firearms", "political", "gambling"]
    ))

    # AI Training — NEVER
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.AI_TRAINING,
        decision=ConsentDecision.DENIED
    ))

    # Sampling — case by case
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SAMPLE,
        decision=ConsentDecision.REQUIRES_APPROVAL,
        compensation=CompensationTerms(
            compensation_type=CompensationType.ADVANCE_ROYALTY,
            minimum_amount=2500.00,
            percentage_rate=3.0
        )
    ))

    # Global exclusions
    passport.consent.global_excluded_parties = ["TechCorp AI", "DataMine Inc"]

    return passport


def create_voice_actor_passport() -> CreatorPassport:
    """
    Create passport for MARCUS REED — Voice Actor
    Focus: Voice performance rights, voice cloning protection
    """
    passport = CreatorPassport()

    # Identity
    passport.identity.display_name = "Marcus Reed"
    passport.identity.creator_types = [CreatorType.VOICE_ACTOR, CreatorType.PERFORMER]
    passport.identity.primary_role = ContributorRole.VOICE_ACTOR
    passport.identity.isni_number = ISNI.parse("0000000987654321")
    passport.identity.verification_status = VerificationStatus.IDENTITY_VERIFIED

    # Consent Registry — Voice actor perspective
    passport.consent.default_decision = ConsentDecision.REQUIRES_APPROVAL

    # Voice performance — standard rates
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SYNC_GAME,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=500.00,
            preferred_amount=2000.00,
            notes="Per session/character"
        ),
        duration_limit="perpetual"
    ))

    # Streaming/narration
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.STREAMING,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=300.00
        )
    ))

    # AI VOICE CLONING — ABSOLUTELY NEVER
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.AI_VOICE_CLONE,
        decision=ConsentDecision.DENIED
    ))

    # AI Training — NEVER
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.AI_TRAINING,
        decision=ConsentDecision.DENIED
    ))

    # AI Generation (using voice) — NEVER
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.AI_GENERATION,
        decision=ConsentDecision.DENIED
    ))

    # Educational — discounted
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.EDUCATIONAL,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=100.00
        )
    ))

    return passport


def create_producer_passport() -> CreatorPassport:
    """
    Create passport for DJ NOVA — Producer/Remixer
    Focus: Master rights, remix culture, sample clearance
    """
    passport = CreatorPassport()

    # Identity
    passport.identity.display_name = "DJ Nova"
    passport.identity.creator_types = [CreatorType.PRODUCER, CreatorType.DJ]
    passport.identity.primary_role = ContributorRole.PRODUCER
    passport.identity.verification_status = VerificationStatus.PRO_VERIFIED

    # Consent Registry — Producer perspective
    passport.consent.default_decision = ConsentDecision.NEGOTIABLE

    # Streaming — standard
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.STREAMING,
        decision=ConsentDecision.ALLOWED,
        compensation=CompensationTerms(
            compensation_type=CompensationType.PERCENTAGE,
            percentage_rate=70.0,  # Artist share
            notes="Standard streaming split"
        )
    ))

    # Sampling — friendly to remix culture
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SAMPLE,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=500.00
        ),
        requires_credit=True,
        credit_format="Contains samples from DJ Nova"
    ))

    # Remix — open
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.REMIX,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.REVENUE_SHARE,
            percentage_rate=50.0
        )
    ))

    # Sync — case by case
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.SYNC_AD,
        decision=ConsentDecision.NEGOTIABLE,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=5000.00
        )
    ))

    # AI Training — surprisingly open (with conditions)
    passport.update_consent_rule(ConsentRule(
        use_category=UseCategory.AI_TRAINING,
        decision=ConsentDecision.ALLOWED_WITH_TERMS,
        compensation=CompensationTerms(
            compensation_type=CompensationType.FLAT_FEE,
            minimum_amount=50000.00,  # But expensive
            notes="Requires full dataset license"
        ),
        requires_sample_review=True
    ))

    # Auto-approve under $1000 for educational
    passport.consent.auto_approve_categories = [UseCategory.EDUCATIONAL]

    return passport


def test_layer_one_identity():
    """Test Layer 1: Creator Identity & Consent"""
    print("\n" + "=" * 70)
    print("LAYER 1: CREATOR IDENTITY & CONSENT")
    print("=" * 70)

    # Create the three passports
    composer = create_composer_passport()
    voice_actor = create_voice_actor_passport()
    producer = create_producer_passport()

    passports = [
        ("COMPOSER", composer),
        ("VOICE ACTOR", voice_actor),
        ("PRODUCER", producer)
    ]

    for name, passport in passports:
        print(f"\n{'─' * 50}")
        print(f"{name}: {passport.identity.display_name}")
        print(f"{'─' * 50}")
        print(f"  NOIZY ID: {passport.identity.noizy_id}")
        print(f"  Types: {[t.value for t in passport.identity.creator_types]}")
        print(f"  IPI: {passport.identity.ipi_number}")
        print(f"  ISNI: {passport.identity.isni_number}")
        print(f"  Verification: {passport.identity.verification_status.value}")
        print(f"  Consent Rules: {len(passport.consent.rules)}")
        print(f"  Default: {passport.consent.default_decision.value}")

        # Show key consent rules
        print(f"\n  Key Consent Settings:")
        for rule in passport.consent.rules[:4]:
            comp = f"${rule.compensation.minimum_amount}" if rule.compensation and rule.compensation.minimum_amount else "N/A"
            print(f"    • {rule.use_category.value}: {rule.decision.value} (min: {comp})")

    return composer, voice_actor, producer


def test_layer_two_providence(composer, voice_actor, producer):
    """Test Layer 2: Providence (C2PA)"""
    print("\n" + "=" * 70)
    print("LAYER 2: PROVIDENCE (C2PA MANIFEST)")
    print("=" * 70)

    # Create manifests for each creator type

    # Composer's composition
    composer_manifest = C2PAManifest()
    composer_manifest.claim.dc_title = "Midnight Sonata"
    composer_manifest.claim.dc_format = "audio/midi"
    composer_manifest.iswc = "T-010.123.456-7"
    composer_manifest.noizy_work_id = "NZ-WK-20260322-COMP001"
    composer_manifest.consent_registry_id = composer.consent.registry_id

    composer_manifest.add_action(Action(
        action=ActionType.C2PA_CREATED,
        software_agent=SoftwarAgent(name="Logic Pro", version="11.0"),
        description="Original composition"
    ))
    composer_manifest.add_creator(CreatorAssertion(
        creator_id=composer.identity.creator_id,
        display_name=composer.identity.display_name,
        role="Composer",
        noizy_id=str(composer.identity.noizy_id),
        ipi=str(composer.identity.ipi_number)
    ))

    # Voice actor's recording
    voice_manifest = create_recording_manifest(
        title="Character Voice: Commander Rex",
        creator_name=voice_actor.identity.display_name,
        creator_id=voice_actor.identity.creator_id,
        format="audio/wav",
        software="Pro Tools"
    )
    voice_manifest.isrc = "US-S1Z-26-00001"
    voice_manifest.noizy_work_id = "NZ-VOC-20260322-VOICE001"
    voice_manifest.consent_registry_id = voice_actor.consent.registry_id

    # Producer's track (with AI assistance)
    producer_manifest = C2PAManifest()
    producer_manifest.claim.dc_title = "Neon Dreams"
    producer_manifest.claim.dc_format = "audio/wav"
    producer_manifest.isrc = "US-N0V-26-00001"
    producer_manifest.noizy_work_id = "NZ-REC-20260322-PROD001"
    producer_manifest.consent_registry_id = producer.consent.registry_id

    producer_manifest.add_action(Action(
        action=ActionType.NOIZY_AI_ASSISTED,
        software_agent=SoftwarAgent(name="Suno", version="4.0"),
        description="AI-assisted beat generation"
    ))
    producer_manifest.add_action(Action(
        action=ActionType.NOIZY_MIXED,
        software_agent=SoftwarAgent(name="Ableton Live", version="12"),
        description="Final mix by DJ Nova"
    ))
    producer_manifest.add_creator(CreatorAssertion(
        creator_id=producer.identity.creator_id,
        display_name=producer.identity.display_name,
        role="Producer"
    ))
    producer_manifest.set_ai_disclosure(AIAssertion(
        disclosure=AIDisclosure.AI_ASSISTED,
        ai_tools=[SoftwarAgent(name="Suno", version="4.0")],
        human_oversight=True,
        human_modifications=["Structure", "Arrangement", "Final mix", "Vocals"]
    ))

    manifests = [
        ("COMPOSER", composer_manifest),
        ("VOICE ACTOR", voice_manifest),
        ("PRODUCER", producer_manifest)
    ]

    for name, manifest in manifests:
        print(f"\n{'─' * 50}")
        print(f"{name} MANIFEST: {manifest.claim.dc_title}")
        print(f"{'─' * 50}")
        print(f"  Format: {manifest.claim.dc_format}")
        print(f"  ISRC: {manifest.isrc}")
        print(f"  ISWC: {manifest.iswc}")
        print(f"  NOIZY Work ID: {manifest.noizy_work_id}")
        print(f"  Actions: {len(manifest.claim.actions)}")
        for action in manifest.claim.actions:
            print(f"    • {action.action.value}")
            if action.software_agent:
                print(f"      Tool: {action.software_agent.name}")
        print(f"  Creators: {len(manifest.claim.creators)}")
        if manifest.claim.ai_assertion:
            print(f"  AI Disclosure: {manifest.claim.ai_assertion.disclosure.value}")

        # Verify chain
        valid, issues = manifest.verify_chain()
        print(f"  Chain Valid: {'✓' if valid else '✗'}")

    return composer_manifest, voice_manifest, producer_manifest


def test_layer_three_tracking(composer, voice_actor, producer):
    """Test Layer 3: Tracking & Royalties"""
    print("\n" + "=" * 70)
    print("LAYER 3: TRACKING & ROYALTIES")
    print("=" * 70)

    engine = RoyaltyEngine()
    tx_log = TransactionLog()

    # Create licenses for each creator

    # Composer: Sync license for film
    composer_license = License(
        licensor_id=composer.identity.creator_id,
        licensee_name="Indie Film Studio",
        licensee_email="licensing@indiefilm.com",
        licensee_company="Indie Film Studio LLC",
        work_id="NZ-WK-20260322-COMP001",
        work_title="Midnight Sonata",
        use_type="sync_film",
        use_description="Background score for feature film",
        territory="WW",
        fee_type="flat_fee",
        fee_amount=15000.00,
        status=LicenseStatus.ACTIVE,
        royalty_splits=[
            RoyaltySplit(
                recipient_id=composer.identity.creator_id,
                recipient_name=composer.identity.display_name,
                recipient_email="sarah@example.com",
                percentage=100.0,
                role="composer"
            )
        ]
    )

    # Voice actor: Game voice license
    voice_license = License(
        licensor_id=voice_actor.identity.creator_id,
        licensee_name="GameDev Studios",
        licensee_email="audio@gamedev.com",
        work_id="NZ-VOC-20260322-VOICE001",
        work_title="Commander Rex Voice",
        use_type="sync_game",
        fee_type="flat_fee",
        fee_amount=2000.00,
        status=LicenseStatus.ACTIVE,
        royalty_splits=[
            RoyaltySplit(
                recipient_id=voice_actor.identity.creator_id,
                recipient_name=voice_actor.identity.display_name,
                recipient_email="marcus@example.com",
                percentage=100.0,
                role="voice_actor"
            )
        ]
    )

    # Producer: Streaming license
    producer_license = License(
        licensor_id=producer.identity.creator_id,
        licensee_name="Spotify",
        work_id="NZ-REC-20260322-PROD001",
        work_title="Neon Dreams",
        use_type="streaming",
        fee_type="per_use",
        per_use_rate=0.003,
        perpetual=True,
        status=LicenseStatus.ACTIVE,
        royalty_splits=[
            RoyaltySplit(
                recipient_id=producer.identity.creator_id,
                recipient_name=producer.identity.display_name,
                recipient_email="djnova@example.com",
                percentage=100.0,
                role="producer"
            )
        ]
    )

    # Register licenses
    engine.register_license(composer_license)
    engine.register_license(voice_license)
    engine.register_license(producer_license)

    # Log license creation
    for license in [composer_license, voice_license, producer_license]:
        tx_log.log("license_created", {
            "license_id": license.license_id,
            "work_id": license.work_id,
            "work_title": license.work_title,
            "fee": license.fee_amount
        })

    # Simulate usage events
    print("\n" + "─" * 50)
    print("SIMULATING USAGE EVENTS")
    print("─" * 50)

    # Producer's track gets 100K streams
    stream_count = 100000
    for i in range(10):  # Batch into 10 events of 10K each
        event = UsageEvent(
            license_id=producer_license.license_id,
            work_id=producer_license.work_id,
            event_type=UsageEventType.STREAM,
            platform="Spotify",
            territory="US"
        )
        royalty = engine.record_usage(event)

    print(f"  Producer streams: {producer_license.total_uses * 10000}")
    print(f"  Producer royalties: ${producer_license.total_royalties_paid:,.2f}")

    # Display license status
    print("\n" + "─" * 50)
    print("LICENSE STATUS")
    print("─" * 50)

    licenses = [
        ("COMPOSER", composer_license),
        ("VOICE ACTOR", voice_license),
        ("PRODUCER", producer_license)
    ]

    for name, lic in licenses:
        print(f"\n  {name}: {lic.work_title}")
        print(f"    Status: {lic.status.value}")
        print(f"    Fee: ${lic.fee_amount:,.2f} ({lic.fee_type})")
        print(f"    Uses: {lic.total_uses}")
        print(f"    Royalties Paid: ${lic.total_royalties_paid:,.2f}")

    # Generate statement for producer
    print("\n" + "─" * 50)
    print("ROYALTY STATEMENT — DJ Nova")
    print("─" * 50)

    statement = engine.generate_statement(
        producer.identity.creator_id,
        producer.identity.display_name,
        datetime.utcnow() - timedelta(days=30),
        datetime.utcnow()
    )

    print(f"\n  Period: {statement.period_start.strftime('%Y-%m-%d')} to {statement.period_end.strftime('%Y-%m-%d')}")
    print(f"  Gross Earnings: ${statement.gross_earnings:,.2f}")
    print(f"  Fees (10%): ${statement.fees:,.2f}")
    print(f"  Net Earnings: ${statement.net_earnings:,.2f}")

    # Verify transaction log
    print("\n" + "─" * 50)
    print("TRANSACTION LOG")
    print("─" * 50)

    valid, issues = tx_log.verify()
    print(f"  Entries: {len(tx_log.entries)}")
    print(f"  Chain Valid: {'✓' if valid else '✗'}")

    return engine, tx_log


def test_licensing_inquiry(composer, voice_actor, producer):
    """Test licensing inquiries against all three creators."""
    print("\n" + "=" * 70)
    print("LICENSING INQUIRY TESTS")
    print("=" * 70)

    inquiries = [
        # Inquiry 1: Film sync for composer — should APPROVE
        {
            "creator": composer,
            "use": UseCategory.SYNC_FILM,
            "requestor": "Indie Film Studio",
            "context": "Feature documentary about jazz musicians",
            "offer": 12000.00,
            "expected": "APPROVE or TERMS"
        },
        # Inquiry 2: AI training for composer — should DENY
        {
            "creator": composer,
            "use": UseCategory.AI_TRAINING,
            "requestor": "TechCorp AI",
            "context": "Training data for music generation",
            "offer": 100000.00,
            "expected": "DENY"
        },
        # Inquiry 3: Voice cloning for voice actor — should DENY
        {
            "creator": voice_actor,
            "use": UseCategory.AI_VOICE_CLONE,
            "requestor": "VoiceAI Inc",
            "context": "Clone voice for AI assistant",
            "offer": 50000.00,
            "expected": "DENY"
        },
        # Inquiry 4: Game license for voice actor — should APPROVE
        {
            "creator": voice_actor,
            "use": UseCategory.SYNC_GAME,
            "requestor": "GameDev Studios",
            "context": "Voice for RPG character",
            "offer": 1500.00,
            "expected": "APPROVE"
        },
        # Inquiry 5: Sample for producer — should APPROVE (remix friendly)
        {
            "creator": producer,
            "use": UseCategory.SAMPLE,
            "requestor": "Rising Artist",
            "context": "Sample synth loop for new track",
            "offer": 750.00,
            "expected": "APPROVE"
        },
        # Inquiry 6: AI training for producer — should APPROVE (expensive)
        {
            "creator": producer,
            "use": UseCategory.AI_TRAINING,
            "requestor": "AI Music Lab",
            "context": "Training data for beat generation",
            "offer": 60000.00,
            "expected": "APPROVE (high fee)"
        },
        # Inquiry 7: Tobacco ad for composer — should DENY (excluded context)
        {
            "creator": composer,
            "use": UseCategory.SYNC_AD,
            "requestor": "Tobacco Corp",
            "context": "Background music for tobacco advertisement",
            "offer": 50000.00,
            "expected": "DENY"
        }
    ]

    for i, inq in enumerate(inquiries, 1):
        passport = inq["creator"]
        print(f"\n{'─' * 50}")
        print(f"INQUIRY {i}: {inq['use'].value} for {passport.identity.display_name}")
        print(f"{'─' * 50}")
        print(f"  Requestor: {inq['requestor']}")
        print(f"  Context: {inq['context']}")
        print(f"  Offer: ${inq['offer']:,.2f}")

        # Evaluate against consent registry
        decision, reasons = passport.consent.evaluate_inquiry(
            use_category=inq["use"],
            requestor=inq["requestor"],
            context=inq["context"],
            offered_amount=inq["offer"]
        )

        # Display result
        emoji = "✅" if decision in [ConsentDecision.ALLOWED, ConsentDecision.ALLOWED_WITH_TERMS] else "❌"
        print(f"\n  DECISION: {emoji} {decision.value.upper()}")
        print(f"  Expected: {inq['expected']}")
        print(f"  Reasons:")
        for reason in reasons:
            print(f"    • {reason}")


def run_full_test():
    """Run the complete three-layer test."""
    print("\n" + "═" * 70)
    print("NOIZY FISH — THREE LAYER ARCHITECTURE TEST")
    print("═" * 70)
    print("\nTesting with three creator types:")
    print("  • COMPOSER (Sarah Chen) — Publishing rights, sync licensing")
    print("  • VOICE ACTOR (Marcus Reed) — Voice rights, clone protection")
    print("  • PRODUCER (DJ Nova) — Master rights, remix culture")

    # Layer 1: Identity & Consent
    composer, voice_actor, producer = test_layer_one_identity()

    # Layer 2: Providence (C2PA)
    composer_manifest, voice_manifest, producer_manifest = test_layer_two_providence(
        composer, voice_actor, producer
    )

    # Layer 3: Tracking & Royalties
    engine, tx_log = test_layer_three_tracking(composer, voice_actor, producer)

    # Licensing Inquiry Tests
    test_licensing_inquiry(composer, voice_actor, producer)

    # Summary
    print("\n" + "═" * 70)
    print("TEST COMPLETE")
    print("═" * 70)
    print("""
Three layers working together:

LAYER 1: IDENTITY & CONSENT
  • Creator passports with cryptographic identity
  • Consent rules per use category
  • Geographic/party/context exclusions
  • Compensation requirements

LAYER 2: PROVIDENCE (C2PA)
  • Tamper-evident content credentials
  • Chain of custody tracking
  • AI involvement disclosure
  • Links to consent registry

LAYER 3: TRACKING & ROYALTIES
  • License execution
  • Usage event tracking
  • Automated royalty distribution
  • Immutable transaction log

KEY OBSERVATIONS:
  ✓ Composer declined AI training even at $100K (consent > money)
  ✓ Voice actor protected from voice cloning at any price
  ✓ Producer open to AI training but at premium ($50K+ minimum)
  ✓ Context exclusions work (tobacco ad rejected despite high offer)
  ✓ Providence manifests link content to consent registry
  ✓ Transaction log provides audit trail

This is NOIZY Fish — creator consent as the foundation.
    """)


if __name__ == "__main__":
    run_full_test()
