"""
The Void
========

The entry point to the DreamChamber.
Darkness. A 30Hz tone. The dissolution of the ordinary.

"You arrive in darkness.
 A low hum begins to vibrate in your chest.
 You are nowhere and everywhere.
 And then... four doors begin to materialize."
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4
import math


class VoidState(Enum):
    """States of the Void experience."""
    APPROACHING = "approaching"     # Transitioning in
    DARKNESS = "darkness"           # Pure black
    TONE_RISING = "tone_rising"     # 30Hz beginning
    RESONANCE = "resonance"         # Full 30Hz immersion
    PARTICLES = "particles"         # Void particles appearing
    EMERGENCE = "emergence"         # Doors materializing
    DISSOLVING = "dissolving"       # Void fading


@dataclass
class VoidParticle:
    """A particle in the Void."""
    particle_id: str = field(default_factory=lambda: str(uuid4())[:8])
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    size: float = 1.0
    opacity: float = 1.0
    color: str = "#1a1a1a"
    lifetime_seconds: float = 5.0
    age: float = 0.0


class TheVoid:
    """
    The Void experience manager.

    Handles the entry sequence:
    1. Darkness descends
    2. 30Hz tone begins
    3. Particles emerge
    4. Four doors materialize
    """

    # Audio settings
    BASE_FREQUENCY = 30.0  # Hz - the sacred tone
    HARMONIC_RATIOS = [1.0, 2.0, 3.0, 4.0]  # Harmonic series
    FADE_IN_SECONDS = 5.0
    RESONANCE_DURATION = 8.0

    # Visual settings
    PARTICLE_COUNT = 500
    DARKNESS_DURATION = 3.0
    EMERGENCE_DURATION = 4.0

    def __init__(self):
        self.state = VoidState.APPROACHING
        self.particles: list[VoidParticle] = []
        self.tone_amplitude = 0.0
        self.elapsed_seconds = 0.0
        self.door_visibility = 0.0  # 0-1

        # State durations
        self.state_durations = {
            VoidState.APPROACHING: 2.0,
            VoidState.DARKNESS: 3.0,
            VoidState.TONE_RISING: 5.0,
            VoidState.RESONANCE: 8.0,
            VoidState.PARTICLES: 4.0,
            VoidState.EMERGENCE: 4.0,
            VoidState.DISSOLVING: 2.0
        }

        self.state_start_time = 0.0

    def start(self):
        """Start the Void experience."""
        self.state = VoidState.APPROACHING
        self.elapsed_seconds = 0.0
        self.state_start_time = 0.0
        self.particles = []
        self.tone_amplitude = 0.0
        self.door_visibility = 0.0

    def update(self, delta_seconds: float) -> dict:
        """Update the Void state."""
        self.elapsed_seconds += delta_seconds
        time_in_state = self.elapsed_seconds - self.state_start_time

        # Check state transitions
        duration = self.state_durations.get(self.state, 5.0)
        if time_in_state >= duration:
            self._advance_state()
            time_in_state = 0.0

        # Update based on current state
        if self.state == VoidState.APPROACHING:
            self._update_approaching(time_in_state)
        elif self.state == VoidState.DARKNESS:
            self._update_darkness(time_in_state)
        elif self.state == VoidState.TONE_RISING:
            self._update_tone_rising(time_in_state)
        elif self.state == VoidState.RESONANCE:
            self._update_resonance(time_in_state)
        elif self.state == VoidState.PARTICLES:
            self._update_particles(time_in_state, delta_seconds)
        elif self.state == VoidState.EMERGENCE:
            self._update_emergence(time_in_state)
        elif self.state == VoidState.DISSOLVING:
            self._update_dissolving(time_in_state)

        return self.get_state()

    def _advance_state(self):
        """Move to the next state."""
        state_order = [
            VoidState.APPROACHING,
            VoidState.DARKNESS,
            VoidState.TONE_RISING,
            VoidState.RESONANCE,
            VoidState.PARTICLES,
            VoidState.EMERGENCE,
            VoidState.DISSOLVING
        ]

        current_index = state_order.index(self.state)
        if current_index < len(state_order) - 1:
            self.state = state_order[current_index + 1]
            self.state_start_time = self.elapsed_seconds

    def _update_approaching(self, time_in_state: float):
        """Update during approach phase."""
        # Screen fading to black
        pass

    def _update_darkness(self, time_in_state: float):
        """Update during pure darkness."""
        # Complete darkness, silence
        self.tone_amplitude = 0.0

    def _update_tone_rising(self, time_in_state: float):
        """Update as the 30Hz tone rises."""
        duration = self.state_durations[VoidState.TONE_RISING]
        progress = min(1.0, time_in_state / duration)

        # Ease-in curve for tone
        self.tone_amplitude = self._ease_in_cubic(progress)

    def _update_resonance(self, time_in_state: float):
        """Update during full resonance."""
        # Full 30Hz, subtle pulsing
        duration = self.state_durations[VoidState.RESONANCE]
        progress = time_in_state / duration

        # Subtle amplitude modulation
        pulse = 0.1 * math.sin(progress * math.pi * 4)
        self.tone_amplitude = 0.9 + pulse

    def _update_particles(self, time_in_state: float, delta: float):
        """Update particle system."""
        duration = self.state_durations[VoidState.PARTICLES]
        progress = min(1.0, time_in_state / duration)

        # Spawn particles
        target_count = int(self.PARTICLE_COUNT * progress)
        while len(self.particles) < target_count:
            self._spawn_particle()

        # Update existing particles
        for p in self.particles:
            p.age += delta
            p.x += p.vx * delta
            p.y += p.vy * delta
            p.z += p.vz * delta

            # Fade based on age
            if p.age > p.lifetime_seconds * 0.8:
                p.opacity = max(0, 1 - (p.age - p.lifetime_seconds * 0.8) / (p.lifetime_seconds * 0.2))

        # Remove dead particles
        self.particles = [p for p in self.particles if p.age < p.lifetime_seconds]

    def _update_emergence(self, time_in_state: float):
        """Update as doors emerge."""
        duration = self.state_durations[VoidState.EMERGENCE]
        progress = min(1.0, time_in_state / duration)

        # Doors become visible
        self.door_visibility = self._ease_out_cubic(progress)

        # Tone shifts slightly
        self.tone_amplitude = 0.8 - (progress * 0.3)

    def _update_dissolving(self, time_in_state: float):
        """Update as Void dissolves."""
        duration = self.state_durations[VoidState.DISSOLVING]
        progress = min(1.0, time_in_state / duration)

        self.door_visibility = 1.0
        self.tone_amplitude = max(0, 0.5 - progress * 0.5)

    def _spawn_particle(self):
        """Spawn a new void particle."""
        import random

        particle = VoidParticle(
            x=random.uniform(-50, 50),
            y=random.uniform(-50, 50),
            z=random.uniform(-100, -10),
            vx=random.uniform(-0.5, 0.5),
            vy=random.uniform(-0.5, 0.5),
            vz=random.uniform(0.5, 2.0),
            size=random.uniform(0.5, 2.0),
            opacity=random.uniform(0.3, 0.8),
            color=random.choice(["#1a1a1a", "#2a2a2a", "#0a0a0a", "#1a1a2e"]),
            lifetime_seconds=random.uniform(3.0, 8.0)
        )
        self.particles.append(particle)

    def _ease_in_cubic(self, t: float) -> float:
        """Cubic ease-in."""
        return t * t * t

    def _ease_out_cubic(self, t: float) -> float:
        """Cubic ease-out."""
        return 1 - pow(1 - t, 3)

    def get_state(self) -> dict:
        """Get current Void state."""
        return {
            "state": self.state.value,
            "elapsed_seconds": self.elapsed_seconds,
            "tone": {
                "frequency": self.BASE_FREQUENCY,
                "amplitude": self.tone_amplitude,
                "harmonics": [
                    {"frequency": self.BASE_FREQUENCY * r, "amplitude": self.tone_amplitude / (i + 1)}
                    for i, r in enumerate(self.HARMONIC_RATIOS)
                ]
            },
            "particles": {
                "count": len(self.particles),
                "positions": [
                    {"x": p.x, "y": p.y, "z": p.z, "size": p.size, "opacity": p.opacity, "color": p.color}
                    for p in self.particles[:100]  # Limit for serialization
                ]
            },
            "door_visibility": self.door_visibility,
            "is_complete": self.state == VoidState.DISSOLVING and self.door_visibility >= 1.0
        }

    def get_audio_config(self) -> dict:
        """Get audio configuration for the Void."""
        return {
            "binaural": {
                "enabled": True,
                "base_frequency": self.BASE_FREQUENCY,
                "beat_frequency": 4.0,  # Theta waves
                "amplitude": self.tone_amplitude
            },
            "ambient": {
                "track": "void_drone",
                "volume": 0.3 * self.tone_amplitude
            },
            "reverb": {
                "enabled": True,
                "decay": 5.0,
                "wet": 0.8
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# Demo
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Demonstrate the Void."""
    print("\n" + "=" * 70)
    print("THE VOID — DEMO")
    print("Darkness. 30Hz. Emergence.")
    print("=" * 70)

    void = TheVoid()
    void.start()

    print("\n  Simulating Void experience...")
    print("  (In browser, this would be immersive WebGL + Web Audio)")

    # Simulate time passing
    delta = 0.5  # 500ms steps
    for i in range(60):  # 30 seconds
        state = void.update(delta)

        if i % 4 == 0:  # Print every 2 seconds
            print(f"\n  t={state['elapsed_seconds']:.1f}s | State: {state['state']}")
            print(f"    Tone amplitude: {state['tone']['amplitude']:.2f}")
            print(f"    Particles: {state['particles']['count']}")
            print(f"    Door visibility: {state['door_visibility']:.2f}")

            if state['is_complete']:
                print("\n    ✓ VOID COMPLETE — Doors are visible")
                break

    print("\n" + "=" * 70)
    print("You are nowhere and everywhere. Four doors await.")
    print("=" * 70)


if __name__ == "__main__":
    demo()
