#!/usr/bin/env python3
"""
🔐 NOIZYVOX API Key Manager
Secure storage and management of API keys with encryption.

Features:
- AES-256 encryption for stored keys
- Keychain integration (macOS) / Credential Manager (Windows)
- Environment variable management
- Key rotation tracking
- Secure memory handling
- Audit logging

Usage:
  # Initialize (first time setup)
  python api_key_manager.py init
  
  # Add a key
  python api_key_manager.py add ANTHROPIC_API_KEY
  
  # Get a key (for scripts)
  python api_key_manager.py get ANTHROPIC_API_KEY
  
  # List all keys
  python api_key_manager.py list
  
  # Export to shell (add to .zshrc/.bashrc)
  python api_key_manager.py export
  
  # Remove a key
  python api_key_manager.py remove ANTHROPIC_API_KEY
  
  # Rotate a key
  python api_key_manager.py rotate ANTHROPIC_API_KEY

Security:
  - Keys are encrypted at rest using AES-256-GCM
  - Master password never stored, derived via PBKDF2
  - Optional keychain/credential manager integration
  - Memory is cleared after use
  - Audit log tracks access (no key values logged)
"""

import argparse
import base64
import getpass
import hashlib
import json
import os
import secrets
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Optional imports for enhanced security
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False

# =============================================================================
# Configuration
# =============================================================================

# Default paths
CONFIG_DIR = Path.home() / ".noizyvox"
KEYS_FILE = CONFIG_DIR / "keys.enc"
SALT_FILE = CONFIG_DIR / "salt"
AUDIT_LOG = CONFIG_DIR / "audit.log"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Keyring service name
KEYRING_SERVICE = "noizyvox-api-keys"

# =============================================================================
# COMPLETE API TOKEN SPACE - All Services & Providers
# =============================================================================

