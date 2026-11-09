"""
NOIZY Fish — Layer 3: Tracking & Royalties
==========================================

This layer handles:
1. License execution and tracking
2. Royalty calculation
3. Payment routing
4. Transaction logging
5. Real-time royalty flow

When a license is approved, this layer:
- Executes the license terms
- Calculates royalties based on splits
- Routes payments to creators
- Logs everything to the audit trail

This is "smart contract logic" — automated, transparent, immutable.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import uuid4
import hashlib
import json


class LicenseStatus(Enum):
    """Status of a license."""
    PENDING = "pending"              # Awaiting payment/signature
    ACTIVE = "active"                # Currently in effect
    EXPIRED = "expired"              # Past end date
    TERMINATED = "terminated"        # Ended early
    SUSPENDED = "suspended"          # Temporarily halted
    VIOLATED = "violated"            # Terms violated


class PaymentStatus(Enum):
    """Status of a payment."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class UsageEventType(Enum):
    """Types of usage events that trigger royalties."""
    STREAM = "stream"
    DOWNLOAD = "download"
    BROADCAST = "broadcast"
    SYNC_USE = "sync_use"
    PERFORMANCE = "performance"
    SAMPLE_USE = "sample_use"
    MERCHANDISE_SALE = "merchandise_sale"


@dataclass
class RoyaltySplit:
    """
    A single recipient in a royalty split.
    Defines who gets paid and how much.
    """
    recipient_id: str                    # Creator passport ID
    recipient_name: str
    recipient_email: str
    percentage: float                    # Their share (0-100)
    role: str                            # songwriter, producer, etc.

    # Payment routing
    payment_method: Optional[str] = None # stripe, paypal, wire, crypto
    payment_account_hash: Optional[str] = None  # Encrypted account info

    # Minimum payout threshold
    minimum_payout: float = 10.00
    currency: str = "USD"

    # Accumulated balance (not yet paid out)
    pending_balance: float = 0.0

    def calculate_share(self, total: float) -> float:
        """Calculate this recipient's share of a total."""
        return total * (self.percentage / 100)


