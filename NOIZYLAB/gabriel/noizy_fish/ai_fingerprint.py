"""
NOIZY Fish — AI Model Fingerprinting
=====================================

Track which AI models have accessed creator content.
Know exactly where your voice, music, or likeness ends up.

Features:
- Model registry with capability tracking
- Training data attestations
- Output attribution detection
- Model lineage tracking (fine-tunes inherit parent attestations)
- Audit trail of all AI interactions

2056 VALUE: Every creator knows which AIs learned from them.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
import hashlib
import json


# ═══════════════════════════════════════════════════════════════════════════════
# AI Model Types & Capabilities
# ═══════════════════════════════════════════════════════════════════════════════

class AICapability(Enum):
    """What can this AI do with creator content?"""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    AUDIO_GENERATION = "audio_generation"
    VIDEO_GENERATION = "video_generation"
    VOICE_SYNTHESIS = "voice_synthesis"
    VOICE_CLONING = "voice_cloning"
    MUSIC_GENERATION = "music_generation"
    STYLE_TRANSFER = "style_transfer"
    EMBEDDING = "embedding"
    CLASSIFICATION = "classification"
    TRANSCRIPTION = "transcription"
    TRANSLATION = "translation"


class ModelType(Enum):
    """AI model architecture types."""
    FOUNDATION = "foundation"           # Base model (GPT, Claude, etc.)
    FINE_TUNED = "fine_tuned"          # Fine-tuned from foundation
    LORA = "lora"                      # LoRA adapter
    MERGED = "merged"                  # Multiple models merged
    DISTILLED = "distilled"            # Knowledge distillation
    CUSTOM = "custom"                  # Custom architecture


class TrainingStatus(Enum):
    """Status of training data usage."""
    DECLARED = "declared"              # Model declares it used the content
    DETECTED = "detected"              # Fingerprint detected in outputs
    SUSPECTED = "suspected"            # High probability based on patterns
    CLEARED = "cleared"                # Verified NOT trained on content
    UNKNOWN = "unknown"                # No information


# ═══════════════════════════════════════════════════════════════════════════════
# AI Model Identity
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AIModelIdentity:
    """Unique identity for an AI model."""
    model_id: str = field(default_factory=lambda: str(uuid4()))

    # Model info
    name: str = ""
    version: str = ""
    provider: str = ""                  # Company/org that created it
    model_type: ModelType = ModelType.FOUNDATION

    # Capabilities
    capabilities: list[AICapability] = field(default_factory=list)

    # Lineage (for fine-tunes)
    parent_model_id: Optional[str] = None
    training_cutoff: Optional[datetime] = None

    # Identifiers
    model_hash: Optional[str] = None    # Hash of model weights (if available)
    api_endpoint: Optional[str] = None  # API URL for detection

    # Registration
    registered_at: datetime = field(default_factory=datetime.utcnow)
    verified: bool = False

    def generate_fingerprint(self) -> str:
        """Generate unique fingerprint for this model."""
        data = f"{self.name}:{self.version}:{self.provider}:{self.model_hash or ''}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]


# ═══════════════════════════════════════════════════════════════════════════════
# Training Data Attestation
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TrainingAttestation:
    """
    Attestation that a model was/wasn't trained on specific content.

    This is the key record: "Model X used Creator Y's content for training"
    """
    attestation_id: str = field(default_factory=lambda: str(uuid4()))

    # What model?
    model_id: str = ""
    model_name: str = ""

    # What content?
    creator_id: str = ""
    work_id: Optional[str] = None       # Specific work, or None for all works
    content_type: str = ""              # "voice", "music", "lyrics", etc.

    # Training details
    status: TrainingStatus = TrainingStatus.UNKNOWN
    training_date: Optional[datetime] = None
    training_samples: Optional[int] = None  # How many samples used
    training_hours: Optional[float] = None  # Hours of audio/video

    # Consent & compensation
    consent_given: bool = False
    consent_id: Optional[str] = None    # Link to consent record
    compensation_paid: bool = False
    compensation_amount: Optional[float] = None

    # Evidence
    detection_method: Optional[str] = None  # How was this discovered?
    confidence_score: float = 0.0       # 0-1 confidence in attestation
    evidence_hash: Optional[str] = None # Hash of evidence data

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# Output Attribution
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class OutputAttribution:
    """
    Attribution of AI-generated output to training sources.

    "This AI-generated song has 73% similarity to Creator X's style"
    """
    attribution_id: str = field(default_factory=lambda: str(uuid4()))

    # The AI output
    output_hash: str = ""               # Hash of the generated content
    output_type: str = ""               # "audio", "voice", "music", etc.
    model_id: str = ""
    generation_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Attributed creators
    attributed_creators: list[dict] = field(default_factory=list)
    # Each: {"creator_id": str, "confidence": float, "contribution_type": str}

    # Analysis
    style_similarity: float = 0.0       # Overall style match (0-1)
    vocal_similarity: float = 0.0       # Voice similarity (0-1)
    melodic_similarity: float = 0.0     # Melody similarity (0-1)

    # Royalty implications
    royalty_triggered: bool = False
    royalty_amount: Optional[float] = None


# ═══════════════════════════════════════════════════════════════════════════════
# AI Fingerprint Registry
# ═══════════════════════════════════════════════════════════════════════════════

class AIFingerprintRegistry:
    """
    Registry of AI models and their training data attestations.

    The goal: Complete transparency about AI training sources.
    """

    def __init__(self, db=None):
        self.db = db
        self.models: dict[str, AIModelIdentity] = {}
        self.attestations: dict[str, TrainingAttestation] = {}
        self.attributions: dict[str, OutputAttribution] = {}

    def register_model(self, model: AIModelIdentity) -> str:
        """Register an AI model in the fingerprint registry."""
        model.registered_at = datetime.utcnow()
        self.models[model.model_id] = model

        # If this is a fine-tune, inherit parent attestations
        if model.parent_model_id and model.parent_model_id in self.models:
            self._inherit_attestations(model.model_id, model.parent_model_id)

        return model.model_id

    def _inherit_attestations(self, child_id: str, parent_id: str):
        """Fine-tuned models inherit their parent's training attestations."""
        for att in self.attestations.values():
            if att.model_id == parent_id:
                # Create inherited attestation
                inherited = TrainingAttestation(
                    model_id=child_id,
                    model_name=self.models[child_id].name,
                    creator_id=att.creator_id,
                    work_id=att.work_id,
                    content_type=att.content_type,
                    status=att.status,
                    training_date=att.training_date,
                    consent_given=att.consent_given,
                    consent_id=att.consent_id,
                    detection_method="inherited_from_parent",
                    confidence_score=att.confidence_score * 0.95  # Slight decay
                )
                self.attestations[inherited.attestation_id] = inherited

    def attest_training(
        self,
        model_id: str,
        creator_id: str,
        status: TrainingStatus,
        work_id: Optional[str] = None,
        content_type: str = "unknown",
        consent_given: bool = False,
        consent_id: Optional[str] = None,
        samples: Optional[int] = None,
        hours: Optional[float] = None,
        confidence: float = 1.0
    ) -> TrainingAttestation:
        """
        Create attestation that a model used creator content.

        Can be self-reported by model provider or detected.
        """
        model = self.models.get(model_id)

        attestation = TrainingAttestation(
            model_id=model_id,
            model_name=model.name if model else "Unknown",
            creator_id=creator_id,
            work_id=work_id,
            content_type=content_type,
            status=status,
            consent_given=consent_given,
            consent_id=consent_id,
            training_samples=samples,
            training_hours=hours,
            confidence_score=confidence
        )

        self.attestations[attestation.attestation_id] = attestation
        return attestation

    def detect_attribution(
        self,
        output_hash: str,
        output_type: str,
        model_id: str,
        analysis_results: dict
    ) -> OutputAttribution:
        """
        Record attribution analysis of AI-generated content.

        analysis_results should contain:
        - attributed_creators: list of {creator_id, confidence, contribution_type}
        - style_similarity, vocal_similarity, melodic_similarity
        """
        attribution = OutputAttribution(
            output_hash=output_hash,
            output_type=output_type,
            model_id=model_id,
            attributed_creators=analysis_results.get("attributed_creators", []),
            style_similarity=analysis_results.get("style_similarity", 0),
            vocal_similarity=analysis_results.get("vocal_similarity", 0),
            melodic_similarity=analysis_results.get("melodic_similarity", 0)
        )

        # Check if royalties are triggered (any creator >50% confidence)
        for creator in attribution.attributed_creators:
            if creator.get("confidence", 0) > 0.5:
                attribution.royalty_triggered = True
                break

        self.attributions[attribution.attribution_id] = attribution
        return attribution

    def get_creator_exposure(self, creator_id: str) -> dict:
        """
        Get complete AI exposure report for a creator.

        Returns: All models that used their content, with details.
        """
        attestations = [
            a for a in self.attestations.values()
            if a.creator_id == creator_id
        ]

        attributions = [
            a for a in self.attributions.values()
            if any(c.get("creator_id") == creator_id for c in a.attributed_creators)
        ]

        # Group by model
        by_model = {}
        for att in attestations:
            if att.model_id not in by_model:
                model = self.models.get(att.model_id)
                by_model[att.model_id] = {
                    "model_id": att.model_id,
                    "model_name": att.model_name,
                    "provider": model.provider if model else "Unknown",
                    "capabilities": [c.value for c in model.capabilities] if model else [],
                    "attestations": [],
                    "total_samples": 0,
                    "total_hours": 0,
                    "consented": True,
                    "compensated": True
                }

            by_model[att.model_id]["attestations"].append({
                "status": att.status.value,
                "content_type": att.content_type,
                "samples": att.training_samples,
                "hours": att.training_hours,
                "consent_given": att.consent_given,
                "compensation_paid": att.compensation_paid
            })

            if att.training_samples:
                by_model[att.model_id]["total_samples"] += att.training_samples
            if att.training_hours:
                by_model[att.model_id]["total_hours"] += att.training_hours
            if not att.consent_given:
                by_model[att.model_id]["consented"] = False
            if not att.compensation_paid:
                by_model[att.model_id]["compensated"] = False

        return {
            "creator_id": creator_id,
            "total_models": len(by_model),
            "total_attestations": len(attestations),
            "total_attributions": len(attributions),
            "models": list(by_model.values()),
            "unconsented_usage": sum(
                1 for m in by_model.values() if not m["consented"]
            ),
            "uncompensated_usage": sum(
                1 for m in by_model.values() if not m["compensated"]
            )
        }

    def get_model_sources(self, model_id: str) -> dict:
        """
        Get all training sources for a model.

        For transparency: "What creators did this model learn from?"
        """
        model = self.models.get(model_id)
        attestations = [
            a for a in self.attestations.values()
            if a.model_id == model_id
        ]

        # Group by creator
        by_creator = {}
        for att in attestations:
            if att.creator_id not in by_creator:
                by_creator[att.creator_id] = {
                    "creator_id": att.creator_id,
                    "content_types": set(),
                    "total_samples": 0,
                    "total_hours": 0,
                    "consented": True,
                    "compensated": True
                }

            by_creator[att.creator_id]["content_types"].add(att.content_type)
            if att.training_samples:
                by_creator[att.creator_id]["total_samples"] += att.training_samples
            if att.training_hours:
                by_creator[att.creator_id]["total_hours"] += att.training_hours
            if not att.consent_given:
                by_creator[att.creator_id]["consented"] = False
            if not att.compensation_paid:
                by_creator[att.creator_id]["compensated"] = False

        # Convert sets to lists
        for c in by_creator.values():
            c["content_types"] = list(c["content_types"])

        return {
            "model_id": model_id,
            "model_name": model.name if model else "Unknown",
            "provider": model.provider if model else "Unknown",
            "total_creators": len(by_creator),
            "creators": list(by_creator.values()),
            "fully_consented": all(c["consented"] for c in by_creator.values()),
            "fully_compensated": all(c["compensated"] for c in by_creator.values())
        }

    def verify_clean_model(self, model_id: str, creator_id: str) -> dict:
        """
        Verify a model is "clean" — not trained on a specific creator's content.

        Useful for: "Can I use this AI without infringing on Creator X?"
        """
        attestations = [
            a for a in self.attestations.values()
            if a.model_id == model_id and a.creator_id == creator_id
        ]

        if not attestations:
            return {
                "verified_clean": None,  # Unknown
                "status": "no_data",
                "message": "No training data information available for this model/creator combination"
            }

        # Check for any usage
        for att in attestations:
            if att.status in [TrainingStatus.DECLARED, TrainingStatus.DETECTED]:
                return {
                    "verified_clean": False,
                    "status": "trained_on_content",
                    "message": f"Model was trained on this creator's content ({att.status.value})",
                    "consent_given": att.consent_given,
                    "compensation_paid": att.compensation_paid
                }
            elif att.status == TrainingStatus.SUSPECTED:
                return {
                    "verified_clean": False,
                    "status": "suspected",
                    "message": "High probability model was trained on this creator's content",
                    "confidence": att.confidence_score
                }

        # Check for explicit clearance
        cleared = [a for a in attestations if a.status == TrainingStatus.CLEARED]
        if cleared:
            return {
                "verified_clean": True,
                "status": "cleared",
                "message": "Model verified NOT trained on this creator's content",
                "verified_at": cleared[0].verified_at.isoformat() if cleared[0].verified_at else None
            }

        return {
            "verified_clean": None,
            "status": "unknown",
            "message": "Training status unknown"
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate AI fingerprinting."""
    print("\n" + "=" * 70)
    print("AI MODEL FINGERPRINTING — DEMO")
    print("Know exactly which AIs learned from your creative work")
    print("=" * 70)

    registry = AIFingerprintRegistry()

    # Register some AI models
    print("\n" + "─" * 50)
    print("1. REGISTERING AI MODELS")
    print("─" * 50)

    # Foundation model
    gpt5 = AIModelIdentity(
        name="GPT-5",
        version="5.0",
        provider="OpenAI",
        model_type=ModelType.FOUNDATION,
        capabilities=[
            AICapability.TEXT_GENERATION,
            AICapability.AUDIO_GENERATION,
            AICapability.VOICE_SYNTHESIS
        ],
        training_cutoff=datetime(2025, 6, 1)
    )
    registry.register_model(gpt5)
    print(f"  Registered: {gpt5.name} ({gpt5.provider})")
    print(f"    Capabilities: {[c.value for c in gpt5.capabilities]}")

    # Voice cloning model
    voice_ai = AIModelIdentity(
        name="VoiceForge Pro",
        version="3.0",
        provider="VoiceTech Inc",
        model_type=ModelType.FOUNDATION,
        capabilities=[
            AICapability.VOICE_CLONING,
            AICapability.VOICE_SYNTHESIS
        ]
    )
    registry.register_model(voice_ai)
    print(f"  Registered: {voice_ai.name} ({voice_ai.provider})")

    # Music generation model
    music_ai = AIModelIdentity(
        name="SunoMax",
        version="2.0",
        provider="Suno",
        model_type=ModelType.FOUNDATION,
        capabilities=[
            AICapability.MUSIC_GENERATION,
            AICapability.AUDIO_GENERATION
        ]
    )
    registry.register_model(music_ai)
    print(f"  Registered: {music_ai.name} ({music_ai.provider})")

    # Fine-tuned model (inherits from parent)
    fine_tune = AIModelIdentity(
        name="VoiceForge-CustomVoice",
        version="1.0",
        provider="SomeStartup",
        model_type=ModelType.FINE_TUNED,
        parent_model_id=voice_ai.model_id,
        capabilities=[AICapability.VOICE_CLONING]
    )
    registry.register_model(fine_tune)
    print(f"  Registered: {fine_tune.name} (fine-tuned from {voice_ai.name})")

    # Create some creators
    creator_1 = "sarah-vocalist-001"
    creator_2 = "marcus-producer-002"
    creator_3 = "elena-composer-003"

    # Attest training data usage
    print("\n" + "─" * 50)
    print("2. ATTESTING TRAINING DATA USAGE")
    print("─" * 50)

    # VoiceForge trained on Sarah's voice (with consent)
    att1 = registry.attest_training(
        model_id=voice_ai.model_id,
        creator_id=creator_1,
        status=TrainingStatus.DECLARED,
        content_type="voice",
        consent_given=True,
        consent_id="consent-sarah-001",
        hours=50.0,
        samples=10000
    )
    att1.compensation_paid = True
    att1.compensation_amount = 25000.0
    print(f"  {voice_ai.name} + Sarah: DECLARED (consented, compensated)")

    # Music AI trained on Marcus's beats (detected, no consent!)
    att2 = registry.attest_training(
        model_id=music_ai.model_id,
        creator_id=creator_2,
        status=TrainingStatus.DETECTED,
        content_type="music",
        consent_given=False,
        samples=500,
        confidence=0.92
    )
    print(f"  {music_ai.name} + Marcus: DETECTED (NO CONSENT!) - 92% confidence")

    # GPT-5 trained on Elena's lyrics (suspected)
    att3 = registry.attest_training(
        model_id=gpt5.model_id,
        creator_id=creator_3,
        status=TrainingStatus.SUSPECTED,
        content_type="lyrics",
        consent_given=False,
        confidence=0.78
    )
    print(f"  {gpt5.name} + Elena: SUSPECTED (no consent) - 78% confidence")

    # Clear GPT-5 for Marcus (verified NOT trained)
    att4 = registry.attest_training(
        model_id=gpt5.model_id,
        creator_id=creator_2,
        status=TrainingStatus.CLEARED,
        content_type="music"
    )
    att4.verified_at = datetime.utcnow()
    att4.verified_by = "independent_auditor"
    print(f"  {gpt5.name} + Marcus: CLEARED (verified not trained)")

    # Check creator exposure
    print("\n" + "─" * 50)
    print("3. CREATOR EXPOSURE REPORTS")
    print("─" * 50)

    print("\n  SARAH'S AI EXPOSURE:")
    sarah_exposure = registry.get_creator_exposure(creator_1)
    print(f"    Total models trained on her content: {sarah_exposure['total_models']}")
    for model in sarah_exposure["models"]:
        print(f"    - {model['model_name']}: {model['total_hours']} hours, {model['total_samples']} samples")
        print(f"      Consented: {model['consented']}, Compensated: {model['compensated']}")

    print("\n  MARCUS'S AI EXPOSURE:")
    marcus_exposure = registry.get_creator_exposure(creator_2)
    print(f"    Total models trained on his content: {marcus_exposure['total_models']}")
    print(f"    UNCONSENTED USAGE: {marcus_exposure['unconsented_usage']} models")
    for model in marcus_exposure["models"]:
        status = "UNAUTHORIZED" if not model["consented"] else "OK"
        print(f"    - {model['model_name']}: {status}")

    # Check model sources
    print("\n" + "─" * 50)
    print("4. MODEL TRANSPARENCY REPORT")
    print("─" * 50)

    print(f"\n  {music_ai.name} TRAINING SOURCES:")
    sources = registry.get_model_sources(music_ai.model_id)
    print(f"    Total creators: {sources['total_creators']}")
    print(f"    Fully consented: {sources['fully_consented']}")
    print(f"    Fully compensated: {sources['fully_compensated']}")

    # Verify clean model
    print("\n" + "─" * 50)
    print("5. CLEAN MODEL VERIFICATION")
    print("─" * 50)

    # Is GPT-5 clean for Marcus?
    check1 = registry.verify_clean_model(gpt5.model_id, creator_2)
    print(f"\n  Can I use {gpt5.name} without infringing on Marcus?")
    print(f"    Status: {check1['status']}")
    print(f"    Verified clean: {check1['verified_clean']}")
    print(f"    Message: {check1['message']}")

    # Is VoiceForge clean for Sarah?
    check2 = registry.verify_clean_model(voice_ai.model_id, creator_1)
    print(f"\n  Can I use {voice_ai.name} without infringing on Sarah?")
    print(f"    Status: {check2['status']}")
    print(f"    Consent given: {check2.get('consent_given')}")
    print(f"    Compensation paid: {check2.get('compensation_paid')}")

    # Is SunoMax clean for Marcus?
    check3 = registry.verify_clean_model(music_ai.model_id, creator_2)
    print(f"\n  Can I use {music_ai.name} without infringing on Marcus?")
    print(f"    Status: {check3['status']}")
    print(f"    Message: {check3['message']}")
    print(f"    Consent given: {check3.get('consent_given')} ← PROBLEM!")

    print("\n" + "=" * 70)
    print("2056 VALUE: Complete AI training transparency")
    print("=" * 70)


if __name__ == "__main__":
    demo()
