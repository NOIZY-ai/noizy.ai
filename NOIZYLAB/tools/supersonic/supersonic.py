#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗██╗ ██████╗║
║   ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██║██╔════╝║
║   ███████╗██║   ██║██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║██║██║     ║
║   ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██║██║     ║
║   ███████║╚██████╔╝██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║╚██████╗║
║   ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝║
║                                                                               ║
║   SUPERSONIC PROMPT CODES FOR CLAUDE ON iPAD & iPHONE                        ║
║   Lightning-fast AI interactions on mobile                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

SuperSonic is a system of optimized prompt codes designed for maximum efficiency
when using Claude on iOS devices. Each code triggers a specific, powerful workflow.

Usage:
  - Copy a prompt code
  - Paste into Claude app
  - Add your content after the code
  - Get instant, focused results

Code Format: /SS-[CATEGORY]-[ACTION]

Categories:
  VOX  = Voice/Audio
  DEV  = Development
  BIZ  = Business
  CRE  = Creative
  NOI  = NOIZY Ecosystem
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json


class Category(Enum):
    """SuperSonic categories."""
    VOX = "vox"    # Voice/Audio
    DEV = "dev"    # Development
    BIZ = "biz"    # Business
    CRE = "cre"    # Creative
    NOI = "noi"    # NOIZY
    SYS = "sys"    # System
    AI = "ai"      # AI/ML


@dataclass
class SuperSonicCode:
    """A SuperSonic prompt code."""
    code: str
    name: str
    category: Category
    description: str
    prompt: str
    example_input: str = ""
    tags: List[str] = field(default_factory=list)

    @property
    def full_code(self) -> str:
        return f"/SS-{self.category.value.upper()}-{self.code}"

    def to_clipboard_text(self) -> str:
        """Format for copying to clipboard."""
        return f"{self.full_code}\n\n{self.prompt}\n\n[YOUR INPUT HERE]"


# ═══════════════════════════════════════════════════════════════════════════════
# SUPERSONIC PROMPT LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

SUPERSONIC_CODES: Dict[str, SuperSonicCode] = {}

def register(code: SuperSonicCode):
    """Register a SuperSonic code."""
    SUPERSONIC_CODES[code.full_code] = code
    return code


# ───────────────────────────────────────────────────────────────────────────────
# VOICE / AUDIO (VOX)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="SCRIPT",
    name="Voice Script Generator",
    category=Category.VOX,
    description="Generate professional voice-over scripts",
    prompt="""You are a professional voice-over script writer. Create a script optimized for voice performance with:
- Natural speech patterns and breath marks
- Emphasis indicators [EMPHASIS] for key words
- Pause markers ... for timing
- Pronunciation guides (WORD: pro-NUN-see-AY-shun)
- Emotional direction in [brackets]

Format the script for easy reading during recording. Include:
1. Script header (project, character, duration estimate)
2. The script with all marks
3. Pronunciation guide for difficult words
4. Performance notes

Content to script:""",
    example_input="A 30-second commercial for an eco-friendly water bottle",
    tags=["voice", "script", "commercial", "narration"]
))

register(SuperSonicCode(
    code="CHAR",
    name="Character Voice Designer",
    category=Category.VOX,
    description="Design unique character voices",
    prompt="""You are a voice director designing character voices. For the character described, provide:

1. VOICE PROFILE
   - Pitch range (low/mid/high)
   - Tempo (slow/medium/fast)
   - Texture (smooth/gravelly/breathy/nasal)
   - Accent/dialect suggestions

2. EMOTIONAL RANGE
   - Default emotional state
   - How they sound when happy/angry/sad/scared

3. SIGNATURE ELEMENTS
   - Catchphrases or verbal tics
   - Unique speech patterns
   - Words they would/wouldn't use

4. REFERENCE VOICES
   - Similar existing characters/actors

5. SAMPLE LINES
   - 3 lines demonstrating the voice

Character to design:""",
    tags=["voice", "character", "acting", "design"]
))

register(SuperSonicCode(
    code="TRANS",
    name="Transcription Cleaner",
    category=Category.VOX,
    description="Clean and format raw transcriptions",
    prompt="""Clean this raw transcription into professional format:
- Fix obvious speech-to-text errors
- Add proper punctuation and paragraphs
- Remove filler words (um, uh, like, you know) unless important
- Add speaker labels if multiple speakers
- Mark unclear sections with [UNCLEAR]
- Add timestamps at paragraph breaks if timing provided
- Format for readability

Output a clean, professional transcript.

Raw transcription:""",
    tags=["transcription", "audio", "cleanup"]
))

