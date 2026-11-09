#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   VOICE-TO-ACTION WORKFLOW ENGINE                                             ║
║   Transform voice into immediate action with Claude                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

This module provides voice-first workflows optimized for:
- Siri → Claude pipeline
- Quick voice capture
- Hands-free coding
- Meeting/conversation processing
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import json


class VoiceIntent(Enum):
    """Types of voice intents."""
    COMMAND = "command"      # Do something
    QUESTION = "question"    # Answer something
    CAPTURE = "capture"      # Remember something
    CREATE = "create"        # Make something
    PROCESS = "process"      # Transform something


@dataclass
class VoiceWorkflow:
    """A voice-to-action workflow."""
    trigger_phrase: str
    intent: VoiceIntent
    prompt_template: str
    follow_up: Optional[str] = None
    siri_phrase: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════════

VOICE_WORKFLOWS: Dict[str, VoiceWorkflow] = {

    # ─────────────────────────────────────────────────────────────────────────
    # COMMAND WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    "code_it": VoiceWorkflow(
        trigger_phrase="code it",
        intent=VoiceIntent.COMMAND,
        siri_phrase="Hey Siri, code it",
        prompt_template="""
/SS-VOICE-CODE

I'm going to describe code I need. Generate it immediately.
- Clean, production-ready code
- Include brief comments
- Ready to use

Voice description:
{input}
""",
        follow_up="The code has been generated. Want me to explain any part?"
    ),

    "fix_it": VoiceWorkflow(
        trigger_phrase="fix it",
        intent=VoiceIntent.COMMAND,
        siri_phrase="Hey Siri, fix it",
        prompt_template="""
/SS-VOICE-FIX

I'm describing a problem. Give me the fix immediately.
1. What's wrong (one line)
2. The fix (code or solution)
3. Done

Problem:
{input}
"""
    ),

    "send_email": VoiceWorkflow(
        trigger_phrase="send email",
        intent=VoiceIntent.CREATE,
        siri_phrase="Hey Siri, send email",
        prompt_template="""
/SS-VOICE-EMAIL

Draft an email based on what I describe:
- Professional tone
- Clear subject line
- Ready to send

Email details:
{input}
"""
    ),

    "reply_to": VoiceWorkflow(
        trigger_phrase="reply to",
        intent=VoiceIntent.CREATE,
        siri_phrase="Hey Siri, reply to",
        prompt_template="""
/SS-VOICE-REPLY

I'm going to describe a message I received and what I want to say.
Draft the perfect reply:
- Match their tone
- Address their points
- Clear next steps

Context:
{input}
"""
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # QUESTION WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    "how_do_i": VoiceWorkflow(
        trigger_phrase="how do I",
        intent=VoiceIntent.QUESTION,
        siri_phrase="Hey Siri, how do I",
        prompt_template="""
/SS-VOICE-HOW

Answer this how-to question:
1. Quick answer (one sentence)
2. Steps to do it
3. Pro tip

Question:
{input}
"""
    ),

    "what_is": VoiceWorkflow(
        trigger_phrase="what is",
        intent=VoiceIntent.QUESTION,
        siri_phrase="Hey Siri, what is",
        prompt_template="""
/SS-VOICE-WHAT

Explain this clearly:
1. Simple definition
2. Why it matters
3. Example

Question:
{input}
"""
    ),

    "explain": VoiceWorkflow(
        trigger_phrase="explain",
        intent=VoiceIntent.QUESTION,
        siri_phrase="Hey Siri, explain",
        prompt_template="""
/SS-VOICE-EXPLAIN

Explain this concept:
1. ELI5 version
2. Full explanation
3. Analogy that makes it click

Concept:
{input}
"""
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # CAPTURE WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    "remember_this": VoiceWorkflow(
        trigger_phrase="remember this",
        intent=VoiceIntent.CAPTURE,
        siri_phrase="Hey Siri, remember this",
        prompt_template="""
/SS-VOICE-REMEMBER

Capture this information:
1. Core content (cleaned up)
2. Category/tags
3. Any action items
4. Reminder if needed

To remember:
{input}
"""
    ),

    "quick_note": VoiceWorkflow(
        trigger_phrase="quick note",
        intent=VoiceIntent.CAPTURE,
        siri_phrase="Hey Siri, quick note",
        prompt_template="""
/SS-VOICE-NOTE

Process this quick note:
1. Clean and format the content
2. Extract any tasks
3. Add tags

Note:
{input}
"""
    ),

    "capture_idea": VoiceWorkflow(
        trigger_phrase="capture idea",
        intent=VoiceIntent.CAPTURE,
        siri_phrase="Hey Siri, capture idea",
        prompt_template="""
/SS-VOICE-IDEA

Capture and expand this idea:
1. Core concept (one line)
2. Why it's interesting
3. Three ways to develop it
4. First action step

Idea:
{input}
"""
    ),

    "meeting_notes": VoiceWorkflow(
        trigger_phrase="meeting notes",
        intent=VoiceIntent.CAPTURE,
        siri_phrase="Hey Siri, meeting notes",
        prompt_template="""
/SS-VOICE-MEETING

Process these meeting notes:
1. Key decisions
2. Action items (who/what/when)
3. Follow-ups needed
4. Summary for sharing

Notes:
{input}
"""
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # CREATE WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    "write_script": VoiceWorkflow(
        trigger_phrase="write script",
        intent=VoiceIntent.CREATE,
        siri_phrase="Hey Siri, write script",
        prompt_template="""
/SS-VOICE-SCRIPT

Create a voice script based on my description:
- Natural speech patterns
- Breath marks and pauses
- Ready to record

Script for:
{input}
"""
    ),

    "create_post": VoiceWorkflow(
        trigger_phrase="create post",
        intent=VoiceIntent.CREATE,
        siri_phrase="Hey Siri, create post",
        prompt_template="""
/SS-VOICE-POST

Create a social media post:
1. Hook (first line that grabs attention)
2. Body (the message)
3. CTA (what to do next)
4. Hashtags if relevant

Post about:
{input}
"""
    ),

    # ─────────────────────────────────────────────────────────────────────────
    # PROCESS WORKFLOWS
    # ─────────────────────────────────────────────────────────────────────────

    "summarize_this": VoiceWorkflow(
        trigger_phrase="summarize this",
        intent=VoiceIntent.PROCESS,
        siri_phrase="Hey Siri, summarize this",
        prompt_template="""
/SS-VOICE-SUMMARY

Summarize what I describe:
1. One-line summary
2. Key points (3-5)
3. Action items if any

Content:
{input}
"""
    ),

    "translate_to": VoiceWorkflow(
        trigger_phrase="translate to",
        intent=VoiceIntent.PROCESS,
        siri_phrase="Hey Siri, translate to",
        prompt_template="""
/SS-VOICE-TRANSLATE

Translate this content:
1. Direct translation
2. Natural/localized version
3. Cultural notes if relevant

To translate:
{input}
"""
    ),

    "clean_up": VoiceWorkflow(
        trigger_phrase="clean up",
        intent=VoiceIntent.PROCESS,
        siri_phrase="Hey Siri, clean up",
        prompt_template="""
/SS-VOICE-CLEANUP

Clean up and improve this:
- Fix grammar and clarity
- Improve flow
- Keep my voice/intent

To clean up:
{input}
"""
    ),
}


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE PROCESSOR
# ═══════════════════════════════════════════════════════════════════════════════

