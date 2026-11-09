"""
NOIZYVOX Royalty Tracker
========================

Voice work earnings, payments, and distribution.

Every voice deserves fair compensation.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4


class PaymentStatus(Enum):
    """Status of a payment."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class PaymentMethod(Enum):
    """Payment methods."""
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    CHECK = "check"
    CRYPTO = "crypto"
    GUILD_CREDIT = "guild_credit"


class EarningsType(Enum):
    """Types of earnings."""
    SESSION_FEE = "session_fee"
    USAGE_FEE = "usage_fee"
    ROYALTY = "royalty"
    BUYOUT = "buyout"
    RESIDUAL = "residual"
    BONUS = "bonus"
    GUILD_DISTRIBUTION = "guild_distribution"


class PayoutSchedule(Enum):
    """Payout frequency."""
    IMMEDIATE = "immediate"
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ON_COMPLETION = "on_completion"


@dataclass
class Earnings:
    """An earnings record."""
    earnings_id: str = field(default_factory=lambda: str(uuid4()))

    # Source
    member_id: str = ""
    project_id: Optional[str] = None
    consent_id: Optional[str] = None

    # Amount
    gross_amount: Decimal = Decimal("0.00")
    guild_fee: Decimal = Decimal("0.00")  # Guild commission
    net_amount: Decimal = Decimal("0.00")

    # Type
    earnings_type: EarningsType = EarningsType.SESSION_FEE
    description: str = ""

    # Status
    paid: bool = False
    payment_id: Optional[str] = None

    # Dates
    earned_date: datetime = field(default_factory=datetime.utcnow)
    paid_date: Optional[datetime] = None

    # Currency
    currency: str = "USD"

    def __post_init__(self):
        """Calculate net amount."""
        if self.net_amount == Decimal("0.00"):
            self.net_amount = self.gross_amount - self.guild_fee


@dataclass
class Payment:
    """A payment record."""
    payment_id: str = field(default_factory=lambda: str(uuid4()))

    # Recipient
    member_id: str = ""
    member_name: str = ""

    # Amount
    amount: Decimal = Decimal("0.00")
    currency: str = "USD"

    # Method
    method: PaymentMethod = PaymentMethod.BANK_TRANSFER

    # Status
    status: PaymentStatus = PaymentStatus.PENDING

    # Earnings included
    earnings_ids: List[str] = field(default_factory=list)

    # Dates
    created_date: datetime = field(default_factory=datetime.utcnow)
    processed_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    # Reference
    transaction_id: Optional[str] = None
    reference_number: Optional[str] = None
    notes: str = ""

    def process(self):
        """Mark payment as processing."""
        self.status = PaymentStatus.PROCESSING
        self.processed_date = datetime.utcnow()

    def complete(self, transaction_id: str):
        """Mark payment as completed."""
        self.status = PaymentStatus.COMPLETED
        self.completed_date = datetime.utcnow()
        self.transaction_id = transaction_id

    def fail(self, reason: str):
        """Mark payment as failed."""
        self.status = PaymentStatus.FAILED
        self.notes += f"\nFailed: {reason}"


