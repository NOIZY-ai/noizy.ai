"""
DreamChamber Experience Engine
==============================

The core engine that orchestrates the DreamChamber experience.

Manages:
- Scene transitions
- User state
- Audio synchronization
- Narrative progression
- Character appearances
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Callable, Any
from uuid import uuid4
import json


# ═══════════════════════════════════════════════════════════════════════════════
# Experience States
# ═══════════════════════════════════════════════════════════════════════════════

class ExperienceState(Enum):
    """Current state of the DreamChamber experience."""
    LOADING = "loading"           # Assets loading
    VOID_ENTRY = "void_entry"     # Entering the Void
    VOID_DEEP = "void_deep"       # Deep in the Void (30Hz)
    EMERGENCE = "emergence"        # Doors appearing
    DOOR_SELECT = "door_select"   # Choosing a door
    TRANSITION = "transition"      # Moving through door
    SCENE_ACTIVE = "scene_active" # In a scene
    DIALOGUE = "dialogue"          # Character dialogue
    PAUSED = "paused"
    ENDED = "ended"


class TransitionType(Enum):
    """Types of scene transitions."""
    FADE_BLACK = "fade_black"
    FADE_WHITE = "fade_white"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOOR_OPEN = "door_open"
    VOID_COLLAPSE = "void_collapse"
    MATERIALIZATION = "materialization"


# ═══════════════════════════════════════════════════════════════════════════════
# Scene Definition
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Scene:
    """A discrete moment in the DreamChamber experience."""
    scene_id: str = field(default_factory=lambda: str(uuid4()))

    # Identity
    name: str = ""
    description: str = ""

    # Visual
    environment: str = "void"     # void, chamber, city, studio, etc.
    lighting: str = "dark"        # dark, dim, ambient, bright, dramatic
    color_palette: list[str] = field(default_factory=list)
    particles: Optional[str] = None  # none, dust, sparks, data, etc.

    # Audio
    ambient_track: Optional[str] = None
    music_track: Optional[str] = None
    binaural_frequency: Optional[float] = None  # Hz
    spatial_audio: bool = True

    # Characters
    characters_present: list[str] = field(default_factory=list)
    focal_character: Optional[str] = None

    # Narrative
    story_beats: list[str] = field(default_factory=list)
    available_choices: list[str] = field(default_factory=list)

    # Interaction
    interactable_objects: list[str] = field(default_factory=list)
    hotspots: list[dict] = field(default_factory=list)

    # Navigation
    next_scenes: dict = field(default_factory=dict)  # choice -> scene_id
    can_return: bool = True

    # Timing
    min_duration_seconds: float = 0.0
    auto_advance_seconds: Optional[float] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Transition:
    """A transition between scenes."""
    transition_id: str = field(default_factory=lambda: str(uuid4()))

    from_scene: str = ""
    to_scene: str = ""

    transition_type: TransitionType = TransitionType.FADE_BLACK
    duration_seconds: float = 1.5

    # Audio
    transition_sound: Optional[str] = None
    crossfade_audio: bool = True

    # Visual effects
    blur_during: bool = False
    color_shift: Optional[str] = None

    # Callbacks
    on_start: Optional[str] = None  # Function name
    on_complete: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# User Session
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class UserSession:
    """Tracks a user's journey through the DreamChamber."""
    session_id: str = field(default_factory=lambda: str(uuid4()))

    # User info
    user_id: Optional[str] = None
    is_anonymous: bool = True

    # State
    current_state: ExperienceState = ExperienceState.LOADING
    current_scene_id: Optional[str] = None

    # Journey
    scenes_visited: list[str] = field(default_factory=list)
    choices_made: list[dict] = field(default_factory=list)
    doors_entered: list[str] = field(default_factory=list)

    # Characters met
    characters_encountered: list[str] = field(default_factory=list)
    dialogue_history: list[dict] = field(default_factory=list)

    # Audio preferences
    audio_enabled: bool = True
    volume_master: float = 0.8
    volume_music: float = 0.7
    volume_voice: float = 1.0
    volume_ambient: float = 0.5
    binaural_enabled: bool = True

    # VR mode
    vr_enabled: bool = False
    vr_device: Optional[str] = None

    # Timing
    started_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)
    total_duration_seconds: float = 0.0

    def record_scene(self, scene_id: str):
        """Record visiting a scene."""
        self.scenes_visited.append(scene_id)
        self.current_scene_id = scene_id
        self.last_activity = datetime.utcnow()

    def record_choice(self, choice_id: str, context: dict = None):
        """Record a choice made."""
        self.choices_made.append({
            "choice_id": choice_id,
            "scene_id": self.current_scene_id,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        })

    def record_door(self, door_type: str):
        """Record entering a door."""
        self.doors_entered.append(door_type)


