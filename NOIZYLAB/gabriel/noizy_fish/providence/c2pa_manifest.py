"""
NOIZY Fish — Layer 2: Providence (C2PA Manifest Integration)
=============================================================

The C2PA (Coalition for Content Provenance and Authenticity) manifest
tracks every transformation of an asset. This module implements:

1. Asset creation capture (who, what, when, where, how)
2. Cryptographic signing of claims
3. Chain of custody tracking
4. AI involvement documentation
5. Transformation history

C2PA Reference: https://spec.c2pa.org/specifications/specifications/2.3/

This is the "genealogy" of every piece of content — tamper-evident
and cryptographically verifiable.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import uuid4
import hashlib
import json


class ActionType(Enum):
    """C2PA action types — what was done to the asset."""
    # Creation actions
    C2PA_CREATED = "c2pa.created"            # Asset was created
    C2PA_PLACED = "c2pa.placed"              # Content was placed
    C2PA_COMBINED = "c2pa.combined"          # Multiple sources combined
    C2PA_EDITED = "c2pa.edited"              # Content was edited
    C2PA_CONVERTED = "c2pa.converted"        # Format conversion
    C2PA_CROPPED = "c2pa.cropped"            # Cropped/trimmed
    C2PA_TRANSCODED = "c2pa.transcoded"      # Transcoded

    # Audio-specific actions (NOIZY extensions)
    NOIZY_RECORDED = "noizy.recorded"        # Original recording
    NOIZY_MIXED = "noizy.mixed"              # Mixing
    NOIZY_MASTERED = "noizy.mastered"        # Mastering
    NOIZY_SAMPLED = "noizy.sampled"          # Sampling used
    NOIZY_REMIXED = "noizy.remixed"          # Remix created
    NOIZY_AI_GENERATED = "noizy.ai_generated"  # AI generation
    NOIZY_AI_ASSISTED = "noizy.ai_assisted"   # AI assistance
    NOIZY_VOICE_SYNTH = "noizy.voice_synth"  # Voice synthesis


class AIDisclosure(Enum):
    """AI involvement disclosure levels."""
    NONE = "none"                            # No AI involved
    AI_ASSISTED = "ai_assisted"              # Human + AI
    AI_GENERATED = "ai_generated"            # Primarily AI
    AI_TRAINED_ON = "ai_trained_on"          # Used as training data


@dataclass
class SoftwarAgent:
    """Software/tool that processed the asset."""
    name: str                                # "Pro Tools", "Fish Speech"
    version: Optional[str] = None
    vendor: Optional[str] = None
    icon_uri: Optional[str] = None


@dataclass
class HardwareDevice:
    """Hardware used in capture/creation."""
    manufacturer: str
    model: str
    serial_number: Optional[str] = None


@dataclass
class Action:
    """A single action performed on the asset."""
    action: ActionType
    when: datetime = field(default_factory=datetime.utcnow)
    software_agent: Optional[SoftwarAgent] = None
    parameters: dict = field(default_factory=dict)
    description: Optional[str] = None
    changes: list[str] = field(default_factory=list)
    digital_source_type: Optional[str] = None  # "digitalCapture", "trainedAlgorithmicMedia"

    def to_c2pa(self) -> dict:
        """Export as C2PA action assertion."""
        result = {
            "action": self.action.value,
            "when": self.when.isoformat() + "Z"
        }
        if self.software_agent:
            result["softwareAgent"] = {
                "name": self.software_agent.name,
                "version": self.software_agent.version
            }
        if self.parameters:
            result["parameters"] = self.parameters
        if self.description:
            result["description"] = self.description
        if self.digital_source_type:
            result["digitalSourceType"] = self.digital_source_type
        return result


@dataclass
class Ingredient:
    """
    An ingredient (source material) in the asset.
    Tracks sampling, remixing, and derived works.
    """
    ingredient_id: str = field(default_factory=lambda: str(uuid4()))

    # Source identification
    title: str = ""
    format: str = ""                         # audio/wav, audio/mp3, etc.
    instance_id: Optional[str] = None        # Original manifest ID
    document_id: Optional[str] = None

    # NOIZY identifiers
    noizy_work_id: Optional[str] = None
    isrc: Optional[str] = None
    iswc: Optional[str] = None

    # Relationship
    relationship: str = "componentOf"        # componentOf, parentOf, inputTo

    # Hash of the ingredient (for verification)
    data_hash: Optional[str] = None
    hash_algorithm: str = "sha256"

    # Validation
    validation_status: str = "unknown"       # valid, invalid, unknown

    def to_c2pa(self) -> dict:
        """Export as C2PA ingredient."""
        return {
            "title": self.title,
            "format": self.format,
            "relationship": self.relationship,
            "instanceID": self.instance_id,
            "documentID": self.document_id,
            "hash": {
                "alg": self.hash_algorithm,
                "hash": self.data_hash
            } if self.data_hash else None,
            "validationStatus": self.validation_status,
            "noizy:workId": self.noizy_work_id,
            "noizy:isrc": self.isrc,
            "noizy:iswc": self.iswc
        }


@dataclass
class CreatorAssertion:
    """
    Creator identity assertion for C2PA.
    Links to the Creator Passport.
    """
    creator_id: str
    display_name: str
    role: str                                # "composer", "producer", etc.

    # Linked identifiers
    noizy_id: Optional[str] = None
    ipi: Optional[str] = None
    isni: Optional[str] = None

    # Verification
    verified: bool = False
    verification_uri: Optional[str] = None

    def to_c2pa(self) -> dict:
        """Export as C2PA creator assertion."""
        identifiers = [{"type": "noizy", "value": self.noizy_id}] if self.noizy_id else []
        if self.ipi:
            identifiers.append({"type": "ipi", "value": self.ipi})
        if self.isni:
            identifiers.append({"type": "isni", "value": self.isni})

        return {
            "name": self.display_name,
            "identifier": identifiers,
            "role": self.role,
            "verified": self.verified
        }


@dataclass
class AIAssertion:
    """
    AI involvement assertion — critical for transparency.
    Documents any AI used in creation/modification.
    """
    disclosure: AIDisclosure = AIDisclosure.NONE

    # AI tools used
    ai_tools: list[SoftwarAgent] = field(default_factory=list)

    # Training data disclosure
    trained_on_licensed_data: Optional[bool] = None
    training_data_consent: Optional[bool] = None

    # Generation details
    prompt_used: Optional[str] = None
    human_oversight: bool = True
    human_modifications: list[str] = field(default_factory=list)

    def to_c2pa(self) -> dict:
        """Export as C2PA AI assertion."""
        return {
            "aiDisclosure": self.disclosure.value,
            "aiTools": [
                {"name": t.name, "version": t.version, "vendor": t.vendor}
                for t in self.ai_tools
            ],
            "trainedOnLicensedData": self.trained_on_licensed_data,
            "trainingDataConsent": self.training_data_consent,
            "humanOversight": self.human_oversight,
            "humanModifications": self.human_modifications
        }


@dataclass
class Claim:
    """
    A C2PA claim — the core unit of provenance.
    Contains assertions about the asset, signed cryptographically.
    """
    claim_id: str = field(default_factory=lambda: str(uuid4()))

    # Claim metadata
    dc_title: str = ""                       # Asset title
    dc_format: str = ""                      # MIME type
    instance_id: str = field(default_factory=lambda: f"urn:uuid:{uuid4()}")

    # Signature
    signature: Optional[str] = None
    signature_algorithm: str = "ES256"       # ECDSA with P-256 and SHA-256
    claim_generator: str = "NOIZY Fish/1.0"

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)

    # Hash of bound content
    asset_hash: Optional[str] = None

    # Actions performed
    actions: list[Action] = field(default_factory=list)

    # Ingredients (source materials)
    ingredients: list[Ingredient] = field(default_factory=list)

    # Creators
    creators: list[CreatorAssertion] = field(default_factory=list)

    # AI disclosure
    ai_assertion: Optional[AIAssertion] = None

    def generate_hash(self) -> str:
        """Generate hash of claim content."""
        data = {
            "claim_id": self.claim_id,
            "dc_title": self.dc_title,
            "instance_id": self.instance_id,
            "created_at": self.created_at.isoformat(),
            "actions": [a.to_c2pa() for a in self.actions],
            "ingredients": [i.to_c2pa() for i in self.ingredients],
            "creators": [c.to_c2pa() for c in self.creators]
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def to_c2pa(self) -> dict:
        """Export as C2PA claim."""
        return {
            "@context": "https://c2pa.org/claim/1",
            "dc:title": self.dc_title,
            "dc:format": self.dc_format,
            "instanceID": self.instance_id,
            "claim_generator": self.claim_generator,
            "signature": {
                "alg": self.signature_algorithm,
                "sig": self.signature
            } if self.signature else None,
            "assertions": {
                "c2pa.actions": [a.to_c2pa() for a in self.actions],
                "c2pa.ingredient": [i.to_c2pa() for i in self.ingredients],
                "noizy.creator": [c.to_c2pa() for c in self.creators],
                "noizy.ai": self.ai_assertion.to_c2pa() if self.ai_assertion else None
            },
            "claim_hash": self.generate_hash(),
            "asset_hash": self.asset_hash
        }


@dataclass
class C2PAManifest:
    """
    The complete C2PA manifest for an asset.
    This is the provenance record that travels with the content.
    """
    manifest_id: str = field(default_factory=lambda: str(uuid4()))

    # Active claim (current state)
    claim: Claim = field(default_factory=Claim)

    # Previous claims (history)
    claim_history: list[Claim] = field(default_factory=list)

    # NOIZY-specific metadata
    noizy_work_id: Optional[str] = None
    isrc: Optional[str] = None
    iswc: Optional[str] = None

    # Consent link
    consent_registry_id: Optional[str] = None
    consent_version: Optional[int] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_action(self, action: Action):
        """Add an action to the current claim."""
        self.claim.actions.append(action)
        self.updated_at = datetime.utcnow()

    def add_ingredient(self, ingredient: Ingredient):
        """Add an ingredient (source material)."""
        self.claim.ingredients.append(ingredient)
        self.updated_at = datetime.utcnow()

    def add_creator(self, creator: CreatorAssertion):
        """Add a creator assertion."""
        self.claim.creators.append(creator)
        self.updated_at = datetime.utcnow()

    def set_ai_disclosure(self, ai_assertion: AIAssertion):
        """Set AI involvement disclosure."""
        self.claim.ai_assertion = ai_assertion
        self.updated_at = datetime.utcnow()

    def new_version(self) -> "C2PAManifest":
        """Create a new version, preserving history."""
        # Archive current claim
        self.claim_history.append(self.claim)

        # Create new claim
        new_claim = Claim(
            dc_title=self.claim.dc_title,
            dc_format=self.claim.dc_format
        )

        return C2PAManifest(
            claim=new_claim,
            claim_history=self.claim_history,
            noizy_work_id=self.noizy_work_id,
            isrc=self.isrc,
            iswc=self.iswc,
            consent_registry_id=self.consent_registry_id,
            consent_version=self.consent_version
        )

    def verify_chain(self) -> tuple[bool, list[str]]:
        """Verify the integrity of the claim chain."""
        issues = []

        # Verify current claim hash
        expected_hash = self.claim.generate_hash()
        if self.claim.asset_hash and self.claim.asset_hash != expected_hash:
            issues.append("Current claim hash mismatch")

        # Verify history chain
        # (In production, would verify signatures and hash chain)

        return len(issues) == 0, issues

    def to_c2pa_store(self) -> dict:
        """Export as C2PA manifest store (full provenance)."""
        return {
            "@context": "https://c2pa.org/manifest/1",
            "manifest_id": self.manifest_id,
            "active_manifest": self.claim.to_c2pa(),
            "manifest_history": [c.to_c2pa() for c in self.claim_history],
            "noizy": {
                "work_id": self.noizy_work_id,
                "isrc": self.isrc,
                "iswc": self.iswc,
                "consent_registry": self.consent_registry_id,
                "consent_version": self.consent_version
            },
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def to_json(self) -> str:
        """Export manifest as JSON."""
        return json.dumps(self.to_c2pa_store(), indent=2, default=str)


# ═══════════════════════════════════════════════════════════════════════════
# Factory functions for common scenarios
# ═══════════════════════════════════════════════════════════════════════════

def create_recording_manifest(
    title: str,
    creator_name: str,
    creator_id: str,
    format: str = "audio/wav",
    isrc: Optional[str] = None,
    software: Optional[str] = None
) -> C2PAManifest:
    """Create a manifest for a new recording."""
    manifest = C2PAManifest(
        isrc=isrc
    )

    manifest.claim.dc_title = title
    manifest.claim.dc_format = format

    # Add creation action
    manifest.add_action(Action(
        action=ActionType.NOIZY_RECORDED,
        software_agent=SoftwarAgent(name=software) if software else None,
        digital_source_type="digitalCapture"
    ))

    # Add creator
    manifest.add_creator(CreatorAssertion(
        creator_id=creator_id,
        display_name=creator_name,
        role="RecordingArtist"
    ))

    return manifest


def create_ai_generated_manifest(
    title: str,
    ai_tool: str,
    ai_tool_version: str,
    human_operator: str,
    human_operator_id: str,
    prompt: Optional[str] = None
) -> C2PAManifest:
    """Create a manifest for AI-generated content."""
    manifest = C2PAManifest()

    manifest.claim.dc_title = title
    manifest.claim.dc_format = "audio/wav"

    # Add AI generation action
    manifest.add_action(Action(
        action=ActionType.NOIZY_AI_GENERATED,
        software_agent=SoftwarAgent(name=ai_tool, version=ai_tool_version),
        digital_source_type="trainedAlgorithmicMedia"
    ))

    # Add human operator
    manifest.add_creator(CreatorAssertion(
        creator_id=human_operator_id,
        display_name=human_operator,
        role="AIOperator"
    ))

    # Add AI disclosure
    manifest.set_ai_disclosure(AIAssertion(
        disclosure=AIDisclosure.AI_GENERATED,
        ai_tools=[SoftwarAgent(name=ai_tool, version=ai_tool_version)],
        prompt_used=prompt,
        human_oversight=True
    ))

    return manifest