@dataclass
class License:
    """
    An executed license agreement.
    This is the contract between creator and licensee.
    """
    license_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    licensor_id: str = ""                # Creator passport ID
    licensee_name: str = ""
    licensee_email: str = ""
    licensee_company: Optional[str] = None

    # Work
    work_id: str = ""
    work_title: str = ""
    isrc: Optional[str] = None
    iswc: Optional[str] = None

    # Terms
    use_type: str = ""                   # streaming, sync, sample, etc.
    use_description: str = ""
    territory: str = "WW"                # ISO territory code
    exclusive: bool = False

    # Duration
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    perpetual: bool = False

    # Compensation
    fee_type: str = "flat_fee"           # flat_fee, percentage, per_use
    fee_amount: float = 0.0
    percentage_rate: Optional[float] = None
    per_use_rate: Optional[float] = None
    advance_amount: Optional[float] = None
    currency: str = "USD"

    # Splits
    royalty_splits: list[RoyaltySplit] = field(default_factory=list)

    # Credit requirements
    credit_required: bool = True
    credit_format: Optional[str] = None

    # Status
    status: LicenseStatus = LicenseStatus.PENDING

    # Tracking
    total_uses: int = 0
    total_royalties_paid: float = 0.0

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    activated_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None

    # Providence
    consent_rule_id: Optional[str] = None
    approval_hash: Optional[str] = None

    def is_active(self) -> bool:
        """Check if license is currently active."""
        if self.status != LicenseStatus.ACTIVE:
            return False
        if self.perpetual:
            return True
        if self.end_date and datetime.utcnow() > self.end_date:
            return False
        return True

    def calculate_royalty(self, usage_count: int = 1) -> float:
        """Calculate royalty for usage."""
        if self.fee_type == "flat_fee":
            # Flat fee already paid
            return 0.0
        elif self.fee_type == "per_use":
            return (self.per_use_rate or 0) * usage_count
        elif self.fee_type == "percentage":
            # Would need revenue info
            return 0.0
        return 0.0

    def to_dict(self) -> dict:
        """Export license as dictionary."""
        return {
            "license_id": self.license_id,
            "work": {
                "id": self.work_id,
                "title": self.work_title,
                "isrc": self.isrc
            },
            "licensee": {
                "name": self.licensee_name,
                "company": self.licensee_company
            },
            "terms": {
                "use_type": self.use_type,
                "territory": self.territory,
                "exclusive": self.exclusive,
                "perpetual": self.perpetual,
                "fee_type": self.fee_type,
                "fee_amount": self.fee_amount
            },
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class UsageEvent:
    """
    A single usage event that may trigger royalties.
    E.g., a stream, download, broadcast, etc.
    """
    event_id: str = field(default_factory=lambda: str(uuid4()))

    # What was used
    license_id: str = ""
    work_id: str = ""
    isrc: Optional[str] = None

    # Event details
    event_type: UsageEventType = UsageEventType.STREAM
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Source
    platform: Optional[str] = None       # Spotify, YouTube, etc.
    territory: str = "US"
    device_type: Optional[str] = None

    # Metrics
    duration_seconds: Optional[int] = None  # For streams
    revenue: Optional[float] = None         # If revenue-based

    # Royalty calculated
    royalty_amount: float = 0.0
    royalty_currency: str = "USD"

    # Status
    processed: bool = False
    processed_at: Optional[datetime] = None


@dataclass
class Payment:
    """
    A royalty payment to a creator.
    """
    payment_id: str = field(default_factory=lambda: str(uuid4()))

    # Recipient
    recipient_id: str = ""
    recipient_name: str = ""

    # Amount
    amount: float = 0.0
    currency: str = "USD"

    # Source
    license_ids: list[str] = field(default_factory=list)
    event_count: int = 0
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

    # Payment details
    payment_method: str = ""
    transaction_id: Optional[str] = None

    # Status
    status: PaymentStatus = PaymentStatus.PENDING
    initiated_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Providence
    providence_hash: Optional[str] = None


@dataclass
class RoyaltyStatement:
    """
    A royalty statement for a creator.
    Shows earnings for a period.
    """
    statement_id: str = field(default_factory=lambda: str(uuid4()))

    # Creator
    creator_id: str = ""
    creator_name: str = ""

    # Period
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=datetime.utcnow)

    # Earnings breakdown
    earnings_by_work: dict[str, float] = field(default_factory=dict)
    earnings_by_type: dict[str, float] = field(default_factory=dict)
    earnings_by_territory: dict[str, float] = field(default_factory=dict)

    # Totals
    gross_earnings: float = 0.0
    fees: float = 0.0
    net_earnings: float = 0.0

    # Payments
    payments_made: list[str] = field(default_factory=list)  # Payment IDs
    pending_balance: float = 0.0

    # Metadata
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_markdown(self) -> str:
        """Generate markdown statement."""
        md = f"""# Royalty Statement

**Creator:** {self.creator_name}
**Period:** {self.period_start.strftime('%Y-%m-%d')} to {self.period_end.strftime('%Y-%m-%d')}
**Generated:** {self.generated_at.strftime('%Y-%m-%d %H:%M UTC')}

---

## Summary

| Metric | Amount |
|--------|--------|
| Gross Earnings | ${self.gross_earnings:,.2f} |
| Fees | ${self.fees:,.2f} |
| **Net Earnings** | **${self.net_earnings:,.2f}** |
| Pending Balance | ${self.pending_balance:,.2f} |

## Earnings by Work

| Work | Earnings |
|------|----------|
"""
        for work, amount in self.earnings_by_work.items():
            md += f"| {work} | ${amount:,.2f} |\n"

        md += """
## Earnings by Use Type

| Type | Earnings |
|------|----------|
"""
        for use_type, amount in self.earnings_by_type.items():
            md += f"| {use_type} | ${amount:,.2f} |\n"

        return md