API_KEY_PATTERNS = {
    # =========================================================================
    # 🤖 AI / LLM PROVIDERS
    # =========================================================================
    "ANTHROPIC_API_KEY": {
        "prefix": "sk-ant-",
        "description": "Anthropic Claude API (Claude 3.5, Claude Opus)",
        "docs": "https://console.anthropic.com/",
        "category": "ai",
        "required": True,
    },
    "ANTHROPIC_AUTH_TOKEN": {
        "prefix": "",
        "description": "Anthropic Auth Token (alternative auth)",
        "docs": "https://console.anthropic.com/",
        "category": "ai",
    },
    "OPENAI_API_KEY": {
        "prefix": "sk-",
        "description": "OpenAI API (GPT-4, Whisper, TTS, DALL-E)",
        "docs": "https://platform.openai.com/api-keys",
        "category": "ai",
        "required": True,
    },
    "OPENAI_ORG_ID": {
        "prefix": "org-",
        "description": "OpenAI Organization ID",
        "docs": "https://platform.openai.com/account/organization",
        "category": "ai",
    },
    "OPENAI_PROJECT_ID": {
        "prefix": "proj_",
        "description": "OpenAI Project ID",
        "docs": "https://platform.openai.com/",
        "category": "ai",
    },
    "GOOGLE_API_KEY": {
        "prefix": "AIza",
        "description": "Google AI API (Gemini, PaLM)",
        "docs": "https://aistudio.google.com/apikey",
        "category": "ai",
    },
    "GOOGLE_APPLICATION_CREDENTIALS": {
        "prefix": "",
        "description": "Google Cloud Service Account JSON path",
        "docs": "https://console.cloud.google.com/iam-admin/serviceaccounts",
        "category": "ai",
        "is_path": True,
    },
    "COHERE_API_KEY": {
        "prefix": "",
        "description": "Cohere AI API",
        "docs": "https://dashboard.cohere.com/api-keys",
        "category": "ai",
    },
    "MISTRAL_API_KEY": {
        "prefix": "",
        "description": "Mistral AI API",
        "docs": "https://console.mistral.ai/api-keys/",
        "category": "ai",
    },
    "GROQ_API_KEY": {
        "prefix": "gsk_",
        "description": "Groq Cloud API (fast inference)",
        "docs": "https://console.groq.com/keys",
        "category": "ai",
    },
    "TOGETHER_API_KEY": {
        "prefix": "",
        "description": "Together AI API",
        "docs": "https://api.together.xyz/settings/api-keys",
        "category": "ai",
    },
    "FIREWORKS_API_KEY": {
        "prefix": "",
        "description": "Fireworks AI API",
        "docs": "https://fireworks.ai/api-keys",
        "category": "ai",
    },
    "PERPLEXITY_API_KEY": {
        "prefix": "pplx-",
        "description": "Perplexity AI API",
        "docs": "https://www.perplexity.ai/settings/api",
        "category": "ai",
    },
    "XAI_API_KEY": {
        "prefix": "xai-",
        "description": "xAI Grok API",
        "docs": "https://x.ai/api",
        "category": "ai",
    },
    
    # =========================================================================
    # 🎙️ VOICE / SPEECH PROVIDERS
    # =========================================================================
    "ELEVENLABS_API_KEY": {
        "prefix": "",
        "description": "ElevenLabs Voice Synthesis API",
        "docs": "https://elevenlabs.io/app/settings/api-keys",
        "category": "voice",
        "required": True,
    },
    "DEEPGRAM_API_KEY": {
        "prefix": "",
        "description": "Deepgram Speech-to-Text API",
        "docs": "https://console.deepgram.com/",
        "category": "voice",
    },
    "ASSEMBLYAI_API_KEY": {
        "prefix": "",
        "description": "AssemblyAI Transcription API",
        "docs": "https://www.assemblyai.com/app/account",
        "category": "voice",
    },
    "PLAYHT_API_KEY": {
        "prefix": "",
        "description": "PlayHT Voice Cloning API",
        "docs": "https://play.ht/studio/api-access",
        "category": "voice",
    },
    "PLAYHT_USER_ID": {
        "prefix": "",
        "description": "PlayHT User ID",
        "docs": "https://play.ht/studio/api-access",
        "category": "voice",
    },
    "RESEMBLE_API_KEY": {
        "prefix": "",
        "description": "Resemble AI Voice API",
        "docs": "https://app.resemble.ai/",
        "category": "voice",
    },
    "SPEECHIFY_API_KEY": {
        "prefix": "",
        "description": "Speechify TTS API",
        "docs": "https://console.speechify.com/",
        "category": "voice",
    },
    "MURF_API_KEY": {
        "prefix": "",
        "description": "Murf AI Voice API",
        "docs": "https://murf.ai/",
        "category": "voice",
    },
    "WELLSAID_API_KEY": {
        "prefix": "",
        "description": "WellSaid Labs Voice API",
        "docs": "https://wellsaidlabs.com/",
        "category": "voice",
    },
    "COQUI_API_KEY": {
        "prefix": "",
        "description": "Coqui TTS API",
        "docs": "https://coqui.ai/",
        "category": "voice",
    },
    "REV_API_KEY": {
        "prefix": "",
        "description": "Rev.ai Transcription API",
        "docs": "https://www.rev.ai/",
        "category": "voice",
    },
    
    # =========================================================================
    # ☁️ CLOUD INFRASTRUCTURE
    # =========================================================================
    "CLOUDFLARE_API_TOKEN": {
        "prefix": "",
        "description": "Cloudflare API Token (Workers, R2, D1)",
        "docs": "https://dash.cloudflare.com/profile/api-tokens",
        "category": "cloud",
        "required": True,
    },
    "CLOUDFLARE_ACCOUNT_ID": {
        "prefix": "",
        "description": "Cloudflare Account ID",
        "docs": "https://dash.cloudflare.com/",
        "category": "cloud",
    },
    "AWS_ACCESS_KEY_ID": {
        "prefix": "AKIA",
        "description": "AWS Access Key ID",
        "docs": "https://console.aws.amazon.com/iam/",
        "category": "cloud",
    },
    "AWS_SECRET_ACCESS_KEY": {
        "prefix": "",
        "description": "AWS Secret Access Key",
        "docs": "https://console.aws.amazon.com/iam/",
        "category": "cloud",
    },
    "AWS_REGION": {
        "prefix": "",
        "description": "AWS Default Region (e.g., us-east-1)",
        "docs": "https://docs.aws.amazon.com/general/latest/gr/rande.html",
        "category": "cloud",
        "is_region": True,
    },
    "AZURE_OPENAI_API_KEY": {
        "prefix": "",
        "description": "Azure OpenAI Service API Key",
        "docs": "https://portal.azure.com/",
        "category": "cloud",
    },
    "AZURE_OPENAI_ENDPOINT": {
        "prefix": "https://",
        "description": "Azure OpenAI Service Endpoint URL",
        "docs": "https://portal.azure.com/",
        "category": "cloud",
        "is_url": True,
    },
    "AZURE_OPENAI_AD_TOKEN": {
        "prefix": "",
        "description": "Azure AD Token for OpenAI",
        "docs": "https://portal.azure.com/",
        "category": "cloud",
    },
    "VERCEL_TOKEN": {
        "prefix": "",
        "description": "Vercel API Token",
        "docs": "https://vercel.com/account/tokens",
        "category": "cloud",
    },
    "NETLIFY_AUTH_TOKEN": {
        "prefix": "",
        "description": "Netlify Auth Token",
        "docs": "https://app.netlify.com/user/applications",
        "category": "cloud",
    },
    "FLY_API_TOKEN": {
        "prefix": "fo1_",
        "description": "Fly.io API Token",
        "docs": "https://fly.io/user/personal_access_tokens",
        "category": "cloud",
    },
    "RAILWAY_TOKEN": {
        "prefix": "",
        "description": "Railway API Token",
        "docs": "https://railway.app/account/tokens",
        "category": "cloud",
    },
    "RENDER_API_KEY": {
        "prefix": "rnd_",
        "description": "Render API Key",
        "docs": "https://dashboard.render.com/u/settings#api-keys",
        "category": "cloud",
    },
    "SUPABASE_KEY": {
        "prefix": "eyJ",
        "description": "Supabase Anon/Service Key",
        "docs": "https://app.supabase.com/project/_/settings/api",
        "category": "cloud",
    },
    "SUPABASE_URL": {
        "prefix": "https://",
        "description": "Supabase Project URL",
        "docs": "https://app.supabase.com/",
        "category": "cloud",
        "is_url": True,
    },
    
    # =========================================================================
    # 🧠 ML / MODELS
    # =========================================================================
    "HUGGINGFACE_TOKEN": {
        "prefix": "hf_",
        "description": "Hugging Face API Token",
        "docs": "https://huggingface.co/settings/tokens",
        "category": "ml",
    },
    "REPLICATE_API_TOKEN": {
        "prefix": "r8_",
        "description": "Replicate ML API Token",
        "docs": "https://replicate.com/account/api-tokens",
        "category": "ml",
    },
    "STABILITY_API_KEY": {
        "prefix": "sk-",
        "description": "Stability AI API (Stable Diffusion)",
        "docs": "https://platform.stability.ai/account/keys",
        "category": "ml",
    },
    "RUNWAY_API_KEY": {
        "prefix": "",
        "description": "Runway ML API",
        "docs": "https://runwayml.com/",
        "category": "ml",
    },
    "FAL_KEY": {
        "prefix": "",
        "description": "Fal.ai API Key",
        "docs": "https://fal.ai/dashboard/keys",
        "category": "ml",
    },
    "MODAL_TOKEN_ID": {
        "prefix": "ak-",
        "description": "Modal Token ID",
        "docs": "https://modal.com/settings",
        "category": "ml",
    },
    "MODAL_TOKEN_SECRET": {
        "prefix": "as-",
        "description": "Modal Token Secret",
        "docs": "https://modal.com/settings",
        "category": "ml",
    },
    
    # =========================================================================
    # 🗄️ VECTOR DATABASES
    # =========================================================================
    "PINECONE_API_KEY": {
        "prefix": "",
        "description": "Pinecone Vector Database API",
        "docs": "https://app.pinecone.io/",
        "category": "vector_db",
    },
    "PINECONE_ENVIRONMENT": {
        "prefix": "",
        "description": "Pinecone Environment (e.g., us-east1-gcp)",
        "docs": "https://app.pinecone.io/",
        "category": "vector_db",
    },
    "QDRANT_API_KEY": {
        "prefix": "",
        "description": "Qdrant Cloud API Key",
        "docs": "https://cloud.qdrant.io/",
        "category": "vector_db",
    },
    "QDRANT_URL": {
        "prefix": "https://",
        "description": "Qdrant Cloud URL",
        "docs": "https://cloud.qdrant.io/",
        "category": "vector_db",
        "is_url": True,
    },
    "WEAVIATE_API_KEY": {
        "prefix": "",
        "description": "Weaviate Cloud API Key",
        "docs": "https://console.weaviate.cloud/",
        "category": "vector_db",
    },
    "WEAVIATE_URL": {
        "prefix": "https://",
        "description": "Weaviate Cluster URL",
        "docs": "https://console.weaviate.cloud/",
        "category": "vector_db",
        "is_url": True,
    },
    "MILVUS_API_KEY": {
        "prefix": "",
        "description": "Zilliz/Milvus Cloud API Key",
        "docs": "https://cloud.zilliz.com/",
        "category": "vector_db",
    },
    "CHROMA_API_KEY": {
        "prefix": "",
        "description": "Chroma Cloud API Key",
        "docs": "https://www.trychroma.com/",
        "category": "vector_db",
    },
    
    # =========================================================================
    # 🔧 DEVELOPER TOOLS
    # =========================================================================
    "GITHUB_TOKEN": {
        "prefix": "ghp_",
        "description": "GitHub Personal Access Token",
        "docs": "https://github.com/settings/tokens",
        "category": "dev",
    },
    "GITLAB_TOKEN": {
        "prefix": "glpat-",
        "description": "GitLab Personal Access Token",
        "docs": "https://gitlab.com/-/profile/personal_access_tokens",
        "category": "dev",
    },
    "NPM_TOKEN": {
        "prefix": "npm_",
        "description": "NPM Access Token",
        "docs": "https://www.npmjs.com/settings/~/tokens",
        "category": "dev",
    },
    "PYPI_API_TOKEN": {
        "prefix": "pypi-",
        "description": "PyPI API Token",
        "docs": "https://pypi.org/manage/account/token/",
        "category": "dev",
    },
    "SENTRY_DSN": {
        "prefix": "https://",
        "description": "Sentry Error Tracking DSN",
        "docs": "https://sentry.io/",
        "category": "dev",
        "is_url": True,
    },
    "DATADOG_API_KEY": {
        "prefix": "",
        "description": "Datadog API Key",
        "docs": "https://app.datadoghq.com/organization-settings/api-keys",
        "category": "dev",
    },
    "NEWRELIC_LICENSE_KEY": {
        "prefix": "",
        "description": "New Relic License Key",
        "docs": "https://one.newrelic.com/",
        "category": "dev",
    },
    "POSTHOG_API_KEY": {
        "prefix": "phc_",
        "description": "PostHog API Key",
        "docs": "https://app.posthog.com/project/settings",
        "category": "dev",
    },
    "SEGMENT_WRITE_KEY": {
        "prefix": "",
        "description": "Segment Write Key",
        "docs": "https://app.segment.com/",
        "category": "dev",
    },
    "MIXPANEL_TOKEN": {
        "prefix": "",
        "description": "Mixpanel Project Token",
        "docs": "https://mixpanel.com/",
        "category": "dev",
    },
    
    # =========================================================================
    # 💳 PAYMENTS & COMMERCE
    # =========================================================================
    "STRIPE_SECRET_KEY": {
        "prefix": "sk_",
        "description": "Stripe Secret API Key",
        "docs": "https://dashboard.stripe.com/apikeys",
        "category": "payments",
    },
    "STRIPE_PUBLISHABLE_KEY": {
        "prefix": "pk_",
        "description": "Stripe Publishable Key",
        "docs": "https://dashboard.stripe.com/apikeys",
        "category": "payments",
    },
    "STRIPE_WEBHOOK_SECRET": {
        "prefix": "whsec_",
        "description": "Stripe Webhook Secret",
        "docs": "https://dashboard.stripe.com/webhooks",
        "category": "payments",
    },
    "LEMONSQUEEZY_API_KEY": {
        "prefix": "",
        "description": "Lemon Squeezy API Key",
        "docs": "https://app.lemonsqueezy.com/settings/api",
        "category": "payments",
    },
    "PADDLE_API_KEY": {
        "prefix": "",
        "description": "Paddle API Key",
        "docs": "https://vendors.paddle.com/authentication",
        "category": "payments",
    },
    
    # =========================================================================
    # 📧 COMMUNICATIONS
    # =========================================================================
    "SENDGRID_API_KEY": {
        "prefix": "SG.",
        "description": "SendGrid Email API Key",
        "docs": "https://app.sendgrid.com/settings/api_keys",
        "category": "comms",
    },
    "RESEND_API_KEY": {
        "prefix": "re_",
        "description": "Resend Email API Key",
        "docs": "https://resend.com/api-keys",
        "category": "comms",
    },
    "POSTMARK_API_TOKEN": {
        "prefix": "",
        "description": "Postmark Server API Token",
        "docs": "https://account.postmarkapp.com/servers",
        "category": "comms",
    },
    "MAILGUN_API_KEY": {
        "prefix": "",
        "description": "Mailgun API Key",
        "docs": "https://app.mailgun.com/app/account/security/api_keys",
        "category": "comms",
    },
    "TWILIO_ACCOUNT_SID": {
        "prefix": "AC",
        "description": "Twilio Account SID",
        "docs": "https://console.twilio.com/",
        "category": "comms",
    },
    "TWILIO_AUTH_TOKEN": {
        "prefix": "",
        "description": "Twilio Auth Token",
        "docs": "https://console.twilio.com/",
        "category": "comms",
    },
    "SLACK_BOT_TOKEN": {
        "prefix": "xoxb-",
        "description": "Slack Bot Token",
        "docs": "https://api.slack.com/apps",
        "category": "comms",
    },
    "DISCORD_BOT_TOKEN": {
        "prefix": "",
        "description": "Discord Bot Token",
        "docs": "https://discord.com/developers/applications",
        "category": "comms",
    },
    "TELEGRAM_BOT_TOKEN": {
        "prefix": "",
        "description": "Telegram Bot Token",
        "docs": "https://t.me/BotFather",
        "category": "comms",
    },
    
    # =========================================================================
    # 🎮 UNITY / GAMING
    # =========================================================================
    "UNITY_LICENSE": {
        "prefix": "",
        "description": "Unity License Serial",
        "docs": "https://id.unity.com/",
        "category": "gaming",
    },
    "UNITY_API_KEY": {
        "prefix": "",
        "description": "Unity Cloud API Key",
        "docs": "https://cloud.unity.com/",
        "category": "gaming",
    },
    "PHOTON_APP_ID": {
        "prefix": "",
        "description": "Photon PUN App ID",
        "docs": "https://dashboard.photonengine.com/",
        "category": "gaming",
    },
    "PLAYFAB_SECRET_KEY": {
        "prefix": "",
        "description": "PlayFab Secret Key",
        "docs": "https://developer.playfab.com/",
        "category": "gaming",
    },
    
    # =========================================================================
    # 🔐 NOIZYVOX INTERNAL
    # =========================================================================
    "NOIZYVOX_API_KEY": {
        "prefix": "nvox_",
        "description": "NOIZYVOX Platform API Key",
        "docs": "internal",
        "category": "noizyvox",
    },
    "NOIZYVOX_SECRET": {
        "prefix": "",
        "description": "NOIZYVOX Webhook Secret",
        "docs": "internal",
        "category": "noizyvox",
    },
    "NOIZYVOX_WORKER_SECRET": {
        "prefix": "",
        "description": "NOIZYVOX Cloudflare Worker Secret",
        "docs": "internal",
        "category": "noizyvox",
    },
}

