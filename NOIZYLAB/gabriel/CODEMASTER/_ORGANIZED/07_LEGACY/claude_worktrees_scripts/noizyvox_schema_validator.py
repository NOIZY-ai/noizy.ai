#!/usr/bin/env python3
"""
NOIZYVOX Schema Validator
Validates Persona Packs and Artifact Manifests against JSON schemas
"""

import json
import hashlib
import secrets
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple

try:
    import jsonschema
    from jsonschema import Draft202012Validator, ValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    print("⚠️  jsonschema not installed. Run: pip install jsonschema")

# Schema paths relative to project root
SCHEMA_DIR = Path(__file__).parent.parent / "schemas"
PERSONA_SCHEMA = SCHEMA_DIR / "persona_pack.schema.json"
MANIFEST_SCHEMA = SCHEMA_DIR / "manifest.schema.json"
CONSENT_SCHEMA = SCHEMA_DIR / "consent.schema.json"
LICENSE_SCHEMA = SCHEMA_DIR / "license.schema.json"
REVOCATION_SCHEMA = SCHEMA_DIR / "revocation.schema.json"
AUTOMATION_SCHEMA = SCHEMA_DIR / "automation_lane.schema.json"
EDGE_DEPLOYMENT_SCHEMA = SCHEMA_DIR / "edge_deployment.schema.json"
AB_TESTING_SCHEMA = SCHEMA_DIR / "ab_testing.schema.json"
DISPUTE_RESOLUTION_SCHEMA = SCHEMA_DIR / "dispute_resolution.schema.json"
POSTHUMOUS_RIGHTS_SCHEMA = SCHEMA_DIR / "posthumous_rights.schema.json"
SECURITY_WATERMARKING_SCHEMA = SCHEMA_DIR / "security_watermarking.schema.json"
GUILD_GOVERNANCE_SCHEMA = SCHEMA_DIR / "guild_governance.schema.json"
VR_AR_SPATIAL_SCHEMA = SCHEMA_DIR / "vr_ar_spatial.schema.json"
DAW_PLUGIN_SCHEMA = SCHEMA_DIR / "daw_plugin.schema.json"
GAME_ENGINE_SDK_SCHEMA = SCHEMA_DIR / "game_engine_sdk.schema.json"
ANALYTICS_DASHBOARD_SCHEMA = SCHEMA_DIR / "analytics_dashboard.schema.json"
ENTERPRISE_DEPLOYMENT_SCHEMA = SCHEMA_DIR / "enterprise_deployment.schema.json"
LLM_ORCHESTRATION_SCHEMA = SCHEMA_DIR / "llm_orchestration.schema.json"
EMOTION_AI_SCHEMA = SCHEMA_DIR / "emotion_ai.schema.json"
VOICE_CLONING_PIPELINE_SCHEMA = SCHEMA_DIR / "voice_cloning_pipeline.schema.json"
AGENTIC_VOICE_SCHEMA = SCHEMA_DIR / "agentic_voice.schema.json"
MULTIMODAL_SYNC_SCHEMA = SCHEMA_DIR / "multimodal_sync.schema.json"
SUPERSONIC_PIPELINE_SCHEMA = SCHEMA_DIR / "supersonic_pipeline.schema.json"
OSS_INTEGRATIONS_SCHEMA = SCHEMA_DIR / "open_source_integrations.schema.json"
OPENAI_VOICE_SCHEMA = SCHEMA_DIR / "openai_voice_integration.schema.json"
OPENAI_VOICE_COMPLETE_SCHEMA = SCHEMA_DIR / "openai_voice_complete.schema.json"


