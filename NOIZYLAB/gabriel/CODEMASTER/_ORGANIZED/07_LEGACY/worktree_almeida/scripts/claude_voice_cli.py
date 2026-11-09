#!/usr/bin/env python3
"""
🎙️ Claude Voice CLI - NOIZYVOX Edition
Enhanced Claude CLI with Speech-to-Text and Text-to-Speech integration.

Features:
- Voice input (speak your prompt)
- Voice output (hear Claude's response)  
- Text input/output (traditional mode)
- Save audio files
- Multiple voice options
- Streaming support

Usage:
  # Text mode (traditional)
  python claude_voice_cli.py "Explain quantum computing"
  
  # Voice input (speak your prompt)
  python claude_voice_cli.py --voice-in
  
  # Voice output (hear response)
  python claude_voice_cli.py "Tell me a joke" --voice-out
  
  # Full voice mode (speak + hear)
  python claude_voice_cli.py --voice-in --voice-out
  
  # Save audio response
  python claude_voice_cli.py "Hello world" --voice-out --save-audio response.mp3
  
  # Choose voice
  python claude_voice_cli.py "Hello" --voice-out --voice nova
  
  # Batch mode with voice output
  python claude_voice_cli.py --file prompts.txt --voice-out --output-dir ./responses/

Requirements:
  pip install anthropic openai sounddevice soundfile numpy pyaudio
"""

import argparse
import os
import sys
import json
import tempfile
import wave
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple

# Check for required packages
MISSING_PACKAGES = []

try:
    import anthropic
except ImportError:
    MISSING_PACKAGES.append("anthropic")

try:
    import openai
except ImportError:
    MISSING_PACKAGES.append("openai")

try:
    import sounddevice as sd
except ImportError:
    MISSING_PACKAGES.append("sounddevice")

try:
    import soundfile as sf
except ImportError:
    MISSING_PACKAGES.append("soundfile")

try:
    import numpy as np
except ImportError:
    MISSING_PACKAGES.append("numpy")

if MISSING_PACKAGES:
    print(f"⚠️  Missing packages: {', '.join(MISSING_PACKAGES)}")
    print(f"   Run: pip install {' '.join(MISSING_PACKAGES)}")
    # Continue anyway for help/version commands

# =============================================================================
# Configuration
# =============================================================================

# API Keys (from environment)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Default models
DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"  # Instruction-guided TTS
DEFAULT_ASR_MODEL = "gpt-4o-mini-transcribe"  # Fast, cost-efficient
DEFAULT_VOICE = "nova"  # Friendly, upbeat

# Available voices
OPENAI_VOICES = {
    "alloy": "Neutral, balanced - General narration",
    "ash": "Clear, professional - Business content",
    "ballad": "Lyrical, expressive - Storytelling",
    "coral": "Warm, engaging - Marketing",
    "echo": "Warm, conversational - Podcasts",
    "fable": "Expressive, dramatic - Audiobooks",
    "nova": "Friendly, upbeat - Customer service",
    "onyx": "Deep, authoritative - Documentaries",
    "sage": "Wise, measured - Educational",
    "shimmer": "Soft, soothing - Meditation",
    "verse": "Poetic, rhythmic - Artistic"
}

# Audio settings
SAMPLE_RATE = 16000  # 16kHz for ASR
CHANNELS = 1
RECORD_SECONDS_DEFAULT = 10
SILENCE_THRESHOLD = 0.01
SILENCE_DURATION = 1.5  # seconds of silence to stop recording

# =============================================================================
# Claude Integration
# =============================================================================