# ═══════════════════════════════════════════════════════════════════════════════
# DreamChamber Experience
# ═══════════════════════════════════════════════════════════════════════════════

class DreamChamberExperience:
    """
    The main orchestrator for the DreamChamber experience.

    This is the engine that powers everything.
    """

    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.transitions: dict[str, Transition] = {}
        self.sessions: dict[str, UserSession] = {}

        # Event handlers
        self._on_state_change: list[Callable] = []
        self._on_scene_enter: list[Callable] = []
        self._on_scene_exit: list[Callable] = []
        self._on_choice: list[Callable] = []

        # Initialize default scenes
        self._init_default_scenes()

    def _init_default_scenes(self):
        """Initialize the core DreamChamber scenes."""

        # The Void - Entry
        self.register_scene(Scene(
            scene_id="void_entry",
            name="The Void",
            description="You arrive in darkness. A low hum begins to vibrate in your chest.",
            environment="void",
            lighting="dark",
            color_palette=["#000000", "#0a0a0a", "#1a1a1a"],
            binaural_frequency=30.0,  # The 30Hz tone
            ambient_track="void_ambient",
            min_duration_seconds=5.0,
            next_scenes={"continue": "void_deep"}
        ))

        # The Void - Deep
        self.register_scene(Scene(
            scene_id="void_deep",
            name="Deep Void",
            description="The darkness is complete. You are nowhere and everywhere.",
            environment="void",
            lighting="dark",
            color_palette=["#000000"],
            binaural_frequency=30.0,
            particles="void_particles",
            min_duration_seconds=8.0,
            auto_advance_seconds=12.0,
            next_scenes={"auto": "emergence"}
        ))

        # Emergence - Doors Appear
        self.register_scene(Scene(
            scene_id="emergence",
            name="Emergence",
            description="Four doors begin to materialize from the darkness.",
            environment="void",
            lighting="dim",
            color_palette=["#0a0a0a", "#1a1a2e", "#16213e"],
            particles="materialization",
            ambient_track="emergence_ambient",
            min_duration_seconds=3.0,
            next_scenes={"auto": "door_select"}
        ))

        # Door Selection
        self.register_scene(Scene(
            scene_id="door_select",
            name="The Four Doors",
            description="Four doors stand before you. Each pulses with different energy.",
            environment="chamber",
            lighting="dramatic",
            color_palette=["#1a1a2e", "#e94560", "#0f3460", "#533483"],
            interactable_objects=["door_vox", "door_lab", "door_kidz", "door_fish"],
            hotspots=[
                {"id": "door_vox", "position": [-3, 0, -5], "label": "NOIZYVOX"},
                {"id": "door_lab", "position": [-1, 0, -5], "label": "NOIZYLAB"},
                {"id": "door_kidz", "position": [1, 0, -5], "label": "NOIZYKIDZ"},
                {"id": "door_fish", "position": [3, 0, -5], "label": "NOIZYFISH"}
            ],
            available_choices=["enter_vox", "enter_lab", "enter_kidz", "enter_fish"],
            next_scenes={
                "enter_vox": "noizyvox_entry",
                "enter_lab": "noizylab_entry",
                "enter_kidz": "noizykidz_entry",
                "enter_fish": "noizyfish_entry"
            }
        ))

        # NOIZYVOX Entry
        self.register_scene(Scene(
            scene_id="noizyvox_entry",
            name="NOIZYVOX Guild Hall",
            description="The Voice Guild. Where human voices are sovereign.",
            environment="guild_hall",
            lighting="warm",
            color_palette=["#e94560", "#ff6b6b", "#feca57"],
            ambient_track="guild_ambient",
            characters_present=["guild_master"],
            next_scenes={"continue": "noizyvox_hub"}
        ))

        # NOIZYLAB Entry
        self.register_scene(Scene(
            scene_id="noizylab_entry",
            name="NOIZYLAB Workshop",
            description="The Repair Network. Where technology serves humanity.",
            environment="workshop",
            lighting="industrial",
            color_palette=["#0f3460", "#16213e", "#1a1a2e"],
            ambient_track="workshop_ambient",
            characters_present=["master_tech"],
            next_scenes={"continue": "noizylab_hub"}
        ))

        # NOIZYKIDZ Entry
        self.register_scene(Scene(
            scene_id="noizykidz_entry",
            name="NOIZYKIDZ Academy",
            description="The Youth Program. Where young minds learn to create.",
            environment="academy",
            lighting="bright",
            color_palette=["#533483", "#9b59b6", "#e056fd"],
            ambient_track="academy_ambient",
            characters_present=["mentor"],
            next_scenes={"continue": "noizykidz_hub"}
        ))

        # NOIZYFISH Entry
        self.register_scene(Scene(
            scene_id="noizyfish_entry",
            name="NOIZYFISH Registry",
            description="The Consent Registry. Where creator rights are absolute.",
            environment="registry",
            lighting="tech",
            color_palette=["#00d9ff", "#00ff88", "#00b894"],
            ambient_track="registry_ambient",
            characters_present=["registrar"],
            next_scenes={"continue": "noizyfish_hub"}
        ))

    def register_scene(self, scene: Scene):
        """Register a scene."""
        self.scenes[scene.scene_id] = scene

    def register_transition(self, transition: Transition):
        """Register a transition."""
        key = f"{transition.from_scene}:{transition.to_scene}"
        self.transitions[key] = transition

    def create_session(self, user_id: str = None) -> UserSession:
        """Create a new user session."""
        session = UserSession(
            user_id=user_id,
            is_anonymous=user_id is None
        )
        self.sessions[session.session_id] = session
        return session

    def start_experience(self, session_id: str) -> dict:
        """Start the DreamChamber experience for a session."""
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        session.current_state = ExperienceState.VOID_ENTRY
        session.record_scene("void_entry")

        scene = self.scenes["void_entry"]

        return {
            "session_id": session_id,
            "state": session.current_state.value,
            "scene": self._serialize_scene(scene),
            "audio": {
                "binaural_frequency": scene.binaural_frequency,
                "ambient_track": scene.ambient_track
            }
        }

    def advance(self, session_id: str, choice: str = None) -> dict:
        """Advance to the next scene."""
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        current_scene = self.scenes.get(session.current_scene_id)
        if not current_scene:
            return {"error": "No current scene"}

        # Determine next scene
        if choice and choice in current_scene.next_scenes:
            next_scene_id = current_scene.next_scenes[choice]
            session.record_choice(choice)
        elif "auto" in current_scene.next_scenes:
            next_scene_id = current_scene.next_scenes["auto"]
        elif "continue" in current_scene.next_scenes:
            next_scene_id = current_scene.next_scenes["continue"]
        else:
            return {"error": "No valid transition"}

        # Get transition
        transition_key = f"{session.current_scene_id}:{next_scene_id}"
        transition = self.transitions.get(transition_key)

        # Record door entry if applicable
        if choice and choice.startswith("enter_"):
            door_type = choice.replace("enter_", "")
            session.record_door(door_type)

        # Move to next scene
        session.record_scene(next_scene_id)
        next_scene = self.scenes.get(next_scene_id)

        # Update state
        if "void" in next_scene_id:
            session.current_state = ExperienceState.VOID_DEEP
        elif "door_select" in next_scene_id:
            session.current_state = ExperienceState.DOOR_SELECT
        else:
            session.current_state = ExperienceState.SCENE_ACTIVE

        return {
            "session_id": session_id,
            "state": session.current_state.value,
            "previous_scene": current_scene.scene_id,
            "scene": self._serialize_scene(next_scene),
            "transition": self._serialize_transition(transition) if transition else None,
            "audio": {
                "binaural_frequency": next_scene.binaural_frequency,
                "ambient_track": next_scene.ambient_track,
                "music_track": next_scene.music_track
            }
        }

    def get_session_state(self, session_id: str) -> dict:
        """Get current session state."""
        session = self.sessions.get(session_id)
        if not session:
            return {"error": "Session not found"}

        current_scene = self.scenes.get(session.current_scene_id)

        return {
            "session_id": session_id,
            "state": session.current_state.value,
            "scene": self._serialize_scene(current_scene) if current_scene else None,
            "journey": {
                "scenes_visited": len(session.scenes_visited),
                "choices_made": len(session.choices_made),
                "doors_entered": session.doors_entered,
                "characters_met": session.characters_encountered,
                "duration_seconds": (datetime.utcnow() - session.started_at).total_seconds()
            }
        }

    def _serialize_scene(self, scene: Scene) -> dict:
        """Serialize a scene for client."""
        return {
            "scene_id": scene.scene_id,
            "name": scene.name,
            "description": scene.description,
            "environment": scene.environment,
            "lighting": scene.lighting,
            "color_palette": scene.color_palette,
            "particles": scene.particles,
            "interactable_objects": scene.interactable_objects,
            "hotspots": scene.hotspots,
            "available_choices": scene.available_choices,
            "characters_present": scene.characters_present,
            "min_duration_seconds": scene.min_duration_seconds,
            "auto_advance_seconds": scene.auto_advance_seconds
        }

    def _serialize_transition(self, transition: Transition) -> dict:
        """Serialize a transition for client."""
        return {
            "type": transition.transition_type.value,
            "duration_seconds": transition.duration_seconds,
            "sound": transition.transition_sound,
            "crossfade_audio": transition.crossfade_audio,
            "blur_during": transition.blur_during,
            "color_shift": transition.color_shift
        }

    # Event registration
    def on_state_change(self, callback: Callable):
        """Register state change callback."""
        self._on_state_change.append(callback)

    def on_scene_enter(self, callback: Callable):
        """Register scene enter callback."""
        self._on_scene_enter.append(callback)

    def on_scene_exit(self, callback: Callable):
        """Register scene exit callback."""
        self._on_scene_exit.append(callback)

    def on_choice(self, callback: Callable):
        """Register choice callback."""
        self._on_choice.append(callback)


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the DreamChamber experience."""
    print("\n" + "=" * 70)
    print("DREAMCHAMBER EXPERIENCE — DEMO")
    print("The immersive portal to the NOIZY universe")
    print("=" * 70)

    experience = DreamChamberExperience()

    print(f"\n  Registered {len(experience.scenes)} scenes")

    # Create session
    print("\n" + "─" * 50)
    print("1. CREATING SESSION")
    print("─" * 50)

    session = experience.create_session()
    print(f"  Session ID: {session.session_id[:8]}...")
    print(f"  Anonymous: {session.is_anonymous}")

    # Start experience
    print("\n" + "─" * 50)
    print("2. ENTERING THE VOID")
    print("─" * 50)

    result = experience.start_experience(session.session_id)
    print(f"  State: {result['state']}")
    print(f"  Scene: {result['scene']['name']}")
    print(f"  Description: {result['scene']['description']}")
    print(f"  Binaural: {result['audio']['binaural_frequency']} Hz")

    # Advance through void
    print("\n" + "─" * 50)
    print("3. GOING DEEPER")
    print("─" * 50)

    result = experience.advance(session.session_id)
    print(f"  Scene: {result['scene']['name']}")
    print(f"  Description: {result['scene']['description']}")

    # Emergence
    print("\n" + "─" * 50)
    print("4. EMERGENCE")
    print("─" * 50)

    result = experience.advance(session.session_id)
    print(f"  Scene: {result['scene']['name']}")
    print(f"  Description: {result['scene']['description']}")

    # Door selection
    print("\n" + "─" * 50)
    print("5. THE FOUR DOORS")
    print("─" * 50)

    result = experience.advance(session.session_id)
    print(f"  Scene: {result['scene']['name']}")
    print(f"  Description: {result['scene']['description']}")
    print(f"  Available choices: {result['scene']['available_choices']}")
    print(f"  Hotspots:")
    for hotspot in result['scene']['hotspots']:
        print(f"    - {hotspot['label']} at {hotspot['position']}")

    # Choose a door
    print("\n" + "─" * 50)
    print("6. CHOOSING NOIZYVOX")
    print("─" * 50)

    result = experience.advance(session.session_id, choice="enter_vox")
    print(f"  Scene: {result['scene']['name']}")
    print(f"  Description: {result['scene']['description']}")
    print(f"  Characters present: {result['scene']['characters_present']}")

    # Get session state
    print("\n" + "─" * 50)
    print("7. SESSION SUMMARY")
    print("─" * 50)

    state = experience.get_session_state(session.session_id)
    print(f"  Scenes visited: {state['journey']['scenes_visited']}")
    print(f"  Choices made: {state['journey']['choices_made']}")
    print(f"  Doors entered: {state['journey']['doors_entered']}")
    print(f"  Duration: {state['journey']['duration_seconds']:.1f} seconds")

    print("\n" + "=" * 70)
    print("This is not a website. This is an experience.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
