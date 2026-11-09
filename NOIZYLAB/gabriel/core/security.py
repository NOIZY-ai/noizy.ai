#!/usr/bin/env python3
"""
🔐 GABRIEL SECURITY SYSTEM
==========================
Secure key management, secret redaction, and least-privilege access.

Features:
- macOS Keychain integration
- Encrypted .env fallback
- Automatic secret redaction from logs
- Role-based key separation (Router, Executor, Verifier)
"""

import os
import re
import subprocess
import json
import hashlib
from pathlib import Path
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import base64

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
SECRETS_DIR = GABRIEL_ROOT / "secrets"
SECRETS_DIR.mkdir(exist_ok=True)

# Service identifier for Keychain
KEYCHAIN_SERVICE = "com.noizylab.gabriel"

# Patterns to redact from logs
REDACTION_PATTERNS = [
    r'sk-[a-zA-Z0-9]{32,}',           # OpenAI keys
    r'sk-ant-[a-zA-Z0-9\-]{32,}',     # Anthropic keys
    r'AIza[a-zA-Z0-9_-]{35}',         # Google API keys
    r'gsk_[a-zA-Z0-9]{32,}',          # Groq keys
    r'xai-[a-zA-Z0-9]{32,}',          # xAI keys
    r'[a-f0-9]{32,64}',               # Generic hex tokens (careful)
    r'ghp_[a-zA-Z0-9]{36}',           # GitHub tokens
    r'Bearer\s+[a-zA-Z0-9\-._~+/]+=*', # Bearer tokens
    r'password["\']?\s*[:=]\s*["\'][^"\']+["\']',  # Passwords
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails (PII)
]

# =============================================================================
# ENUMS & TYPES
# =============================================================================

class Role(Enum):
    """Access roles for key separation."""
    ROUTER = "router"         # Only needs to decide routing
    EXECUTOR = "executor"     # Runs actual LLM calls
    VERIFIER = "verifier"     # Fact-checking
    SEARCH = "search"         # Web search grounding
    VOICE = "voice"           # TTS/STT services
    ADMIN = "admin"           # Full access (use sparingly)

