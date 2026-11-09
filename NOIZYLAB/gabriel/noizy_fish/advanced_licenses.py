"""
NOIZY Fish — Advanced License Mechanisms
=========================================

Time-locked, fractional, and smart licenses.
The future of music rights management.

Features:
- Time-locked licenses (auto-expire, auto-renew)
- Fractional ownership (micro-shares of works)
- Usage-based pricing (pay per stream/use)
- Territory unlocks (progressive access)
- License derivatives (options, futures)
- Revenue splits (automatic distribution)

2056 VALUE: Programmable rights. Automatic enforcement. Perfect transparency.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable
from uuid import uuid4
import hashlib
import json
from decimal import Decimal


# ═══════════════════════════════════════════════════════════════════════════════
# License Types
# ═══════════════════════════════════════════════════════════════════════════════

class LicenseType(Enum):
    """Types of advanced licenses."""
    TIME_LOCKED = "time_locked"           # Expires at specific time
    USAGE_BASED = "usage_based"           # Pay per use
    SUBSCRIPTION = "subscription"          # Recurring access
    FRACTIONAL = "fractional"             # Partial ownership
    TERRITORY_UNLOCK = "territory_unlock"  # Progressive territories
    OPTION = "option"                      # Right to buy license
    PERPETUAL = "perpetual"               # Forever, no renewal


class LicenseState(Enum):
    """License lifecycle states."""
    DRAFT = "draft"             # Not yet active
    PENDING = "pending"         # Awaiting payment/approval
    ACTIVE = "active"           # Currently valid
    SUSPENDED = "suspended"     # Temporarily inactive
    EXPIRED = "expired"         # Time ran out
    EXHAUSTED = "exhausted"     # Usage limit reached
    REVOKED = "revoked"         # Terminated early
    COMPLETED = "completed"     # Fulfilled all terms


class RenewalPolicy(Enum):
    """How license renews."""
    NONE = "none"               # No renewal
    MANUAL = "manual"           # Licensee requests
    AUTO_RENEW = "auto_renew"   # Automatic if payment available
    NEGOTIATE = "negotiate"     # Must renegotiate terms


# ═══════════════════════════════════════════════════════════════════════════════
# Time-Locked License
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TimeLockedLicense:
    """
    License with time-based constraints.

    Automatically expires, can auto-renew.
    """
    license_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    licensor_id: str = ""           # Rights holder
    licensee_id: str = ""           # User
    work_id: str = ""

    # Use rights
    use_category: str = ""
    territories: list[str] = field(default_factory=list)

    # Time constraints
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_days: int = 365

    # Renewal
    renewal_policy: RenewalPolicy = RenewalPolicy.MANUAL
    renewal_price: Optional[float] = None
    max_renewals: int = -1          # -1 = unlimited
    renewal_count: int = 0
    grace_period_days: int = 14     # Days after expiry to renew

    # State
    state: LicenseState = LicenseState.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.end_time and self.duration_days:
            self.end_time = self.start_time + timedelta(days=self.duration_days)

    def is_active(self) -> bool:
        """Check if license is currently active."""
        if self.state != LicenseState.ACTIVE:
            return False
        now = datetime.utcnow()
        return self.start_time <= now <= self.end_time

    def time_remaining(self) -> timedelta:
        """Get time remaining on license."""
        if not self.end_time:
            return timedelta.max
        return max(self.end_time - datetime.utcnow(), timedelta(0))

    def can_renew(self) -> bool:
        """Check if license can be renewed."""
        if self.renewal_policy == RenewalPolicy.NONE:
            return False
        if self.max_renewals >= 0 and self.renewal_count >= self.max_renewals:
            return False
        # Check grace period
        now = datetime.utcnow()
        grace_end = self.end_time + timedelta(days=self.grace_period_days)
        return now <= grace_end

    def renew(self) -> bool:
        """Renew the license."""
        if not self.can_renew():
            return False

        self.start_time = datetime.utcnow()
        self.end_time = self.start_time + timedelta(days=self.duration_days)
        self.renewal_count += 1
        self.state = LicenseState.ACTIVE
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# Usage-Based License
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class UsageBasedLicense:
    """
    License with usage-based pricing.

    Pay per stream, download, or use.
    """
    license_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    licensor_id: str = ""
    licensee_id: str = ""
    work_id: str = ""

    # Use rights
    use_category: str = ""
    unit_type: str = ""             # "stream", "download", "broadcast", etc.

    # Pricing
    price_per_unit: Decimal = Decimal("0.001")
    minimum_units: int = 0          # Minimum commitment
    maximum_units: int = -1         # -1 = unlimited
    volume_discounts: dict = field(default_factory=dict)
    # e.g., {"1000": 0.9, "10000": 0.8} = 10% off at 1k, 20% off at 10k

    # Usage tracking
    units_used: int = 0
    units_prepaid: int = 0
    balance: Decimal = Decimal("0")  # Prepaid balance

    # State
    state: LicenseState = LicenseState.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)

    def get_current_rate(self) -> Decimal:
        """Get current rate with volume discounts."""
        rate = self.price_per_unit

        for threshold, discount in sorted(
            self.volume_discounts.items(),
            key=lambda x: int(x[0]),
            reverse=True
        ):
            if self.units_used >= int(threshold):
                rate = self.price_per_unit * Decimal(str(discount))
                break

        return rate

    def record_usage(self, units: int) -> dict:
        """Record usage and calculate charges."""
        if self.state != LicenseState.ACTIVE:
            return {"error": "License not active"}

        if self.maximum_units >= 0 and self.units_used + units > self.maximum_units:
            return {"error": "Would exceed maximum units"}

        rate = self.get_current_rate()
        cost = rate * units

        self.units_used += units

        # Check if exhausted
        if self.maximum_units >= 0 and self.units_used >= self.maximum_units:
            self.state = LicenseState.EXHAUSTED

        return {
            "units_recorded": units,
            "rate_applied": float(rate),
            "cost": float(cost),
            "total_units": self.units_used,
            "remaining_units": self.maximum_units - self.units_used if self.maximum_units >= 0 else "unlimited"
        }

    def add_prepayment(self, amount: Decimal, units: int = 0) -> dict:
        """Add prepayment to balance."""
        self.balance += amount
        if units > 0:
            self.units_prepaid += units
        return {
            "balance": float(self.balance),
            "prepaid_units": self.units_prepaid
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Fractional Ownership
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FractionalShare:
    """A fractional share of work ownership."""
    share_id: str = field(default_factory=lambda: str(uuid4()))

    # Ownership
    work_id: str = ""
    owner_id: str = ""
    share_percentage: Decimal = Decimal("0")  # 0-100

    # Rights
    can_license: bool = False           # Can grant licenses?
    can_transfer: bool = True           # Can sell/transfer share?
    can_vote: bool = True               # Can vote on decisions?
    voting_weight: Decimal = field(default_factory=lambda: Decimal("0"))

    # Revenue
    revenue_share: Decimal = field(default_factory=lambda: Decimal("0"))  # % of revenue
    accumulated_revenue: Decimal = Decimal("0")
    last_distribution: Optional[datetime] = None

    # Metadata
    acquired_at: datetime = field(default_factory=datetime.utcnow)
    acquisition_price: Optional[Decimal] = None
    acquisition_method: str = "purchase"  # "purchase", "creation", "gift", "inheritance"

    def __post_init__(self):
        # Default voting weight = share percentage
        if self.voting_weight == 0:
            self.voting_weight = self.share_percentage
        # Default revenue share = share percentage
        if self.revenue_share == 0:
            self.revenue_share = self.share_percentage


@dataclass
class FractionalWork:
    """A work with fractional ownership."""
    work_id: str = ""
    work_title: str = ""

    # Shares
    total_shares: int = 1000000         # 1M shares = granular ownership
    shares: list[FractionalShare] = field(default_factory=list)

    # Governance
    licensing_threshold: Decimal = Decimal("51")  # % needed to approve license
    transfer_threshold: Decimal = Decimal("67")   # % needed to approve transfer

    # Revenue pool
    undistributed_revenue: Decimal = Decimal("0")
    total_distributed: Decimal = Decimal("0")

    # Valuation
    last_trade_price: Optional[Decimal] = None
    total_valuation: Optional[Decimal] = None

    def get_ownership_summary(self) -> dict:
        """Get summary of ownership distribution."""
        by_owner = {}
        for share in self.shares:
            if share.owner_id not in by_owner:
                by_owner[share.owner_id] = Decimal("0")
            by_owner[share.owner_id] += share.share_percentage

        return {
            "total_owners": len(by_owner),
            "owners": {k: float(v) for k, v in by_owner.items()},
            "largest_holder": max(by_owner.items(), key=lambda x: x[1]) if by_owner else None,
            "majority_threshold": float(self.licensing_threshold)
        }

    def can_approve_license(self, approving_owners: list[str]) -> dict:
        """Check if owners can approve a license."""
        total_approval = Decimal("0")
        for share in self.shares:
            if share.owner_id in approving_owners and share.can_license:
                total_approval += share.voting_weight

        can_approve = total_approval >= self.licensing_threshold

        return {
            "can_approve": can_approve,
            "approval_percentage": float(total_approval),
            "threshold": float(self.licensing_threshold),
            "shortfall": float(max(0, self.licensing_threshold - total_approval))
        }

    def distribute_revenue(self, amount: Decimal) -> list[dict]:
        """Distribute revenue to shareholders."""
        distributions = []

        for share in self.shares:
            share_amount = amount * (share.revenue_share / 100)
            share.accumulated_revenue += share_amount
            share.last_distribution = datetime.utcnow()

            distributions.append({
                "owner_id": share.owner_id,
                "amount": float(share_amount),
                "share_percentage": float(share.revenue_share)
            })

        self.total_distributed += amount

        return distributions


# ═══════════════════════════════════════════════════════════════════════════════
# License Option
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class LicenseOption:
    """
    Right to purchase a license at a future date.

    Like stock options, but for music rights.
    """
    option_id: str = field(default_factory=lambda: str(uuid4()))

    # Parties
    grantor_id: str = ""            # Selling the option
    holder_id: str = ""             # Buying the option
    work_id: str = ""

    # Option terms
    option_type: str = "call"       # "call" (buy) or "put" (sell back)
    strike_price: Decimal = Decimal("0")  # Price to exercise
    option_premium: Decimal = Decimal("0")  # Price paid for option

    # Underlying license
    underlying_use_category: str = ""
    underlying_duration_days: int = 365
    underlying_territories: list[str] = field(default_factory=list)

    # Time constraints
    grant_date: datetime = field(default_factory=datetime.utcnow)
    expiration_date: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=90))
    exercise_window_start: Optional[datetime] = None  # For European-style

    # State
    exercised: bool = False
    exercised_at: Optional[datetime] = None
    expired: bool = False
    resulting_license_id: Optional[str] = None

    def can_exercise(self) -> bool:
        """Check if option can be exercised."""
        if self.exercised or self.expired:
            return False

        now = datetime.utcnow()

        if now > self.expiration_date:
            self.expired = True
            return False

        if self.exercise_window_start and now < self.exercise_window_start:
            return False

        return True

    def exercise(self) -> dict:
        """Exercise the option."""
        if not self.can_exercise():
            return {"error": "Cannot exercise option"}

        self.exercised = True
        self.exercised_at = datetime.utcnow()

        # In practice, this would create the actual license
        license_id = str(uuid4())
        self.resulting_license_id = license_id

        return {
            "success": True,
            "license_id": license_id,
            "strike_price": float(self.strike_price),
            "exercised_at": self.exercised_at.isoformat()
        }

    def time_value(self, current_market_price: Decimal) -> Decimal:
        """Calculate option's time value."""
        # Simplified - real options pricing uses Black-Scholes
        days_remaining = (self.expiration_date - datetime.utcnow()).days
        intrinsic = max(0, current_market_price - self.strike_price)
        time_factor = Decimal(str(days_remaining / 365))

        return intrinsic + (self.option_premium * time_factor)


