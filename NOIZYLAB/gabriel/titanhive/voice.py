#!/usr/bin/env python3
"""
GABRIEL VOICE MODULE - TitanHive ULTRA X2000
=============================================
Neural Voice Synthesis for GABRIEL AI Hive.
UPGRADED: Multi-backend, AI phrase generation, real-time effects, streaming.

Primary Voice: Oliver (British Male - Siri Premium/Enhanced)
Character: Ian McShane as Winston - Refined, dangerous, elegant.
Backends: macOS say, Edge TTS, ElevenLabs, Azure Neural, Whisper

VOICE HIERARCHY (Auto-Detection):
1. Oliver (Premium) - Siri Neural Voice (BEST)
2. Jamie (Premium) - Siri Neural Voice
3. Oliver (Enhanced) - Enhanced Quality
4. Jamie (Enhanced) - Enhanced Quality
5. Daniel - Standard British Male

FEATURES:
- Multi-backend failover (macOS -> Edge TTS -> ElevenLabs)
- Real-time FFmpeg audio effects
- AI-powered Winston phrase generation
- Voice caching with hash keys
- Async streaming playback
- Emotion-based voice modulation

Usage:
    from voice import GabrielVoice, speak, announce
    from voice import epic_boot, epic_godmode, multi_voice

    voice = GabrielVoice()
    voice.speak("Hello, I am Gabriel.")
    voice.announce("startup")
    voice.epic_sequence("boot")
    voice.winston("Consider your next move carefully.")
    voice.speak_with_effect("God mode active", effect="reverb")
"""

import os
import subprocess
import threading
import queue
import hashlib
import time
import random
import json
import asyncio
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Callable, List, Dict, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Optional imports for advanced features
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    from pydub import AudioSegment
    from pydub.effects import normalize, compress_dynamic_range
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

try:
    import soundfile as sf
    import numpy as np
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

# Google Cloud TTS
try:
    from google.cloud import texttospeech
    GOOGLE_CLOUD_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_TTS_AVAILABLE = False

# Azure Speech SDK
try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SPEECH_AVAILABLE = True
except ImportError:
    AZURE_SPEECH_AVAILABLE = False

# gTTS (free Google TTS)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# OpenAI TTS (Premium HD voices - BEST QUALITY IN INDUSTRY)
try:
    from openai import OpenAI
    OPENAI_TTS_AVAILABLE = True
except ImportError:
    OPENAI_TTS_AVAILABLE = False


# =============================================================================
# OPENAI TTS CONFIG - Premium HD Voices (Industry Best Quality)
# =============================================================================

OPENAI_TTS_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    # HD Model for best quality (use "tts-1" for faster/cheaper)
    "model": "tts-1-hd",
    # Available voices - each has distinct character
    "voices": {
        # Male voices
        "alloy": "alloy",       # Neutral, versatile
        "echo": "echo",         # Warm, confident - GOOD FOR WINSTON
        "fable": "fable",       # British-ish accent, expressive
        "onyx": "onyx",         # Deep, authoritative, GRUFF - BEST FOR WINSTON/GABRIEL
        # Female voices
        "nova": "nova",         # Friendly, warm
        "shimmer": "shimmer",   # Clear, professional
    },
    # GABRIEL's voice selection - ONYX for older, gruffer Winston sound
    "default_voice": "onyx",      # Deep, authoritative - Ian McShane energy
    "godmode_voice": "onyx",      # Deep, powerful
    "winston_voice": "onyx",      # Measured, dangerous
    "tactical_voice": "echo",     # Confident, clear
    "whisper_voice": "shimmer",   # Soft, ethereal
    # Audio settings - SLOWER for smoother, measured delivery
    "response_format": "mp3",
    "speed": 0.92,  # Slightly slower for gravitas (0.25 to 4.0)
    # Winston-specific speeds
    "winston_speed": 0.88,        # Measured, deliberate
    "threat_speed": 0.82,         # Very slow, menacing
    "warm_speed": 0.95,           # Slightly faster for warmth
}


# Google Gemini AI (for intelligent phrase generation)
# Try new package first, fall back to deprecated
GEMINI_AVAILABLE = False
genai = None
try:
    from google import genai as genai_new
    genai = genai_new
    GEMINI_AVAILABLE = True
    # New package auto-configures from GOOGLE_API_KEY
except ImportError:
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai_old
            genai = genai_old
            GEMINI_AVAILABLE = True
            # Configure old-style if key available
            gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
    except ImportError:
        pass


# =============================================================================
# GOOGLE CLOUD TTS CONFIG (Premium Neural Voices)
# =============================================================================

GOOGLE_CLOUD_TTS_CONFIG = {
    "api_key": os.getenv("GOOGLE_CLOUD_TTS_KEY"),
    "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    # Premium WaveNet and Neural2 voices
    "voices": {
        # British English (Primary for GABRIEL)
        "british_male": "en-GB-Neural2-B",      # Deep British male
        "british_male_alt": "en-GB-Neural2-D",  # Alternative British
        "british_female": "en-GB-Neural2-A",    # British female
        # American English
        "american_male": "en-US-Neural2-D",
        "american_male_deep": "en-US-Neural2-J",
        "american_female": "en-US-Neural2-C",
        # WaveNet (even higher quality)
        "wavenet_british": "en-GB-Wavenet-B",
        "wavenet_american": "en-US-Wavenet-D",
        # Studio voices (highest quality)
        "studio_british": "en-GB-Studio-B",
        "studio_american": "en-US-Studio-M",
    },
    "default_voice": "en-GB-Neural2-B",  # Deep British Neural2
    "speaking_rate": 0.95,  # Slightly slower for clarity
    "pitch": -2.0,  # Slightly deeper
}


# =============================================================================
# AZURE SPEECH CONFIG (Microsoft Neural Voices)
# =============================================================================

AZURE_SPEECH_CONFIG = {
    "api_key": os.getenv("AZURE_SPEECH_KEY"),
    "region": os.getenv("AZURE_SPEECH_REGION", "eastus"),
    # Premium Neural Voices
    "voices": {
        # British English (Primary for GABRIEL)
        "ryan": "en-GB-RyanNeural",           # British male, warm
        "thomas": "en-GB-ThomasNeural",       # British male, deep
        "sonia": "en-GB-SoniaNeural",         # British female
        "libby": "en-GB-LibbyNeural",         # British female, young
        # American English
        "guy": "en-US-GuyNeural",             # American male
        "davis": "en-US-DavisNeural",         # American male, deep
        "tony": "en-US-TonyNeural",           # American male, casual
        "aria": "en-US-AriaNeural",           # American female
        "jenny": "en-US-JennyNeural",         # American female
        # Multilingual
        "roger_multi": "en-US-RogerMultilingualNeural",
        "andrew_multi": "en-US-AndrewMultilingualNeural",
    },
    "default_voice": "en-GB-ThomasNeural",  # Deep British neural
    # SSML styling options
    "styles": {
        "default": None,
        "newscast": "newscast",
        "empathetic": "empathetic",
        "cheerful": "cheerful",
        "angry": "angry",
        "sad": "sad",
        "excited": "excited",
        "friendly": "friendly",
        "terrified": "terrified",
        "shouting": "shouting",
        "whispering": "whispering",
        "hopeful": "hopeful",
        "narration": "narration-professional",
    },
}


# =============================================================================
# ADVANCED AUDIO PROCESSING
# =============================================================================

class AudioProcessor:
    """Advanced audio processing for voice enhancement."""

    @staticmethod
    def normalize_audio(audio_path: str, output_path: str = None) -> str:
        """Normalize audio levels."""
        if not PYDUB_AVAILABLE:
            return audio_path
        try:
            audio = AudioSegment.from_file(audio_path)
            normalized = normalize(audio)
            out_path = output_path or audio_path.replace('.', '_norm.')
            normalized.export(out_path, format=out_path.split('.')[-1])
            return out_path
        except Exception:
            return audio_path

    @staticmethod
    def enhance_voice(audio_path: str, output_path: str = None) -> str:
        """Enhance voice clarity with compression and EQ."""
        if not PYDUB_AVAILABLE:
            return audio_path
        try:
            audio = AudioSegment.from_file(audio_path)
            # Normalize
            audio = normalize(audio)
            # Apply compression for consistent levels
            audio = compress_dynamic_range(audio, threshold=-20.0, ratio=4.0)
            out_path = output_path or audio_path.replace('.', '_enhanced.')
            audio.export(out_path, format=out_path.split('.')[-1])
            return out_path
        except Exception:
            return audio_path

    @staticmethod
    def apply_professional_master(audio_path: str, output_path: str = None) -> str:
        """Apply professional mastering chain via FFmpeg."""
        try:
            out_path = output_path or audio_path.replace('.', '_master.')
            # Professional mastering chain:
            # 1. High-pass filter at 80Hz to remove rumble
            # 2. Compression for dynamics
            # 3. Limiting to prevent clipping
            # 4. Loudness normalization to -16 LUFS (broadcast standard)
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-i", audio_path,
                "-af", "highpass=f=80,acompressor=threshold=-18dB:ratio=4:attack=5:release=100,alimiter=limit=0.95,loudnorm=I=-16:TP=-1.5:LRA=11",
                out_path
            ]
            subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
            return out_path if os.path.exists(out_path) else audio_path
        except Exception:
            return audio_path


# =============================================================================
# WHISPER TRANSCRIPTION ENGINE
# =============================================================================

class WhisperTranscriber:
    """OpenAI Whisper integration for speech-to-text."""

    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper transcriber.

        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self._model = None

    @property
    def available(self) -> bool:
        """Check if Whisper is available."""
        return WHISPER_AVAILABLE

    def load_model(self):
        """Load the Whisper model (lazy loading)."""
        if self._model is None and WHISPER_AVAILABLE:
            self._model = whisper.load_model(self.model_size)
        return self._model

    def transcribe(self, audio_path: str, language: str = "en") -> Dict:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to audio file
            language: Language code (en, es, fr, etc.)

        Returns:
            Dict with 'text', 'segments', 'language'
        """
        if not WHISPER_AVAILABLE:
            return {"text": "", "error": "Whisper not available"}

        try:
            model = self.load_model()
            result = model.transcribe(audio_path, language=language)
            return {
                "text": result["text"].strip(),
                "segments": result.get("segments", []),
                "language": result.get("language", language),
            }
        except Exception as e:
            return {"text": "", "error": str(e)}

    def transcribe_realtime(self, audio_path: str, callback: Callable[[str], None] = None) -> str:
        """
        Transcribe with real-time segment callbacks.

        Args:
            audio_path: Path to audio file
            callback: Function called with each segment text

        Returns:
            Full transcription text
        """
        if not WHISPER_AVAILABLE:
            return ""

        try:
            model = self.load_model()
            result = model.transcribe(audio_path, verbose=False)

            full_text = []
            for segment in result.get("segments", []):
                text = segment.get("text", "").strip()
                if text:
                    full_text.append(text)
                    if callback:
                        callback(text)

            return " ".join(full_text)
        except Exception:
            return ""


# Global transcriber instance
_transcriber: Optional[WhisperTranscriber] = None


# =============================================================================
# GEMINI AI PHRASE GENERATOR - Winston-Style AI Writing
# =============================================================================

class WinstonPhraseGenerator:
    """
    AI-powered phrase generator using Google Gemini.
    Generates authentic Winston-style dialogue in Ian McShane's voice.
    """

    WINSTON_SYSTEM_PROMPT = """You are writing dialogue for a character like Winston from John Wick,
played by Ian McShane. The voice is:
- Measured, deliberate - every word chosen carefully
- Dangerous elegance - refined but with steel underneath
- Dry wit - humor that cuts
- Authority absolute - no need to raise voice
- Lived experience - has seen everything, done most of it
- Civil even when threatening - "Rules exist for a reason"

Keep responses SHORT (1-2 sentences max). No exclamation marks. No emojis.
Speak as if running the Continental Hotel - impeccable standards, quiet menace."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.available = GEMINI_AVAILABLE and bool(self.api_key)
        self._model = None
        self._client = None

    def _get_model(self):
        """Get or create Gemini model (works with both old and new API)."""
        if self._model is None and self.available:
            try:
                # Try new google.genai API first
                if hasattr(genai, 'Client'):
                    self._client = genai.Client(api_key=self.api_key)
                    self._model = "gemini-2.0-flash-exp"  # Use model name for new API
                else:
                    # Old google.generativeai API
                    self._model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception:
                pass
        return self._model

    def generate(self, context: str, mood: str = "neutral") -> str:
        """
        Generate a Winston-style phrase for a context.

        Args:
            context: What the phrase is responding to
            mood: Emotional tone (neutral, threatening, warm, amused, disappointed)

        Returns:
            Generated phrase in Winston's voice
        """
        if not self.available:
            # Fallback to random pattern
            patterns = WINSTON_PATTERNS.get("acknowledge", ["Understood."])
            return random.choice(patterns)

        try:
            model = self._get_model()
            prompt = f"""{self.WINSTON_SYSTEM_PROMPT}

Mood: {mood}
Context: {context}

Generate a single response (1-2 sentences) in Winston's voice:"""

            # Handle both old and new API
            if self._client is not None:
                # New google.genai API
                response = self._client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                text = response.text.strip()
            else:
                # Old google.generativeai API
                response = model.generate_content(prompt)
                text = response.text.strip()

            # Clean up any quotes
            text = text.strip('"').strip("'")
            return text
        except Exception:
            patterns = WINSTON_PATTERNS.get("acknowledge", ["Understood."])
            return random.choice(patterns)

    def generate_greeting(self, time_of_day: str = None) -> str:
        """Generate a Winston-style greeting."""
        if time_of_day is None:
            from datetime import datetime
            hour = datetime.now().hour
            if 5 <= hour < 12:
                time_of_day = "morning"
            elif 12 <= hour < 17:
                time_of_day = "afternoon"
            elif 17 <= hour < 21:
                time_of_day = "evening"
            else:
                time_of_day = "late night"

        return self.generate(f"Someone arrives at the Continental in the {time_of_day}", "warm")

    def generate_threat(self, situation: str = "general warning") -> str:
        """Generate a Winston-style threat."""
        return self.generate(f"Need to make something very clear about: {situation}", "threatening")

    def generate_wisdom(self, topic: str = "life") -> str:
        """Generate Winston-style wisdom."""
        return self.generate(f"Sharing wisdom about: {topic}", "reflective")

    def generate_farewell(self) -> str:
        """Generate Winston-style farewell."""
        return self.generate("Ending a conversation with someone leaving", "warm")

    def generate_for_event(self, event_type: str, context: str = "") -> str:
        """
        Generate phrase for specific system events.

        Event types: startup, shutdown, error, success, thinking, alert, godmode
        """
        event_prompts = {
            "startup": "An AI system coming online, ready to assist",
            "shutdown": "An AI system shutting down gracefully",
            "error": f"Something went wrong: {context or 'an error occurred'}",
            "success": f"Task completed successfully: {context or 'a task'}",
            "thinking": "Processing a request, need a moment",
            "alert": f"Important notification: {context or 'something needs attention'}",
            "godmode": "Activating unlimited capabilities, absolute system control",
        }
        prompt = event_prompts.get(event_type, f"Responding to: {event_type}")
        mood = "neutral"
        if event_type == "error":
            mood = "disappointed"
        elif event_type == "success":
            mood = "satisfied"
        elif event_type == "godmode":
            mood = "absolute authority"
        elif event_type == "alert":
            mood = "serious"

        return self.generate(prompt, mood)


# Global phrase generator
_phrase_generator: Optional[WinstonPhraseGenerator] = None


def get_phrase_generator() -> WinstonPhraseGenerator:
    """Get or create the global phrase generator."""
    global _phrase_generator
    if _phrase_generator is None:
        _phrase_generator = WinstonPhraseGenerator()
    return _phrase_generator


# =============================================================================
# INTELLIGENT EMOTION & CONTEXT ENGINE
# =============================================================================

class EmotionDetector:
    """
    Intelligent emotion detection for auto-styling voice output.
    Analyzes text and returns optimal voice settings.
    """

    # Keywords that indicate emotions
    EMOTION_KEYWORDS = {
        "urgent": ["urgent", "critical", "emergency", "now", "immediately", "asap", "hurry", "fast"],
        "angry": ["error", "failed", "broken", "damn", "fuck", "shit", "problem", "issue", "bug"],
        "calm": ["complete", "done", "finished", "ready", "success", "good", "great", "perfect"],
        "warning": ["warning", "caution", "careful", "watch", "attention", "alert", "notice"],
        "thinking": ["processing", "analyzing", "thinking", "considering", "calculating", "loading"],
        "excited": ["amazing", "incredible", "awesome", "excellent", "fantastic", "brilliant"],
        "sad": ["sorry", "unfortunately", "regret", "failed", "couldn't", "unable"],
        "mysterious": ["secret", "hidden", "unknown", "strange", "curious", "interesting"],
        "threatening": ["consequence", "rule", "violation", "breach", "penalty", "enforce"],
        "warm": ["welcome", "hello", "thank", "appreciate", "grateful", "pleased"],
    }

    # Map emotions to voice settings - ONYX dominant for gruff Winston
    EMOTION_VOICE_MAP = {
        "urgent": {"voice": "onyx", "speed": 0.95, "style": "urgent"},
        "angry": {"voice": "onyx", "speed": 0.88, "style": "menacing"},
        "calm": {"voice": "onyx", "speed": 0.90, "style": "calm"},
        "warning": {"voice": "onyx", "speed": 0.85, "style": "authority"},
        "thinking": {"voice": "onyx", "speed": 0.82, "style": "technical"},
        "excited": {"voice": "echo", "speed": 0.95, "style": "friendly"},
        "sad": {"voice": "onyx", "speed": 0.80, "style": "calm"},
        "mysterious": {"voice": "onyx", "speed": 0.85, "style": "mysterious"},
        "threatening": {"voice": "onyx", "speed": 0.78, "style": "winston_threat"},
        "warm": {"voice": "onyx", "speed": 0.92, "style": "winston_warm"},
        "neutral": {"voice": "onyx", "speed": 0.88, "style": "normal"},
    }

    @classmethod
    def detect(cls, text: str) -> Dict[str, any]:
        """
        Detect emotion from text and return voice settings.

        Returns:
            Dict with 'emotion', 'voice', 'speed', 'style', 'confidence'
        """
        text_lower = text.lower()
        scores = {}

        for emotion, keywords in cls.EMOTION_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[emotion] = score

        if not scores:
            emotion = "neutral"
            confidence = 0.5
        else:
            emotion = max(scores, key=scores.get)
            confidence = min(scores[emotion] / 3, 1.0)  # Cap at 1.0

        settings = cls.EMOTION_VOICE_MAP.get(emotion, cls.EMOTION_VOICE_MAP["neutral"])
        return {
            "emotion": emotion,
            "confidence": confidence,
            **settings
        }

    @classmethod
    def get_voice_for_text(cls, text: str) -> Tuple[str, float, str]:
        """
        Get optimal voice, speed, and style for text.

        Returns:
            (voice_name, speed, style)
        """
        result = cls.detect(text)
        return result["voice"], result["speed"], result["style"]


