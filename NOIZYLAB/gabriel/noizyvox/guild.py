"""
NOIZYVOX Guild System
=====================

The heart of the Voice Guild.

Manages members, tiers, governance, and community.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import hashlib


class GuildTier(Enum):
    """Guild membership tiers based on experience and contribution."""
    INITIATE = "initiate"       # 0-6 months, learning
    APPRENTICE = "apprentice"   # 6-18 months, developing
    JOURNEYMAN = "journeyman"   # 18+ months, professional
    MASTER = "master"           # 5+ years, established
    ELDER = "elder"             # 10+ years, leadership

    @property
    def min_months(self) -> int:
        """Minimum months of membership for this tier."""
        return {
            GuildTier.INITIATE: 0,
            GuildTier.APPRENTICE: 6,
            GuildTier.JOURNEYMAN: 18,
            GuildTier.MASTER: 60,
            GuildTier.ELDER: 120
        }[self]

    @property
    def voting_weight(self) -> float:
        """Voting weight in guild decisions."""
        return {
            GuildTier.INITIATE: 0.0,      # Cannot vote
            GuildTier.APPRENTICE: 0.5,    # Half vote
            GuildTier.JOURNEYMAN: 1.0,    # Full vote
            GuildTier.MASTER: 1.5,        # Enhanced vote
            GuildTier.ELDER: 2.0          # Double vote
        }[self]

    @property
    def revenue_share(self) -> float:
        """Share of guild revenue pool."""
        return {
            GuildTier.INITIATE: 0.05,
            GuildTier.APPRENTICE: 0.10,
            GuildTier.JOURNEYMAN: 0.15,
            GuildTier.MASTER: 0.25,
            GuildTier.ELDER: 0.35
        }[self]


class GuildRole(Enum):
    """Functional roles within the Guild."""
    MEMBER = "member"                   # Standard member
    MENTOR = "mentor"                   # Guides apprentices
    ARBITER = "arbiter"                 # Resolves disputes
    REGISTRAR = "registrar"             # Manages voice registry
    TREASURER = "treasurer"             # Handles finances
    COUNCIL = "council"                 # Governing council
    GUILD_MASTER = "guild_master"       # Overall leadership


class MemberStatus(Enum):
    """Member account status."""
    PENDING = "pending"           # Application submitted
    ACTIVE = "active"             # Full member
    SUSPENDED = "suspended"       # Temporarily restricted
    EMERITUS = "emeritus"         # Retired with honor
    REVOKED = "revoked"           # Membership revoked


class VoiceSpecialty(Enum):
    """Voice work specializations."""
    NARRATION = "narration"
    AUDIOBOOK = "audiobook"
    COMMERCIAL = "commercial"
    ANIMATION = "animation"
    VIDEO_GAME = "video_game"
    PODCAST = "podcast"
    DOCUMENTARY = "documentary"
    E_LEARNING = "e_learning"
    IVR = "ivr"
    SINGING = "singing"
    DUBBING = "dubbing"
    LIVE_ANNOUNCE = "live_announce"


@dataclass
class GuildMember:
    """A member of the Voice Guild."""
    member_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    legal_name: str = ""
    stage_name: str = ""
    email: str = ""
    phone: Optional[str] = None

    # Guild status
    tier: GuildTier = GuildTier.INITIATE
    roles: List[GuildRole] = field(default_factory=lambda: [GuildRole.MEMBER])
    status: MemberStatus = MemberStatus.PENDING

    # Voice profile
    voice_print_id: Optional[str] = None
    specialties: List[VoiceSpecialty] = field(default_factory=list)
    languages: List[str] = field(default_factory=lambda: ["English"])
    accents: List[str] = field(default_factory=list)
    voice_range: str = ""  # e.g., "Baritone", "Soprano", etc.

    # Experience
    years_experience: float = 0.0
    portfolio_url: Optional[str] = None
    demo_reel_url: Optional[str] = None

    # Consent & Protection
    noizyfish_id: Optional[str] = None  # Link to NOIZYFISH registry
    ai_training_consent: bool = False
    synthetic_voice_consent: bool = False
    consent_last_updated: Optional[datetime] = None

    # Financial
    hourly_rate_min: float = 0.0
    hourly_rate_max: float = 0.0
    total_earnings: float = 0.0
    pending_payments: float = 0.0

    # Mentorship
    mentor_id: Optional[str] = None
    mentees: List[str] = field(default_factory=list)

    # Dates
    application_date: datetime = field(default_factory=datetime.utcnow)
    join_date: Optional[datetime] = None
    last_active: datetime = field(default_factory=datetime.utcnow)

    # Metadata
    bio: str = ""
    location: str = ""
    timezone: str = "UTC"
    equipment: List[str] = field(default_factory=list)
    home_studio: bool = False

    def __post_init__(self):
        """Generate stage name if not provided."""
        if not self.stage_name and self.legal_name:
            self.stage_name = self.legal_name

    @property
    def membership_months(self) -> int:
        """Months of active membership."""
        if not self.join_date:
            return 0
        delta = datetime.utcnow() - self.join_date
        return int(delta.days / 30)

    @property
    def eligible_tier(self) -> GuildTier:
        """Highest tier member is eligible for based on time."""
        months = self.membership_months
        years = self.years_experience

        if years >= 10 or months >= 120:
            return GuildTier.ELDER
        elif years >= 5 or months >= 60:
            return GuildTier.MASTER
        elif months >= 18:
            return GuildTier.JOURNEYMAN
        elif months >= 6:
            return GuildTier.APPRENTICE
        else:
            return GuildTier.INITIATE

    @property
    def can_vote(self) -> bool:
        """Whether member can vote in guild decisions."""
        return (
            self.status == MemberStatus.ACTIVE and
            self.tier.voting_weight > 0
        )

    @property
    def can_mentor(self) -> bool:
        """Whether member can mentor others."""
        return self.tier in [GuildTier.JOURNEYMAN, GuildTier.MASTER, GuildTier.ELDER]

    def activate(self):
        """Activate membership."""
        self.status = MemberStatus.ACTIVE
        self.join_date = datetime.utcnow()

    def update_tier(self):
        """Update tier based on eligibility."""
        eligible = self.eligible_tier
        if eligible.min_months > self.tier.min_months:
            self.tier = eligible
            return True
        return False

    def assign_mentor(self, mentor_id: str):
        """Assign a mentor to this member."""
        self.mentor_id = mentor_id

    def add_mentee(self, mentee_id: str):
        """Add a mentee to this member."""
        if mentee_id not in self.mentees:
            self.mentees.append(mentee_id)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "member_id": self.member_id,
            "legal_name": self.legal_name,
            "stage_name": self.stage_name,
            "email": self.email,
            "tier": self.tier.value,
            "roles": [r.value for r in self.roles],
            "status": self.status.value,
            "specialties": [s.value for s in self.specialties],
            "languages": self.languages,
            "years_experience": self.years_experience,
            "membership_months": self.membership_months,
            "ai_training_consent": self.ai_training_consent,
            "synthetic_voice_consent": self.synthetic_voice_consent,
            "can_vote": self.can_vote,
            "can_mentor": self.can_mentor
        }


class Guild:
    """
    The Voice Guild.

    Manages all members, governance, and operations.
    """

    def __init__(self, name: str = "NOIZYVOX"):
        self.name = name
        self.guild_id = str(uuid4())
        self.members: Dict[str, GuildMember] = {}
        self.founded = datetime.utcnow()

        # Governance
        self.council_size = 7
        self.quorum_percentage = 0.6

        # Finances
        self.treasury_balance = 0.0
        self.membership_fee_monthly = 25.0
        self.revenue_pool = 0.0

    # ─────────────────────────────────────────────────────────────────────────
    # Member Management
    # ─────────────────────────────────────────────────────────────────────────

    def apply(self, member: GuildMember) -> str:
        """Submit a membership application."""
        member.status = MemberStatus.PENDING
        member.application_date = datetime.utcnow()
        self.members[member.member_id] = member
        return member.member_id

    def approve(self, member_id: str) -> bool:
        """Approve a membership application."""
        member = self.members.get(member_id)
        if not member:
            return False

        member.activate()
        return True

    def suspend(self, member_id: str, reason: str = "") -> bool:
        """Suspend a member."""
        member = self.members.get(member_id)
        if not member:
            return False

        member.status = MemberStatus.SUSPENDED
        return True

    def revoke(self, member_id: str, reason: str = "") -> bool:
        """Revoke membership entirely."""
        member = self.members.get(member_id)
        if not member:
            return False

        member.status = MemberStatus.REVOKED
        return True

    def promote(self, member_id: str) -> Optional[GuildTier]:
        """Promote member to their eligible tier."""
        member = self.members.get(member_id)
        if not member:
            return None

        if member.update_tier():
            return member.tier
        return None

    def assign_role(self, member_id: str, role: GuildRole) -> bool:
        """Assign a role to a member."""
        member = self.members.get(member_id)
        if not member:
            return False

        if role not in member.roles:
            member.roles.append(role)
        return True

    def get_member(self, member_id: str) -> Optional[GuildMember]:
        """Get a member by ID."""
        return self.members.get(member_id)

    def find_by_email(self, email: str) -> Optional[GuildMember]:
        """Find a member by email."""
        for member in self.members.values():
            if member.email.lower() == email.lower():
                return member
        return None

    def find_by_stage_name(self, name: str) -> Optional[GuildMember]:
        """Find a member by stage name."""
        for member in self.members.values():
            if member.stage_name.lower() == name.lower():
                return member
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # Queries
    # ─────────────────────────────────────────────────────────────────────────

    def get_active_members(self) -> List[GuildMember]:
        """Get all active members."""
        return [m for m in self.members.values() if m.status == MemberStatus.ACTIVE]

    def get_members_by_tier(self, tier: GuildTier) -> List[GuildMember]:
        """Get members of a specific tier."""
        return [m for m in self.get_active_members() if m.tier == tier]

    def get_members_by_specialty(self, specialty: VoiceSpecialty) -> List[GuildMember]:
        """Get members with a specific specialty."""
        return [m for m in self.get_active_members() if specialty in m.specialties]

    def get_available_mentors(self) -> List[GuildMember]:
        """Get members available to mentor."""
        return [m for m in self.get_active_members()
                if m.can_mentor and len(m.mentees) < 3]

    def get_council_members(self) -> List[GuildMember]:
        """Get governing council members."""
        return [m for m in self.get_active_members()
                if GuildRole.COUNCIL in m.roles or GuildRole.GUILD_MASTER in m.roles]

    # ─────────────────────────────────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get guild statistics."""
        active = self.get_active_members()

        tier_counts = {}
        for tier in GuildTier:
            tier_counts[tier.value] = len(self.get_members_by_tier(tier))

        specialty_counts = {}
        for specialty in VoiceSpecialty:
            specialty_counts[specialty.value] = len(self.get_members_by_specialty(specialty))

        return {
            "guild_name": self.name,
            "guild_id": self.guild_id,
            "founded": self.founded.isoformat(),
            "total_members": len(self.members),
            "active_members": len(active),
            "pending_applications": len([m for m in self.members.values()
                                         if m.status == MemberStatus.PENDING]),
            "tier_distribution": tier_counts,
            "specialty_distribution": specialty_counts,
            "total_voting_power": sum(m.tier.voting_weight for m in active if m.can_vote),
            "council_members": len(self.get_council_members()),
            "treasury_balance": self.treasury_balance,
            "revenue_pool": self.revenue_pool
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Mentorship
    # ─────────────────────────────────────────────────────────────────────────

    def pair_mentor(self, mentee_id: str, mentor_id: str = None) -> bool:
        """Pair a mentee with a mentor."""
        mentee = self.members.get(mentee_id)
        if not mentee or mentee.tier not in [GuildTier.INITIATE, GuildTier.APPRENTICE]:
            return False

        # Find or validate mentor
        if mentor_id:
            mentor = self.members.get(mentor_id)
        else:
            # Auto-assign available mentor
            available = self.get_available_mentors()
            if not available:
                return False
            # Match by specialty if possible
            matching = [m for m in available
                        if any(s in m.specialties for s in mentee.specialties)]
            mentor = matching[0] if matching else available[0]

        if not mentor or not mentor.can_mentor:
            return False

        mentee.assign_mentor(mentor.member_id)
        mentor.add_mentee(mentee.member_id)
        return True


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Guild system."""
    print("\n" + "=" * 70)
    print("NOIZYVOX GUILD — DEMO")
    print("Where human voices are sovereign")
    print("=" * 70)

    # Create guild
    guild = Guild("NOIZYVOX")

    print(f"\n  Guild created: {guild.name}")
    print(f"  Guild ID: {guild.guild_id[:8]}...")

    # Create members
    print("\n" + "─" * 50)
    print("  REGISTERING MEMBERS")
    print("─" * 50)

    # Elder member
    elder = GuildMember(
        legal_name="Marcus Williams",
        stage_name="Marcus the Narrator",
        email="marcus@noizyvox.ai",
        years_experience=15,
        specialties=[VoiceSpecialty.AUDIOBOOK, VoiceSpecialty.NARRATION, VoiceSpecialty.DOCUMENTARY],
        languages=["English", "Spanish"],
        voice_range="Baritone",
        bio="Fifteen years in audiobooks. Voice of the people.",
        home_studio=True
    )
    elder.tier = GuildTier.ELDER
    elder.roles = [GuildRole.MEMBER, GuildRole.MENTOR, GuildRole.COUNCIL]
    guild.apply(elder)
    guild.approve(elder.member_id)
    print(f"  ✓ {elder.stage_name} — Elder, Council Member")

    # Master member
    master = GuildMember(
        legal_name="Sarah Chen",
        stage_name="Sarah Chen",
        email="sarah@noizyvox.ai",
        years_experience=7,
        specialties=[VoiceSpecialty.ANIMATION, VoiceSpecialty.VIDEO_GAME, VoiceSpecialty.COMMERCIAL],
        languages=["English", "Mandarin"],
        voice_range="Mezzo-soprano",
        home_studio=True
    )
    master.tier = GuildTier.MASTER
    master.roles = [GuildRole.MEMBER, GuildRole.MENTOR]
    guild.apply(master)
    guild.approve(master.member_id)
    print(f"  ✓ {master.stage_name} — Master, Mentor")

    # Journeyman member
    journeyman = GuildMember(
        legal_name="David Park",
        stage_name="Dave Park VO",
        email="dave@noizyvox.ai",
        years_experience=3,
        specialties=[VoiceSpecialty.E_LEARNING, VoiceSpecialty.IVR, VoiceSpecialty.COMMERCIAL],
        languages=["English", "Korean"],
        voice_range="Tenor",
        home_studio=True
    )
    journeyman.tier = GuildTier.JOURNEYMAN
    guild.apply(journeyman)
    guild.approve(journeyman.member_id)
    print(f"  ✓ {journeyman.stage_name} — Journeyman")

    # New initiate
    initiate = GuildMember(
        legal_name="Jordan Taylor",
        stage_name="J.T. Voice",
        email="jt@noizyvox.ai",
        years_experience=0.5,
        specialties=[VoiceSpecialty.PODCAST, VoiceSpecialty.NARRATION],
        languages=["English"],
        voice_range="Alto",
        home_studio=False
    )
    guild.apply(initiate)
    guild.approve(initiate.member_id)
    print(f"  ✓ {initiate.stage_name} — Initiate")

    # Pair mentor
    print("\n" + "─" * 50)
    print("  MENTORSHIP PAIRING")
    print("─" * 50)

    if guild.pair_mentor(initiate.member_id):
        print(f"  ✓ {initiate.stage_name} paired with mentor")
        mentor = guild.get_member(initiate.mentor_id)
        if mentor:
            print(f"    Mentor: {mentor.stage_name}")

    # Guild stats
    print("\n" + "─" * 50)
    print("  GUILD STATISTICS")
    print("─" * 50)

    stats = guild.get_stats()
    print(f"\n  Total members: {stats['total_members']}")
    print(f"  Active members: {stats['active_members']}")
    print(f"  Council members: {stats['council_members']}")
    print(f"  Total voting power: {stats['total_voting_power']}")

    print(f"\n  Tier distribution:")
    for tier, count in stats['tier_distribution'].items():
        if count > 0:
            print(f"    {tier}: {count}")

    print(f"\n  Top specialties:")
    sorted_specs = sorted(stats['specialty_distribution'].items(), key=lambda x: x[1], reverse=True)
    for spec, count in sorted_specs[:5]:
        if count > 0:
            print(f"    {spec}: {count}")

    # Available mentors
    print("\n" + "─" * 50)
    print("  AVAILABLE MENTORS")
    print("─" * 50)

    mentors = guild.get_available_mentors()
    for mentor in mentors:
        print(f"  • {mentor.stage_name} ({mentor.tier.value})")
        print(f"    Specialties: {', '.join(s.value for s in mentor.specialties)}")

    print("\n" + "=" * 70)
    print("Your voice is your birthright. The Guild protects it.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