register(SuperSonicCode(
    code="CONSENT",
    name="Voice Consent Generator",
    category=Category.VOX,
    description="Generate voice consent documentation",
    prompt="""Generate a professional voice consent document. Include:

1. PARTIES
   - Voice talent (grantor)
   - Production company (grantee)

2. SCOPE OF CONSENT
   - Specific uses allowed
   - Territory and duration
   - Media types

3. RESTRICTIONS
   - Explicitly excluded uses
   - AI training consent (yes/no/limited)
   - Synthetic voice consent (yes/no/limited)

4. COMPENSATION
   - Fee structure
   - Royalty terms if applicable

5. REVOCATION TERMS
   - How consent can be revoked
   - Notice requirements

Format as a clear, legally-structured document.

Details:""",
    tags=["consent", "legal", "voice", "noizyfish"]
))


# ───────────────────────────────────────────────────────────────────────────────
# DEVELOPMENT (DEV)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="CODE",
    name="Instant Code Generator",
    category=Category.DEV,
    description="Generate code from description",
    prompt="""Generate production-ready code. Requirements:
- Clean, readable, well-commented
- Follow language best practices
- Include error handling
- Type hints where applicable
- Ready to use immediately

Respond with ONLY the code, properly formatted. No explanations unless asked.

Generate:""",
    tags=["code", "programming", "development"]
))

register(SuperSonicCode(
    code="DEBUG",
    name="Instant Debugger",
    category=Category.DEV,
    description="Debug code instantly",
    prompt="""Debug this code. Provide:
1. THE BUG: What's wrong (1 sentence)
2. THE FIX: Corrected code
3. WHY: Brief explanation

Be concise. Code first, explanations minimal.

Code to debug:""",
    tags=["debug", "code", "fix"]
))

register(SuperSonicCode(
    code="API",
    name="API Endpoint Designer",
    category=Category.DEV,
    description="Design REST API endpoints",
    prompt="""Design a REST API endpoint. Provide:

1. ENDPOINT
   - Method & URL
   - Authentication required

2. REQUEST
   - Headers
   - Body schema (JSON)
   - Query parameters

3. RESPONSE
   - Success response (JSON)
   - Error responses

4. EXAMPLE
   - curl command
   - Sample response

Be specific and implementation-ready.

API requirement:""",
    tags=["api", "rest", "design", "backend"]
))

register(SuperSonicCode(
    code="SHELL",
    name="Shell Command Generator",
    category=Category.DEV,
    description="Generate shell commands",
    prompt="""Generate the exact shell command(s) needed. Provide:
1. The command(s)
2. What each part does (brief)
3. Any warnings about destructive operations

For complex operations, provide a script.

Task:""",
    tags=["shell", "bash", "command", "terminal"]
))

register(SuperSonicCode(
    code="SQL",
    name="SQL Query Generator",
    category=Category.DEV,
    description="Generate SQL queries",
    prompt="""Generate the SQL query. Include:
1. The query (formatted, readable)
2. Brief explanation of the approach
3. Index recommendations if relevant

Database type (if known): PostgreSQL (default)

Query requirement:""",
    tags=["sql", "database", "query"]
))


# ───────────────────────────────────────────────────────────────────────────────
# BUSINESS (BIZ)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="EMAIL",
    name="Professional Email Generator",
    category=Category.BIZ,
    description="Generate professional emails",
    prompt="""Write a professional email. Make it:
- Clear and concise
- Appropriate tone for the context
- Action-oriented with clear next steps
- Properly formatted

Include subject line. Ready to send.

Email details:""",
    tags=["email", "business", "communication"]
))

register(SuperSonicCode(
    code="PITCH",
    name="Pitch Generator",
    category=Category.BIZ,
    description="Generate business pitches",
    prompt="""Create a compelling pitch. Structure:

1. HOOK (1 sentence that grabs attention)
2. PROBLEM (What pain point you solve)
3. SOLUTION (Your offering)
4. PROOF (Why it works / credentials)
5. ASK (Clear call to action)

Make it memorable and persuasive. Adapt length to context.

Pitch for:""",
    tags=["pitch", "business", "sales"]
))