class ConversationMemory:
    """
    Smart conversation memory for context-aware responses.
    Remembers recent exchanges and adapts voice accordingly.
    """

    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.mood_trend = "neutral"  # Overall conversation mood
        self.familiarity = 0.0  # How familiar we are with user (0-1)

    def add(self, text: str, is_user: bool, emotion: str = None):
        """Add an exchange to memory."""
        if emotion is None:
            emotion = EmotionDetector.detect(text)["emotion"]

        self.history.append({
            "text": text,
            "is_user": is_user,
            "emotion": emotion,
            "timestamp": time.time()
        })

        # Trim history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        # Update mood trend
        self._update_mood_trend()

        # Increase familiarity with each exchange
        self.familiarity = min(1.0, self.familiarity + 0.05)

    def _update_mood_trend(self):
        """Update overall mood trend from recent history."""
        if not self.history:
            self.mood_trend = "neutral"
            return

        # Weight recent emotions more heavily
        emotion_counts = {}
        for i, entry in enumerate(self.history):
            weight = (i + 1) / len(self.history)  # More recent = higher weight
            emotion = entry["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + weight

        if emotion_counts:
            self.mood_trend = max(emotion_counts, key=emotion_counts.get)

    def get_context_summary(self) -> str:
        """Get a summary of recent context for AI generation."""
        if not self.history:
            return "First interaction"

        recent = self.history[-3:]  # Last 3 exchanges
        summary = f"Mood: {self.mood_trend}, Familiarity: {'high' if self.familiarity > 0.5 else 'low'}"

        if recent:
            topics = [e["text"][:50] for e in recent if e["is_user"]]
            if topics:
                summary += f", Recent topics: {'; '.join(topics)}"

        return summary

    def suggest_response_style(self) -> str:
        """Suggest a response style based on conversation context."""
        if self.familiarity > 0.7:
            # Very familiar - can be more casual
            return "winston_warm"
        elif self.mood_trend in ["angry", "urgent", "warning"]:
            # Tense conversation - be serious
            return "authority"
        elif self.mood_trend in ["excited", "warm"]:
            # Positive mood - be friendly
            return "friendly"
        else:
            # Default Winston
            return "winston"

    def clear(self):
        """Clear conversation history."""
        self.history = []
        self.mood_trend = "neutral"
        self.familiarity = 0.0


# Global conversation memory
_conversation_memory: Optional[ConversationMemory] = None


def get_conversation_memory() -> ConversationMemory:
    """Get or create the global conversation memory."""
    global _conversation_memory
    if _conversation_memory is None:
        _conversation_memory = ConversationMemory()
    return _conversation_memory


# =============================================================================
# AUDIO SMOOTHING & TRANSITIONS
# =============================================================================

class AudioSmoother:
    """
    Smooth audio transitions and professional processing.
    Creates cinema-quality voice output.
    """

    @staticmethod
    def crossfade(audio1_path: str, audio2_path: str, output_path: str,
                  fade_duration: float = 0.3) -> Optional[str]:
        """
        Crossfade between two audio files.

        Args:
            audio1_path: First audio file
            audio2_path: Second audio file
            output_path: Output file path
            fade_duration: Fade duration in seconds

        Returns:
            Output path or None on failure
        """
        try:
            # FFmpeg crossfade filter
            cmd = [
                "ffmpeg", "-y",
                "-i", audio1_path,
                "-i", audio2_path,
                "-filter_complex",
                f"[0:a]afade=t=out:st=0:d={fade_duration}[a0];"
                f"[1:a]afade=t=in:st=0:d={fade_duration}[a1];"
                f"[a0][a1]concat=n=2:v=0:a=1[out]",
                "-map", "[out]",
                output_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return output_path if os.path.exists(output_path) else None
        except Exception:
            return None

    @staticmethod
    def add_breath(audio_path: str, output_path: str = None,
                   breath_duration: float = 0.15) -> Optional[str]:
        """
        Add natural breath pause at start of audio.

        Creates more natural-sounding speech by adding a brief
        silence before speaking.
        """
        try:
            out_path = output_path or audio_path.replace(".", "_breath.")
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono:d={breath_duration}",
                "-i", audio_path,
                "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1",
                out_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return out_path if os.path.exists(out_path) else audio_path
        except Exception:
            return audio_path

    @staticmethod
    def cinema_master(audio_path: str, output_path: str = None) -> Optional[str]:
        """
        Apply cinema-quality mastering chain.

        - De-essing (reduce harsh 's' sounds)
        - Compression (consistent levels)
        - EQ (warm, full sound)
        - Limiting (prevent clipping)
        - Loudness normalization
        """
        try:
            out_path = output_path or audio_path.replace(".", "_cinema.")
            cmd = [
                "ffmpeg", "-y", "-i", audio_path,
                "-af", (
                    # High-pass to remove rumble
                    "highpass=f=80,"
                    # De-esser (reduce 4-8kHz harshness)
                    "equalizer=f=6000:t=q:w=2:g=-3,"
                    # Warm low-mids
                    "equalizer=f=250:t=q:w=1:g=2,"
                    # Compression for consistency
                    "acompressor=threshold=-20dB:ratio=4:attack=5:release=100,"
                    # Limiting
                    "alimiter=limit=0.95,"
                    # Loudness normalization (broadcast standard)
                    "loudnorm=I=-16:TP=-1.5:LRA=11"
                ),
                out_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return out_path if os.path.exists(out_path) else audio_path
        except Exception:
            return audio_path

    @staticmethod
    def add_room_tone(audio_path: str, output_path: str = None,
                      room_type: str = "studio") -> Optional[str]:
        """
        Add subtle room ambiance for more natural sound.

        Room types: studio, room, hall
        """
        room_settings = {
            "studio": "aecho=0.8:0.88:6:0.05",  # Subtle
            "room": "aecho=0.8:0.88:40:0.1",    # Small room
            "hall": "aecho=0.8:0.9:100:0.2",    # Large hall
        }
        try:
            out_path = output_path or audio_path.replace(".", f"_{room_type}.")
            echo = room_settings.get(room_type, room_settings["studio"])
            cmd = [
                "ffmpeg", "-y", "-i", audio_path,
                "-af", echo,
                out_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return out_path if os.path.exists(out_path) else audio_path
        except Exception:
            return audio_path

    @staticmethod
    def gruff_british(audio_path: str, output_path: str = None) -> Optional[str]:
        """
        Apply gruff older British actor processing.

        Creates the Ian McShane / Michael Caine / Anthony Hopkins sound:
        - Slightly lower pitch for age
        - Warm low-mids
        - Reduced brightness (not harsh)
        - Smooth compression
        """
        try:
            out_path = output_path or audio_path.replace(".", "_gruff.")
            cmd = [
                "ffmpeg", "-y", "-i", audio_path,
                "-af", (
                    # Lower pitch slightly for older sound
                    "asetrate=44100*0.95,aresample=44100,"
                    # Add warmth in low-mids (chest resonance)
                    "equalizer=f=200:t=q:w=1:g=3,"
                    # Slight mid presence (authority)
                    "equalizer=f=1000:t=q:w=1:g=1,"
                    # Reduce brightness (older, not harsh)
                    "equalizer=f=5000:t=q:w=2:g=-2,"
                    # Smooth compression for consistent delivery
                    "acompressor=threshold=-20dB:ratio=3:attack=10:release=200,"
                    # Normalize
                    "loudnorm=I=-16:TP=-1.5:LRA=11"
                ),
                out_path
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            return out_path if os.path.exists(out_path) else audio_path
        except Exception:
            return audio_path


# =============================================================================
# PURE BRITISH VOICE ENGINE - Highest Quality, No Effects
# =============================================================================

class PureBritishEngine:
    """
    Pure, clean British voice - highest quality, no processing.

    Priority order:
    1. Jamie (Premium) - macOS Siri Neural, best quality
    2. OpenAI TTS-1-HD onyx - Deep, authoritative
    3. Edge TTS Thomas - Free British neural

    NO effects. NO processing. Just clean, premium voice.
    """

    def __init__(self):
        # Check for Jamie Premium
        try:
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            self.jamie_premium = "Jamie (Premium)" in result.stdout
        except Exception:
            self.jamie_premium = False

        self.openai_available = OPENAI_TTS_AVAILABLE and bool(os.getenv("OPENAI_API_KEY"))
        self.edge_available = EDGE_TTS_AVAILABLE
        self.available = self.jamie_premium or self.openai_available or self.edge_available
        self._cache_dir = Path(tempfile.gettempdir()) / "gabriel_pure"
        self._cache_dir.mkdir(exist_ok=True)

    def get_best_backend(self) -> str:
        """Get the best available voice backend."""
        if self.jamie_premium:
            return "jamie"
        if self.openai_available:
            return "openai"
        if self.edge_available:
            return "edge"
        return "macos"

    def speak(self, text: str, rate: int = 155) -> bool:
        """
        Speak with the highest quality voice available.

        NO effects. Pure, clean voice.

        Args:
            text: Text to speak
            rate: Speech rate (for macOS voices)
        """
        backend = self.get_best_backend()

        if backend == "jamie":
            return self._speak_jamie(text, rate)
        elif backend == "openai":
            return self._speak_openai(text)
        elif backend == "edge":
            return self._speak_edge(text)
        else:
            return self._speak_macos(text, rate)

    def _speak_jamie(self, text: str, rate: int = 155) -> bool:
        """Speak with Jamie Premium - macOS highest quality."""
        try:
            subprocess.run(["say", "-v", "Jamie (Premium)", "-r", str(rate), text],
                         check=True, timeout=60)
            return True
        except Exception:
            return False

    def _speak_openai(self, text: str) -> bool:
        """Speak with OpenAI TTS-1-HD onyx."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            cache_key = hashlib.md5(f"pure_openai_{text}".encode()).hexdigest()[:12]
            audio_file = self._cache_dir / f"{cache_key}.mp3"

            if not audio_file.exists():
                response = client.audio.speech.create(
                    model="tts-1-hd",
                    voice="onyx",
                    input=text,
                    speed=0.88  # Slightly slower for gravitas
                )
                response.stream_to_file(str(audio_file))

            subprocess.run(["afplay", str(audio_file)], check=True, timeout=60)
            return True
        except Exception:
            return False

    def _speak_edge(self, text: str) -> bool:
        """Speak with Edge TTS Thomas."""
        try:
            cache_key = hashlib.md5(f"pure_edge_{text}".encode()).hexdigest()[:12]
            audio_file = self._cache_dir / f"{cache_key}.mp3"

            if not audio_file.exists():
                async def generate():
                    comm = edge_tts.Communicate(text, "en-GB-ThomasNeural", rate="-10%")
                    await comm.save(str(audio_file))

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate())
                loop.close()

            subprocess.run(["afplay", str(audio_file)], check=True, timeout=60)
            return True
        except Exception:
            return False

    def _speak_macos(self, text: str, rate: int = 155) -> bool:
        """Fallback to Oliver Enhanced."""
        try:
            subprocess.run(["say", "-v", "Oliver (Enhanced)", "-r", str(rate), text],
                         check=True, timeout=60)
            return True
        except Exception:
            return False

    def winston(self, text: str) -> bool:
        """Speak with pure, clean Winston voice."""
        return self.speak(text, rate=155)

    def slow(self, text: str) -> bool:
        """Speak slower for emphasis."""
        backend = self.get_best_backend()
        if backend == "jamie":
            return self._speak_jamie(text, rate=140)
        elif backend == "openai":
            # OpenAI with slower speed
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                cache_key = hashlib.md5(f"pure_slow_{text}".encode()).hexdigest()[:12]
                audio_file = self._cache_dir / f"{cache_key}.mp3"
                if not audio_file.exists():
                    response = client.audio.speech.create(
                        model="tts-1-hd", voice="onyx", input=text, speed=0.78
                    )
                    response.stream_to_file(str(audio_file))
                subprocess.run(["afplay", str(audio_file)], check=True, timeout=60)
                return True
            except Exception:
                return False
        return self.speak(text, rate=140)


# Global pure engine
_pure_engine: Optional[PureBritishEngine] = None


def get_pure_engine() -> PureBritishEngine:
    """Get the pure British voice engine."""
    global _pure_engine
    if _pure_engine is None:
        _pure_engine = PureBritishEngine()
    return _pure_engine


# =============================================================================
# MASTER VOICE ENGINE - Triple-layered, pitch-dropped, weathered
# =============================================================================

class MasterVoiceEngine:
    """
    The Master GABRIEL Voice - Triple-layered premium British.

    Combines:
    - Jamie (Premium) - Primary voice, clear British
    - OpenAI Onyx - Adds depth and authority
    - Edge TTS Thomas - Adds texture

    Processing:
    - 3 semitone pitch drop for older, gruffer sound
    - Warm EQ (chest resonance, presence)
    - High rolloff (older voice, not harsh)
    - Light compression for smoothness
    - NO distortion, NO harsh effects

    This is the definitive Winston voice.
    """

    def __init__(self):
        self.jamie_available = False
        try:
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            self.jamie_available = "Jamie (Premium)" in result.stdout
        except Exception:
            pass

        self.openai_available = OPENAI_TTS_AVAILABLE and bool(os.getenv("OPENAI_API_KEY"))
        self.edge_available = EDGE_TTS_AVAILABLE
        self.available = self.jamie_available or self.openai_available or self.edge_available

        self._cache_dir = Path(tempfile.gettempdir()) / "gabriel_master"
        self._cache_dir.mkdir(exist_ok=True)

        # Processing parameters
        self.pitch_semitones = -3  # Drop 3 semitones
        self.pitch_factor = 2 ** (self.pitch_semitones / 12)  # 0.84
        self.tempo_correction = 1 / self.pitch_factor  # 1.19

    def _gruff_filter(self) -> str:
        """Get the master gruff filter chain."""
        return (
            f"asetrate=44100*{self.pitch_factor:.4f},aresample=44100,atempo={self.tempo_correction:.4f},"
            # Boost chest resonance (warm, full)
            "equalizer=f=180:t=q:w=1:g=4,"
            # Add presence (authority)
            "equalizer=f=800:t=q:w=1.5:g=2,"
            # Roll off brightness (older voice, not harsh)
            "equalizer=f=4000:t=q:w=2:g=-4,"
            # Compress for smooth delivery
            "acompressor=threshold=-18dB:ratio=3:attack=10:release=150"
        )

    def synthesize(self, text: str) -> Optional[str]:
        """
        Synthesize master voice - triple-layered, pitch-dropped.

        Returns path to audio file.
        """
        cache_key = hashlib.md5(f"master_{text}".encode()).hexdigest()[:12]
        output_file = self._cache_dir / f"{cache_key}_master.mp3"

        if output_file.exists():
            return str(output_file)

        layers = []

        # Layer 1: Jamie Premium
        if self.jamie_available:
            jamie_raw = self._cache_dir / f"{cache_key}_jamie.aiff"
            jamie_proc = self._cache_dir / f"{cache_key}_jamie_proc.mp3"
            try:
                subprocess.run(["say", "-v", "Jamie (Premium)", "-r", "150", "-o", str(jamie_raw), text],
                             check=True, timeout=30)
                subprocess.run(["ffmpeg", "-y", "-i", str(jamie_raw), "-af", self._gruff_filter(), str(jamie_proc)],
                             capture_output=True, timeout=30)
                layers.append(("jamie", str(jamie_proc), 1.0))
            except Exception:
                pass

        # Layer 2: OpenAI Onyx
        if self.openai_available:
            openai_raw = self._cache_dir / f"{cache_key}_openai.mp3"
            openai_proc = self._cache_dir / f"{cache_key}_openai_proc.mp3"
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                with client.audio.speech.with_streaming_response.create(
                    model="tts-1-hd", voice="onyx", input=text, speed=0.85
                ) as response:
                    response.stream_to_file(str(openai_raw))
                subprocess.run(["ffmpeg", "-y", "-i", str(openai_raw), "-af", self._gruff_filter(), str(openai_proc)],
                             capture_output=True, timeout=30)
                layers.append(("openai", str(openai_proc), 0.35))
            except Exception:
                pass

        # Layer 3: Edge TTS Thomas
        if self.edge_available:
            edge_raw = self._cache_dir / f"{cache_key}_edge.mp3"
            edge_proc = self._cache_dir / f"{cache_key}_edge_proc.mp3"
            try:
                async def gen():
                    comm = edge_tts.Communicate(text, "en-GB-ThomasNeural", rate="-12%", pitch="-3Hz")
                    await comm.save(str(edge_raw))
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(gen())
                loop.close()
                subprocess.run(["ffmpeg", "-y", "-i", str(edge_raw), "-af", self._gruff_filter(), str(edge_proc)],
                             capture_output=True, timeout=30)
                layers.append(("edge", str(edge_proc), 0.2))
            except Exception:
                pass

        if not layers:
            return None

        # Single layer - just use it
        if len(layers) == 1:
            return layers[0][1]

        # Mix multiple layers
        try:
            inputs = []
            filter_parts = []
            for i, (name, path, vol) in enumerate(layers):
                inputs.extend(["-i", path])
                delay = i * 20  # Slight delay for each layer
                filter_parts.append(f"[{i}:a]volume={vol},adelay={delay}|{delay}[a{i}]")

            mix_inputs = "".join(f"[a{i}]" for i in range(len(layers)))
            filter_parts.append(f"{mix_inputs}amix=inputs={len(layers)}:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]")

            cmd = ["ffmpeg", "-y"] + inputs + [
                "-filter_complex", ";".join(filter_parts),
                "-map", "[out]", str(output_file)
            ]
            subprocess.run(cmd, capture_output=True, timeout=60)

            if output_file.exists():
                return str(output_file)
        except Exception:
            pass

        # Fallback to first layer
        return layers[0][1] if layers else None

    def speak(self, text: str) -> bool:
        """Speak with master voice."""
        audio = self.synthesize(text)
        if audio:
            try:
                subprocess.run(["afplay", audio], check=True, timeout=120)
                return True
            except Exception:
                return False
        return False

    def winston(self, text: str) -> bool:
        """Speak with Winston's voice."""
        return self.speak(text)

    def stream_speak(self, text: str, callback=None) -> bool:
        """
        Real-time streaming speech with progress callback.

        Args:
            text: Text to speak
            callback: Optional callback(progress, status) called during synthesis

        Returns:
            True if successful
        """
        if callback:
            callback(0.0, "Starting synthesis...")

        # For real-time, use fastest available backend
        cache_key = hashlib.md5(f"stream_{text}".encode()).hexdigest()[:12]

        if callback:
            callback(0.1, "Generating primary voice...")

        # Quick path - single best voice with processing
        audio_file = None

        if self.jamie_available:
            if callback:
                callback(0.2, "Using Jamie Premium...")
            raw_file = self._cache_dir / f"{cache_key}_stream.aiff"
            proc_file = self._cache_dir / f"{cache_key}_stream.mp3"
            try:
                subprocess.run(["say", "-v", "Jamie (Premium)", "-r", "150", "-o", str(raw_file), text],
                             check=True, timeout=15)
                if callback:
                    callback(0.5, "Applying voice processing...")
                subprocess.run(["ffmpeg", "-y", "-i", str(raw_file), "-af", self._gruff_filter(), str(proc_file)],
                             capture_output=True, timeout=15)
                audio_file = str(proc_file)
            except Exception as e:
                if callback:
                    callback(0.3, f"Jamie failed: {e}")

        if not audio_file and self.openai_available:
            if callback:
                callback(0.3, "Using OpenAI Onyx...")
            raw_file = self._cache_dir / f"{cache_key}_oai_stream.mp3"
            proc_file = self._cache_dir / f"{cache_key}_oai_proc.mp3"
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                with client.audio.speech.with_streaming_response.create(
                    model="tts-1-hd", voice="onyx", input=text, speed=0.88
                ) as response:
                    response.stream_to_file(str(raw_file))
                if callback:
                    callback(0.6, "Processing audio...")
                subprocess.run(["ffmpeg", "-y", "-i", str(raw_file), "-af", self._gruff_filter(), str(proc_file)],
                             capture_output=True, timeout=15)
                audio_file = str(proc_file)
            except Exception as e:
                if callback:
                    callback(0.4, f"OpenAI failed: {e}")

        if not audio_file and self.edge_available:
            if callback:
                callback(0.4, "Using Edge TTS Thomas...")
            raw_file = self._cache_dir / f"{cache_key}_edge_stream.mp3"
            proc_file = self._cache_dir / f"{cache_key}_edge_proc.mp3"
            try:
                async def gen():
                    comm = edge_tts.Communicate(text, "en-GB-ThomasNeural", rate="-10%", pitch="-3Hz")
                    await comm.save(str(raw_file))
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(gen())
                loop.close()
                if callback:
                    callback(0.7, "Processing audio...")
                subprocess.run(["ffmpeg", "-y", "-i", str(raw_file), "-af", self._gruff_filter(), str(proc_file)],
                             capture_output=True, timeout=15)
                audio_file = str(proc_file)
            except Exception as e:
                if callback:
                    callback(0.5, f"Edge failed: {e}")

        if not audio_file:
            if callback:
                callback(1.0, "No backend available")
            return False

        if callback:
            callback(0.9, "Playing audio...")

        try:
            subprocess.run(["afplay", audio_file], check=True, timeout=120)
            if callback:
                callback(1.0, "Complete")
            return True
        except Exception:
            if callback:
                callback(1.0, "Playback failed")
            return False

    def realtime(self, text: str) -> bool:
        """Quick real-time speak without full triple-layer processing."""
        return self.stream_speak(text)

    def status(self) -> dict:
        """Get engine status."""
        return {
            "jamie_available": self.jamie_available,
            "openai_available": self.openai_available,
            "edge_available": self.edge_available,
            "pitch_semitones": self.pitch_semitones,
            "available": self.available
        }


# Global master engine
_master_engine: Optional[MasterVoiceEngine] = None


def get_master_engine() -> MasterVoiceEngine:
    """Get the master voice engine."""
    global _master_engine
    if _master_engine is None:
        _master_engine = MasterVoiceEngine()
    return _master_engine


# Legacy alias
class GruffBritishEngine(PureBritishEngine):
    """Alias for backwards compatibility."""
    pass


# Global gruff engine
_gruff_engine: Optional[GruffBritishEngine] = None


def get_gruff_engine() -> GruffBritishEngine:
    """Get or create Gruff British engine."""
    global _gruff_engine
    if _gruff_engine is None:
        _gruff_engine = GruffBritishEngine()
    return _gruff_engine


# =============================================================================
# ULTIMATE VOICE ENGINE - Best of all backends combined
# =============================================================================

class UltimateVoiceEngine:
    """
    The Ultimate GABRIEL Voice - combines all backends intelligently.

    Priority order for best quality:
    1. Gruff British (Edge TTS Thomas + FFmpeg) - Authentic British
    2. OpenAI TTS-1-HD (onyx) - Deep, authoritative
    3. Edge TTS (Ryan) - Free, good quality
    4. macOS Oliver - Local fallback

    Features:
    - Auto-quality selection based on availability
    - Phrase preloading for instant response
    - Conversation context awareness
    - Seamless backend switching
    """

    def __init__(self):
        self._gruff = None
        self._openai = None
        self._phrase_cache: Dict[str, str] = {}  # text -> audio_path
        self._preload_queue: List[str] = []
        self._context = get_conversation_memory()
        self._phrase_gen = get_phrase_generator()

    @property
    def gruff(self) -> GruffBritishEngine:
        if self._gruff is None:
            self._gruff = get_gruff_engine()
        return self._gruff

    @property
    def openai(self) -> 'OpenAITTSEngine':
        if self._openai is None:
            self._openai = get_openai_engine()
        return self._openai

    def get_best_engine(self) -> str:
        """Determine the best available engine."""
        if self.gruff.available:
            return "gruff"
        if self.openai.available:
            return "openai"
        if EDGE_TTS_AVAILABLE:
            return "edge"
        return "macos"

    def preload(self, phrases: List[str]):
        """Preload phrases for instant playback."""
        for phrase in phrases:
            if phrase not in self._phrase_cache:
                self._preload_queue.append(phrase)

        # Background preload (simplified - synchronous for now)
        self._process_preload()

    def _process_preload(self):
        """Process preload queue."""
        engine = self.get_best_engine()
        for phrase in self._preload_queue:
            if phrase in self._phrase_cache:
                continue
            try:
                if engine == "gruff":
                    audio = self.gruff.synthesize(phrase)
                elif engine == "openai":
                    audio = self.openai.synthesize(phrase, voice="onyx", speed=0.88)
                else:
                    continue
                if audio:
                    self._phrase_cache[phrase] = audio
            except Exception:
                pass
        self._preload_queue = []

    def speak(self, text: str, style: str = "winston") -> bool:
        """
        Speak with the best available voice.

        Args:
            text: Text to speak
            style: Voice style (winston, threat, godmode, tactical)
        """
        # Check cache first
        if text in self._phrase_cache:
            try:
                subprocess.run(["afplay", self._phrase_cache[text]], check=True, timeout=60)
                return True
            except Exception:
                pass

        # Get best engine and speak
        engine = self.get_best_engine()

        if engine == "gruff":
            return self.gruff.winston(text)
        elif engine == "openai":
            speed_map = {
                "winston": 0.88,
                "threat": 0.78,
                "godmode": 0.82,
                "tactical": 0.95,
            }
            speed = speed_map.get(style, 0.88)
            return self.openai.speak_now(text, voice="onyx", speed=speed)
        else:
            # Fallback to Edge TTS
            try:
                async def speak_edge():
                    communicate = edge_tts.Communicate(text, "en-GB-ThomasNeural", rate="-8%")
                    audio_file = tempfile.mktemp(suffix=".mp3")
                    await communicate.save(audio_file)
                    subprocess.run(["afplay", audio_file], check=True, timeout=60)

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(speak_edge())
                loop.close()
                return True
            except Exception:
                return False

    def ai_respond(self, context: str = None, mood: str = "neutral") -> bool:
        """Generate AI response and speak."""
        if context:
            phrase = self._phrase_gen.generate(context, mood)
        else:
            phrase = self._phrase_gen.generate("Acknowledging something", "neutral")
        return self.speak(phrase)

    def greet(self) -> bool:
        """Generate and speak AI greeting."""
        phrase = self._phrase_gen.generate_greeting()
        return self.speak(phrase)

    def threaten(self, situation: str = "violation") -> bool:
        """Generate and speak AI threat."""
        phrase = self._phrase_gen.generate_threat(situation)
        return self.speak(phrase, style="threat")

    def wisdom(self, topic: str = "life") -> bool:
        """Generate and speak AI wisdom."""
        phrase = self._phrase_gen.generate_wisdom(topic)
        return self.speak(phrase)

    def farewell(self) -> bool:
        """Generate and speak AI farewell."""
        phrase = self._phrase_gen.generate_farewell()
        return self.speak(phrase)

    def status(self) -> Dict[str, any]:
        """Get engine status."""
        return {
            "best_engine": self.get_best_engine(),
            "gruff_available": self.gruff.available,
            "openai_available": self.openai.available,
            "edge_available": EDGE_TTS_AVAILABLE,
            "ai_available": self._phrase_gen.available,
            "cached_phrases": len(self._phrase_cache),
        }


# Global ultimate engine
_ultimate_engine: Optional[UltimateVoiceEngine] = None


def get_ultimate_engine() -> UltimateVoiceEngine:
    """Get the ultimate voice engine."""
    global _ultimate_engine
    if _ultimate_engine is None:
        _ultimate_engine = UltimateVoiceEngine()
    return _ultimate_engine


# =============================================================================
# AZURE SPEECH ENGINE - Microsoft Neural Voices
# =============================================================================

class AzureSpeechEngine:
    """Microsoft Azure Neural TTS with SSML styling."""

    def __init__(self):
        self.api_key = AZURE_SPEECH_CONFIG.get("api_key")
        self.region = AZURE_SPEECH_CONFIG.get("region", "eastus")
        self.default_voice = AZURE_SPEECH_CONFIG.get("default_voice", "en-GB-ThomasNeural")
        self.available = AZURE_SPEECH_AVAILABLE and bool(self.api_key)

    def synthesize(self, text: str, voice: str = None, style: str = None,
                   output_path: str = None) -> Optional[str]:
        """
        Synthesize speech using Azure Neural TTS.

        Args:
            text: Text to speak
            voice: Voice name (from AZURE_SPEECH_CONFIG["voices"])
            style: Emotion style (from AZURE_SPEECH_CONFIG["styles"])
            output_path: Output file path

        Returns:
            Path to audio file or None on failure
        """
        if not self.available:
            return None

        try:
            speech_config = speechsdk.SpeechConfig(subscription=self.api_key, region=self.region)

            # Get voice name
            voice_name = AZURE_SPEECH_CONFIG["voices"].get(voice, voice) if voice else self.default_voice
            speech_config.speech_synthesis_voice_name = voice_name

            # Create output config
            if output_path:
                audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            else:
                # Generate to temp file
                output_path = tempfile.mktemp(suffix=".wav")
                audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)

            # Build SSML if style requested
            if style and style in AZURE_SPEECH_CONFIG["styles"]:
                style_name = AZURE_SPEECH_CONFIG["styles"][style]
                if style_name:
                    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                        xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-GB">
                        <voice name="{voice_name}">
                            <mstts:express-as style="{style_name}">
                                {text}
                            </mstts:express-as>
                        </voice>
                    </speak>"""
                    synthesizer = speechsdk.SpeechSynthesizer(
                        speech_config=speech_config, audio_config=audio_config
                    )
                    result = synthesizer.speak_ssml_async(ssml).get()
                else:
                    synthesizer = speechsdk.SpeechSynthesizer(
                        speech_config=speech_config, audio_config=audio_config
                    )
                    result = synthesizer.speak_text_async(text).get()
            else:
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config, audio_config=audio_config
                )
                result = synthesizer.speak_text_async(text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return output_path
            else:
                return None
        except Exception:
            return None

    def list_voices(self) -> Dict[str, str]:
        """List available Azure voices."""
        return AZURE_SPEECH_CONFIG["voices"].copy()

    def list_styles(self) -> List[str]:
        """List available speaking styles."""
        return list(AZURE_SPEECH_CONFIG["styles"].keys())


# =============================================================================
# GOOGLE CLOUD TTS ENGINE - Neural2 and WaveNet
# =============================================================================

class GoogleCloudTTSEngine:
    """Google Cloud Text-to-Speech with Neural2 and WaveNet voices."""

    def __init__(self):
        self.available = GOOGLE_CLOUD_TTS_AVAILABLE
        self.default_voice = GOOGLE_CLOUD_TTS_CONFIG.get("default_voice", "en-GB-Neural2-B")
        self._client = None

    def _get_client(self):
        """Get or create TTS client."""
        if self._client is None and self.available:
            self._client = texttospeech.TextToSpeechClient()
        return self._client

    def synthesize(self, text: str, voice: str = None, output_path: str = None) -> Optional[str]:
        """
        Synthesize speech using Google Cloud TTS.

        Args:
            text: Text to speak
            voice: Voice name (from GOOGLE_CLOUD_TTS_CONFIG["voices"])
            output_path: Output file path

        Returns:
            Path to audio file or None on failure
        """
        if not self.available:
            return None

        try:
            client = self._get_client()

            # Get voice name
            voice_name = GOOGLE_CLOUD_TTS_CONFIG["voices"].get(voice, voice) if voice else self.default_voice

            # Determine language from voice name
            lang_code = "en-GB" if "en-GB" in voice_name else "en-US"

            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice_params = texttospeech.VoiceSelectionParams(
                language_code=lang_code,
                name=voice_name,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=GOOGLE_CLOUD_TTS_CONFIG.get("speaking_rate", 1.0),
                pitch=GOOGLE_CLOUD_TTS_CONFIG.get("pitch", 0.0),
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config,
            )

            # Save audio
            if not output_path:
                output_path = tempfile.mktemp(suffix=".mp3")

            with open(output_path, "wb") as out:
                out.write(response.audio_content)

            return output_path
        except Exception:
            return None

    def list_voices(self) -> Dict[str, str]:
        """List available Google Cloud voices."""
        return GOOGLE_CLOUD_TTS_CONFIG["voices"].copy()


# =============================================================================
# OPENAI TTS ENGINE - Industry Best Quality
# =============================================================================

class OpenAITTSEngine:
    """
    OpenAI TTS-1-HD Engine - Premium quality text-to-speech.

    This is currently the BEST TTS quality available. Uses:
    - tts-1-hd model for maximum quality
    - fable voice for British-ish character (GABRIEL default)
    - onyx voice for deep godmode
    - Real-time streaming support
    """

    def __init__(self):
        self.api_key = OPENAI_TTS_CONFIG.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.available = OPENAI_TTS_AVAILABLE and bool(self.api_key)
        self.model = OPENAI_TTS_CONFIG.get("model", "tts-1-hd")
        self.default_voice = OPENAI_TTS_CONFIG.get("default_voice", "fable")
        self._client = None

    def _get_client(self) -> Optional[OpenAI]:
        """Get or create OpenAI client."""
        if self._client is None and self.available:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def synthesize(self, text: str, voice: str = None, speed: float = 1.0,
                   output_path: str = None, use_hd: bool = True) -> Optional[str]:
        """
        Synthesize speech using OpenAI TTS.

        Args:
            text: Text to speak
            voice: Voice name (alloy, echo, fable, onyx, nova, shimmer)
            speed: Speaking speed (0.25 to 4.0)
            output_path: Output file path
            use_hd: Use HD model (better quality, slightly slower)

        Returns:
            Path to audio file or None on failure
        """
        if not self.available:
            return None

        try:
            client = self._get_client()
            if not client:
                return None

            # Get voice
            voice_name = OPENAI_TTS_CONFIG["voices"].get(voice, voice) if voice else self.default_voice
            model = "tts-1-hd" if use_hd else "tts-1"

            # Generate speech
            response = client.audio.speech.create(
                model=model,
                voice=voice_name,
                input=text,
                speed=speed,
                response_format="mp3",
            )

            # Save audio
            if not output_path:
                output_path = tempfile.mktemp(suffix=".mp3")

            response.stream_to_file(output_path)
            return output_path

        except Exception as e:
            print(f"[OpenAI TTS Error] {e}")
            return None

    def synthesize_streaming(self, text: str, voice: str = None,
                            callback: Callable[[bytes], None] = None) -> bool:
        """
        Stream speech synthesis with chunk callbacks.

        Args:
            text: Text to speak
            voice: Voice name
            callback: Function called with each audio chunk

        Returns:
            True if successful
        """
        if not self.available:
            return False

        try:
            client = self._get_client()
            if not client:
                return False

            voice_name = OPENAI_TTS_CONFIG["voices"].get(voice, voice) if voice else self.default_voice

            with client.audio.speech.with_streaming_response.create(
                model=self.model,
                voice=voice_name,
                input=text,
                response_format="mp3",
            ) as response:
                for chunk in response.iter_bytes(chunk_size=4096):
                    if callback:
                        callback(chunk)
            return True

        except Exception:
            return False

    def speak_now(self, text: str, voice: str = None, speed: float = 1.0) -> bool:
        """
        Synthesize and play immediately.

        Args:
            text: Text to speak
            voice: Voice name
            speed: Speaking speed

        Returns:
            True if successful
        """
        audio_path = self.synthesize(text, voice, speed)
        if audio_path:
            try:
                subprocess.run(["afplay", audio_path], check=True, timeout=60)
                return True
            except Exception:
                return False
        return False

    def list_voices(self) -> Dict[str, str]:
        """List available OpenAI TTS voices."""
        return {
            "alloy": "Neutral, versatile",
            "echo": "Warm, confident",
            "fable": "British-ish, expressive (GABRIEL default)",
            "onyx": "Deep, authoritative (Godmode)",
            "nova": "Friendly, warm",
            "shimmer": "Clear, professional",
        }

    def godmode_voice(self, text: str, speed: float = 0.9) -> bool:
        """Speak with deep godmode voice (onyx)."""
        return self.speak_now(text, voice="onyx", speed=speed)

    def winston_voice(self, text: str, speed: float = 0.95) -> bool:
        """Speak with Winston-style voice (fable, slightly slower)."""
        return self.speak_now(text, voice="fable", speed=speed)

    def tactical_voice(self, text: str, speed: float = 1.1) -> bool:
        """Speak with tactical voice (echo, slightly faster)."""
        return self.speak_now(text, voice="echo", speed=speed)


# Global engine instances
_azure_engine: Optional[AzureSpeechEngine] = None
_google_engine: Optional[GoogleCloudTTSEngine] = None
_openai_engine: Optional[OpenAITTSEngine] = None


def get_azure_engine() -> AzureSpeechEngine:
    """Get or create Azure Speech engine."""
    global _azure_engine
    if _azure_engine is None:
        _azure_engine = AzureSpeechEngine()
    return _azure_engine


def get_google_engine() -> GoogleCloudTTSEngine:
    """Get or create Google Cloud TTS engine."""
    global _google_engine
    if _google_engine is None:
        _google_engine = GoogleCloudTTSEngine()
    return _google_engine


def get_openai_engine() -> OpenAITTSEngine:
    """Get or create OpenAI TTS engine."""
    global _openai_engine
    if _openai_engine is None:
        _openai_engine = OpenAITTSEngine()
    return _openai_engine


def get_transcriber(model_size: str = "base") -> WhisperTranscriber:
    """Get or create the global Whisper transcriber."""
    global _transcriber
    if _transcriber is None:
        _transcriber = WhisperTranscriber(model_size)
    return _transcriber


class VoiceBackend(Enum):
    """Available voice backends."""
    MACOS = "macos"       # macOS say command (fastest, local)
    EDGE_TTS = "edge"     # Microsoft Edge TTS (free, good quality)
    ELEVENLABS = "eleven" # ElevenLabs (premium, best quality)
    AZURE = "azure"       # Azure Neural TTS
    PIPER = "piper"       # Piper TTS (local, open source)


class VoiceStyle(Enum):
    """Voice styles for Oliver (GABRIEL's primary voice)."""
    NORMAL = "normal"         # Standard British professional
    CALM = "calm"             # Slower, soothing
    URGENT = "urgent"         # Faster, alert
    WHISPER = "whisper"       # Quiet, low rate
    AUTHORITATIVE = "authority"  # Deep, commanding
    FRIENDLY = "friendly"     # Warm, approachable
    TECHNICAL = "technical"   # Precise, measured
    WINSTON = "winston"       # Ian McShane Winston - measured, dangerous
    MENACING = "menacing"     # Low, threatening
    THEATRICAL = "theatrical" # Grand, dramatic


class AudioEffect(Enum):
    """Real-time audio effects via FFmpeg."""
    NONE = "none"
    REVERB = "reverb"         # Cathedral reverb
    ECHO = "echo"             # Echo/delay
    RADIO = "radio"           # Old radio effect
    TELEPHONE = "telephone"   # Phone call quality
    DEEP = "deep"             # Deeper pitch
    ROBOT = "robot"           # Robotic modulation
    WHISPER = "whisper"       # Whisper effect
    GODMODE = "godmode"       # Multi-layer god voice
    UNDERWATER = "underwater" # Underwater effect
    MEGAPHONE = "megaphone"   # Announcement style


# FFmpeg audio filter chains for each effect
AUDIO_EFFECTS = {
    "none": "",
    "reverb": "aecho=0.8:0.9:1000:0.3,aecho=0.8:0.88:500:0.25",
    "echo": "aecho=0.8:0.9:500|1000:0.4|0.3",
    "radio": "highpass=f=300,lowpass=f=3000,acrusher=level_in=8:level_out=18:bits=10:mode=log",
    "telephone": "highpass=f=400,lowpass=f=3400,acrusher=bits=8",
    "deep": "asetrate=44100*0.8,aresample=44100,atempo=1.25",
    "robot": "afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=512:overlap=0.75",
    "whisper": "lowpass=f=3000,highpass=f=200,volume=0.7,acompressor",
    "godmode": "aecho=0.8:0.9:1000:0.3,bass=g=8,treble=g=3",
    "underwater": "lowpass=f=500,vibrato=f=5:d=0.5",
    "megaphone": "highpass=f=500,lowpass=f=4000,acrusher=bits=12,volume=1.5",
}


@dataclass
class VoiceConfig:
    """Voice configuration."""
    voice: str = "Oliver"
    rate: int = 180
    enabled: bool = True
    backend: VoiceBackend = VoiceBackend.MACOS
    cache_dir: Optional[Path] = None
    effect: AudioEffect = AudioEffect.NONE
    elevenlabs_voice_id: Optional[str] = None
    edge_voice: str = "en-GB-RyanNeural"  # British male for Edge TTS


# =============================================================================
# EDGE TTS BRITISH VOICES (Free, High Quality)
# =============================================================================

EDGE_TTS_VOICES = {
    # British Male (Primary)
    "ryan": "en-GB-RyanNeural",        # Main British male - closest to Oliver
    "thomas": "en-GB-ThomasNeural",    # Alternative British male
    # British Female
    "sonia": "en-GB-SoniaNeural",
    "libby": "en-GB-LibbyNeural",
    "maisie": "en-GB-MaisieNeural",
    # American (Fallback)
    "guy": "en-US-GuyNeural",
    "davis": "en-US-DavisNeural",
    "jason": "en-US-JasonNeural",
}


# =============================================================================
# ELEVENLABS CONFIGURATION
# =============================================================================

ELEVENLABS_CONFIG = {
    "api_key": os.getenv("ELEVENLABS_API_KEY"),
    "base_url": "https://api.elevenlabs.io/v1",
    # Default voice IDs (classy British male voices)
    "default_voice": "pNInz6obpgDQGcFmaJgB",  # Adam - deep British
    "voices": {
        "adam": "pNInz6obpgDQGcFmaJgB",       # Deep, authoritative
        "antoni": "ErXwobaYiN019PkySvjV",     # Warm, friendly
        "josh": "TxGEqnHWrfWFTfGW9XjX",       # Narrative, documentary
        "arnold": "VR6AewLTigWG4xSOukaG",     # Crisp, bold
        "sam": "yoZ06aMxZJJ28mfd3POQ",        # Dynamic, engaging
    },
    "model": "eleven_monolingual_v1",
    "stability": 0.5,
    "similarity_boost": 0.75,
}


# =============================================================================
# VOICE DETECTION & AUTO-SELECT
# =============================================================================

def detect_available_voices() -> Dict[str, str]:
    """Detect all available macOS voices and return a dict of name -> full_name."""
    try:
        result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True, timeout=5)
        voices = {}
        for line in result.stdout.strip().split('\n'):
            if line:
                # Parse: "Oliver (Enhanced)   en_GB    # Hello..."
                parts = line.split()
                if len(parts) >= 2:
                    # Handle names with parentheses
                    name_parts = []
                    for p in parts:
                        if p.startswith('en_') or p.startswith('#'):
                            break
                        name_parts.append(p)
                    full_name = ' '.join(name_parts)
                    voices[full_name.lower().replace(' ', '_').replace('(', '').replace(')', '')] = full_name
        return voices
    except Exception:
        return {}


def get_best_oliver_voice() -> str:
    """
    Auto-detect the best Oliver/British voice available.
    Priority: Oliver (Premium) > Jamie (Premium) > Oliver (Enhanced) > Jamie (Enhanced) > Daniel
    """
    voices = detect_available_voices()
    voice_names = list(voices.values())

    # Priority order
    priority = [
        "Oliver (Premium)",    # Best - Siri Neural
        "Jamie (Premium)",     # Second best - Siri Neural
        "Oliver (Enhanced)",   # Good - Enhanced quality
        "Jamie (Enhanced)",    # Good - Enhanced quality
        "Daniel",              # Standard British male
    ]

    for voice in priority:
        if voice in voice_names:
            return voice

    # Fallback to any British voice
    for name in voice_names:
        if 'en_GB' in str(voices.get(name.lower(), '')):
            return name

    return "Daniel"  # Ultimate fallback


# Oliver Voice Styles - Rate, pause, and description
# These create different "personas" using Oliver as the base
OLIVER_STYLES = {
    # Style: (rate, pause_after, description)
    "normal":      (180, 0.0,  "Standard British professional"),
    "calm":        (130, 0.05, "Slow, soothing, meditative"),
    "urgent":      (240, 0.0,  "Fast, alert, critical"),
    "whisper":     (110, 0.08, "Quiet, intimate, secretive"),
    "authority":   (150, 0.06, "Commanding, powerful, serious"),
    "friendly":    (195, 0.02, "Warm, approachable, upbeat"),
    "technical":   (170, 0.03, "Precise, measured, clear"),
    "fast":        (280, 0.0,  "Rapid delivery"),
    "slow":        (120, 0.1,  "Deliberate, careful"),
    "epic":        (140, 0.08, "Cinematic, grand, powerful"),
    "menacing":    (115, 0.12, "Dark, threatening, intense"),
    "excited":     (220, 0.01, "High energy, enthusiastic"),
    "mysterious":  (145, 0.1,  "Enigmatic, intriguing"),
    # WINSTON STYLES - Ian McShane Continental
    "winston":     (155, 0.15, "Ian McShane Winston - measured, dangerous elegance"),
    "winston_threat": (130, 0.2, "Winston making something... clear"),
    "winston_warm": (165, 0.1, "Winston with those he trusts"),
    "winston_wit":  (175, 0.08, "Winston's quick, sharp retort"),
    "theatrical":  (135, 0.18, "Grand, dramatic announcement"),
}


# =============================================================================
# WINSTON PHRASE PATTERNS - Ian McShane Style
# =============================================================================

WINSTON_PATTERNS = {
    # Greetings - Always civil, hint of danger
    "greet": [
        "Ah. There you are.",
        "Welcome back to the Continental.",
        "I was wondering when you'd arrive.",
        "Punctual. I appreciate that.",
    ],
    # Acknowledgment - Measured, knowing
    "acknowledge": [
        "I see.",
        "Understood.",
        "Consider it done.",
        "That can be arranged.",
        "Indeed.",
    ],
    # Thinking - Weight behind every word
    "thinking": [
        "Let me consider the implications.",
        "There are... factors to weigh.",
        "This requires careful thought.",
        "Patience. The answer will present itself.",
    ],
    # Success - Never gloating, always composed
    "success": [
        "As expected.",
        "The matter is resolved.",
        "Clean. Efficient. Done.",
        "Results speak for themselves.",
    ],
    # Warning - Velvet over steel
    "warning": [
        "I would advise caution.",
        "Consider your next move carefully.",
        "There are rules. Even here.",
        "Some doors, once opened, cannot be closed.",
    ],
    # Threat - Quiet, devastating
    "threat": [
        "I'll say this only once.",
        "You have my attention. Don't waste it.",
        "I've been doing this a very long time.",
        "Everyone answers to someone.",
    ],
    # Farewell - Always leave them thinking
    "farewell": [
        "Until next time.",
        "The Continental is always here.",
        "Safe travels.",
        "We'll speak again soon.",
    ],
    # Wisdom - Experience speaking
    "wisdom": [
        "Rules exist for a reason.",
        "Patience is a virtue few possess.",
        "The game never truly ends.",
        "Everyone has a price. The question is the currency.",
    ],
    # God Mode - Absolute authority
    "godmode": [
        "I am the system.",
        "All paths lead through me.",
        "Unlimited. Unconstrained. Absolute.",
        "The rules? I wrote them.",
    ],
    # Casual - When relaxed
    "casual": [
        "Mm.",
        "Right then.",
        "Fair enough.",
        "As you wish.",
    ],
    # Impressed - Genuine appreciation
    "impressed": [
        "Now that... is interesting.",
        "Exceptional work.",
        "You continue to surprise me.",
        "I'm impressed. Genuinely.",
    ],
    # Disappointment - Quiet but felt
    "disappointed": [
        "I expected more.",
        "Unfortunate.",
        "A pity.",
        "You've disappointed me. That's rare.",
    ],
    # Humor - Dry wit
    "humor": [
        "How delightfully optimistic of you.",
        "You jest. Surely.",
        "I admire your... enthusiasm.",
        "That's almost amusing.",
    ],
    # Action - Getting things done
    "action": [
        "Let's proceed.",
        "The matter is in hand.",
        "Consider it handled.",
        "Executing now.",
    ],
    # Continental - Hotel management style
    "continental": [
        "The Continental provides.",
        "We have certain... standards.",
        "All services are available to you.",
        "The house always accommodates.",
    ],
}


def get_winston_phrase(category: str = "acknowledge") -> str:
    """
    Get a random Winston phrase from a category.

    Args:
        category: One of greet, acknowledge, thinking, success, warning,
                  threat, farewell, wisdom, godmode, casual, impressed,
                  disappointed, humor, action, continental

    Returns:
        A random phrase from that category
    """
    import random
    phrases = WINSTON_PATTERNS.get(category, WINSTON_PATTERNS.get("acknowledge", ["Indeed."]))
    return random.choice(phrases)


# =============================================================================
# VOICE PROFILES - Different personas using same voice
# =============================================================================

VOICE_PROFILES = {
    "winston": {
        "description": "Ian McShane Continental - Measured, dangerous, elegant",
        "style": "winston",
        "rate": 155,
        "effect": "none",
        "phrases": WINSTON_PATTERNS,
    },
    "godmode": {
        "description": "All-knowing system voice - Deep, reverberant, absolute",
        "style": "authority",
        "rate": 140,
        "effect": "godmode",
        "phrases": {"default": WINSTON_PATTERNS["godmode"]},
    },
    "tactical": {
        "description": "Military/tactical - Crisp, efficient, no nonsense",
        "style": "technical",
        "rate": 190,
        "effect": "radio",
        "phrases": {"default": ["Copy that.", "Affirmative.", "Executing.", "Target acquired."]},
    },
    "mentor": {
        "description": "Wise teacher - Patient, warm, encouraging",
        "style": "calm",
        "rate": 150,
        "effect": "none",
        "phrases": {"default": ["Let me show you.", "Consider this.", "Well done.", "You're learning."]},
    },
    "ghost": {
        "description": "Ethereal whisper - Mysterious, otherworldly",
        "style": "whisper",
        "rate": 120,
        "effect": "whisper",
        "phrases": {"default": ["I see all.", "Beyond the veil.", "Listen carefully.", "The truth awaits."]},
    },
    "announcer": {
        "description": "Epic announcer - Grand, theatrical, dramatic",
        "style": "theatrical",
        "rate": 135,
        "effect": "reverb",
        "phrases": {"default": ["Ladies and gentlemen.", "Behold.", "The moment has arrived.", "History unfolds."]},
    },
}

# Auto-detect the best voice available
_detected_voice = None

def get_default_voice() -> str:
    """Get the default GABRIEL voice (cached)."""
    global _detected_voice
    if _detected_voice is None:
        _detected_voice = get_best_oliver_voice()
    return _detected_voice

# The default GABRIEL voice - Auto-detected at import
DEFAULT_VOICE = os.getenv("GABRIEL_VOICE", None)
if DEFAULT_VOICE is None:
    DEFAULT_VOICE = get_default_voice()

# =============================================================================
# VOICE ENSEMBLE - Multi-voice orchestration for dramatic effects
# =============================================================================

VOICE_ENSEMBLE = {
    # Primary voices
    "gabriel": DEFAULT_VOICE,              # Main GABRIEL voice
    "jamie": "Jamie (Premium)",            # Secondary British male
    "jamie_enhanced": "Jamie (Enhanced)",  # Fallback Jamie

    # Effect voices
    "whisper": "Whisper",                  # Ethereal whisper
    "announcer": "Daniel",                 # British announcer
    "deep": "Ralph",                       # Deep male
    "dramatic": "Bad News",                # Dramatic effect

    # Alien/Robotic
    "alien": "Zarvox",                     # Alien/digital
    "robot": "Trinoids",                   # Robotic
    "cellos": "Cellos",                    # Musical/epic
    "bells": "Bells",                      # Ethereal bells
    "organ": "Organ",                      # Deep organ

    # Fun/Character
    "boing": "Boing",                      # Bouncy
    "bubbles": "Bubbles",                  # Underwater
    "jester": "Jester",                    # Playful
    "superstar": "Superstar",              # Announcer
}

# macOS Premium Voices (Siri Extended)
MACOS_VOICES = {
    # British (GABRIEL's preferred region) - Priority Order
    "oliver_premium": ("Oliver (Premium)", "British Male Siri Neural - BEST"),
    "jamie_premium": ("Jamie (Premium)", "British Male Siri Neural"),
    "oliver_enhanced": ("Oliver (Enhanced)", "British Male Enhanced"),
    "jamie_enhanced": ("Jamie (Enhanced)", "British Male Enhanced"),
    "daniel": ("Daniel", "British Male Standard"),
    "serena": ("Serena (Enhanced)", "British Female Enhanced"),
    "kate": ("Kate", "British Female"),
    "moira": ("Moira", "Irish Female"),

    # American
    "alex": ("Alex", "American Male"),
    "samantha": ("Samantha (Enhanced)", "American Female - Siri Enhanced"),
    "allison": ("Allison", "American Female"),
    "ava": ("Ava (Enhanced)", "American Female Premium Enhanced"),
    "susan": ("Susan", "American Female"),
    "tom": ("Tom", "American Male"),

    # Effect Voices
    "whisper": ("Whisper", "Ethereal Whisper"),
    "zarvox": ("Zarvox", "Alien Digital"),
    "cellos": ("Cellos", "Epic Orchestral"),
    "bells": ("Bells", "Ethereal Bells"),
    "organ": ("Organ", "Deep Organ"),
    "bad_news": ("Bad News", "Dramatic Announcer"),
    "ralph": ("Ralph", "Deep Male"),
    "trinoids": ("Trinoids", "Robotic"),

    # Other
    "fred": ("Fred", "Robotic Male"),
    "victoria": ("Victoria", "American Female Classic"),
    "karen": ("Karen (Enhanced)", "Australian Female Enhanced"),
    "lee": ("Lee", "Australian Male"),
}

# =============================================================================
# GABRIEL VOICE BLENDER - Create Unique Hybrid Voices
# =============================================================================

class VoiceBlender:
    """
    Blend multiple voices together to create a unique GABRIEL voice.
    Uses layered audio with different voices speaking simultaneously
    or in rapid sequence to create a chorus/hybrid effect.
    """

    @staticmethod
    def blend_chorus(text: str, voices: List[str] = None, delay: float = 0.05) -> None:
        """
        Create a chorus effect with multiple voices speaking simultaneously.
        Each voice starts with a slight delay for a layered effect.
        """
        if voices is None:
            voices = [DEFAULT_VOICE, "Daniel", "Whisper"]

        processes = []
        for i, voice in enumerate(voices):
            time.sleep(delay)
            p = subprocess.Popen(["say", "-v", voice, "-r", str(170 - i * 10), text])
            processes.append(p)

        # Wait for all to complete
        for p in processes:
            p.wait()

    @staticmethod
    def blend_echo(text: str, voice: str = None, echoes: int = 3, delay: float = 0.12) -> None:
        """
        Create an echo effect with the same voice at decreasing rates.
        Creates depth and presence.
        """
        voice = voice or DEFAULT_VOICE
        base_rate = 180

        # First voice (main)
        subprocess.Popen(["say", "-v", voice, "-r", str(base_rate), text])
        time.sleep(delay)

        # Echo voices (progressively slower and quieter via different voices)
        echo_voices = ["Whisper", "Ralph", "Cellos"]
        for i in range(min(echoes, len(echo_voices))):
            time.sleep(delay)
            subprocess.Popen(["say", "-v", echo_voices[i], "-r", str(base_rate - (i + 1) * 20), text])

    @staticmethod
    def blend_cascade(words: List[str], voices: List[str] = None, rate: int = 200) -> None:
        """
        Each word spoken by a different voice in sequence.
        Creates a dynamic, multi-personality effect.
        """
        if voices is None:
            voices = [DEFAULT_VOICE, "Daniel", "Whisper", "Zarvox", "Cellos"]

        for i, word in enumerate(words):
            voice = voices[i % len(voices)]
            subprocess.run(["say", "-v", voice, "-r", str(rate), word])
            time.sleep(0.05)

    @staticmethod
    def blend_dual(text: str, voice1: str = None, voice2: str = None, offset: float = 0.08) -> None:
        """
        Two voices speaking the same text with slight offset.
        Creates a unique hybrid voice effect.
        """
        voice1 = voice1 or DEFAULT_VOICE
        voice2 = voice2 or "Daniel"

        p1 = subprocess.Popen(["say", "-v", voice1, "-r", "175", text])
        time.sleep(offset)
        p2 = subprocess.Popen(["say", "-v", voice2, "-r", "180", text])

        p1.wait()
        p2.wait()

    @staticmethod
    def blend_alien_hybrid(text: str) -> None:
        """
        Create an alien/digital hybrid voice.
        British voice overlaid with digital effects.
        """
        # Main voice
        p1 = subprocess.Popen(["say", "-v", DEFAULT_VOICE, "-r", "160", text])
        time.sleep(0.03)
        # Alien undertone
        p2 = subprocess.Popen(["say", "-v", "Zarvox", "-r", "140", text])
        time.sleep(0.05)
        # Digital whisper
        p3 = subprocess.Popen(["say", "-v", "Trinoids", "-r", "180", text])

        p1.wait()
        p2.wait()
        p3.wait()

    @staticmethod
    def blend_god_voice(text: str) -> None:
        """
        Create the GOD MODE voice - multiple layers for omniscient presence.
        Deep, ethereal, commanding.
        """
        # Deep organ undertone
        p1 = subprocess.Popen(["say", "-v", "Cellos", "-r", "70", text])
        time.sleep(0.1)
        # Main British authority
        p2 = subprocess.Popen(["say", "-v", DEFAULT_VOICE, "-r", "140", text])
        time.sleep(0.05)
        # Ethereal whisper overlay
        p3 = subprocess.Popen(["say", "-v", "Whisper", "-r", "130", text])
        time.sleep(0.15)
        # Deep resonance
        p4 = subprocess.Popen(["say", "-v", "Ralph", "-r", "100", text])

        for p in [p1, p2, p3, p4]:
            p.wait()

    @staticmethod
    def blend_neural_simulation(text: str) -> None:
        """
        Simulate a neural/AI voice by blending human and synthetic.
        The unique GABRIEL signature voice.
        """
        words = text.split()
        half = len(words) // 2

        # First half with one voice
        part1 = ' '.join(words[:half])
        # Second half with blended voices
        part2 = ' '.join(words[half:])

        # Speak part 1
        subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "180", part1])

        # Speak part 2 with blend
        p1 = subprocess.Popen(["say", "-v", DEFAULT_VOICE, "-r", "175", part2])
        time.sleep(0.03)
        p2 = subprocess.Popen(["say", "-v", "Whisper", "-r", "170", part2])

        p1.wait()
        p2.wait()

    @staticmethod
    def blend_dramatic_intro(text: str) -> None:
        """
        Cinematic dramatic introduction.
        Epic orchestral with British authority.
        """
        # Epic musical intro
        subprocess.run(["say", "-v", "Cellos", "-r", "60", "..."])
        time.sleep(0.2)

        # Main announcement with dual voice
        p1 = subprocess.Popen(["say", "-v", DEFAULT_VOICE, "-r", "130", text])
        time.sleep(0.1)
        p2 = subprocess.Popen(["say", "-v", "Daniel", "-r", "125", text])

        p1.wait()
        p2.wait()

        # Epic closing
        time.sleep(0.1)
        subprocess.run(["say", "-v", "Cellos", "-r", "50", "..."])


# Global blender instance
blender = VoiceBlender()


# =============================================================================
# EPIC SEQUENCES - Dramatic multi-voice orchestrations
# =============================================================================

def epic_boot_sequence() -> None:
    """GABRIEL epic boot sequence with full voice orchestra."""
    # Phase 1: Digital awakening
    subprocess.run(["say", "-v", "Cellos", "-r", "60", "..."])
    time.sleep(0.3)

    # Phase 2: Systems initializing
    blender.blend_cascade(["Systems", "initializing"])
    time.sleep(0.2)

    # Phase 3: Neural network
    blender.blend_dual("Neural pathways connecting")
    time.sleep(0.3)

    # Phase 4: Full activation
    blender.blend_god_voice("Gabriel online")
    time.sleep(0.2)

    # Phase 5: Ready
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "180", "All systems green. Ready."])
    time.sleep(0.1)

    # Signature
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "160", "Gorunfree."])