class RoyaltyTracker:
    """
    The Royalty Tracker.

    Manages all voice work earnings and payments.
    """

    def __init__(self):
        self.tracker_id = str(uuid4())
        self.earnings: Dict[str, Earnings] = {}
        self.payments: Dict[str, Payment] = {}
        self.created = datetime.utcnow()

        # Guild settings
        self.guild_fee_percentage = Decimal("0.10")  # 10% guild fee
        self.minimum_payout = Decimal("50.00")

    # ─────────────────────────────────────────────────────────────────────────
    # Earnings
    # ─────────────────────────────────────────────────────────────────────────

    def record_earnings(
        self,
        member_id: str,
        gross_amount: float,
        earnings_type: EarningsType,
        description: str = "",
        project_id: str = None,
        consent_id: str = None
    ) -> Earnings:
        """Record new earnings."""
        gross = Decimal(str(gross_amount))
        fee = gross * self.guild_fee_percentage
        net = gross - fee

        earnings = Earnings(
            member_id=member_id,
            project_id=project_id,
            consent_id=consent_id,
            gross_amount=gross,
            guild_fee=fee,
            net_amount=net,
            earnings_type=earnings_type,
            description=description
        )

        self.earnings[earnings.earnings_id] = earnings
        return earnings

    def get_member_earnings(self, member_id: str) -> List[Earnings]:
        """Get all earnings for a member."""
        return [e for e in self.earnings.values() if e.member_id == member_id]

    def get_unpaid_earnings(self, member_id: str) -> List[Earnings]:
        """Get unpaid earnings for a member."""
        return [
            e for e in self.earnings.values()
            if e.member_id == member_id and not e.paid
        ]

    def get_member_balance(self, member_id: str) -> Decimal:
        """Get unpaid balance for a member."""
        unpaid = self.get_unpaid_earnings(member_id)
        return sum(e.net_amount for e in unpaid)

    # ─────────────────────────────────────────────────────────────────────────
    # Payments
    # ─────────────────────────────────────────────────────────────────────────

    def create_payment(
        self,
        member_id: str,
        member_name: str,
        method: PaymentMethod = PaymentMethod.BANK_TRANSFER
    ) -> Optional[Payment]:
        """Create a payment for unpaid earnings."""
        unpaid = self.get_unpaid_earnings(member_id)

        if not unpaid:
            return None

        total = sum(e.net_amount for e in unpaid)

        if total < self.minimum_payout:
            return None

        payment = Payment(
            member_id=member_id,
            member_name=member_name,
            amount=total,
            method=method,
            earnings_ids=[e.earnings_id for e in unpaid]
        )

        self.payments[payment.payment_id] = payment
        return payment

    def process_payment(self, payment_id: str) -> bool:
        """Process a payment."""
        payment = self.payments.get(payment_id)
        if not payment or payment.status != PaymentStatus.PENDING:
            return False

        payment.process()
        return True

    def complete_payment(self, payment_id: str, transaction_id: str) -> bool:
        """Complete a payment."""
        payment = self.payments.get(payment_id)
        if not payment or payment.status != PaymentStatus.PROCESSING:
            return False

        payment.complete(transaction_id)

        # Mark earnings as paid
        for earnings_id in payment.earnings_ids:
            earnings = self.earnings.get(earnings_id)
            if earnings:
                earnings.paid = True
                earnings.paid_date = datetime.utcnow()
                earnings.payment_id = payment_id

        return True

    def get_member_payments(self, member_id: str) -> List[Payment]:
        """Get all payments for a member."""
        return [p for p in self.payments.values() if p.member_id == member_id]

    # ─────────────────────────────────────────────────────────────────────────
    # Reports
    # ─────────────────────────────────────────────────────────────────────────

    def get_member_summary(self, member_id: str) -> Dict[str, Any]:
        """Get earnings summary for a member."""
        all_earnings = self.get_member_earnings(member_id)
        unpaid = self.get_unpaid_earnings(member_id)
        payments = self.get_member_payments(member_id)

        return {
            "member_id": member_id,
            "total_gross": float(sum(e.gross_amount for e in all_earnings)),
            "total_guild_fees": float(sum(e.guild_fee for e in all_earnings)),
            "total_net": float(sum(e.net_amount for e in all_earnings)),
            "unpaid_balance": float(self.get_member_balance(member_id)),
            "total_payments": len([p for p in payments if p.status == PaymentStatus.COMPLETED]),
            "pending_payments": len([p for p in payments if p.status == PaymentStatus.PENDING]),
            "earnings_count": len(all_earnings),
            "unpaid_count": len(unpaid)
        }

    def get_guild_summary(self) -> Dict[str, Any]:
        """Get guild-wide earnings summary."""
        all_earnings = list(self.earnings.values())
        all_payments = list(self.payments.values())

        return {
            "total_gross_earnings": float(sum(e.gross_amount for e in all_earnings)),
            "total_guild_fees": float(sum(e.guild_fee for e in all_earnings)),
            "total_net_to_members": float(sum(e.net_amount for e in all_earnings)),
            "total_paid_out": float(sum(
                p.amount for p in all_payments
                if p.status == PaymentStatus.COMPLETED
            )),
            "pending_payouts": float(sum(
                p.amount for p in all_payments
                if p.status == PaymentStatus.PENDING
            )),
            "total_members_paid": len(set(
                p.member_id for p in all_payments
                if p.status == PaymentStatus.COMPLETED
            ))
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Royalty Tracker."""
    print("\n" + "=" * 70)
    print("NOIZYVOX ROYALTY TRACKER — DEMO")
    print("Every voice deserves fair compensation")
    print("=" * 70)

    tracker = RoyaltyTracker()

    # Record earnings
    print("\n" + "─" * 50)
    print("  RECORDING EARNINGS")
    print("─" * 50)

    e1 = tracker.record_earnings(
        member_id="member_123",
        gross_amount=500.00,
        earnings_type=EarningsType.SESSION_FEE,
        description="Audiobook Chapter 1-3",
        project_id="proj_001"
    )
    print(f"  ✓ Session: ${e1.gross_amount} gross → ${e1.net_amount} net")

    e2 = tracker.record_earnings(
        member_id="member_123",
        gross_amount=1500.00,
        earnings_type=EarningsType.USAGE_FEE,
        description="TV Commercial - 1 year broadcast",
        project_id="proj_002"
    )
    print(f"  ✓ Usage: ${e2.gross_amount} gross → ${e2.net_amount} net")

    e3 = tracker.record_earnings(
        member_id="member_123",
        gross_amount=250.00,
        earnings_type=EarningsType.ROYALTY,
        description="Q4 Royalties - Video Game",
        project_id="proj_003"
    )
    print(f"  ✓ Royalty: ${e3.gross_amount} gross → ${e3.net_amount} net")

    # Check balance
    print("\n" + "─" * 50)
    print("  MEMBER BALANCE")
    print("─" * 50)

    balance = tracker.get_member_balance("member_123")
    print(f"  Unpaid balance: ${balance}")

    # Create payment
    print("\n" + "─" * 50)
    print("  CREATING PAYMENT")
    print("─" * 50)

    payment = tracker.create_payment(
        member_id="member_123",
        member_name="Marcus Williams",
        method=PaymentMethod.BANK_TRANSFER
    )

    if payment:
        print(f"  Payment ID: {payment.payment_id[:8]}...")
        print(f"  Amount: ${payment.amount}")
        print(f"  Method: {payment.method.value}")
        print(f"  Earnings included: {len(payment.earnings_ids)}")

        # Process and complete
        tracker.process_payment(payment.payment_id)
        print(f"  Status: {payment.status.value}")

        tracker.complete_payment(payment.payment_id, "TXN_" + str(uuid4())[:8])
        print(f"  Status: {payment.status.value}")
        print(f"  Transaction: {payment.transaction_id}")

    # Member summary
    print("\n" + "─" * 50)
    print("  MEMBER SUMMARY")
    print("─" * 50)

    summary = tracker.get_member_summary("member_123")
    print(f"  Total gross: ${summary['total_gross']:.2f}")
    print(f"  Guild fees: ${summary['total_guild_fees']:.2f}")
    print(f"  Total net: ${summary['total_net']:.2f}")
    print(f"  Unpaid balance: ${summary['unpaid_balance']:.2f}")
    print(f"  Payments completed: {summary['total_payments']}")

    # Guild summary
    print("\n" + "─" * 50)
    print("  GUILD SUMMARY")
    print("─" * 50)

    guild = tracker.get_guild_summary()
    print(f"  Total gross: ${guild['total_gross_earnings']:.2f}")
    print(f"  Guild revenue: ${guild['total_guild_fees']:.2f}")
    print(f"  Paid to members: ${guild['total_paid_out']:.2f}")

    print("\n" + "=" * 70)
    print("Fair pay for fair work.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
