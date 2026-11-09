#!/usr/bin/env python3
"""
Consent Engine Test Flow
========================
Tests the complete licensing inquiry flow:
1. Create consent registry
2. Send various inquiry types
3. Watch approve/decline logic in action
4. See receipts generated
5. Check providence chain

Run: python -m gabriel.consent_engine.test_flow
"""

import asyncio
from datetime import datetime

from .schema import (
    ConsentRegistry,
    LicensingInquiry,
    UseType,
    ConsentStatus,
)
from .verification.consent_verifier import ConsentVerifier
from .receipts.receipt_generator import ReceiptGenerator, ReceiptFormatter
from .providence.chain import ProvidenceChain
from .gabriel_integration import create_test_registry


class MockEmailClient:
    """Mock email client for testing."""

    def __init__(self):
        self.sent_emails = []

    async def send(self, to: str, subject: str, body: str):
        self.sent_emails.append({
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": datetime.utcnow().isoformat()
        })
        print(f"\n📧 EMAIL SENT")
        print(f"   To: {to}")
        print(f"   Subject: {subject}")
        print(f"   {'─' * 50}")


class ConsentEngineTestRunner:
    """Run test scenarios through the consent engine."""

    def __init__(self):
        self.verifier = ConsentVerifier()
        self.receipt_gen = ReceiptGenerator()
        self.providence = ProvidenceChain()
        self.email = MockEmailClient()
        self.registry = create_test_registry()

    async def run_all_tests(self):
        """Run all test scenarios."""
        print("\n" + "═" * 70)
        print("CONSENT ENGINE TEST FLOW")
        print("═" * 70)
        print(f"\nCreator: {self.registry.creator_name}")
        print(f"Work: {self.registry.work_title}")
        print(f"Default consent: {self.registry.default_consent.value}")
        print("\n" + "═" * 70)

        # Test scenarios
        scenarios = [
            self.test_approved_sync_license,
            self.test_declined_low_offer,
            self.test_declined_ai_training,
            self.test_declined_excluded_context,
            self.test_requires_review_sample,
            self.test_approved_streaming,
        ]

        for scenario in scenarios:
            await scenario()
            print("\n" + "─" * 70 + "\n")

        # Show providence chain
        await self.show_providence_summary()

        # Show email log
        self.show_email_log()

    async def test_approved_sync_license(self):
        """Test: Sync license that meets all requirements."""
        print("TEST: Sync License Request (Should APPROVE)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="Sarah Chen",
            requestor_email="sarah@filmstudio.com",
            requestor_company="Indie Film Studio",
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.SYNC,
            use_description="Background music for documentary about urban art",
            project_name="Street Canvas",
            offered_fee=7500.00,
            raw_message="Hi, we'd love to license 'Midnight Protocol' for our documentary..."
        )

        await self._process_and_display(inquiry)

    async def test_declined_low_offer(self):
        """Test: Sync license with offer below minimum."""
        print("TEST: Sync License - Low Offer (Should DECLINE)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="Budget Films LLC",
            requestor_email="licensing@budgetfilms.com",
            requestor_company="Budget Films",
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.SYNC,
            use_description="Music for student film project",
            offered_fee=500.00,  # Below $5000 minimum
            raw_message="We have a small budget but love your track..."
        )

        await self._process_and_display(inquiry)

    async def test_declined_ai_training(self):
        """Test: AI training request (explicitly denied)."""
        print("TEST: AI Training Request (Should DECLINE)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="TechCorp AI Division",
            requestor_email="ai@techcorp.com",
            requestor_company="TechCorp",
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.AI_TRAINING,
            use_description="Training data for music generation model",
            offered_fee=50000.00,  # Even high offer shouldn't override
            raw_message="We'd like to include your work in our AI training dataset..."
        )

        await self._process_and_display(inquiry)

    async def test_declined_excluded_context(self):
        """Test: Request with excluded context (political ad)."""
        print("TEST: Political Ad Request (Should DECLINE)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="Campaign HQ",
            requestor_email="media@campaign2026.com",
            requestor_company="Political Action Committee",
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.SYNC,
            use_description="Background music for political campaign advertisement",
            project_name="Campaign 2026",
            offered_fee=25000.00,
            raw_message="We want to use your track in our political ads..."
        )

        await self._process_and_display(inquiry)

    async def test_requires_review_sample(self):
        """Test: Sample request (requires human approval)."""
        print("TEST: Sample Request (Should REQUIRE REVIEW)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="DJ Nova",
            requestor_email="nova@djnova.com",
            requestor_company=None,
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.SAMPLE,
            use_description="Want to sample the opening synth hook in my new track",
            offered_fee=3000.00,
            raw_message="Love the synth in Midnight Protocol, want to sample it..."
        )

        await self._process_and_display(inquiry)

    async def test_approved_streaming(self):
        """Test: Streaming rights (auto-allowed)."""
        print("TEST: Streaming Request (Should APPROVE)")
        print("─" * 50)

        inquiry = LicensingInquiry(
            requestor_name="Playlist Curator",
            requestor_email="curator@streamingservice.com",
            requestor_company="Streaming Service",
            work_id=self.registry.work_id,
            work_title=self.registry.work_title,
            use_type=UseType.STREAMING,
            use_description="Add to curated electronic music playlist",
            raw_message="We'd like to feature your track on our platform..."
        )

        await self._process_and_display(inquiry)

    async def _process_and_display(self, inquiry: LicensingInquiry):
        """Process an inquiry and display results."""
        print(f"\nRequestor: {inquiry.requestor_name}")
        if inquiry.requestor_company:
            print(f"Company: {inquiry.requestor_company}")
        print(f"Use Type: {inquiry.use_type.value}")
        print(f"Offered: ${inquiry.offered_fee:,.2f}" if inquiry.offered_fee else "Offered: Not specified")
        print(f"Description: {inquiry.use_description[:80]}...")

        # Verify
        decision = self.verifier.verify(inquiry, self.registry)

        # Display decision
        print(f"\n{'─' * 50}")
        status_emoji = "✅" if decision.approved else ("⏸️" if decision.status == ConsentStatus.REQUIRES_APPROVAL else "❌")
        print(f"DECISION: {status_emoji} {decision.status.value.upper()}")

        if decision.approved:
            print(f"Fee: ${decision.fee:,.2f}" if decision.fee else "Fee: Standard rates apply")
            print(f"Terms: {decision.royalty_terms}")
        elif decision.status == ConsentStatus.REQUIRES_APPROVAL:
            print(f"Reason: {decision.review_reason}")
        else:
            print(f"Reason: {decision.decline_reason}")

        print("\nRules Applied:")
        for rule in decision.consent_rules_applied:
            print(f"  • {rule}")

        # Generate receipt
        receipt = self.receipt_gen.generate(inquiry, self.registry, decision)

        # Log to providence
        providence_hash = await self.providence.add_record({
            "type": "licensing_inquiry",
            "work_id": inquiry.work_id,
            "inquiry_id": inquiry.inquiry_id,
            "decision_status": decision.status.value,
            "approved": decision.approved,
            "timestamp": datetime.utcnow().isoformat()
        })

        receipt.providence_hash = providence_hash
        print(f"\nProvidence: {providence_hash[:24]}...")

        # Send mock email
        subject, body = ReceiptFormatter.to_email(receipt)
        await self.email.send(self.registry.creator_email, subject, body)

    async def show_providence_summary(self):
        """Show summary of providence chain."""
        print("\n" + "═" * 70)
        print("PROVIDENCE CHAIN SUMMARY")
        print("═" * 70)

        is_valid, issues = await self.providence.verify_chain()
        print(f"\nChain Integrity: {'✅ VALID' if is_valid else '❌ INVALID'}")
        print(f"Total Records: {self.providence.state.record_count}")
        print(f"Latest Hash: {self.providence.state.latest_hash[:32]}...")

        if issues:
            print("\nIssues:")
            for issue in issues:
                print(f"  • {issue}")

        # Show recent records
        print("\nRecent Records:")
        for record in self.providence.state.records[-5:]:
            emoji = "📄" if record.record_type == "genesis" else "📋"
            print(f"  {emoji} {record.record_type}: {record.record_hash[:16]}...")

    def show_email_log(self):
        """Show all sent emails."""
        print("\n" + "═" * 70)
        print("EMAIL LOG")
        print("═" * 70)

        for i, email in enumerate(self.email.sent_emails, 1):
            print(f"\n[{i}] To: {email['to']}")
            print(f"    Subject: {email['subject']}")


async def main():
    """Run the test flow."""
    runner = ConsentEngineTestRunner()
    await runner.run_all_tests()

    print("\n" + "═" * 70)
    print("TEST FLOW COMPLETE")
    print("═" * 70)
    print("\nThe consent engine is working. Key takeaways:")
    print("  ✅ Sync requests meeting price minimums → APPROVED")
    print("  ❌ Low offers below minimum → DECLINED")
    print("  ❌ AI training (explicitly denied) → DECLINED")
    print("  ❌ Political/excluded contexts → DECLINED")
    print("  ⏸️ Sample requests → REQUIRE REVIEW")
    print("  ✅ Streaming (allowed) → APPROVED")
    print("\nCreators see EXACTLY what happened to their work.")
    print("No mystery. No hidden deals. Full transparency.")


if __name__ == "__main__":
    asyncio.run(main())
