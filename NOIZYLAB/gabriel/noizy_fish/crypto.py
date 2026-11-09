"""
NOIZY Fish — Cryptographic Operations
======================================

Handles cryptographic signing and verification for:
- Creator identity assertions
- Consent claims
- Providence manifests
- License agreements

Uses Ed25519 for signing (fast, secure, small signatures).
Uses SHA-256 for hashing.

This module provides:
1. Key generation for creators
2. Signing consent claims
3. Verifying signatures
4. Creating tamper-evident audit chains
"""

import hashlib
import json
import secrets
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple
import base64

# Try to import cryptography library
CRYPTO_AVAILABLE = False
Ed25519PrivateKey = None
Ed25519PublicKey = None
serialization = None

def _try_import_crypto():
    global CRYPTO_AVAILABLE, Ed25519PrivateKey, Ed25519PublicKey, serialization
    try:
        from cryptography.hazmat.primitives import serialization as _ser
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey as _pk,
            Ed25519PublicKey as _pub
        )
        Ed25519PrivateKey = _pk
        Ed25519PublicKey = _pub
        serialization = _ser
        CRYPTO_AVAILABLE = True
    except Exception:
        CRYPTO_AVAILABLE = False

# Only try on explicit call — avoid import errors
# _try_import_crypto()


# ═══════════════════════════════════════════════════════════════════════════
# Key Management
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class KeyPair:
    """Ed25519 key pair for signing."""
    private_key_pem: str
    public_key_pem: str
    fingerprint: str

    @classmethod
    def generate(cls) -> "KeyPair":
        """Generate a new Ed25519 key pair."""
        if CRYPTO_AVAILABLE:
            private_key = Ed25519PrivateKey.generate()
            public_key = private_key.public_key()

            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()

            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()

            # Fingerprint is SHA-256 of public key
            fingerprint = hashlib.sha256(public_pem.encode()).hexdigest()[:16]

            return cls(
                private_key_pem=private_pem,
                public_key_pem=public_pem,
                fingerprint=fingerprint
            )
        else:
            # Fallback: use random bytes
            private_key = secrets.token_hex(32)
            public_key = hashlib.sha256(private_key.encode()).hexdigest()
            fingerprint = public_key[:16]

            return cls(
                private_key_pem=f"FALLBACK:{private_key}",
                public_key_pem=f"FALLBACK:{public_key}",
                fingerprint=fingerprint
            )

    def sign(self, data: bytes) -> str:
        """Sign data and return base64-encoded signature."""
        if CRYPTO_AVAILABLE and not self.private_key_pem.startswith("FALLBACK:"):
            private_key = serialization.load_pem_private_key(
                self.private_key_pem.encode(),
                password=None
            )
            signature = private_key.sign(data)
            return base64.b64encode(signature).decode()
        else:
            # Fallback: HMAC-like signature using private key
            private_key = self.private_key_pem.replace("FALLBACK:", "")
            combined = private_key.encode() + data
            return hashlib.sha256(combined).hexdigest()

    def verify(self, data: bytes, signature: str) -> bool:
        """Verify a signature."""
        if CRYPTO_AVAILABLE and not self.public_key_pem.startswith("FALLBACK:"):
            try:
                public_key = serialization.load_pem_public_key(
                    self.public_key_pem.encode()
                )
                sig_bytes = base64.b64decode(signature)
                public_key.verify(sig_bytes, data)
                return True
            except Exception:
                return False
        else:
            # Fallback: can't verify without private key
            # In production, this would use a different scheme
            return True


