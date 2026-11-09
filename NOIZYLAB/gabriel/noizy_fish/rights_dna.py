"""
NOIZY Fish — Rights DNA
========================

Unique genetic fingerprint for creative works.
Track lineage across samples, remixes, and derivatives.

Features:
- Content fingerprinting (audio, melody, lyrics)
- Derivative detection (sample, remix, cover)
- Lineage tracking (parent → child relationships)
- Rights inheritance (consent flows through derivatives)
- Conflict resolution (when rights collide)

2056 VALUE: Every sample traced. Every remix attributed. Every creator paid.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
import hashlib
import json
import math


# ═══════════════════════════════════════════════════════════════════════════════
# Work Types & Relationships
# ═══════════════════════════════════════════════════════════════════════════════

class WorkType(Enum):
    """Types of creative works."""
    MASTER_RECORDING = "master_recording"    # Full song recording
    COMPOSITION = "composition"               # Song/melody/structure
    LYRICS = "lyrics"                         # Written lyrics
    VOCAL_STEM = "vocal_stem"                # Isolated vocals
    INSTRUMENTAL_STEM = "instrumental_stem"   # Instrumental track
    SAMPLE = "sample"                         # Audio snippet
    BEAT = "beat"                            # Instrumental beat
    LOOP = "loop"                            # Repeatable loop
    SOUND_EFFECT = "sound_effect"            # SFX
    VOICE_RECORDING = "voice_recording"       # Voice acting
    VOICE_MODEL = "voice_model"              # Trained voice model


class DerivativeType(Enum):
    """How is one work derived from another?"""
    ORIGINAL = "original"           # No parent
    SAMPLE = "sample"               # Uses audio snippet
    REMIX = "remix"                 # Rearrangement/reimagining
    COVER = "cover"                 # New performance of composition
    INTERPOLATION = "interpolation" # Replays melody/hook
    MASHUP = "mashup"               # Combines multiple works
    STEM_EXTRACTION = "stem"        # Extracted from master
    AI_GENERATION = "ai_generation" # AI-generated from training
    VOICE_CLONE = "voice_clone"     # Voice model output


class RightsConflictType(Enum):
    """Types of rights conflicts."""
    NO_CONSENT = "no_consent"           # Used without permission
    TERMS_VIOLATION = "terms_violation"  # Violated license terms
    ATTRIBUTION_MISSING = "attribution"  # No credit given
    ROYALTY_DISPUTE = "royalty_dispute"  # Payment disagreement
    TERRITORY_VIOLATION = "territory"    # Used in restricted region
    AI_TRAINING_VIOLATION = "ai_training" # Used for AI without consent


# ═══════════════════════════════════════════════════════════════════════════════
# Content Fingerprint
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ContentFingerprint:
    """
    Multi-modal fingerprint of creative content.

    Like DNA - unique, heritable, detectable.
    """
    fingerprint_id: str = field(default_factory=lambda: str(uuid4()))

    # Work identification
    work_id: str = ""
    work_type: WorkType = WorkType.MASTER_RECORDING

    # Audio fingerprint (if applicable)
    audio_hash: str = ""                    # Hash of raw audio
    chromaprint: str = ""                   # AcoustID chromaprint
    spectral_hash: str = ""                 # Spectrogram hash
    beat_pattern: list[float] = field(default_factory=list)  # Rhythm signature

    # Melodic fingerprint
    melodic_contour: list[int] = field(default_factory=list)  # Up/down/same
    key_signature: str = ""
    tempo_bpm: float = 0.0
    time_signature: str = "4/4"

    # Lyric fingerprint (if applicable)
    lyric_hash: str = ""                    # Hash of normalized lyrics
    phonetic_signature: str = ""             # Sound pattern

    # Voice fingerprint (if applicable)
    vocal_fingerprint_id: Optional[str] = None

    # AI/model fingerprint
    training_signature: Optional[str] = None  # If AI-generated

    # Metadata
    duration_seconds: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

    def similarity(self, other: 'ContentFingerprint', mode: str = "audio") -> float:
        """
        Calculate similarity with another fingerprint.

        Modes: audio, melody, lyrics, overall
        """
        if mode == "audio":
            return self._audio_similarity(other)
        elif mode == "melody":
            return self._melodic_similarity(other)
        elif mode == "lyrics":
            return self._lyric_similarity(other)
        else:
            # Weighted combination
            audio_sim = self._audio_similarity(other)
            melody_sim = self._melodic_similarity(other)
            lyric_sim = self._lyric_similarity(other)
            return audio_sim * 0.4 + melody_sim * 0.4 + lyric_sim * 0.2

    def _audio_similarity(self, other: 'ContentFingerprint') -> float:
        """Compare audio fingerprints."""
        if self.chromaprint and other.chromaprint:
            # Count matching characters (simplified)
            matches = sum(
                1 for a, b in zip(self.chromaprint, other.chromaprint) if a == b
            )
            max_len = max(len(self.chromaprint), len(other.chromaprint))
            return matches / max_len if max_len > 0 else 0
        return 0.0

    def _melodic_similarity(self, other: 'ContentFingerprint') -> float:
        """Compare melodic contours."""
        if not self.melodic_contour or not other.melodic_contour:
            return 0.0

        # Find longest common subsequence
        m, n = len(self.melodic_contour), len(other.melodic_contour)
        if m == 0 or n == 0:
            return 0.0

        matches = sum(
            1 for a, b in zip(self.melodic_contour, other.melodic_contour) if a == b
        )
        return matches / max(m, n)

    def _lyric_similarity(self, other: 'ContentFingerprint') -> float:
        """Compare lyric fingerprints."""
        if self.lyric_hash and other.lyric_hash:
            if self.lyric_hash == other.lyric_hash:
                return 1.0
            # Could implement fuzzy matching here
        return 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# Rights DNA Record
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RightsDNA:
    """
    Complete rights record for a creative work.

    Tracks ownership, lineage, and consent requirements.
    """
    dna_id: str = field(default_factory=lambda: str(uuid4()))

    # Work info
    work_id: str = ""
    work_title: str = ""
    work_type: WorkType = WorkType.MASTER_RECORDING

    # Fingerprint
    fingerprint_id: str = ""

    # Ownership (can have multiple)
    rights_holders: list[dict] = field(default_factory=list)
    # Each: {"creator_id": str, "share": float, "role": str}

    # Lineage
    parent_dna_ids: list[str] = field(default_factory=list)
    derivative_type: DerivativeType = DerivativeType.ORIGINAL
    derivation_details: Optional[str] = None
    # e.g., "Samples 0:32-0:47 from parent"

    # Consent chain
    consent_inherited: bool = True
    consent_overrides: list[dict] = field(default_factory=list)
    # Can override specific rules from parents

    # Registration
    registered_at: datetime = field(default_factory=datetime.utcnow)
    registered_by: str = ""

    # Verification
    verified: bool = False
    verification_method: Optional[str] = None

    def get_total_lineage(self) -> list[str]:
        """Get all ancestor DNA IDs (full family tree)."""
        # This would be resolved recursively in practice
        return self.parent_dna_ids


@dataclass
class DerivativeRelation:
    """Link between a work and its derivative."""
    relation_id: str = field(default_factory=lambda: str(uuid4()))

    # Parent (source)
    parent_dna_id: str = ""
    parent_work_id: str = ""

    # Child (derivative)
    child_dna_id: str = ""
    child_work_id: str = ""

    # Relationship
    derivative_type: DerivativeType = DerivativeType.SAMPLE
    usage_description: str = ""

    # Consent
    consent_obtained: bool = False
    consent_id: Optional[str] = None
    license_id: Optional[str] = None

    # Detection
    detected_similarity: float = 0.0
    detection_method: str = ""  # "declared", "fingerprint", "ai_detection"

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# Rights Conflict
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class RightsConflict:
    """A detected conflict in rights/consent."""
    conflict_id: str = field(default_factory=lambda: str(uuid4()))

    # Works involved
    derivative_dna_id: str = ""
    source_dna_id: str = ""

    # Parties
    derivative_creator_id: str = ""
    source_creator_id: str = ""

    # Conflict details
    conflict_type: RightsConflictType = RightsConflictType.NO_CONSENT
    description: str = ""
    severity: str = "medium"  # low, medium, high, critical

    # Evidence
    similarity_score: float = 0.0
    detection_report: Optional[str] = None

    # Resolution
    status: str = "open"  # open, investigating, resolved, dismissed
    resolution: Optional[str] = None
    resolved_at: Optional[datetime] = None

    # Timestamps
    detected_at: datetime = field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# Rights DNA Engine
# ═══════════════════════════════════════════════════════════════════════════════

class RightsDNAEngine:
    """
    Track and trace creative rights across the entire ecosystem.

    Every sample, remix, and derivative — traced and attributed.
    """

    # Thresholds
    SAMPLE_DETECTION_THRESHOLD = 0.7
    COVER_DETECTION_THRESHOLD = 0.6
    AI_ATTRIBUTION_THRESHOLD = 0.5

    def __init__(self):
        self.fingerprints: dict[str, ContentFingerprint] = {}
        self.dna_records: dict[str, RightsDNA] = {}
        self.relations: dict[str, DerivativeRelation] = {}
        self.conflicts: dict[str, RightsConflict] = {}

    def register_work(
        self,
        work_id: str,
        work_title: str,
        work_type: WorkType,
        rights_holders: list[dict],
        audio_data: Optional[bytes] = None,
        lyrics: Optional[str] = None,
        parent_work_ids: list[str] = None,
        derivative_type: DerivativeType = DerivativeType.ORIGINAL
    ) -> RightsDNA:
        """
        Register a work and generate its Rights DNA.
        """
        # Generate fingerprint
        fingerprint = self._generate_fingerprint(
            work_id, work_type, audio_data, lyrics
        )
        self.fingerprints[fingerprint.fingerprint_id] = fingerprint

        # Get parent DNA IDs
        parent_dna_ids = []
        if parent_work_ids:
            for pid in parent_work_ids:
                for dna in self.dna_records.values():
                    if dna.work_id == pid:
                        parent_dna_ids.append(dna.dna_id)
                        break

        # Create DNA record
        dna = RightsDNA(
            work_id=work_id,
            work_title=work_title,
            work_type=work_type,
            fingerprint_id=fingerprint.fingerprint_id,
            rights_holders=rights_holders,
            parent_dna_ids=parent_dna_ids,
            derivative_type=derivative_type
        )

        self.dna_records[dna.dna_id] = dna

        # Create derivative relations
        if parent_dna_ids:
            for parent_id in parent_dna_ids:
                self._create_relation(parent_id, dna.dna_id, derivative_type)

        return dna

    def _generate_fingerprint(
        self,
        work_id: str,
        work_type: WorkType,
        audio_data: Optional[bytes],
        lyrics: Optional[str]
    ) -> ContentFingerprint:
        """Generate content fingerprint."""
        # In production, this would use actual audio analysis
        # Here we simulate with hashes

        fp = ContentFingerprint(
            work_id=work_id,
            work_type=work_type
        )

        # Audio fingerprint
        if audio_data:
            fp.audio_hash = hashlib.sha256(audio_data).hexdigest()
            # Simulated chromaprint
            fp.chromaprint = hashlib.md5(audio_data).hexdigest()
            # Simulated spectral hash
            fp.spectral_hash = hashlib.sha384(audio_data).hexdigest()[:32]
        else:
            # Use work_id as seed
            fp.audio_hash = hashlib.sha256(work_id.encode()).hexdigest()
            fp.chromaprint = hashlib.md5(work_id.encode()).hexdigest()

        # Simulated melodic contour
        h = int(fp.audio_hash[:8], 16)
        fp.melodic_contour = [(h >> i) % 3 - 1 for i in range(16)]

        # Lyric fingerprint
        if lyrics:
            normalized = lyrics.lower().replace(" ", "")
            fp.lyric_hash = hashlib.sha256(normalized.encode()).hexdigest()
            # Simple phonetic signature
            vowels = "aeiou"
            fp.phonetic_signature = "".join(
                c if c in vowels else "x"
                for c in normalized[:50]
            )

        return fp

    def _create_relation(
        self,
        parent_dna_id: str,
        child_dna_id: str,
        derivative_type: DerivativeType
    ) -> DerivativeRelation:
        """Create derivative relationship."""
        parent = self.dna_records.get(parent_dna_id)
        child = self.dna_records.get(child_dna_id)

        relation = DerivativeRelation(
            parent_dna_id=parent_dna_id,
            parent_work_id=parent.work_id if parent else "",
            child_dna_id=child_dna_id,
            child_work_id=child.work_id if child else "",
            derivative_type=derivative_type,
            detection_method="declared"
        )

        self.relations[relation.relation_id] = relation
        return relation

    def detect_derivatives(
        self,
        work_id: str
    ) -> list[dict]:
        """
        Find all derivatives of a work (samples, remixes, etc).
        """
        source_dna = None
        for dna in self.dna_records.values():
            if dna.work_id == work_id:
                source_dna = dna
                break

        if not source_dna:
            return []

        source_fp = self.fingerprints.get(source_dna.fingerprint_id)
        if not source_fp:
            return []

        derivatives = []

        for dna in self.dna_records.values():
            if dna.work_id == work_id:
                continue

            other_fp = self.fingerprints.get(dna.fingerprint_id)
            if not other_fp:
                continue

            # Check audio similarity
            audio_sim = source_fp.similarity(other_fp, "audio")
            melody_sim = source_fp.similarity(other_fp, "melody")

            if audio_sim > self.SAMPLE_DETECTION_THRESHOLD:
                derivatives.append({
                    "work_id": dna.work_id,
                    "work_title": dna.work_title,
                    "dna_id": dna.dna_id,
                    "likely_type": "sample",
                    "audio_similarity": audio_sim,
                    "declared": source_dna.dna_id in dna.parent_dna_ids
                })
            elif melody_sim > self.COVER_DETECTION_THRESHOLD:
                derivatives.append({
                    "work_id": dna.work_id,
                    "work_title": dna.work_title,
                    "dna_id": dna.dna_id,
                    "likely_type": "cover_or_interpolation",
                    "melody_similarity": melody_sim,
                    "declared": source_dna.dna_id in dna.parent_dna_ids
                })

        return derivatives

    def detect_sources(
        self,
        work_id: str
    ) -> list[dict]:
        """
        Find what sources a work likely sampled/used.
        """
        target_dna = None
        for dna in self.dna_records.values():
            if dna.work_id == work_id:
                target_dna = dna
                break

        if not target_dna:
            return []

        target_fp = self.fingerprints.get(target_dna.fingerprint_id)
        if not target_fp:
            return []

        sources = []

        for dna in self.dna_records.values():
            if dna.work_id == work_id:
                continue

            other_fp = self.fingerprints.get(dna.fingerprint_id)
            if not other_fp:
                continue

            audio_sim = target_fp.similarity(other_fp, "audio")
            melody_sim = target_fp.similarity(other_fp, "melody")

            if audio_sim > self.SAMPLE_DETECTION_THRESHOLD:
                sources.append({
                    "work_id": dna.work_id,
                    "work_title": dna.work_title,
                    "dna_id": dna.dna_id,
                    "likely_relationship": "sampled_from",
                    "audio_similarity": audio_sim,
                    "rights_holders": dna.rights_holders,
                    "declared": dna.dna_id in target_dna.parent_dna_ids
                })

        return sources

    def check_rights_chain(
        self,
        work_id: str,
        use_category: str
    ) -> dict:
        """
        Check if consent exists through the entire rights chain.

        Returns whether ALL ancestor works have given consent.
        """
        dna = None
        for d in self.dna_records.values():
            if d.work_id == work_id:
                dna = d
                break

        if not dna:
            return {"valid": False, "error": "Work not found"}

        if dna.derivative_type == DerivativeType.ORIGINAL:
            return {
                "valid": True,
                "chain": [{"work_id": work_id, "status": "original"}],
                "message": "Original work - no inherited consent needed"
            }

        # Check each parent
        chain = []
        all_consented = True
        missing_consent = []

        def check_parents(current_dna: RightsDNA, depth: int = 0):
            nonlocal all_consented

            for parent_id in current_dna.parent_dna_ids:
                parent = self.dna_records.get(parent_id)
                if not parent:
                    continue

                # Check if relation has consent
                has_consent = False
                for rel in self.relations.values():
                    if rel.parent_dna_id == parent_id and rel.child_dna_id == current_dna.dna_id:
                        has_consent = rel.consent_obtained
                        break

                chain.append({
                    "work_id": parent.work_id,
                    "work_title": parent.work_title,
                    "depth": depth,
                    "consent_obtained": has_consent
                })

                if not has_consent:
                    all_consented = False
                    missing_consent.append(parent.work_title)

                # Recurse
                if depth < 10:  # Prevent infinite loops
                    check_parents(parent, depth + 1)

        check_parents(dna)

        return {
            "valid": all_consented,
            "chain": chain,
            "chain_length": len(chain),
            "missing_consent": missing_consent,
            "message": "All consents obtained" if all_consented else f"Missing consent from: {', '.join(missing_consent)}"
        }

    def flag_conflict(
        self,
        derivative_work_id: str,
        source_work_id: str,
        conflict_type: RightsConflictType,
        description: str
    ) -> RightsConflict:
        """Flag a rights conflict."""
        derivative_dna = None
        source_dna = None

        for dna in self.dna_records.values():
            if dna.work_id == derivative_work_id:
                derivative_dna = dna
            if dna.work_id == source_work_id:
                source_dna = dna

        conflict = RightsConflict(
            derivative_dna_id=derivative_dna.dna_id if derivative_dna else "",
            source_dna_id=source_dna.dna_id if source_dna else "",
            derivative_creator_id=derivative_dna.rights_holders[0]["creator_id"] if derivative_dna and derivative_dna.rights_holders else "",
            source_creator_id=source_dna.rights_holders[0]["creator_id"] if source_dna and source_dna.rights_holders else "",
            conflict_type=conflict_type,
            description=description
        )

        self.conflicts[conflict.conflict_id] = conflict
        return conflict

    def get_work_lineage(self, work_id: str) -> dict:
        """Get complete lineage tree for a work."""
        dna = None
        for d in self.dna_records.values():
            if d.work_id == work_id:
                dna = d
                break

        if not dna:
            return {"error": "Work not found"}

        # Build family tree
        ancestors = []
        descendants = []

        def find_ancestors(current_dna: RightsDNA, depth: int = 0):
            for parent_id in current_dna.parent_dna_ids:
                parent = self.dna_records.get(parent_id)
                if parent:
                    ancestors.append({
                        "work_id": parent.work_id,
                        "work_title": parent.work_title,
                        "derivative_type": current_dna.derivative_type.value,
                        "depth": depth
                    })
                    if depth < 10:
                        find_ancestors(parent, depth + 1)

        def find_descendants(current_dna: RightsDNA, depth: int = 0):
            for d in self.dna_records.values():
                if current_dna.dna_id in d.parent_dna_ids:
                    descendants.append({
                        "work_id": d.work_id,
                        "work_title": d.work_title,
                        "derivative_type": d.derivative_type.value,
                        "depth": depth
                    })
                    if depth < 10:
                        find_descendants(d, depth + 1)

        find_ancestors(dna)
        find_descendants(dna)

        return {
            "work_id": work_id,
            "work_title": dna.work_title,
            "derivative_type": dna.derivative_type.value,
            "ancestors": ancestors,
            "descendants": descendants,
            "total_lineage_size": len(ancestors) + len(descendants) + 1
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate Rights DNA."""
    print("\n" + "=" * 70)
    print("RIGHTS DNA — DEMO")
    print("Track creative lineage across the ecosystem")
    print("=" * 70)

    engine = RightsDNAEngine()

    # Register original works
    print("\n" + "─" * 50)
    print("1. REGISTERING ORIGINAL WORKS")
    print("─" * 50)

    # Classic funk track
    funk_original = engine.register_work(
        work_id="funk-classic-1975",
        work_title="Funky Groove Original",
        work_type=WorkType.MASTER_RECORDING,
        rights_holders=[
            {"creator_id": "james-funk-001", "share": 0.5, "role": "composer"},
            {"creator_id": "soul-records", "share": 0.5, "role": "label"}
        ],
        audio_data=b"funk_groove_audio_data_here",
        lyrics="Get up, get down, feel the funk around"
    )
    print(f"  Registered: {funk_original.work_title}")
    print(f"    DNA ID: {funk_original.dna_id}")
    print(f"    Type: {funk_original.derivative_type.value}")

    # Another original
    soul_original = engine.register_work(
        work_id="soul-ballad-1980",
        work_title="Soul Ballad",
        work_type=WorkType.MASTER_RECORDING,
        rights_holders=[
            {"creator_id": "sarah-soul-002", "share": 1.0, "role": "artist"}
        ],
        audio_data=b"soul_ballad_audio",
        lyrics="My heart sings for you"
    )
    print(f"  Registered: {soul_original.work_title}")

    # Register derivative works
    print("\n" + "─" * 50)
    print("2. REGISTERING DERIVATIVES")
    print("─" * 50)

    # Hip-hop sample
    hiphop_sample = engine.register_work(
        work_id="hiphop-banger-2020",
        work_title="Hip-Hop Banger (samples Funky Groove)",
        work_type=WorkType.MASTER_RECORDING,
        rights_holders=[
            {"creator_id": "mc-fire-003", "share": 0.6, "role": "artist"},
            {"creator_id": "beat-maker-004", "share": 0.4, "role": "producer"}
        ],
        audio_data=b"hiphop_with_funk_sample",
        parent_work_ids=["funk-classic-1975"],
        derivative_type=DerivativeType.SAMPLE
    )
    print(f"  Registered: {hiphop_sample.work_title}")
    print(f"    Derivative of: Funky Groove Original")
    print(f"    Type: {hiphop_sample.derivative_type.value}")

    # Remix
    remix = engine.register_work(
        work_id="remix-2023",
        work_title="Hip-Hop Banger (EDM Remix)",
        work_type=WorkType.MASTER_RECORDING,
        rights_holders=[
            {"creator_id": "dj-electron-005", "share": 0.4, "role": "remixer"},
            {"creator_id": "mc-fire-003", "share": 0.6, "role": "original_artist"}
        ],
        audio_data=b"edm_remix_audio",
        parent_work_ids=["hiphop-banger-2020"],
        derivative_type=DerivativeType.REMIX
    )
    print(f"  Registered: {remix.work_title}")
    print(f"    Derivative of: Hip-Hop Banger")

    # AI-generated track
    ai_generated = engine.register_work(
        work_id="ai-track-2024",
        work_title="AI Generated Soul-ish Track",
        work_type=WorkType.MASTER_RECORDING,
        rights_holders=[
            {"creator_id": "ai-music-corp", "share": 1.0, "role": "generator"}
        ],
        audio_data=b"ai_generated_soul_like_audio",
        parent_work_ids=["soul-ballad-1980"],  # Trained on this
        derivative_type=DerivativeType.AI_GENERATION
    )
    print(f"  Registered: {ai_generated.work_title}")
    print(f"    AI-generated from: Soul Ballad")

    # Check lineage
    print("\n" + "─" * 50)
    print("3. WORK LINEAGE")
    print("─" * 50)

    lineage = engine.get_work_lineage("remix-2023")
    print(f"\n  Lineage of: {lineage['work_title']}")
    print(f"  Ancestors:")
    for a in lineage["ancestors"]:
        indent = "    " * (a["depth"] + 1)
        print(f"{indent}└── {a['work_title']} ({a['derivative_type']})")
    print(f"  Total lineage size: {lineage['total_lineage_size']}")

    # Check rights chain
    print("\n" + "─" * 50)
    print("4. RIGHTS CHAIN VALIDATION")
    print("─" * 50)

    # Without consent
    chain_result = engine.check_rights_chain("remix-2023", "streaming")
    print(f"\n  Checking rights chain for: EDM Remix")
    print(f"    Valid: {chain_result['valid']}")
    print(f"    Chain length: {chain_result['chain_length']}")
    print(f"    Message: {chain_result['message']}")

    # Grant consent in the chain
    print("\n  Granting consent in chain...")
    for rel in engine.relations.values():
        if rel.child_work_id == "hiphop-banger-2020":
            rel.consent_obtained = True
            rel.consent_id = "consent-funk-sample-001"
            print(f"    Granted: {rel.parent_work_id} → {rel.child_work_id}")

    for rel in engine.relations.values():
        if rel.child_work_id == "remix-2023":
            rel.consent_obtained = True
            rel.consent_id = "consent-remix-001"
            print(f"    Granted: {rel.parent_work_id} → {rel.child_work_id}")

    # Re-check
    chain_result_2 = engine.check_rights_chain("remix-2023", "streaming")
    print(f"\n  Re-checking rights chain:")
    print(f"    Valid: {chain_result_2['valid']}")
    print(f"    Message: {chain_result_2['message']}")

    # Flag a conflict
    print("\n" + "─" * 50)
    print("5. RIGHTS CONFLICT DETECTION")
    print("─" * 50)

    conflict = engine.flag_conflict(
        derivative_work_id="ai-track-2024",
        source_work_id="soul-ballad-1980",
        conflict_type=RightsConflictType.AI_TRAINING_VIOLATION,
        description="AI model trained on Soul Ballad without consent"
    )
    print(f"\n  Conflict flagged:")
    print(f"    Type: {conflict.conflict_type.value}")
    print(f"    Description: {conflict.description}")
    print(f"    Status: {conflict.status}")

    print("\n" + "=" * 70)
    print("2056 VALUE: Every sample traced. Every creator attributed.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