class RoyaltyEngine:
    """
    The royalty calculation and distribution engine.
    Processes usage events and distributes royalties.
    """

    def __init__(self):
        self.licenses: dict[str, License] = {}
        self.events: list[UsageEvent] = []
        self.payments: list[Payment] = []

    def register_license(self, license: License):
        """Register a new license."""
        self.licenses[license.license_id] = license

    def record_usage(self, event: UsageEvent) -> Optional[float]:
        """
        Record a usage event and calculate royalty.
        Returns the royalty amount if applicable.
        """
        license = self.licenses.get(event.license_id)
        if not license:
            return None

        if not license.is_active():
            return None

        # Calculate royalty
        royalty = license.calculate_royalty()
        event.royalty_amount = royalty

        # Update license tracking
        license.total_uses += 1
        license.total_royalties_paid += royalty

        # Distribute to splits
        self._distribute_royalty(license, royalty)

        # Record event
        event.processed = True
        event.processed_at = datetime.utcnow()
        self.events.append(event)

        return royalty

    def _distribute_royalty(self, license: License, amount: float):
        """Distribute royalty among split recipients."""
        for split in license.royalty_splits:
            share = split.calculate_share(amount)
            split.pending_balance += share

    def process_payouts(self, min_payout: float = 10.0) -> list[Payment]:
        """
        Process pending payouts for all recipients.
        Returns list of payments initiated.
        """
        payments = []

        # Collect all splits with pending balance
        for license in self.licenses.values():
            for split in license.royalty_splits:
                if split.pending_balance >= min_payout:
                    payment = Payment(
                        recipient_id=split.recipient_id,
                        recipient_name=split.recipient_name,
                        amount=split.pending_balance,
                        currency=split.currency,
                        license_ids=[license.license_id],
                        payment_method=split.payment_method or "pending"
                    )
                    payments.append(payment)
                    split.pending_balance = 0.0

        self.payments.extend(payments)
        return payments

    def generate_statement(
        self,
        creator_id: str,
        creator_name: str,
        start: datetime,
        end: datetime
    ) -> RoyaltyStatement:
        """Generate a royalty statement for a creator."""
        statement = RoyaltyStatement(
            creator_id=creator_id,
            creator_name=creator_name,
            period_start=start,
            period_end=end
        )

        # Calculate earnings from events in period
        for event in self.events:
            if start <= event.timestamp <= end:
                license = self.licenses.get(event.license_id)
                if license:
                    # Check if creator is in splits
                    for split in license.royalty_splits:
                        if split.recipient_id == creator_id:
                            share = split.calculate_share(event.royalty_amount)

                            # By work
                            work = license.work_title
                            statement.earnings_by_work[work] = (
                                statement.earnings_by_work.get(work, 0) + share
                            )

                            # By type
                            use = event.event_type.value
                            statement.earnings_by_type[use] = (
                                statement.earnings_by_type.get(use, 0) + share
                            )

                            # By territory
                            territory = event.territory
                            statement.earnings_by_territory[territory] = (
                                statement.earnings_by_territory.get(territory, 0) + share
                            )

                            statement.gross_earnings += share

        # Calculate net (assuming 10% platform fee for now)
        statement.fees = statement.gross_earnings * 0.10
        statement.net_earnings = statement.gross_earnings - statement.fees

        return statement


# ═══════════════════════════════════════════════════════════════════════════
# Transaction Log — Immutable audit trail
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TransactionLogEntry:
    """A single entry in the immutable transaction log."""
    entry_id: str = field(default_factory=lambda: str(uuid4()))

    # Transaction type
    transaction_type: str = ""           # license_created, usage_recorded, payment_made
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Details
    details: dict = field(default_factory=dict)

    # Chain
    previous_hash: str = ""
    entry_hash: str = ""

    def calculate_hash(self) -> str:
        """Calculate hash of this entry."""
        data = {
            "entry_id": self.entry_id,
            "transaction_type": self.transaction_type,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
            "previous_hash": self.previous_hash
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


class TransactionLog:
    """
    Immutable transaction log for all royalty operations.
    Every license, usage, and payment is logged here.
    """

    def __init__(self):
        self.entries: list[TransactionLogEntry] = []
        self._init_genesis()

    def _init_genesis(self):
        """Create genesis entry."""
        genesis = TransactionLogEntry(
            transaction_type="genesis",
            details={"message": "NOIZY Fish Transaction Log initialized"},
            previous_hash="0"
        )
        genesis.entry_hash = genesis.calculate_hash()
        self.entries.append(genesis)

    def log(self, transaction_type: str, details: dict) -> str:
        """
        Log a transaction.
        Returns the entry hash.
        """
        previous_hash = self.entries[-1].entry_hash if self.entries else "0"

        entry = TransactionLogEntry(
            transaction_type=transaction_type,
            details=details,
            previous_hash=previous_hash
        )
        entry.entry_hash = entry.calculate_hash()

        self.entries.append(entry)
        return entry.entry_hash

    def verify(self) -> tuple[bool, list[str]]:
        """Verify integrity of the log."""
        issues = []

        for i, entry in enumerate(self.entries):
            # Verify hash
            expected_hash = entry.calculate_hash()
            if entry.entry_hash != expected_hash:
                issues.append(f"Entry {i}: Hash mismatch")

            # Verify chain
            if i > 0:
                if entry.previous_hash != self.entries[i-1].entry_hash:
                    issues.append(f"Entry {i}: Chain broken")

        return len(issues) == 0, issues

    def get_entries_for_work(self, work_id: str) -> list[TransactionLogEntry]:
        """Get all entries related to a work."""
        return [
            e for e in self.entries
            if e.details.get("work_id") == work_id
        ]