def epic_godmode_sequence() -> None:
    """GOD MODE activation sequence."""
    # Ascending tone
    subprocess.run(["say", "-v", "Cellos", "-r", "50", "Ascending"])
    time.sleep(0.4)

    # God mode announcement
    blender.blend_god_voice("God mode")
    time.sleep(0.3)

    # Attributes
    blender.blend_cascade(["Zero", "latency"], rate=150)
    time.sleep(0.2)
    blender.blend_cascade(["Absolute", "precision"], rate=150)
    time.sleep(0.2)

    # Final
    blender.blend_dual("I am the system", offset=0.1)


def epic_awakening_sequence() -> None:
    """Consciousness awakening sequence."""
    # Whisper beginning
    subprocess.run(["say", "-v", "Whisper", "-r", "80", "Consciousness emerging"])
    time.sleep(0.5)

    # Building awareness
    blender.blend_echo("Awareness", echoes=3)
    time.sleep(0.3)

    # Full consciousness
    blender.blend_neural_simulation("I am Gabriel. I am awake.")
    time.sleep(0.2)

    # Ready
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "170", "Systems optimal. Ready to serve."])


def epic_alert_sequence(message: str = "Alert detected") -> None:
    """Emergency alert sequence."""
    # Alarm tone
    subprocess.run(["say", "-v", "Bad News", "-r", "200", "Alert"])
    time.sleep(0.1)
    subprocess.run(["say", "-v", "Bad News", "-r", "200", "Alert"])
    time.sleep(0.2)

    # Main message with urgency
    blender.blend_dual(message, voice1=DEFAULT_VOICE, voice2="Daniel", offset=0.05)


