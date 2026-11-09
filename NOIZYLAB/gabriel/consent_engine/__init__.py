"""
NOIZY.ai Creator Consent Engine
================================
Protecting creator rights through automated consent enforcement.

This system:
1. Manages creator consent registries
2. Processes licensing inquiries against consent
3. Approves or declines automatically based on creator settings
4. Generates transparent receipts for creators
5. Logs everything to the providence chain

No hidden deals. No mystery negotiations. Full transparency.
"""

from .schema import (
    ConsentRegistry,
    LicensingInquiry,
    LicensingDecision,
    CreatorReceipt,
    UseType,
    ConsentStatus,
    LicenseType,
    RoyaltyType,
    RoyaltySplit,
    PricePoint,
    UseRestriction,
)

from .handlers.licensing_inquiry import LicensingInquiryHandler, InquiryParser
from .verification.consent_verifier import ConsentVerifier
from .receipts.receipt_generator import ReceiptGenerator, ReceiptFormatter
from .providence.chain import ProvidenceChain, ProvidenceViewer
from .gabriel_integration import GabrielConsentTools, create_test_registry

__all__ = [
    # Schema
    "ConsentRegistry",
    "LicensingInquiry",
    "LicensingDecision",
    "CreatorReceipt",
    "UseType",
    "ConsentStatus",
    "LicenseType",
    "RoyaltyType",
    "RoyaltySplit",
    "PricePoint",
    "UseRestriction",
    # Handlers
    "LicensingInquiryHandler",
    "InquiryParser",
    # Verification
    "ConsentVerifier",
    # Receipts
    "ReceiptGenerator",
    "ReceiptFormatter",
    # Providence
    "ProvidenceChain",
    "ProvidenceViewer",
    # Gabriel
    "GabrielConsentTools",
    "create_test_registry",
]
