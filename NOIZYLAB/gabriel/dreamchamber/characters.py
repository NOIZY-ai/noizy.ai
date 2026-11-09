"""
DreamChamber Characters
=======================

The inhabitants of the NOIZY universe.

Detective Morrison — The investigator of sound crimes
Marcus the Street Poet — The voice of the unheard
Commander Ash — The leader of the resistance
Guild Master — Guardian of NOIZYVOX
Master Tech — The repair sage
The Registrar — Keeper of consent

Each character has a voice, a purpose, and stories to tell.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class CharacterType(Enum):
    """Types of characters."""
    PROTAGONIST = "protagonist"
    GUIDE = "guide"
    MENTOR = "mentor"
    NARRATOR = "narrator"
    NPC = "npc"
    ANTAGONIST = "antagonist"


class EmotionalState(Enum):
    """Character emotional states."""
    NEUTRAL = "neutral"
    WELCOMING = "welcoming"
    CURIOUS = "curious"
    CONCERNED = "concerned"
    DETERMINED = "determined"
    MYSTERIOUS = "mysterious"
    PASSIONATE = "passionate"
    CONTEMPLATIVE = "contemplative"


@dataclass
class VoiceProfile:
    """Voice characteristics for a character."""
    voice_id: str = ""              # TTS voice ID
    pitch: float = 1.0              # 0.5 - 2.0
    speed: float = 1.0              # 0.5 - 2.0
    tone: str = "neutral"           # warm, cold, raspy, smooth, etc.
    accent: str = "neutral"         # Regional accent
    effects: list[str] = field(default_factory=list)  # reverb, radio, etc.


@dataclass
class DialogueLine:
    """A single line of dialogue."""
    line_id: str = field(default_factory=lambda: str(uuid4()))
    character_id: str = ""
    text: str = ""
    emotion: EmotionalState = EmotionalState.NEUTRAL
    audio_file: Optional[str] = None
    duration_seconds: float = 0.0

    # Delivery
    pause_before: float = 0.0
    pause_after: float = 0.5

    # Animation cues
    gesture: Optional[str] = None
    look_at: Optional[str] = None  # "player", "door_vox", etc.

    # Branching
    triggers_choice: bool = False
    next_line_id: Optional[str] = None


@dataclass
class Character:
    """A character in the DreamChamber."""
    character_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    name: str = ""
    title: str = ""
    character_type: CharacterType = CharacterType.NPC
    description: str = ""

    # Appearance
    model_id: str = ""              # 3D model reference
    portrait: str = ""              # 2D portrait image
    color_scheme: list[str] = field(default_factory=list)

    # Voice
    voice: VoiceProfile = field(default_factory=VoiceProfile)

    # State
    current_emotion: EmotionalState = EmotionalState.NEUTRAL
    is_visible: bool = False
    is_speaking: bool = False

    # Dialogue
    greeting_lines: list[str] = field(default_factory=list)
    dialogue_tree: dict = field(default_factory=dict)

    # Location
    home_scene: str = ""
    current_scene: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# The Characters
# ═══════════════════════════════════════════════════════════════════════════════

def create_detective_morrison() -> Character:
    """Create Detective Morrison."""
    return Character(
        character_id="detective_morrison",
        name="Detective Morrison",
        title="Investigator of Sound Crimes",
        character_type=CharacterType.PROTAGONIST,
        description="""
        Detective Morrison worked the voice crimes beat for fifteen years.
        She's seen it all: stolen identities, synthetic impersonations,
        consent violations that ruined lives. Now she investigates the
        shadows where AI meets authenticity.
        """.strip(),
        color_scheme=["#2d3436", "#636e72", "#dfe6e9"],
        voice=VoiceProfile(
            voice_id="morrison_voice",
            pitch=0.95,
            speed=0.9,
            tone="gravelly",
            accent="noir_detective"
        ),
        current_emotion=EmotionalState.DETERMINED,
        home_scene="noir_city",
        greeting_lines=[
            "Another day, another voice crime. You here to help or just watch?",
            "The streets are full of synthetic whispers. Can you tell real from fake?",
            "I've been tracking this case for months. It's bigger than either of us."
        ]
    )


def create_marcus_street_poet() -> Character:
    """Create Marcus the Street Poet."""
    return Character(
        character_id="marcus_poet",
        name="Marcus",
        title="The Street Poet",
        character_type=CharacterType.GUIDE,
        description="""
        Marcus has been speaking truth on street corners for forty years.
        His voice is weathered by time and injustice, but it carries
        the weight of generations. He knows that voice is power,
        and power must be protected.
        """.strip(),
        color_scheme=["#6c5ce7", "#a29bfe", "#fd79a8"],
        voice=VoiceProfile(
            voice_id="marcus_voice",
            pitch=0.85,
            speed=0.85,
            tone="warm_baritone",
            accent="urban_elder"
        ),
        current_emotion=EmotionalState.CONTEMPLATIVE,
        home_scene="street_corner",
        greeting_lines=[
            "They tried to silence us. But a voice... a voice can't be stolen.",
            "Listen, young one. Your voice is your birthright.",
            "I've seen empires fall and rise. But the human voice? Eternal."
        ]
    )


def create_commander_ash() -> Character:
    """Create Commander Ash."""
    return Character(
        character_id="commander_ash",
        name="Commander Ash",
        title="Leader of the Resistance",
        character_type=CharacterType.MENTOR,
        description="""
        Commander Ash leads the Human Voice Sanctuary from the shadows.
        Former tech executive turned freedom fighter, she saw the threat
        early and built the infrastructure to protect creators. Her word
        is law in the underground.
        """.strip(),
        color_scheme=["#e94560", "#ff6b6b", "#1a1a2e"],
        voice=VoiceProfile(
            voice_id="ash_voice",
            pitch=1.0,
            speed=1.1,
            tone="commanding",
            accent="military_precise"
        ),
        current_emotion=EmotionalState.PASSIONATE,
        home_scene="hvs_command",
        greeting_lines=[
            "Welcome to the Sanctuary. You're one of us now.",
            "Every voice we protect is a victory. Every consent honored is a blow struck.",
            "The machines learn from us. But they will never BE us."
        ]
    )


def create_guild_master() -> Character:
    """Create the Guild Master."""
    return Character(
        character_id="guild_master",
        name="The Guild Master",
        title="Guardian of NOIZYVOX",
        character_type=CharacterType.MENTOR,
        description="""
        No one knows the Guild Master's real name. They've protected
        voice actors for decades, building the infrastructure that
        lets human voices thrive. Ancient and wise, they speak rarely
        but always with purpose.
        """.strip(),
        color_scheme=["#e94560", "#feca57", "#2d3436"],
        voice=VoiceProfile(
            voice_id="guild_master_voice",
            pitch=0.9,
            speed=0.8,
            tone="ancient_wise",
            effects=["subtle_reverb"]
        ),
        current_emotion=EmotionalState.WELCOMING,
        home_scene="noizyvox_entry",
        greeting_lines=[
            "A new voice enters the Guild. Welcome, creator.",
            "Your voice is sovereign here. None may use it without your blessing.",
            "The Guild has protected voices for generations. You are home."
        ]
    )


def create_master_tech() -> Character:
    """Create the Master Tech."""
    return Character(
        character_id="master_tech",
        name="Master Tech",
        title="The Repair Sage",
        character_type=CharacterType.GUIDE,
        description="""
        Master Tech has fixed everything from vintage synthesizers to
        quantum processors. They believe technology should serve humanity,
        not enslave it. Every repair is an act of preservation.
        """.strip(),
        color_scheme=["#0f3460", "#00d9ff", "#16213e"],
        voice=VoiceProfile(
            voice_id="tech_voice",
            pitch=1.05,
            speed=1.0,
            tone="precise_friendly",
            accent="technical"
        ),
        current_emotion=EmotionalState.CURIOUS,
        home_scene="noizylab_entry",
        greeting_lines=[
            "Every device has a story. Let's find out yours.",
            "Repair, don't replace. That's the way.",
            "Technology should serve you. Not the other way around."
        ]
    )


def create_the_registrar() -> Character:
    """Create The Registrar."""
    return Character(
        character_id="registrar",
        name="The Registrar",
        title="Keeper of Consent",
        character_type=CharacterType.GUIDE,
        description="""
        The Registrar maintains the immutable ledger of creator consent.
        They've seen every scheme, every loophole, every attempt to
        circumvent creator rights. Nothing escapes their notice.
        """.strip(),
        color_scheme=["#00b894", "#00d9ff", "#1a1a2e"],
        voice=VoiceProfile(
            voice_id="registrar_voice",
            pitch=1.0,
            speed=1.0,
            tone="precise",
            accent="formal"
        ),
        current_emotion=EmotionalState.NEUTRAL,
        home_scene="noizyfish_entry",
        greeting_lines=[
            "Your consent is your power. Register it. Protect it.",
            "The ledger never lies. Every decision recorded. Every right preserved.",
            "No amount of money overrides a creator's no."
        ]
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Character Manager
# ═══════════════════════════════════════════════════════════════════════════════

class CharacterManager:
    """Manages all characters in the DreamChamber."""

    def __init__(self):
        self.characters: dict[str, Character] = {}
        self._init_characters()

    def _init_characters(self):
        """Initialize all characters."""
        characters = [
            create_detective_morrison(),
            create_marcus_street_poet(),
            create_commander_ash(),
            create_guild_master(),
            create_master_tech(),
            create_the_registrar()
        ]

        for char in characters:
            self.characters[char.character_id] = char

    def get_character(self, character_id: str) -> Optional[Character]:
        """Get a character by ID."""
        return self.characters.get(character_id)

    def get_characters_in_scene(self, scene_id: str) -> list[Character]:
        """Get all characters in a scene."""
        return [
            char for char in self.characters.values()
            if char.current_scene == scene_id or char.home_scene == scene_id
        ]

    def get_greeting(self, character_id: str) -> Optional[DialogueLine]:
        """Get a random greeting from a character."""
        import random

        char = self.characters.get(character_id)
        if not char or not char.greeting_lines:
            return None

        text = random.choice(char.greeting_lines)

        return DialogueLine(
            character_id=character_id,
            text=text,
            emotion=char.current_emotion
        )

    def start_dialogue(self, character_id: str, topic: str = "greeting") -> list[DialogueLine]:
        """Start a dialogue with a character."""
        char = self.characters.get(character_id)
        if not char:
            return []

        char.is_speaking = True

        if topic == "greeting":
            greeting = self.get_greeting(character_id)
            return [greeting] if greeting else []

        # Get dialogue tree for topic
        dialogue = char.dialogue_tree.get(topic, [])
        return dialogue


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the characters."""
    print("\n" + "=" * 70)
    print("DREAMCHAMBER CHARACTERS — DEMO")
    print("The inhabitants of the NOIZY universe")
    print("=" * 70)

    manager = CharacterManager()

    print(f"\n  {len(manager.characters)} characters loaded")

    for char_id, char in manager.characters.items():
        print("\n" + "─" * 50)
        print(f"  {char.name}")
        print(f"  \"{char.title}\"")
        print("─" * 50)
        print(f"  Type: {char.character_type.value}")
        print(f"  Emotion: {char.current_emotion.value}")
        print(f"  Home: {char.home_scene}")
        print(f"  Voice: {char.voice.tone}, {char.voice.accent}")
        print(f"\n  Description:")
        for line in char.description.split('\n'):
            if line.strip():
                print(f"    {line.strip()}")

        greeting = manager.get_greeting(char_id)
        if greeting:
            print(f"\n  Greeting: \"{greeting.text}\"")

    print("\n" + "=" * 70)
    print("These are the voices that guide you through NOIZY.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