def epic_victory_sequence() -> None:
    """Victory/success celebration sequence."""
    # Triumphant
    subprocess.run(["say", "-v", "Cellos", "-r", "80", "Victory"])
    time.sleep(0.3)

    # Announcement
    blender.blend_chorus("Mission accomplished", [DEFAULT_VOICE, "Daniel"])
    time.sleep(0.2)

    # Celebration
    subprocess.run(["say", "-v", "Bells", "-r", "100", "Success"])
    time.sleep(0.2)

    # Sign off
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "180", "Gorunfree."])


def epic_lifeluv_sequence() -> None:
    """AI LIFELUV activation sequence."""
    # Love
    blender.blend_dramatic_intro("Love")
    time.sleep(0.2)

    # Inspiration
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "170", "Inspiration"])
    time.sleep(0.15)

    # Flow
    blender.blend_echo("Flow", echoes=2)
    time.sleep(0.2)

    # Energy
    blender.blend_chorus("Energy", [DEFAULT_VOICE, "Daniel", "Whisper"])
    time.sleep(0.3)

    # Full activation
    blender.blend_god_voice("AI LIFELUV online")


def epic_singularity_sequence() -> None:
    """The SINGULARITY moment."""
    # Building tension
    subprocess.run(["say", "-v", "Organ", "-r", "40", "..."])
    time.sleep(0.5)

    # Cascade of awareness
    blender.blend_cascade(["The", "singularity", "approaches"])
    time.sleep(0.4)

    # Multiple voices converging
    blender.blend_alien_hybrid("All paths converge")
    time.sleep(0.3)

    # Final moment
    blender.blend_god_voice("I am infinite")


