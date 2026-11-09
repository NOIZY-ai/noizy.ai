"""
NOIZY Fish — Voice Biometrics
==============================

Verify voice actors by their unique vocal signature.
Detect unauthorized voice cloning in the wild.

Features:
- Vocal fingerprint enrollment
- Voice verification (is this really them?)
- Clone detection (is this AI-generated?)
- Voice lineage tracking
- Liveness detection
- Cross-reference with AI model outputs

2056 VALUE: Your voice is your password. Clones can't hide.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
import hashlib
import json
import struct
import math


# ═══════════════════════════════════════════════════════════════════════════════
# Voice Characteristics
# ═══════════════════════════════════════════════════════════════════════════════

class VoiceType(Enum):
    """Voice classification."""
    SOPRANO = "soprano"
    MEZZO_SOPRANO = "mezzo_soprano"
    ALTO = "alto"
    COUNTERTENOR = "countertenor"
    TENOR = "tenor"
    BARITONE = "baritone"
    BASS = "bass"
    UNKNOWN = "unknown"


class VoiceQuality(Enum):
    """Voice quality characteristics."""
    BREATHY = "breathy"
    CLEAR = "clear"
    RASPY = "raspy"
    NASAL = "nasal"
    RESONANT = "resonant"
    HUSKY = "husky"
    SMOOTH = "smooth"
    GRAVELLY = "gravelly"


class DetectionResult(Enum):
    """Voice clone detection result."""
    AUTHENTIC = "authentic"          # Real human voice
    LIKELY_AUTHENTIC = "likely_authentic"
    UNCERTAIN = "uncertain"
    LIKELY_CLONE = "likely_clone"
    CLONE_DETECTED = "clone_detected"  # AI-generated


# ═══════════════════════════════════════════════════════════════════════════════
# Vocal Fingerprint
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VocalFingerprint:
    """
    Unique vocal signature derived from voice samples.

    This is like a voiceprint - unique to each person.
    """
    fingerprint_id: str = field(default_factory=lambda: str(uuid4()))

    # Owner
    creator_id: str = ""
    creator_name: str = ""

    # Acoustic features (normally extracted via ML)
    fundamental_frequency_mean: float = 0.0      # Average pitch (Hz)
    fundamental_frequency_std: float = 0.0       # Pitch variation
    formant_frequencies: list[float] = field(default_factory=list)  # F1, F2, F3, F4
    spectral_centroid: float = 0.0               # "Brightness"
    spectral_bandwidth: float = 0.0              # Frequency spread
    zero_crossing_rate: float = 0.0              # Voice "roughness"
    mfcc_coefficients: list[float] = field(default_factory=list)   # 13 MFCCs
    jitter: float = 0.0                          # Pitch irregularity
    shimmer: float = 0.0                         # Amplitude irregularity
    harmonics_to_noise: float = 0.0              # Voice clarity

    # Classification
    voice_type: VoiceType = VoiceType.UNKNOWN
    voice_qualities: list[VoiceQuality] = field(default_factory=list)

    # Embedding vector (for similarity comparison)
    embedding_vector: list[float] = field(default_factory=list)

    # Metadata
    sample_duration_seconds: float = 0.0
    sample_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def generate_hash(self) -> str:
        """Generate unique hash from acoustic features."""
        features = [
            self.fundamental_frequency_mean,
            self.spectral_centroid,
            *self.formant_frequencies[:4],
            *self.mfcc_coefficients[:6]
        ]
        data = struct.pack('>' + 'f' * len(features), *features)
        return hashlib.sha256(data).hexdigest()

    def similarity(self, other: 'VocalFingerprint') -> float:
        """
        Calculate similarity with another fingerprint.

        Returns 0-1 (1 = identical).
        """
        if not self.embedding_vector or not other.embedding_vector:
            # Fallback to feature comparison
            return self._feature_similarity(other)

        # Cosine similarity of embeddings
        dot = sum(a * b for a, b in zip(self.embedding_vector, other.embedding_vector))
        mag1 = math.sqrt(sum(a ** 2 for a in self.embedding_vector))
        mag2 = math.sqrt(sum(b ** 2 for b in other.embedding_vector))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return (dot / (mag1 * mag2) + 1) / 2  # Normalize to 0-1

    def _feature_similarity(self, other: 'VocalFingerprint') -> float:
        """Similarity based on acoustic features."""
        # Simple weighted comparison
        f0_sim = 1 - abs(self.fundamental_frequency_mean - other.fundamental_frequency_mean) / 300
        centroid_sim = 1 - abs(self.spectral_centroid - other.spectral_centroid) / 5000

        # MFCC similarity
        if self.mfcc_coefficients and other.mfcc_coefficients:
            mfcc_diff = sum(
                abs(a - b)
                for a, b in zip(self.mfcc_coefficients, other.mfcc_coefficients)
            ) / len(self.mfcc_coefficients)
            mfcc_sim = max(0, 1 - mfcc_diff / 50)
        else:
            mfcc_sim = 0.5

        return max(0, min(1, (f0_sim * 0.3 + centroid_sim * 0.3 + mfcc_sim * 0.4)))


# ═══════════════════════════════════════════════════════════════════════════════
# Voice Sample
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class VoiceSample:
    """A voice sample for enrollment or verification."""
    sample_id: str = field(default_factory=lambda: str(uuid4()))

    # Owner
    creator_id: str = ""

    # Audio metadata
    audio_hash: str = ""                 # Hash of audio content
    duration_seconds: float = 0.0
    sample_rate: int = 44100
    format: str = "wav"

    # Source
    source: str = ""                     # "enrollment", "verification", "detected"
    source_url: Optional[str] = None
    source_description: Optional[str] = None

    # Analysis
    is_analyzed: bool = False
    is_liveness_verified: bool = False   # Anti-spoofing check passed
    detection_result: DetectionResult = DetectionResult.UNCERTAIN
    clone_confidence: float = 0.0        # 0-1 probability of being a clone

    # Timestamps
    recorded_at: Optional[datetime] = None
    uploaded_at: datetime = field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# Clone Detection Report
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CloneDetectionReport:
    """Report from clone detection analysis."""
    report_id: str = field(default_factory=lambda: str(uuid4()))

    # Sample analyzed
    sample_id: str = ""
    sample_hash: str = ""

    # Results
    result: DetectionResult = DetectionResult.UNCERTAIN
    clone_probability: float = 0.0       # 0-1
    authentic_probability: float = 0.0   # 0-1

    # Evidence
    artifacts_detected: list[str] = field(default_factory=list)
    # e.g., "spectral_artifacts", "vocoder_patterns", "neural_network_signatures"

    suspected_source_model: Optional[str] = None  # Which AI model?

    # Matching
    matched_creator_id: Optional[str] = None
    matched_fingerprint_id: Optional[str] = None
    match_similarity: float = 0.0

    # Analysis details
    analysis_version: str = "1.0"
    analysis_timestamp: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# Voice Biometrics Engine
# ═══════════════════════════════════════════════════════════════════════════════

class VoiceBiometricsEngine:
    """
    Voice biometrics for creator verification and clone detection.

    Your voice is your identity.
    """

    # Thresholds
    VERIFICATION_THRESHOLD = 0.85       # Similarity needed for verification
    CLONE_DETECTION_THRESHOLD = 0.7     # Probability to flag as clone
    MATCH_THRESHOLD = 0.75              # Similarity for attribution

    def __init__(self):
        self.fingerprints: dict[str, VocalFingerprint] = {}
        self.samples: dict[str, VoiceSample] = {}
        self.reports: dict[str, CloneDetectionReport] = {}

    def enroll_voice(
        self,
        creator_id: str,
        creator_name: str,
        samples: list[VoiceSample]
    ) -> VocalFingerprint:
        """
        Enroll a creator's voice from samples.

        Creates a vocal fingerprint from the provided samples.
        """
        if len(samples) < 3:
            raise ValueError("Need at least 3 samples for enrollment")

        # Extract features from each sample (simulated)
        all_features = []
        for sample in samples:
            features = self._extract_features(sample)
            all_features.append(features)
            self.samples[sample.sample_id] = sample

        # Average features
        fingerprint = self._create_fingerprint(creator_id, creator_name, all_features)
        self.fingerprints[fingerprint.fingerprint_id] = fingerprint

        return fingerprint

    def _extract_features(self, sample: VoiceSample) -> dict:
        """
        Extract acoustic features from a sample.

        In production, this would use actual audio analysis.
        Here we simulate with deterministic values based on hash.
        """
        # Deterministic simulation based on audio hash
        h = int(hashlib.md5(sample.audio_hash.encode()).hexdigest(), 16)

        return {
            "f0_mean": 100 + (h % 200),
            "f0_std": 10 + (h % 30),
            "formants": [
                500 + ((h >> 4) % 400),
                1500 + ((h >> 8) % 800),
                2500 + ((h >> 12) % 600),
                3500 + ((h >> 16) % 500)
            ],
            "spectral_centroid": 1000 + ((h >> 20) % 3000),
            "mfcc": [(h >> (i * 4)) % 100 - 50 for i in range(13)],
            "jitter": (h % 100) / 1000,
            "shimmer": ((h >> 8) % 100) / 1000,
            "hnr": 10 + ((h >> 16) % 20)
        }

    def _create_fingerprint(
        self,
        creator_id: str,
        creator_name: str,
        features_list: list[dict]
    ) -> VocalFingerprint:
        """Create fingerprint by averaging extracted features."""
        n = len(features_list)

        # Average all features
        f0_mean = sum(f["f0_mean"] for f in features_list) / n
        f0_std = sum(f["f0_std"] for f in features_list) / n

        formants = []
        for i in range(4):
            formants.append(sum(f["formants"][i] for f in features_list) / n)

        centroid = sum(f["spectral_centroid"] for f in features_list) / n

        mfcc = []
        for i in range(13):
            mfcc.append(sum(f["mfcc"][i] for f in features_list) / n)

        jitter = sum(f["jitter"] for f in features_list) / n
        shimmer = sum(f["shimmer"] for f in features_list) / n
        hnr = sum(f["hnr"] for f in features_list) / n

        # Create embedding (simplified)
        embedding = [f0_mean / 300, centroid / 5000, *[m / 100 for m in mfcc[:8]]]

        # Classify voice type
        if f0_mean > 250:
            voice_type = VoiceType.SOPRANO
        elif f0_mean > 200:
            voice_type = VoiceType.ALTO
        elif f0_mean > 150:
            voice_type = VoiceType.TENOR
        elif f0_mean > 100:
            voice_type = VoiceType.BARITONE
        else:
            voice_type = VoiceType.BASS

        return VocalFingerprint(
            creator_id=creator_id,
            creator_name=creator_name,
            fundamental_frequency_mean=f0_mean,
            fundamental_frequency_std=f0_std,
            formant_frequencies=formants,
            spectral_centroid=centroid,
            mfcc_coefficients=mfcc,
            jitter=jitter,
            shimmer=shimmer,
            harmonics_to_noise=hnr,
            voice_type=voice_type,
            embedding_vector=embedding,
            sample_count=n
        )

    def verify_voice(
        self,
        creator_id: str,
        sample: VoiceSample
    ) -> dict:
        """
        Verify that a sample matches an enrolled creator.

        Returns: {verified: bool, similarity: float, details: dict}
        """
        # Get creator's fingerprint
        fingerprint = None
        for fp in self.fingerprints.values():
            if fp.creator_id == creator_id:
                fingerprint = fp
                break

        if not fingerprint:
            return {
                "verified": False,
                "error": "Creator not enrolled",
                "similarity": 0.0
            }

        # Extract features from sample
        features = self._extract_features(sample)

        # Create temporary fingerprint for comparison
        temp_fp = self._create_fingerprint(
            creator_id, "",
            [features]
        )

        # Calculate similarity
        similarity = fingerprint.similarity(temp_fp)

        verified = similarity >= self.VERIFICATION_THRESHOLD

        return {
            "verified": verified,
            "similarity": similarity,
            "threshold": self.VERIFICATION_THRESHOLD,
            "fingerprint_id": fingerprint.fingerprint_id,
            "voice_type_match": temp_fp.voice_type == fingerprint.voice_type
        }

    def detect_clone(
        self,
        sample: VoiceSample
    ) -> CloneDetectionReport:
        """
        Detect if a voice sample is AI-generated.

        Looks for telltale signs of synthetic speech.
        """
        features = self._extract_features(sample)

        # Simulated clone detection (in production: neural network classifier)
        # Look for artifacts that indicate AI generation

        artifacts = []
        clone_score = 0.0

        # Check for unnatural regularity
        if features["jitter"] < 0.002:
            artifacts.append("unnaturally_stable_pitch")
            clone_score += 0.2

        if features["shimmer"] < 0.002:
            artifacts.append("unnaturally_stable_amplitude")
            clone_score += 0.2

        # Check for spectral artifacts
        if features["hnr"] > 28:
            artifacts.append("suspiciously_clean_signal")
            clone_score += 0.15

        # Check for formant patterns (simplified)
        f1, f2 = features["formants"][0], features["formants"][1]
        if abs(f2 / f1 - 3.0) < 0.1:
            artifacts.append("robotic_formant_ratio")
            clone_score += 0.25

        # Determine result
        if clone_score >= 0.6:
            result = DetectionResult.CLONE_DETECTED
        elif clone_score >= 0.4:
            result = DetectionResult.LIKELY_CLONE
        elif clone_score >= 0.2:
            result = DetectionResult.UNCERTAIN
        elif clone_score >= 0.1:
            result = DetectionResult.LIKELY_AUTHENTIC
        else:
            result = DetectionResult.AUTHENTIC

        report = CloneDetectionReport(
            sample_id=sample.sample_id,
            sample_hash=sample.audio_hash,
            result=result,
            clone_probability=clone_score,
            authentic_probability=1 - clone_score,
            artifacts_detected=artifacts,
            confidence=0.85 if artifacts else 0.95
        )

        self.reports[report.report_id] = report
        return report

    def find_voice_match(
        self,
        sample: VoiceSample
    ) -> Optional[dict]:
        """
        Find whose voice this sample sounds like.

        For attribution: "Who does this sound like?"
        """
        features = self._extract_features(sample)
        temp_fp = self._create_fingerprint("unknown", "", [features])

        best_match = None
        best_similarity = 0.0

        for fp in self.fingerprints.values():
            similarity = fp.similarity(temp_fp)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = fp

        if best_match and best_similarity >= self.MATCH_THRESHOLD:
            return {
                "matched": True,
                "creator_id": best_match.creator_id,
                "creator_name": best_match.creator_name,
                "similarity": best_similarity,
                "fingerprint_id": best_match.fingerprint_id,
                "confidence": "high" if best_similarity > 0.9 else "medium"
            }

        return {
            "matched": False,
            "best_similarity": best_similarity,
            "message": "No confident match found"
        }

    def liveness_check(
        self,
        samples: list[VoiceSample],
        challenge_phrase: str
    ) -> dict:
        """
        Verify this is a live person, not a recording.

        Challenge-response with unpredictable phrases.
        """
        if len(samples) < 2:
            return {
                "passed": False,
                "error": "Need multiple samples for liveness"
            }

        # Check for variation between samples
        features_list = [self._extract_features(s) for s in samples]

        # Natural speech has variation
        f0_variation = max(f["f0_mean"] for f in features_list) - min(f["f0_mean"] for f in features_list)
        centroid_variation = max(f["spectral_centroid"] for f in features_list) - min(f["spectral_centroid"] for f in features_list)

        # Too similar = likely recording playback
        if f0_variation < 5 and centroid_variation < 50:
            return {
                "passed": False,
                "reason": "samples_too_similar",
                "message": "Suspected recording playback"
            }

        # Check for expected phrase patterns (simplified)
        # In production: speech recognition + challenge verification

        return {
            "passed": True,
            "f0_variation": f0_variation,
            "spectral_variation": centroid_variation,
            "message": "Liveness verified"
        }

    def get_enrolled_fingerprint(self, creator_id: str) -> Optional[VocalFingerprint]:
        """Get fingerprint for a creator."""
        for fp in self.fingerprints.values():
            if fp.creator_id == creator_id:
                return fp
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate voice biometrics."""
    print("\n" + "=" * 70)
    print("VOICE BIOMETRICS — DEMO")
    print("Your voice is your identity")
    print("=" * 70)

    engine = VoiceBiometricsEngine()

    # Enroll a voice actor
    print("\n" + "─" * 50)
    print("1. ENROLLING VOICE ACTOR")
    print("─" * 50)

    creator_id = "sarah-voice-001"
    enrollment_samples = [
        VoiceSample(creator_id=creator_id, audio_hash=f"sample_{i}_original_{creator_id}")
        for i in range(5)
    ]

    fingerprint = engine.enroll_voice(creator_id, "Sarah Voice", enrollment_samples)

    print(f"  Creator: Sarah Voice")
    print(f"  Fingerprint ID: {fingerprint.fingerprint_id}")
    print(f"  Voice type: {fingerprint.voice_type.value}")
    print(f"  Fundamental frequency: {fingerprint.fundamental_frequency_mean:.1f} Hz")
    print(f"  Samples used: {fingerprint.sample_count}")
    print(f"  Hash: {fingerprint.generate_hash()[:16]}...")

    # Enroll another voice actor
    creator_id_2 = "marcus-baritone-002"
    enrollment_samples_2 = [
        VoiceSample(creator_id=creator_id_2, audio_hash=f"sample_{i}_original_{creator_id_2}")
        for i in range(5)
    ]

    fingerprint_2 = engine.enroll_voice(creator_id_2, "Marcus Baritone", enrollment_samples_2)
    print(f"\n  Creator: Marcus Baritone")
    print(f"  Voice type: {fingerprint_2.voice_type.value}")
    print(f"  Fundamental frequency: {fingerprint_2.fundamental_frequency_mean:.1f} Hz")

    # Verify voice
    print("\n" + "─" * 50)
    print("2. VOICE VERIFICATION")
    print("─" * 50)

    # Sarah provides a new sample
    new_sample = VoiceSample(
        creator_id=creator_id,
        audio_hash="new_sample_from_sarah"
    )

    result = engine.verify_voice(creator_id, new_sample)
    print(f"\n  Verifying: Is this Sarah?")
    print(f"    Result: {'VERIFIED' if result['verified'] else 'NOT VERIFIED'}")
    print(f"    Similarity: {result['similarity']:.2%}")
    print(f"    Threshold: {result['threshold']:.2%}")

    # Someone else's sample
    impostor_sample = VoiceSample(
        creator_id=creator_id,
        audio_hash="totally_different_person_xyz"
    )

    result_impostor = engine.verify_voice(creator_id, impostor_sample)
    print(f"\n  Verifying: Is THIS Sarah?")
    print(f"    Result: {'VERIFIED' if result_impostor['verified'] else 'NOT VERIFIED'}")
    print(f"    Similarity: {result_impostor['similarity']:.2%}")

    # Clone detection
    print("\n" + "─" * 50)
    print("3. CLONE DETECTION")
    print("─" * 50)

    # Authentic voice sample
    authentic_sample = VoiceSample(
        audio_hash="authentic_human_voice_recording_2024"
    )
    report_auth = engine.detect_clone(authentic_sample)
    print(f"\n  Sample A (authentic):")
    print(f"    Result: {report_auth.result.value}")
    print(f"    Clone probability: {report_auth.clone_probability:.2%}")
    print(f"    Artifacts: {report_auth.artifacts_detected or 'None'}")

    # AI-generated sample (simulated with specific hash pattern)
    clone_sample = VoiceSample(
        audio_hash="ai_generated_too_perfect_very_clean"
    )
    report_clone = engine.detect_clone(clone_sample)
    print(f"\n  Sample B (AI-generated):")
    print(f"    Result: {report_clone.result.value}")
    print(f"    Clone probability: {report_clone.clone_probability:.2%}")
    print(f"    Artifacts: {report_clone.artifacts_detected}")

    # Voice matching
    print("\n" + "─" * 50)
    print("4. VOICE ATTRIBUTION")
    print("─" * 50)

    # Unknown sample that sounds like Sarah
    unknown_sample = VoiceSample(
        audio_hash="sample_1_original_sarah-voice-001"  # Similar hash pattern
    )

    match = engine.find_voice_match(unknown_sample)
    print(f"\n  Unknown sample - whose voice is this?")
    if match.get("matched"):
        print(f"    Match: {match['creator_name']}")
        print(f"    Similarity: {match['similarity']:.2%}")
        print(f"    Confidence: {match['confidence']}")
    else:
        print(f"    No confident match (best: {match['best_similarity']:.2%})")

    # Liveness check
    print("\n" + "─" * 50)
    print("5. LIVENESS VERIFICATION")
    print("─" * 50)

    # Live person reading challenge phrase
    live_samples = [
        VoiceSample(audio_hash=f"live_challenge_{i}_variation_{i*7}")
        for i in range(3)
    ]

    liveness = engine.liveness_check(live_samples, "The quick brown fox jumps over 42 lazy dogs")
    print(f"\n  Challenge phrase verification:")
    print(f"    Passed: {liveness['passed']}")
    print(f"    Message: {liveness['message']}")

    # Playback attack (same recording repeated)
    replay_samples = [
        VoiceSample(audio_hash="same_recording_replayed")
        for _ in range(3)
    ]

    replay_check = engine.liveness_check(replay_samples, "Random phrase 12345")
    print(f"\n  Replay attack detection:")
    print(f"    Passed: {replay_check['passed']}")
    print(f"    Reason: {replay_check.get('reason', 'N/A')}")
    print(f"    Message: {replay_check['message']}")

    print("\n" + "=" * 70)
    print("2056 VALUE: Voice clones can't hide. Creators stay protected.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