def call_claude(
    prompt: str,
    model: str = DEFAULT_CLAUDE_MODEL,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None,
    stream: bool = False
) -> str:
    """Call Claude API and return response."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    messages = [{"role": "user", "content": prompt}]
    
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    
    if temperature is not None:
        kwargs["temperature"] = temperature
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    if stream:
        response_text = ""
        with client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                response_text += text
        print()  # newline after stream
        return response_text
    else:
        response = client.messages.create(**kwargs)
        return response.content[0].text

# =============================================================================
# Speech-to-Text (Voice Input)
# =============================================================================

def record_audio(
    duration: Optional[float] = None,
    auto_stop: bool = True,
    sample_rate: int = SAMPLE_RATE
) -> np.ndarray:
    """
    Record audio from microphone.
    
    Args:
        duration: Fixed recording duration (seconds). If None, uses auto-stop.
        auto_stop: Stop recording after silence detected.
        sample_rate: Audio sample rate.
    
    Returns:
        numpy array of audio data
    """
    print("🎤 Recording... (speak now, silence will stop recording)")
    
    if duration:
        # Fixed duration recording
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=CHANNELS,
            dtype='float32'
        )
        sd.wait()
        print("✅ Recording complete")
        return audio.flatten()
    
    # Auto-stop recording based on silence
    audio_chunks = []
    silence_counter = 0
    chunk_duration = 0.1  # 100ms chunks
    chunk_samples = int(sample_rate * chunk_duration)
    max_duration = 60  # Maximum 60 seconds
    total_samples = 0
    
    try:
        with sd.InputStream(samplerate=sample_rate, channels=CHANNELS, dtype='float32') as stream:
            while total_samples < max_duration * sample_rate:
                chunk, _ = stream.read(chunk_samples)
                audio_chunks.append(chunk.flatten())
                total_samples += chunk_samples
                
                # Check for silence
                rms = np.sqrt(np.mean(chunk**2))
                if rms < SILENCE_THRESHOLD:
                    silence_counter += chunk_duration
                    if silence_counter >= SILENCE_DURATION and total_samples > sample_rate:
                        # At least 1 second recorded before stopping
                        break
                else:
                    silence_counter = 0
                    
    except KeyboardInterrupt:
        pass
    
    print("✅ Recording complete")
    return np.concatenate(audio_chunks) if audio_chunks else np.array([])


def save_audio_to_file(audio: np.ndarray, filepath: str, sample_rate: int = SAMPLE_RATE):
    """Save audio array to file."""
    sf.write(filepath, audio, sample_rate)


def transcribe_audio(
    audio: np.ndarray,
    model: str = DEFAULT_ASR_MODEL,
    language: Optional[str] = None
) -> str:
    """
    Transcribe audio using OpenAI's ASR.
    
    Args:
        audio: numpy array of audio data
        model: ASR model to use
        language: Optional language code (e.g., 'en')
    
    Returns:
        Transcribed text
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Save audio to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = f.name
        sf.write(temp_path, audio, SAMPLE_RATE)
    
    try:
        with open(temp_path, "rb") as audio_file:
            kwargs = {
                "model": model,
                "file": audio_file,
            }
            if language:
                kwargs["language"] = language
            
            transcript = client.audio.transcriptions.create(**kwargs)
        
        return transcript.text
    finally:
        os.unlink(temp_path)


def voice_input(
    duration: Optional[float] = None,
    model: str = DEFAULT_ASR_MODEL,
    language: Optional[str] = None,
    save_recording: Optional[str] = None
) -> str:
    """
    Record voice and transcribe to text.
    
    Args:
        duration: Fixed recording duration (None for auto-stop)
        model: ASR model
        language: Language code
        save_recording: Optional path to save recording
    
    Returns:
        Transcribed text
    """
    # Record audio
    audio = record_audio(duration=duration)
    
    if len(audio) == 0:
        raise ValueError("No audio recorded")
    
    # Save recording if requested
    if save_recording:
        save_audio_to_file(audio, save_recording)
        print(f"💾 Recording saved to: {save_recording}")
    
    # Transcribe
    print("📝 Transcribing...")
    text = transcribe_audio(audio, model=model, language=language)
    print(f"📝 You said: {text}")
    
    return text

# =============================================================================
# Text-to-Speech (Voice Output)
# =============================================================================

