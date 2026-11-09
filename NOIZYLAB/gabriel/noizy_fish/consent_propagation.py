"""
NOIZY Fish — Consent Propagation Engine
========================================

Automatic consent inheritance across derivative works.
Smart rules that flow through the creative supply chain.

Features:
- Consent inheritance (derivatives inherit parent restrictions)
- Override rules (child can tighten, not loosen)
- Propagation policies (how consent flows)
- Conflict resolution (when rules collide)
- Time-decay rules (consent can expire)

2056 VALUE: One consent decision protects your work forever, everywhere.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable
from uuid import uuid4
import json


# ═══════════════════════════════════════════════════════════════════════════════
# Propagation Types
# ═══════════════════════════════════════════════════════════════════════════════

class PropagationPolicy(Enum):
    """How consent propagates to derivatives."""
    STRICT_INHERIT = "strict_inherit"       # Exact copy of parent rules
    INHERIT_AND_TIGHTEN = "inherit_tighten" # Can only add restrictions
    NEGOTIABLE = "negotiable"               # Each level negotiates
    INDEPENDENT = "independent"             # No inheritance


class ConflictResolution(Enum):
    """How to resolve conflicting consent rules."""
    MOST_RESTRICTIVE = "most_restrictive"   # Default: tightest rule wins
    MOST_PERMISSIVE = "most_permissive"     # Loosest rule wins (rare)
    CREATOR_PRIORITY = "creator_priority"   # Original creator decides
    MAJORITY_SHARE = "majority_share"       # Majority rights holder decides


class ConsentType(Enum):
    """Types of consent decisions."""
    ALLOW = "allow"
    ALLOW_WITH_TERMS = "allow_terms"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    NEGOTIATE = "negotiate"


# ═══════════════════════════════════════════════════════════════════════════════
# Consent Rule
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PropagatedConsent:
    """
    A consent rule that can propagate through derivatives.
    """
    rule_id: str = field(default_factory=lambda: str(uuid4()))

    # Source
    source_work_id: str = ""
    source_creator_id: str = ""

    # Rule
    use_category: str = ""
    consent_type: ConsentType = ConsentType.REQUIRE_APPROVAL

    # Terms
    minimum_fee: Optional[float] = None
    royalty_rate: Optional[float] = None
    attribution_required: bool = True
    territorial_restrictions: list[str] = field(default_factory=list)  # ISO codes
    excluded_parties: list[str] = field(default_factory=list)
    excluded_contexts: list[str] = field(default_factory=list)

    # Propagation
    propagation_policy: PropagationPolicy = PropagationPolicy.INHERIT_AND_TIGHTEN
    propagation_depth: int = -1  # -1 = infinite
    can_be_overridden: bool = False

    # Time constraints
    valid_from: datetime = field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = None
    auto_expire_on_transfer: bool = False

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def is_valid(self) -> bool:
        """Check if consent is currently valid."""
        now = datetime.utcnow()
        if now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        return True

    def applies_to(
        self,
        territory: str = None,
        party: str = None,
        context: str = None
    ) -> bool:
        """Check if consent applies to given parameters."""
        if not self.is_valid():
            return False

        if territory and self.territorial_restrictions:
            if territory not in self.territorial_restrictions:
                return False

        if party and self.excluded_parties:
            if party in self.excluded_parties:
                return False

        if context and self.excluded_contexts:
            if any(ec in context.lower() for ec in self.excluded_contexts):
                return False

        return True


@dataclass
class ConsentOverride:
    """An override applied by a derivative work."""
    override_id: str = field(default_factory=lambda: str(uuid4()))

    # Context
    derivative_work_id: str = ""
    original_rule_id: str = ""

    # Override
    override_type: str = ""  # "tighten", "extend", "restrict_territory"
    override_value: dict = field(default_factory=dict)

    # Validation
    is_valid: bool = True
    validation_error: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# Consent Chain
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ConsentChain:
    """
    The complete consent chain for a derivative work.

    Shows how consent flows from original through all intermediaries.
    """
    chain_id: str = field(default_factory=lambda: str(uuid4()))

    # Target
    work_id: str = ""
    use_category: str = ""

    # Chain
    links: list[dict] = field(default_factory=list)
    # Each: {"work_id", "creator_id", "consent_type", "rule_id", "depth"}

    # Resolution
    final_consent: ConsentType = ConsentType.REQUIRE_APPROVAL
    resolution_method: ConflictResolution = ConflictResolution.MOST_RESTRICTIVE
    blocking_rule: Optional[str] = None  # Which rule blocked (if denied)

    # Aggregated terms
    total_minimum_fee: float = 0.0
    total_royalty_rate: float = 0.0
    all_attributions: list[str] = field(default_factory=list)
    combined_restrictions: list[str] = field(default_factory=list)

    # Metadata
    computed_at: datetime = field(default_factory=datetime.utcnow)
    chain_length: int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# Consent Propagation Engine
# ═══════════════════════════════════════════════════════════════════════════════

class ConsentPropagationEngine:
    """
    Propagates consent rules through derivative works.

    When you set a rule, it flows through all derivatives automatically.
    """

    def __init__(self):
        self.rules: dict[str, PropagatedConsent] = {}
        self.overrides: dict[str, ConsentOverride] = {}
        self.work_parents: dict[str, list[str]] = {}  # work_id -> parent_work_ids
        self.work_creators: dict[str, list[str]] = {}  # work_id -> creator_ids

    def register_work(
        self,
        work_id: str,
        creator_ids: list[str],
        parent_work_ids: list[str] = None
    ):
        """Register a work and its lineage."""
        self.work_creators[work_id] = creator_ids
        self.work_parents[work_id] = parent_work_ids or []

    def set_consent_rule(
        self,
        work_id: str,
        creator_id: str,
        use_category: str,
        consent_type: ConsentType,
        propagation_policy: PropagationPolicy = PropagationPolicy.INHERIT_AND_TIGHTEN,
        **kwargs
    ) -> PropagatedConsent:
        """Set a consent rule for a work."""
        rule = PropagatedConsent(
            source_work_id=work_id,
            source_creator_id=creator_id,
            use_category=use_category,
            consent_type=consent_type,
            propagation_policy=propagation_policy,
            **kwargs
        )

        self.rules[rule.rule_id] = rule
        return rule

    def apply_override(
        self,
        derivative_work_id: str,
        original_rule_id: str,
        override_type: str,
        override_value: dict
    ) -> ConsentOverride:
        """
        Apply an override to an inherited rule.

        Overrides can only TIGHTEN restrictions, not loosen them.
        """
        original = self.rules.get(original_rule_id)
        if not original:
            raise ValueError("Original rule not found")

        if not original.can_be_overridden:
            if original.propagation_policy == PropagationPolicy.STRICT_INHERIT:
                return ConsentOverride(
                    derivative_work_id=derivative_work_id,
                    original_rule_id=original_rule_id,
                    override_type=override_type,
                    override_value=override_value,
                    is_valid=False,
                    validation_error="Original rule does not allow overrides"
                )

        # Validate override tightens, doesn't loosen
        override = ConsentOverride(
            derivative_work_id=derivative_work_id,
            original_rule_id=original_rule_id,
            override_type=override_type,
            override_value=override_value
        )

        # Check override is valid (tightening only)
        if override_type == "increase_fee":
            if override_value.get("minimum_fee", 0) < (original.minimum_fee or 0):
                override.is_valid = False
                override.validation_error = "Cannot lower minimum fee"

        elif override_type == "restrict_territory":
            # Can only remove territories, not add
            new_territories = set(override_value.get("territories", []))
            old_territories = set(original.territorial_restrictions or [])
            if new_territories - old_territories:
                override.is_valid = False
                override.validation_error = "Cannot add new territories"

        elif override_type == "change_consent":
            # Can only become more restrictive
            restriction_order = [
                ConsentType.ALLOW,
                ConsentType.ALLOW_WITH_TERMS,
                ConsentType.NEGOTIATE,
                ConsentType.REQUIRE_APPROVAL,
                ConsentType.DENY
            ]
            new_consent = ConsentType(override_value.get("consent_type", "deny"))
            if restriction_order.index(new_consent) < restriction_order.index(original.consent_type):
                override.is_valid = False
                override.validation_error = "Cannot make consent more permissive"

        if override.is_valid:
            self.overrides[override.override_id] = override

        return override

    def compute_consent_chain(
        self,
        work_id: str,
        use_category: str,
        requestor: str = None,
        territory: str = None,
        context: str = None,
        resolution: ConflictResolution = ConflictResolution.MOST_RESTRICTIVE
    ) -> ConsentChain:
        """
        Compute the complete consent chain for a work.

        Walks up the derivative tree, collecting and merging rules.
        """
        chain = ConsentChain(
            work_id=work_id,
            use_category=use_category,
            resolution_method=resolution
        )

        # Collect all applicable rules
        all_rules = []

        def collect_rules(wid: str, depth: int):
            if depth > 50:  # Prevent infinite loops
                return

            # Get rules for this work
            for rule in self.rules.values():
                if rule.source_work_id == wid and rule.use_category == use_category:
                    if rule.applies_to(territory, requestor, context):
                        # Check propagation depth
                        if rule.propagation_depth >= 0 and depth > rule.propagation_depth:
                            continue

                        all_rules.append((rule, depth))

                        chain.links.append({
                            "work_id": wid,
                            "creator_id": rule.source_creator_id,
                            "consent_type": rule.consent_type.value,
                            "rule_id": rule.rule_id,
                            "depth": depth
                        })

            # Recurse to parents
            parents = self.work_parents.get(wid, [])
            for parent_id in parents:
                collect_rules(parent_id, depth + 1)

        collect_rules(work_id, 0)
        chain.chain_length = len(all_rules)

        if not all_rules:
            # No rules found - default behavior
            chain.final_consent = ConsentType.REQUIRE_APPROVAL
            return chain

        # Apply overrides
        for rule, depth in all_rules:
            for override in self.overrides.values():
                if (override.original_rule_id == rule.rule_id and
                    override.derivative_work_id == work_id and
                    override.is_valid):
                    # Apply override
                    if override.override_type == "increase_fee":
                        rule.minimum_fee = override.override_value.get(
                            "minimum_fee", rule.minimum_fee
                        )
                    elif override.override_type == "change_consent":
                        rule.consent_type = ConsentType(
                            override.override_value.get("consent_type")
                        )

        # Resolve conflicts
        if resolution == ConflictResolution.MOST_RESTRICTIVE:
            chain.final_consent = self._resolve_most_restrictive(all_rules)
        elif resolution == ConflictResolution.CREATOR_PRIORITY:
            chain.final_consent = self._resolve_creator_priority(all_rules)
        else:
            chain.final_consent = self._resolve_most_restrictive(all_rules)

        # Find blocking rule if denied
        if chain.final_consent == ConsentType.DENY:
            for rule, depth in all_rules:
                if rule.consent_type == ConsentType.DENY:
                    chain.blocking_rule = rule.rule_id
                    break

        # Aggregate terms
        for rule, depth in all_rules:
            if rule.minimum_fee:
                chain.total_minimum_fee += rule.minimum_fee
            if rule.royalty_rate:
                chain.total_royalty_rate += rule.royalty_rate
            if rule.attribution_required:
                chain.all_attributions.append(rule.source_creator_id)
            chain.combined_restrictions.extend(rule.territorial_restrictions)

        # Dedupe
        chain.all_attributions = list(set(chain.all_attributions))
        chain.combined_restrictions = list(set(chain.combined_restrictions))

        return chain

    def _resolve_most_restrictive(
        self,
        rules: list[tuple[PropagatedConsent, int]]
    ) -> ConsentType:
        """Resolve by taking most restrictive consent."""
        restriction_order = [
            ConsentType.ALLOW,
            ConsentType.ALLOW_WITH_TERMS,
            ConsentType.NEGOTIATE,
            ConsentType.REQUIRE_APPROVAL,
            ConsentType.DENY
        ]

        most_restrictive = ConsentType.ALLOW
        for rule, depth in rules:
            if restriction_order.index(rule.consent_type) > restriction_order.index(most_restrictive):
                most_restrictive = rule.consent_type

        return most_restrictive

    def _resolve_creator_priority(
        self,
        rules: list[tuple[PropagatedConsent, int]]
    ) -> ConsentType:
        """Resolve by original creator's rule (depth 0 or highest depth)."""
        # Find the deepest rule (closest to original)
        deepest = max(rules, key=lambda x: x[1], default=None)
        if deepest:
            return deepest[0].consent_type
        return ConsentType.REQUIRE_APPROVAL

    def propagate_rule_change(
        self,
        rule_id: str,
        new_consent_type: ConsentType = None,
        new_minimum_fee: float = None
    ) -> list[str]:
        """
        Propagate a rule change to all affected works.

        Returns list of affected work IDs.
        """
        rule = self.rules.get(rule_id)
        if not rule:
            return []

        # Update rule
        if new_consent_type:
            rule.consent_type = new_consent_type
        if new_minimum_fee is not None:
            rule.minimum_fee = new_minimum_fee
        rule.version += 1

        # Find affected works
        affected = []
        source_work = rule.source_work_id

        def find_descendants(work_id: str, depth: int):
            if depth > 50:
                return
            for wid, parents in self.work_parents.items():
                if work_id in parents:
                    if rule.propagation_depth < 0 or depth <= rule.propagation_depth:
                        affected.append(wid)
                        find_descendants(wid, depth + 1)

        find_descendants(source_work, 1)

        return list(set(affected))

    def get_consent_summary(
        self,
        work_id: str,
        use_categories: list[str] = None
    ) -> dict:
        """Get summary of consent status across categories."""
        if not use_categories:
            use_categories = [
                "streaming", "sync_film", "sync_commercial",
                "ai_training", "ai_voice_clone", "sampling"
            ]

        summary = {
            "work_id": work_id,
            "categories": {}
        }

        for category in use_categories:
            chain = self.compute_consent_chain(work_id, category)
            summary["categories"][category] = {
                "consent": chain.final_consent.value,
                "chain_length": chain.chain_length,
                "total_fee": chain.total_minimum_fee,
                "attributions_required": len(chain.all_attributions),
                "blocked_by": chain.blocking_rule
            }

        return summary


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate consent propagation."""
    print("\n" + "=" * 70)
    print("CONSENT PROPAGATION — DEMO")
    print("One decision protects your work everywhere")
    print("=" * 70)

    engine = ConsentPropagationEngine()

    # Register works with lineage
    print("\n" + "─" * 50)
    print("1. REGISTERING WORK HIERARCHY")
    print("─" * 50)

    # Original
    engine.register_work("original-song", ["creator-A"])
    print("  original-song (Creator A)")

    # Sample
    engine.register_work("sample-track", ["creator-B"], ["original-song"])
    print("    └── sample-track (Creator B) - samples original")

    # Remix
    engine.register_work("remix-version", ["creator-C"], ["sample-track"])
    print("        └── remix-version (Creator C) - remixes sample")

    # AI derivative
    engine.register_work("ai-generated", ["ai-company"], ["original-song"])
    print("    └── ai-generated (AI Company) - AI trained on original")

    # Set consent rules
    print("\n" + "─" * 50)
    print("2. SETTING CONSENT RULES")
    print("─" * 50)

    # Creator A allows streaming, denies AI training
    rule1 = engine.set_consent_rule(
        work_id="original-song",
        creator_id="creator-A",
        use_category="streaming",
        consent_type=ConsentType.ALLOW,
        minimum_fee=0.001,  # Per stream
        propagation_policy=PropagationPolicy.INHERIT_AND_TIGHTEN
    )
    print(f"  Creator A: ALLOW streaming (inheritable)")

    rule2 = engine.set_consent_rule(
        work_id="original-song",
        creator_id="creator-A",
        use_category="ai_training",
        consent_type=ConsentType.DENY,
        propagation_policy=PropagationPolicy.STRICT_INHERIT  # Cannot be overridden!
    )
    print(f"  Creator A: DENY AI training (strict - NO overrides)")

    rule3 = engine.set_consent_rule(
        work_id="original-song",
        creator_id="creator-A",
        use_category="sync_commercial",
        consent_type=ConsentType.ALLOW_WITH_TERMS,
        minimum_fee=5000.0,
        propagation_policy=PropagationPolicy.INHERIT_AND_TIGHTEN
    )
    print(f"  Creator A: ALLOW sync with $5,000 minimum")

    # Creator B adds their own rule
    rule4 = engine.set_consent_rule(
        work_id="sample-track",
        creator_id="creator-B",
        use_category="sync_commercial",
        consent_type=ConsentType.ALLOW_WITH_TERMS,
        minimum_fee=2000.0  # Their additional fee
    )
    print(f"  Creator B: Additional $2,000 for sync on sample")

    # Compute consent chains
    print("\n" + "─" * 50)
    print("3. COMPUTING CONSENT CHAINS")
    print("─" * 50)

    # Check remix for streaming
    print("\n  REMIX → STREAMING:")
    chain1 = engine.compute_consent_chain("remix-version", "streaming")
    print(f"    Final consent: {chain1.final_consent.value}")
    print(f"    Chain length: {chain1.chain_length}")
    print(f"    Total fee per stream: ${chain1.total_minimum_fee:.4f}")

    # Check remix for AI training
    print("\n  REMIX → AI TRAINING:")
    chain2 = engine.compute_consent_chain("remix-version", "ai_training")
    print(f"    Final consent: {chain2.final_consent.value}")
    print(f"    Chain length: {chain2.chain_length}")
    print(f"    Blocked by: {chain2.blocking_rule}")
    print("    ← Creator A's DENY propagates through ALL derivatives!")

    # Check remix for sync
    print("\n  REMIX → SYNC COMMERCIAL:")
    chain3 = engine.compute_consent_chain("remix-version", "sync_commercial")
    print(f"    Final consent: {chain3.final_consent.value}")
    print(f"    Chain length: {chain3.chain_length}")
    print(f"    Total minimum fee: ${chain3.total_minimum_fee:,.2f}")
    print(f"    Attributions required: {chain3.all_attributions}")

    # Try to override (should fail for AI)
    print("\n" + "─" * 50)
    print("4. ATTEMPTING OVERRIDES")
    print("─" * 50)

    # Try to override AI training denial
    override_attempt = engine.apply_override(
        derivative_work_id="sample-track",
        original_rule_id=rule2.rule_id,
        override_type="change_consent",
        override_value={"consent_type": "allow"}  # Try to allow
    )
    print(f"\n  Attempting to override AI training denial:")
    print(f"    Valid: {override_attempt.is_valid}")
    print(f"    Error: {override_attempt.validation_error}")
    print("    ← Cannot loosen strict inherit rules!")

    # Valid override: increase sync fee
    override_valid = engine.apply_override(
        derivative_work_id="remix-version",
        original_rule_id=rule3.rule_id,
        override_type="increase_fee",
        override_value={"minimum_fee": 10000.0}  # Increase to $10k
    )
    print(f"\n  Increasing sync fee for remix:")
    print(f"    Valid: {override_valid.is_valid}")
    print("    ← Tightening is allowed!")

    # Propagate a rule change
    print("\n" + "─" * 50)
    print("5. RULE CHANGE PROPAGATION")
    print("─" * 50)

    print("\n  Creator A changes streaming fee to $0.002...")
    affected = engine.propagate_rule_change(
        rule_id=rule1.rule_id,
        new_minimum_fee=0.002
    )
    print(f"    Affected works: {affected}")
    print("    ← All derivatives automatically updated!")

    # Get consent summary
    print("\n" + "─" * 50)
    print("6. CONSENT SUMMARY")
    print("─" * 50)

    summary = engine.get_consent_summary("remix-version")
    print(f"\n  Summary for remix-version:")
    for category, status in summary["categories"].items():
        blocked = " (BLOCKED)" if status["blocked_by"] else ""
        print(f"    {category}: {status['consent']}{blocked}")
        if status["total_fee"] > 0:
            print(f"      └── Total fee: ${status['total_fee']:,.2f}")

    print("\n" + "=" * 70)
    print("2056 VALUE: Consent decisions flow through the entire creative tree")
    print("=" * 70)


if __name__ == "__main__":
    demo()
