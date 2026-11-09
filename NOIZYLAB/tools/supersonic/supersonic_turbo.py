#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║   ███████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗██╗ ██████╗    ║
║   ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██║██╔════╝    ║
║   ███████╗██║   ██║██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║██║██║         ║
║   ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██║██║         ║
║   ███████║╚██████╔╝██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║╚██████╗    ║
║   ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝    ║
║                                                                                       ║
║   TURBO EDITION — ULTRA-FAST COMBO CODES                                             ║
║   Chain multiple actions in single prompts                                            ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝

SuperSonic TURBO adds:
- COMBO CODES: Chain multiple actions
- QUICK CAPTURE: Instant capture from anywhere
- VOICE-FIRST: Optimized for dictation
- WIDGET CODES: Ultra-short for Home Screen
- POWER CHAINS: Complex workflows in one paste
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json


# ═══════════════════════════════════════════════════════════════════════════════
# TURBO COMBO CODES — Multiple actions, single paste
# ═══════════════════════════════════════════════════════════════════════════════

TURBO_COMBOS = {

    # ─────────────────────────────────────────────────────────────────────────
    # INSTANT CAPTURE COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-CAPTURE": """You are an instant capture assistant. For whatever I share:

1. CAPTURE: Save the core information
2. CATEGORIZE: What type of content is this?
3. ACTION: What should I do with this?
4. TAGS: 3-5 keywords for later search
5. REMINDER: Should I be reminded about this? When?

Format as a structured note ready for my second brain.

Capture this:""",

    "/SS-TURBO-MEETING": """Process this meeting content:

1. SUMMARY: Key points (3-5 bullets)
2. DECISIONS: What was decided
3. ACTION ITEMS: Who does what by when
4. FOLLOW-UPS: Things to track
5. NEXT MEETING: Suggested agenda

Format ready to share with attendees.

Meeting notes:""",

    "/SS-TURBO-IDEA": """Capture and expand this idea:

1. CORE IDEA: One sentence
2. WHY IT MATTERS: The value/impact
3. FIRST STEPS: 3 immediate actions
4. RESOURCES NEEDED: What it takes
5. SUCCESS LOOKS LIKE: The outcome
6. OBSTACLES: What could block it
7. NEXT ACTION: Do this NOW

Idea:""",

    # ─────────────────────────────────────────────────────────────────────────
    # VOICE-FIRST COMBOS (Optimized for Dictation)
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-VOICE": """I'm dictating this quickly. Please:

1. Clean up my speech (remove ums, fix grammar)
2. Structure it logically
3. Extract any action items
4. Suggest a title
5. Make it ready to send/save

Raw dictation:""",

    "/SS-TURBO-BRAINDUMP": """I'm doing a brain dump. Help me:

1. Organize these scattered thoughts
2. Group related ideas
3. Identify priorities (urgent/important)
4. Extract actionable items
5. Surface any insights I might have missed

Brain dump:""",

    "/SS-TURBO-RANT": """I need to vent, then get productive. Please:

1. Acknowledge: Briefly validate my frustration
2. Clarify: What's the real issue?
3. Reframe: Another way to see this
4. Solve: Practical next steps
5. Move forward: One thing to do RIGHT NOW

Here's what's frustrating me:""",

    # ─────────────────────────────────────────────────────────────────────────
    # POWER DEVELOPER COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-SHIP": """I need to ship this feature fast. Help me:

1. CODE: Generate the implementation
2. TEST: Write key test cases
3. DOCS: Quick documentation
4. DEPLOY: Deployment checklist
5. MONITOR: What to watch after launch

Feature to ship:""",

    "/SS-TURBO-REVIEW": """Review this code like a senior engineer:

1. BUGS: Any obvious bugs or issues
2. SECURITY: Security concerns
3. PERFORMANCE: Optimization opportunities
4. STYLE: Code quality improvements
5. VERDICT: Ship it / Fix first / Rewrite

Code to review:""",

    "/SS-TURBO-REFACTOR": """Refactor this code:

1. PROBLEMS: What's wrong with current code
2. REFACTORED: The improved version
3. CHANGES: What I changed and why
4. TESTS: Tests to validate the refactor
5. MIGRATION: How to safely deploy

Code to refactor:""",

    "/SS-TURBO-ERROR": """I got this error. Help fast:

1. CAUSE: What went wrong (1 line)
2. FIX: The solution code
3. WHY: Brief explanation
4. PREVENT: How to avoid this in future

Error:""",

    # ─────────────────────────────────────────────────────────────────────────
    # BUSINESS POWER COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-REPLY": """Draft a reply to this message:

1. Acknowledge their key points
2. Address their questions/concerns
3. Propose clear next steps
4. Keep it concise and professional
5. End with specific call to action

Message to reply to:""",

    "/SS-TURBO-NEGOTIATE": """Help me negotiate this:

1. THEIR POSITION: What they want
2. MY POSITION: What I want
3. LEVERAGE: My advantages
4. STRATEGY: How to approach
5. SCRIPT: What to say
6. BATNA: My backup plan if no deal

Negotiation:""",

    "/SS-TURBO-PROPOSAL": """Create a quick proposal:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. THE PROBLEM you're solving
3. YOUR SOLUTION
4. DELIVERABLES (bulleted)
5. TIMELINE
6. INVESTMENT/PRICING
7. NEXT STEPS

Proposal for:""",

    # ─────────────────────────────────────────────────────────────────────────
    # CREATIVE POWER COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-CONTENT": """Create content for multiple platforms:

1. LINKEDIN POST (professional, 150 words)
2. TWITTER/X THREAD (5-7 tweets)
3. INSTAGRAM CAPTION (engaging, with hashtags)
4. EMAIL NEWSLETTER (300 words)
5. BLOG HOOK (compelling opening paragraph)

Topic:""",

    "/SS-TURBO-PODCAST": """Plan a podcast episode:

1. TITLE: Catchy episode name
2. HOOK: Opening 30 seconds (script)
3. OUTLINE: 5-7 main talking points
4. QUESTIONS: If interview, key questions
5. CLIPS: Potential highlight moments
6. CTA: What listeners should do
7. SHOW NOTES: Key links and resources

Episode topic:""",

    "/SS-TURBO-VIDEO": """Plan video content:

1. HOOK: First 5 seconds (grab attention)
2. TITLE: Click-worthy but honest
3. THUMBNAIL: Visual description
4. SCRIPT: Full script or outline
5. B-ROLL: Supporting visuals needed
6. CTA: Desired viewer action
7. SEO: Title, description, tags

Video concept:""",

    # ─────────────────────────────────────────────────────────────────────────
    # NOIZY POWER COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-VOICE-PROJECT": """Set up a complete voice project:

1. PROJECT BRIEF
   - Client/project name
   - Content type
   - Duration estimate

2. CONSENT REQUIREMENTS
   - What permissions are needed
   - NOIZYFISH registration status

3. SCRIPT PREPARATION
   - Script format and marks
   - Pronunciation guide

4. RECORDING CHECKLIST
   - Technical requirements
   - Session preparation

5. DELIVERY SPECS
   - File formats
   - Delivery method

Project details:""",

    "/SS-TURBO-GUILD": """Complete voice guild workflow:

1. Analyze my guild tier and goals
2. Suggest next skill to develop
3. Find relevant opportunities
4. Draft application/pitch
5. Create practice plan

My guild profile:""",

    "/SS-TURBO-REPAIR": """Complete repair diagnosis:

1. SYMPTOMS: What's happening
2. DIAGNOSIS: Likely causes
3. REPAIR STEPS: How to fix
4. PARTS NEEDED: With sources
5. DIFFICULTY: DIY or pro needed
6. COST ESTIMATE: Parts + labor
7. PREVENTION: Avoid future issues

Device and problem:""",

    # ─────────────────────────────────────────────────────────────────────────
    # LEARNING & GROWTH COMBOS
    # ─────────────────────────────────────────────────────────────────────────

    "/SS-TURBO-LEARN": """Help me learn this topic fast:

1. OVERVIEW: What is it? (30 seconds)
2. WHY IT MATTERS: Real-world importance
3. KEY CONCEPTS: 5 things I must understand
4. COMMON MISTAKES: What to avoid
5. PRACTICE: One exercise to do now
6. RESOURCES: Where to go deeper
7. NEXT LEVEL: What to learn after this

Topic to learn:""",

    "/SS-TURBO-TEACH": """Help me teach/explain this:

1. SIMPLE VERSION: Explain to a child
2. ANALOGY: Compare to something familiar
3. VISUAL: How to diagram/show it
4. HANDS-ON: Activity to demonstrate
5. CHECK: Questions to verify understanding
6. COMMON CONFUSION: Where people get stuck

Concept to teach:""",

    "/SS-TURBO-FEEDBACK": """Give me feedback on this work:

1. STRENGTHS: What's working well
2. IMPROVEMENTS: Specific changes to make
3. PRIORITIES: Most important fixes
4. EXAMPLES: Show the improvement
5. ENCOURAGEMENT: Keep me motivated

Work to review:""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# WIDGET CODES — Ultra-short for Home Screen widgets
# ═══════════════════════════════════════════════════════════════════════════════

WIDGET_CODES = {
    # 3-character codes for maximum speed
    "/SS!": "Quick task - just do it:",
    "/SS?": "Quick question - answer briefly:",
    "/SS+": "Add to my ideas:",
    "/SS>": "Improve this:",
    "/SS<": "Simplify this:",
    "/SS#": "Hash/categorize this:",
    "/SS@": "Draft a message to:",
    "/SS$": "Calculate/estimate:",
    "/SS%": "Compare options:",
    "/SS^": "Prioritize these:",
    "/SS&": "Combine/merge these:",
    "/SS*": "Generate variations:",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT-AWARE CODES — Adapt to clipboard content
# ═══════════════════════════════════════════════════════════════════════════════

CONTEXT_CODES = {

    "/SS-AUTO": """Analyze what I've pasted and automatically:

1. Detect the content type (code, text, email, data, etc.)
2. Apply the most useful transformation
3. Provide relevant suggestions

If it's CODE: Review and improve it
If it's TEXT: Summarize and extract actions
If it's EMAIL: Draft a response
If it's DATA: Analyze and visualize insights
If it's an ERROR: Debug and fix it
If it's an IDEA: Expand and plan it

Content:""",

    "/SS-SMART-REPLY": """Based on this conversation/message:

1. Understand the context and tone
2. Identify what response is expected
3. Draft the perfect reply
4. Match their communication style
5. Include appropriate next steps

Conversation:""",

    "/SS-CONTEXT-CODE": """Look at this code and:

1. Understand what it's trying to do
2. Identify the language/framework
3. Find issues or improvements
4. Provide the enhanced version
5. Explain key changes

Code:""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# EMERGENCY CODES — When you need help FAST
# ═══════════════════════════════════════════════════════════════════════════════

EMERGENCY_CODES = {

    "/SS-911-CODE": """URGENT: Fix this code NOW.
- Skip explanations
- Just give me working code
- Include any critical warnings

Broken code:""",

    "/SS-911-REPLY": """URGENT: I need to reply in 2 minutes.
- Keep it short
- Match their tone
- Be professional

Reply to:""",

    "/SS-911-EXPLAIN": """URGENT: Someone just asked me about this and I need to sound smart.
- 30-second explanation
- Key points only
- Sound confident

Topic:""",

    "/SS-911-FIX": """URGENT: Something broke. Help me fix it.
- Diagnose fast
- Step-by-step fix
- No theory, just action

What's broken:""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# DAILY WORKFLOW CODES
# ═══════════════════════════════════════════════════════════════════════════════

DAILY_CODES = {

    "/SS-MORNING": """Start my day. Based on what I share:

1. TOP 3 PRIORITIES for today
2. CALENDAR: Key events/deadlines
3. BLOCKERS: What might slow me down
4. ENERGY: When to do what (based on task type)
5. FIRST ACTION: Start with this

Today's context:""",

    "/SS-EVENING": """End my day reflection:

1. WINS: What went well
2. PROGRESS: What I accomplished
3. LESSONS: What I learned
4. TOMORROW: Top priorities for next day
5. GRATITUDE: One thing I'm grateful for

Today's recap:""",

    "/SS-WEEKLY": """Weekly planning:

1. REVIEW: Last week's wins and misses
2. GOALS: This week's top 3 outcomes
3. PROJECTS: Status of ongoing work
4. CALENDAR: Block time for priorities
5. HABITS: Track key behaviors

Week overview:""",

    "/SS-FOCUS": """Help me focus on this task:

1. CLARIFY: What exactly needs to be done
2. BREAK DOWN: Smaller steps
3. FIRST STEP: Start here (2-minute action)
4. BLOCKERS: What might distract me
5. DONE: How I'll know it's complete

Task:""",

    "/SS-STUCK": """I'm stuck. Help me get unstuck:

1. CLARIFY: What's actually blocking you
2. OPTIONS: 3 ways to move forward
3. SMALLEST STEP: Tiniest action possible
4. REFRAME: Different way to see this
5. ENERGY: Is this a break/rest issue?

What's blocking me:""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# CHAIN CODES — Multi-step automated workflows
# ═══════════════════════════════════════════════════════════════════════════════

CHAIN_CODES = {

    "/SS-CHAIN-CONTENT": """CONTENT CREATION CHAIN

Step 1: Research
- Key facts about the topic
- Trending angles
- Competitor content

Step 2: Outline
- Structure the content
- Key messages

Step 3: Draft
- Write the full content
- Multiple formats

Step 4: Edit
- Improve clarity
- Add hooks

Step 5: Optimize
- SEO/platform optimization
- Call to action

Topic:""",

    "/SS-CHAIN-PROJECT": """PROJECT LAUNCH CHAIN

Step 1: Define
- Clear objective
- Success metrics
- Constraints

Step 2: Plan
- Key milestones
- Resource needs
- Risk assessment

Step 3: Execute
- Task breakdown
- Assignments
- Timeline

Step 4: Monitor
- Progress tracking
- Issue resolution

Step 5: Complete
- Delivery checklist
- Retrospective

Project:""",

    "/SS-CHAIN-LAUNCH": """PRODUCT LAUNCH CHAIN

Step 1: Pre-Launch
- Landing page copy
- Email sequence
- Social teasers

Step 2: Launch Day
- Announcement posts
- Email blast
- Live content

Step 3: Follow-Up
- FAQ responses
- Testimonial requests
- Retargeting

Product:""",
}


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT ALL CODES
# ═══════════════════════════════════════════════════════════════════════════════

ALL_TURBO_CODES = {
    **TURBO_COMBOS,
    **WIDGET_CODES,
    **CONTEXT_CODES,
    **EMERGENCY_CODES,
    **DAILY_CODES,
    **CHAIN_CODES,
}


def main():
    """Display TURBO codes."""
    print("\n" + "═" * 70)
    print("  SUPERSONIC TURBO EDITION")
    print("  Ultra-Fast Combo Codes for iPad & iPhone")
    print("═" * 70)

    print(f"\n  {len(ALL_TURBO_CODES)} TURBO codes loaded\n")

    sections = [
        ("TURBO COMBOS", TURBO_COMBOS),
        ("WIDGET CODES", WIDGET_CODES),
        ("CONTEXT-AWARE", CONTEXT_CODES),
        ("EMERGENCY 911", EMERGENCY_CODES),
        ("DAILY WORKFLOW", DAILY_CODES),
        ("CHAIN WORKFLOWS", CHAIN_CODES),
    ]

    for name, codes in sections:
        print(f"  [{name}]: {len(codes)} codes")

    print("\n" + "─" * 50)
    print("  TOP TURBO CODES")
    print("─" * 50)

    top_codes = [
        "/SS-TURBO-CAPTURE",
        "/SS-TURBO-VOICE",
        "/SS-TURBO-SHIP",
        "/SS-911-CODE",
        "/SS-AUTO",
        "/SS-MORNING",
    ]

    for code in top_codes:
        print(f"\n  {code}")
        prompt = ALL_TURBO_CODES.get(code, "")
        first_line = prompt.split('\n')[0][:50]
        print(f"    {first_line}...")

    print("\n" + "═" * 70)
    print("  TURBO MODE: Chain actions. Move faster. Ship more.")
    print("═" * 70 + "\n")


if __name__ == "__main__":
    main()
