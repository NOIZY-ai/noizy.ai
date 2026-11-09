"""
NOIZY DreamChamber
==================

The immersive portal to the NOIZY universe.

"You land in the Void.
 You experience the 30Hz tone.
 You see the four doors materialize.
 You FEEL something before you understand anything."

Components:
- The Void: Entry experience (30Hz tone, darkness, emergence)
- The Four Doors: NOIZYVOX, NOIZYLAB, NOIZYKIDZ, NOIZYFISH
- Characters: Detective Morrison, Marcus, Commander Ash
- Scenes: Interactive narrative moments
- Audio Engine: Spatial audio, binaural beats, voice synthesis

Architecture:
- WebGL/Three.js for 3D rendering
- Web Audio API for spatial sound
- WebXR for VR (MetaQuest 2)
- FastAPI backend for state/auth
- WebSocket for real-time events

This is not a website. This is an experience.
"""

__version__ = "1.0.0"
__author__ = "NOIZYLAB"

from .experience import DreamChamberExperience, Scene, Transition
from .void import TheVoid, VoidState
from .doors import Door, DoorType, FourDoors
from .characters import Character, CharacterType, DialogueLine
from .audio import AudioEngine, SpatialSound, BinauralBeat
from .narrative import NarrativeEngine, StoryBeat, Choice

__all__ = [
    "DreamChamberExperience",
    "Scene",
    "Transition",
    "TheVoid",
    "VoidState",
    "Door",
    "DoorType",
    "FourDoors",
    "Character",
    "CharacterType",
    "DialogueLine",
    "AudioEngine",
    "SpatialSound",
    "BinauralBeat",
    "NarrativeEngine",
    "StoryBeat",
    "Choice"
]