def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load a JSON schema from file."""
    with open(schema_path, 'r') as f:
        return json.load(f)


def validate_document(document: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, list]:
    """
    Validate a document against a schema.
    Returns (is_valid, list of errors)
    """
    if not HAS_JSONSCHEMA:
        return False, ["jsonschema library not installed"]
    
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(document))
    
    if errors:
        error_messages = []
        for error in errors:
            path = " -> ".join(str(p) for p in error.absolute_path) or "root"
            error_messages.append(f"[{path}] {error.message}")
        return False, error_messages
    
    return True, []


def generate_id(prefix: str, length: int = 12) -> str:
    """Generate a random ID with prefix."""
    return f"{prefix}{secrets.token_hex(length // 2)}"


def generate_hash(content: str) -> str:
    """Generate SHA-256 hash of content."""
    return f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"


def create_sample_persona_pack() -> Dict[str, Any]:
    """Create a sample persona pack for testing."""
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "persona_id": "solar_sentinel_hero",
        "version": "1.0.0",
        "display_name": "Solar Sentinel",
        "artist": {
            "artist_id": generate_id("artist_"),
            "legal_name": "Jane Doe",
            "stage_name": "Solar Voice",
            "guild_status": "verified",
            "verified_at": now,
            "verification_method": "video_verification",
            "contact_email": "artist@example.com"
        },
        "archetype_tags": ["Solar Sentinel", "inspirational", "warm", "heroic"],
        "short_bio": "A warm, inspirational voice that embodies hope and determination.",
        "recommended_prosody": {
            "pitch_base_hz": 180,
            "pitch_range_st": 8,
            "rate_wpm": 140,
            "volume_db": 0,
            "breathiness": 0.2,
            "warmth": 0.8,
            "articulation": "theatrical"
        },
        "ssml_template": "<speak><prosody rate=\"medium\" pitch=\"+2st\">{{text}}</prosody></speak>",
        "dsp_recipe": {
            "eq": {
                "low_cut_hz": 80,
                "low_shelf_hz": 200,
                "low_shelf_gain_db": 2,
                "mid_freq_hz": 2500,
                "mid_gain_db": 1.5,
                "mid_q": 1.2,
                "high_shelf_hz": 8000,
                "high_shelf_gain_db": 3,
                "presence_freq_hz": 4000,
                "presence_gain_db": 2
            },
            "compressor": {
                "threshold_db": -18,
                "ratio": 3,
                "attack_ms": 10,
                "release_ms": 100,
                "knee_db": 6,
                "makeup_gain_db": 4
            },
            "reverb": {
                "type": "studio",
                "decay_s": 1.2,
                "predelay_ms": 20,
                "wet_dry_mix": 0.15,
                "diffusion": 0.7
            },
            "lufs_target": -16,
            "limiter": {
                "ceiling_db": -1,
                "release_ms": 50
            },
            "de_esser": {
                "frequency_hz": 6000,
                "threshold_db": -20,
                "reduction_db": 4
            }
        },
        "animation_cues": {
            "rig_format": "arkit_52",
            "blink_rate_hz": 0.25,
            "micro_expression_intensity": 0.6,
            "head_motion": {
                "nod_intensity": 0.4,
                "sway_intensity": 0.2,
                "look_at_variance_deg": 8
            }
        },
        "consent": {
            "voice_capture_consent": True,
            "ai_training_consent": True,
            "commercial_use_consent": True,
            "derivative_works_consent": True,
            "content_restrictions": ["political", "adult"],
            "consent_timestamp": now,
            "consent_hash": generate_hash(f"consent_{now}"),
            "revocation_policy": {
                "notice_period_days": 90,
                "existing_licenses_honored": True,
                "immediate_takedown_allowed": False
            }
        },
        "provenance": {
            "created_at": now,
            "commit_hash": hashlib.sha256(b"sample_commit").hexdigest(),
            "artifact_hash": generate_hash(f"artifact_{now}"),
            "watermark_id": generate_id("wm_", 16)
        },
        "licensing": {
            "available_tiers": ["micro", "non_exclusive", "exclusive"],
            "pricing": {
                "micro_per_minute_usd": 0.10,
                "non_exclusive_monthly_usd": 99,
                "exclusive_buyout_usd": 5000
            },
            "revenue_split": {
                "artist_percent": 75,
                "platform_percent": 25
            },
            "minimum_payout_usd": 25
        }
    }


def create_sample_manifest(persona_id: str = "solar_sentinel_hero") -> Dict[str, Any]:
    """Create a sample artifact manifest for testing."""
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "manifest_id": generate_id("mf_", 24),
        "version": "1.0.0",
        "created_at": now,
        "artifact_type": "audio_render",
        "persona_id": persona_id,
        "artist_id": generate_id("artist_"),
        "license_id": generate_id("lic_", 16),
        "licensee": {
            "licensee_id": "user_123",
            "organization": "NOIZYVOX Demo",
            "email": "demo@noizyvox.ai",
            "tier": "non_exclusive"
        },
        "content_hash": generate_hash(f"content_{now}"),
        "watermark": {
            "watermark_id": generate_id("wm_", 16),
            "method": "spectral",
            "embedded_at": now,
            "detection_endpoint": "https://api.noizyvox.ai/watermark/detect",
            "robustness_level": "broadcast"
        },
        "fingerprint": {
            "algorithm": "chromaprint",
            "fingerprint_hash": generate_hash(f"fingerprint_{now}"),
            "duration_ms": 45000,
            "registered_at": now
        },
        "input_script": {
            "text": "Welcome to NOIZYVOX, where voices come alive.",
            "text_hash": generate_hash("Welcome to NOIZYVOX, where voices come alive."),
            "language": "en-US",
            "ssml_version": "1.1"
        },
        "render_params": {
            "dsp_recipe_hash": generate_hash("dsp_recipe"),
            "target_environment": "studio",
            "sample_rate_hz": 48000,
            "bit_depth": 24,
            "format": "wav"
        },
        "moderation": {
            "scanned_at": now,
            "passed": True,
            "flags": [],
            "appeal_status": "none"
        },
        "usage_tracking": {
            "plays": 0,
            "downloads": 0,
            "api_calls": 1,
            "last_accessed_at": now
        }
    }


def validate_persona_pack(file_path: Path) -> bool:
    """Validate a persona pack JSON file."""
    print(f"\n🎭 Validating Persona Pack: {file_path}")
    
    schema = load_schema(PERSONA_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Persona Pack is valid!")
        print(f"   ID: {document.get('persona_id')}")
        print(f"   Display Name: {document.get('display_name')}")
        print(f"   Version: {document.get('version')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_manifest(file_path: Path) -> bool:
    """Validate an artifact manifest JSON file."""
    print(f"\n📋 Validating Artifact Manifest: {file_path}")
    
    schema = load_schema(MANIFEST_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Manifest is valid!")
        print(f"   ID: {document.get('manifest_id')}")
        print(f"   Type: {document.get('artifact_type')}")
        print(f"   Persona: {document.get('persona_id')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_consent(file_path: Path) -> bool:
    """Validate a consent record JSON file."""
    print(f"\n📝 Validating Consent Record: {file_path}")
    
    schema = load_schema(CONSENT_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Consent Record is valid!")
        print(f"   ID: {document.get('consent_id')}")
        print(f"   Artist: {document.get('legal_name')}")
        print(f"   Status: {document.get('status')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_license(file_path: Path) -> bool:
    """Validate a license record JSON file."""
    print(f"\n🎫 Validating License Record: {file_path}")
    
    schema = load_schema(LICENSE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ License Record is valid!")
        print(f"   ID: {document.get('license_id')}")
        print(f"   Tier: {document.get('tier')}")
        print(f"   Licensee: {document.get('licensee', {}).get('organization')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_revocation(file_path: Path) -> bool:
    """Validate a revocation record JSON file."""
    print(f"\n🚫 Validating Revocation Record: {file_path}")
    
    schema = load_schema(REVOCATION_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Revocation Record is valid!")
        print(f"   ID: {document.get('revocation_id')}")
        print(f"   Type: {document.get('revocation_type')}")
        print(f"   Status: {document.get('status')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_automation(file_path: Path) -> bool:
    """Validate an automation lane JSON file."""
    print(f"\n🎚️  Validating Automation Lane: {file_path}")
    
    schema = load_schema(AUTOMATION_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Automation Lane is valid!")
        print(f"   ID: {document.get('automation_id')}")
        print(f"   Text: {document.get('text', '')[:50]}..." if len(document.get('text', '')) > 50 else f"   Text: {document.get('text', '')}")
        print(f"   Words: {len(document.get('words', []))}")
        print(f"   Duration: {document.get('duration_ms')}ms")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_edge_deployment(file_path: Path) -> bool:
    """Validate an edge deployment JSON file."""
    print(f"\n📡 Validating Edge Deployment: {file_path}")
    
    schema = load_schema(EDGE_DEPLOYMENT_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Edge Deployment is valid!")
        print(f"   ID: {document.get('deployment_id')}")
        print(f"   Persona: {document.get('persona_id')}")
        model = document.get('model_package', {})
        print(f"   Format: {model.get('format')} ({model.get('quantization', 'fp32')})")
        print(f"   Size: {model.get('size_mb')}MB")
        platforms = document.get('target_platforms', [])
        print(f"   Platforms: {[p.get('platform') for p in platforms]}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_experiment(file_path: Path) -> bool:
    """Validate an A/B testing experiment JSON file."""
    print(f"\n🧪 Validating A/B Experiment: {file_path}")
    
    schema = load_schema(AB_TESTING_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ A/B Experiment is valid!")
        print(f"   ID: {document.get('experiment_id')}")
        print(f"   Name: {document.get('name')}")
        print(f"   Status: {document.get('status')}")
        variants = document.get('variants', [])
        print(f"   Variants: {len(variants)}")
        results = document.get('results', {})
        if results.get('winner'):
            print(f"   Winner: {results.get('winner')} ({results.get('recommendation')})")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_dispute(file_path: Path) -> bool:
    """Validate a dispute resolution JSON file."""
    print(f"\n⚖️  Validating Dispute Resolution: {file_path}")
    
    schema = load_schema(DISPUTE_RESOLUTION_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Dispute Resolution is valid!")
        print(f"   ID: {document.get('dispute_id')}")
        print(f"   Type: {document.get('dispute_type')}")
        print(f"   Status: {document.get('status')}")
        print(f"   Priority: {document.get('priority')}")
        parties = document.get('parties', {})
        claimant = parties.get('claimant', {}).get('name', 'N/A')
        respondent = parties.get('respondent', {}).get('name', 'N/A')
        print(f"   Claimant: {claimant}")
        print(f"   Respondent: {respondent}")
        resolution = document.get('resolution')
        if resolution:
            print(f"   Resolved: {resolution.get('resolved_at')}")
            print(f"   Prevailing Party: {resolution.get('prevailing_party', 'N/A')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_estate_plan(file_path: Path) -> bool:
    """Validate a posthumous rights / estate plan JSON file."""
    print(f"\n🏛️  Validating Estate Plan: {file_path}")
    
    schema = load_schema(POSTHUMOUS_RIGHTS_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Estate Plan is valid!")
        print(f"   ID: {document.get('estate_plan_id')}")
        print(f"   Artist: {document.get('artist_id')}")
        print(f"   Status: {document.get('status')}")
        primary = document.get('primary_beneficiary', {})
        print(f"   Primary Beneficiary: {primary.get('name', 'N/A')}")
        executor = document.get('executor', {})
        print(f"   Executor: {executor.get('name', 'N/A')}")
        directives = document.get('directives', {})
        if directives.get('sunset_date'):
            print(f"   Sunset Date: {directives.get('sunset_date')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_security_watermark(file_path: Path) -> bool:
    """Validate a security/watermarking JSON file."""
    print(f"\n🔐 Validating Security Watermark: {file_path}")
    
    schema = load_schema(SECURITY_WATERMARKING_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Security Watermark is valid!")
        watermark = document.get('watermark', {})
        print(f"   ID: {watermark.get('watermark_id')}")
        methods = watermark.get('methods', [])
        method_names = [m.get('method') for m in methods]
        print(f"   Methods: {', '.join(method_names)}")
        fingerprinting = document.get('fingerprinting', {})
        if fingerprinting.get('algorithms'):
            print(f"   Fingerprinting: {', '.join(fingerprinting.get('algorithms', []))}")
        deepfake = document.get('deepfake_detection', {})
        if deepfake.get('enabled'):
            models = deepfake.get('detection_models', [])
            print(f"   Deepfake Detection: {len(models)} model(s)")
        provenance = document.get('provenance_chain', {})
        if provenance.get('c2pa_enabled'):
            print(f"   C2PA Provenance: Enabled")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_guild_governance(file_path: Path) -> bool:
    """Validate a guild governance JSON file."""
    print(f"\n🏛️  Validating Guild Governance: {file_path}")
    
    schema = load_schema(GUILD_GOVERNANCE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Guild Governance is valid!")
        print(f"   ID: {document.get('guild_id')}")
        print(f"   Name: {document.get('name')}")
        membership = document.get('membership', {})
        print(f"   Total Members: {membership.get('total_members', 'N/A')}")
        tiers = membership.get('tiers', {})
        founding = tiers.get('founding', {})
        verified = tiers.get('verified', {})
        print(f"   Founding: {founding.get('current_members', 0)} / {founding.get('max_members', 100)}")
        print(f"   Verified: {verified.get('current_members', 0)}")
        council = document.get('governance_structure', {}).get('council', {})
        print(f"   Council Seats: {council.get('seats', 9)}")
        treasury = document.get('treasury', {})
        if treasury.get('balance_usd'):
            print(f"   Treasury: ${treasury.get('balance_usd'):,.0f}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_vr_ar_spatial(file_path: Path) -> bool:
    """Validate a VR/AR spatial audio JSON file."""
    print(f"\n🥽 Validating VR/AR Spatial Audio: {file_path}")
    
    schema = load_schema(VR_AR_SPATIAL_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ VR/AR Spatial Audio is valid!")
        print(f"   ID: {document.get('spatial_config_id')}")
        print(f"   Persona: {document.get('persona_id')}")
        print(f"   Platform: {document.get('platform')}")
        hrtf = document.get('hrtf', {})
        if hrtf:
            personalization = hrtf.get('personalization', {})
            if personalization.get('enabled'):
                print(f"   HRTF: personalized ({hrtf.get('database', 'custom')})")
            else:
                print(f"   HRTF: {hrtf.get('database', 'generic')}")
        spatialization = document.get('spatialization', {})
        if spatialization:
            print(f"   Spatialization: {spatialization.get('algorithm', 'N/A')}")
        head_tracking = document.get('head_tracking', {})
        if head_tracking.get('enabled'):
            print(f"   Head Tracking: {head_tracking.get('update_rate_hz')}Hz")
        lip_sync = document.get('lip_sync', {})
        if lip_sync.get('enabled'):
            print(f"   Lip Sync: {lip_sync.get('viseme_set', 'N/A')}")
        passthrough = document.get('passthrough_ar', {})
        if passthrough.get('enabled'):
            print(f"   Passthrough AR: blend={passthrough.get('blend_virtual_real', 0.5)}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_daw_plugin(file_path: Path) -> bool:
    """Validate a DAW plugin JSON file."""
    print(f"\n🎛️  Validating DAW Plugin: {file_path}")
    
    schema = load_schema(DAW_PLUGIN_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ DAW Plugin is valid!")
        print(f"   ID: {document.get('plugin_id')}")
        print(f"   Version: {document.get('version')}")
        formats = document.get('formats', [])
        format_names = [f.get('format') for f in formats]
        print(f"   Formats: {', '.join(format_names)}")
        daw_compat = document.get('daw_compatibility', [])
        certified = [d.get('daw') for d in daw_compat if d.get('certification') == 'certified']
        compatible = [d.get('daw') for d in daw_compat if d.get('certification') == 'compatible']
        if certified:
            print(f"   Certified DAWs: {', '.join(certified)}")
        if compatible:
            print(f"   Compatible DAWs: {', '.join(compatible)}")
        audio = document.get('audio_specs', {})
        if audio:
            latency = audio.get('latency', {})
            if latency:
                print(f"   Latency: {latency.get('reported_samples')} samples ({latency.get('actual_ms')}ms)")
        features = document.get('features', {})
        if features:
            feature_list = []
            if features.get('ssml_editor', {}).get('visual_editor'):
                feature_list.append('SSML Editor')
            if features.get('editing', {}).get('pitch_drawing'):
                feature_list.append('Pitch Drawing')
            if features.get('waveform_display', {}).get('spectrogram'):
                feature_list.append('Spectrogram')
            if feature_list:
                print(f"   Features: {', '.join(feature_list)}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_game_engine_sdk(file_path: Path) -> bool:
    """Validate a Game Engine SDK JSON file."""
    print(f"\n🎮 Validating Game Engine SDK: {file_path}")
    
    schema = load_schema(GAME_ENGINE_SDK_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Game Engine SDK is valid!")
        print(f"   ID: {document.get('sdk_id')}")
        print(f"   Version: {document.get('version')}")
        engines = document.get('engines', [])
        engine_names = [e.get('engine') for e in engines]
        print(f"   Engines: {', '.join(engine_names)}")
        platforms = document.get('platforms', [])
        certified = [p.get('platform') for p in platforms if p.get('certification_status') == 'certified']
        if certified:
            print(f"   Certified Platforms: {', '.join(certified)}")
        api = document.get('api', {})
        core_classes = api.get('core_classes', [])
        if core_classes:
            class_names = [c.get('class_name') for c in core_classes]
            print(f"   Core Classes: {', '.join(class_names)}")
        lip_sync = document.get('lip_sync', {})
        if lip_sync:
            methods = lip_sync.get('methods', [])
            if methods:
                print(f"   Lip Sync: {', '.join(methods)}")
        networking = document.get('networking', {})
        offline = networking.get('offline_mode', {})
        if offline.get('enabled'):
            print(f"   Offline Mode: {offline.get('bundled_personas')} bundled personas")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_analytics_dashboard(file_path: Path) -> bool:
    """Validate an Analytics Dashboard JSON file."""
    print(f"\n📊 Validating Analytics Dashboard: {file_path}")
    
    schema = load_schema(ANALYTICS_DASHBOARD_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Analytics Dashboard is valid!")
        print(f"   ID: {document.get('dashboard_id')}")
        print(f"   Owner: {document.get('owner_type')} ({document.get('owner_id')})")
        time_range = document.get('time_range', {})
        if time_range:
            print(f"   Time Range: {time_range.get('preset', 'custom')}")
        artist_metrics = document.get('artist_metrics', {})
        if artist_metrics:
            revenue = artist_metrics.get('revenue', {})
            if revenue:
                print(f"   Total Earnings: ${revenue.get('total_earnings_usd', 0):,.2f}")
                print(f"   Pending Payout: ${revenue.get('pending_payout_usd', 0):,.2f}")
            usage = artist_metrics.get('usage', {})
            if usage:
                print(f"   Total Generations: {usage.get('total_generations', 0):,}")
                print(f"   Audio Minutes: {usage.get('total_audio_minutes', 0):,.1f}")
            licensing = artist_metrics.get('licensing', {})
            if licensing:
                print(f"   Active Licenses: {licensing.get('active_licenses', 0)}")
            quality = artist_metrics.get('quality', {})
            if quality:
                print(f"   Average Rating: {quality.get('average_rating', 0):.1f}/5 ({quality.get('total_ratings', 0)} ratings)")
        alerts = document.get('alerts', [])
        if alerts:
            critical = len([a for a in alerts if a.get('severity') == 'critical'])
            warning = len([a for a in alerts if a.get('severity') == 'warning'])
            info = len([a for a in alerts if a.get('severity') == 'info'])
            print(f"   Alerts: {critical} critical, {warning} warning, {info} info")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_enterprise_deployment(file_path: Path) -> bool:
    """Validate an Enterprise Deployment JSON file."""
    print(f"\n🏢 Validating Enterprise Deployment: {file_path}")
    
    schema = load_schema(ENTERPRISE_DEPLOYMENT_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Enterprise Deployment is valid!")
        print(f"   ID: {document.get('deployment_id')}")
        org = document.get('organization', {})
        print(f"   Organization: {org.get('name')} ({org.get('size', 'unknown')})")
        print(f"   Industry: {org.get('industry', 'unspecified')}")
        print(f"   Deployment Type: {document.get('deployment_type')}")
        infra = document.get('infrastructure', {})
        if infra:
            print(f"   Cloud Provider: {infra.get('cloud_provider', 'N/A')}")
            regions = infra.get('regions', [])
            if regions:
                print(f"   Regions: {', '.join(regions)}")
            compute = infra.get('dedicated_compute', {})
            if compute:
                gpu_info = f"{compute.get('gpu_count', 0)}x {compute.get('gpu_type', 'N/A')}"
                print(f"   Compute: {gpu_info}, {compute.get('ram_gb', 0)}GB RAM")
            k8s = infra.get('kubernetes', {})
            if k8s.get('enabled'):
                print(f"   Kubernetes: {k8s.get('distribution', 'unknown')}")
        security = document.get('security', {})
        if security:
            sso = security.get('sso', {})
            if sso:
                print(f"   SSO: {sso.get('provider', 'N/A')}")
            compliance = security.get('compliance', {})
            certs = compliance.get('certifications', [])
            if certs:
                print(f"   Compliance: {', '.join(certs)}")
        support = document.get('support', {})
        if support:
            print(f"   Support Tier: {support.get('tier', 'standard')}")
            if support.get('dedicated_csm'):
                print(f"   Dedicated CSM: {support.get('csm_name', 'Assigned')}")
        billing = document.get('billing', {})
        if billing:
            print(f"   Billing Model: {billing.get('model')}")
            if billing.get('commitment_amount_usd'):
                print(f"   Commitment: ${billing.get('commitment_amount_usd'):,.2f}/year")
            if billing.get('contract_term_months'):
                print(f"   Contract Term: {billing.get('contract_term_months')} months")
        dr = document.get('disaster_recovery', {})
        if dr.get('enabled'):
            print(f"   DR: {dr.get('type', 'N/A')} (RPO: {dr.get('rpo_hours')}h, RTO: {dr.get('rto_hours')}h)")
        status = document.get('status', 'unknown')
        print(f"   Status: {status}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_llm_orchestration(file_path: Path) -> bool:
    """Validate an LLM Orchestration JSON file."""
    print(f"\n🤖 Validating LLM Orchestration: {file_path}")
    
    schema = load_schema(LLM_ORCHESTRATION_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ LLM Orchestration is valid!")
        print(f"   ID: {document.get('orchestration_id')}")
        print(f"   Version: {document.get('version')}")
        providers = document.get('providers', [])
        if providers:
            print(f"   Providers: {len(providers)}")
            for p in providers:
                prio = "primary" if p.get('priority') == 1 else f"fallback (p{p.get('priority')})"
                caps = len(p.get('capabilities', []))
                print(f"     • {p.get('provider')}/{p.get('model')} [{prio}] - {caps} capabilities")
        dramaturgy = document.get('dramaturgy_engine', {})
        if dramaturgy.get('enabled'):
            features = dramaturgy.get('features', {})
            analysis = features.get('script_analysis', {})
            enhancement = features.get('script_enhancement', {})
            direction = features.get('character_direction', {})
            enabled_count = sum(1 for v in analysis.values() if v) + \
                           sum(1 for v in enhancement.values() if v) + \
                           sum(1 for v in direction.values() if v)
            print(f"   Dramaturgy: {enabled_count} features enabled")
        rag = document.get('persona_consistency_engine', {})
        if rag.get('enabled'):
            vs = rag.get('vector_store', {})
            print(f"   RAG: {vs.get('provider', 'N/A')} ({vs.get('embedding_model', 'N/A')})")
            retrieval = rag.get('retrieval_config', {})
            print(f"   Retrieval: top_k={retrieval.get('top_k', 10)}, threshold={retrieval.get('similarity_threshold', 0.75)}")
        adaptation = document.get('real_time_adaptation', {})
        if adaptation.get('enabled'):
            triggers = adaptation.get('adaptation_triggers', [])
            print(f"   Real-time Adaptation: {len(triggers)} triggers")
        cot = document.get('chain_of_thought', {})
        if cot.get('enabled'):
            print(f"   Chain of Thought: {cot.get('reasoning_format', 'structured')}")
        context = document.get('multi_turn_context', {})
        if context.get('enabled'):
            print(f"   Multi-turn Context: max {context.get('max_turns', 50)} turns")
        guardrails = document.get('guardrails', {})
        enabled_guards = sum(1 for k, v in guardrails.items() if v is True)
        print(f"   Guardrails: {enabled_guards} active")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_emotion_ai(file_path: Path) -> bool:
    """Validate an Emotion AI JSON file."""
    print(f"\n😊 Validating Emotion AI: {file_path}")
    
    schema = load_schema(EMOTION_AI_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Emotion AI is valid!")
        print(f"   ID: {document.get('emotion_engine_id')}")
        print(f"   Version: {document.get('version')}")
        taxonomy = document.get('emotion_taxonomy', {})
        if taxonomy:
            primary = len(taxonomy.get('primary_emotions', []))
            secondary = len(taxonomy.get('secondary_emotions', []))
            print(f"   Taxonomy: {primary} primary, {secondary} secondary emotions")
        analysis = document.get('text_emotion_analysis', {})
        if analysis.get('enabled'):
            models = analysis.get('models', [])
            print(f"   Text Analysis: {len(models)} models")
            for m in models:
                print(f"     • {m.get('model_name')} ({m.get('model_type')}) - {m.get('accuracy', 0)*100:.0f}% accuracy")
        synthesis = document.get('emotion_synthesis', {})
        if synthesis.get('enabled'):
            method = synthesis.get('synthesis_method', 'neural')
            mappings = len(synthesis.get('emotion_to_prosody_mapping', {}))
            print(f"   Synthesis: {method} ({mappings} emotion mappings)")
            blending = synthesis.get('emotion_blending', {})
            if blending.get('enabled'):
                print(f"   Blending: {blending.get('blending_method', 'linear')}, max {blending.get('max_simultaneous_emotions', 3)} emotions")
        transfer = document.get('emotion_transfer', {})
        if transfer.get('enabled'):
            refs = len(transfer.get('reference_types', []))
            encoder = transfer.get('style_encoder', {})
            print(f"   Transfer: {encoder.get('architecture', 'N/A')} encoder, {refs} reference types")
        tracking = document.get('real_time_emotion_tracking', {})
        if tracking.get('enabled'):
            sources = len(tracking.get('tracking_sources', []))
            voice = tracking.get('user_voice_analysis', {})
            if voice.get('enabled'):
                print(f"   Real-time Tracking: {sources} sources, {voice.get('update_rate_hz', 10)}Hz voice analysis")
        memory = document.get('emotion_memory', {})
        enabled_features = sum(1 for k, v in memory.items() if v is True)
        if enabled_features > 0:
            print(f"   Emotion Memory: {enabled_features} features")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_voice_cloning_pipeline(file_path: Path) -> bool:
    """Validate a Voice Cloning Pipeline JSON file."""
    print(f"\n🎙️ Validating Voice Cloning Pipeline: {file_path}")
    
    schema = load_schema(VOICE_CLONING_PIPELINE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Voice Cloning Pipeline is valid!")
        print(f"   Pipeline ID: {document.get('pipeline_id')}")
        print(f"   Artist ID: {document.get('artist_id')}")
        print(f"   Status: {document.get('status')}")
        session = document.get('recording_session', {})
        if session:
            print(f"   Session Type: {session.get('session_type', 'N/A')}")
            coverage = session.get('script_coverage', {})
            if coverage:
                print(f"   Phoneme Coverage: {coverage.get('phoneme_coverage_percent', 0):.1f}%")
            script = session.get('recording_script', {})
            if script:
                print(f"   Script: {script.get('total_sentences', 0)} sentences")
        processing = document.get('audio_processing', {})
        if processing:
            seg = processing.get('segmentation', {})
            print(f"   Segmentation: {seg.get('method', 'N/A')} ({seg.get('granularity', 'N/A')})")
        training = document.get('model_training', {})
        if training:
            arch = training.get('architecture', {})
            print(f"   Model: {arch.get('base_model', 'N/A')} + {arch.get('vocoder', 'N/A')}")
            config = training.get('training_config', {})
            if config:
                print(f"   Training: {config.get('epochs', 0)} epochs, {config.get('gpu_count', 1)}x {config.get('gpu_type', 'GPU')}")
                if config.get('estimated_training_hours'):
                    print(f"   Estimated Time: {config.get('estimated_training_hours')}h")
        validation = document.get('validation', {})
        if validation:
            auto = validation.get('automatic_metrics', {})
            mos = auto.get('mos_prediction', {})
            sim = auto.get('speaker_similarity', {})
            if mos or sim:
                print(f"   Metrics: MOS>{mos.get('threshold', 4.0)}, Similarity>{sim.get('threshold', 0.85)}")
            human = validation.get('human_evaluation', {})
            if human.get('required'):
                print(f"   Human Eval: {human.get('evaluator_count', 5)} evaluators, {human.get('evaluation_samples', 20)} samples")
        opt = document.get('model_optimization', {})
        if opt:
            quant = opt.get('quantization', {})
            exports = opt.get('export_formats', [])
            if quant.get('enabled'):
                print(f"   Optimization: {quant.get('precision', 'fp16')} ({quant.get('method', 'ptq')})")
            if exports:
                print(f"   Export Formats: {', '.join(exports)}")
        versioning = document.get('versioning', {})
        if versioning:
            print(f"   Version: {versioning.get('model_version', 'N/A')}")
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_agentic_voice(file_path: Path) -> bool:
    """Validate an Agentic Voice JSON file."""
    print(f"\n🤖 Validating Agentic Voice: {file_path}")
    
    schema = load_schema(AGENTIC_VOICE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Agentic Voice is valid!")
        print(f"   Agent ID: {document.get('agent_id')}")
        print(f"   Name: {document.get('name')}")
        print(f"   Agent Type: {document.get('agent_type')}")
        print(f"   Persona ID: {document.get('persona_id')}")
        
        # LLM Backbone
        llm = document.get('llm_backbone', {})
        if llm:
            print(f"   LLM: {llm.get('provider', 'N/A')}/{llm.get('model', 'N/A')}")
            few_shot = llm.get('few_shot_examples', [])
            if few_shot:
                print(f"   Few-Shot Examples: {len(few_shot)}")
        
        # Voice Interaction
        voice = document.get('voice_interaction', {})
        if voice:
            stt = voice.get('speech_to_text', {})
            tts = voice.get('text_to_speech', {})
            turn = voice.get('turn_taking', {})
            if stt:
                print(f"   STT: {stt.get('provider', 'N/A')}/{stt.get('model', 'N/A')}")
            if tts.get('streaming_enabled'):
                print(f"   TTS: Streaming enabled (chunk: {tts.get('chunk_size_ms', 50)}ms)")
            if turn:
                print(f"   Turn-Taking: {turn.get('model', 'N/A')} (barge-in: {turn.get('barge_in_enabled', False)})")
        
        # Conversation Management
        conv = document.get('conversation_management', {})
        if conv:
            ctx = conv.get('context_window', {})
            mem = conv.get('memory', {})
            if ctx:
                print(f"   Context: {ctx.get('max_tokens', 0)} tokens, {ctx.get('max_turns', 0)} turns")
            if mem:
                mem_types = []
                if mem.get('short_term'): mem_types.append('short')
                if mem.get('long_term'): mem_types.append('long')
                if mem.get('episodic'): mem_types.append('episodic')
                if mem.get('semantic'): mem_types.append('semantic')
                if mem_types:
                    print(f"   Memory: {', '.join(mem_types)}")
        
        # Function Calling
        func = document.get('function_calling', {})
        if func:
            functions = func.get('available_functions', [])
            mcp = func.get('mcp_integration', {})
            if functions:
                print(f"   Functions: {len(functions)} available")
            if mcp.get('enabled'):
                servers = mcp.get('servers', [])
                print(f"   MCP Servers: {len(servers)} connected")
        
        # Personality
        personality = document.get('personality', {})
        if personality:
            traits = personality.get('traits', {})
            style = personality.get('communication_style', {})
            if traits:
                top_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)[:3]
                trait_strs = [f"{k}:{v:.1f}" for k, v in top_traits]
                print(f"   Top Traits: {', '.join(trait_strs)}")
            if style:
                print(f"   Style: formality={style.get('formality', 0.5):.1f}, humor={style.get('humor', 0.3):.1f}")
        
        # Guardrails
        guardrails = document.get('guardrails', {})
        if guardrails:
            content = guardrails.get('content_policy', {})
            safety = guardrails.get('safety', {})
            if content:
                prohibited = content.get('prohibited_topics', [])
                print(f"   Content Policy: {len(prohibited)} prohibited topics")
            if safety.get('crisis_detection'):
                print(f"   Crisis Detection: enabled")
        
        # Deployment
        deploy = document.get('deployment', {})
        if deploy:
            channels = deploy.get('channels', [])
            if channels:
                print(f"   Channels: {', '.join(channels)}")
            latency = deploy.get('performance', {}).get('target_latency_ms')
            if latency:
                print(f"   Target Latency: {latency}ms")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_multimodal_sync(file_path: Path) -> bool:
    """Validate a Multimodal Sync JSON file."""
    print(f"\n🎬 Validating Multimodal Sync: {file_path}")
    
    schema = load_schema(MULTIMODAL_SYNC_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Multimodal Sync is valid!")
        print(f"   Sync ID: {document.get('sync_id')}")
        print(f"   Version: {document.get('version')}")
        
        # Video to Voice
        v2v = document.get('video_to_voice', {})
        if v2v.get('enabled'):
            lip = v2v.get('lip_reading', {})
            dub = v2v.get('dubbing_mode', {})
            if lip.get('enabled'):
                print(f"   Lip Reading: {lip.get('model', 'N/A')}")
            if dub.get('enabled'):
                print(f"   Dubbing: {dub.get('target_language', 'N/A')}")
        
        # Voice to Animation
        v2a = document.get('voice_to_animation', {})
        if v2a.get('enabled'):
            face = v2a.get('face_animation', {})
            if face:
                print(f"   Face Animation: {face.get('method', 'N/A')} -> {face.get('output_format', 'N/A')}")
                print(f"   FPS: {face.get('fps', 60)}, Blendshapes: {face.get('blendshape_set', 'N/A')}")
            head = v2a.get('head_motion', {})
            body = v2a.get('body_gesture', {})
            if head.get('enabled'):
                print(f"   Head Motion: {head.get('method', 'N/A')}")
            if body.get('enabled'):
                print(f"   Body Gesture: {body.get('method', 'N/A')}")
        
        # Image to Talking Head
        i2th = document.get('image_to_talking_head', {})
        if i2th.get('enabled'):
            res = i2th.get('output_resolution', {})
            print(f"   Talking Head: {i2th.get('animation_method', 'N/A')}")
            print(f"   Resolution: {res.get('width', 512)}x{res.get('height', 512)}")
        
        # Avatar Integration
        avatar = document.get('avatar_integration', {})
        if avatar.get('enabled'):
            print(f"   Avatar: {avatar.get('avatar_format', 'N/A')}")
            render = avatar.get('rendering', {})
            if render:
                print(f"   Rendering: {render.get('engine', 'N/A')} ({render.get('quality_preset', 'N/A')})")
            stream = avatar.get('streaming', {})
            if stream.get('enabled'):
                print(f"   Streaming: {stream.get('protocol', 'N/A')} ({stream.get('latency_mode', 'N/A')})")
        
        # Real-time Sync
        rts = document.get('real_time_sync', {})
        if rts.get('enabled'):
            print(f"   Real-time: {rts.get('target_latency_ms', 100)}ms target, {rts.get('sync_strategy', 'N/A')}")
        
        # Video Generation
        vg = document.get('video_generation', {})
        if vg.get('enabled'):
            out = vg.get('output_settings', {})
            print(f"   Video Gen: {vg.get('model', 'N/A')}")
            print(f"   Output: {out.get('resolution', 'N/A')} @ {out.get('fps', 24)}fps")
        
        # Motion Capture
        mocap = document.get('motion_capture', {})
        if mocap.get('enabled'):
            track = mocap.get('tracking', {})
            tracked = [k for k, v in track.items() if v]
            print(f"   MoCap: {mocap.get('input_source', 'N/A')} ({', '.join(tracked)})")
        
        # Output Formats
        out = document.get('output_formats', {})
        if out:
            vid = out.get('video', {})
            if vid:
                print(f"   Video Output: {vid.get('codec', 'N/A')}/{vid.get('container', 'N/A')}")
        
        # Performance
        perf = document.get('performance', {})
        if perf:
            print(f"   GPU: {perf.get('gpu_acceleration', False)}, Precision: {perf.get('precision', 'fp32')}")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_supersonic_pipeline(file_path: Path) -> bool:
    """Validate a Supersonic Pipeline JSON file."""
    print(f"\n🚀 Validating Supersonic Pipeline: {file_path}")
    
    schema = load_schema(SUPERSONIC_PIPELINE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ Supersonic Pipeline is valid!")
        print(f"   Pipeline ID: {document.get('pipeline_id')}")
        print(f"   Version: {document.get('version')}")
        if document.get('name'):
            print(f"   Name: {document.get('name')}")
        if document.get('active_tier'):
            print(f"   Active Tier: {document.get('active_tier')}")
        
        # Recommended Stack
        stack = document.get('recommended_stack', {})
        if stack:
            tiers = [k for k in stack.keys()]
            print(f"   Tiers Available: {', '.join(tiers)}")
        
        # Pipeline Stages
        stages = document.get('pipeline_stages', [])
        if stages:
            gpu_stages = sum(1 for s in stages if s.get('gpu_required'))
            stream_stages = sum(1 for s in stages if s.get('can_stream'))
            print(f"   Stages: {len(stages)} total, {gpu_stages} GPU, {stream_stages} streamable")
            total_latency = sum(s.get('latency_target_ms', 0) for s in stages)
            print(f"   Total Latency Target: {total_latency}ms")
        
        # Model Registry
        registry = document.get('model_registry', {})
        if registry:
            commercial = sum(1 for m in registry.values() if m.get('commercial_use'))
            print(f"   Models Registered: {len(registry)} ({commercial} commercial-friendly)")
        
        # Performance Benchmarks
        bench = document.get('performance_benchmarks', {})
        if bench:
            print(f"   RTF Target: {bench.get('rtf_target', 'N/A')} ({int(1/bench.get('rtf_target', 1))}x real-time)")
            print(f"   First Byte: {bench.get('first_byte_ms', 'N/A')}ms")
            print(f"   MOS Target: {bench.get('quality_mos_target', 'N/A')}")
        
        # Cost Comparison
        cost = document.get('cost_comparison', {})
        if cost:
            savings = cost.get('savings_percent', 0)
            print(f"   Cost Savings: {savings}% vs commercial")
            infra = cost.get('infrastructure_monthly_cost', {})
            if infra.get('total'):
                print(f"   Monthly Infra: ${infra.get('total')}")
        
        # Hardware Requirements
        hw = document.get('hardware_requirements', {})
        if hw:
            t1 = hw.get('tier_1_premium', {})
            if t1:
                print(f"   Tier 1 GPU: {t1.get('gpu', 'N/A')}")
        
        # Optimization
        opt = document.get('optimization_settings', {})
        if opt:
            features = []
            if opt.get('batching', {}).get('enabled'): features.append('batching')
            if opt.get('caching', {}).get('enabled'): features.append('caching')
            if opt.get('streaming', {}).get('enabled'): features.append('streaming')
            if opt.get('quantization', {}).get('enabled'): 
                features.append(f"quant({opt.get('quantization', {}).get('precision', 'fp16')})")
            if features:
                print(f"   Optimizations: {', '.join(features)}")
        
        # Fallback Chain
        fallbacks = document.get('fallback_chain', [])
        if fallbacks:
            print(f"   Fallback Chains: {len(fallbacks)} components")
        
        # Quality Gates
        gates = document.get('quality_gates', {})
        if gates:
            print(f"   Quality Gates: MOS>{gates.get('mos_minimum', 3.8)}, Similarity>{gates.get('speaker_similarity_minimum', 0.8)}")
        
        # Monitoring
        mon = document.get('monitoring', {})
        if mon.get('enabled'):
            print(f"   Monitoring: {mon.get('log_level', 'info')}, sample={mon.get('sample_rate', 0.1)}")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_openai_voice_integration(file_path: Path) -> bool:
    """Validate an OpenAI Voice Integration JSON file."""
    print(f"\n🤖 Validating OpenAI Voice Integration: {file_path}")
    
    schema = load_schema(OPENAI_VOICE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ OpenAI Voice Integration is valid!")
        print(f"   Integration ID: {document.get('integration_id')}")
        print(f"   Version: {document.get('version')}")
        print(f"   Provider: {document.get('provider')}")
        
        # TTS Models
        tts = document.get('tts_models', {})
        if tts:
            enabled = [k for k, v in tts.items() if v.get('enabled')]
            print(f"   TTS Models: {len(enabled)} enabled")
            for name, cfg in tts.items():
                if cfg.get('enabled'):
                    pricing = cfg.get('pricing', {})
                    cost_str = ""
                    if pricing.get('per_1m_chars'):
                        cost_str = f"${pricing.get('per_1m_chars')}/1M chars"
                    elif pricing.get('per_minute_audio'):
                        cost_str = f"${pricing.get('per_minute_audio')}/min"
                    print(f"     • {cfg.get('model_id', name)}: {cfg.get('use_case', '')} ({cost_str})")
        
        # ASR Models
        asr = document.get('asr_models', {})
        if asr:
            enabled = [k for k, v in asr.items() if v.get('enabled')]
            print(f"   ASR Models: {len(enabled)} enabled")
            for name, cfg in asr.items():
                if cfg.get('enabled'):
                    pricing = cfg.get('pricing', {})
                    cost_str = f"${pricing.get('per_minute', 'N/A')}/min"
                    print(f"     • {cfg.get('model_id', name)}: {cfg.get('use_case', '')} ({cost_str})")
        
        # Realtime Models
        realtime = document.get('realtime_models', {})
        if realtime:
            enabled = [k for k, v in realtime.items() if v.get('enabled')]
            print(f"   Realtime Models: {len(enabled)} enabled")
            for name, cfg in realtime.items():
                if cfg.get('enabled'):
                    conn = cfg.get('connection_methods', [])
                    print(f"     • {cfg.get('model_id', name)}: {cfg.get('use_case', '')} ({', '.join(conn)})")
        
        # Voice Presets
        voices = document.get('voice_presets', {})
        if voices:
            print(f"   Voice Presets: {len(voices)}")
            voice_list = [v.get('voice_id', k) for k, v in voices.items()]
            print(f"     {', '.join(voice_list[:5])}{'...' if len(voice_list) > 5 else ''}")
        
        # Architecture
        arch = document.get('voice_agent_architecture', {})
        if arch:
            s2s = arch.get('speech_to_speech', {})
            chained = arch.get('chained', {})
            if s2s.get('enabled'):
                print(f"   Speech-to-Speech: {s2s.get('model', 'enabled')}")
            if chained.get('enabled'):
                pipeline = chained.get('pipeline', [])
                print(f"   Chained: {' → '.join(pipeline)}")
        
        # Recommendations
        recs = document.get('noizyvox_recommendations', {})
        if recs:
            tts_strat = recs.get('tts_strategy', {})
            if tts_strat.get('hybrid_recommendation'):
                print(f"   Strategy: {tts_strat.get('hybrid_recommendation')[:60]}...")
        
        # Hybrid
        hybrid = document.get('hybrid_architecture', {})
        if hybrid and hybrid.get('enabled'):
            print(f"   Hybrid Mode: Enabled")
            savings = hybrid.get('estimated_savings', {})
            if savings:
                print(f"   Savings: TTS bulk {savings.get('tts_bulk', 'N/A')}, ASR bulk {savings.get('asr_bulk', 'N/A')}")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_oss_integrations(file_path: Path) -> bool:
    """Validate an Open Source Integrations JSON file."""
    print(f"\n🔧 Validating OSS Integrations: {file_path}")
    
    schema = load_schema(OSS_INTEGRATIONS_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ OSS Integrations is valid!")
        print(f"   Integration ID: {document.get('integration_id')}")
        print(f"   Version: {document.get('version')}")
        if document.get('name'):
            print(f"   Name: {document.get('name')}")
        
        # TTS Models
        tts = document.get('tts_models', {})
        if tts:
            enabled = [k for k, v in tts.items() if v.get('enabled')]
            commercial = [k for k, v in tts.items() if v.get('enabled') and v.get('commercial_use')]
            print(f"   TTS Models: {len(enabled)} enabled ({len(commercial)} commercial)")
        
        # ASR Models
        asr = document.get('asr_models', {})
        if asr:
            enabled = [k for k, v in asr.items() if v.get('enabled')]
            print(f"   ASR Models: {len(enabled)} enabled")
        
        # Vocoder Models
        voc = document.get('vocoder_models', {})
        if voc:
            enabled = [k for k, v in voc.items() if v.get('enabled')]
            print(f"   Vocoders: {len(enabled)} enabled")
        
        # Lip Sync Models
        lip = document.get('lip_sync_models', {})
        if lip:
            enabled = [k for k, v in lip.items() if v.get('enabled')]
            commercial = [k for k, v in lip.items() if v.get('enabled') and v.get('commercial_use')]
            print(f"   Lip Sync: {len(enabled)} enabled ({len(commercial)} commercial)")
        
        # Emotion Models
        emo = document.get('emotion_models', {})
        if emo:
            enabled = [k for k, v in emo.items() if v.get('enabled')]
            print(f"   Emotion: {len(enabled)} enabled")
        
        # Embedding Models
        emb = document.get('embedding_models', {})
        if emb:
            enabled = [k for k, v in emb.items() if v.get('enabled')]
            print(f"   Embeddings: {len(enabled)} enabled")
        
        # LLM Models
        llm = document.get('llm_models', {})
        if llm:
            enabled = [k for k, v in llm.items() if v.get('enabled')]
            for name, cfg in llm.items():
                if cfg.get('enabled'):
                    config = cfg.get('config', {})
                    print(f"   LLM: {name} {cfg.get('version', '')} ({config.get('model_size', 'N/A')}, {config.get('backend', 'N/A')})")
        
        # Audio Enhancement
        enh = document.get('audio_enhancement', {})
        if enh:
            enabled = [k for k, v in enh.items() if v.get('enabled')]
            print(f"   Audio Enhancement: {len(enabled)} enabled")
        
        # Vector Databases
        vdb = document.get('vector_databases', {})
        if vdb:
            enabled = [k for k, v in vdb.items() if v.get('enabled')]
            print(f"   Vector DBs: {', '.join(enabled)}")
        
        # Runtime Config
        runtime = document.get('runtime_config', {})
        if runtime:
            print(f"   Device: {runtime.get('device', 'auto')}")
            if runtime.get('model_cache_dir'):
                print(f"   Cache: {runtime.get('model_cache_dir')}")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def validate_openai_voice_complete(file_path: Path) -> bool:
    """Validate an OpenAI Voice Complete JSON file."""
    print(f"\n🎤 Validating OpenAI Voice Complete: {file_path}")
    
    schema = load_schema(OPENAI_VOICE_COMPLETE_SCHEMA)
    with open(file_path, 'r') as f:
        document = json.load(f)
    
    is_valid, errors = validate_document(document, schema)
    
    if is_valid:
        print("✅ OpenAI Voice Complete is valid!")
        print(f"   Integration ID: {document.get('integration_id')}")
        print(f"   Version: {document.get('version')}")
        if document.get('name'):
            print(f"   Name: {document.get('name')}")
        
        # OpenAI Audio Model Family
        family = document.get('openai_audio_model_family', {})
        if family:
            tts = family.get('text_to_speech_models', [])
            asr = family.get('speech_to_text_models', [])
            realtime = family.get('realtime_speech_models', [])
            audio_preview = family.get('audio_preview_models', [])
            print(f"   TTS Models: {len(tts)}")
            print(f"   ASR Models: {len(asr)}")
            print(f"   Realtime Models: {len(realtime)}")
            print(f"   Audio Preview Models: {len(audio_preview)}")
        
        # Voice Engine Preview
        engine = document.get('voice_engine_preview', {})
        if engine:
            print(f"   Voice Engine: {engine.get('status', 'N/A')}")
        
        # Voice Characteristics
        chars = document.get('voice_characteristics', {})
        if chars:
            standard = chars.get('standard_voices', [])
            extended = chars.get('extended_voices', [])
            exclusive = chars.get('exclusive_realtime_voices', [])
            print(f"   Voices: {len(standard)} standard, {len(extended)} extended, {len(exclusive)} exclusive")
        
        # Instruction Guided Synthesis
        igs = document.get('instruction_guided_synthesis', {})
        if igs:
            caps = igs.get('capabilities', {})
            emotion = caps.get('emotion_control', {})
            styles = caps.get('speaking_style_control', {})
            if emotion:
                emotions = emotion.get('supported_emotions', [])
                print(f"   Supported Emotions: {len(emotions)}")
            if styles:
                style_list = styles.get('supported_styles', [])
                print(f"   Speaking Styles: {len(style_list)}")
        
        # API Architecture
        api = document.get('api_architecture', {})
        if api:
            rest = api.get('rest_endpoints', {})
            ws = api.get('websocket_endpoints', {})
            webrtc = api.get('webrtc_endpoints', {})
            print(f"   API Endpoints: {len(rest)} REST, {len(ws)} WebSocket, {len(webrtc)} WebRTC")
        
        # SDK Ecosystem
        sdk = document.get('sdk_ecosystem', {})
        if sdk:
            official = sdk.get('official_sdks', [])
            azure = sdk.get('azure_openai_sdk', {})
            print(f"   Official SDKs: {len(official)}")
            if azure:
                print(f"   Azure SDK: {azure.get('name', 'Available')}")
        
        # Pricing
        pricing = document.get('pricing_complete', {})
        if pricing:
            tts_pricing = pricing.get('text_to_speech', {})
            asr_pricing = pricing.get('speech_to_text', {})
            realtime_pricing = pricing.get('realtime_api', {})
            print(f"   Pricing: {len(tts_pricing)} TTS, {len(asr_pricing)} ASR, {len(realtime_pricing)} Realtime")
        
        # NOIZYVOX Recommendations
        recs = document.get('noizyvox_recommendations', {})
        if recs:
            tiers = [k for k in recs.keys() if 'tier' in k.lower()]
            strategies = [k for k in recs.keys() if 'strategy' in k.lower()]
            print(f"   Recommendations: {len(tiers)} tiers, {len(strategies)} strategies")
        
        return True
    else:
        print("❌ Validation errors:")
        for error in errors:
            print(f"   • {error}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="NOIZYVOX Schema Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate sample files
  python noizyvox_schema_validator.py --generate-samples
  
  # Validate a persona pack
  python noizyvox_schema_validator.py --persona path/to/persona.json
  
  # Validate an artifact manifest
  python noizyvox_schema_validator.py --manifest path/to/manifest.json
  
  # Validate all JSON files in a directory
  python noizyvox_schema_validator.py --validate-dir path/to/personas/
        """
    )
    
    parser.add_argument('--persona', type=Path, help='Validate a persona pack JSON file')
    parser.add_argument('--manifest', type=Path, help='Validate an artifact manifest JSON file')
    parser.add_argument('--validate-dir', type=Path, help='Validate all JSON files in directory')
    parser.add_argument('--generate-samples', action='store_true', help='Generate sample JSON files')
    parser.add_argument('--output-dir', type=Path, default=Path('.'), help='Output directory for samples')
    
    args = parser.parse_args()
    
    if args.generate_samples:
        output_dir = args.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate sample persona pack
        persona = create_sample_persona_pack()
        persona_file = output_dir / "sample_persona_pack.json"
        with open(persona_file, 'w') as f:
            json.dump(persona, f, indent=2)
        print(f"✅ Created sample persona pack: {persona_file}")
        
        # Generate sample manifest
        manifest = create_sample_manifest(persona['persona_id'])
        manifest_file = output_dir / "sample_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"✅ Created sample manifest: {manifest_file}")
        
        # Validate the samples
        print("\n--- Validating generated samples ---")
        validate_persona_pack(persona_file)
        validate_manifest(manifest_file)
        return
    
    if args.persona:
        validate_persona_pack(args.persona)
        return
    
    if args.manifest:
        validate_manifest(args.manifest)
        return
    
    if args.validate_dir:
        json_files = list(args.validate_dir.glob("*.json"))
        if not json_files:
            print(f"No JSON files found in {args.validate_dir}")
            return
        
        print(f"Found {len(json_files)} JSON files")
        
        for json_file in json_files:
            # Try to detect type based on content
            # Order matters: license_id before consent_id since licenses also have consent_id
            with open(json_file, 'r') as f:
                try:
                    doc = json.load(f)
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {json_file}")
                    continue
            
            if 'manifest_id' in doc:
                validate_manifest(json_file)
            elif 'sync_id' in doc:
                validate_multimodal_sync(json_file)
            elif 'integration_id' in doc:
                # Differentiate between OpenAI Complete (oai_), OpenAI Voice (oai_voice_), and OSS (oss_) integrations
                iid = doc.get('integration_id', '')
                if iid.startswith('oai_') and not iid.startswith('oai_voice_'):
                    # OpenAI Voice Complete (new comprehensive schema)
                    validate_openai_voice_complete(json_file)
                elif iid.startswith('oai_voice_') or doc.get('provider') == 'openai':
                    # OpenAI Voice Integration (legacy schema)
                    validate_openai_voice_integration(json_file)
                else:
                    # OSS integrations (oss_ prefix)
                    validate_oss_integrations(json_file)
            elif 'agent_id' in doc:
                validate_agentic_voice(json_file)
            elif 'orchestration_id' in doc:
                validate_llm_orchestration(json_file)
            elif 'emotion_engine_id' in doc:
                validate_emotion_ai(json_file)
            elif 'pipeline_id' in doc:
                # Differentiate between voice cloning (clone_) and supersonic (sonic_) pipelines
                pid = doc.get('pipeline_id', '')
                if pid.startswith('sonic_'):
                    validate_supersonic_pipeline(json_file)
                else:
                    validate_voice_cloning_pipeline(json_file)
            elif 'experiment_id' in doc:
                validate_experiment(json_file)
            elif 'dispute_id' in doc:
                validate_dispute(json_file)
            elif 'estate_plan_id' in doc:
                validate_estate_plan(json_file)
            elif 'guild_id' in doc:
                validate_guild_governance(json_file)
            elif 'spatial_config_id' in doc:
                validate_vr_ar_spatial(json_file)
            elif 'plugin_id' in doc:
                validate_daw_plugin(json_file)
            elif 'sdk_id' in doc:
                validate_game_engine_sdk(json_file)
            elif 'dashboard_id' in doc:
                validate_analytics_dashboard(json_file)
            elif 'watermark' in doc and 'watermark_id' in doc.get('watermark', {}):
                validate_security_watermark(json_file)
            elif 'deployment_id' in doc:
                # Differentiate between enterprise (ent_) and edge (edge_) deployments
                dep_id = doc.get('deployment_id', '')
                if dep_id.startswith('ent_') or 'organization' in doc:
                    validate_enterprise_deployment(json_file)
                else:
                    validate_edge_deployment(json_file)
            elif 'automation_id' in doc:
                validate_automation(json_file)
            elif 'license_id' in doc:
                validate_license(json_file)
            elif 'revocation_id' in doc:
                validate_revocation(json_file)
            elif 'consent_id' in doc:
                validate_consent(json_file)
            elif 'persona_id' in doc:
                validate_persona_pack(json_file)
            else:
                print(f"⚠️  Unknown document type: {json_file}")
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()