"""
DreamChamber Narrative Engine
=============================

Branching stories, choices, and consequences.

Every visitor creates their own journey through NOIZY.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class BeatType(Enum):
    """Types of story beats."""
    EXPOSITION = "exposition"       # Scene setting
    DIALOGUE = "dialogue"           # Character speaks
    CHOICE = "choice"               # Player makes choice
    REVELATION = "revelation"       # Important information
    TRANSITION = "transition"       # Move to new scene
    CHALLENGE = "challenge"         # Task or puzzle
    CONSEQUENCE = "consequence"     # Result of prior choice


class StoryBranch(Enum):
    """Major story branches."""
    MAIN = "main"                   # Main narrative
    VOICE_GUILD = "voice_guild"     # NOIZYVOX storyline
    REPAIR_PATH = "repair_path"     # NOIZYLAB storyline
    YOUTH_JOURNEY = "youth_journey" # NOIZYKIDZ storyline
    CONSENT_WAR = "consent_war"     # NOIZYFISH storyline
    UNDERGROUND = "underground"     # Hidden paths


@dataclass
class Choice:
    """A choice the player can make."""
    choice_id: str = field(default_factory=lambda: str(uuid4()))

    # Content
    text: str = ""
    subtext: str = ""  # Smaller hint text

    # Requirements
    requires_flag: Optional[str] = None
    requires_visit: Optional[str] = None  # Scene ID

    # Effects
    sets_flag: Optional[str] = None
    leads_to: str = ""  # Beat ID
    triggers_event: Optional[str] = None

    # Presentation
    position: int = 0  # Order in choice list
    style: str = "default"  # default, highlighted, dangerous


@dataclass
class StoryBeat:
    """A single moment in the narrative."""
    beat_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    name: str = ""
    beat_type: BeatType = BeatType.EXPOSITION
    branch: StoryBranch = StoryBranch.MAIN

    # Content
    text: str = ""
    speaker_id: Optional[str] = None  # Character ID
    scene_id: Optional[str] = None

    # Choices
    choices: list[Choice] = field(default_factory=list)
    auto_advance: bool = False
    auto_advance_delay: float = 3.0
    next_beat_id: Optional[str] = None

    # Effects
    sets_flags: list[str] = field(default_factory=list)
    triggers_audio: Optional[str] = None
    triggers_visual: Optional[str] = None
    unlocks_scene: Optional[str] = None

    # Requirements
    requires_flags: list[str] = field(default_factory=list)

    # Metadata
    is_critical: bool = False  # Can't be skipped
    emotional_tone: str = "neutral"


@dataclass
class NarrativeState:
    """Current state of the narrative."""
    current_beat_id: Optional[str] = None
    current_branch: StoryBranch = StoryBranch.MAIN

    # Flags (key decisions made)
    flags: set = field(default_factory=set)

    # History
    beats_visited: list[str] = field(default_factory=list)
    choices_made: list[dict] = field(default_factory=list)

    # Progress
    branches_unlocked: set = field(default_factory=lambda: {StoryBranch.MAIN})
    scenes_unlocked: set = field(default_factory=set)

    def has_flag(self, flag: str) -> bool:
        """Check if flag is set."""
        return flag in self.flags

    def set_flag(self, flag: str):
        """Set a flag."""
        self.flags.add(flag)


class NarrativeEngine:
    """
    The narrative engine for the DreamChamber.

    Manages:
    - Story progression
    - Branching paths
    - Player choices
    - Flags and consequences
    """

    def __init__(self):
        self.beats: dict[str, StoryBeat] = {}
        self.state = NarrativeState()

        # Initialize core narrative
        self._init_core_narrative()

    def _init_core_narrative(self):
        """Initialize the core narrative beats."""

        # ─────────────────────────────────────────────────────────────────
        # THE VOID SEQUENCE
        # ─────────────────────────────────────────────────────────────────

        self.add_beat(StoryBeat(
            beat_id="void_opening",
            name="The Void",
            beat_type=BeatType.EXPOSITION,
            text="""
            You arrive in darkness.
            A low hum begins to vibrate in your chest.
            30 Hz. The frequency of the earth itself.
            """.strip(),
            emotional_tone="mysterious",
            auto_advance=True,
            auto_advance_delay=8.0,
            next_beat_id="void_question"
        ))

        self.add_beat(StoryBeat(
            beat_id="void_question",
            name="The Question",
            beat_type=BeatType.DIALOGUE,
            text="Why are you here?",
            emotional_tone="mysterious",
            choices=[
                Choice(
                    text="I'm looking for something.",
                    leads_to="void_seeker",
                    sets_flag="seeker"
                ),
                Choice(
                    text="I was called.",
                    leads_to="void_called",
                    sets_flag="called"
                ),
                Choice(
                    text="I don't know.",
                    leads_to="void_lost",
                    sets_flag="lost"
                )
            ]
        ))

        self.add_beat(StoryBeat(
            beat_id="void_seeker",
            name="The Seeker",
            beat_type=BeatType.REVELATION,
            text="""
            A seeker. Good.
            The four doors hold what you seek.
            But choose wisely. Each path changes you.
            """.strip(),
            auto_advance=True,
            auto_advance_delay=5.0,
            next_beat_id="doors_appear"
        ))

        self.add_beat(StoryBeat(
            beat_id="void_called",
            name="The Called",
            beat_type=BeatType.REVELATION,
            text="""
            Yes. You were called.
            We've been waiting for you.
            The resistance needs voices like yours.
            """.strip(),
            sets_flags=["resistance_aware"],
            auto_advance=True,
            auto_advance_delay=5.0,
            next_beat_id="doors_appear"
        ))

        self.add_beat(StoryBeat(
            beat_id="void_lost",
            name="The Lost",
            beat_type=BeatType.DIALOGUE,
            text="""
            Being lost is the first step to being found.
            Let the doors guide you.
            Trust the one that calls to you.
            """.strip(),
            auto_advance=True,
            auto_advance_delay=5.0,
            next_beat_id="doors_appear"
        ))

        self.add_beat(StoryBeat(
            beat_id="doors_appear",
            name="The Four Doors",
            beat_type=BeatType.REVELATION,
            text="""
            Four doors materialize from the darkness.
            Each pulses with different energy.
            Each leads to a different world.
            """.strip(),
            triggers_visual="doors_materialize",
            triggers_audio="emergence_sound",
            auto_advance=True,
            auto_advance_delay=4.0,
            next_beat_id="door_choice"
        ))

        self.add_beat(StoryBeat(
            beat_id="door_choice",
            name="Choose Your Path",
            beat_type=BeatType.CHOICE,
            text="Which door calls to you?",
            is_critical=True,
            choices=[
                Choice(
                    text="NOIZYVOX — The Voice Guild",
                    subtext="Where human voices are sovereign",
                    leads_to="noizyvox_entry",
                    sets_flag="chose_vox",
                    style="highlighted"
                ),
                Choice(
                    text="NOIZYLAB — The Repair Network",
                    subtext="Where technology serves humanity",
                    leads_to="noizylab_entry",
                    sets_flag="chose_lab"
                ),
                Choice(
                    text="NOIZYKIDZ — The Youth Program",
                    subtext="Where young minds learn to create",
                    leads_to="noizykidz_entry",
                    sets_flag="chose_kidz"
                ),
                Choice(
                    text="NOIZYFISH — The Consent Registry",
                    subtext="Where creator rights are absolute",
                    leads_to="noizyfish_entry",
                    sets_flag="chose_fish"
                )
            ]
        ))

        # ─────────────────────────────────────────────────────────────────
        # NOIZYVOX ENTRY
        # ─────────────────────────────────────────────────────────────────

        self.add_beat(StoryBeat(
            beat_id="noizyvox_entry",
            name="Guild Hall",
            beat_type=BeatType.TRANSITION,
            branch=StoryBranch.VOICE_GUILD,
            text="""
            The door opens with a resonant hum.
            You step into the Guild Hall.
            Ancient columns reach toward a ceiling lost in shadow.
            """.strip(),
            scene_id="noizyvox_hall",
            triggers_visual="door_open_vox",
            auto_advance=True,
            auto_advance_delay=4.0,
            next_beat_id="guild_master_intro"
        ))

        self.add_beat(StoryBeat(
            beat_id="guild_master_intro",
            name="The Guild Master",
            beat_type=BeatType.DIALOGUE,
            branch=StoryBranch.VOICE_GUILD,
            speaker_id="guild_master",
            text="A new voice enters the Guild. Welcome, creator.",
            emotional_tone="welcoming",
            choices=[
                Choice(
                    text="What is this place?",
                    leads_to="guild_explanation"
                ),
                Choice(
                    text="How do I join?",
                    leads_to="guild_join"
                ),
                Choice(
                    text="I'm just looking.",
                    leads_to="guild_observe"
                )
            ]
        ))

        # ─────────────────────────────────────────────────────────────────
        # NOIZYFISH ENTRY
        # ─────────────────────────────────────────────────────────────────

        self.add_beat(StoryBeat(
            beat_id="noizyfish_entry",
            name="The Registry",
            beat_type=BeatType.TRANSITION,
            branch=StoryBranch.CONSENT_WAR,
            text="""
            The door dissolves into streams of data.
            You step into the Registry.
            Walls of flowing consent records stretch infinitely.
            """.strip(),
            scene_id="noizyfish_registry",
            triggers_visual="door_open_fish",
            auto_advance=True,
            auto_advance_delay=4.0,
            next_beat_id="registrar_intro"
        ))

        self.add_beat(StoryBeat(
            beat_id="registrar_intro",
            name="The Registrar",
            beat_type=BeatType.DIALOGUE,
            branch=StoryBranch.CONSENT_WAR,
            speaker_id="registrar",
            text="Your consent is your power. Register it. Protect it.",
            emotional_tone="precise",
            choices=[
                Choice(
                    text="What is consent in this context?",
                    leads_to="consent_explanation"
                ),
                Choice(
                    text="I want to register my work.",
                    leads_to="registration_flow"
                ),
                Choice(
                    text="Show me the ledger.",
                    leads_to="ledger_view"
                )
            ]
        ))

    def add_beat(self, beat: StoryBeat):
        """Add a story beat."""
        self.beats[beat.beat_id] = beat

    def start(self, beat_id: str = "void_opening") -> dict:
        """Start the narrative."""
        self.state = NarrativeState()
        return self.go_to_beat(beat_id)

    def go_to_beat(self, beat_id: str) -> dict:
        """Navigate to a specific beat."""
        beat = self.beats.get(beat_id)
        if not beat:
            return {"error": f"Beat not found: {beat_id}"}

        # Check requirements
        for flag in beat.requires_flags:
            if not self.state.has_flag(flag):
                return {"error": f"Missing required flag: {flag}"}

        # Set state
        self.state.current_beat_id = beat_id
        self.state.current_branch = beat.branch
        self.state.beats_visited.append(beat_id)

        # Apply effects
        for flag in beat.sets_flags:
            self.state.set_flag(flag)

        if beat.unlocks_scene:
            self.state.scenes_unlocked.add(beat.unlocks_scene)

        # Filter available choices
        available_choices = []
        for choice in beat.choices:
            if choice.requires_flag and not self.state.has_flag(choice.requires_flag):
                continue
            available_choices.append({
                "choice_id": choice.choice_id,
                "text": choice.text,
                "subtext": choice.subtext,
                "style": choice.style,
                "position": choice.position
            })

        return {
            "beat_id": beat_id,
            "name": beat.name,
            "type": beat.beat_type.value,
            "branch": beat.branch.value,
            "text": beat.text,
            "speaker_id": beat.speaker_id,
            "scene_id": beat.scene_id,
            "emotional_tone": beat.emotional_tone,
            "choices": sorted(available_choices, key=lambda c: c["position"]),
            "auto_advance": beat.auto_advance,
            "auto_advance_delay": beat.auto_advance_delay if beat.auto_advance else None,
            "triggers": {
                "audio": beat.triggers_audio,
                "visual": beat.triggers_visual
            }
        }

    def make_choice(self, choice_id: str) -> dict:
        """Make a choice."""
        current_beat = self.beats.get(self.state.current_beat_id)
        if not current_beat:
            return {"error": "No current beat"}

        # Find the choice
        choice = None
        for c in current_beat.choices:
            if c.choice_id == choice_id:
                choice = c
                break

        if not choice:
            return {"error": f"Choice not found: {choice_id}"}

        # Record choice
        self.state.choices_made.append({
            "beat_id": current_beat.beat_id,
            "choice_id": choice_id,
            "text": choice.text,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Apply choice effects
        if choice.sets_flag:
            self.state.set_flag(choice.sets_flag)

        # Navigate to next beat
        return self.go_to_beat(choice.leads_to)

    def advance(self) -> dict:
        """Auto-advance to next beat."""
        current_beat = self.beats.get(self.state.current_beat_id)
        if not current_beat:
            return {"error": "No current beat"}

        if not current_beat.next_beat_id:
            return {"error": "No next beat"}

        return self.go_to_beat(current_beat.next_beat_id)

    def get_state(self) -> dict:
        """Get current narrative state."""
        return {
            "current_beat_id": self.state.current_beat_id,
            "current_branch": self.state.current_branch.value,
            "flags": list(self.state.flags),
            "beats_visited": len(self.state.beats_visited),
            "choices_made": len(self.state.choices_made),
            "branches_unlocked": [b.value for b in self.state.branches_unlocked],
            "scenes_unlocked": list(self.state.scenes_unlocked)
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the narrative engine."""
    print("\n" + "=" * 70)
    print("DREAMCHAMBER NARRATIVE ENGINE — DEMO")
    print("Your journey through NOIZY")
    print("=" * 70)

    engine = NarrativeEngine()

    print(f"\n  {len(engine.beats)} story beats loaded")

    # Start the narrative
    print("\n" + "─" * 50)
    print("1. THE VOID")
    print("─" * 50)

    result = engine.start()
    print(f"\n  [{result['name']}]")
    print(f"  {result['text']}")
    print(f"\n  (auto-advancing in {result['auto_advance_delay']}s...)")

    # Advance
    result = engine.advance()
    print(f"\n  [{result['name']}]")
    print(f"  \"{result['text']}\"")
    print(f"\n  Choices:")
    for choice in result['choices']:
        print(f"    - {choice['text']}")

    # Make a choice
    print("\n" + "─" * 50)
    print("2. CHOOSING 'I WAS CALLED'")
    print("─" * 50)

    choice_id = result['choices'][1]['choice_id']  # "I was called"
    result = engine.make_choice(choice_id)
    print(f"\n  [{result['name']}]")
    print(f"  {result['text']}")

    state = engine.get_state()
    print(f"\n  Flags set: {state['flags']}")

    # Continue to doors
    print("\n" + "─" * 50)
    print("3. THE FOUR DOORS")
    print("─" * 50)

    result = engine.advance()  # doors_appear
    print(f"\n  [{result['name']}]")
    print(f"  {result['text']}")
    print(f"  Triggers: {result['triggers']}")

    result = engine.advance()  # door_choice
    print(f"\n  [{result['name']}]")
    print(f"  \"{result['text']}\"")
    print(f"\n  Choices:")
    for choice in result['choices']:
        style_marker = "*" if choice['style'] == 'highlighted' else " "
        print(f"  {style_marker} {choice['text']}")
        print(f"      {choice['subtext']}")

    # Choose NOIZYVOX
    print("\n" + "─" * 50)
    print("4. ENTERING NOIZYVOX")
    print("─" * 50)

    choice_id = result['choices'][0]['choice_id']  # NOIZYVOX
    result = engine.make_choice(choice_id)
    print(f"\n  [{result['name']}] — Branch: {result['branch']}")
    print(f"  {result['text']}")

    result = engine.advance()  # guild_master_intro
    print(f"\n  Character: {result['speaker_id']}")
    print(f"  \"{result['text']}\"")

    # Final state
    print("\n" + "─" * 50)
    print("5. JOURNEY STATE")
    print("─" * 50)

    state = engine.get_state()
    print(f"\n  Beats visited: {state['beats_visited']}")
    print(f"  Choices made: {state['choices_made']}")
    print(f"  Flags: {state['flags']}")
    print(f"  Current branch: {state['current_branch']}")

    print("\n" + "=" * 70)
    print("Every choice shapes your journey through NOIZY.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
