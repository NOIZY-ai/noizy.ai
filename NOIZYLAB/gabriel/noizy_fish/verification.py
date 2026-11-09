"""
NOIZY Fish — Creator Verification System
==========================================

Multi-level verification for creators:

Level 1: Email Verified
  - Email address confirmed

Level 2: Identity Verified
  - Government ID checked
  - Name matches display name

Level 3: PRO Verified
  - PRO membership confirmed (ASCAP, BMI, etc.)
  - IPI number validated

Level 4: Fully Verified
  - All above complete
  - Portfolio reviewed
  - Human verification badge

Verification increases trust and may affect auto-approval thresholds.
"""

import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import uuid4

from .identity.creator_passport import VerificationStatus
from .notifications import (
    NotificationService, Event, EventType,
    get_notification_service
)


class VerificationStep(Enum):
    """Individual verification steps."""
    EMAIL = "email"
    PHONE = "phone"
    IDENTITY = "identity"
    PRO_MEMBERSHIP = "pro_membership"
    IPI_VALIDATION = "ipi_validation"
    PORTFOLIO_REVIEW = "portfolio_review"
    HUMAN_REVIEW = "human_review"


@dataclass
class VerificationCode:
    """A verification code for email/phone."""
    code_id: str = field(default_factory=lambda: str(uuid4()))
    creator_id: str = ""
    step: VerificationStep = VerificationStep.EMAIL
    code: str = field(default_factory=lambda: secrets.token_hex(3).upper())  # 6 chars
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=24))
    used: bool = False
    used_at: Optional[datetime] = None

    def is_valid(self, submitted_code: str) -> bool:
        """Check if submitted code is valid."""
        if self.used:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        return secrets.compare_digest(self.code.upper(), submitted_code.upper())

    def mark_used(self):
        """Mark code as used."""
        self.used = True
        self.used_at = datetime.utcnow()


@dataclass
class VerificationRecord:
    """Record of a completed verification step."""
    record_id: str = field(default_factory=lambda: str(uuid4()))
    creator_id: str = ""
    step: VerificationStep = VerificationStep.EMAIL
    completed_at: datetime = field(default_factory=datetime.utcnow)
    verified_by: Optional[str] = None  # System or human reviewer ID
    evidence_hash: Optional[str] = None  # Hash of evidence (for audit)
    notes: Optional[str] = None
    expires_at: Optional[datetime] = None  # Some verifications expire


