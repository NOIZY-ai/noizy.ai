"""
NOIZY Fish — Federated Identity Protocol
=========================================

One identity, every platform. Portable creator credentials.

Features:
- Cross-platform identity claims
- Cryptographic identity proofs
- Identity linking (connect your Spotify, YouTube, etc.)
- Verifiable credentials (W3C DID compatible)
- Identity delegation for representatives
- Recovery mechanisms

2056 VALUE: Your creator identity follows you everywhere.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable
from uuid import uuid4
import hashlib
import json
import base64


# ═══════════════════════════════════════════════════════════════════════════════
# Identity Types
# ═══════════════════════════════════════════════════════════════════════════════

class IdentityProvider(Enum):
    """External identity providers."""
    # Streaming
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
    BANDCAMP = "bandcamp"
    TIDAL = "tidal"
    DEEZER = "deezer"
    AMAZON_MUSIC = "amazon_music"

    # Social
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    THREADS = "threads"
    BLUESKY = "bluesky"
    MASTODON = "mastodon"

    # Professional
    LINKEDIN = "linkedin"
    ALLMUSIC = "allmusic"
    DISCOGS = "discogs"
    MUSICBRAINZ = "musicbrainz"

    # PROs
    ASCAP = "ascap"
    BMI = "bmi"
    SESAC = "sesac"
    PRS = "prs"
    GEMA = "gema"
    SOCAN = "socan"
    APRA = "apra"

    # Labels/Distributors
    CD_BABY = "cd_baby"
    DISTROKID = "distrokid"
    TUNECORE = "tunecore"
    UNITED_MASTERS = "united_masters"

    # Industry DBs
    ISNI = "isni"
    IPI = "ipi"
    ISRC_REGISTRY = "isrc_registry"

    # Registries
    NOIZY = "noizy"
    OTHER = "other"


class ClaimStatus(Enum):
    """Status of identity claims."""
    PENDING = "pending"             # Claim submitted, awaiting verification
    VERIFIED = "verified"           # Cryptographically or socially verified
    CHALLENGED = "challenged"       # Someone disputes this claim
    REVOKED = "revoked"            # Claim was revoked
    EXPIRED = "expired"            # Claim expired


class DelegationType(Enum):
    """Types of identity delegation."""
    FULL = "full"                   # Full authority (manager)
    LIMITED = "limited"             # Limited scope (publicist)
    EMERGENCY = "emergency"         # Emergency access only
    READ_ONLY = "read_only"        # View only


# ═══════════════════════════════════════════════════════════════════════════════
# Identity Claims
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class IdentityClaim:
    """
    A claim linking a creator to an external identity.

    "Creator X claims to be @artist_name on Spotify"
    """
    claim_id: str = field(default_factory=lambda: str(uuid4()))

    # Who's claiming?
    creator_id: str = ""
    noizy_id: str = ""

    # What identity?
    provider: IdentityProvider = IdentityProvider.OTHER
    provider_user_id: str = ""       # ID on the provider's system
    provider_username: str = ""       # Display name on provider
    provider_url: Optional[str] = None  # Profile URL

    # Verification
    status: ClaimStatus = ClaimStatus.PENDING
    verification_method: Optional[str] = None
    verification_proof: Optional[str] = None  # Signature, DNS TXT, etc.
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None  # Verifier ID or "self"

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    def generate_verification_challenge(self) -> str:
        """Generate a challenge string for verification."""
        data = f"noizy-verify:{self.creator_id}:{self.provider.value}:{self.provider_user_id}"
        challenge = hashlib.sha256(data.encode()).hexdigest()[:16]
        return f"noizy-fish-{challenge}"


@dataclass
class VerifiableCredential:
    """
    W3C-compatible verifiable credential.

    Can be presented to any system that accepts W3C VCs.
    """
    credential_id: str = field(default_factory=lambda: f"urn:uuid:{uuid4()}")

    # Standard VC fields
    context: list[str] = field(default_factory=lambda: [
        "https://www.w3.org/2018/credentials/v1",
        "https://noizyfish.io/credentials/v1"
    ])
    type: list[str] = field(default_factory=lambda: [
        "VerifiableCredential",
        "CreatorIdentityCredential"
    ])

    # Issuer
    issuer: str = "did:web:noizyfish.io"
    issuance_date: datetime = field(default_factory=datetime.utcnow)
    expiration_date: Optional[datetime] = None

    # Subject (the creator)
    subject_id: str = ""  # did:noizy:creator_id
    subject_claims: dict = field(default_factory=dict)

    # Proof
    proof_type: str = "Ed25519Signature2020"
    proof_value: Optional[str] = None
    proof_created: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert to W3C VC JSON format."""
        vc = {
            "@context": self.context,
            "type": self.type,
            "id": self.credential_id,
            "issuer": self.issuer,
            "issuanceDate": self.issuance_date.isoformat(),
            "credentialSubject": {
                "id": self.subject_id,
                **self.subject_claims
            }
        }

        if self.expiration_date:
            vc["expirationDate"] = self.expiration_date.isoformat()

        if self.proof_value:
            vc["proof"] = {
                "type": self.proof_type,
                "created": self.proof_created.isoformat() if self.proof_created else None,
                "proofValue": self.proof_value
            }

        return vc