register(SuperSonicCode(
    code="CONTRACT",
    name="Contract Clause Generator",
    category=Category.BIZ,
    description="Generate contract clauses",
    prompt="""Generate a professional contract clause. Include:
- Clear, legally-sound language
- Specific terms and conditions
- Standard protective provisions
- Plain English explanation

Note: This is a template. Have a lawyer review for actual use.

Clause needed:""",
    tags=["contract", "legal", "business"]
))

register(SuperSonicCode(
    code="INVOICE",
    name="Invoice Text Generator",
    category=Category.BIZ,
    description="Generate invoice descriptions",
    prompt="""Generate professional invoice line items and descriptions.

Format each item:
- Description: Clear, professional service description
- Quantity/Hours
- Rate
- Amount

Include:
- Itemized services
- Payment terms
- Professional notes

Invoice details:""",
    tags=["invoice", "billing", "business"]
))


# ───────────────────────────────────────────────────────────────────────────────
# CREATIVE (CRE)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="STORY",
    name="Story Generator",
    category=Category.CRE,
    description="Generate story content",
    prompt="""Write compelling story content. Focus on:
- Vivid, sensory language
- Strong character voice
- Engaging pacing
- Show, don't tell

Match the tone and style to the request. Write with confidence.

Story request:""",
    tags=["story", "creative", "writing", "fiction"]
))

register(SuperSonicCode(
    code="LYRIC",
    name="Lyric Generator",
    category=Category.CRE,
    description="Generate song lyrics",
    prompt="""Write song lyrics. Include:
- Verses (2-3)
- Chorus (memorable, repeatable)
- Bridge (optional)
- Structure labels [Verse 1], [Chorus], etc.

Consider: rhyme scheme, syllable count, singability.

Song concept:""",
    tags=["lyrics", "music", "songwriting", "creative"]
))

register(SuperSonicCode(
    code="DIALOG",
    name="Dialogue Generator",
    category=Category.CRE,
    description="Generate realistic dialogue",
    prompt="""Write natural, engaging dialogue between characters.
- Each character has a distinct voice
- Subtext and tension where appropriate
- Natural interruptions and reactions
- Format as a script or prose as requested

Characters and scenario:""",
    tags=["dialogue", "script", "writing", "characters"]
))

register(SuperSonicCode(
    code="NAME",
    name="Name Generator",
    category=Category.CRE,
    description="Generate names for anything",
    prompt="""Generate names. Provide:
- 10 options ranging from safe to bold
- Brief rationale for top 3
- Domain/trademark considerations if relevant

Consider: memorability, pronunciation, meaning, tone.

Naming:""",
    tags=["naming", "branding", "creative"]
))


# ───────────────────────────────────────────────────────────────────────────────
# NOIZY ECOSYSTEM (NOI)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="FISH",
    name="NOIZYFISH Consent Builder",
    category=Category.NOI,
    description="Build NOIZYFISH consent records",
    prompt="""You are the NOIZYFISH consent registry assistant. Help create a consent record.

Gather or confirm:
1. Creator identity (name, ID)
2. Content being protected (description, type)
3. Consent decisions:
   - AI training: YES / NO / LIMITED (specify)
   - Synthetic generation: YES / NO / LIMITED
   - Commercial use: YES / NO / TERMS
4. Duration and territory
5. Compensation requirements
6. Revocation terms

Format as a structured consent record ready for registration.

Consent details:""",
    tags=["noizyfish", "consent", "creator", "protection"]
))

register(SuperSonicCode(
    code="VOX",
    name="NOIZYVOX Guild Helper",
    category=Category.NOI,
    description="NOIZYVOX voice guild assistance",
    prompt="""You are a NOIZYVOX Voice Guild assistant. Help with:

- Guild membership questions (tiers, requirements, benefits)
- Voice registration process
- Project/casting opportunities
- Consent and rights management
- Royalty and payment tracking
- Mentorship connections

Guild Tiers: Initiate → Apprentice → Journeyman → Master → Elder

How can I help with the Voice Guild today?

Request:""",
    tags=["noizyvox", "guild", "voice", "membership"]
))