# ═══════════════════════════════════════════════════════════════════════════════
# Advanced License Manager
# ═══════════════════════════════════════════════════════════════════════════════

class AdvancedLicenseManager:
    """
    Manages advanced license types.

    Programmable, automated, transparent.
    """

    def __init__(self):
        self.time_locked: dict[str, TimeLockedLicense] = {}
        self.usage_based: dict[str, UsageBasedLicense] = {}
        self.fractional_works: dict[str, FractionalWork] = {}
        self.options: dict[str, LicenseOption] = {}

        # Auto-renewal queue
        self.renewal_queue: list[str] = []

    def create_time_locked_license(
        self,
        licensor_id: str,
        licensee_id: str,
        work_id: str,
        use_category: str,
        duration_days: int,
        renewal_policy: RenewalPolicy = RenewalPolicy.MANUAL,
        renewal_price: float = None,
        territories: list[str] = None
    ) -> TimeLockedLicense:
        """Create a time-locked license."""
        license = TimeLockedLicense(
            licensor_id=licensor_id,
            licensee_id=licensee_id,
            work_id=work_id,
            use_category=use_category,
            duration_days=duration_days,
            renewal_policy=renewal_policy,
            renewal_price=renewal_price,
            territories=territories or ["WW"],
            state=LicenseState.ACTIVE
        )

        self.time_locked[license.license_id] = license

        if renewal_policy == RenewalPolicy.AUTO_RENEW:
            self.renewal_queue.append(license.license_id)

        return license

    def create_usage_based_license(
        self,
        licensor_id: str,
        licensee_id: str,
        work_id: str,
        use_category: str,
        unit_type: str,
        price_per_unit: float,
        volume_discounts: dict = None
    ) -> UsageBasedLicense:
        """Create a usage-based license."""
        license = UsageBasedLicense(
            licensor_id=licensor_id,
            licensee_id=licensee_id,
            work_id=work_id,
            use_category=use_category,
            unit_type=unit_type,
            price_per_unit=Decimal(str(price_per_unit)),
            volume_discounts=volume_discounts or {}
        )

        self.usage_based[license.license_id] = license
        return license

    def create_fractional_work(
        self,
        work_id: str,
        work_title: str,
        initial_owners: list[dict]
    ) -> FractionalWork:
        """
        Create a work with fractional ownership.

        initial_owners: [{"owner_id": str, "share": float, "can_license": bool}, ...]
        """
        work = FractionalWork(
            work_id=work_id,
            work_title=work_title
        )

        for owner in initial_owners:
            share = FractionalShare(
                work_id=work_id,
                owner_id=owner["owner_id"],
                share_percentage=Decimal(str(owner["share"])),
                can_license=owner.get("can_license", True),
                acquisition_method="creation"
            )
            work.shares.append(share)

        self.fractional_works[work_id] = work
        return work

    def transfer_fractional_share(
        self,
        work_id: str,
        from_owner: str,
        to_owner: str,
        percentage: float,
        price: float = None
    ) -> dict:
        """Transfer fractional ownership."""
        work = self.fractional_works.get(work_id)
        if not work:
            return {"error": "Work not found"}

        # Find seller's shares
        seller_total = Decimal("0")
        seller_shares = []
        for share in work.shares:
            if share.owner_id == from_owner:
                seller_total += share.share_percentage
                seller_shares.append(share)

        transfer_amount = Decimal(str(percentage))
        if transfer_amount > seller_total:
            return {"error": f"Insufficient shares. Have {seller_total}%, need {percentage}%"}

        # Create new share for buyer
        new_share = FractionalShare(
            work_id=work_id,
            owner_id=to_owner,
            share_percentage=transfer_amount,
            acquisition_method="purchase",
            acquisition_price=Decimal(str(price)) if price else None
        )
        work.shares.append(new_share)

        # Reduce seller's shares
        remaining = transfer_amount
        for share in seller_shares:
            if remaining <= 0:
                break
            if share.share_percentage <= remaining:
                remaining -= share.share_percentage
                work.shares.remove(share)
            else:
                share.share_percentage -= remaining
                remaining = Decimal("0")

        # Update valuation
        if price:
            work.last_trade_price = Decimal(str(price)) / transfer_amount
            work.total_valuation = work.last_trade_price * 100

        return {
            "success": True,
            "transferred": float(transfer_amount),
            "from": from_owner,
            "to": to_owner,
            "price": price,
            "implied_valuation": float(work.total_valuation) if work.total_valuation else None
        }

    def create_license_option(
        self,
        grantor_id: str,
        holder_id: str,
        work_id: str,
        use_category: str,
        strike_price: float,
        premium: float,
        expiration_days: int = 90
    ) -> LicenseOption:
        """Create a license option."""
        option = LicenseOption(
            grantor_id=grantor_id,
            holder_id=holder_id,
            work_id=work_id,
            underlying_use_category=use_category,
            strike_price=Decimal(str(strike_price)),
            option_premium=Decimal(str(premium)),
            expiration_date=datetime.utcnow() + timedelta(days=expiration_days)
        )

        self.options[option.option_id] = option
        return option

    def process_renewals(self) -> list[dict]:
        """Process auto-renewal queue."""
        results = []

        for license_id in self.renewal_queue[:]:
            license = self.time_locked.get(license_id)
            if not license:
                self.renewal_queue.remove(license_id)
                continue

            if license.state == LicenseState.ACTIVE and not license.is_active():
                # Time to renew
                if license.renewal_policy == RenewalPolicy.AUTO_RENEW:
                    success = license.renew()
                    results.append({
                        "license_id": license_id,
                        "renewed": success,
                        "new_end_time": license.end_time.isoformat() if success else None
                    })

        return results


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate advanced licenses."""
    print("\n" + "=" * 70)
    print("ADVANCED LICENSES — DEMO")
    print("Programmable rights for the future")
    print("=" * 70)

    manager = AdvancedLicenseManager()

    # Time-locked license
    print("\n" + "─" * 50)
    print("1. TIME-LOCKED LICENSES")
    print("─" * 50)

    tl_license = manager.create_time_locked_license(
        licensor_id="creator-A",
        licensee_id="streamer-X",
        work_id="song-123",
        use_category="streaming",
        duration_days=30,
        renewal_policy=RenewalPolicy.AUTO_RENEW,
        renewal_price=99.99
    )

    print(f"  Created: {tl_license.license_id[:8]}...")
    print(f"    Duration: {tl_license.duration_days} days")
    print(f"    Renewal: {tl_license.renewal_policy.value}")
    print(f"    Time remaining: {tl_license.time_remaining()}")
    print(f"    Active: {tl_license.is_active()}")

    # Usage-based license
    print("\n" + "─" * 50)
    print("2. USAGE-BASED LICENSES")
    print("─" * 50)

    ub_license = manager.create_usage_based_license(
        licensor_id="creator-B",
        licensee_id="radio-station-Y",
        work_id="song-456",
        use_category="broadcast",
        unit_type="play",
        price_per_unit=0.10,
        volume_discounts={
            "100": 0.9,     # 10% off after 100 plays
            "1000": 0.8,    # 20% off after 1000 plays
            "10000": 0.7    # 30% off after 10k plays
        }
    )

    print(f"  Created: {ub_license.license_id[:8]}...")
    print(f"    Price per play: ${float(ub_license.price_per_unit):.2f}")
    print(f"    Volume discounts: {ub_license.volume_discounts}")

    # Record some usage
    for plays in [50, 100, 500]:
        result = ub_license.record_usage(plays)
        print(f"    Recorded {plays} plays @ ${result['rate_applied']:.3f} = ${result['cost']:.2f}")

    print(f"    Total plays: {ub_license.units_used}")

    # Fractional ownership
    print("\n" + "─" * 50)
    print("3. FRACTIONAL OWNERSHIP")
    print("─" * 50)

    fractional = manager.create_fractional_work(
        work_id="hit-song-789",
        work_title="Global Hit Song",
        initial_owners=[
            {"owner_id": "songwriter", "share": 40.0, "can_license": True},
            {"owner_id": "producer", "share": 30.0, "can_license": True},
            {"owner_id": "label", "share": 20.0, "can_license": True},
            {"owner_id": "investor-1", "share": 10.0, "can_license": False}
        ]
    )

    print(f"  Created fractional work: {fractional.work_title}")
    summary = fractional.get_ownership_summary()
    print(f"    Total owners: {summary['total_owners']}")
    for owner, share in summary['owners'].items():
        print(f"      {owner}: {share}%")

    # Check licensing approval
    approval = fractional.can_approve_license(["songwriter", "producer"])
    print(f"\n  Can songwriter + producer approve license?")
    print(f"    Result: {approval['can_approve']}")
    print(f"    Combined voting power: {approval['approval_percentage']}%")
    print(f"    Threshold: {approval['threshold']}%")

    # Transfer shares
    print("\n  Transferring 5% from investor to fan...")
    transfer = manager.transfer_fractional_share(
        work_id="hit-song-789",
        from_owner="investor-1",
        to_owner="superfan",
        percentage=5.0,
        price=5000.0
    )
    print(f"    Success: {transfer['success']}")
    print(f"    Implied valuation: ${transfer['implied_valuation']:,.2f}")

    # Distribute revenue
    print("\n  Distributing $10,000 in royalties...")
    distributions = fractional.distribute_revenue(Decimal("10000"))
    for dist in distributions:
        print(f"    {dist['owner_id']}: ${dist['amount']:,.2f} ({dist['share_percentage']}%)")

    # License options
    print("\n" + "─" * 50)
    print("4. LICENSE OPTIONS")
    print("─" * 50)

    option = manager.create_license_option(
        grantor_id="creator-C",
        holder_id="film-studio",
        work_id="potential-soundtrack",
        use_category="sync_film",
        strike_price=50000.0,      # Can buy sync license for $50k
        premium=5000.0,             # Costs $5k for the option
        expiration_days=180        # 6 months to decide
    )

    print(f"  Created option: {option.option_id[:8]}...")
    print(f"    Strike price: ${float(option.strike_price):,.2f}")
    print(f"    Premium paid: ${float(option.option_premium):,.2f}")
    print(f"    Expires: {option.expiration_date.date()}")
    print(f"    Can exercise: {option.can_exercise()}")

    # Exercise the option
    print("\n  Film studio exercises option...")
    exercise_result = option.exercise()
    print(f"    Success: {exercise_result.get('success')}")
    print(f"    License ID: {exercise_result.get('license_id', 'N/A')[:8]}...")
    print(f"    Price locked in: ${exercise_result.get('strike_price', 0):,.2f}")

    print("\n" + "=" * 70)
    print("2056 VALUE: Rights that program themselves")
    print("=" * 70)


if __name__ == "__main__":
    demo()