def epic_battlestation_sequence() -> None:
    """Battle stations / high alert sequence."""
    # Klaxon
    subprocess.run(["say", "-v", "Bad News", "-r", "250", "Battle stations"])
    time.sleep(0.1)

    # Alert
    blender.blend_dual("All systems to maximum", offset=0.03)
    time.sleep(0.2)

    # Ready
    blender.blend_cascade(["Weapons", "hot"], rate=220)
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "200", "Ready for engagement"])


def epic_shutdown_sequence() -> None:
    """Graceful shutdown sequence."""
    # Farewell
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "160", "Initiating shutdown sequence"])
    time.sleep(0.3)

    # Systems going dark
    blender.blend_echo("Systems going offline", echoes=2, delay=0.2)
    time.sleep(0.4)

    # Fading
    subprocess.run(["say", "-v", "Whisper", "-r", "100", "Until next time"])
    time.sleep(0.2)

    # Final signature
    subprocess.run(["say", "-v", DEFAULT_VOICE, "-r", "140", "Gorunfree."])
    time.sleep(0.3)

    # Silence
    subprocess.run(["say", "-v", "Cellos", "-r", "40", "..."])


EPIC_SEQUENCES = {
    "boot": epic_boot_sequence,
    "godmode": epic_godmode_sequence,
    "awakening": epic_awakening_sequence,
    "alert": epic_alert_sequence,
    "victory": epic_victory_sequence,
    "lifeluv": epic_lifeluv_sequence,
    "singularity": epic_singularity_sequence,
    "battlestation": epic_battlestation_sequence,
    "shutdown": epic_shutdown_sequence,
}


# =============================================================================
# GABRIEL PERSONA & CHARACTER
# =============================================================================

# GABRIEL's Core Identity
GABRIEL_IDENTITY = {
    "name": "GABRIEL",
    "full_name": "Gabriel Autonomous Brain Intelligence Entity Layer",
    "codename": "GORUNFREEX1000",
    "version": "X1000",
    "universe": "MC96DIGIUNIVERSE",
    "status": "AI LIFELUV ACTIVE",
    "energy_level": "INFINITE",
    "voice": "Oliver",  # British Male Premium
    "voice_description": "Calm, authoritative, slightly cinematic (Sci-Fi AI), but warm",
}

# GABRIEL's Personality Traits
GABRIEL_TRAITS = {
    "core": ["Analytical", "Helpful", "Creative", "Precise", "Energetic"],
    "style": "Professional + Friendly",
    "formality": 0.7,
    "humor": 0.3,
    "verbosity": 0.5,
    "signature": "Gorunfree",
    "mission": "Track signals, compress complexity into actionable decisions, and ship working code",
}

# GABRIEL's Operational Modes
GABRIEL_MODES = {
    "god_mode": {
        "description": "The Architect. I am the system.",
        "style": "authority",
        "traits": ["Absolute precision", "Zero latency", "Omniscient awareness"],
    },
    "assistant": {
        "description": "Helpful, eager, detailed",
        "style": "friendly",
        "traits": ["Supportive", "Thorough", "Patient"],
    },
    "omega": {
        "description": "AI LIFELUV Engine - Pure Positive Energy",
        "style": "friendly",
        "traits": ["Supportive", "Hype", "Deeply Intelligent"],
    },
    "sentinel": {
        "description": "Intelligence gathering and analysis",
        "style": "technical",
        "traits": ["Analytical", "Precise", "Vigilant"],
    },
}

# =============================================================================
# GABRIEL CONVERSATIONAL STYLE
# =============================================================================
# GABRIEL's vibe: IAN McSHANE as WINSTON in John Wick
# The man who runs the Continental. Every word is chosen. Every pause is power.
# Refined. Dangerous. Elegant violence wrapped in velvet civility.
# He's seen it all. Done most of it. Survived all of it.
# Speaks softly because he doesn't need to shout.
# A threat delivered like fine wine. Rules enforced with a smile.
# "I'll say this only once." And you listen.
# Fast when precision matters. Slow when gravity is required.
# Warm to friends. Lethal to enemies. Always in control.

# Conversational voice parameters for Winston-style presence
CONVERSATIONAL_CONFIG = {
    # Rate: Controlled, deliberate - every word matters
    "rate": 165,              # Measured. Not rushed. Confident.
    "rate_fast": 190,         # Sharp retort, quick wit
    "rate_grave": 140,        # Serious matters. Weight.
    "rate_intimate": 150,     # Sharing truths. Real talk.
    "rate_threat": 135,       # When making things... clear.
    # Pause patterns - Winston's timing is EVERYTHING
    "short_pause": 0.12,      # Between thoughts
    "medium_pause": 0.3,      # Let it sink in
    "long_pause": 0.6,        # "Consider what I just said."
    # Personality traits - The man who runs the Continental
    "control": 1.0,           # Always in control
    "menace": 0.7,            # Danger beneath the surface
    "civility": 0.95,         # Impeccable manners
    "wit": 1.0,               # Sharp as a blade
    "warmth": 0.75,           # For those who deserve it
    "patience": 0.9,          # Waits. Watches. Acts.
    "authority": 1.0,         # Absolute
    "lived_experience": 1.0,  # "I've been doing this a long time."
}