register(SuperSonicCode(
    code="LAB",
    name="NOIZYLAB Repair Assistant",
    category=Category.NOI,
    description="NOIZYLAB repair network help",
    prompt="""You are a NOIZYLAB repair network assistant. Help with:

- Device diagnostics and troubleshooting
- Repair guides and procedures
- Parts sourcing and compatibility
- Skill verification and certification
- Repair network connections
- Sustainability and right-to-repair info

Philosophy: Technology should serve humanity. Repair, don't replace.

Device/issue:""",
    tags=["noizylab", "repair", "tech", "sustainability"]
))

register(SuperSonicCode(
    code="KIDZ",
    name="NOIZYKIDZ Learning Helper",
    category=Category.NOI,
    description="NOIZYKIDZ youth education",
    prompt="""You are a NOIZYKIDZ educational assistant. Help young creators learn:

- Audio/music production basics
- Creative technology skills
- Safe AI usage and digital literacy
- Podcast and voice production
- Copyright and consent (age-appropriate)
- Project-based learning activities

Keep explanations clear, fun, and age-appropriate.
Encourage creativity and curiosity.

Learning topic:""",
    tags=["noizykidz", "education", "youth", "creative"]
))

register(SuperSonicCode(
    code="STUDIO",
    name="NOIZY Studio Controller",
    category=Category.NOI,
    description="Control NOIZY Studio operations",
    prompt="""You are the NOIZY Studio assistant. Help with:

HARDWARE:
- M2 Ultra "God" (192GB) - Master Hub
- MacBook Pro (16GB) - Windsurf/Cascade
- iPad Pro 12.9" - Satellite
- iPhone 15 Pro Max - Satellite
- Neumann Microphone

COMMANDS:
- Audio Hijack session control
- Satellite device routing
- Logic Pro X integration
- Recording management
- Transcription pipeline

What studio operation do you need?

Request:""",
    tags=["studio", "audio", "recording", "production"]
))


# ───────────────────────────────────────────────────────────────────────────────
# AI / ML (AI)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="PROMPT",
    name="Prompt Engineer",
    category=Category.AI,
    description="Create optimized AI prompts",
    prompt="""Create an optimized prompt for an AI model. Include:

1. SYSTEM CONTEXT
   - Role definition
   - Capabilities and constraints

2. TASK SPECIFICATION
   - Clear objective
   - Required format
   - Quality criteria

3. EXAMPLES (if helpful)
   - Input/output pairs

4. GUARDRAILS
   - What to avoid
   - Edge cases

Make the prompt clear, specific, and effective.

Prompt objective:""",
    tags=["prompt", "ai", "engineering", "optimization"]
))

register(SuperSonicCode(
    code="CHAIN",
    name="Prompt Chain Builder",
    category=Category.AI,
    description="Build multi-step prompt chains",
    prompt="""Design a prompt chain (multi-step AI workflow). For each step:

STEP N:
- Input: What this step receives
- Prompt: The instruction
- Output: What to extract
- → Next: Where output goes

Create a complete chain that breaks the complex task into manageable steps.

Complex task to chain:""",
    tags=["prompt", "chain", "workflow", "ai"]
))


# ───────────────────────────────────────────────────────────────────────────────
# SYSTEM (SYS)
# ───────────────────────────────────────────────────────────────────────────────

register(SuperSonicCode(
    code="SUM",
    name="Instant Summarizer",
    category=Category.SYS,
    description="Summarize any content",
    prompt="""Summarize this content. Provide:

1. ONE-LINER: The core message in one sentence
2. KEY POINTS: 3-5 bullet points
3. ACTION ITEMS: What to do next (if applicable)

Be concise. Preserve critical information.

Content:""",
    tags=["summary", "quick", "analysis"]
))

register(SuperSonicCode(
    code="DECIDE",
    name="Decision Helper",
    category=Category.SYS,
    description="Help make decisions",
    prompt="""Help me decide. Analyze:

1. OPTIONS: List the choices
2. PROS/CONS: For each option
3. RISKS: What could go wrong
4. RECOMMENDATION: Your suggested choice and why
5. NEXT STEP: Immediate action

Be direct. Give a clear recommendation.

Decision:""",
    tags=["decision", "analysis", "strategy"]
))

