"""
DreamChamber Audio Engine
=========================

Spatial audio, binaural beats, and voice synthesis.

The sound of the NOIZY universe.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4
import math


class AudioLayer(Enum):
    """Audio layers for mixing."""
    MASTER = "master"
    MUSIC = "music"
    AMBIENT = "ambient"
    VOICE = "voice"
    SFX = "sfx"
    BINAURAL = "binaural"


class SpatialMode(Enum):
    """Spatial audio modes."""
    STEREO = "stereo"           # Standard stereo
    BINAURAL = "binaural"       # Headphone 3D
    SURROUND = "surround"       # 5.1/7.1
    AMBISONICS = "ambisonics"   # Full 3D sphere


@dataclass
class AudioSource:
    """A positioned audio source."""
    source_id: str = field(default_factory=lambda: str(uuid4()))

    # Audio file
    audio_file: str = ""
    audio_type: str = "sample"  # sample, stream, generated

    # Spatial
    position: tuple = (0, 0, 0)
    direction: tuple = (0, 0, -1)
    is_spatial: bool = True

    # Playback
    volume: float = 1.0
    pitch: float = 1.0
    pan: float = 0.0  # -1 to 1

    # Looping
    loop: bool = False
    loop_start: float = 0.0
    loop_end: float = -1.0  # -1 = end of file

    # Envelope
    fade_in: float = 0.0
    fade_out: float = 0.0

    # 3D settings
    distance_min: float = 1.0
    distance_max: float = 50.0
    rolloff: str = "linear"  # linear, logarithmic, exponential

    # State
    is_playing: bool = False
    current_time: float = 0.0


@dataclass
class BinauralBeat:
    """A binaural beat generator."""
    beat_id: str = field(default_factory=lambda: str(uuid4()))

    # Frequencies
    base_frequency: float = 200.0     # Hz (carrier)
    beat_frequency: float = 10.0       # Hz (difference)

    # Left = base_frequency
    # Right = base_frequency + beat_frequency
    # Brain perceives beat_frequency as the "beat"

    # Amplitude
    amplitude: float = 0.5

    # Waveform
    waveform: str = "sine"  # sine, triangle

    # State
    is_active: bool = False

    # Brain states by frequency:
    # Delta (0.5-4 Hz): Deep sleep
    # Theta (4-8 Hz): Meditation, creativity
    # Alpha (8-14 Hz): Relaxation, calm
    # Beta (14-30 Hz): Alertness, focus
    # Gamma (30-100 Hz): Higher cognition

    @classmethod
    def delta_wave(cls, amplitude: float = 0.3) -> 'BinauralBeat':
        """Create delta wave (deep relaxation)."""
        return cls(base_frequency=100, beat_frequency=2.0, amplitude=amplitude)

    @classmethod
    def theta_wave(cls, amplitude: float = 0.4) -> 'BinauralBeat':
        """Create theta wave (meditation)."""
        return cls(base_frequency=150, beat_frequency=6.0, amplitude=amplitude)

    @classmethod
    def alpha_wave(cls, amplitude: float = 0.5) -> 'BinauralBeat':
        """Create alpha wave (relaxation)."""
        return cls(base_frequency=200, beat_frequency=10.0, amplitude=amplitude)

    @classmethod
    def void_tone(cls, amplitude: float = 0.6) -> 'BinauralBeat':
        """Create the Void tone (30Hz sub-bass)."""
        return cls(base_frequency=30, beat_frequency=4.0, amplitude=amplitude)


@dataclass
class SpatialSound:
    """A sound positioned in 3D space."""
    sound_id: str = field(default_factory=lambda: str(uuid4()))

    # Source
    audio_source: AudioSource = field(default_factory=AudioSource)

    # Position
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    # Movement
    velocity: tuple = (0, 0, 0)
    path: list = field(default_factory=list)  # Waypoints for movement
    path_speed: float = 1.0

    # Occlusion
    occluded: bool = False
    occlusion_amount: float = 0.0  # 0-1

    # Doppler
    doppler_enabled: bool = True
    doppler_factor: float = 1.0

    def update_position(self, listener_position: tuple) -> dict:
        """Calculate spatial parameters relative to listener."""
        dx = self.x - listener_position[0]
        dy = self.y - listener_position[1]
        dz = self.z - listener_position[2]

        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        distance = max(0.1, distance)

        # Pan based on x position
        pan = max(-1, min(1, dx / 10))

        # Volume based on distance
        attenuation = 1 / (1 + distance * 0.1)

        # Angle for HRTF
        angle = math.atan2(dx, -dz) * 180 / math.pi

        return {
            "distance": distance,
            "pan": pan,
            "attenuation": attenuation,
            "angle": angle,
            "elevation": math.atan2(dy, distance) * 180 / math.pi
        }


class AudioEngine:
    """
    The DreamChamber audio engine.

    Manages:
    - Spatial audio sources
    - Binaural beats
    - Music/ambient layers
    - Voice playback
    - Real-time mixing
    """

    def __init__(self):
        self.sources: dict[str, AudioSource] = {}
        self.spatial_sounds: dict[str, SpatialSound] = {}
        self.binaural_beats: dict[str, BinauralBeat] = {}

        # Listener
        self.listener_position: tuple = (0, 0, 0)
        self.listener_rotation: tuple = (0, 0, 0)

        # Layer volumes
        self.layer_volumes: dict[AudioLayer, float] = {
            AudioLayer.MASTER: 1.0,
            AudioLayer.MUSIC: 0.7,
            AudioLayer.AMBIENT: 0.5,
            AudioLayer.VOICE: 1.0,
            AudioLayer.SFX: 0.8,
            AudioLayer.BINAURAL: 0.6
        }

        # Mode
        self.spatial_mode = SpatialMode.BINAURAL
        self.reverb_enabled = True
        self.reverb_decay = 2.0

    def set_listener(self, position: tuple, rotation: tuple = (0, 0, 0)):
        """Set listener position and rotation."""
        self.listener_position = position
        self.listener_rotation = rotation

    def add_source(self, source: AudioSource) -> str:
        """Add an audio source."""
        self.sources[source.source_id] = source
        return source.source_id

    def add_spatial_sound(self, sound: SpatialSound) -> str:
        """Add a spatial sound."""
        self.spatial_sounds[sound.sound_id] = sound
        self.sources[sound.audio_source.source_id] = sound.audio_source
        return sound.sound_id

    def add_binaural(self, beat: BinauralBeat) -> str:
        """Add a binaural beat."""
        self.binaural_beats[beat.beat_id] = beat
        return beat.beat_id

    def start_void_tone(self) -> str:
        """Start the signature Void tone."""
        beat = BinauralBeat.void_tone()
        beat.is_active = True
        return self.add_binaural(beat)

    def play_source(self, source_id: str):
        """Play an audio source."""
        if source_id in self.sources:
            self.sources[source_id].is_playing = True

    def stop_source(self, source_id: str):
        """Stop an audio source."""
        if source_id in self.sources:
            self.sources[source_id].is_playing = False

    def set_layer_volume(self, layer: AudioLayer, volume: float):
        """Set volume for a layer."""
        self.layer_volumes[layer] = max(0, min(1, volume))

    def update(self, delta_seconds: float) -> dict:
        """Update all audio state."""
        # Update spatial sounds
        spatial_states = {}
        for sound_id, sound in self.spatial_sounds.items():
            if sound.audio_source.is_playing:
                spatial_states[sound_id] = sound.update_position(self.listener_position)

        # Update source times
        for source in self.sources.values():
            if source.is_playing:
                source.current_time += delta_seconds

        return {
            "listener": {
                "position": self.listener_position,
                "rotation": self.listener_rotation
            },
            "active_sources": sum(1 for s in self.sources.values() if s.is_playing),
            "active_binaural": sum(1 for b in self.binaural_beats.values() if b.is_active),
            "spatial_sounds": spatial_states,
            "layer_volumes": {l.value: v for l, v in self.layer_volumes.items()}
        }

    def get_web_audio_config(self) -> dict:
        """Get configuration for Web Audio API implementation."""
        return {
            "context": {
                "sample_rate": 48000,
                "latency_hint": "interactive"
            },
            "binaural": [
                {
                    "id": b.beat_id,
                    "left_frequency": b.base_frequency,
                    "right_frequency": b.base_frequency + b.beat_frequency,
                    "amplitude": b.amplitude,
                    "waveform": b.waveform
                }
                for b in self.binaural_beats.values()
                if b.is_active
            ],
            "reverb": {
                "enabled": self.reverb_enabled,
                "decay": self.reverb_decay,
                "wet": 0.3
            },
            "compressor": {
                "threshold": -24,
                "knee": 30,
                "ratio": 12,
                "attack": 0.003,
                "release": 0.25
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the audio engine."""
    print("\n" + "=" * 70)
    print("DREAMCHAMBER AUDIO ENGINE — DEMO")
    print("Spatial audio, binaural beats, immersion")
    print("=" * 70)

    engine = AudioEngine()

    print("\n" + "─" * 50)
    print("1. STARTING THE VOID TONE")
    print("─" * 50)

    void_id = engine.start_void_tone()
    beat = engine.binaural_beats[void_id]
    print(f"  Binaural beat ID: {void_id[:8]}...")
    print(f"  Base frequency: {beat.base_frequency} Hz")
    print(f"  Beat frequency: {beat.beat_frequency} Hz")
    print(f"  Left ear hears: {beat.base_frequency} Hz")
    print(f"  Right ear hears: {beat.base_frequency + beat.beat_frequency} Hz")
    print(f"  Brain perceives: {beat.beat_frequency} Hz beat (theta wave)")

    print("\n" + "─" * 50)
    print("2. ADDING SPATIAL SOUNDS")
    print("─" * 50)

    # Add some spatial sounds
    door_vox = SpatialSound(
        audio_source=AudioSource(audio_file="door_hum_vox.wav", loop=True),
        x=-3, y=0, z=-5
    )
    door_vox.audio_source.is_playing = True
    engine.add_spatial_sound(door_vox)
    print(f"  Added: NOIZYVOX door at ({door_vox.x}, {door_vox.y}, {door_vox.z})")

    door_lab = SpatialSound(
        audio_source=AudioSource(audio_file="door_hum_lab.wav", loop=True),
        x=-1, y=0, z=-5
    )
    door_lab.audio_source.is_playing = True
    engine.add_spatial_sound(door_lab)
    print(f"  Added: NOIZYLAB door at ({door_lab.x}, {door_lab.y}, {door_lab.z})")

    print("\n" + "─" * 50)
    print("3. SPATIAL CALCULATIONS")
    print("─" * 50)

    engine.set_listener((0, 0, 0))
    print(f"  Listener at origin")

    for sound_id, sound in engine.spatial_sounds.items():
        params = sound.update_position(engine.listener_position)
        print(f"\n  Sound at ({sound.x}, {sound.y}, {sound.z}):")
        print(f"    Distance: {params['distance']:.2f}")
        print(f"    Pan: {params['pan']:.2f}")
        print(f"    Attenuation: {params['attenuation']:.2f}")
        print(f"    Angle: {params['angle']:.1f}")

    print("\n" + "─" * 50)
    print("4. WEB AUDIO CONFIG")
    print("─" * 50)

    config = engine.get_web_audio_config()
    print(f"  Sample rate: {config['context']['sample_rate']} Hz")
    print(f"  Active binaural: {len(config['binaural'])}")
    print(f"  Reverb enabled: {config['reverb']['enabled']}")

    print("\n" + "─" * 50)
    print("5. BRAINWAVE STATES")
    print("─" * 50)

    states = [
        ("Delta (0.5-4 Hz)", "Deep sleep, healing", BinauralBeat.delta_wave()),
        ("Theta (4-8 Hz)", "Meditation, creativity", BinauralBeat.theta_wave()),
        ("Alpha (8-14 Hz)", "Relaxation, calm", BinauralBeat.alpha_wave()),
        ("Void (30 Hz)", "Sub-bass immersion", BinauralBeat.void_tone())
    ]

    for name, desc, beat in states:
        print(f"  {name}")
        print(f"    {desc}")
        print(f"    Carrier: {beat.base_frequency} Hz, Beat: {beat.beat_frequency} Hz")

    print("\n" + "=" * 70)
    print("Sound is the bridge between worlds.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