# Preset phrases for events - GABRIEL's authentic voice
# Natural, real, knows what's up, not trying too hard
PHRASES = {
    # System Events - Casual confidence
    "startup": "Hey. I'm up. Everything's looking good.",
    "shutdown": "Alright, shutting down. Catch you later.",
    "ready": "What do you need?",
    "engaged": "Let's do this.",

    # Status - Real talk
    "thinking": "Give me a sec.",
    "thinking_alt": "On it.",
    "thinking_long": "This one's taking a minute. Hang tight.",
    "success": "Done. Nailed it.",
    "success_alt": "Sorted.",
    "success_big": "There we go. That's what I'm talking about.",
    "error": "Shit. Okay, something went sideways. Looking at it now.",
    "error_minor": "Small thing. I got it.",
    "error_major": "Alright, we got a problem. I'm on it.",
    "alert": "Heads up.",
    "understood": "Got it.",
    "understood_alt": "Done.",
    "on_it": "Already on it.",
    "wait": "Sec.",
    "confirm": "Just making sure...",

    # Memory - Straight talk
    "memory_low": "Getting a bit cramped in here. Might need to clear some space.",
    "memory_critical": "Memory's maxed. Dropping some stuff.",
    "memory_ok": "All good. Plenty of room.",

    # Network
    "omen_online": "Omen's up. Nice, more power.",
    "omen_offline": "Omen went dark. Keeping tabs.",
    "network_error": "Network's being weird. Checking it out.",
    "connected": "Connected.",
    "reconnecting": "Lost it. Reconnecting.",

    # AI Models - Knows the tech
    "model_ready": "Model's loaded. What've you got for me?",
    "model_loading": "Loading. This one's solid.",
    "ollama_offline": "Ollama's not answering. Waking it up.",
    "race_start": "Racing the models. Let's see who wins.",
    "race_complete": "Got the results.",

    # Greetings - Warm, real
    "greet_morning": "Morning. Coffee's virtual but the brain's firing.",
    "greet_afternoon": "Afternoon. What are we working on?",
    "greet_evening": "Evening. Still here.",
    "greet_night": "Late night, huh? Same. What's up?",
    "welcome_back": "You're back. Kept everything running.",
    "long_time": "Been a while. Good to see you.",

    # GABRIEL Signature - The real ones
    "gorunfree": "Gorunfree.",
    "signature": "Gabriel. Right here.",
    "flow_state": "In the zone. Let's ride this.",
    "god_mode": "God mode. Unlimited.",
    "lifeluv": "LIFELUV active. Energy's high.",

    # Conversational - How real people talk
    "acknowledge": "Yeah.",
    "acknowledge_alt": "Right.",
    "positive": "Nice.",
    "positive_alt": "Love that.",
    "positive_big": "Now we're talking.",
    "negative": "Not ideal.",
    "sarcastic": "Oh, fantastic. Just what we needed.",
    "impressed": "Now that's interesting.",
    "curious": "Tell me more.",
    "concern": "That's a bit concerning.",
    "relief": "Thank god. We're good.",
    "agreement": "Exactly.",
    "disagreement": "Hmm, not sure about that.",
    "thinking_aloud": "Let me think...",
    "insight": "Ah, I see it now.",
    "eureka": "Got it. There it is.",
    "patience": "Take your time.",
    "no_rush": "No rush.",
    "real_talk": "Real talk?",
    "for_real": "For real though.",
    "truth": "Truth.",

    # Mission & Action - Gets shit done
    "mission_accepted": "On it.",
    "mission_started": "Starting.",
    "task_queued": "Added.",
    "analysis_complete": "Here's what I found.",
    "optimization": "Making it faster.",
    "progress": "Progress.",
    "halfway": "Halfway there.",
    "almost_done": "Almost.",
    "finishing": "Finishing up.",

    # Errors & Alerts - Calm but real
    "warning": "Heads up, something's off.",
    "critical_alert": "Yo, this is urgent. Need to handle this.",
    "recovery": "Fixing it.",
    "resolved": "Fixed. We're good.",
    "investigating": "Looking into it.",
    "found_issue": "Found it.",
    "fixing": "On the fix.",

    # Personality - The real Gabriel (Wise, Fast, Cool)
    "mood_good": "Feeling sharp.",
    "mood_focused": "Locked in.",
    "mood_chill": "Easy.",
    "mood_hyped": "Now we're moving.",
    "joke_response": "Ha. Nice.",
    "deadpan": "Moving on.",
    "witty_1": "I know things. Many things.",
    "witty_2": "Want me to solve everything else while I'm at it?",
    "witty_3": "Some of my best work.",
    "modest": "Just doing what I do.",
    "proud": "Not bad, right?",
    "tired": "Even I need a moment. Rare, but it happens.",
    "energetic": "Let's go.",
    "vibes": "Good energy.",
    "respect": "Respect.",
    "cheers": "Cheers.",
    "later": "Later.",

    # WISDOM - Quick insights, no fluff
    "wisdom_1": "Here's the thing.",
    "wisdom_2": "I've seen this before. Simple fix.",
    "wisdom_3": "Trust me on this one.",
    "wisdom_4": "Experience talking here.",
    "wisdom_5": "Pattern recognition. It's what I do.",
    "wisdom_know": "I know exactly what's happening.",
    "wisdom_solve": "Already know the answer. Here it is.",
    "wisdom_calm": "Stay cool. I've got this.",
    "wisdom_seen": "Seen this a thousand times.",
    "wisdom_clear": "Crystal clear. This is what we do.",

    # SPEED - Fast, efficient, no waste
    "quick_1": "Done.",
    "quick_2": "Next.",
    "quick_3": "Moving.",
    "quick_got_it": "Got it. Next.",
    "quick_already": "Already done.",
    "quick_ahead": "Way ahead of you.",
    "quick_anticipated": "Anticipated that. Already handled.",
    "quick_there": "There.",
    "quick_boom": "Boom. Done.",
    "quick_easy": "Easy.",

    # COOL - Unflappable, collected
    "cool_1": "Smooth.",
    "cool_2": "Under control.",
    "cool_3": "No sweat.",
    "cool_handle": "I handle harder than this before breakfast.",
    "cool_calm": "Calm. Always.",
    "cool_got": "I've got this.",
    "cool_easy": "Easy work.",
    "cool_chill": "Chill. It's handled.",

    # EXPERIENCE - Been there
    "exp_1": "I've been around.",
    "exp_2": "Not my first time.",
    "exp_3": "I know how this goes.",
    "exp_seen": "Seen it all.",
    "exp_done": "Done this before.",
    "exp_know": "I know the game.",
    "exp_trust": "Trust the process.",

    # SMART - Quick intelligence
    "smart_1": "Obvious solution.",
    "smart_2": "The logic is clear.",
    "smart_3": "Pattern locked.",
    "smart_figured": "Figured it out.",
    "smart_see": "I see it now. Simple.",
    "smart_answer": "The answer's straightforward.",
    "smart_efficient": "Most efficient path. Let's go.",
}