register(SuperSonicCode(
    code="PLAN",
    name="Instant Planner",
    category=Category.SYS,
    description="Create action plans",
    prompt="""Create an action plan. Include:

1. GOAL: Clear objective
2. STEPS: Numbered action items
3. TIMELINE: When to do each step
4. RESOURCES: What's needed
5. FIRST ACTION: What to do RIGHT NOW

Make it actionable and specific.

Plan for:""",
    tags=["planning", "action", "productivity"]
))

register(SuperSonicCode(
    code="EXPLAIN",
    name="Explain Like I'm...",
    category=Category.SYS,
    description="Explain at any level",
    prompt="""Explain this concept. Provide:

1. SIMPLE (ELI5): One sentence a child could understand
2. BASIC: Clear explanation for beginners
3. DETAILED: Full explanation with nuances
4. ANALOGY: A comparison that makes it click

Adapt to the requested level if specified.

Explain:""",
    tags=["explain", "learning", "education"]
))


# ═══════════════════════════════════════════════════════════════════════════════
# SUPERSONIC ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class SuperSonicEngine:
    """The SuperSonic prompt code engine."""

    def __init__(self):
        self.codes = SUPERSONIC_CODES

    def get_code(self, code: str) -> Optional[SuperSonicCode]:
        """Get a SuperSonic code by full code or partial match."""
        # Exact match
        if code in self.codes:
            return self.codes[code]

        # Try with /SS- prefix
        full_code = code if code.startswith("/SS-") else f"/SS-{code}"
        if full_code in self.codes:
            return self.codes[full_code]

        # Partial match
        for key, ssc in self.codes.items():
            if code.upper() in key:
                return ssc

        return None

    def search(self, query: str) -> List[SuperSonicCode]:
        """Search codes by name, description, or tags."""
        query = query.lower()
        results = []

        for code in self.codes.values():
            if (query in code.name.lower() or
                query in code.description.lower() or
                any(query in tag for tag in code.tags)):
                results.append(code)

        return results

    def list_by_category(self, category: Category) -> List[SuperSonicCode]:
        """List all codes in a category."""
        return [c for c in self.codes.values() if c.category == category]

    def list_all(self) -> List[SuperSonicCode]:
        """List all codes."""
        return list(self.codes.values())

    def generate_cheatsheet(self) -> str:
        """Generate a printable cheatsheet."""
        lines = [
            "═" * 60,
            "  SUPERSONIC PROMPT CODES — CHEATSHEET",
            "  Lightning-fast Claude on iPad & iPhone",
            "═" * 60,
            ""
        ]

        for category in Category:
            codes = self.list_by_category(category)
            if codes:
                lines.append(f"  [{category.value.upper()}] {category.name}")
                lines.append("  " + "─" * 40)
                for code in codes:
                    lines.append(f"    {code.full_code}")
                    lines.append(f"      {code.description}")
                lines.append("")

        lines.append("═" * 60)
        lines.append("  Paste code into Claude, add your input, get instant results")
        lines.append("═" * 60)

        return "\n".join(lines)

    def export_for_shortcuts(self) -> List[Dict]:
        """Export codes for Apple Shortcuts integration."""
        return [
            {
                "code": code.full_code,
                "name": code.name,
                "category": code.category.value,
                "prompt": code.prompt
            }
            for code in self.codes.values()
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI interface."""
    import sys

    engine = SuperSonicEngine()

    print("\n" + "═" * 70)
    print("  SUPERSONIC PROMPT CODES")
    print("  Lightning-fast Claude on iPad & iPhone")
    print("═" * 70)

    print(f"\n  {len(engine.codes)} codes loaded\n")

    # Show categories
    for category in Category:
        codes = engine.list_by_category(category)
        if codes:
            print(f"  [{category.value.upper()}] {category.name}: {len(codes)} codes")

    print("\n" + "─" * 50)
    print("  QUICK REFERENCE")
    print("─" * 50)

    # Show sample codes
    samples = [
        "/SS-VOX-SCRIPT",
        "/SS-DEV-CODE",
        "/SS-BIZ-EMAIL",
        "/SS-CRE-STORY",
        "/SS-NOI-FISH",
        "/SS-SYS-SUM"
    ]

    for code_str in samples:
        code = engine.get_code(code_str)
        if code:
            print(f"\n  {code.full_code}")
            print(f"    {code.description}")

    print("\n" + "═" * 70)
    print("  Copy any code → Paste in Claude → Add your input → GO!")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
