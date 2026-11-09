#!/usr/bin/env python3
"""
✅ GABRIEL VERIFICATION SYSTEM
==============================
Two-pass verification with claim extraction and citations.

Features:
- Claim extraction from responses
- Risk rating (low/medium/high)
- Grounded verification for medium/high risk claims
- Citations contract enforcement
- Search grounding toggle
"""

import json
import re
import hashlib
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

# =============================================================================
# CONFIGURATION
# =============================================================================

GABRIEL_ROOT = Path("/Users/m2ultra/NOIZYLAB/GABRIEL")
VERIFY_DIR = GABRIEL_ROOT / "verification"
VERIFY_DIR.mkdir(exist_ok=True)

# =============================================================================
# TYPES
# =============================================================================

class RiskLevel(Enum):
    """Risk level for claims."""
    LOW = "low"           # Creative, subjective, opinion
    MEDIUM = "medium"     # Factual but common knowledge
    HIGH = "high"         # Specific facts, numbers, citations needed
    CRITICAL = "critical" # Medical, legal, financial advice

class VerificationStatus(Enum):
    """Verification result status."""
    OK_TO_SHIP = "OK_TO_SHIP"           # Verified, can publish
    NEEDS_REVIEW = "NEEDS_REVIEW"       # Human review recommended
    UNVERIFIED = "UNVERIFIED"           # Could not verify
    FLAGGED = "FLAGGED"                 # Contains problematic claims
    FAILED = "FAILED"                   # Verification failed

@dataclass
class Claim:
    """An extracted claim from content."""
    id: str
    text: str
    risk_level: RiskLevel
    category: str  # factual, statistical, quote, reference, opinion
    context: str   # Surrounding text
    
    # Verification results
    verified: Optional[bool] = None
    sources: List[str] = field(default_factory=list)
    confidence: float = 0.0
    notes: str = ""

@dataclass
class VerificationResult:
    """Result of verification process."""
    status: VerificationStatus
    timestamp: str
    
    # Content info
    content_hash: str
    content_preview: str
    
    # Claims analysis
    total_claims: int = 0
    verified_claims: int = 0
    unverified_claims: int = 0
    flagged_claims: int = 0
    
    claims: List[Claim] = field(default_factory=list)
    
    # Overall assessment
    risk_score: float = 0.0  # 0-1, higher = more risky
    citations_required: bool = False
    citations_provided: List[str] = field(default_factory=list)
    
    # Recommendations
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d['status'] = self.status.value
        for i, c in enumerate(d['claims']):
            c['risk_level'] = self.claims[i].risk_level.value
        return d

# =============================================================================
# CLAIM PATTERNS
# =============================================================================

# Patterns that indicate factual claims needing verification
FACTUAL_PATTERNS = [
    r'\d+%',                           # Percentages
    r'\$[\d,]+',                       # Dollar amounts
    r'\d{4}',                          # Years
    r'according to',                   # Attribution
    r'studies show',                   # Research claims
    r'research (indicates|shows|proves)',
    r'scientifically proven',
    r'experts (say|agree|believe)',
    r'statistics show',
    r'data (shows|indicates)',
    r'\d+ (million|billion|thousand)', # Large numbers
    r'(always|never|every|none)',      # Absolutes
]

# Patterns indicating high-risk content
HIGH_RISK_PATTERNS = [
    r'(cure|treat|heal)\s+\w+',        # Medical claims
    r'guaranteed (returns?|results?)', # Financial promises
    r'legal(ly)?\s+(allowed|required)',# Legal claims
    r'(FDA|SEC|FTC)\s+approved',       # Regulatory claims
    r'investment (advice|recommendation)',
    r'(diagnos|prescri)',              # Medical advice
    r'(will|won\'t)\s+cause\s+cancer', # Health claims
]

# Low-risk patterns (opinions, creative content)
LOW_RISK_PATTERNS = [
    r'I (think|believe|feel)',
    r'in my opinion',
    r'(might|could|may)\s+be',
    r'(seems|appears)\s+to',
    r'one (way|option|approach)',
    r'consider(ing)?',
]

# =============================================================================
# CLAIM EXTRACTOR
# =============================================================================