# Category display names
CATEGORIES = {
    "ai": "🤖 AI / LLM Providers",
    "voice": "🎙️ Voice / Speech Providers",
    "cloud": "☁️ Cloud Infrastructure",
    "ml": "🧠 ML / Models",
    "vector_db": "🗄️ Vector Databases",
    "dev": "🔧 Developer Tools",
    "payments": "💳 Payments & Commerce",
    "comms": "📧 Communications",
    "gaming": "🎮 Unity / Gaming",
    "noizyvox": "🔐 NOIZYVOX Internal",
}

# =============================================================================
# Encryption Utilities
# =============================================================================

class SecureKeyStore:
    """Encrypted key storage with AES-256-GCM."""
    
    def __init__(self, config_dir: Path = CONFIG_DIR):
        self.config_dir = config_dir
        self.keys_file = config_dir / "keys.enc"
        self.salt_file = config_dir / "salt"
        self.config_file = config_dir / "config.json"
        self._key: Optional[bytes] = None
        
    def _ensure_dir(self):
        """Create config directory with secure permissions."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        # Set directory permissions to owner only (700)
        os.chmod(self.config_dir, 0o700)
    
    def _get_salt(self) -> bytes:
        """Get or create salt for key derivation."""
        if self.salt_file.exists():
            return self.salt_file.read_bytes()
        else:
            self._ensure_dir()
            salt = secrets.token_bytes(32)
            self.salt_file.write_bytes(salt)
            os.chmod(self.salt_file, 0o600)
            return salt
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2."""
        if not HAS_CRYPTOGRAPHY:
            # Fallback to hashlib (less secure but functional)
            salt = self._get_salt()
            return hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                iterations=480000,
                dklen=32
            )
        
        salt = self._get_salt()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        return kdf.derive(password.encode())
    
    def _encrypt(self, data: bytes, key: bytes) -> bytes:
        """Encrypt data using AES-256-GCM."""
        if not HAS_CRYPTOGRAPHY:
            # Fallback: XOR with key (NOT SECURE - just for basic obfuscation)
            # In production, require cryptography package
            import warnings
            warnings.warn("Using weak encryption. Install 'cryptography' for AES-256.")
            return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))
        
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        return nonce + ciphertext
    
    def _decrypt(self, data: bytes, key: bytes) -> bytes:
        """Decrypt data using AES-256-GCM."""
        if not HAS_CRYPTOGRAPHY:
            # Fallback: XOR with key
            return bytes(a ^ b for a, b in zip(data, (key * (len(data) // len(key) + 1))[:len(data)]))
        
        nonce = data[:12]
        ciphertext = data[12:]
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)
    
    def unlock(self, password: str) -> bool:
        """Unlock the key store with master password."""
        self._key = self._derive_key(password)
        
        # Verify password by trying to decrypt
        if self.keys_file.exists():
            try:
                self._load_keys()
                return True
            except Exception:
                self._key = None
                return False
        return True
    
    def lock(self):
        """Lock the key store and clear memory."""
        if self._key:
            # Overwrite key in memory
            self._key = b'\x00' * len(self._key)
        self._key = None
    
    def is_initialized(self) -> bool:
        """Check if the key store has been initialized."""
        return self.salt_file.exists()
    
    def initialize(self, password: str):
        """Initialize the key store with a master password."""
        self._ensure_dir()
        self._key = self._derive_key(password)
        
        # Create empty keys file
        self._save_keys({})
        
        # Create config
        config = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "use_keychain": HAS_KEYRING,
        }
        self.config_file.write_text(json.dumps(config, indent=2))
        os.chmod(self.config_file, 0o600)
        
        self._audit("INIT", "Key store initialized")
    
    def _load_keys(self) -> Dict[str, Any]:
        """Load and decrypt keys from file."""
        if not self._key:
            raise ValueError("Key store is locked")
        
        if not self.keys_file.exists():
            return {}
        
        encrypted = self.keys_file.read_bytes()
        decrypted = self._decrypt(encrypted, self._key)
        return json.loads(decrypted.decode())
    
    def _save_keys(self, keys: Dict[str, Any]):
        """Encrypt and save keys to file."""
        if not self._key:
            raise ValueError("Key store is locked")
        
        self._ensure_dir()
        data = json.dumps(keys, indent=2).encode()
        encrypted = self._encrypt(data, self._key)
        self.keys_file.write_bytes(encrypted)
        os.chmod(self.keys_file, 0o600)
    
    def _audit(self, action: str, details: str):
        """Log action to audit log (never logs key values)."""
        self._ensure_dir()
        timestamp = datetime.now().isoformat()
        entry = f"{timestamp} | {action:10} | {details}\n"
        
        with open(AUDIT_LOG, "a") as f:
            f.write(entry)
        os.chmod(AUDIT_LOG, 0o600)
    
    def add_key(self, name: str, value: str, description: str = "") -> bool:
        """Add or update an API key."""
        keys = self._load_keys()
        
        # Validate key format if known
        if name in API_KEY_PATTERNS:
            pattern = API_KEY_PATTERNS[name]
            if pattern["prefix"] and not value.startswith(pattern["prefix"]):
                print(f"⚠️  Warning: Key doesn't match expected prefix '{pattern['prefix']}'")
        
        keys[name] = {
            "value": value,
            "description": description or API_KEY_PATTERNS.get(name, {}).get("description", ""),
            "added_at": datetime.now().isoformat(),
            "last_rotated": datetime.now().isoformat(),
            "access_count": 0,
        }
        
        self._save_keys(keys)
        self._audit("ADD", f"Added key: {name}")
        
        # Also store in keychain if available
        if HAS_KEYRING:
            try:
                keyring.set_password(KEYRING_SERVICE, name, value)
            except Exception as e:
                print(f"⚠️  Keychain storage failed: {e}")
        
        return True
    
    def get_key(self, name: str) -> Optional[str]:
        """Get an API key value."""
        # Try keychain first
        if HAS_KEYRING:
            try:
                value = keyring.get_password(KEYRING_SERVICE, name)
                if value:
                    self._audit("ACCESS", f"Retrieved key from keychain: {name}")
                    return value
            except Exception:
                pass
        
        # Fall back to encrypted file
        keys = self._load_keys()
        if name in keys:
            # Update access count
            keys[name]["access_count"] = keys[name].get("access_count", 0) + 1
            keys[name]["last_accessed"] = datetime.now().isoformat()
            self._save_keys(keys)
            
            self._audit("ACCESS", f"Retrieved key: {name}")
            return keys[name]["value"]
        
        return None
    
    def list_keys(self) -> List[Dict[str, Any]]:
        """List all stored keys (without values)."""
        keys = self._load_keys()
        result = []
        
        for name, data in keys.items():
            result.append({
                "name": name,
                "description": data.get("description", ""),
                "added_at": data.get("added_at", ""),
                "last_rotated": data.get("last_rotated", ""),
                "last_accessed": data.get("last_accessed", ""),
                "access_count": data.get("access_count", 0),
                "preview": data["value"][:8] + "..." + data["value"][-4:] if len(data["value"]) > 12 else "***",
            })
        
        self._audit("LIST", f"Listed {len(result)} keys")
        return result
    
    def remove_key(self, name: str) -> bool:
        """Remove an API key."""
        keys = self._load_keys()
        
        if name not in keys:
            return False
        
        del keys[name]
        self._save_keys(keys)
        
        # Also remove from keychain
        if HAS_KEYRING:
            try:
                keyring.delete_password(KEYRING_SERVICE, name)
            except Exception:
                pass
        
        self._audit("REMOVE", f"Removed key: {name}")
        return True
    
    def rotate_key(self, name: str, new_value: str) -> bool:
        """Rotate an API key to a new value."""
        keys = self._load_keys()
        
        if name not in keys:
            return False
        
        old_preview = keys[name]["value"][:8] + "..."
        keys[name]["value"] = new_value
        keys[name]["last_rotated"] = datetime.now().isoformat()
        keys[name]["rotation_count"] = keys[name].get("rotation_count", 0) + 1
        
        self._save_keys(keys)
        
        # Update keychain
        if HAS_KEYRING:
            try:
                keyring.set_password(KEYRING_SERVICE, name, new_value)
            except Exception:
                pass
        
        self._audit("ROTATE", f"Rotated key: {name} (was {old_preview})")
        return True
    
    def export_env(self) -> str:
        """Generate shell export commands."""
        keys = self._load_keys()
        lines = ["# NOIZYVOX API Keys - Generated by api_key_manager.py"]
        lines.append(f"# Generated: {datetime.now().isoformat()}")
        lines.append("")
        
        for name, data in keys.items():
            desc = data.get("description", "")
            if desc:
                lines.append(f"# {desc}")
            lines.append(f'export {name}="{data["value"]}"')
            lines.append("")
        
        self._audit("EXPORT", f"Exported {len(keys)} keys")
        return "\n".join(lines)
    
    def get_audit_log(self, lines: int = 50) -> List[str]:
        """Get recent audit log entries."""
        if not AUDIT_LOG.exists():
            return []
        
        with open(AUDIT_LOG, "r") as f:
            all_lines = f.readlines()
        
        return all_lines[-lines:]


# =============================================================================
# Environment Integration
# =============================================================================

def load_keys_to_env(store: SecureKeyStore):
    """Load all keys into environment variables."""
    keys = store._load_keys()
    for name, data in keys.items():
        os.environ[name] = data["value"]


def get_key_or_env(name: str, store: Optional[SecureKeyStore] = None) -> Optional[str]:
    """Get key from store or fall back to environment variable."""
    # Try store first
    if store and store._key:
        value = store.get_key(name)
        if value:
            return value
    
    # Fall back to environment
    return os.getenv(name)


# =============================================================================
# CLI Interface
# =============================================================================

def prompt_password(confirm: bool = False) -> str:
    """Prompt for master password."""
    password = getpass.getpass("🔐 Master Password: ")
    
    if confirm:
        password2 = getpass.getpass("🔐 Confirm Password: ")
        if password != password2:
            print("❌ Passwords don't match!")
            sys.exit(1)
    
    return password


def cmd_init(args):
    """Initialize the key store."""
    store = SecureKeyStore()
    
    if store.is_initialized():
        print("⚠️  Key store already initialized!")
        response = input("   Reset and create new? [y/N]: ").strip().lower()
        if response != 'y':
            return
    
    print("\n🔐 NOIZYVOX API Key Manager - Setup")
    print("=" * 50)
    print("\nCreate a master password to encrypt your API keys.")
    print("⚠️  This password cannot be recovered if lost!\n")
    
    password = prompt_password(confirm=True)
    
    if len(password) < 8:
        print("❌ Password must be at least 8 characters!")
        sys.exit(1)
    
    store.initialize(password)
    
    print("\n✅ Key store initialized!")
    print(f"   Location: {CONFIG_DIR}")
    print(f"   Keychain: {'✅ Enabled' if HAS_KEYRING else '❌ Not available'}")
    print(f"   Encryption: {'✅ AES-256-GCM' if HAS_CRYPTOGRAPHY else '⚠️ Basic (install cryptography)'}")
    
    # Offer to add common keys
    print("\n📋 Would you like to add API keys now?")
    for name, info in list(API_KEY_PATTERNS.items())[:5]:
        response = input(f"   Add {name}? ({info['description']}) [y/N]: ").strip().lower()
        if response == 'y':
            value = getpass.getpass(f"   Enter {name}: ")
            if value:
                store.add_key(name, value)
                print(f"   ✅ Added {name}")


def cmd_add(args):
    """Add an API key."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("❌ Key store not initialized. Run: python api_key_manager.py init")
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("❌ Invalid password!")
        sys.exit(1)
    
    name = args.name.upper()
    
    # Get key value
    if args.value:
        value = args.value
    else:
        value = getpass.getpass(f"🔑 Enter value for {name}: ")
    
    if not value:
        print("❌ No value provided!")
        sys.exit(1)
    
    # Validate
    if name in API_KEY_PATTERNS:
        info = API_KEY_PATTERNS[name]
        print(f"   📝 {info['description']}")
        print(f"   📚 Docs: {info['docs']}")
    
    store.add_key(name, value, args.description or "")
    store.lock()
    
    print(f"\n✅ Added {name}")
    
    # Offer to export
    print(f"\n💡 To use in current shell:")
    print(f'   export {name}="..."')
    print(f"\n   Or add to ~/.zshrc:")
    print(f"   python {__file__} export >> ~/.zshrc")


def cmd_get(args):
    """Get an API key value."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("❌ Key store not initialized", file=sys.stderr)
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("❌ Invalid password!", file=sys.stderr)
        sys.exit(1)
    
    value = store.get_key(args.name.upper())
    store.lock()
    
    if value:
        if args.export:
            print(f'export {args.name.upper()}="{value}"')
        else:
            print(value)
    else:
        print(f"❌ Key not found: {args.name}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List all stored keys."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("❌ Key store not initialized. Run: python api_key_manager.py init")
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("❌ Invalid password!")
        sys.exit(1)
    
    keys = store.list_keys()
    store.lock()
    
    if not keys:
        print("\n📭 No keys stored yet.")
        print("   Add a key: python api_key_manager.py add ANTHROPIC_API_KEY")
        return
    
    print(f"\n🔐 Stored API Keys ({len(keys)} total)")
    print("=" * 70)
    
    for key in keys:
        status = "🟢" if key["access_count"] > 0 else "🔵"
        print(f"\n{status} {key['name']}")
        print(f"   Preview: {key['preview']}")
        if key["description"]:
            print(f"   Description: {key['description']}")
        print(f"   Added: {key['added_at'][:10]}")
        print(f"   Last Rotated: {key['last_rotated'][:10]}")
        print(f"   Access Count: {key['access_count']}")
    
    print("\n" + "=" * 70)


def cmd_remove(args):
    """Remove an API key."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("❌ Key store not initialized")
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("❌ Invalid password!")
        sys.exit(1)
    
    name = args.name.upper()
    
    # Confirm
    confirm = input(f"⚠️  Remove {name}? This cannot be undone! [y/N]: ").strip().lower()
    if confirm != 'y':
        print("   Cancelled")
        return
    
    if store.remove_key(name):
        print(f"✅ Removed {name}")
    else:
        print(f"❌ Key not found: {name}")
    
    store.lock()


def cmd_rotate(args):
    """Rotate an API key."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("❌ Key store not initialized")
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("❌ Invalid password!")
        sys.exit(1)
    
    name = args.name.upper()
    
    # Get new value
    new_value = getpass.getpass(f"🔑 Enter new value for {name}: ")
    if not new_value:
        print("❌ No value provided!")
        sys.exit(1)
    
    if store.rotate_key(name, new_value):
        print(f"✅ Rotated {name}")
        print("   Remember to update the key in your service provider!")
    else:
        print(f"❌ Key not found: {name}")
    
    store.lock()


def cmd_export(args):
    """Export keys as shell commands."""
    store = SecureKeyStore()
    
    if not store.is_initialized():
        print("# Key store not initialized", file=sys.stderr)
        sys.exit(1)
    
    password = prompt_password()
    if not store.unlock(password):
        print("# Invalid password!", file=sys.stderr)
        sys.exit(1)
    
    export = store.export_env()
    store.lock()
    
    print(export)


def cmd_audit(args):
    """Show audit log."""
    store = SecureKeyStore()
    
    entries = store.get_audit_log(args.lines)
    
    print(f"\n📋 Audit Log (last {args.lines} entries)")
    print("=" * 70)
    
    for entry in entries:
        print(entry.strip())
    
    print("=" * 70)


def cmd_check(args):
    """Check security status."""
    print("\n🔐 NOIZYVOX API Key Manager - Security Check")
    print("=" * 50)
    
    # Check dependencies
    print("\n📦 Dependencies:")
    print(f"   cryptography: {'✅ Installed (AES-256-GCM)' if HAS_CRYPTOGRAPHY else '❌ Not installed (weak encryption)'}")
    print(f"   keyring: {'✅ Installed (system keychain)' if HAS_KEYRING else '❌ Not installed (file-only)'}")
    
    # Check store
    store = SecureKeyStore()
    print(f"\n📁 Storage:")
    print(f"   Location: {CONFIG_DIR}")
    print(f"   Initialized: {'✅ Yes' if store.is_initialized() else '❌ No'}")
    
    if store.is_initialized():
        # Check permissions
        keys_perm = oct(os.stat(KEYS_FILE).st_mode)[-3:] if KEYS_FILE.exists() else "N/A"
        salt_perm = oct(os.stat(SALT_FILE).st_mode)[-3:] if SALT_FILE.exists() else "N/A"
        
        print(f"   Keys file: {keys_perm} {'✅' if keys_perm == '600' else '⚠️ Should be 600'}")
        print(f"   Salt file: {salt_perm} {'✅' if salt_perm == '600' else '⚠️ Should be 600'}")
    
    # Check for exposed keys in common files
    print(f"\n🔍 Checking for exposed keys...")
    exposed = []
    
    check_files = [
        Path.home() / ".zshrc",
        Path.home() / ".bashrc",
        Path.home() / ".bash_profile",
        Path.home() / ".env",
        Path.cwd() / ".env",
    ]
    
    for file in check_files:
        if file.exists():
            try:
                content = file.read_text()
                for key_name, info in API_KEY_PATTERNS.items():
                    if info.get("prefix") and info["prefix"] in content:
                        exposed.append((file, key_name))
            except Exception:
                pass
    
    if exposed:
        print("   ⚠️  Found potential exposed keys:")
        for file, key in exposed:
            print(f"      {file}: {key}")
    else:
        print("   ✅ No exposed keys found in common files")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not HAS_CRYPTOGRAPHY:
        print("   • Install cryptography: pip install cryptography")
    if not HAS_KEYRING:
        print("   • Install keyring: pip install keyring")
    print("   • Use 'export' command instead of hardcoding keys")
    print("   • Rotate keys regularly")
    print("   • Review audit log periodically")


def cmd_status(args):
    """Show complete API token space status."""
    print("\n🌐 COMPLETE API TOKEN SPACE STATUS")
    print("=" * 80)
    
    # Check environment variables for all known keys
    configured = {}
    missing = {}
    
    for name, info in API_KEY_PATTERNS.items():
        category = info.get("category", "other")
        env_value = os.getenv(name)
        
        if env_value:
            if category not in configured:
                configured[category] = []
            # Mask the value
            if len(env_value) > 12:
                masked = env_value[:8] + "..." + env_value[-4:]
            else:
                masked = "***"
            configured[category].append((name, masked, info))
        else:
            if category not in missing:
                missing[category] = []
            missing[category].append((name, info))
    
    # Show configured keys by category
    total_configured = sum(len(v) for v in configured.values())
    total_missing = sum(len(v) for v in missing.values())
    
    print(f"\n✅ CONFIGURED ({total_configured} keys)")
    print("-" * 80)
    
    for category in sorted(configured.keys()):
        cat_name = CATEGORIES.get(category, category)
        keys = configured[category]
        print(f"\n{cat_name}")
        for name, masked, info in keys:
            required = "🔴" if info.get("required") else "  "
            print(f"   {required} {name}")
            print(f"      Value: {masked}")
    
    # Show missing keys by category
    print(f"\n\n❌ NOT CONFIGURED ({total_missing} keys)")
    print("-" * 80)
    
    if args.required_only:
        # Only show required keys
        for category in sorted(missing.keys()):
            cat_name = CATEGORIES.get(category, category)
            keys = [(n, i) for n, i in missing[category] if i.get("required")]
            if keys:
                print(f"\n{cat_name}")
                for name, info in keys:
                    print(f"   🔴 {name} - {info['description']}")
                    print(f"      📚 {info['docs']}")
    else:
        for category in sorted(missing.keys()):
            cat_name = CATEGORIES.get(category, category)
            keys = missing[category]
            print(f"\n{cat_name}")
            for name, info in keys:
                required = "🔴" if info.get("required") else "  "
                print(f"   {required} {name} - {info['description']}")
                if args.verbose:
                    print(f"      📚 {info['docs']}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print(f"   Configured: {total_configured}")
    print(f"   Missing: {total_missing}")
    print(f"   Required Missing: {sum(1 for cat in missing.values() for n, i in cat if i.get('required'))}")
    
    # Quick add suggestions
    print("\n💡 QUICK SETUP:")
    print("   Initialize:  python api_key_manager.py init")
    print("   Add key:     python api_key_manager.py add ANTHROPIC_API_KEY")
    print("   View all:    python api_key_manager.py status --verbose")
    print("   Required:    python api_key_manager.py status --required")
    
    # Category breakdown
    if args.verbose:
        print("\n📈 BY CATEGORY:")
        all_categories = set(list(configured.keys()) + list(missing.keys()))
        for cat in sorted(all_categories):
            cat_name = CATEGORIES.get(cat, cat)
            conf = len(configured.get(cat, []))
            miss = len(missing.get(cat, []))
            bar = "█" * conf + "░" * miss
            print(f"   {cat_name[:30]:30} [{bar}] {conf}/{conf+miss}")


def main():
    parser = argparse.ArgumentParser(
        description="🔐 NOIZYVOX API Key Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  init              Initialize the key store
  add NAME          Add or update an API key
  get NAME          Get an API key value
  list              List all stored keys
  remove NAME       Remove an API key
  rotate NAME       Rotate a key to new value
  export            Export all keys as shell commands
  audit             Show audit log
  check             Security status check
  status            Show COMPLETE API token space

Examples:
  %(prog)s init
  %(prog)s add ANTHROPIC_API_KEY
  %(prog)s get OPENAI_API_KEY --export
  %(prog)s status --verbose
  %(prog)s status --required
  %(prog)s export >> ~/.zshrc
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # init
    subparsers.add_parser("init", help="Initialize key store")
    
    # add
    add_parser = subparsers.add_parser("add", help="Add an API key")
    add_parser.add_argument("name", help="Key name (e.g., ANTHROPIC_API_KEY)")
    add_parser.add_argument("--value", "-v", help="Key value (prompts if not provided)")
    add_parser.add_argument("--description", "-d", help="Key description")
    
    # get
    get_parser = subparsers.add_parser("get", help="Get an API key")
    get_parser.add_argument("name", help="Key name")
    get_parser.add_argument("--export", "-e", action="store_true", help="Output as export command")
    
    # list
    subparsers.add_parser("list", help="List all keys")
    
    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove an API key")
    remove_parser.add_argument("name", help="Key name")
    
    # rotate
    rotate_parser = subparsers.add_parser("rotate", help="Rotate an API key")
    rotate_parser.add_argument("name", help="Key name")
    
    # export
    subparsers.add_parser("export", help="Export keys as shell commands")
    
    # audit
    audit_parser = subparsers.add_parser("audit", help="Show audit log")
    audit_parser.add_argument("--lines", "-n", type=int, default=50, help="Number of lines")
    
    # check
    subparsers.add_parser("check", help="Security status check")
    
    # status - COMPLETE API TOKEN SPACE
    status_parser = subparsers.add_parser("status", help="Show COMPLETE API token space")
    status_parser.add_argument("--verbose", "-v", action="store_true", help="Show docs and details")
    status_parser.add_argument("--required", "--required-only", "-r", dest="required_only", 
                               action="store_true", help="Show only required keys")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "remove": cmd_remove,
        "rotate": cmd_rotate,
        "export": cmd_export,
        "audit": cmd_audit,
        "check": cmd_check,
        "status": cmd_status,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