class Provider(Enum):
    """Supported AI providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROQ = "groq"
    XAI = "xai"
    ELEVEN_LABS = "elevenlabs"
    LOCAL = "local"  # No key needed

@dataclass
class KeyConfig:
    """Configuration for a specific key."""
    provider: Provider
    role: Role
    env_var: str
    key_name: str  # Keychain account name
    rate_limit: int = 100  # requests per minute
    budget_cents: int = 1000  # max spend in cents

# =============================================================================
# KEY REGISTRY
# =============================================================================

KEY_REGISTRY: Dict[str, KeyConfig] = {
    # Router keys (low cost, high volume)
    "router_groq": KeyConfig(Provider.GROQ, Role.ROUTER, "GROQ_API_KEY_ROUTER", "gabriel-router-groq", rate_limit=200, budget_cents=100),
    
    # Executor keys (main workload)
    "executor_anthropic": KeyConfig(Provider.ANTHROPIC, Role.EXECUTOR, "ANTHROPIC_API_KEY", "gabriel-executor-anthropic", rate_limit=50, budget_cents=5000),
    "executor_openai": KeyConfig(Provider.OPENAI, Role.EXECUTOR, "OPENAI_API_KEY", "gabriel-executor-openai", rate_limit=50, budget_cents=5000),
    "executor_google": KeyConfig(Provider.GOOGLE, Role.EXECUTOR, "GOOGLE_API_KEY", "gabriel-executor-google", rate_limit=100, budget_cents=2000),
    "executor_groq": KeyConfig(Provider.GROQ, Role.EXECUTOR, "GROQ_API_KEY", "gabriel-executor-groq", rate_limit=100, budget_cents=500),
    "executor_xai": KeyConfig(Provider.XAI, Role.EXECUTOR, "XAI_API_KEY", "gabriel-executor-xai", rate_limit=50, budget_cents=3000),
    
    # Verifier keys (fact-checking, search)
    "verifier_google": KeyConfig(Provider.GOOGLE, Role.VERIFIER, "GOOGLE_API_KEY_VERIFIER", "gabriel-verifier-google", rate_limit=100, budget_cents=1000),
    
    # Voice keys
    "voice_elevenlabs": KeyConfig(Provider.ELEVEN_LABS, Role.VOICE, "ELEVENLABS_API_KEY", "gabriel-voice-elevenlabs", rate_limit=20, budget_cents=2000),
}

# =============================================================================
# KEYCHAIN OPERATIONS (macOS)
# =============================================================================

class KeychainManager:
    """Manage secrets in macOS Keychain."""
    
    @staticmethod
    def store_key(account: str, password: str, service: str = KEYCHAIN_SERVICE) -> bool:
        """Store a key in Keychain."""
        try:
            # Delete existing if present
            subprocess.run(
                ["security", "delete-generic-password", "-s", service, "-a", account],
                capture_output=True
            )
            # Add new
            result = subprocess.run(
                ["security", "add-generic-password", "-s", service, "-a", account, "-w", password],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Keychain store failed: {e}")
            return False
    
    @staticmethod
    def get_key(account: str, service: str = KEYCHAIN_SERVICE) -> Optional[str]:
        """Retrieve a key from Keychain."""
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None
    
    @staticmethod
    def delete_key(account: str, service: str = KEYCHAIN_SERVICE) -> bool:
        """Delete a key from Keychain."""
        try:
            result = subprocess.run(
                ["security", "delete-generic-password", "-s", service, "-a", account],
                capture_output=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    @staticmethod
    def list_keys(service: str = KEYCHAIN_SERVICE) -> List[str]:
        """List all GABRIEL keys in Keychain."""
        try:
            result = subprocess.run(
                ["security", "dump-keychain"],
                capture_output=True, text=True
            )
            # Parse for our service
            keys = []
            for line in result.stdout.split('\n'):
                if f'svce"<blob>="{service}"' in line or f'"acct"<blob>="gabriel-' in line:
                    # Extract account name
                    match = re.search(r'"acct"<blob>="([^"]+)"', line)
                    if match:
                        keys.append(match.group(1))
            return list(set(keys))
        except Exception:
            return []

# =============================================================================
# SECRET REDACTION
# =============================================================================

class SecretRedactor:
    """Redact secrets from logs and outputs."""
    
    def __init__(self, patterns: List[str] = None):
        self.patterns = patterns or REDACTION_PATTERNS
        self._compiled = [re.compile(p, re.IGNORECASE) for p in self.patterns]
        self._known_secrets: set = set()
    
    def add_known_secret(self, secret: str):
        """Add a specific secret to always redact."""
        if secret and len(secret) > 4:
            self._known_secrets.add(secret)
    
    def redact(self, text: str) -> str:
        """Redact all secrets from text."""
        if not text:
            return text
        
        result = text
        
        # Redact known secrets first
        for secret in self._known_secrets:
            if secret in result:
                # Show first/last 2 chars
                masked = f"{secret[:2]}{'*' * (len(secret)-4)}{secret[-2:]}"
                result = result.replace(secret, f"[REDACTED:{masked}]")
        
        # Apply pattern-based redaction
        for pattern in self._compiled:
            result = pattern.sub("[REDACTED]", result)
        
        return result
    
    def redact_dict(self, data: dict) -> dict:
        """Recursively redact secrets from a dictionary."""
        if not isinstance(data, dict):
            return data
        
        result = {}
        sensitive_keys = {'password', 'secret', 'key', 'token', 'api_key', 'apikey', 'auth', 'credential'}
        
        for k, v in data.items():
            k_lower = k.lower()
            if any(s in k_lower for s in sensitive_keys):
                result[k] = "[REDACTED]"
            elif isinstance(v, dict):
                result[k] = self.redact_dict(v)
            elif isinstance(v, list):
                result[k] = [self.redact_dict(i) if isinstance(i, dict) else self.redact(str(i)) if isinstance(i, str) else i for i in v]
            elif isinstance(v, str):
                result[k] = self.redact(v)
            else:
                result[k] = v
        
        return result
    
    def redact_file(self, filepath: Path) -> bool:
        """Redact secrets from a file in place."""
        try:
            content = filepath.read_text()
            redacted = self.redact(content)
            if content != redacted:
                filepath.write_text(redacted)
                return True
            return False
        except Exception:
            return False

# =============================================================================
# SECURE KEY LOADER
# =============================================================================

class SecureKeyLoader:
    """Load keys with role-based access control."""
    
    def __init__(self):
        self.keychain = KeychainManager()
        self.redactor = SecretRedactor()
        self._loaded_keys: Dict[str, str] = {}
        self._access_log: List[Dict] = []
    
    def get_key(self, key_id: str, role: Role = None) -> Optional[str]:
        """
        Get a key by ID with optional role verification.
        
        Args:
            key_id: Key identifier from KEY_REGISTRY
            role: Required role (enforces least-privilege)
        """
        if key_id not in KEY_REGISTRY:
            self._log_access(key_id, role, success=False, reason="unknown_key")
            return None
        
        config = KEY_REGISTRY[key_id]
        
        # Role check
        if role and config.role != role and config.role != Role.ADMIN:
            self._log_access(key_id, role, success=False, reason="role_mismatch")
            return None
        
        # Check cache
        if key_id in self._loaded_keys:
            self._log_access(key_id, role, success=True, source="cache")
            return self._loaded_keys[key_id]
        
        # Try Keychain first
        key = self.keychain.get_key(config.key_name)
        if key:
            self._loaded_keys[key_id] = key
            self.redactor.add_known_secret(key)
            self._log_access(key_id, role, success=True, source="keychain")
            return key
        
        # Fallback to environment
        key = os.environ.get(config.env_var)
        if key:
            self._loaded_keys[key_id] = key
            self.redactor.add_known_secret(key)
            self._log_access(key_id, role, success=True, source="env")
            return key
        
        self._log_access(key_id, role, success=False, reason="not_found")
        return None
    
    def get_provider_key(self, provider: Provider, role: Role) -> Optional[str]:
        """Get the best key for a provider and role."""
        for key_id, config in KEY_REGISTRY.items():
            if config.provider == provider and config.role == role:
                return self.get_key(key_id, role)
        
        # Fallback: any key for this provider
        for key_id, config in KEY_REGISTRY.items():
            if config.provider == provider:
                return self.get_key(key_id)
        
        return None
    
    def _log_access(self, key_id: str, role: Role, success: bool, source: str = None, reason: str = None):
        """Log key access for audit."""
        self._access_log.append({
            "timestamp": datetime.now().isoformat(),
            "key_id": key_id,
            "role": role.value if role else None,
            "success": success,
            "source": source,
            "reason": reason
        })
    
    def get_access_log(self) -> List[Dict]:
        """Get audit log of key accesses."""
        return self._access_log.copy()
    
    def store_key_interactive(self, key_id: str, key_value: str) -> bool:
        """Store a key in Keychain (for setup)."""
        if key_id not in KEY_REGISTRY:
            print(f"Unknown key_id: {key_id}")
            print(f"Available: {list(KEY_REGISTRY.keys())}")
            return False
        
        config = KEY_REGISTRY[key_id]
        success = self.keychain.store_key(config.key_name, key_value)
        if success:
            print(f"✅ Stored {key_id} in Keychain")
        else:
            print(f"❌ Failed to store {key_id}")
        return success

# =============================================================================
# ENCRYPTION UTILITIES
# =============================================================================

class SimpleEncryption:
    """Simple encryption for .env fallback (not for high-security)."""
    
    @staticmethod
    def derive_key(password: str, salt: bytes = b'gabriel_salt_v1') -> bytes:
        """Derive encryption key from password."""
        import hashlib
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)[:32]
    
    @staticmethod
    def encrypt(plaintext: str, password: str) -> str:
        """Encrypt plaintext with password."""
        try:
            from cryptography.fernet import Fernet
            import base64
            key = base64.urlsafe_b64encode(SimpleEncryption.derive_key(password))
            f = Fernet(key)
            return f.encrypt(plaintext.encode()).decode()
        except ImportError:
            # Fallback: base64 obfuscation (NOT secure, just basic)
            return base64.b64encode(plaintext.encode()).decode()
    
    @staticmethod
    def decrypt(ciphertext: str, password: str) -> str:
        """Decrypt ciphertext with password."""
        try:
            from cryptography.fernet import Fernet
            import base64
            key = base64.urlsafe_b64encode(SimpleEncryption.derive_key(password))
            f = Fernet(key)
            return f.decrypt(ciphertext.encode()).decode()
        except ImportError:
            return base64.b64decode(ciphertext.encode()).decode()

# =============================================================================
# CLI FOR KEY MANAGEMENT
# =============================================================================

def setup_keys_interactive():
    """Interactive key setup wizard."""
    print("\n🔐 GABRIEL KEY SETUP WIZARD")
    print("=" * 50)
    
    loader = SecureKeyLoader()
    
    for key_id, config in KEY_REGISTRY.items():
        existing = loader.keychain.get_key(config.key_name)
        status = "✅ SET" if existing else "❌ NOT SET"
        
        print(f"\n{key_id}:")
        print(f"  Provider: {config.provider.value}")
        print(f"  Role: {config.role.value}")
        print(f"  Env var: {config.env_var}")
        print(f"  Status: {status}")
        
        if not existing:
            response = input("  Enter key (or press Enter to skip): ").strip()
            if response:
                loader.store_key_interactive(key_id, response)
    
    print("\n✅ Key setup complete!")

# =============================================================================
# SINGLETON INSTANCES
# =============================================================================

# Global instances
_key_loader: Optional[SecureKeyLoader] = None
_redactor: Optional[SecretRedactor] = None

def get_key_loader() -> SecureKeyLoader:
    """Get the global key loader instance."""
    global _key_loader
    if _key_loader is None:
        _key_loader = SecureKeyLoader()
    return _key_loader

def get_redactor() -> SecretRedactor:
    """Get the global redactor instance."""
    global _redactor
    if _redactor is None:
        _redactor = SecretRedactor()
    return _redactor

def redact(text: str) -> str:
    """Convenience function to redact secrets."""
    return get_redactor().redact(text)

def get_api_key(provider: str, role: str = "executor") -> Optional[str]:
    """
    Convenience function to get an API key.
    
    Usage:
        key = get_api_key("anthropic", "executor")
    """
    try:
        p = Provider(provider.lower())
        r = Role(role.lower())
        return get_key_loader().get_provider_key(p, r)
    except ValueError:
        return None

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_keys_interactive()
    else:
        print("🔐 GABRIEL Security Module")
        print("\nUsage:")
        print("  python security.py setup    # Interactive key setup")
        print("\nProgrammatic usage:")
        print("  from security import get_api_key, redact")
        print("  key = get_api_key('anthropic', 'executor')")
        print("  safe_log = redact(log_with_secrets)")
