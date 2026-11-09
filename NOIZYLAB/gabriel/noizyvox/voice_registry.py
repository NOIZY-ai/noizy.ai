"""
NOIZYVOX Voice Registry
=======================

Voice print registration and protection.

Every voice is unique. Every voice is sovereign.
The Registry protects your vocal identity.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import hashlib
import json


class VoiceCapability(Enum):
    """Voice capabilities and characteristics."""
    # Range
    BASS = "bass"
    BARITONE = "baritone"
    TENOR = "tenor"
    ALTO = "alto"
    MEZZO_SOPRANO = "mezzo_soprano"
    SOPRANO = "soprano"

    # Character types
    HERO = "hero"
    VILLAIN = "villain"
    COMEDIC = "comedic"
    DRAMATIC = "dramatic"
    AUTHORITATIVE = "authoritative"
    WARM = "warm"
    EDGY = "edgy"
    SULTRY = "sultry"

    # Special skills
    ACCENTS = "accents"
    DIALECTS = "dialects"
    SINGING = "singing"
    SCREAMING = "screaming"
    WHISPERING = "whispering"
    CREATURE_SOUNDS = "creature_sounds"
    IMPRESSIONS = "impressions"
    RAPID_FIRE = "rapid_fire"

    # Age ranges
    CHILD = "child"
    TEEN = "teen"
    YOUNG_ADULT = "young_adult"
    MIDDLE_AGE = "middle_age"
    ELDERLY = "elderly"


class VoicePrintStatus(Enum):
    """Status of voice print registration."""
    PENDING = "pending"           # Awaiting verification
    VERIFIED = "verified"         # Confirmed authentic
    PROTECTED = "protected"       # Active AI protection
    DISPUTED = "disputed"         # Ownership disputed
    REVOKED = "revoked"          # Registration cancelled


@dataclass
class VoiceSample:
    """A voice sample for registration."""
    sample_id: str = field(default_factory=lambda: str(uuid4()))

    # File info
    file_path: str = ""
    file_hash: str = ""
    duration_seconds: float = 0.0
    sample_rate: int = 48000
    bit_depth: int = 24

    # Content
    transcript: str = ""
    language: str = "English"
    sample_type: str = "general"  # general, character, narration, commercial, etc.

    # Technical
    noise_floor_db: float = -60.0
    peak_db: float = 0.0
    rms_db: float = -20.0

    # Metadata
    recorded_date: datetime = field(default_factory=datetime.utcnow)
    recording_location: str = ""
    equipment_used: List[str] = field(default_factory=list)

    def compute_hash(self, file_content: bytes) -> str:
        """Compute SHA-256 hash of file content."""
        self.file_hash = hashlib.sha256(file_content).hexdigest()
        return self.file_hash


@dataclass
class VoicePrint:
    """
    A registered voice print.

    The cryptographic identity of a voice.
    """
    print_id: str = field(default_factory=lambda: str(uuid4()))

    # Owner
    member_id: str = ""
    owner_name: str = ""

    # Status
    status: VoicePrintStatus = VoicePrintStatus.PENDING

    # Voice samples (minimum 3 for verification)
    samples: List[VoiceSample] = field(default_factory=list)

    # Biometric fingerprint
    fingerprint_hash: str = ""  # Hash of extracted voice features
    spectral_signature: Optional[str] = None
    formant_pattern: Optional[str] = None

    # Characteristics
    capabilities: List[VoiceCapability] = field(default_factory=list)
    pitch_range_hz: tuple = (85, 300)  # Low to high
    natural_tempo_wpm: int = 150

    # Protection
    ai_protection_enabled: bool = True
    synthetic_clone_registered: bool = False
    authorized_uses: List[str] = field(default_factory=list)

    # NOIZYFISH integration
    noizyfish_registration_id: Optional[str] = None
    consent_hash: Optional[str] = None

    # Dates
    registered_date: datetime = field(default_factory=datetime.utcnow)
    last_verified: Optional[datetime] = None
    protection_expires: Optional[datetime] = None

    @property
    def is_verified(self) -> bool:
        """Check if voice print is verified."""
        return self.status in [VoicePrintStatus.VERIFIED, VoicePrintStatus.PROTECTED]

    @property
    def sample_count(self) -> int:
        """Number of registered samples."""
        return len(self.samples)

    @property
    def total_duration(self) -> float:
        """Total duration of all samples."""
        return sum(s.duration_seconds for s in self.samples)

    def add_sample(self, sample: VoiceSample):
        """Add a voice sample."""
        self.samples.append(sample)

    def generate_fingerprint(self) -> str:
        """Generate fingerprint hash from samples."""
        # In production, this would extract actual voice biometrics
        # For now, we hash sample metadata
        data = json.dumps({
            "member_id": self.member_id,
            "sample_hashes": [s.file_hash for s in self.samples],
            "sample_count": len(self.samples),
            "total_duration": self.total_duration
        }, sort_keys=True)

        self.fingerprint_hash = hashlib.sha256(data.encode()).hexdigest()
        return self.fingerprint_hash

    def verify(self) -> bool:
        """Verify voice print (requires 3+ samples, 60+ seconds total)."""
        if self.sample_count < 3:
            return False
        if self.total_duration < 60:
            return False

        self.generate_fingerprint()
        self.status = VoicePrintStatus.VERIFIED
        self.last_verified = datetime.utcnow()
        return True

    def enable_protection(self) -> bool:
        """Enable AI protection for this voice print."""
        if not self.is_verified:
            return False

        self.status = VoicePrintStatus.PROTECTED
        self.ai_protection_enabled = True
        return True


@dataclass
class VoiceProfile:
    """
    Complete voice profile for a guild member.

    Combines voice print with portfolio and settings.
    """
    profile_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    member_id: str = ""
    display_name: str = ""

    # Voice print
    voice_print: Optional[VoicePrint] = None

    # Portfolio
    demo_reel_url: Optional[str] = None
    portfolio_samples: List[VoiceSample] = field(default_factory=list)

    # Capabilities
    primary_capabilities: List[VoiceCapability] = field(default_factory=list)
    languages: List[str] = field(default_factory=lambda: ["English"])
    accents: List[str] = field(default_factory=list)

    # Availability
    available_for_work: bool = True
    turnaround_days: int = 3
    accepts_rush_jobs: bool = True

    # Rates
    hourly_rate: float = 0.0
    per_finished_hour: float = 0.0
    buyout_multiplier: float = 2.0

    # Preferences
    will_do_ai_training: bool = False
    will_do_synthetic_clone: bool = False
    preferred_project_types: List[str] = field(default_factory=list)
    excluded_content: List[str] = field(default_factory=list)

    # Stats
    projects_completed: int = 0
    average_rating: float = 5.0
    response_rate: float = 1.0

    @property
    def is_protected(self) -> bool:
        """Check if voice is protected."""
        return (
            self.voice_print is not None and
            self.voice_print.status == VoicePrintStatus.PROTECTED
        )


class VoiceRegistry:
    """
    The Voice Registry.

    Central registry for all voice prints and profiles.
    """

    def __init__(self):
        self.registry_id = str(uuid4())
        self.voice_prints: Dict[str, VoicePrint] = {}
        self.profiles: Dict[str, VoiceProfile] = {}
        self.created = datetime.utcnow()

    # ─────────────────────────────────────────────────────────────────────────
    # Registration
    # ─────────────────────────────────────────────────────────────────────────

    def register_voice_print(self, member_id: str, owner_name: str) -> VoicePrint:
        """Create a new voice print registration."""
        print = VoicePrint(
            member_id=member_id,
            owner_name=owner_name
        )
        self.voice_prints[print.print_id] = print
        return print

    def add_sample_to_print(self, print_id: str, sample: VoiceSample) -> bool:
        """Add a sample to a voice print."""
        print = self.voice_prints.get(print_id)
        if not print:
            return False

        print.add_sample(sample)
        return True

    def verify_voice_print(self, print_id: str) -> bool:
        """Verify a voice print."""
        print = self.voice_prints.get(print_id)
        if not print:
            return False

        return print.verify()

    def enable_protection(self, print_id: str) -> bool:
        """Enable AI protection for a voice print."""
        print = self.voice_prints.get(print_id)
        if not print:
            return False

        return print.enable_protection()

    # ─────────────────────────────────────────────────────────────────────────
    # Profiles
    # ─────────────────────────────────────────────────────────────────────────

    def create_profile(self, member_id: str, display_name: str) -> VoiceProfile:
        """Create a voice profile."""
        profile = VoiceProfile(
            member_id=member_id,
            display_name=display_name
        )
        self.profiles[profile.profile_id] = profile
        return profile

    def link_voice_print(self, profile_id: str, print_id: str) -> bool:
        """Link a voice print to a profile."""
        profile = self.profiles.get(profile_id)
        print = self.voice_prints.get(print_id)

        if not profile or not print:
            return False

        profile.voice_print = print
        return True

    def get_profile(self, profile_id: str) -> Optional[VoiceProfile]:
        """Get a profile by ID."""
        return self.profiles.get(profile_id)

    def get_profile_by_member(self, member_id: str) -> Optional[VoiceProfile]:
        """Get profile by member ID."""
        for profile in self.profiles.values():
            if profile.member_id == member_id:
                return profile
        return None

    # ─────────────────────────────────────────────────────────────────────────
    # Search
    # ─────────────────────────────────────────────────────────────────────────

    def search_by_capability(self, capability: VoiceCapability) -> List[VoiceProfile]:
        """Find profiles with a specific capability."""
        return [
            p for p in self.profiles.values()
            if capability in p.primary_capabilities and p.available_for_work
        ]

    def search_by_language(self, language: str) -> List[VoiceProfile]:
        """Find profiles that speak a language."""
        return [
            p for p in self.profiles.values()
            if language in p.languages and p.available_for_work
        ]

    def search_available(self, max_rate: float = None) -> List[VoiceProfile]:
        """Find available profiles, optionally by rate."""
        profiles = [p for p in self.profiles.values() if p.available_for_work]

        if max_rate:
            profiles = [p for p in profiles if p.hourly_rate <= max_rate]

        return sorted(profiles, key=lambda p: p.average_rating, reverse=True)

    # ─────────────────────────────────────────────────────────────────────────
    # AI Protection
    # ─────────────────────────────────────────────────────────────────────────

    def check_protected_voice(self, fingerprint: str) -> Optional[VoicePrint]:
        """Check if a voice fingerprint matches a protected voice."""
        for print in self.voice_prints.values():
            if print.fingerprint_hash == fingerprint:
                if print.ai_protection_enabled:
                    return print
        return None

    def report_unauthorized_use(self, print_id: str, evidence: Dict) -> str:
        """Report unauthorized use of a protected voice."""
        report_id = str(uuid4())
        # In production, this would create a formal complaint
        # and potentially integrate with legal systems
        return report_id

    # ─────────────────────────────────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        protected_count = sum(
            1 for p in self.voice_prints.values()
            if p.status == VoicePrintStatus.PROTECTED
        )

        return {
            "total_voice_prints": len(self.voice_prints),
            "verified_prints": sum(1 for p in self.voice_prints.values() if p.is_verified),
            "protected_prints": protected_count,
            "total_profiles": len(self.profiles),
            "available_for_work": sum(1 for p in self.profiles.values() if p.available_for_work),
            "total_samples": sum(p.sample_count for p in self.voice_prints.values()),
            "total_duration_hours": sum(p.total_duration for p in self.voice_prints.values()) / 3600
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Voice Registry."""
    print("\n" + "=" * 70)
    print("NOIZYVOX VOICE REGISTRY — DEMO")
    print("Voice print registration and protection")
    print("=" * 70)

    registry = VoiceRegistry()

    # Register a voice print
    print("\n" + "─" * 50)
    print("  REGISTERING VOICE PRINT")
    print("─" * 50)

    voice_print = registry.register_voice_print(
        member_id="member_123",
        owner_name="Marcus Williams"
    )
    print(f"  Created voice print: {voice_print.print_id[:8]}...")

    # Add samples
    samples = [
        VoiceSample(
            file_path="/audio/marcus_sample_1.wav",
            duration_seconds=45.0,
            sample_type="narration",
            transcript="The voice is the most human instrument of all..."
        ),
        VoiceSample(
            file_path="/audio/marcus_sample_2.wav",
            duration_seconds=30.0,
            sample_type="character",
            transcript="I've seen things you wouldn't believe..."
        ),
        VoiceSample(
            file_path="/audio/marcus_sample_3.wav",
            duration_seconds=25.0,
            sample_type="commercial",
            transcript="When quality matters, choose excellence."
        )
    ]

    for sample in samples:
        sample.compute_hash(f"fake_audio_data_{sample.sample_id}".encode())
        registry.add_sample_to_print(voice_print.print_id, sample)
        print(f"  Added sample: {sample.sample_type} ({sample.duration_seconds}s)")

    print(f"\n  Total duration: {voice_print.total_duration}s")
    print(f"  Sample count: {voice_print.sample_count}")

    # Verify
    print("\n" + "─" * 50)
    print("  VERIFYING VOICE PRINT")
    print("─" * 50)

    if registry.verify_voice_print(voice_print.print_id):
        print(f"  ✓ Voice print verified")
        print(f"  Fingerprint: {voice_print.fingerprint_hash[:16]}...")
    else:
        print("  ✗ Verification failed")

    # Enable protection
    print("\n" + "─" * 50)
    print("  ENABLING AI PROTECTION")
    print("─" * 50)

    if registry.enable_protection(voice_print.print_id):
        print(f"  ✓ AI protection enabled")
        print(f"  Status: {voice_print.status.value}")

    # Create profile
    print("\n" + "─" * 50)
    print("  CREATING VOICE PROFILE")
    print("─" * 50)

    profile = registry.create_profile(
        member_id="member_123",
        display_name="Marcus Williams"
    )
    profile.primary_capabilities = [
        VoiceCapability.BARITONE,
        VoiceCapability.AUTHORITATIVE,
        VoiceCapability.WARM,
        VoiceCapability.DRAMATIC
    ]
    profile.languages = ["English", "Spanish"]
    profile.hourly_rate = 350.0
    profile.available_for_work = True

    registry.link_voice_print(profile.profile_id, voice_print.print_id)

    print(f"  Profile: {profile.display_name}")
    print(f"  Capabilities: {', '.join(c.value for c in profile.primary_capabilities)}")
    print(f"  Protected: {profile.is_protected}")
    print(f"  Rate: ${profile.hourly_rate}/hr")

    # Stats
    print("\n" + "─" * 50)
    print("  REGISTRY STATISTICS")
    print("─" * 50)

    stats = registry.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print("Every voice is unique. Every voice is sovereign.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
