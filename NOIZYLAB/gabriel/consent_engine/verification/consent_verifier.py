"""
Consent Verification Engine
============================
The brain of the consent system.

Compares licensing inquiries against creator consent registries
and makes decisions: APPROVE, DECLINE, or REVIEW.
"""

from dataclasses import dataclass
from typing import Optional

from ..schema import (
    LicensingInquiry,
    LicensingDecision,
    ConsentRegistry,
    ConsentStatus,
    UseType,
    LicenseType,
    PricePoint,
    UseRestriction,
)


@dataclass
class VerificationResult:
    """Detailed result of consent verification."""
    passes: bool
    status: ConsentStatus
    reasons: list[str]
    rules_applied: list[str]
    suggested_fee: Optional[float] = None
    suggested_terms: Optional[str] = None


class ConsentVerifier:
    """
    Verifies licensing inquiries against consent registries.

    Checks:
    1. Is this use type allowed?
    2. Is the requestor excluded?
    3. Is the context excluded?
    4. Does the offer meet price requirements?
    5. Are there specific restrictions?

    Returns a decision with full transparency on which rules applied.
    """

    def verify(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry
    ) -> LicensingDecision:
        """
        Main verification method.
        Returns a complete LicensingDecision.
        """
        rules_applied = []
        decline_reasons = []

        # Check 1: Is this use type explicitly denied?
        use_check = self._check_use_type(inquiry.use_type, registry)
        rules_applied.extend(use_check.rules_applied)

        if use_check.status == ConsentStatus.DENIED:
            return self._create_decline(
                inquiry,
                registry,
                use_check.reasons[0] if use_check.reasons else "Use type not permitted",
                rules_applied
            )

        # Check 2: Is the requestor excluded?
        if inquiry.requestor_company:
            party_check = self._check_party(inquiry.requestor_company, registry)
            rules_applied.extend(party_check.rules_applied)

            if not party_check.passes:
                return self._create_decline(
                    inquiry,
                    registry,
                    party_check.reasons[0] if party_check.reasons else "Party excluded",
                    rules_applied
                )

        # Check 3: Is the context excluded?
        context_check = self._check_context(inquiry.use_description, registry)
        rules_applied.extend(context_check.rules_applied)

        if not context_check.passes:
            return self._create_decline(
                inquiry,
                registry,
                context_check.reasons[0] if context_check.reasons else "Context excluded",
                rules_applied
            )

        # Check 4: Does the offer meet price requirements?
        price_check = self._check_pricing(inquiry, registry)
        rules_applied.extend(price_check.rules_applied)

        if not price_check.passes and price_check.status != ConsentStatus.NEGOTIABLE:
            return self._create_decline(
                inquiry,
                registry,
                price_check.reasons[0] if price_check.reasons else "Pricing requirements not met",
                rules_applied
            )

        # Check 5: Does this need human review?
        if use_check.status == ConsentStatus.REQUIRES_APPROVAL:
            return self._create_review_needed(
                inquiry,
                registry,
                "Creator requires approval for this use type",
                rules_applied
            )

        if price_check.status == ConsentStatus.NEGOTIABLE:
            return self._create_review_needed(
                inquiry,
                registry,
                "Pricing requires negotiation",
                rules_applied
            )

        # All checks passed — APPROVE
        return self._create_approval(
            inquiry,
            registry,
            price_check.suggested_fee,
            price_check.suggested_terms,
            rules_applied
        )

    def _check_use_type(
        self,
        use_type: UseType,
        registry: ConsentRegistry
    ) -> VerificationResult:
        """Check if the use type is allowed."""
        restriction = registry.get_consent_for_use(use_type)

        rules = [f"Checked consent for {use_type.value}"]

        if restriction.status == ConsentStatus.DENIED:
            return VerificationResult(
                passes=False,
                status=ConsentStatus.DENIED,
                reasons=[f"Creator has explicitly denied {use_type.value} use"],
                rules_applied=rules + [f"DENIED: {use_type.value} not permitted"]
            )

        if restriction.status == ConsentStatus.ALLOWED:
            return VerificationResult(
                passes=True,
                status=ConsentStatus.ALLOWED,
                reasons=[],
                rules_applied=rules + [f"ALLOWED: {use_type.value} permitted"]
            )

        if restriction.status == ConsentStatus.REQUIRES_APPROVAL:
            return VerificationResult(
                passes=True,
                status=ConsentStatus.REQUIRES_APPROVAL,
                reasons=["Requires creator approval"],
                rules_applied=rules + [f"REVIEW: {use_type.value} requires approval"]
            )

        # Default consent
        return VerificationResult(
            passes=True,
            status=registry.default_consent,
            reasons=[],
            rules_applied=rules + [f"DEFAULT: Using default consent ({registry.default_consent.value})"]
        )

    def _check_party(
        self,
        party_name: str,
        registry: ConsentRegistry
    ) -> VerificationResult:
        """Check if the requesting party is excluded."""
        rules = [f"Checked party: {party_name}"]

        if registry.is_party_excluded(party_name):
            return VerificationResult(
                passes=False,
                status=ConsentStatus.DENIED,
                reasons=[f"'{party_name}' is on creator's exclusion list"],
                rules_applied=rules + [f"DENIED: {party_name} is excluded"]
            )

        return VerificationResult(
            passes=True,
            status=ConsentStatus.ALLOWED,
            reasons=[],
            rules_applied=rules + [f"PASSED: {party_name} not excluded"]
        )

    def _check_context(
        self,
        context: str,
        registry: ConsentRegistry
    ) -> VerificationResult:
        """Check if the use context is excluded."""
        rules = ["Checked context against exclusions"]

        # Check all restrictions for excluded contexts
        for restriction in registry.use_restrictions:
            for excluded in restriction.excluded_contexts:
                if excluded.lower() in context.lower():
                    return VerificationResult(
                        passes=False,
                        status=ConsentStatus.DENIED,
                        reasons=[f"Context includes excluded term: '{excluded}'"],
                        rules_applied=rules + [f"DENIED: Context contains '{excluded}'"]
                    )

        return VerificationResult(
            passes=True,
            status=ConsentStatus.ALLOWED,
            reasons=[],
            rules_applied=rules + ["PASSED: No excluded contexts found"]
        )

    def _check_pricing(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry
    ) -> VerificationResult:
        """Check if the offered price meets requirements."""
        price_point = registry.get_price_for_use(inquiry.use_type)
        rules = [f"Checked pricing for {inquiry.use_type.value}"]

        if not price_point:
            # No pricing set — negotiable
            return VerificationResult(
                passes=True,
                status=ConsentStatus.NEGOTIABLE,
                reasons=["No pricing set for this use type"],
                rules_applied=rules + ["REVIEW: No pricing set, requires negotiation"],
                suggested_fee=None,
                suggested_terms="To be negotiated"
            )

        # Auto-approve under threshold?
        if registry.auto_approve_under and inquiry.offered_fee:
            if inquiry.offered_fee >= registry.auto_approve_under:
                return VerificationResult(
                    passes=True,
                    status=ConsentStatus.ALLOWED,
                    reasons=["Offer meets auto-approve threshold"],
                    rules_applied=rules + [f"AUTO-APPROVED: Offer ${inquiry.offered_fee} >= ${registry.auto_approve_under}"],
                    suggested_fee=inquiry.offered_fee,
                    suggested_terms=f"Auto-approved at ${inquiry.offered_fee}"
                )

        # Check against minimum
        if inquiry.offered_fee:
            if inquiry.offered_fee < price_point.minimum_fee:
                return VerificationResult(
                    passes=False,
                    status=ConsentStatus.DENIED,
                    reasons=[f"Offer ${inquiry.offered_fee} below minimum ${price_point.minimum_fee}"],
                    rules_applied=rules + [f"DENIED: Offer below minimum (${price_point.minimum_fee})"]
                )
            else:
                return VerificationResult(
                    passes=True,
                    status=ConsentStatus.ALLOWED,
                    reasons=["Offer meets minimum"],
                    rules_applied=rules + [f"APPROVED: Offer ${inquiry.offered_fee} >= minimum ${price_point.minimum_fee}"],
                    suggested_fee=inquiry.offered_fee,
                    suggested_terms=f"Flat fee: ${inquiry.offered_fee}"
                )

        # No offer made — use creator's preferred pricing
        return VerificationResult(
            passes=True,
            status=ConsentStatus.ALLOWED,
            reasons=["Using creator's preferred pricing"],
            rules_applied=rules + [f"PRICED: Using minimum fee ${price_point.minimum_fee}"],
            suggested_fee=price_point.preferred_fee or price_point.minimum_fee,
            suggested_terms=f"Fee: ${price_point.preferred_fee or price_point.minimum_fee}"
        )

    def _create_approval(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry,
        fee: Optional[float],
        terms: Optional[str],
        rules: list[str]
    ) -> LicensingDecision:
        """Create an approval decision."""
        # Get usage boundaries from restrictions
        restriction = registry.get_consent_for_use(inquiry.use_type)
        boundaries = restriction.restrictions if restriction else []

        # Get credit requirements
        credit = restriction.credit_format if restriction and restriction.requires_credit else None
        if not credit and restriction and restriction.requires_credit:
            credit = f"Credit: {registry.creator_name}"

        return LicensingDecision(
            inquiry_id=inquiry.inquiry_id,
            registry_id=registry.registry_id,
            status=ConsentStatus.ALLOWED,
            approved=True,
            license_type=LicenseType.NON_EXCLUSIVE,
            fee=fee,
            royalty_terms=terms,
            usage_boundaries=boundaries,
            credit_requirements=credit,
            consent_rules_applied=rules,
            decided_by="automated"
        )

    def _create_decline(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry,
        reason: str,
        rules: list[str]
    ) -> LicensingDecision:
        """Create a decline decision."""
        return LicensingDecision(
            inquiry_id=inquiry.inquiry_id,
            registry_id=registry.registry_id,
            status=ConsentStatus.DENIED,
            approved=False,
            decline_reason=reason,
            consent_rules_applied=rules,
            decided_by="automated"
        )

    def _create_review_needed(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry,
        reason: str,
        rules: list[str]
    ) -> LicensingDecision:
        """Create a decision requiring human review."""
        return LicensingDecision(
            inquiry_id=inquiry.inquiry_id,
            registry_id=registry.registry_id,
            status=ConsentStatus.REQUIRES_APPROVAL,
            approved=False,
            review_reason=reason,
            consent_rules_applied=rules,
            decided_by="requires_human"
        )