class ClaimExtractor:
    """Extract and classify claims from content."""
    
    def __init__(self):
        self._factual_patterns = [re.compile(p, re.IGNORECASE) for p in FACTUAL_PATTERNS]
        self._high_risk_patterns = [re.compile(p, re.IGNORECASE) for p in HIGH_RISK_PATTERNS]
        self._low_risk_patterns = [re.compile(p, re.IGNORECASE) for p in LOW_RISK_PATTERNS]
    
    def extract_claims(self, content: str) -> List[Claim]:
        """Extract claims from content."""
        claims = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]\s+', content)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            
            # Determine risk level
            risk = self._assess_risk(sentence)
            
            # Determine category
            category = self._categorize(sentence)
            
            # Only extract non-trivial claims
            if risk != RiskLevel.LOW or category == "factual":
                claim = Claim(
                    id=f"claim_{hashlib.md5(sentence.encode()).hexdigest()[:8]}",
                    text=sentence,
                    risk_level=risk,
                    category=category,
                    context=self._get_context(sentences, i)
                )
                claims.append(claim)
        
        return claims
    
    def _assess_risk(self, text: str) -> RiskLevel:
        """Assess risk level of a claim."""
        # Check high risk first
        for pattern in self._high_risk_patterns:
            if pattern.search(text):
                return RiskLevel.HIGH
        
        # Check low risk
        for pattern in self._low_risk_patterns:
            if pattern.search(text):
                return RiskLevel.LOW
        
        # Check factual patterns (medium risk)
        factual_matches = sum(1 for p in self._factual_patterns if p.search(text))
        if factual_matches >= 2:
            return RiskLevel.HIGH
        elif factual_matches >= 1:
            return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
    
    def _categorize(self, text: str) -> str:
        """Categorize the type of claim."""
        text_lower = text.lower()
        
        if any(p in text_lower for p in ['according to', 'said', 'stated', 'reported']):
            return "quote"
        if re.search(r'\d+%|\d+ (percent|million|billion)', text_lower):
            return "statistical"
        if re.search(r'(study|research|data|survey)', text_lower):
            return "reference"
        if any(p.search(text) for p in self._low_risk_patterns):
            return "opinion"
        
        return "factual"
    
    def _get_context(self, sentences: List[str], index: int) -> str:
        """Get surrounding context."""
        start = max(0, index - 1)
        end = min(len(sentences), index + 2)
        return ' '.join(sentences[start:end])[:200]

# =============================================================================
# VERIFIER
# =============================================================================