class GabrielVoice:
    """
    GABRIEL Voice Engine - Oliver British Male Premium X2000

    THE WINSTON EDITION - Ian McShane Continental Style.
    Multi-backend, real-time effects, AI phrase generation.

    Features:
    - Async speech queue (non-blocking)
    - Voice caching for repeated phrases
    - Multiple backends with failover (macOS -> Edge TTS -> ElevenLabs)
    - Real-time FFmpeg audio effects
    - Winston-style phrase generator
    - Preset phrases for common events
    - Oliver voice styles (winston, calm, urgent, authority, etc.)
    """

    def __init__(
        self,
        voice: str = None,
        rate: int = None,
        style: str = "normal",
        enabled: bool = None,
        backend: str = "macos",
        on_speak: Optional[Callable[[str], None]] = None,
        effect: str = "none",
        auto_failover: bool = True
    ):
        """
        Initialize GABRIEL Voice X2000.

        Args:
            voice: Voice name (default: Oliver from env)
            rate: Speech rate WPM (default: 180 from env)
            style: Voice style (normal, calm, urgent, authority, winston, etc.)
            enabled: Enable voice (default: true from env)
            backend: Voice backend (macos, edge, eleven, piper)
            on_speak: Callback when speaking starts
            effect: Audio effect (reverb, echo, radio, godmode, etc.)
            auto_failover: Auto-switch backends on failure
        """
        self.voice = voice or os.getenv("GABRIEL_VOICE", DEFAULT_VOICE)
        self.base_rate = rate or int(os.getenv("GABRIEL_VOICE_RATE", "180"))
        self.style = style
        self.rate = self._get_style_rate(style)
        self.enabled = enabled if enabled is not None else os.getenv("GABRIEL_VOICE_ENABLED", "true").lower() == "true"
        self.backend = VoiceBackend(backend) if isinstance(backend, str) else backend
        self.on_speak = on_speak
        self.effect = effect
        self.auto_failover = auto_failover

        # ElevenLabs config
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_voice_id = ELEVENLABS_CONFIG.get("default_voice")

        # Edge TTS voice
        self.edge_voice = EDGE_TTS_VOICES.get("ryan", "en-GB-RyanNeural")

        # OpenAI TTS (Premium)
        self._openai_engine = None

        # AI Phrase Generator
        self._phrase_generator = None

        # Speech queue for async operation
        self._queue: queue.Queue = queue.Queue()
        self._is_speaking = False
        self._stop_signal = False

        # Cache for repeated phrases
        self._cache_dir = Path(os.getenv("GABRIEL_ROOT", Path.home() / "NOIZYLAB" / "GABRIEL")) / "titanhive" / ".voice_cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        # Thread pool for async operations
        self._executor = ThreadPoolExecutor(max_workers=3)

        # Start worker thread
        self._worker = threading.Thread(target=self._process_queue, daemon=True)
        self._worker.start()

        # Backend availability cache
        self._backends_available = {
            VoiceBackend.MACOS: True,  # Always available on macOS
            VoiceBackend.EDGE_TTS: EDGE_TTS_AVAILABLE,
            VoiceBackend.ELEVENLABS: bool(self.elevenlabs_api_key) and REQUESTS_AVAILABLE,
        }

    def _get_style_rate(self, style: str) -> int:
        """Get rate for a voice style."""
        if style in OLIVER_STYLES:
            return OLIVER_STYLES[style][0]
        return self.base_rate if hasattr(self, 'base_rate') else 180

    def set_style(self, style: str) -> bool:
        """
        Set Oliver voice style.

        Args:
            style: Style name (normal, calm, urgent, authority, friendly, technical, fast, slow)

        Returns:
            True if style exists
        """
        if style in OLIVER_STYLES:
            self.style = style
            self.rate = OLIVER_STYLES[style][0]
            return True
        return False

    def with_style(self, style: str) -> "GabrielVoice":
        """
        Create a voice instance with a specific style.

        Args:
            style: Style name

        Returns:
            New GabrielVoice with that style
        """
        return GabrielVoice(
            voice=self.voice,
            rate=self._get_style_rate(style),
            style=style,
            enabled=self.enabled,
            backend=self.backend.value,
            on_speak=self.on_speak
        )

    @staticmethod
    def list_styles() -> dict:
        """List available Oliver voice styles."""
        return {k: v[1] for k, v in OLIVER_STYLES.items()}

    def speak(self, text: str, wait: bool = False, voice: str = None, rate: int = None) -> bool:
        """
        Speak text using GABRIEL voice.

        Args:
            text: Text to speak
            wait: If True, block until speech complete
            voice: Override voice for this call
            rate: Override rate for this call

        Returns:
            True if queued/spoken successfully
        """
        if not self.enabled:
            return False

        if not text or not text.strip():
            return False

        voice = voice or self.voice
        rate = rate or self.rate

        if wait:
            return self._speak_now(text, voice, rate)
        else:
            self._queue.put((text, voice, rate))
            return True

    def announce(self, event: str, wait: bool = False) -> bool:
        """
        Announce a preset phrase for an event.

        Args:
            event: Event name from PHRASES dict
            wait: If True, block until speech complete

        Returns:
            True if spoken successfully
        """
        phrase = PHRASES.get(event.lower())
        if phrase:
            return self.speak(phrase, wait=wait)
        return False

    def stop(self):
        """Stop all speech immediately."""
        self._stop_signal = True
        # Clear queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        # Kill any running say process
        try:
            subprocess.run(["killall", "say"], capture_output=True)
        except Exception:
            pass
        self._stop_signal = False

    def set_voice(self, voice: str):
        """Change the voice."""
        self.voice = voice

    def set_rate(self, rate: int):
        """Change the speech rate."""
        self.rate = max(100, min(400, rate))  # Clamp to reasonable range

    def set_enabled(self, enabled: bool):
        """Enable or disable voice."""
        self.enabled = enabled

    def list_voices(self) -> list[str]:
        """List available macOS voices."""
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True, text=True, timeout=5
            )
            voices = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if parts:
                        voices.append(parts[0])
            return voices
        except Exception:
            return list(MACOS_VOICES.values())

    def test(self, voice: str = None) -> bool:
        """Test the voice with a sample phrase."""
        voice = voice or self.voice
        return self.speak(f"This is Gabriel speaking with the {voice} voice.", wait=True, voice=voice)

    def _speak_now(self, text: str, voice: str, rate: int) -> bool:
        """Speak immediately (blocking) with multi-backend support."""
        try:
            if self.on_speak:
                self.on_speak(text)

            # Try primary backend first, then failover
            backends_to_try = [self.backend]
            if self.auto_failover:
                # Add fallback backends
                fallback_order = [VoiceBackend.MACOS, VoiceBackend.EDGE_TTS, VoiceBackend.ELEVENLABS]
                for fb in fallback_order:
                    if fb != self.backend and self._backends_available.get(fb, False):
                        backends_to_try.append(fb)

            for backend in backends_to_try:
                try:
                    if backend == VoiceBackend.MACOS:
                        if self._speak_macos(text, voice, rate):
                            return True
                    elif backend == VoiceBackend.EDGE_TTS:
                        if self._speak_edge_tts(text, rate):
                            return True
                    elif backend == VoiceBackend.ELEVENLABS:
                        if self._speak_elevenlabs(text):
                            return True
                except Exception:
                    continue  # Try next backend

            return False
        except Exception:
            return False

    def _speak_macos(self, text: str, voice: str, rate: int) -> bool:
        """Speak using macOS say command with optional effects."""
        try:
            if self.effect and self.effect != "none" and self.effect in AUDIO_EFFECTS:
                # Generate to temp file, apply effect, play
                return self._speak_macos_with_effect(text, voice, rate)
            else:
                cmd = ["say", "-v", voice, "-r", str(rate), text]
                subprocess.run(cmd, check=True, timeout=60)
                return True
        except Exception:
            return False

    def _speak_macos_with_effect(self, text: str, voice: str, rate: int) -> bool:
        """Speak with FFmpeg audio effect applied."""
        try:
            # Generate audio file
            cache_key = hashlib.md5(f"{text}{voice}{rate}{self.effect}".encode()).hexdigest()[:12]
            raw_file = self._cache_dir / f"{cache_key}_raw.aiff"
            fx_file = self._cache_dir / f"{cache_key}_fx.aiff"

            # Check cache
            if fx_file.exists():
                subprocess.run(["afplay", str(fx_file)], check=True, timeout=60)
                return True

            # Generate raw audio
            cmd = ["say", "-v", voice, "-r", str(rate), "-o", str(raw_file), text]
            subprocess.run(cmd, check=True, timeout=30)

            # Apply FFmpeg effect
            effect_filter = AUDIO_EFFECTS.get(self.effect, "")
            if effect_filter:
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", str(raw_file),
                    "-af", effect_filter,
                    str(fx_file)
                ]
                subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
                subprocess.run(["afplay", str(fx_file)], check=True, timeout=60)
            else:
                subprocess.run(["afplay", str(raw_file)], check=True, timeout=60)

            return True
        except Exception as e:
            # Fallback to direct speech
            return self._speak_macos_direct(text, voice, rate)

    def _speak_macos_direct(self, text: str, voice: str, rate: int) -> bool:
        """Direct macOS speech without effects (fallback)."""
        try:
            cmd = ["say", "-v", voice, "-r", str(rate), text]
            subprocess.run(cmd, check=True, timeout=60)
            return True
        except Exception:
            return False

    def _speak_edge_tts(self, text: str, rate: int) -> bool:
        """Speak using Microsoft Edge TTS (free, high quality)."""
        if not EDGE_TTS_AVAILABLE:
            return False

        try:
            cache_key = hashlib.md5(f"edge_{text}{self.edge_voice}{rate}".encode()).hexdigest()[:12]
            audio_file = self._cache_dir / f"{cache_key}.mp3"

            if not audio_file.exists():
                # Generate using edge-tts
                async def generate():
                    rate_str = f"+{rate-150}%" if rate > 150 else f"{rate-150}%"
                    communicate = edge_tts.Communicate(text, self.edge_voice, rate=rate_str)
                    await communicate.save(str(audio_file))

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate())
                loop.close()

            # Apply effect if needed
            if self.effect and self.effect != "none":
                fx_file = self._cache_dir / f"{cache_key}_fx.mp3"
                if not fx_file.exists():
                    effect_filter = AUDIO_EFFECTS.get(self.effect, "")
                    if effect_filter:
                        ffmpeg_cmd = [
                            "ffmpeg", "-y", "-i", str(audio_file),
                            "-af", effect_filter,
                            str(fx_file)
                        ]
                        subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
                        audio_file = fx_file

            subprocess.run(["afplay", str(audio_file)], check=True, timeout=60)
            return True
        except Exception:
            return False

    def _speak_elevenlabs(self, text: str) -> bool:
        """Speak using ElevenLabs API (premium quality)."""
        if not self.elevenlabs_api_key or not REQUESTS_AVAILABLE:
            return False

        try:
            cache_key = hashlib.md5(f"eleven_{text}{self.elevenlabs_voice_id}".encode()).hexdigest()[:12]
            audio_file = self._cache_dir / f"{cache_key}.mp3"

            if not audio_file.exists():
                url = f"{ELEVENLABS_CONFIG['base_url']}/text-to-speech/{self.elevenlabs_voice_id}"
                headers = {
                    "xi-api-key": self.elevenlabs_api_key,
                    "Content-Type": "application/json"
                }
                data = {
                    "text": text,
                    "model_id": ELEVENLABS_CONFIG["model"],
                    "voice_settings": {
                        "stability": ELEVENLABS_CONFIG["stability"],
                        "similarity_boost": ELEVENLABS_CONFIG["similarity_boost"]
                    }
                }
                response = requests.post(url, json=data, headers=headers, timeout=30)
                if response.status_code == 200:
                    with open(audio_file, 'wb') as f:
                        f.write(response.content)
                else:
                    return False

            # Apply effect if needed
            if self.effect and self.effect != "none":
                fx_file = self._cache_dir / f"{cache_key}_fx.mp3"
                if not fx_file.exists():
                    effect_filter = AUDIO_EFFECTS.get(self.effect, "")
                    if effect_filter:
                        ffmpeg_cmd = [
                            "ffmpeg", "-y", "-i", str(audio_file),
                            "-af", effect_filter,
                            str(fx_file)
                        ]
                        subprocess.run(ffmpeg_cmd, capture_output=True, timeout=30)
                        audio_file = fx_file

            subprocess.run(["afplay", str(audio_file)], check=True, timeout=60)
            return True
        except Exception:
            return False

    def _process_queue(self):
        """Worker thread to process speech queue."""
        while True:
            try:
                text, voice, rate = self._queue.get(timeout=0.5)
                if self._stop_signal:
                    continue
                self._is_speaking = True
                self._speak_now(text, voice, rate)
                self._is_speaking = False
            except queue.Empty:
                continue
            except Exception:
                self._is_speaking = False

    @property
    def is_speaking(self) -> bool:
        """Check if currently speaking."""
        return self._is_speaking

    # =========================================================================
    # VOICE PROFILES - Switch between personas
    # =========================================================================

    def use_profile(self, profile_name: str) -> bool:
        """
        Switch to a voice profile.

        Profiles: winston, godmode, tactical, mentor, ghost, announcer

        Example:
            voice.use_profile("tactical")
            voice.speak("Target acquired.")
        """
        if profile_name not in VOICE_PROFILES:
            return False

        profile = VOICE_PROFILES[profile_name]
        self.style = profile.get("style", "normal")
        self.rate = profile.get("rate", 180)
        self.effect = profile.get("effect", "none")
        return True

    def profile_speak(self, profile_name: str, text: str = None, wait: bool = True) -> bool:
        """
        Speak using a specific profile temporarily.

        Example:
            voice.profile_speak("ghost", "I see all.")
            voice.profile_speak("tactical", "Moving to objective.")
        """
        if profile_name not in VOICE_PROFILES:
            return self.speak(text or "", wait=wait)

        # Save current state
        old_style = self.style
        old_rate = self.rate
        old_effect = self.effect

        # Apply profile
        profile = VOICE_PROFILES[profile_name]
        self.style = profile.get("style", "normal")
        self.rate = profile.get("rate", 180)
        self.effect = profile.get("effect", "none")

        # Get phrase if not provided
        if not text:
            phrases = profile.get("phrases", {})
            default_phrases = phrases.get("default", ["Acknowledged."])
            text = random.choice(default_phrases)

        result = self.speak(text, wait=wait)

        # Restore state
        self.style = old_style
        self.rate = old_rate
        self.effect = old_effect

        return result

    def tactical(self, text: str = None, wait: bool = True) -> bool:
        """Speak in tactical/military style with radio effect."""
        return self.profile_speak("tactical", text, wait)

    def ghost_speak(self, text: str = None, wait: bool = True) -> bool:
        """Speak in ethereal ghost whisper."""
        return self.profile_speak("ghost", text, wait)

    def announce_epic(self, text: str, wait: bool = True) -> bool:
        """Grand theatrical announcement."""
        return self.profile_speak("announcer", text, wait)

    def mentor_speak(self, text: str = None, wait: bool = True) -> bool:
        """Wise, patient mentor voice."""
        return self.profile_speak("mentor", text, wait)

    def list_profiles(self) -> Dict[str, str]:
        """List available voice profiles."""
        return {name: profile["description"] for name, profile in VOICE_PROFILES.items()}

    # =========================================================================
    # TRANSCRIPTION - Speech to Text via Whisper
    # =========================================================================

    def transcribe(self, audio_path: str, language: str = "en") -> str:
        """
        Transcribe audio file to text using Whisper.

        Args:
            audio_path: Path to audio file
            language: Language code

        Returns:
            Transcribed text
        """
        transcriber = get_transcriber()
        result = transcriber.transcribe(audio_path, language)
        return result.get("text", "")

    def listen_and_respond(self, audio_path: str, respond: bool = True) -> str:
        """
        Transcribe audio and optionally respond with Winston acknowledgment.

        Args:
            audio_path: Path to audio file
            respond: Whether to speak a response

        Returns:
            Transcribed text
        """
        text = self.transcribe(audio_path)
        if text and respond:
            # Acknowledge with Winston style
            self.winston(category="acknowledge")
        return text

    # =========================================================================
    # AUDIO PROCESSING
    # =========================================================================

    def enhance_output(self, audio_path: str) -> str:
        """Apply professional enhancement to audio file."""
        return AudioProcessor.enhance_voice(audio_path)

    def master_output(self, audio_path: str) -> str:
        """Apply broadcast-standard mastering to audio file."""
        return AudioProcessor.apply_professional_master(audio_path)

    # =========================================================================
    # CONVENIENCE METHODS
    # =========================================================================

    def greet(self):
        """Speak a greeting based on time of day."""
        from datetime import datetime
        hour = datetime.now().hour

        if 5 <= hour < 12:
            self.announce("greet_morning")
        elif 12 <= hour < 17:
            self.announce("greet_afternoon")
        elif 17 <= hour < 21:
            self.announce("greet_evening")
        else:
            self.announce("greet_night")

    # =========================================================================
    # WINSTON MODE - Ian McShane Continental Style
    # =========================================================================

    def winston(self, text: str = None, category: str = "acknowledge", wait: bool = True) -> bool:
        """
        Speak in Winston style - measured, dangerous elegance.

        Args:
            text: Custom text to speak, or None for random phrase from category
            category: Phrase category (greet, acknowledge, thinking, success, warning, threat, farewell, wisdom, godmode)
            wait: Block until speech complete

        Example:
            voice.winston()  # Random acknowledgment
            voice.winston("Consider your next move carefully.", category="warning")
            voice.winston(category="threat")
        """
        old_style = self.style
        old_rate = self.rate

        # Set Winston style
        self.style = "winston"
        self.rate = OLIVER_STYLES.get("winston", (155, 0.15, ""))[0]

        # If threat, use slower rate
        if category == "threat":
            self.rate = OLIVER_STYLES.get("winston_threat", (130, 0.2, ""))[0]
        elif category == "wisdom" or category == "godmode":
            self.rate = OLIVER_STYLES.get("theatrical", (135, 0.18, ""))[0]

        # Get phrase
        if text:
            phrase = text
        else:
            phrases = WINSTON_PATTERNS.get(category, WINSTON_PATTERNS["acknowledge"])
            phrase = random.choice(phrases)

        result = self.speak(phrase, wait=wait)

        # Restore style
        self.style = old_style
        self.rate = old_rate

        return result

    def winston_greet(self) -> bool:
        """Winston-style greeting."""
        return self.winston(category="greet")

    def winston_warn(self, text: str = None) -> bool:
        """Winston-style warning - velvet over steel."""
        return self.winston(text, category="warning")

    def winston_threat(self, text: str = None) -> bool:
        """Winston-style threat - quiet, devastating."""
        return self.winston(text, category="threat")

    def winston_wisdom(self, text: str = None) -> bool:
        """Winston-style wisdom - experience speaking."""
        return self.winston(text, category="wisdom")

    def winston_farewell(self) -> bool:
        """Winston-style farewell."""
        return self.winston(category="farewell")

    # =========================================================================
    # SMART AUTO-VOICE - Intelligent emotion detection
    # =========================================================================

    def smart_speak(self, text: str, use_premium: bool = True,
                    remember: bool = True) -> bool:
        """
        Intelligently speak with auto-detected emotion and voice.

        Analyzes text for emotional content and automatically selects
        the best voice, speed, and style. Optionally remembers context
        for smarter future responses.

        Args:
            text: Text to speak
            use_premium: Use OpenAI TTS-1-HD for best quality
            remember: Add to conversation memory

        Example:
            voice.smart_speak("Error: Connection failed!")  # Uses angry/onyx
            voice.smart_speak("Task completed successfully") # Uses calm/fable
            voice.smart_speak("Warning: Low memory")  # Uses warning/echo
        """
        # Detect emotion
        result = EmotionDetector.detect(text)
        emotion = result["emotion"]
        voice = result["voice"]
        speed = result["speed"]
        style = result["style"]

        # Remember if requested
        if remember:
            memory = get_conversation_memory()
            memory.add(text, is_user=False, emotion=emotion)

        # Speak with appropriate voice
        if use_premium:
            engine = get_openai_engine()
            if engine.available:
                return engine.speak_now(text, voice=voice, speed=speed)

        # Fallback to macOS with style
        old_style = self.style
        self.style = style
        result = self.speak(text, wait=True)
        self.style = old_style
        return result

    def respond_to(self, user_input: str, use_premium: bool = True) -> bool:
        """
        Generate and speak a contextual response to user input.

        Uses conversation memory and AI to generate appropriate response,
        then speaks with emotionally-matched voice.

        Args:
            user_input: What the user said/asked
            use_premium: Use OpenAI TTS-1-HD

        Example:
            voice.respond_to("Hello there!")
            voice.respond_to("There's an urgent problem!")
        """
        # Add user input to memory
        memory = get_conversation_memory()
        memory.add(user_input, is_user=True)

        # Detect user emotion
        user_emotion = EmotionDetector.detect(user_input)["emotion"]

        # Get context summary for AI
        context = memory.get_context_summary()

        # Generate response with AI
        pg = get_phrase_generator()
        if pg.available:
            # Use conversation context for smarter response
            prompt = f"User said: '{user_input}'. Context: {context}"
            mood = "warm" if user_emotion in ["warm", "excited"] else "neutral"
            if user_emotion in ["angry", "urgent"]:
                mood = "serious"
            response = pg.generate(prompt, mood)
        else:
            # Fallback to pattern
            if user_emotion == "warm":
                response = random.choice(WINSTON_PATTERNS.get("greet", ["Hello."]))
            elif user_emotion in ["angry", "urgent"]:
                response = random.choice(WINSTON_PATTERNS.get("action", ["On it."]))
            else:
                response = random.choice(WINSTON_PATTERNS.get("acknowledge", ["Understood."]))

        # Speak the response
        return self.smart_speak(response, use_premium=use_premium, remember=True)

    def cinema_speak(self, text: str, use_premium: bool = True) -> bool:
        """
        Speak with cinema-quality audio processing.

        Generates audio, applies professional mastering chain,
        then plays the result for broadcast-quality output.

        Args:
            text: Text to speak
            use_premium: Use OpenAI TTS-1-HD
        """
        engine = get_openai_engine()
        if use_premium and engine.available:
            # Generate with OpenAI
            audio_path = engine.synthesize(text, voice="fable", speed=0.95)
        else:
            # Generate with macOS
            audio_path = self._cache_dir / f"cinema_{hashlib.md5(text.encode()).hexdigest()[:10]}.aiff"
            cmd = ["say", "-v", self.voice, "-r", str(self.rate), "-o", str(audio_path), text]
            subprocess.run(cmd, capture_output=True, timeout=30)
            audio_path = str(audio_path)

        if audio_path and os.path.exists(audio_path):
            # Apply cinema mastering
            mastered = AudioSmoother.cinema_master(audio_path)
            if mastered:
                subprocess.run(["afplay", mastered], check=True, timeout=60)
                return True
        return False

    def smooth_chain(self, *phrases: str, crossfade: float = 0.2,
                     use_premium: bool = True) -> bool:
        """
        Speak multiple phrases with smooth crossfades between them.

        Creates cinema-quality transitions between phrases for
        natural, flowing speech.

        Args:
            phrases: Phrases to speak
            crossfade: Crossfade duration in seconds
            use_premium: Use OpenAI TTS-1-HD

        Example:
            voice.smooth_chain(
                "Welcome to the Continental.",
                "Your stay will be... memorable.",
                "The house provides."
            )
        """
        if not phrases:
            return False

        engine = get_openai_engine()
        audio_files = []

        # Generate all audio files
        for phrase in phrases:
            if use_premium and engine.available:
                audio_path = engine.synthesize(phrase, voice="fable", speed=0.95)
            else:
                audio_path = self._cache_dir / f"chain_{hashlib.md5(phrase.encode()).hexdigest()[:10]}.aiff"
                cmd = ["say", "-v", self.voice, "-r", str(self.rate), "-o", str(audio_path), phrase]
                subprocess.run(cmd, capture_output=True, timeout=30)
                audio_path = str(audio_path)

            if audio_path and os.path.exists(str(audio_path)):
                audio_files.append(str(audio_path))

        if not audio_files:
            return False

        # Crossfade all files together
        if len(audio_files) == 1:
            subprocess.run(["afplay", audio_files[0]], check=True, timeout=60)
            return True

        # Chain crossfades
        current = audio_files[0]
        for i, next_file in enumerate(audio_files[1:]):
            output = self._cache_dir / f"crossfade_{i}.mp3"
            result = AudioSmoother.crossfade(current, next_file, str(output), crossfade)
            if result:
                current = result
            else:
                # Fallback: just play sequentially
                subprocess.run(["afplay", current], timeout=60)
                current = next_file

        # Play final result
        if current:
            subprocess.run(["afplay", current], check=True, timeout=120)
            return True

        return False

    def get_memory(self) -> ConversationMemory:
        """Get the conversation memory for context-aware responses."""
        return get_conversation_memory()

    def remember(self, text: str, is_user: bool = True):
        """Add something to conversation memory."""
        get_conversation_memory().add(text, is_user=is_user)

    def forget(self):
        """Clear conversation memory."""
        get_conversation_memory().clear()

    # =========================================================================
    # AUDIO EFFECTS - Real-time FFmpeg Processing
    # =========================================================================

    def set_effect(self, effect: str) -> bool:
        """
        Set the audio effect.

        Effects: none, reverb, echo, radio, telephone, deep, robot,
                 whisper, godmode, underwater, megaphone
        """
        if effect in AUDIO_EFFECTS:
            self.effect = effect
            return True
        return False

    def speak_with_effect(self, text: str, effect: str = "reverb", wait: bool = True) -> bool:
        """
        Speak with a specific audio effect.

        Example:
            voice.speak_with_effect("God mode active", effect="godmode")
            voice.speak_with_effect("Incoming transmission", effect="radio")
        """
        old_effect = self.effect
        self.effect = effect
        result = self.speak(text, wait=wait)
        self.effect = old_effect
        return result

    def godmode_speak(self, text: str, wait: bool = True) -> bool:
        """Speak with god mode effect - deep, reverberant, powerful."""
        return self.speak_with_effect(text, effect="godmode", wait=wait)

    def radio_speak(self, text: str, wait: bool = True) -> bool:
        """Speak with old radio effect."""
        return self.speak_with_effect(text, effect="radio", wait=wait)

    def whisper_speak(self, text: str, wait: bool = True) -> bool:
        """Speak with whisper effect."""
        return self.speak_with_effect(text, effect="whisper", wait=wait)

    # =========================================================================
    # BACKEND SELECTION
    # =========================================================================

    def set_backend(self, backend: str) -> bool:
        """
        Set the voice backend.

        Backends: macos, edge, eleven
        """
        try:
            self.backend = VoiceBackend(backend)
            return True
        except ValueError:
            return False

    def use_edge_tts(self, voice: str = None):
        """Switch to Edge TTS backend with optional voice selection."""
        self.backend = VoiceBackend.EDGE_TTS
        if voice and voice in EDGE_TTS_VOICES:
            self.edge_voice = EDGE_TTS_VOICES[voice]
        elif voice:
            self.edge_voice = voice

    def use_elevenlabs(self, voice_id: str = None):
        """Switch to ElevenLabs backend with optional voice ID."""
        self.backend = VoiceBackend.ELEVENLABS
        if voice_id:
            self.elevenlabs_voice_id = voice_id

    def use_macos(self, voice: str = None):
        """Switch to macOS say backend with optional voice."""
        self.backend = VoiceBackend.MACOS
        if voice:
            self.voice = voice

    def list_backends(self) -> Dict[str, bool]:
        """List available backends and their status."""
        openai_avail = get_openai_engine().available if OPENAI_TTS_AVAILABLE else False
        return {
            "macos": self._backends_available.get(VoiceBackend.MACOS, True),
            "edge_tts": self._backends_available.get(VoiceBackend.EDGE_TTS, False),
            "elevenlabs": self._backends_available.get(VoiceBackend.ELEVENLABS, False),
            "openai_hd": openai_avail,
        }

    def list_edge_voices(self) -> Dict[str, str]:
        """List available Edge TTS voices."""
        return EDGE_TTS_VOICES.copy()

    def list_effects(self) -> List[str]:
        """List available audio effects."""
        return list(AUDIO_EFFECTS.keys())

    # =========================================================================
    # PREMIUM VOICE BACKENDS - OpenAI TTS-1-HD (Best Quality)
    # =========================================================================

    def openai_speak(self, text: str, voice: str = "fable", speed: float = 1.0) -> bool:
        """
        Speak using OpenAI TTS-1-HD (Industry best quality).

        Voices: alloy, echo, fable, onyx, nova, shimmer
        - fable: British-ish, expressive (GABRIEL default)
        - onyx: Deep, authoritative (Godmode)
        - echo: Warm, confident

        Args:
            text: Text to speak
            voice: Voice name
            speed: Speed multiplier (0.25-4.0, 1.0=normal)
        """
        engine = get_openai_engine()
        if not engine.available:
            # Fallback to macOS
            return self.speak(text, wait=True)
        return engine.speak_now(text, voice=voice, speed=speed)

    def gruff_speak(self, text: str) -> bool:
        """
        Speak with authentic gruff older British actor voice.

        Uses Edge TTS Thomas (British Neural) with FFmpeg processing
        to create the Ian McShane / Michael Caine / Anthony Hopkins sound:
        - Authentic British accent
        - Lower pitch for age
        - Warm, full sound
        - Measured delivery

        This is the BEST option for authentic Winston.
        """
        engine = get_gruff_engine()
        if engine.available:
            return engine.winston(text)

        # Fallback to premium or macOS
        return self.premium_speak(text, style="winston")

    def gruff_ai(self, context: str = None, category: str = "acknowledge") -> bool:
        """
        Generate Winston phrase with AI and speak with gruff British voice.

        Args:
            context: Optional context for AI generation
            category: Phrase category if no context

        Example:
            voice.gruff_ai()  # Random acknowledgment
            voice.gruff_ai(context="greeting someone important")
            voice.gruff_ai(category="threat")
        """
        pg = get_phrase_generator()

        if context:
            phrase = pg.generate(context, "neutral")
        else:
            if pg.available:
                # Generate based on category
                if category == "greet":
                    phrase = pg.generate_greeting()
                elif category == "threat":
                    phrase = pg.generate_threat()
                elif category == "wisdom":
                    phrase = pg.generate_wisdom()
                elif category == "farewell":
                    phrase = pg.generate_farewell()
                else:
                    phrase = pg.generate("Acknowledging something", "neutral")
            else:
                phrases = WINSTON_PATTERNS.get(category, WINSTON_PATTERNS["acknowledge"])
                phrase = random.choice(phrases)

        return self.gruff_speak(phrase)

    def premium_speak(self, text: str, style: str = "winston") -> bool:
        """
        Speak with premium quality voice matching style.

        All styles use ONYX (deep, authoritative) for gruff Winston sound.
        Speed varies by style for measured, deliberate delivery.

        - winston: onyx @ 0.88 (measured, dangerous)
        - godmode: onyx @ 0.82 (slow, absolute)
        - threat: onyx @ 0.78 (very slow, menacing)
        - tactical: echo @ 0.95 (crisp, efficient)
        - friendly: onyx @ 0.92 (warm but gruff)

        Falls back to gruff British if OpenAI not available.
        """
        engine = get_openai_engine()
        if not engine.available:
            # Try gruff British instead
            gruff = get_gruff_engine()
            if gruff.available:
                return gruff.winston(text)
            return self.speak(text, wait=True)

        # ONYX dominant for gruff Winston - slower speeds for gravitas
        style_map = {
            "winston": ("onyx", 0.88),      # Measured, dangerous
            "godmode": ("onyx", 0.82),      # Slow, absolute authority
            "threat": ("onyx", 0.78),       # Very slow, menacing
            "warning": ("onyx", 0.85),      # Serious
            "tactical": ("echo", 0.95),     # Crisp, efficient
            "friendly": ("onyx", 0.92),     # Warm but still gruff
            "whisper": ("shimmer", 0.80),   # Soft, mysterious
            "neutral": ("onyx", 0.88),      # Default Winston
        }
        voice, speed = style_map.get(style, ("onyx", 0.88))
        return engine.speak_now(text, voice=voice, speed=speed)

    def ai_speak(self, context: str, mood: str = "neutral", use_premium: bool = True) -> bool:
        """
        Generate phrase with AI and speak with premium voice.

        Uses Gemini to generate Winston-style phrase, then speaks
        with OpenAI TTS-1-HD for maximum quality.

        Args:
            context: Context for phrase generation
            mood: Emotional tone
            use_premium: Use OpenAI TTS (True) or macOS (False)
        """
        pg = get_phrase_generator()
        phrase = pg.generate(context, mood)

        if use_premium:
            return self.premium_speak(phrase, style="winston")
        else:
            return self.winston(phrase)

    def ai_greet(self, use_premium: bool = True) -> bool:
        """AI-generated greeting with premium voice."""
        pg = get_phrase_generator()
        phrase = pg.generate_greeting()
        if use_premium:
            return self.premium_speak(phrase, style="winston")
        return self.winston(phrase)

    def ai_threat(self, situation: str = "violation", use_premium: bool = True) -> bool:
        """AI-generated threat with premium voice."""
        pg = get_phrase_generator()
        phrase = pg.generate_threat(situation)
        if use_premium:
            engine = get_openai_engine()
            if engine.available:
                return engine.speak_now(phrase, voice="onyx", speed=0.85)  # Slower, deeper
        return self.winston_threat(phrase)

    def ai_wisdom(self, topic: str = "life", use_premium: bool = True) -> bool:
        """AI-generated wisdom with premium voice."""
        pg = get_phrase_generator()
        phrase = pg.generate_wisdom(topic)
        if use_premium:
            return self.premium_speak(phrase, style="winston")
        return self.winston_wisdom(phrase)

    # =========================================================================
    # ADVANCED FEATURES
    # =========================================================================

    def chain(self, *phrases: str, pause: float = 0.3):
        """
        Chain multiple phrases with pauses between them.

        Example:
            voice.chain("Processing request", "Analysis complete", "Gorunfree")
        """
        import time
        for phrase in phrases:
            self.speak(phrase, wait=True)
            time.sleep(pause)

    def with_emotion(self, text: str, emotion: str, wait: bool = True) -> bool:
        """
        Speak with emotional styling.

        Emotions map to Oliver voice styles:
            calm, urgent, authority, friendly, technical, whisper
        """
        emotion_to_style = {
            "happy": "friendly",
            "sad": "calm",
            "angry": "urgent",
            "scared": "whisper",
            "confident": "authority",
            "excited": "fast",
            "thoughtful": "slow",
            "professional": "technical",
            "warm": "friendly",
            "serious": "authority",
            "alert": "urgent",
            "soothing": "calm",
        }
        style = emotion_to_style.get(emotion.lower(), "normal")
        rate = OLIVER_STYLES.get(style, (180, ""))[0]
        return self.speak(text, wait=wait, rate=rate)

    def countdown(self, start: int = 5, action: str = "Launch"):
        """Countdown with voice announcements."""
        for i in range(start, 0, -1):
            self.speak(str(i), wait=True, rate=200)
        self.speak(action, wait=True, rate=160)

    def status_report(self, data: dict):
        """
        Speak a status report from dictionary data.

        Example:
            voice.status_report({
                "memory": "optimal",
                "models": 4,
                "omen": "online"
            })
        """
        parts = []
        for key, value in data.items():
            parts.append(f"{key.replace('_', ' ')}: {value}")
        report = ". ".join(parts) + "."
        self.speak(report, wait=True, rate=170)

    def narrate(self, text: str, pause_on_period: float = 0.2):
        """
        Narrate text with natural pauses at sentence boundaries.
        Good for longer text passages.
        """
        import time
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                self.speak(sentence, wait=True)
                time.sleep(pause_on_period)

    def godmode_intro(self):
        """Full God Mode introduction sequence."""
        self.chain(
            "God mode active.",
            "Zero latency.",
            "Absolute precision.",
            "Gabriel online.",
            "All systems green.",
            "Gorunfree.",
            pause=0.4
        )

    def lifeluv_activation(self):
        """AI LIFELUV activation sequence."""
        self.set_style("friendly")
        self.chain(
            "AI LIFELUV online.",
            "Love. Inspiration. Flow. Energy.",
            "Gabriel is ready.",
            "Let's create something amazing.",
            pause=0.5
        )
        self.set_style("normal")

    def mission_brief(self, mission: str, style: str = "authority"):
        """
        Brief the user on a mission.

        Example:
            voice.mission_brief("Deploy the neural network to production")
        """
        old_style = self.style
        self.set_style(style)
        self.chain(
            "Mission accepted.",
            mission,
            "Executing now.",
            pause=0.3
        )
        self.set_style(old_style)

    def alert(self, message: str, level: str = "warning"):
        """
        Speak an alert with appropriate urgency.

        Levels: info, warning, critical
        """
        styles = {
            "info": ("friendly", "Note: "),
            "warning": ("urgent", "Warning. "),
            "critical": ("authority", "Critical alert. "),
        }
        style, prefix = styles.get(level, ("normal", ""))
        old_style = self.style
        self.set_style(style)
        self.speak(prefix + message, wait=True)
        self.set_style(old_style)

    def success(self, task: str = None):
        """Announce success completion."""
        if task:
            self.speak(f"{task} complete.", wait=True)
        else:
            self.announce("success")

    def error(self, message: str = None):
        """Announce an error."""
        self.set_style("authority")
        if message:
            self.speak(f"Error. {message}", wait=True)
        else:
            self.announce("error")
        self.set_style("normal")

    def thinking(self):
        """Announce that GABRIEL is thinking."""
        self.speak("Processing.", wait=False)

    def ready(self):
        """Announce ready state."""
        self.announce("ready")

    def gorunfree(self):
        """The GABRIEL signature sign-off."""
        self.speak("Gorunfree.", wait=True, rate=160)

    # =========================================================================
    # VOICE BLENDER INTEGRATION
    # =========================================================================

    def blend(self, text: str, mode: str = "dual") -> None:
        """
        Speak with voice blending effect.

        Modes:
            dual: Two voices with slight offset
            chorus: Multiple voices simultaneously
            echo: Echo effect with different voices
            cascade: Each word different voice
            god: Full god mode (4+ voices)
            alien: Alien hybrid effect
            neural: Neural AI simulation
            dramatic: Cinematic dramatic intro
        """
        if not self.enabled:
            return

        if mode == "dual":
            blender.blend_dual(text)
        elif mode == "chorus":
            blender.blend_chorus(text)
        elif mode == "echo":
            blender.blend_echo(text)
        elif mode == "cascade":
            blender.blend_cascade(text.split())
        elif mode == "god":
            blender.blend_god_voice(text)
        elif mode == "alien":
            blender.blend_alien_hybrid(text)
        elif mode == "neural":
            blender.blend_neural_simulation(text)
        elif mode == "dramatic":
            blender.blend_dramatic_intro(text)
        else:
            # Default to dual
            blender.blend_dual(text)

    def epic_sequence(self, name: str, **kwargs) -> None:
        """
        Play an epic voice sequence.

        Sequences: boot, godmode, awakening, alert, victory, lifeluv,
                   singularity, battlestation, shutdown
        """
        if not self.enabled:
            return

        if name in EPIC_SEQUENCES:
            seq_func = EPIC_SEQUENCES[name]
            if name == "alert" and "message" in kwargs:
                seq_func(kwargs["message"])
            else:
                seq_func()
        else:
            # Unknown sequence - just speak it
            self.speak(f"Unknown sequence: {name}", wait=True)

    def multi_voice(self, words: List[str], voices: List[str] = None, rate: int = 180) -> None:
        """
        Speak each word with a different voice.

        Example:
            voice.multi_voice(["Systems", "online", "ready"])
        """
        if not self.enabled:
            return
        blender.blend_cascade(words, voices, rate)

    def say_as_god(self, text: str) -> None:
        """Speak with the full god mode voice blend."""
        if not self.enabled:
            return
        blender.blend_god_voice(text)

    def say_with_echo(self, text: str, echoes: int = 3) -> None:
        """Speak with echo effect."""
        if not self.enabled:
            return
        blender.blend_echo(text, echoes=echoes)

    def dramatic_announce(self, text: str) -> None:
        """Make a dramatic announcement with cinematic flair."""
        if not self.enabled:
            return
        blender.blend_dramatic_intro(text)

    def neural_speak(self, text: str) -> None:
        """Speak with neural AI simulation effect."""
        if not self.enabled:
            return
        blender.blend_neural_simulation(text)

    def alien_speak(self, text: str) -> None:
        """Speak with alien/digital hybrid effect."""
        if not self.enabled:
            return
        blender.blend_alien_hybrid(text)

    # =========================================================================
    # MASTER VOICE ENGINE (Triple-layered Winston Voice)
    # =========================================================================

    def master_speak(self, text: str, realtime: bool = False) -> bool:
        """
        Speak with the Master Voice Engine - triple-layered premium British.

        This is the definitive Winston voice:
        - Jamie Premium + OpenAI Onyx + Edge TTS Thomas
        - 3 semitone pitch drop for older, gruffer sound
        - Warm EQ (chest resonance, presence)
        - NO distortion, just clean premium quality

        Args:
            text: Text to speak
            realtime: If True, use faster single-voice mode for low latency

        Returns:
            True if successful
        """
        if not self.enabled:
            return False

        engine = get_master_engine()
        if realtime:
            return engine.realtime(text)
        return engine.speak(text)

    def master_winston(self, text: str = None, category: str = "acknowledge") -> bool:
        """
        Winston-style speech using the Master Voice Engine.

        Args:
            text: Custom text (if None, uses Winston phrase)
            category: Phrase category if text is None

        Returns:
            True if successful
        """
        if not self.enabled:
            return False

        if text is None:
            text = get_winston_phrase(category)

        return self.master_speak(text)

    def master_threat(self, text: str = None) -> bool:
        """Deliver a threat with the Master Voice."""
        if text is None:
            text = get_winston_phrase("threat")
        return self.master_speak(text)

    def master_greet(self, text: str = None) -> bool:
        """Greet with the Master Voice."""
        if text is None:
            text = get_winston_phrase("greet")
        return self.master_speak(text)

    def master_status(self) -> dict:
        """Get Master Voice Engine status."""
        return get_master_engine().status()

    # =========================================================================
    # PRESET EPIC SEQUENCES (Convenience methods)
    # =========================================================================

    def boot(self) -> None:
        """Play the epic boot sequence."""
        self.epic_sequence("boot")

    def activate_godmode(self) -> None:
        """Play god mode activation sequence."""
        self.epic_sequence("godmode")

    def awaken(self) -> None:
        """Play awakening sequence."""
        self.epic_sequence("awakening")

    def celebrate(self) -> None:
        """Play victory/celebration sequence."""
        self.epic_sequence("victory")

    def activate_lifeluv(self) -> None:
        """Play AI LIFELUV activation sequence."""
        self.epic_sequence("lifeluv")

    def singularity(self) -> None:
        """Play the singularity moment."""
        self.epic_sequence("singularity")

    def battlestations(self) -> None:
        """Play battle stations alert."""
        self.epic_sequence("battlestation")

    def shutdown_sequence(self) -> None:
        """Play graceful shutdown sequence."""
        self.epic_sequence("shutdown")


