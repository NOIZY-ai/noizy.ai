"""
Creator Receipt Generator
=========================
Generates human-readable receipts that tell creators
exactly what happened with their work.

No mystery. No hidden deals. Full transparency.
"""

from datetime import datetime

from ..schema import (
    LicensingInquiry,
    LicensingDecision,
    ConsentRegistry,
    CreatorReceipt,
    ConsentStatus,
)


class ReceiptGenerator:
    """
    Generates receipts for creators after licensing decisions.

    Every receipt answers:
    - WHO asked?
    - WHAT did they want?
    - WHAT did we decide?
    - WHY? (which consent rules applied)
    """

    def generate(
        self,
        inquiry: LicensingInquiry,
        registry: ConsentRegistry,
        decision: LicensingDecision
    ) -> CreatorReceipt:
        """Generate a complete receipt for the creator."""

        # Build inquiry summary (plain English)
        inquiry_summary = self._build_inquiry_summary(inquiry)

        # Build decision summary (plain English)
        decision_summary = self._build_decision_summary(decision)

        return CreatorReceipt(
            creator_name=registry.creator_name,
            creator_email=registry.creator_email,
            work_title=registry.work_title,
            inquiry_summary=inquiry_summary,
            decision_summary=decision_summary,
            requestor_name=inquiry.requestor_name,
            requestor_company=inquiry.requestor_company,
            use_type=inquiry.use_type.value,
            use_description=inquiry.use_description,
            approved=decision.approved,
            fee_if_approved=decision.fee if decision.approved else None,
            terms_if_approved=decision.royalty_terms if decision.approved else None,
            decline_reason_if_declined=decision.decline_reason if not decision.approved else None,
            consent_rules_applied=decision.consent_rules_applied,
            full_inquiry_text=inquiry.raw_message,
            inquiry_received=inquiry.received_at,
            decision_made=decision.decided_at,
            receipt_sent=datetime.utcnow(),
        )

    def _build_inquiry_summary(self, inquiry: LicensingInquiry) -> str:
        """Build plain English summary of what was requested."""
        company_part = f" from {inquiry.requestor_company}" if inquiry.requestor_company else ""

        summary = f"{inquiry.requestor_name}{company_part} wants to use your work "
        summary += f"\"{inquiry.work_title}\" for {inquiry.use_type.value}."

        if inquiry.project_name:
            summary += f" This is for their project \"{inquiry.project_name}\"."

        if inquiry.use_description:
            summary += f" Specifically: {inquiry.use_description[:200]}"

        if inquiry.offered_fee:
            summary += f" They offered ${inquiry.offered_fee:,.2f}."

        return summary

    def _build_decision_summary(self, decision: LicensingDecision) -> str:
        """Build plain English summary of the decision."""
        if decision.status == ConsentStatus.ALLOWED and decision.approved:
            summary = f"APPROVED. "
            if decision.fee:
                summary += f"License granted for ${decision.fee:,.2f}. "
            if decision.royalty_terms:
                summary += f"Terms: {decision.royalty_terms}. "
            summary += "This matches your consent settings."
            return summary

        if decision.status == ConsentStatus.DENIED:
            summary = f"DECLINED. "
            summary += f"Reason: {decision.decline_reason}. "
            summary += "Your consent settings protected you from this request."
            return summary

        if decision.status == ConsentStatus.REQUIRES_APPROVAL:
            summary = f"PENDING YOUR REVIEW. "
            summary += f"Reason: {decision.review_reason}. "
            summary += "Please reply to approve or decline this request."
            return summary

        return "Decision pending."


class ReceiptFormatter:
    """Format receipts for different output channels."""

    @staticmethod
    def to_email(receipt: CreatorReceipt) -> tuple[str, str]:
        """Format receipt as email subject and body."""
        status = "APPROVED" if receipt.approved else "DECLINED"
        subject = f"[NOIZY] Licensing: {receipt.work_title} — {status}"
        body = receipt.to_email_body()
        return subject, body

    @staticmethod
    def to_slack(receipt: CreatorReceipt) -> dict:
        """Format receipt as Slack message."""
        status_emoji = "✅" if receipt.approved else "❌"
        status_text = "Approved" if receipt.approved else "Declined"

        return {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"{status_emoji} Licensing Inquiry: {receipt.work_title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Requestor:*\n{receipt.requestor_name}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Company:*\n{receipt.requestor_company or 'N/A'}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Use Type:*\n{receipt.use_type}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Decision:*\n{status_text}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Summary:*\n{receipt.decision_summary}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Providence: `{receipt.providence_hash or 'pending'}`"
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def to_json(receipt: CreatorReceipt) -> dict:
        """Format receipt as JSON for API responses."""
        from dataclasses import asdict
        return asdict(receipt)

    @staticmethod
    def to_markdown(receipt: CreatorReceipt) -> str:
        """Format receipt as Markdown."""
        status = "✅ APPROVED" if receipt.approved else "❌ DECLINED"

        md = f"""# Licensing Receipt: {receipt.work_title}

**Status:** {status}
**Date:** {receipt.decision_made.strftime("%Y-%m-%d %H:%M UTC")}

---

## Request Details

| Field | Value |
|-------|-------|
| Requestor | {receipt.requestor_name} |
| Company | {receipt.requestor_company or 'N/A'} |
| Use Type | {receipt.use_type} |

### Description
{receipt.use_description}

---

## Decision

{receipt.decision_summary}

"""

        if receipt.approved and receipt.fee_if_approved:
            md += f"""### Terms
- **Fee:** ${receipt.fee_if_approved:,.2f}
- **Terms:** {receipt.terms_if_approved}

"""
        elif not receipt.approved:
            md += f"""### Decline Reason
{receipt.decline_reason_if_declined}

"""

        md += """### Consent Rules Applied
"""
        for rule in receipt.consent_rules_applied:
            md += f"- {rule}\n"

        md += f"""
---

**Providence Record:** `{receipt.providence_hash or 'pending'}`
"""
        return md
