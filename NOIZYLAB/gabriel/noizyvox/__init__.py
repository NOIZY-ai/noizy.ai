"""
NOIZYVOX — The Voice Guild
===========================

Where human voices are sovereign.

"Your voice is your birthright. No algorithm shall steal it.
 No corporation shall own it. No AI shall clone it without blessing."

The Guild protects voice actors, narrators, podcasters, singers,
and every human who earns their living through the power of voice.

Components:
- Guild: Member management, tiers, governance
- VoiceRegistry: Voice print registration and protection
- ConsentEngine: Integration with NOIZYFISH
- RoyaltyTracker: Earnings and payment distribution
- ProjectManager: Voice work assignments and contracts

Guild Tiers:
- Initiate: New members (0-6 months)
- Apprentice: Learning the craft (6-18 months)
- Journeyman: Professional work (18+ months)
- Master: Established career (5+ years)
- Elder: Guild leadership (10+ years)
"""

__version__ = "1.0.0"
__author__ = "NOIZYLAB"

from .guild import (
    Guild,
    GuildMember,
    GuildTier,
    GuildRole,
    MemberStatus
)
from .voice_registry import (
    VoiceRegistry,
    VoiceProfile,
    VoicePrint,
    VoiceCapability
)
from .consent import (
    VoiceConsent,
    ConsentType,
    UsageRights,
    ConsentStatus
)
from .royalties import (
    RoyaltyTracker,
    Payment,
    Earnings,
    PayoutSchedule
)
from .projects import (
    Project,
    ProjectStatus,
    VoiceRole,
    Contract
)

__all__ = [
    # Guild
    "Guild",
    "GuildMember",
    "GuildTier",
    "GuildRole",
    "MemberStatus",
    # Voice Registry
    "VoiceRegistry",
    "VoiceProfile",
    "VoicePrint",
    "VoiceCapability",
    # Consent
    "VoiceConsent",
    "ConsentType",
    "UsageRights",
    "ConsentStatus",
    # Royalties
    "RoyaltyTracker",
    "Payment",
    "Earnings",
    "PayoutSchedule",
    # Projects
    "Project",
    "ProjectStatus",
    "VoiceRole",
    "Contract"
]