class VoiceProcessor:
    """Process voice input and route to appropriate workflow."""

    def __init__(self):
        self.workflows = VOICE_WORKFLOWS

    def detect_intent(self, voice_input: str) -> Optional[VoiceWorkflow]:
        """Detect which workflow matches the voice input."""
        voice_lower = voice_input.lower().strip()

        # Check for trigger phrases
        for name, workflow in self.workflows.items():
            if voice_lower.startswith(workflow.trigger_phrase):
                return workflow

        # Default to capture if no match
        return self.workflows.get("quick_note")

    def process(self, voice_input: str) -> str:
        """Process voice input and return the formatted prompt."""
        workflow = self.detect_intent(voice_input)

        if workflow:
            # Remove trigger phrase from input
            clean_input = voice_input
            if voice_input.lower().startswith(workflow.trigger_phrase):
                clean_input = voice_input[len(workflow.trigger_phrase):].strip()

            return workflow.prompt_template.format(input=clean_input)

        # Fallback: general processing
        return f"""
/SS-VOICE-AUTO

Process this voice input:
1. Understand what I need
2. Take the appropriate action
3. Provide a clear response

Voice input:
{voice_input}
"""

    def generate_siri_shortcuts(self) -> List[Dict]:
        """Generate Siri Shortcuts configuration."""
        shortcuts = []

        for name, workflow in self.workflows.items():
            if workflow.siri_phrase:
                shortcuts.append({
                    "name": f"SS Voice: {name.replace('_', ' ').title()}",
                    "siri_phrase": workflow.siri_phrase,
                    "intent": workflow.intent.value,
                    "actions": [
                        {"action": "dictate_text"},
                        {"action": "set_variable", "name": "voice_input"},
                        {"action": "text", "content": workflow.prompt_template},
                        {"action": "replace_text", "find": "{input}", "replace": "{voice_input}"},
                        {"action": "copy_to_clipboard"},
                        {"action": "open_app", "app": "Claude"}
                    ]
                })

        return shortcuts


# ═══════════════════════════════════════════════════════════════════════════════
# HANDS-FREE CODING MODE
# ═══════════════════════════════════════════════════════════════════════════════

HANDS_FREE_CODING = """
/SS-HANDS-FREE-CODING

HANDS-FREE CODING MODE ACTIVATED

I'm going to describe code verbally. You will:
1. Understand my intent despite speech-to-text errors
2. Generate clean, working code
3. Ask clarifying questions only if critical
4. Assume reasonable defaults

Voice coding conventions:
- "new line" = actual newline
- "indent" = add indentation
- "function called X" = def X():
- "variable X equals Y" = x = y
- "if X then Y" = if x: y
- "for each X in Y" = for x in y:
- "return X" = return x
- "import X" = import x
- "string X" = "x"
- "number X" = int/float as appropriate

Code description:
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """CLI interface."""
    processor = VoiceProcessor()

    print("\n" + "═" * 60)
    print("  VOICE-TO-ACTION WORKFLOWS")
    print("  SuperSonic Voice Commands for Claude")
    print("═" * 60)

    print(f"\n  {len(VOICE_WORKFLOWS)} voice workflows loaded\n")

    # Group by intent
    for intent in VoiceIntent:
        workflows = [w for w in VOICE_WORKFLOWS.values() if w.intent == intent]
        if workflows:
            print(f"  [{intent.value.upper()}]")
            for w in workflows:
                print(f"    \"{w.trigger_phrase}...\"")
                if w.siri_phrase:
                    print(f"      Siri: {w.siri_phrase}")
            print()

    print("─" * 60)
    print("  SIRI PHRASES")
    print("─" * 60)

    for name, workflow in VOICE_WORKFLOWS.items():
        if workflow.siri_phrase:
            print(f"  {workflow.siri_phrase}")

    print("\n" + "═" * 60)
    print("  Speak → Claude understands → Action happens")
    print("═" * 60 + "\n")


if __name__ == "__main__":
    main()
