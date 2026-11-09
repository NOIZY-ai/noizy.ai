"""
The Four Doors
==============

The portals from the Void to the NOIZY universe.

Each door has its own energy, color, sound, and promise.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import math


class DoorType(Enum):
    """The four doors."""
    NOIZYVOX = "noizyvox"     # Voice Guild
    NOIZYLAB = "noizylab"     # Repair Network
    NOIZYKIDZ = "noizykidz"   # Youth Program
    NOIZYFISH = "noizyfish"   # Consent Registry


class DoorState(Enum):
    """State of a door."""
    HIDDEN = "hidden"           # Not yet visible
    MATERIALIZING = "materializing"
    IDLE = "idle"               # Visible, waiting
    HOVER = "hover"             # User attention
    OPENING = "opening"         # Being entered
    OPEN = "open"               # Fully open


@dataclass
class Door:
    """A door to one of the four NOIZY domains."""
    door_type: DoorType

    # Visual
    position: tuple = (0, 0, -5)
    rotation: float = 0.0
    scale: float = 1.0
    state: DoorState = DoorState.HIDDEN

    # Colors
    primary_color: str = "#ffffff"
    secondary_color: str = "#000000"
    glow_color: str = "#ffffff"
    glow_intensity: float = 0.5

    # Animation
    pulse_speed: float = 1.0
    pulse_amount: float = 0.1
    hover_scale: float = 1.1

    # Audio
    ambient_sound: str = ""
    hover_sound: str = "door_hover"
    open_sound: str = "door_open"

    # Content
    title: str = ""
    subtitle: str = ""
    description: str = ""

    # Destination
    destination_url: str = ""
    destination_scene: str = ""

    def __post_init__(self):
        """Initialize door properties based on type."""
        configs = {
            DoorType.NOIZYVOX: {
                "position": (-3, 0, -5),
                "primary_color": "#e94560",
                "secondary_color": "#ff6b6b",
                "glow_color": "#ff4757",
                "title": "NOIZYVOX",
                "subtitle": "The Voice Guild",
                "description": "Where human voices are sovereign.",
                "ambient_sound": "vox_hum",
                "destination_url": "https://noizyvox.ai",
                "destination_scene": "noizyvox_entry"
            },
            DoorType.NOIZYLAB: {
                "position": (-1, 0, -5),
                "primary_color": "#0f3460",
                "secondary_color": "#16213e",
                "glow_color": "#00d9ff",
                "title": "NOIZYLAB",
                "subtitle": "The Repair Network",
                "description": "Where technology serves humanity.",
                "ambient_sound": "lab_pulse",
                "destination_url": "https://noizylab.ca",
                "destination_scene": "noizylab_entry"
            },
            DoorType.NOIZYKIDZ: {
                "position": (1, 0, -5),
                "primary_color": "#533483",
                "secondary_color": "#9b59b6",
                "glow_color": "#e056fd",
                "title": "NOIZYKIDZ",
                "subtitle": "The Youth Program",
                "description": "Where young minds learn to create.",
                "ambient_sound": "kidz_melody",
                "destination_url": "https://noizykidz.org",
                "destination_scene": "noizykidz_entry"
            },
            DoorType.NOIZYFISH: {
                "position": (3, 0, -5),
                "primary_color": "#00b894",
                "secondary_color": "#00d9ff",
                "glow_color": "#00ff88",
                "title": "NOIZYFISH",
                "subtitle": "The Consent Registry",
                "description": "Where creator rights are absolute.",
                "ambient_sound": "fish_data",
                "destination_url": "https://noizyfish.io",
                "destination_scene": "noizyfish_entry"
            }
        }

        config = configs.get(self.door_type, {})
        for key, value in config.items():
            setattr(self, key, value)

    def get_render_state(self, time: float) -> dict:
        """Get current render state for the door."""
        # Pulse animation
        pulse = math.sin(time * self.pulse_speed * math.pi * 2) * self.pulse_amount

        # Scale based on state
        current_scale = self.scale
        if self.state == DoorState.HOVER:
            current_scale = self.hover_scale
        elif self.state == DoorState.OPENING:
            current_scale = self.hover_scale * 1.2

        return {
            "door_type": self.door_type.value,
            "state": self.state.value,
            "position": self.position,
            "rotation": self.rotation,
            "scale": current_scale + pulse,
            "colors": {
                "primary": self.primary_color,
                "secondary": self.secondary_color,
                "glow": self.glow_color,
                "glow_intensity": self.glow_intensity + pulse * 0.5
            },
            "content": {
                "title": self.title,
                "subtitle": self.subtitle,
                "description": self.description
            },
            "destination": {
                "url": self.destination_url,
                "scene": self.destination_scene
            }
        }


class FourDoors:
    """
    Manager for the four doors.

    Handles:
    - Materialization sequence
    - Hover interactions
    - Door selection
    - Transition to destination
    """

    def __init__(self):
        self.doors: dict[DoorType, Door] = {
            door_type: Door(door_type)
            for door_type in DoorType
        }

        self.materialization_progress = 0.0
        self.selected_door: Optional[DoorType] = None
        self.hovered_door: Optional[DoorType] = None

    def start_materialization(self):
        """Begin the door materialization sequence."""
        self.materialization_progress = 0.0
        for door in self.doors.values():
            door.state = DoorState.MATERIALIZING

    def update(self, delta_seconds: float, time: float) -> dict:
        """Update door states."""
        # Materialization
        if self.materialization_progress < 1.0:
            self.materialization_progress += delta_seconds / 4.0  # 4 second materialization
            self.materialization_progress = min(1.0, self.materialization_progress)

            # Stagger door appearances
            order = [DoorType.NOIZYFISH, DoorType.NOIZYKIDZ, DoorType.NOIZYLAB, DoorType.NOIZYVOX]
            for i, door_type in enumerate(order):
                door = self.doors[door_type]
                threshold = i * 0.2  # 0.0, 0.2, 0.4, 0.6

                if self.materialization_progress > threshold + 0.3:
                    door.state = DoorState.IDLE
                elif self.materialization_progress > threshold:
                    door.state = DoorState.MATERIALIZING

        return {
            "materialization_progress": self.materialization_progress,
            "hovered_door": self.hovered_door.value if self.hovered_door else None,
            "selected_door": self.selected_door.value if self.selected_door else None,
            "doors": {
                door_type.value: door.get_render_state(time)
                for door_type, door in self.doors.items()
            }
        }

    def set_hover(self, door_type: Optional[DoorType]):
        """Set hovered door."""
        # Clear previous hover
        if self.hovered_door:
            self.doors[self.hovered_door].state = DoorState.IDLE

        self.hovered_door = door_type

        # Set new hover
        if door_type:
            self.doors[door_type].state = DoorState.HOVER

    def select_door(self, door_type: DoorType) -> dict:
        """Select and open a door."""
        self.selected_door = door_type
        door = self.doors[door_type]
        door.state = DoorState.OPENING

        return {
            "selected": door_type.value,
            "destination_url": door.destination_url,
            "destination_scene": door.destination_scene,
            "transition": {
                "type": "door_open",
                "color": door.glow_color,
                "duration": 2.0
            }
        }

    def get_door_at_position(self, x: float, y: float) -> Optional[DoorType]:
        """Get door at screen position (for click detection)."""
        # Simplified - in real implementation, would do raycasting
        for door_type, door in self.doors.items():
            dx = x - door.position[0]
            if abs(dx) < 0.8:  # Approximate door width
                return door_type
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Four Doors."""
    print("\n" + "=" * 70)
    print("THE FOUR DOORS — DEMO")
    print("Portals to the NOIZY universe")
    print("=" * 70)

    doors = FourDoors()
    doors.start_materialization()

    print("\n  Materializing doors...")

    # Simulate materialization
    time = 0.0
    delta = 0.5
    for i in range(12):
        state = doors.update(delta, time)
        time += delta

        if i % 2 == 0:
            print(f"\n  t={time:.1f}s | Progress: {state['materialization_progress']:.1%}")
            for door_type, door_state in state['doors'].items():
                print(f"    {door_type}: {door_state['state']}")

    print("\n" + "─" * 50)
    print("  DOOR DETAILS")
    print("─" * 50)

    for door_type in DoorType:
        door = doors.doors[door_type]
        print(f"\n  {door.title}")
        print(f"    {door.subtitle}")
        print(f"    \"{door.description}\"")
        print(f"    Color: {door.primary_color}")
        print(f"    → {door.destination_url}")

    print("\n" + "─" * 50)
    print("  SELECTING NOIZYVOX")
    print("─" * 50)

    result = doors.select_door(DoorType.NOIZYVOX)
    print(f"\n  Selected: {result['selected']}")
    print(f"  Destination: {result['destination_url']}")
    print(f"  Transition: {result['transition']['type']} ({result['transition']['duration']}s)")

    print("\n" + "=" * 70)
    print("Four doors. Four paths. One NOIZY universe.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
