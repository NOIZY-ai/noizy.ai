"""
Licensing Inquiry Handler
=========================
Receives licensing inquiries, verifies against consent registry,
approves or declines, generates receipts, logs to providence chain.

This is Module 1 — the core of creator protection.
"""

import json
import hashlib
from datetime import datetime
from typing import Optional
from dataclasses import asdict

from ..schema import (
    LicensingInquiry,
    LicensingDecision,
    CreatorReceipt,
    ConsentRegistry,
    ConsentStatus,
    UseType,
    LicenseType,
)
from ..verification.consent_verifier import ConsentVerifier
from ..receipts.receipt_generator import ReceiptGenerator
from ..providence.chain import ProvidenceChain


class LicensingInquiryHandler:
    """
    The main entry point for licensing inquiries.

    Flow:
    1. Receive inquiry (email, form, API)
    2. Extract: WHO, WHAT, WHY
    3. Query Gabriel MCP for creator's consent registry
    4. Verify request against consent
    5. Approve, decline, or flag for review
    6. Generate receipt
    7. Email creator
    8. Log to providence chain
    """

    def __init__(self, gabriel_mcp_client=None, email_client=None):
        self.gabriel = gabriel_mcp_client
        self.email = email_client
        self.verifier = ConsentVerifier()
        self.receipt_gen = ReceiptGenerator()
        self.providence = ProvidenceChain()

    async def handle_inquiry(self, inquiry: LicensingInquiry) -> LicensingDecision:
        """
        Main handler — process a licensing inquiry end-to-end.
        """
        print(f"\n{'='*60}")
        print(f"LICENSING INQUIRY RECEIVED")
        print(f"{'='*60}")
        print(f"From: {inquiry.requestor_name} ({inquiry.requestor_company})")
        print(f"Work: {inquiry.work_title}")
        print(f"Use:  {inquiry.use_type.value}")
        print(f"{'='*60}\n")

        # Step 1: Fetch creator's consent registry from Gabriel MCP
        registry = await self._fetch_consent_registry(inquiry.work_id)

        if not registry:
            return self._create_error_decision(
                inquiry,
                "Work not found in consent registry"
            )

        print(f"✓ Fetched consent registry for: {registry.creator_name}")
        print(f"  Work: {registry.work_title}")
        print(f"  Default consent: {registry.default_consent.value}")

        # Step 2: Verify inquiry against consent
        decision = self.verifier.verify(inquiry, registry)

        print(f"\n{'─'*60}")
        print(f"VERIFICATION RESULT: {decision.status.value.upper()}")
        print(f"{'─'*60}")

        # Step 3: Generate creator receipt
        receipt = self.receipt_gen.generate(inquiry, registry, decision)

        # Step 4: Log to providence chain
        providence_hash = await self._log_to_providence(inquiry, decision, receipt)
        decision.providence_hash = providence_hash
        receipt.providence_hash = providence_hash

        print(f"✓ Logged to providence chain: {providence_hash[:16]}...")

        # Step 5: Email creator
        if registry.notify_on_approval or registry.notify_on_decline:
            await self._email_creator(registry, receipt)
            print(f"✓ Receipt emailed to: {registry.creator_email}")

        # Step 6: Email requestor with decision
        await self._email_requestor(inquiry, decision, registry)
        print(f"✓ Decision emailed to: {inquiry.requestor_email}")

        print(f"\n{'='*60}")
        print(f"INQUIRY PROCESSING COMPLETE")
        print(f"{'='*60}\n")

        return decision

    async def _fetch_consent_registry(self, work_id: str) -> Optional[ConsentRegistry]:
        """Query Gabriel MCP for the consent registry."""
        if self.gabriel:
            # Real Gabriel MCP query
            result = await self.gabriel.call_tool(
                "consent_registry_query",
                {"work_id": work_id}
            )
            if result:
                return ConsentRegistry(**result)

        # For testing without Gabriel MCP
        return None

    def _create_error_decision(
        self,
        inquiry: LicensingInquiry,
        error: str
    ) -> LicensingDecision:
        """Create a decision for error cases."""
        return LicensingDecision(
            inquiry_id=inquiry.inquiry_id,
            status=ConsentStatus.DENIED,
            approved=False,
            decline_reason=error,
            decided_by="system_error"
        )

    async def _log_to_providence(
        self,
        inquiry: LicensingInquiry,
        decision: LicensingDecision,
        receipt: CreatorReceipt
    ) -> str:
        """Log the transaction to the providence chain."""
        record = {
            "type": "licensing_inquiry",
            "inquiry": asdict(inquiry),
            "decision": asdict(decision),
            "receipt_id": receipt.receipt_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        return await self.providence.add_record(record)

    async def _email_creator(
        self,
        registry: ConsentRegistry,
        receipt: CreatorReceipt
    ):
        """Send the receipt to the creator."""
        if self.email:
            subject = f"Licensing Inquiry: {receipt.work_title} — {'APPROVED' if receipt.approved else 'DECLINED'}"
            body = receipt.to_email_body()
            await self.email.send(
                to=registry.creator_email,
                subject=subject,
                body=body
            )

    async def _email_requestor(
        self,
        inquiry: LicensingInquiry,
        decision: LicensingDecision,
        registry: ConsentRegistry
    ):
        """Send the decision to the requestor."""
        if not self.email:
            return

        if decision.approved:
            subject = f"License Approved: {registry.work_title}"
            body = self._generate_approval_email(inquiry, decision, registry)
        else:
            subject = f"License Request: {registry.work_title}"
            body = self._generate_decline_email(inquiry, decision, registry)

        await self.email.send(
            to=inquiry.requestor_email,
            subject=subject,
            body=body
        )

    def _generate_approval_email(
        self,
        inquiry: LicensingInquiry,
        decision: LicensingDecision,
        registry: ConsentRegistry
    ) -> str:
        """Generate approval email for requestor."""
        return f"""
Dear {inquiry.requestor_name},

Your licensing request for "{registry.work_title}" has been APPROVED.

LICENSE TERMS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Work: {registry.work_title}
Creator: {registry.creator_name}
Use Type: {inquiry.use_type.value}

Fee: ${decision.fee:,.2f} USD
License Type: {decision.license_type.value if decision.license_type else 'Standard'}

USAGE BOUNDARIES:
{chr(10).join(f'  • {b}' for b in decision.usage_boundaries)}

CREDIT REQUIREMENTS:
{decision.credit_requirements or 'Standard credit required'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To proceed, please confirm acceptance of these terms by replying
to this email. Payment instructions will follow.

This license is subject to the terms outlined above. Any use
outside these boundaries requires a new licensing agreement.

Providence Record: {decision.providence_hash}

— NOIZY.ai Licensing
"""

    def _generate_decline_email(
        self,
        inquiry: LicensingInquiry,
        decision: LicensingDecision,
        registry: ConsentRegistry
    ) -> str:
        """Generate decline email for requestor."""
        return f"""
Dear {inquiry.requestor_name},

Thank you for your interest in licensing "{registry.work_title}".

After reviewing your request against the creator's consent preferences,
we are unable to approve this license at this time.

REASON:
{decision.decline_reason}

CONSENT RULES THAT APPLIED:
{chr(10).join(f'  • {r}' for r in decision.consent_rules_applied)}

This decision reflects the creator's stated preferences for how their
work may be used. NOIZY.ai enforces creator consent — we don't negotiate
against their wishes.

If you believe this decision was made in error, or would like to submit
a modified request, please reply to this email with additional context.

— NOIZY.ai Licensing
"""


class InquiryParser:
    """
    Parse incoming emails/messages into structured LicensingInquiry objects.
    Uses Claude to extract the key information.
    """

    def __init__(self, claude_client=None):
        self.claude = claude_client

    async def parse_email(self, email_content: str, sender: str) -> LicensingInquiry:
        """
        Parse an email into a LicensingInquiry.
        Extracts: WHO, WHAT, WHY
        """
        # Use Claude to extract structured data
        if self.claude:
            extraction = await self._extract_with_claude(email_content)
        else:
            extraction = self._basic_extraction(email_content)

        return LicensingInquiry(
            requestor_name=extraction.get("name", "Unknown"),
            requestor_email=sender,
            requestor_company=extraction.get("company"),
            work_title=extraction.get("work_title", "Unknown"),
            use_type=self._parse_use_type(extraction.get("use_type", "commercial")),
            use_description=extraction.get("use_description", email_content[:500]),
            project_name=extraction.get("project_name"),
            project_description=extraction.get("project_description"),
            territory=extraction.get("territory", "worldwide"),
            duration=extraction.get("duration"),
            offered_fee=extraction.get("offered_fee"),
            offered_terms=extraction.get("offered_terms"),
            raw_message=email_content
        )

    async def _extract_with_claude(self, content: str) -> dict:
        """Use Claude to extract licensing inquiry details."""
        prompt = f"""
Extract licensing inquiry details from this email. Return JSON:

{{
    "name": "requestor's name",
    "company": "their company/organization",
    "work_title": "the work they want to license",
    "use_type": "streaming|sync|sample|remix|cover|ai_training|commercial|etc",
    "use_description": "what they want to do with it",
    "project_name": "name of their project if mentioned",
    "project_description": "description of their project",
    "territory": "geographic scope",
    "duration": "how long they need it",
    "offered_fee": numeric fee if mentioned,
    "offered_terms": "any terms they proposed"
}}

EMAIL:
{content}
"""
        # This would call Claude API
        # response = await self.claude.messages.create(...)
        return {}

    def _basic_extraction(self, content: str) -> dict:
        """Basic extraction without Claude."""
        return {
            "name": "Unknown",
            "use_description": content[:500]
        }

    def _parse_use_type(self, use_str: str) -> UseType:
        """Convert string to UseType enum."""
        mapping = {
            "streaming": UseType.STREAMING,
            "sync": UseType.SYNC,
            "sample": UseType.SAMPLE,
            "remix": UseType.REMIX,
            "cover": UseType.COVER,
            "ai_training": UseType.AI_TRAINING,
            "ai": UseType.AI_TRAINING,
            "broadcast": UseType.BROADCAST,
            "live": UseType.LIVE_PERFORMANCE,
            "merch": UseType.MERCHANDISE,
            "nft": UseType.NFT,
            "education": UseType.EDUCATIONAL,
            "nonprofit": UseType.NON_PROFIT,
            "personal": UseType.PERSONAL,
            "commercial": UseType.COMMERCIAL,
        }
        return mapping.get(use_str.lower(), UseType.COMMERCIAL)