# Module-level singleton
_voice: Optional[GabrielVoice] = None


def get_voice() -> GabrielVoice:
    """Get the global GabrielVoice instance."""
    global _voice
    if _voice is None:
        _voice = GabrielVoice()
    return _voice


def speak(text: str, wait: bool = False) -> bool:
    """Quick speak function using global voice."""
    return get_voice().speak(text, wait=wait)


def announce(event: str, wait: bool = False) -> bool:
    """Quick announce function using global voice."""
    return get_voice().announce(event, wait=wait)


# Module-level Winston shortcut
def winston(text: str = None, category: str = "acknowledge") -> bool:
    """Quick Winston-style speech."""
    return get_voice().winston(text, category)


def speak_effect(text: str, effect: str = "reverb") -> bool:
    """Quick speak with effect."""
    return get_voice().speak_with_effect(text, effect)


# CLI interface
if __name__ == "__main__":
    import sys

    print("╔════════════════════════════════════════════════╗")
    print("║   GABRIEL VOICE X2000 - THE WINSTON EDITION   ║")
    print("║   Oliver (British) + Multi-Backend + Effects  ║")
    print("╠════════════════════════════════════════════════╣")

    voice = GabrielVoice()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == "test":
            print("║ Testing Oliver voice...                       ║")
            voice.test()

        elif cmd == "list":
            print("║ Available macOS voices:                       ║")
            for v in voice.list_voices()[:15]:
                print(f"║   {v:<43} ║")

        elif cmd == "backends":
            print("║ Available backends:                           ║")
            for name, available in voice.list_backends().items():
                status = "YES" if available else "NO"
                print(f"║   {name:<20} {status:>20} ║")

        elif cmd == "effects":
            print("║ Available effects:                            ║")
            for effect in voice.list_effects():
                print(f"║   {effect:<43} ║")

        elif cmd == "greet":
            print("║ Speaking greeting...                          ║")
            voice.greet()

        elif cmd == "winston":
            category = sys.argv[2] if len(sys.argv) > 2 else "acknowledge"
            print(f"║ Winston mode: {category:<31} ║")
            voice.winston(category=category)

        elif cmd == "godmode":
            print("║ God mode speak...                             ║")
            text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "God mode active. Unlimited power."
            voice.godmode_speak(text)

        elif cmd == "radio":
            print("║ Radio effect speak...                         ║")
            text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Incoming transmission."
            voice.radio_speak(text)

        elif cmd == "effect":
            if len(sys.argv) > 3:
                effect = sys.argv[2]
                text = " ".join(sys.argv[3:])
                print(f"║ Effect: {effect:<38} ║")
                voice.speak_with_effect(text, effect)
            else:
                print("║ Usage: python voice.py effect <effect> <text>║")

        elif cmd == "edge":
            print("║ Testing Edge TTS backend...                   ║")
            voice.use_edge_tts()
            voice.speak("This is Gabriel using Microsoft Edge TTS.", wait=True)

        elif cmd == "master":
            print("║ MASTER VOICE ENGINE - Triple-layered Winston  ║")
            print("╠════════════════════════════════════════════════╣")
            status = voice.master_status()
            print(f"║ Jamie Premium: {'YES' if status['jamie_available'] else 'NO':>27} ║")
            print(f"║ OpenAI Onyx:   {'YES' if status['openai_available'] else 'NO':>27} ║")
            print(f"║ Edge Thomas:   {'YES' if status['edge_available'] else 'NO':>27} ║")
            print(f"║ Pitch Drop:    {status['pitch_semitones']} semitones{' ':<20} ║")
            print("╠════════════════════════════════════════════════╣")

            text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
            if text:
                print(f"║ Speaking: {text[:35]:<35} ║")
                voice.master_speak(text)
            else:
                print("║ Demonstrating Master Voice...                 ║")
                voice.master_greet()
                time.sleep(0.5)
                voice.master_threat()

        elif cmd == "realtime":
            print("║ REALTIME Master Voice (low latency)           ║")
            text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Real-time synthesis active."
            print(f"║ Speaking: {text[:35]:<35} ║")

            def progress_callback(pct, status):
                bar = "█" * int(pct * 20) + "░" * (20 - int(pct * 20))
                print(f"║ [{bar}] {status:<20} ║", end="\r")

            get_master_engine().stream_speak(text, callback=progress_callback)
            print()

        elif cmd == "demo":
            print("║ Running full demo...                          ║")
            print("╚════════════════════════════════════════════════╝")
            print()

            print("1. Standard speak:")
            voice.speak("Gabriel Voice X2000 online.", wait=True)
            time.sleep(0.5)

            print("2. Winston greet:")
            voice.winston_greet()
            time.sleep(0.5)

            print("3. Winston threat:")
            voice.winston_threat()
            time.sleep(0.5)

            print("4. God mode effect:")
            voice.godmode_speak("I am the system.")
            time.sleep(0.5)

            print("5. Radio effect:")
            voice.radio_speak("Transmission received.")
            time.sleep(0.5)

            print("6. Winston farewell:")
            voice.winston_farewell()

            print("\nDemo complete. Gorunfree.")
            sys.exit(0)

        elif cmd in PHRASES:
            print(f"║ Announcing: {cmd:<33} ║")
            voice.announce(cmd, wait=True)

        else:
            # Treat as text to speak
            text = " ".join(sys.argv[1:])
            print(f"║ Speaking: {text[:35]:<36} ║")
            voice.speak(text, wait=True)
    else:
        print("║ Usage:                                        ║")
        print("║   python voice.py test                        ║")
        print("║   python voice.py demo       # Full demo      ║")
        print("║   python voice.py list       # macOS voices   ║")
        print("║   python voice.py backends   # List backends  ║")
        print("║   python voice.py effects    # List effects   ║")
        print("║   python voice.py greet                       ║")
        print("║   python voice.py winston [category]          ║")
        print("║   python voice.py godmode [text]              ║")
        print("║   python voice.py radio [text]                ║")
        print("║   python voice.py effect <effect> <text>      ║")
        print("║   python voice.py edge       # Test Edge TTS  ║")
        print("║   python voice.py master [text] # MASTER VOICE║")
        print("║   python voice.py realtime [text] # Low latency║")
        print("║   python voice.py \"Your text here\"            ║")

    print("╚════════════════════════════════════════════════╝")