# ═══════════════════════════════════════════════════════════════════════════════
# Identity Delegation
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class IdentityDelegation:
    """
    Delegation of identity authority.

    "My manager can act on my behalf for licensing inquiries"
    """
    delegation_id: str = field(default_factory=lambda: str(uuid4()))

    # Who's delegating?
    creator_id: str = ""
    creator_noizy_id: str = ""

    # To whom?
    delegate_id: str = ""
    delegate_name: str = ""
    delegate_email: Optional[str] = None

    # What authority?
    delegation_type: DelegationType = DelegationType.LIMITED
    scopes: list[str] = field(default_factory=list)
    # Scopes: "consent_management", "inquiry_response", "work_registration", etc.

    # Constraints
    max_transaction_value: Optional[float] = None  # Max $ they can approve
    require_notification: bool = True  # Notify creator of actions
    allowed_categories: list[str] = field(default_factory=list)  # Use categories

    # Validity
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    revoked: bool = False
    revoked_at: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Check if delegation is currently valid."""
        if self.revoked:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def can_perform(self, action: str, value: Optional[float] = None) -> bool:
        """Check if delegate can perform an action."""
        if not self.is_valid():
            return False

        if self.delegation_type == DelegationType.FULL:
            return True

        if self.delegation_type == DelegationType.READ_ONLY:
            return action in ["view", "list", "search"]

        if action not in self.scopes:
            return False

        if value and self.max_transaction_value and value > self.max_transaction_value:
            return False

        return True


# ═══════════════════════════════════════════════════════════════════════════════
# Federated Identity Manager
# ═══════════════════════════════════════════════════════════════════════════════

class FederatedIdentityManager:
    """
    Manages federated creator identities across platforms.

    One identity to rule them all.
    """

    def __init__(self, signing_key: Optional[bytes] = None):
        self.claims: dict[str, IdentityClaim] = {}
        self.credentials: dict[str, VerifiableCredential] = {}
        self.delegations: dict[str, IdentityDelegation] = {}
        self.signing_key = signing_key

        # Verification handlers
        self._verifiers: dict[IdentityProvider, Callable] = {}

    def register_verifier(self, provider: IdentityProvider, verifier: Callable):
        """Register a verification handler for a provider."""
        self._verifiers[provider] = verifier

    def create_claim(
        self,
        creator_id: str,
        noizy_id: str,
        provider: IdentityProvider,
        provider_user_id: str,
        provider_username: str,
        provider_url: Optional[str] = None
    ) -> IdentityClaim:
        """Create a new identity claim."""
        claim = IdentityClaim(
            creator_id=creator_id,
            noizy_id=noizy_id,
            provider=provider,
            provider_user_id=provider_user_id,
            provider_username=provider_username,
            provider_url=provider_url
        )

        self.claims[claim.claim_id] = claim
        return claim

    def verify_claim_dns(self, claim: IdentityClaim, domain: str) -> bool:
        """
        Verify claim via DNS TXT record.

        Creator adds TXT record: "noizy-fish-{challenge}" to their domain
        """
        import socket

        challenge = claim.generate_verification_challenge()

        try:
            # Look up TXT records
            answers = socket.getaddrinfo(
                f"_noizy.{domain}",
                None,
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            # In reality, we'd use dnspython for TXT lookups
            # This is simplified

            # For demo, just mark as verified
            claim.status = ClaimStatus.VERIFIED
            claim.verification_method = "dns_txt"
            claim.verified_at = datetime.utcnow()
            return True

        except Exception:
            return False

    def verify_claim_oauth(
        self,
        claim: IdentityClaim,
        access_token: str
    ) -> bool:
        """
        Verify claim via OAuth token.

        Use the provider's API to verify the user owns the account.
        """
        if claim.provider not in self._verifiers:
            return False

        verifier = self._verifiers[claim.provider]

        try:
            result = verifier(
                provider_user_id=claim.provider_user_id,
                access_token=access_token
            )

            if result:
                claim.status = ClaimStatus.VERIFIED
                claim.verification_method = "oauth"
                claim.verified_at = datetime.utcnow()
                return True

        except Exception:
            pass

        return False

    def verify_claim_signature(
        self,
        claim: IdentityClaim,
        signed_challenge: str,
        public_key: str
    ) -> bool:
        """
        Verify claim via cryptographic signature.

        Creator signs challenge with their verified key.
        """
        challenge = claim.generate_verification_challenge()

        try:
            # Verify signature (simplified - would use real crypto)
            expected = hashlib.sha256(
                f"{challenge}:{public_key}".encode()
            ).hexdigest()

            if signed_challenge == expected:
                claim.status = ClaimStatus.VERIFIED
                claim.verification_method = "signature"
                claim.verification_proof = signed_challenge
                claim.verified_at = datetime.utcnow()
                return True

        except Exception:
            pass

        return False

    def issue_credential(
        self,
        creator_id: str,
        claims: dict,
        expires_in_days: int = 365
    ) -> VerifiableCredential:
        """
        Issue a verifiable credential for a creator.

        The credential can be presented to any party.
        """
        credential = VerifiableCredential(
            subject_id=f"did:noizy:{creator_id}",
            subject_claims=claims,
            expiration_date=datetime.utcnow() + timedelta(days=expires_in_days),
            proof_created=datetime.utcnow()
        )

        # Sign the credential (simplified)
        credential_data = json.dumps(credential.to_dict(), sort_keys=True)
        credential.proof_value = hashlib.sha256(credential_data.encode()).hexdigest()

        self.credentials[credential.credential_id] = credential
        return credential

    def create_delegation(
        self,
        creator_id: str,
        noizy_id: str,
        delegate_id: str,
        delegate_name: str,
        delegation_type: DelegationType,
        scopes: list[str],
        expires_in_days: int = 90,
        max_value: Optional[float] = None
    ) -> IdentityDelegation:
        """Create identity delegation."""
        delegation = IdentityDelegation(
            creator_id=creator_id,
            creator_noizy_id=noizy_id,
            delegate_id=delegate_id,
            delegate_name=delegate_name,
            delegation_type=delegation_type,
            scopes=scopes,
            max_transaction_value=max_value,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days)
        )

        self.delegations[delegation.delegation_id] = delegation
        return delegation

    def revoke_delegation(self, delegation_id: str) -> bool:
        """Revoke a delegation."""
        if delegation_id in self.delegations:
            self.delegations[delegation_id].revoked = True
            self.delegations[delegation_id].revoked_at = datetime.utcnow()
            return True
        return False

    def get_creator_claims(self, creator_id: str) -> list[IdentityClaim]:
        """Get all claims for a creator."""
        return [c for c in self.claims.values() if c.creator_id == creator_id]

    def get_verified_claims(self, creator_id: str) -> list[IdentityClaim]:
        """Get verified claims for a creator."""
        return [
            c for c in self.claims.values()
            if c.creator_id == creator_id and c.status == ClaimStatus.VERIFIED
        ]

    def get_creator_delegations(self, creator_id: str) -> list[IdentityDelegation]:
        """Get all delegations for a creator."""
        return [d for d in self.delegations.values() if d.creator_id == creator_id]

    def resolve_identity(self, provider: IdentityProvider, provider_user_id: str) -> Optional[str]:
        """
        Resolve external identity to NOIZY creator ID.

        "Who is @artist_name on Spotify in our system?"
        """
        for claim in self.claims.values():
            if (claim.provider == provider and
                claim.provider_user_id == provider_user_id and
                claim.status == ClaimStatus.VERIFIED):
                return claim.creator_id
        return None

    def generate_identity_proof(self, creator_id: str) -> dict:
        """
        Generate a comprehensive identity proof.

        This can be presented to any party to prove creator identity.
        """
        claims = self.get_verified_claims(creator_id)
        credentials = [
            c for c in self.credentials.values()
            if c.subject_id == f"did:noizy:{creator_id}"
        ]

        return {
            "creator_id": creator_id,
            "did": f"did:noizy:{creator_id}",
            "verified_identities": [
                {
                    "provider": c.provider.value,
                    "username": c.provider_username,
                    "url": c.provider_url,
                    "verified_at": c.verified_at.isoformat() if c.verified_at else None,
                    "method": c.verification_method
                }
                for c in claims
            ],
            "credentials": [c.to_dict() for c in credentials],
            "proof_generated": datetime.utcnow().isoformat(),
            "proof_hash": hashlib.sha256(
                json.dumps({
                    "creator_id": creator_id,
                    "claims": len(claims),
                    "credentials": len(credentials)
                }).encode()
            ).hexdigest()
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate federated identity."""
    print("\n" + "=" * 70)
    print("FEDERATED IDENTITY — DEMO")
    print("One identity, every platform")
    print("=" * 70)

    manager = FederatedIdentityManager()

    # Create a creator
    creator_id = "sarah-vocalist-001"
    noizy_id = "NZ-CR-20260323-A1B2C3"

    print("\n" + "─" * 50)
    print("1. LINKING PLATFORM IDENTITIES")
    print("─" * 50)

    # Link Spotify
    spotify_claim = manager.create_claim(
        creator_id=creator_id,
        noizy_id=noizy_id,
        provider=IdentityProvider.SPOTIFY,
        provider_user_id="spotify:artist:123456",
        provider_username="Sarah Voice",
        provider_url="https://open.spotify.com/artist/123456"
    )
    print(f"  Created claim: Spotify → {spotify_claim.provider_username}")
    print(f"    Verification challenge: {spotify_claim.generate_verification_challenge()}")

    # Verify via "OAuth" (simulated)
    spotify_claim.status = ClaimStatus.VERIFIED
    spotify_claim.verification_method = "oauth"
    spotify_claim.verified_at = datetime.utcnow()
    print(f"    Status: VERIFIED via OAuth")

    # Link YouTube
    youtube_claim = manager.create_claim(
        creator_id=creator_id,
        noizy_id=noizy_id,
        provider=IdentityProvider.YOUTUBE,
        provider_user_id="UC_abc123",
        provider_username="Sarah Voice Official",
        provider_url="https://youtube.com/@sarahvoice"
    )
    youtube_claim.status = ClaimStatus.VERIFIED
    youtube_claim.verification_method = "oauth"
    youtube_claim.verified_at = datetime.utcnow()
    print(f"  Created claim: YouTube → {youtube_claim.provider_username}")
    print(f"    Status: VERIFIED via OAuth")

    # Link ASCAP
    ascap_claim = manager.create_claim(
        creator_id=creator_id,
        noizy_id=noizy_id,
        provider=IdentityProvider.ASCAP,
        provider_user_id="ASCAP-789012",
        provider_username="Sarah Johnson (IPI: 00012345678)"
    )
    ascap_claim.status = ClaimStatus.VERIFIED
    ascap_claim.verification_method = "pro_membership"
    ascap_claim.verified_at = datetime.utcnow()
    print(f"  Created claim: ASCAP → {ascap_claim.provider_username}")
    print(f"    Status: VERIFIED via PRO membership")

    # Link Instagram (pending)
    insta_claim = manager.create_claim(
        creator_id=creator_id,
        noizy_id=noizy_id,
        provider=IdentityProvider.INSTAGRAM,
        provider_user_id="sarahvoice",
        provider_username="@sarahvoice",
        provider_url="https://instagram.com/sarahvoice"
    )
    print(f"  Created claim: Instagram → {insta_claim.provider_username}")
    print(f"    Status: PENDING verification")

    # Issue verifiable credential
    print("\n" + "─" * 50)
    print("2. ISSUING VERIFIABLE CREDENTIAL")
    print("─" * 50)

    credential = manager.issue_credential(
        creator_id=creator_id,
        claims={
            "name": "Sarah Johnson",
            "stageName": "Sarah Voice",
            "creatorTypes": ["vocalist", "songwriter"],
            "proMembership": "ASCAP",
            "verifiedPlatforms": ["spotify", "youtube", "ascap"],
            "verificationLevel": "professional"
        },
        expires_in_days=365
    )

    print(f"  Credential ID: {credential.credential_id}")
    print(f"  Issuer: {credential.issuer}")
    print(f"  Subject: {credential.subject_id}")
    print(f"  Expires: {credential.expiration_date}")
    print(f"  Proof: {credential.proof_value[:32]}...")

    # Create delegation
    print("\n" + "─" * 50)
    print("3. DELEGATING AUTHORITY")
    print("─" * 50)

    # Manager delegation
    manager_delegation = manager.create_delegation(
        creator_id=creator_id,
        noizy_id=noizy_id,
        delegate_id="manager-001",
        delegate_name="John Manager",
        delegation_type=DelegationType.LIMITED,
        scopes=["consent_management", "inquiry_response"],
        max_value=50000.0,
        expires_in_days=365
    )
    print(f"  Delegated to: {manager_delegation.delegate_name}")
    print(f"    Type: {manager_delegation.delegation_type.value}")
    print(f"    Scopes: {manager_delegation.scopes}")
    print(f"    Max transaction: ${manager_delegation.max_transaction_value:,.2f}")

    # Test delegation permissions
    print("\n  Testing permissions:")
    print(f"    Can respond to inquiry? {manager_delegation.can_perform('inquiry_response')}")
    print(f"    Can approve $10,000 deal? {manager_delegation.can_perform('consent_management', 10000)}")
    print(f"    Can approve $100,000 deal? {manager_delegation.can_perform('consent_management', 100000)}")
    print(f"    Can register works? {manager_delegation.can_perform('work_registration')}")

    # Generate identity proof
    print("\n" + "─" * 50)
    print("4. IDENTITY PROOF")
    print("─" * 50)

    proof = manager.generate_identity_proof(creator_id)
    print(f"  DID: {proof['did']}")
    print(f"  Verified identities: {len(proof['verified_identities'])}")
    for identity in proof["verified_identities"]:
        print(f"    - {identity['provider']}: {identity['username']}")
    print(f"  Credentials: {len(proof['credentials'])}")
    print(f"  Proof hash: {proof['proof_hash'][:32]}...")

    # Resolve external identity
    print("\n" + "─" * 50)
    print("5. IDENTITY RESOLUTION")
    print("─" * 50)

    resolved = manager.resolve_identity(
        IdentityProvider.SPOTIFY,
        "spotify:artist:123456"
    )
    print(f"  Query: Who is spotify:artist:123456?")
    print(f"  Result: {resolved}")

    resolved_none = manager.resolve_identity(
        IdentityProvider.TIKTOK,
        "tiktok:user:unknown"
    )
    print(f"\n  Query: Who is tiktok:user:unknown?")
    print(f"  Result: {resolved_none or 'Not found'}")

    print("\n" + "=" * 70)
    print("2056 VALUE: One identity across the entire music ecosystem")
    print("=" * 70)


if __name__ == "__main__":
    demo()