def text_to_speech(
    text: str,
    model: str = DEFAULT_TTS_MODEL,
    voice: str = DEFAULT_VOICE,
    instructions: Optional[str] = None,
    output_path: Optional[str] = None,
    play_audio: bool = True
) -> Optional[bytes]:
    """
    Convert text to speech using OpenAI's TTS.
    
    Args:
        text: Text to speak
        model: TTS model
        voice: Voice preset
        instructions: Voice instructions (for gpt-4o-mini-tts)
        output_path: Optional path to save audio
        play_audio: Whether to play the audio
    
    Returns:
        Audio bytes if not playing
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Build request
    kwargs = {
        "model": model,
        "voice": voice,
        "input": text,
        "response_format": "mp3"
    }
    
    # Add instructions for instruction-guided TTS
    if instructions and model == "gpt-4o-mini-tts":
        kwargs["instructions"] = instructions
    
    print(f"🔊 Generating speech with voice '{voice}'...")
    response = client.audio.speech.create(**kwargs)
    
    audio_content = response.content
    
    # Save to file if requested
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_content)
        print(f"💾 Audio saved to: {output_path}")
    
    # Play audio
    if play_audio:
        play_audio_bytes(audio_content)
    
    return audio_content


def play_audio_bytes(audio_bytes: bytes):
    """Play audio from bytes (MP3 format)."""
    # Save to temp file and play
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = f.name
        f.write(audio_bytes)
    
    try:
        # Try using soundfile + sounddevice
        data, sample_rate = sf.read(temp_path)
        print("🔊 Playing response...")
        sd.play(data, sample_rate)
        sd.wait()
        print("✅ Playback complete")
    except Exception as e:
        # Fallback to system player
        print(f"⚠️  Falling back to system player: {e}")
        import subprocess
        if sys.platform == "darwin":  # macOS
            subprocess.run(["afplay", temp_path], check=True)
        elif sys.platform == "linux":
            subprocess.run(["aplay", temp_path], check=True)
        elif sys.platform == "win32":
            subprocess.run(["start", temp_path], shell=True, check=True)
    finally:
        os.unlink(temp_path)

# =============================================================================
# Batch Processing
# =============================================================================

def process_batch(
    prompts_file: str,
    output_file: Optional[str] = None,
    output_dir: Optional[str] = None,
    voice_out: bool = False,
    voice: str = DEFAULT_VOICE,
    model: str = DEFAULT_CLAUDE_MODEL,
    max_tokens: int = 4096,
    temperature: float = 0.7
) -> List[Tuple[str, str]]:
    """
    Process batch of prompts from file.
    
    Args:
        prompts_file: Path to file with prompts (one per line)
        output_file: CSV output file
        output_dir: Directory for audio files
        voice_out: Generate audio responses
        voice: Voice preset
        model: Claude model
        max_tokens: Max tokens
        temperature: Temperature
    
    Returns:
        List of (prompt, response) tuples
    """
    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]
    
    results = []
    
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n📝 Processing prompt {i}/{len(prompts)}: {prompt[:50]}...")
        
        try:
            response = call_claude(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
            results.append((prompt, response))
            
            if voice_out:
                audio_path = None
                if output_dir:
                    audio_path = os.path.join(output_dir, f"response_{i:03d}.mp3")
                text_to_speech(response, voice=voice, output_path=audio_path, play_audio=False)
            
            print(f"✅ Response: {response[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((prompt, f"ERROR: {e}"))
    
    # Save to CSV if requested
    if output_file:
        import csv
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["prompt", "response"])
            writer.writerows(results)
        print(f"\n💾 Results saved to: {output_file}")
    
    return results

# =============================================================================
# Interactive Mode
# =============================================================================

def interactive_mode(
    voice_in: bool = False,
    voice_out: bool = False,
    voice: str = DEFAULT_VOICE,
    model: str = DEFAULT_CLAUDE_MODEL,
    system_prompt: Optional[str] = None
):
    """Run interactive conversation mode."""
    print("\n🎙️ Claude Voice CLI - Interactive Mode")
    print("=" * 50)
    print(f"Model: {model}")
    print(f"Voice Input: {'✅ Enabled' if voice_in else '❌ Disabled'}")
    print(f"Voice Output: {'✅ Enabled' if voice_out else '❌ Disabled'}")
    if voice_out:
        print(f"Voice: {voice}")
    print("\nCommands: 'quit' to exit, 'voice' to toggle voice output")
    print("=" * 50)
    
    while True:
        try:
            if voice_in:
                print("\n🎤 Press Enter to start recording (or type 'quit' to exit):")
                user_input = input().strip()
                if user_input.lower() == 'quit':
                    break
                if user_input.lower() == 'voice':
                    voice_out = not voice_out
                    print(f"Voice output: {'✅ Enabled' if voice_out else '❌ Disabled'}")
                    continue
                
                prompt = voice_input()
            else:
                prompt = input("\n💬 You: ").strip()
                if not prompt:
                    continue
                if prompt.lower() == 'quit':
                    break
                if prompt.lower() == 'voice':
                    voice_out = not voice_out
                    print(f"Voice output: {'✅ Enabled' if voice_out else '❌ Disabled'}")
                    continue
            
            print("\n🤖 Claude: ", end="")
            response = call_claude(prompt, model=model, system_prompt=system_prompt, stream=True)
            
            if voice_out:
                text_to_speech(response, voice=voice)
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

# =============================================================================
# Main CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🎙️ Claude Voice CLI - NOIZYVOX Edition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text mode
  %(prog)s "Explain quantum computing"
  
  # Voice input (speak your prompt)
  %(prog)s --voice-in
  
  # Voice output (hear response)
  %(prog)s "Tell me a joke" --voice-out
  
  # Full voice conversation
  %(prog)s --voice-in --voice-out --interactive
  
  # Save audio response
  %(prog)s "Hello world" --voice-out --save-audio response.mp3
  
  # Choose voice
  %(prog)s "Hello" --voice-out --voice shimmer
  
  # Batch processing
  %(prog)s --file prompts.txt --output responses.csv
  
  # List available voices
  %(prog)s --list-voices

Environment Variables:
  ANTHROPIC_API_KEY  - Your Anthropic API key
  OPENAI_API_KEY     - Your OpenAI API key (for voice features)
"""
    )
    
    # Prompt argument
    parser.add_argument("prompt", nargs="?", help="Prompt to send to Claude")
    
    # Claude options
    parser.add_argument("--model", "-m", default=DEFAULT_CLAUDE_MODEL,
                        help=f"Claude model (default: {DEFAULT_CLAUDE_MODEL})")
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="Max tokens in response (default: 4096)")
    parser.add_argument("--temperature", "-t", type=float, default=0.7,
                        help="Temperature (default: 0.7)")
    parser.add_argument("--system", "-s", help="System prompt")
    parser.add_argument("--stream", action="store_true", help="Stream response")
    
    # Voice input options
    parser.add_argument("--voice-in", "-vi", action="store_true",
                        help="Use voice input (speak your prompt)")
    parser.add_argument("--record-duration", type=float,
                        help="Fixed recording duration in seconds")
    parser.add_argument("--asr-model", default=DEFAULT_ASR_MODEL,
                        help=f"ASR model (default: {DEFAULT_ASR_MODEL})")
    parser.add_argument("--language", "-l", help="Language code for ASR (e.g., 'en')")
    parser.add_argument("--save-recording", help="Save voice recording to file")
    
    # Voice output options
    parser.add_argument("--voice-out", "-vo", action="store_true",
                        help="Use voice output (hear response)")
    parser.add_argument("--voice", "-v", default=DEFAULT_VOICE,
                        choices=list(OPENAI_VOICES.keys()),
                        help=f"Voice preset (default: {DEFAULT_VOICE})")
    parser.add_argument("--tts-model", default=DEFAULT_TTS_MODEL,
                        help=f"TTS model (default: {DEFAULT_TTS_MODEL})")
    parser.add_argument("--voice-instructions", help="Voice instructions (for gpt-4o-mini-tts)")
    parser.add_argument("--save-audio", help="Save audio response to file")
    parser.add_argument("--no-play", action="store_true", help="Don't play audio (just save)")
    
    # Batch options
    parser.add_argument("--file", "-f", help="File with prompts (one per line)")
    parser.add_argument("--output", "-o", help="Output CSV file for batch mode")
    parser.add_argument("--output-dir", help="Output directory for audio files")
    
    # Interactive mode
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive conversation mode")
    
    # Utility
    parser.add_argument("--list-voices", action="store_true",
                        help="List available voices")
    parser.add_argument("--version", action="version", version="Claude Voice CLI 1.0.0")
    
    args = parser.parse_args()
    
    # List voices
    if args.list_voices:
        print("\n🎤 Available Voices:")
        print("=" * 60)
        for voice, desc in OPENAI_VOICES.items():
            marker = "→" if voice == DEFAULT_VOICE else " "
            print(f" {marker} {voice:10} - {desc}")
        print("\n💡 Use --voice <name> to select a voice")
        return
    
    # Check for missing packages
    if MISSING_PACKAGES:
        if args.voice_in or args.voice_out:
            print(f"❌ Voice features require: pip install {' '.join(MISSING_PACKAGES)}")
            sys.exit(1)
    
    # Interactive mode
    if args.interactive:
        interactive_mode(
            voice_in=args.voice_in,
            voice_out=args.voice_out,
            voice=args.voice,
            model=args.model,
            system_prompt=args.system
        )
        return
    
    # Batch mode
    if args.file:
        process_batch(
            prompts_file=args.file,
            output_file=args.output,
            output_dir=args.output_dir,
            voice_out=args.voice_out,
            voice=args.voice,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature
        )
        return
    
    # Get prompt
    prompt = args.prompt
    
    # Voice input
    if args.voice_in:
        prompt = voice_input(
            duration=args.record_duration,
            model=args.asr_model,
            language=args.language,
            save_recording=args.save_recording
        )
    
    if not prompt:
        parser.print_help()
        return
    
    # Call Claude
    print("\n🤖 Claude: ", end="" if args.stream else "\n")
    response = call_claude(
        prompt,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        system_prompt=args.system,
        stream=args.stream
    )
    
    if not args.stream:
        print(response)
    
    # Voice output
    if args.voice_out:
        text_to_speech(
            response,
            model=args.tts_model,
            voice=args.voice,
            instructions=args.voice_instructions,
            output_path=args.save_audio,
            play_audio=not args.no_play
        )


if __name__ == "__main__":
    main()
