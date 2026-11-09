#!/usr/bin/env python3
"""Record Jamie (Premium) speaking comprehensive phrases for voice cloning"""

import subprocess
import os

OUTPUT_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Comprehensive text corpus for voice cloning (needs ~5-30 minutes of audio)
PHRASES = [
    # Phonetically diverse sentences
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump.",
    "Sphinx of black quartz, judge my vow.",
    "Two driven jocks help fax my big quiz.",
    
    # Character-specific (Dr. Gabriel Almeida)
    "Good morning, my friend. Welcome to my study.",
    "After decades at Cambridge, one learns to appreciate precision.",
    "Music and mathematics share the same fundamental beauty.",
    "When I founded the Berklee program, we focused on creativity first.",
    "A fine Rioja pairs wonderfully with contemplation.",
    "Every great film tells a story that words alone cannot convey.",
    "Coding is simply the art of precise expression.",
    "I have read every book worth reading, and many that were not.",
    "Wisdom comes not from knowing everything, but from knowing what matters.",
    "Let me share a story from my years in London.",
    "Spain taught me passion. Cambridge taught me precision. Life taught me balance.",
    
    # Emotional range
    "This is absolutely fascinating! Tell me more.",
    "I'm deeply sorry to hear that. What happened?",
    "Remarkable. Simply remarkable.",
    "Hmm, let me consider that for a moment.",
    "Yes. Yes, I believe you are correct.",
    "No, I'm afraid that won't do at all.",
    "Ha! That reminds me of something amusing.",
    
    # Technical/educational
    "The fundamental frequency of the human voice varies with age.",
    "Consider the polyrhythmic structures in West African drumming.",
    "In cinema, the rule of thirds guides our visual composition.",
    "A well-crafted algorithm is elegant in its simplicity.",
    "The brain processes language in Broca's and Wernicke's areas.",
    
    # Long passages for prosody learning
    """Throughout my many years, I have discovered that the greatest 
    wisdom lies not in the accumulation of knowledge, but in the 
    thoughtful application of what we have learned. Each conversation 
    is an opportunity to grow, to understand, and to share.""",
    
    """When I walk through the streets of London, I am reminded of 
    my youth. The cobblestones, the architecture, the very air itself 
    speaks of history. And yet, the city evolves, as must we all.""",
]

def record_phrase(text, index):
    filename = f"{OUTPUT_DIR}/jamie_{index:03d}.aiff"
    wav_file = f"{OUTPUT_DIR}/jamie_{index:03d}.wav"
    
    # Generate with Jamie Premium at conversational rate
    subprocess.run([
        "say", "-v", "Jamie (Premium)", "-r", "145", text, "-o", filename
    ])
    
    # Convert to WAV for compatibility
    subprocess.run([
        "ffmpeg", "-y", "-i", filename, wav_file
    ], capture_output=True)
    
    print(f"✅ Recorded: jamie_{index:03d} ({len(text)} chars)")
    return wav_file

def main():
    print("🎤 Recording Jamie (Premium) Voice Dataset")
    print("=" * 50)
    
    total_duration = 0
    for i, phrase in enumerate(PHRASES, 1):
        wav = record_phrase(phrase, i)
        # Estimate: ~150 words/minute at rate 145
        words = len(phrase.split())
        duration = words / 2.4  # seconds
        total_duration += duration
    
    print("=" * 50)
    print(f"✅ Recorded {len(PHRASES)} phrases")
    print(f"📊 Estimated total: {total_duration/60:.1f} minutes")
    print(f"📁 Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