class VerificationService:
    """
    Handles creator verification workflow.
    """

    def __init__(self, db=None):
        self.db = db
        self.pending_codes: dict[str, VerificationCode] = {}
        self.completed_records: dict[str, list[VerificationRecord]] = {}
        self.notifications = get_notification_service()

    # ─────────────────────────────────────────────────────────────────────────
    # Email Verification
    # ─────────────────────────────────────────────────────────────────────────

    def start_email_verification(self, creator_id: str, email: str) -> VerificationCode:
        """
        Start email verification flow.
        Returns a code that should be sent to the email.
        """
        code = VerificationCode(
            creator_id=creator_id,
            step=VerificationStep.EMAIL
        )
        self.pending_codes[code.code_id] = code

        # In production: send email with code
        print(f"📧 Verification code for {email}: {code.code}")

        return code

    def verify_email(self, code_id: str, submitted_code: str) -> tuple[bool, str]:
        """
        Verify email with submitted code.
        Returns (success, message).
        """
        code = self.pending_codes.get(code_id)
        if not code:
            return False, "Verification code not found"

        if not code.is_valid(submitted_code):
            if code.used:
                return False, "Code already used"
            if datetime.utcnow() > code.expires_at:
                return False, "Code expired"
            return False, "Invalid code"

        # Mark code as used
        code.mark_used()

        # Create verification record
        record = VerificationRecord(
            creator_id=code.creator_id,
            step=VerificationStep.EMAIL,
            verified_by="system"
        )
        self._add_record(code.creator_id, record)

        # Update creator status
        self._update_creator_status(code.creator_id)

        return True, "Email verified successfully"

    # ─────────────────────────────────────────────────────────────────────────
    # PRO Membership Verification
    # ─────────────────────────────────────────────────────────────────────────

    def verify_pro_membership(
        self,
        creator_id: str,
        pro_name: str,
        member_id: str,
        ipi_number: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Verify PRO membership.
        In production: would call PRO APIs (ASCAP, BMI, SESAC).
        """
        # Simulated verification
        # In production: API calls to verify membership

        supported_pros = ["ASCAP", "BMI", "SESAC", "SOCAN", "PRS", "SACEM", "GEMA"]
        if pro_name.upper() not in supported_pros:
            return False, f"Unsupported PRO: {pro_name}"

        if not member_id or len(member_id) < 4:
            return False, "Invalid member ID"

        # Record PRO verification
        record = VerificationRecord(
            creator_id=creator_id,
            step=VerificationStep.PRO_MEMBERSHIP,
            verified_by="system",
            evidence_hash=hashlib.sha256(f"{pro_name}:{member_id}".encode()).hexdigest()[:16],
            notes=f"PRO: {pro_name}, Member ID: {member_id[:4]}***"
        )
        self._add_record(creator_id, record)

        # Verify IPI if provided
        if ipi_number:
            ipi_record = VerificationRecord(
                creator_id=creator_id,
                step=VerificationStep.IPI_VALIDATION,
                verified_by="system",
                evidence_hash=hashlib.sha256(ipi_number.encode()).hexdigest()[:16]
            )
            self._add_record(creator_id, ipi_record)

        # Update status
        self._update_creator_status(creator_id)

        return True, "PRO membership verified"

    # ─────────────────────────────────────────────────────────────────────────
    # Identity Verification
    # ─────────────────────────────────────────────────────────────────────────

    def start_identity_verification(self, creator_id: str) -> str:
        """
        Start identity verification.
        Returns a verification session ID for external ID service.
        In production: would integrate with Stripe Identity, Veriff, etc.
        """
        session_id = str(uuid4())

        # Store pending verification
        code = VerificationCode(
            code_id=session_id,
            creator_id=creator_id,
            step=VerificationStep.IDENTITY
        )
        code.expires_at = datetime.utcnow() + timedelta(hours=1)
        self.pending_codes[session_id] = code

        # In production: redirect to ID verification service
        print(f"🆔 Identity verification session: {session_id}")

        return session_id

    def complete_identity_verification(
        self,
        session_id: str,
        verified: bool,
        name_match: bool = True
    ) -> tuple[bool, str]:
        """
        Complete identity verification (callback from ID service).
        """
        code = self.pending_codes.get(session_id)
        if not code:
            return False, "Session not found"

        if code.used:
            return False, "Session already completed"

        if not verified:
            return False, "Identity verification failed"

        if not name_match:
            return False, "Name does not match registered name"

        # Mark complete
        code.mark_used()

        # Record verification
        record = VerificationRecord(
            creator_id=code.creator_id,
            step=VerificationStep.IDENTITY,
            verified_by="identity_service",
            evidence_hash=hashlib.sha256(session_id.encode()).hexdigest()[:16],
            expires_at=datetime.utcnow() + timedelta(days=365)  # Valid for 1 year
        )
        self._add_record(code.creator_id, record)

        # Update status
        self._update_creator_status(code.creator_id)

        return True, "Identity verified"

    # ─────────────────────────────────────────────────────────────────────────
    # Human Review
    # ─────────────────────────────────────────────────────────────────────────

    def submit_for_human_review(
        self,
        creator_id: str,
        portfolio_urls: list[str],
        notes: Optional[str] = None
    ) -> str:
        """
        Submit creator for human review.
        Returns a review ticket ID.
        """
        ticket_id = str(uuid4())

        # Store pending review
        code = VerificationCode(
            code_id=ticket_id,
            creator_id=creator_id,
            step=VerificationStep.HUMAN_REVIEW
        )
        code.expires_at = datetime.utcnow() + timedelta(days=30)
        self.pending_codes[ticket_id] = code

        # In production: create review ticket
        print(f"👤 Human review ticket: {ticket_id}")
        print(f"   Portfolio: {portfolio_urls}")

        return ticket_id

    def complete_human_review(
        self,
        ticket_id: str,
        reviewer_id: str,
        approved: bool,
        notes: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Complete human review.
        """
        code = self.pending_codes.get(ticket_id)
        if not code:
            return False, "Review ticket not found"

        if code.used:
            return False, "Review already completed"

        code.mark_used()

        if approved:
            # Record both portfolio and human review
            portfolio_record = VerificationRecord(
                creator_id=code.creator_id,
                step=VerificationStep.PORTFOLIO_REVIEW,
                verified_by=reviewer_id,
                notes=notes
            )
            self._add_record(code.creator_id, portfolio_record)

            human_record = VerificationRecord(
                creator_id=code.creator_id,
                step=VerificationStep.HUMAN_REVIEW,
                verified_by=reviewer_id,
                notes=notes
            )
            self._add_record(code.creator_id, human_record)

            # Update status
            self._update_creator_status(code.creator_id)

            return True, "Human review approved"
        else:
            return False, f"Human review denied: {notes}"

    # ─────────────────────────────────────────────────────────────────────────
    # Status Management
    # ─────────────────────────────────────────────────────────────────────────

    def _add_record(self, creator_id: str, record: VerificationRecord):
        """Add a verification record."""
        if creator_id not in self.completed_records:
            self.completed_records[creator_id] = []
        self.completed_records[creator_id].append(record)

    def get_verification_status(self, creator_id: str) -> dict:
        """Get current verification status for a creator."""
        records = self.completed_records.get(creator_id, [])

        completed_steps = {r.step.value for r in records}

        # Calculate level
        level = VerificationStatus.UNVERIFIED

        if VerificationStep.EMAIL.value in completed_steps:
            level = VerificationStatus.EMAIL_VERIFIED

        if VerificationStep.IDENTITY.value in completed_steps:
            level = VerificationStatus.IDENTITY_VERIFIED

        if VerificationStep.PRO_MEMBERSHIP.value in completed_steps:
            level = VerificationStatus.PRO_VERIFIED

        if (VerificationStep.HUMAN_REVIEW.value in completed_steps and
            VerificationStep.PORTFOLIO_REVIEW.value in completed_steps):
            level = VerificationStatus.FULLY_VERIFIED

        return {
            "creator_id": creator_id,
            "level": level.value,
            "completed_steps": list(completed_steps),
            "records": [
                {
                    "step": r.step.value,
                    "completed_at": r.completed_at.isoformat(),
                    "verified_by": r.verified_by
                }
                for r in records
            ]
        }

    def _update_creator_status(self, creator_id: str):
        """Update creator's verification status in database."""
        status = self.get_verification_status(creator_id)

        if self.db:
            # Update in database
            with self.db._get_conn() as conn:
                conn.execute(
                    "UPDATE creators SET verification_status = ? WHERE creator_id = ?",
                    (status["level"], creator_id)
                )

        # Emit notification
        event = Event(
            event_type=EventType.CREATOR_VERIFIED,
            creator_id=creator_id,
            data=status
        )
        self.notifications.emit_sync(event)


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate verification flow."""
    print("\n" + "=" * 70)
    print("NOIZY FISH VERIFICATION — DEMO")
    print("=" * 70)

    service = VerificationService()
    creator_id = "test-creator-123"

    # Email verification
    print("\n" + "─" * 50)
    print("STEP 1: EMAIL VERIFICATION")
    print("─" * 50)

    code = service.start_email_verification(creator_id, "creator@example.com")
    print(f"  Code sent: {code.code}")

    success, message = service.verify_email(code.code_id, code.code)
    print(f"  Result: {'✓' if success else '✗'} {message}")

    # PRO verification
    print("\n" + "─" * 50)
    print("STEP 2: PRO MEMBERSHIP VERIFICATION")
    print("─" * 50)

    success, message = service.verify_pro_membership(
        creator_id,
        pro_name="ASCAP",
        member_id="ABC123456",
        ipi_number="00123456789"
    )
    print(f"  Result: {'✓' if success else '✗'} {message}")

    # Identity verification
    print("\n" + "─" * 50)
    print("STEP 3: IDENTITY VERIFICATION")
    print("─" * 50)

    session_id = service.start_identity_verification(creator_id)
    print(f"  Session: {session_id}")

    success, message = service.complete_identity_verification(
        session_id, verified=True, name_match=True
    )
    print(f"  Result: {'✓' if success else '✗'} {message}")

    # Human review
    print("\n" + "─" * 50)
    print("STEP 4: HUMAN REVIEW")
    print("─" * 50)

    ticket_id = service.submit_for_human_review(
        creator_id,
        portfolio_urls=["https://spotify.com/artist/xyz", "https://soundcloud.com/creator"],
        notes="Established artist with verified discography"
    )
    print(f"  Ticket: {ticket_id}")

    success, message = service.complete_human_review(
        ticket_id,
        reviewer_id="reviewer-001",
        approved=True,
        notes="Verified professional artist"
    )
    print(f"  Result: {'✓' if success else '✗'} {message}")

    # Final status
    print("\n" + "─" * 50)
    print("FINAL STATUS")
    print("─" * 50)

    status = service.get_verification_status(creator_id)
    print(f"  Level: {status['level']}")
    print(f"  Completed Steps: {status['completed_steps']}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
