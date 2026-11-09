"""
NOIZY Fish — Industry Standards Reference
==========================================

This module defines the standard identifiers used in the music industry
that NOIZY Fish integrates with.

References:
- ISRC: ISO 3901:2019 — International Standard Recording Code
- ISWC: ISO 15707:2022 — International Standard Musical Work Code
- IPI: Interested Parties Information (CISAC)
- ISNI: ISO 27729 — International Standard Name Identifier
- C2PA: Coalition for Content Provenance and Authenticity
- DDEX/RIN: Recording Information Notification

Sources:
- https://isrc.ifpi.org/
- https://www.iswc.org/
- https://www.cisac.org/services/information-services/ipi
- https://spec.c2pa.org/
- https://ddex.net/standards/recording-information-notification/
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# ISRC — International Standard Recording Code (ISO 3901:2019)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ISRC:
    """
    International Standard Recording Code.
    Uniquely identifies sound recordings and music videos.

    Format: CC-XXX-YY-NNNNN (12 characters)
    - CC: Country code (2 letters) — Note: In ISO 3901:2019, treated as prefix
    - XXX: Registrant code (3 alphanumeric)
    - YY: Year of reference (2 digits)
    - NNNNN: Designation code (5 digits)

    Example: US-S1Z-03-00001 (Sony Music, 2003, first track)
    """
    prefix: str          # 5 characters: CC + XXX (e.g., "USS1Z")
    year: str            # 2 digits (e.g., "03")
    designation: str     # 5 digits (e.g., "00001")

    @classmethod
    def parse(cls, isrc_string: str) -> "ISRC":
        """Parse an ISRC string (with or without dashes)."""
        # Remove dashes and spaces
        clean = re.sub(r'[-\s]', '', isrc_string.upper())

        if len(clean) != 12:
            raise ValueError(f"Invalid ISRC length: {len(clean)} (expected 12)")

        return cls(
            prefix=clean[:5],
            year=clean[5:7],
            designation=clean[7:12]
        )

    def __str__(self) -> str:
        """Format as standard ISRC with dashes."""
        return f"{self.prefix[:2]}-{self.prefix[2:]}-{self.year}-{self.designation}"

    @property
    def raw(self) -> str:
        """Return raw 12-character code."""
        return f"{self.prefix}{self.year}{self.designation}"

    def validate(self) -> bool:
        """Validate ISRC format."""
        if len(self.prefix) != 5:
            return False
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{3}$', self.prefix):
            return False
        if not re.match(r'^\d{2}$', self.year):
            return False
        if not re.match(r'^\d{5}$', self.designation):
            return False
        return True


# ═══════════════════════════════════════════════════════════════════════════
# ISWC — International Standard Musical Work Code (ISO 15707:2022)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ISWC:
    """
    International Standard Musical Work Code.
    Uniquely identifies musical works (compositions, not recordings).

    Format: T-NNNNNNNNN-C (11 characters + prefix T)
    - T: Prefix (always "T")
    - NNNNNNNNN: 9-digit work identifier
    - C: Check digit (1 digit)

    Example: T-000.000.001-0 (first ISWC ever — "Dancing Queen" by ABBA)

    Note: ISWC identifies the composition, not the recording.
    A single ISWC can have multiple ISRC recordings.
    """
    work_id: str         # 9 digits
    check_digit: str     # 1 digit

    @classmethod
    def parse(cls, iswc_string: str) -> "ISWC":
        """Parse an ISWC string."""
        # Remove prefix, dashes, dots, spaces
        clean = re.sub(r'^ISWC\s*', '', iswc_string, flags=re.IGNORECASE)
        clean = re.sub(r'^T[-.\s]*', '', clean)
        clean = re.sub(r'[-.\s]', '', clean)

        if len(clean) != 10:
            raise ValueError(f"Invalid ISWC length: {len(clean)} (expected 10)")

        return cls(
            work_id=clean[:9],
            check_digit=clean[9]
        )

    def __str__(self) -> str:
        """Format as standard ISWC."""
        return f"T-{self.work_id[:3]}.{self.work_id[3:6]}.{self.work_id[6:9]}-{self.check_digit}"

    @property
    def raw(self) -> str:
        """Return raw code without formatting."""
        return f"T{self.work_id}{self.check_digit}"

    def validate(self) -> bool:
        """Validate ISWC format and check digit."""
        if not re.match(r'^\d{9}$', self.work_id):
            return False
        if not re.match(r'^\d$', self.check_digit):
            return False
        # TODO: Implement actual check digit algorithm
        return True


# ═══════════════════════════════════════════════════════════════════════════
# IPI — Interested Parties Information (CISAC)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class IPI:
    """
    Interested Parties Information number.
    Uniquely identifies rights holders (composers, lyricists, publishers).

    Format: 11 digits
    - Assigned by CMOs (Collective Management Organizations)
    - Formerly known as CAE (Composer, Author and Publisher)

    Example: 00014107338

    Used by:
    - ASCAP, BMI, SESAC (US)
    - PRS (UK)
    - SACEM (France)
    - All CISAC member societies (120+ countries)
    """
    number: str          # 11 digits

    @classmethod
    def parse(cls, ipi_string: str) -> "IPI":
        """Parse an IPI string."""
        clean = re.sub(r'[-\s]', '', ipi_string)

        # Some systems prefix with "I-" or "IPI"
        clean = re.sub(r'^(IPI|I)[-\s]*', '', clean, flags=re.IGNORECASE)

        if len(clean) != 11:
            raise ValueError(f"Invalid IPI length: {len(clean)} (expected 11)")

        return cls(number=clean)

    def __str__(self) -> str:
        return self.number

    def validate(self) -> bool:
        """Validate IPI format."""
        return bool(re.match(r'^\d{11}$', self.number))


# ═══════════════════════════════════════════════════════════════════════════
# ISNI — International Standard Name Identifier (ISO 27729)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ISNI:
    """
    International Standard Name Identifier.
    Uniquely identifies public identities of contributors (people/organizations).

    Format: 16 digits (displayed as 4 groups of 4)
    - Assigned by ISNI International Agency

    Example: 0000 0001 2103 2683 (Taylor Swift)

    Used for:
    - Performers, producers, engineers
    - Organizations (labels, publishers)
    - Anyone contributing to creative works
    """
    number: str          # 16 characters (15 digits + check character)

    @classmethod
    def parse(cls, isni_string: str) -> "ISNI":
        """Parse an ISNI string."""
        clean = re.sub(r'[-\s]', '', isni_string.upper())
        clean = re.sub(r'^ISNI\s*', '', clean, flags=re.IGNORECASE)

        if len(clean) != 16:
            raise ValueError(f"Invalid ISNI length: {len(clean)} (expected 16)")

        return cls(number=clean)

    def __str__(self) -> str:
        """Format as standard ISNI with spaces."""
        return f"{self.number[:4]} {self.number[4:8]} {self.number[8:12]} {self.number[12:]}"

    def validate(self) -> bool:
        """Validate ISNI format."""
        return bool(re.match(r'^\d{15}[\dX]$', self.number))


# ═══════════════════════════════════════════════════════════════════════════
# DDEX Role Codes — From DDEX-AVS (Allowed Value Set)
# ═══════════════════════════════════════════════════════════════════════════

class ContributorRole(Enum):
    """
    Standard contributor roles from DDEX.
    Used in RIN (Recording Information Notification) messages.
    """
    # Performance roles
    ARTIST = "Artist"
    FEATURED_ARTIST = "FeaturedArtist"
    MAIN_ARTIST = "MainArtist"
    CONDUCTOR = "Conductor"
    ORCHESTRA = "Orchestra"
    ENSEMBLE = "Ensemble"
    SOLOIST = "Soloist"

    # Songwriting roles
    COMPOSER = "Composer"
    COMPOSER_LYRICIST = "ComposerLyricist"
    LYRICIST = "Lyricist"
    ARRANGER = "Arranger"
    ADAPTER = "Adapter"
    TRANSLATOR = "Translator"

    # Production roles
    PRODUCER = "Producer"
    EXECUTIVE_PRODUCER = "ExecutiveProducer"
    CO_PRODUCER = "CoProducer"
    MIXER = "Mixer"
    REMIXER = "Remixer"
    MASTERING_ENGINEER = "MasteringEngineer"
    RECORDING_ENGINEER = "RecordingEngineer"
    MIX_ENGINEER = "MixEngineer"
    ASSISTANT_ENGINEER = "AssistantEngineer"

    # Other roles
    PROGRAMMER = "Programmer"
    STUDIO_PERSONNEL = "StudioPersonnel"
    VOICE_ACTOR = "VoiceActor"
    NARRATOR = "Narrator"
    UNKNOWN = "Unknown"


class RightsType(Enum):
    """Types of rights in music."""
    MASTER = "master"                    # Sound recording rights
    PUBLISHING = "publishing"            # Composition/songwriting rights
    MECHANICAL = "mechanical"            # Reproduction rights
    PERFORMANCE = "performance"          # Public performance rights
    SYNC = "synchronization"             # Sync licensing rights
    NEIGHBORING = "neighboring"          # Performer/producer rights
    MORAL = "moral"                      # Moral rights (attribution, integrity)


class TerritoryCode(Enum):
    """
    ISO 3166-1 alpha-2 territory codes.
    Common territories for music licensing.
    """
    WORLDWIDE = "WW"
    UNITED_STATES = "US"
    UNITED_KINGDOM = "GB"
    CANADA = "CA"
    AUSTRALIA = "AU"
    GERMANY = "DE"
    FRANCE = "FR"
    JAPAN = "JP"
    BRAZIL = "BR"
    MEXICO = "MX"
    SPAIN = "ES"
    ITALY = "IT"
    NETHERLANDS = "NL"
    SWEDEN = "SE"
    SOUTH_KOREA = "KR"
    INDIA = "IN"
    CHINA = "CN"
    EUROPE = "EU"  # Not ISO but commonly used
    NORTH_AMERICA = "NA"  # Not ISO but commonly used


# ═══════════════════════════════════════════════════════════════════════════
# NOIZY Fish Identifier — Our native identifier
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class NoizyID:
    """
    NOIZY Fish native identifier.
    Links to external standards while providing our own addressing.

    Format: NZ-{type}-{timestamp}-{random}
    Types:
    - CR: Creator
    - WK: Work (composition)
    - REC: Recording
    - VOC: Voice asset
    - LIC: License
    - TXN: Transaction

    Example: NZ-CR-20260322-A1B2C3D4
    """
    id_type: str         # CR, WK, REC, VOC, LIC, TXN
    timestamp: str       # YYYYMMDD
    unique: str          # 8 alphanumeric

    # Linked external identifiers
    isrc: Optional[ISRC] = None
    iswc: Optional[ISWC] = None
    ipi: Optional[IPI] = None
    isni: Optional[ISNI] = None

    @classmethod
    def generate(cls, id_type: str) -> "NoizyID":
        """Generate a new NOIZY ID."""
        from datetime import datetime
        import secrets

        return cls(
            id_type=id_type.upper(),
            timestamp=datetime.utcnow().strftime("%Y%m%d"),
            unique=secrets.token_hex(4).upper()
        )

    def __str__(self) -> str:
        return f"NZ-{self.id_type}-{self.timestamp}-{self.unique}"

    def to_dict(self) -> dict:
        """Export with linked identifiers."""
        result = {
            "noizy_id": str(self),
            "type": self.id_type,
            "created": self.timestamp
        }
        if self.isrc:
            result["isrc"] = str(self.isrc)
        if self.iswc:
            result["iswc"] = str(self.iswc)
        if self.ipi:
            result["ipi"] = str(self.ipi)
        if self.isni:
            result["isni"] = str(self.isni)
        return result


# ═══════════════════════════════════════════════════════════════════════════
# Validation utilities
# ═══════════════════════════════════════════════════════════════════════════

def validate_all_identifiers(
    isrc: Optional[str] = None,
    iswc: Optional[str] = None,
    ipi: Optional[str] = None,
    isni: Optional[str] = None
) -> dict:
    """Validate all provided identifiers."""
    results = {}

    if isrc:
        try:
            parsed = ISRC.parse(isrc)
            results["isrc"] = {"valid": parsed.validate(), "parsed": str(parsed)}
        except ValueError as e:
            results["isrc"] = {"valid": False, "error": str(e)}

    if iswc:
        try:
            parsed = ISWC.parse(iswc)
            results["iswc"] = {"valid": parsed.validate(), "parsed": str(parsed)}
        except ValueError as e:
            results["iswc"] = {"valid": False, "error": str(e)}

    if ipi:
        try:
            parsed = IPI.parse(ipi)
            results["ipi"] = {"valid": parsed.validate(), "parsed": str(parsed)}
        except ValueError as e:
            results["ipi"] = {"valid": False, "error": str(e)}

    if isni:
        try:
            parsed = ISNI.parse(isni)
            results["isni"] = {"valid": parsed.validate(), "parsed": str(parsed)}
        except ValueError as e:
            results["isni"] = {"valid": False, "error": str(e)}

    return results