class Verifier:
    """
    Two-pass verification system.
    
    Usage:
        verifier = Verifier()
        result = await verifier.verify(content, search_grounding=True)
        
        if result.status == VerificationStatus.OK_TO_SHIP:
            # Safe to publish
        elif result.status == VerificationStatus.NEEDS_REVIEW:
            # Human review needed
    """
    
    def __init__(self, search_grounding: bool = True):
        self.search_grounding = search_grounding
        self.extractor = ClaimExtractor()
    
    async def verify(self, content: str, context: Dict = None) -> VerificationResult:
        """
        Two-pass verification.
        
        Pass 1: Extract claims, rate risk
        Pass 2: Verify medium/high risk claims
        """
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Pass 1: Claim extraction
        claims = self.extractor.extract_claims(content)
        
        # Pass 2: Verify risky claims
        verified_count = 0
        flagged_count = 0
        
        for claim in claims:
            if claim.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
                # Verify this claim
                await self._verify_claim(claim)
                
                if claim.verified:
                    verified_count += 1
                elif claim.verified is False:
                    flagged_count += 1
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(claims)
        
        # Determine status
        status = self._determine_status(claims, risk_score, flagged_count)
        
        # Check citations requirement
        citations_required = any(c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] 
                                 and c.category == "factual" for c in claims)
        
        # Extract any citations in content
        citations_provided = self._extract_citations(content)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(claims, status, citations_required, citations_provided)
        
        result = VerificationResult(
            status=status,
            timestamp=datetime.now().isoformat(),
            content_hash=content_hash,
            content_preview=content[:200],
            total_claims=len(claims),
            verified_claims=verified_count,
            unverified_claims=len([c for c in claims if c.verified is None]),
            flagged_claims=flagged_count,
            claims=claims,
            risk_score=risk_score,
            citations_required=citations_required,
            citations_provided=citations_provided,
            recommendations=recommendations
        )
        
        # Save verification result
        self._save_result(result)
        
        return result
    
    async def _verify_claim(self, claim: Claim):
        """Verify a single claim (placeholder for actual verification)."""
        # In production, this would:
        # 1. Search for corroborating sources
        # 2. Check against known facts database
        # 3. Use a verification LLM
        
        if self.search_grounding:
            # Simulate search verification
            # TODO: Integrate with actual search API
            pass
        
        # For now, mark as unverified if no search
        if not self.search_grounding:
            claim.verified = None
            claim.notes = "Search grounding disabled"
            return
        
        # Default: needs manual verification
        claim.verified = None
        claim.confidence = 0.5
        claim.notes = "Requires manual verification"
    
    def _calculate_risk_score(self, claims: List[Claim]) -> float:
        """Calculate overall risk score (0-1)."""
        if not claims:
            return 0.0
        
        weights = {
            RiskLevel.LOW: 0.1,
            RiskLevel.MEDIUM: 0.4,
            RiskLevel.HIGH: 0.7,
            RiskLevel.CRITICAL: 1.0
        }
        
        total_weight = sum(weights[c.risk_level] for c in claims)
        return min(1.0, total_weight / len(claims))
    
    def _determine_status(self, claims: List[Claim], risk_score: float, 
                         flagged_count: int) -> VerificationStatus:
        """Determine overall verification status."""
        if flagged_count > 0:
            return VerificationStatus.FLAGGED
        
        if any(c.risk_level == RiskLevel.CRITICAL and not c.verified for c in claims):
            return VerificationStatus.NEEDS_REVIEW
        
        if risk_score > 0.7:
            return VerificationStatus.NEEDS_REVIEW
        
        if risk_score > 0.4:
            unverified = sum(1 for c in claims if c.verified is None and 
                           c.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH])
            if unverified > 2:
                return VerificationStatus.UNVERIFIED
        
        return VerificationStatus.OK_TO_SHIP
    
    def _extract_citations(self, content: str) -> List[str]:
        """Extract citations/references from content."""
        citations = []
        
        # URL patterns
        urls = re.findall(r'https?://[^\s\)]+', content)
        citations.extend(urls[:10])
        
        # Reference patterns like [1], [source], etc.
        refs = re.findall(r'\[([^\]]+)\]', content)
        for ref in refs[:10]:
            if not ref.startswith('http'):
                citations.append(f"[{ref}]")
        
        return citations
    
    def _generate_recommendations(self, claims: List[Claim], status: VerificationStatus,
                                   citations_required: bool, citations_provided: List[str]) -> List[str]:
        """Generate recommendations based on verification."""
        recommendations = []
        
        if status == VerificationStatus.FLAGGED:
            recommendations.append("⚠️ Content contains flagged claims - DO NOT PUBLISH without review")
        
        if status == VerificationStatus.NEEDS_REVIEW:
            recommendations.append("👁️ Human review recommended before publishing")
        
        if citations_required and not citations_provided:
            recommendations.append("📚 Add citations for factual claims (required for OK_TO_SHIP)")
        
        high_risk = [c for c in claims if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        if high_risk:
            recommendations.append(f"🎯 {len(high_risk)} high-risk claims need verification")
        
        unverified = [c for c in claims if c.verified is None]
        if unverified:
            recommendations.append(f"❓ {len(unverified)} claims could not be automatically verified")
        
        if not recommendations:
            recommendations.append("✅ Content passed verification checks")
        
        return recommendations
    
    def _save_result(self, result: VerificationResult):
        """Save verification result to disk."""
        result_file = VERIFY_DIR / f"verify_{result.content_hash}.json"
        result_file.write_text(json.dumps(result.to_dict(), indent=2))

# =============================================================================
# CITATIONS CONTRACT
# =============================================================================

class CitationsContract:
    """
    Enforce citations contract.
    
    If verdict=OK_TO_SHIP and content is factual:
    - Must include citations, OR
    - Must mark as "UNVERIFIED"
    """
    
    @staticmethod
    def check(result: VerificationResult, content: str) -> Tuple[bool, str]:
        """
        Check if content meets citations contract.
        
        Returns:
            (passes, message)
        """
        if result.status != VerificationStatus.OK_TO_SHIP:
            return True, "Not shipping - citations not required"
        
        if not result.citations_required:
            return True, "No high-risk factual claims"
        
        # Check for citations
        if result.citations_provided:
            return True, f"Citations provided: {len(result.citations_provided)}"
        
        # Check for UNVERIFIED marker
        if "UNVERIFIED" in content or "[unverified]" in content.lower():
            return True, "Content marked as UNVERIFIED"
        
        return False, "❌ CITATIONS CONTRACT VIOLATION: Factual claims require citations or UNVERIFIED marker"
    
    @staticmethod
    def add_unverified_marker(content: str, claims: List[Claim]) -> str:
        """Add UNVERIFIED markers to content."""
        unverified_claims = [c for c in claims if c.verified is None 
                           and c.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]]
        
        if not unverified_claims:
            return content
        
        # Add disclaimer
        disclaimer = "\n\n---\n⚠️ **UNVERIFIED CONTENT**: The following claims could not be independently verified:\n"
        for claim in unverified_claims[:5]:
            disclaimer += f"- \"{claim.text[:100]}...\"\n"
        
        return content + disclaimer

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def verify_content(content: str, search_grounding: bool = True) -> VerificationResult:
    """Quick verification of content."""
    verifier = Verifier(search_grounding=search_grounding)
    return await verifier.verify(content)

def extract_claims(content: str) -> List[Dict]:
    """Extract and analyze claims from content."""
    extractor = ClaimExtractor()
    claims = extractor.extract_claims(content)
    return [asdict(c) for c in claims]

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    import asyncio
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "test":
            # Test with sample content
            test_content = """
            According to a 2023 study, 73% of developers use AI tools daily.
            The global AI market will reach $500 billion by 2025.
            I think this is a great approach to solving the problem.
            This medicine can cure your headaches instantly.
            """
            
            async def test():
                result = await verify_content(test_content, search_grounding=False)
                print("\n✅ VERIFICATION RESULT")
                print("=" * 50)
                print(f"Status: {result.status.value}")
                print(f"Risk Score: {result.risk_score:.2f}")
                print(f"Total Claims: {result.total_claims}")
                print(f"\nClaims:")
                for c in result.claims:
                    print(f"  [{c.risk_level.value}] {c.text[:60]}...")
                print(f"\nRecommendations:")
                for r in result.recommendations:
                    print(f"  {r}")
            
            asyncio.run(test())
        
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("✅ GABRIEL Verification System")
        print("\nUsage:")
        print("  python verifier.py test   # Run test verification")