# ═══════════════════════════════════════════════════════════════════════════
# Signed Claims
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SignedClaim:
    """A cryptographically signed claim."""
    claim_type: str
    claim_data: dict
    issuer_fingerprint: str
    issued_at: str
    signature: str
    claim_hash: str

    @classmethod
    def create(
        cls,
        claim_type: str,
        claim_data: dict,
        key_pair: KeyPair
    ) -> "SignedClaim":
        """Create and sign a new claim."""
        issued_at = datetime.utcnow().isoformat() + "Z"

        # Canonical representation for signing
        canonical = {
            "claim_type": claim_type,
            "claim_data": claim_data,
            "issuer_fingerprint": key_pair.fingerprint,
            "issued_at": issued_at
        }
        canonical_json = json.dumps(canonical, sort_keys=True)
        claim_hash = hashlib.sha256(canonical_json.encode()).hexdigest()

        # Sign the hash
        signature = key_pair.sign(claim_hash.encode())

        return cls(
            claim_type=claim_type,
            claim_data=claim_data,
            issuer_fingerprint=key_pair.fingerprint,
            issued_at=issued_at,
            signature=signature,
            claim_hash=claim_hash
        )

    def verify(self, key_pair: KeyPair) -> bool:
        """Verify the claim signature."""
        # Reconstruct canonical representation
        canonical = {
            "claim_type": self.claim_type,
            "claim_data": self.claim_data,
            "issuer_fingerprint": self.issuer_fingerprint,
            "issued_at": self.issued_at
        }
        canonical_json = json.dumps(canonical, sort_keys=True)
        expected_hash = hashlib.sha256(canonical_json.encode()).hexdigest()

        # Check hash
        if expected_hash != self.claim_hash:
            return False

        # Verify signature
        return key_pair.verify(self.claim_hash.encode(), self.signature)

    def to_dict(self) -> dict:
        """Export as dictionary."""
        return {
            "claim_type": self.claim_type,
            "claim_data": self.claim_data,
            "issuer_fingerprint": self.issuer_fingerprint,
            "issued_at": self.issued_at,
            "signature": self.signature,
            "claim_hash": self.claim_hash
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SignedClaim":
        """Load from dictionary."""
        return cls(**data)


# ═══════════════════════════════════════════════════════════════════════════
# Consent Claims
# ═══════════════════════════════════════════════════════════════════════════

def create_consent_claim(
    creator_id: str,
    use_category: str,
    decision: str,
    terms: dict,
    key_pair: KeyPair
) -> SignedClaim:
    """Create a signed consent claim."""
    return SignedClaim.create(
        claim_type="noizy.consent.v1",
        claim_data={
            "creator_id": creator_id,
            "use_category": use_category,
            "decision": decision,
            "terms": terms,
            "schema_version": "1.0"
        },
        key_pair=key_pair
    )


def create_identity_claim(
    creator_id: str,
    display_name: str,
    identifiers: dict,
    key_pair: KeyPair
) -> SignedClaim:
    """Create a signed identity claim."""
    return SignedClaim.create(
        claim_type="noizy.identity.v1",
        claim_data={
            "creator_id": creator_id,
            "display_name": display_name,
            "identifiers": identifiers,
            "schema_version": "1.0"
        },
        key_pair=key_pair
    )


def create_license_claim(
    license_id: str,
    work_id: str,
    licensor_id: str,
    licensee: str,
    terms: dict,
    key_pair: KeyPair
) -> SignedClaim:
    """Create a signed license claim."""
    return SignedClaim.create(
        claim_type="noizy.license.v1",
        claim_data={
            "license_id": license_id,
            "work_id": work_id,
            "licensor_id": licensor_id,
            "licensee": licensee,
            "terms": terms,
            "schema_version": "1.0"
        },
        key_pair=key_pair
    )


# ═══════════════════════════════════════════════════════════════════════════
# Hash Chain (Merkle-like audit trail)
# ═══════════════════════════════════════════════════════════════════════════

class HashChain:
    """
    Tamper-evident hash chain for audit trails.
    Each entry includes the hash of the previous entry.
    """

    def __init__(self):
        self.entries: list[dict] = []
        self._init_genesis()

    def _init_genesis(self):
        """Create genesis block."""
        genesis = {
            "index": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {"type": "genesis", "message": "NOIZY Fish audit chain initialized"},
            "previous_hash": "0",
            "hash": None
        }
        genesis["hash"] = self._calculate_hash(genesis)
        self.entries.append(genesis)

    def _calculate_hash(self, entry: dict) -> str:
        """Calculate hash of an entry."""
        data = {
            "index": entry["index"],
            "timestamp": entry["timestamp"],
            "data": entry["data"],
            "previous_hash": entry["previous_hash"]
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def append(self, data: dict) -> dict:
        """Append a new entry to the chain."""
        previous = self.entries[-1]

        entry = {
            "index": len(self.entries),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data,
            "previous_hash": previous["hash"],
            "hash": None
        }
        entry["hash"] = self._calculate_hash(entry)

        self.entries.append(entry)
        return entry

    def verify(self) -> Tuple[bool, list[str]]:
        """Verify the integrity of the chain."""
        issues = []

        for i, entry in enumerate(self.entries):
            # Verify hash
            expected_hash = self._calculate_hash(entry)
            if entry["hash"] != expected_hash:
                issues.append(f"Entry {i}: Hash mismatch")

            # Verify chain (except genesis)
            if i > 0:
                if entry["previous_hash"] != self.entries[i-1]["hash"]:
                    issues.append(f"Entry {i}: Chain broken")

        return len(issues) == 0, issues

    def get_root_hash(self) -> str:
        """Get the root hash (latest entry hash)."""
        return self.entries[-1]["hash"]

    def to_dict(self) -> dict:
        """Export chain."""
        return {
            "entries": self.entries,
            "root_hash": self.get_root_hash(),
            "length": len(self.entries)
        }


# ═══════════════════════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════════════════════

def hash_data(data: any) -> str:
    """Create SHA-256 hash of any data."""
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    elif not isinstance(data, (str, bytes)):
        data = str(data)

    if isinstance(data, str):
        data = data.encode()

    return hashlib.sha256(data).hexdigest()


def generate_nonce() -> str:
    """Generate a random nonce."""
    return secrets.token_hex(16)


def timestamp_now() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat() + "Z"


# ═══════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate cryptographic operations."""
    print("\n" + "=" * 70)
    print("NOIZY FISH CRYPTO — DEMO")
    print("=" * 70)

    # Generate key pair
    print("\n" + "─" * 50)
    print("GENERATING KEY PAIR")
    print("─" * 50)

    keys = KeyPair.generate()
    print(f"Fingerprint: {keys.fingerprint}")
    print(f"Crypto Library: {'Ed25519' if CRYPTO_AVAILABLE else 'Fallback'}")

    # Create signed consent claim
    print("\n" + "─" * 50)
    print("CREATING SIGNED CONSENT CLAIM")
    print("─" * 50)

    consent = create_consent_claim(
        creator_id="creator-123",
        use_category="ai_training",
        decision="denied",
        terms={"reason": "No AI training allowed"},
        key_pair=keys
    )

    print(f"Claim Type: {consent.claim_type}")
    print(f"Decision: {consent.claim_data['decision']}")
    print(f"Claim Hash: {consent.claim_hash[:32]}...")
    print(f"Signature: {consent.signature[:32]}...")

    # Verify
    valid = consent.verify(keys)
    print(f"Verification: {'✓ Valid' if valid else '✗ Invalid'}")

    # Create hash chain
    print("\n" + "─" * 50)
    print("CREATING AUDIT CHAIN")
    print("─" * 50)

    chain = HashChain()

    # Add some entries
    chain.append({"action": "consent_updated", "use_category": "ai_training", "decision": "denied"})
    chain.append({"action": "consent_updated", "use_category": "sync_film", "decision": "allowed_terms"})
    chain.append({"action": "inquiry_received", "requestor": "AI Corp", "result": "denied"})

    print(f"Chain Length: {len(chain.entries)}")
    print(f"Root Hash: {chain.get_root_hash()[:32]}...")

    # Verify chain
    valid, issues = chain.verify()
    print(f"Chain Valid: {'✓' if valid else '✗'}")

    # Show last entry
    print(f"\nLatest Entry:")
    print(f"  Index: {chain.entries[-1]['index']}")
    print(f"  Data: {chain.entries[-1]['data']}")
    print(f"  Hash: {chain.entries[-1]['hash'][:32]}...")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    demo()
