#!/usr/bin/env python3
"""Record EXPANDED Jamie (Premium) Dataset - 100+ Samples for Professional Cloning"""

import subprocess, os

OUTPUT_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 100+ Phrases covering all phonemes, emotions, and styles
PHRASES = [
    # --- PHYSICAL & SCIENTIFIC (1-10) ---
    "Quantum entanglement suggests a profound interconnectedness in the universe.",
    "The mitochondria is the powerhouse of the cell, generating adenosine triphosphate.",
    "Gravitational waves ripple through the fabric of spacetime itself.",
    "Photosynthesis converts light energy into chemical energy within the chloroplasts.",
    "The human brain contains approximately eighty-six billion neurons.",
    "Plate tectonics drive the slow but constant reshaping of our continents.",
    "Dark matter accounts for approximately eighty-five percent of the matter in the universe.",
    "The Doppler effect explains the change in frequency of a wave for an observer.",
    "Thermodynamics dictates that entropy in an isolated system always increases.",
    "DNA replication is the biological process of producing two identical replicas of DNA.",

    # --- EMOTIONAL & DRAMATIC (11-20) ---
    "I cannot believe you would say something so utterly heartless!",
    "It is with a heavy heart that I must deliver this devastating news.",
    "Oh, the absolute joy of seeing the sunrise over the mountains!",
    "I am terrified of what might be lurking in the shadows.",
    "This is the most magnificent achievement of my entire life!",
    "Why must we always fight about things that do not verify matter?",
    "I feel a profound sense of peace when I walk through the forest.",
    "The grief was overwhelming, crashing over him like a tidal wave.",
    "Victory! We have finally succeeded against all odds!",
    "I am so incredibly proud of everything you have accomplished.",

    # --- NARRATIVE & STORYTELLING (21-30) ---
    "Once upon a time, in a kingdom far away, there lived a wise old king.",
    "The detective stepped into the dimly lit room, scanning for clues.",
    "The spaceship glided silently through the asteroid field, dodging debris.",
    "She opened the ancient book, and dust motes danced in the shaft of light.",
    "The wind howled outside the cabin, shaking the windows in their frames.",
    "He watched the stranger approach from across the crowded marketplace.",
    "The dragon awoke from its slumber, smoke curling from its nostrils.",
    "It was a dark and stormy night, and the rain lashed against the roof.",
    "The secret map led them deep into the heart of the forbidden jungle.",
    "As the clock struck midnight, the magic spell began to fade away.",

    # --- CONVERSATIONAL (31-40) ---
    "Could you please pass the salt? Thank you very much.",
    "I was thinking we could grab some coffee later this afternoon.",
    "What do you think about the new project proposal?",
    "I'm not sure if I can make it to the meeting on time today.",
    "That sounds like a wonderful idea, let's definitely do that.",
    "Have you heard the latest news from the research department?",
    "I really appreciate your help with this difficult task.",
    "Do you have a moment to discuss the budget for next quarter?",
    "I'm afraid I have to disagree with your assessment of the situation.",
    "Let's touch base again tomorrow morning to finalize the details.",

    # --- PHONETIC PANAGRAMS (41-50) ---
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump.",
    "Sphinx of black quartz, judge my vow.",
    "Two driven jocks help fax my big quiz.",
    "Five quacking zephyrs jolt my wax bed.",
    "The five boxing wizards jump quickly.",
    "Jackdaws love my big sphinx of quartz.",
    "Mr. Jock, TV quiz PhD, bags few lynx.",
    "Crazy Fredrick bought many very exquisite opal jewels.",

    # --- TECHNICAL & CODING (51-60) ---
    "Initialize the variable with a default floating-point value.",
    "The function returns a boolean indicating success or failure.",
    "Iterate through the array using a standard for-loop structure.",
    "Caught an unhandled exception in the main execution thread.",
    "Compiling the source code generated several warning messages.",
    "The database query returned zero rows matching the criteria.",
    "Implement the interface to ensure polymorphic behavior.",
    "Maximize the window to view the full terminal output.",
    "Recursion depth exceeded the maximum stack size limit.",
    "Deploy the application to the staging environment for testing.",

    # --- PHILOSOPHICAL (61-70) ---
    "To be, or not to be, that is the literal question.",
    "I think, therefore I am, said the philosopher Descartes.",
    "The unexamined life is not worth living for a human being.",
    "Man is born free, and everywhere he is in chains.",
    "Happiness depends upon ourselves, according to Aristotle.",
    "The only true wisdom is in knowing you know nothing.",
    "He who has a why to live can bear almost any how.",
    "Life is what happens when you're busy making other plans.",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
    "In the midst of chaos, there is also opportunity.",

    # --- FAST & SLOW (71-80) ---
    "This-sentence-is-spoken-very-quickly-to-test-speed.",
    "Sloooow... doooown... eeeevery... wooooord... caaaarefully.",
    "Hurry up! We function on a very tight schedule here!",
    "Take... your... time... there... is... no... rush.",
    "Rapid fire questions require rapid fire answers immediately.",
    "Pause. Breathe. Reflect. Then proceed with caution.",
    "Accelerate the vehicle to maximum velocity right now!",
    "Drifting slowly through the endless void of space.",
    "Sprint potential is maximized by explosive muscle fibers.",
    "Lethargy crept into his limbs, making movement difficult.",

    # --- NEWSCASTER STYLE (81-90) ---
    "Breaking news tonight: a major breakthrough in renewable energy.",
    "Stocks closed higher today as the market responded to positive data.",
    "Weather forecast for the weekend calls for sunny skies and warm temperatures.",
    "Local authorities are advising residents to stay indoors due to the storm.",
    "In sports, the home team secured a decisive victory in the playoffs.",
    "The international summit concluded with a historic agreement.",
    "Traffic is backed up on the main highway due to an earlier accident.",
    "Scientists have discovered a new species of deep-sea marine life.",
    "The economy shows signs of recovery after a period of stagnation.",
    "Stay tuned for more updates on this developing story at eleven.",

    # --- DR. GABRIEL ALMEIDA SPECIFIC (91-100) ---
    "My dear friend, welcome back to the Dreamchamber.",
    "I have analyzed the data and the results are quite intriguing.",
    "Let us delve deeper into the mysteries of this codebase.",
    "Optimization is not just a goal, it is a way of life.",
    "The neural network is performing within expected parameters.",
    "I am re-routing the power couplings to the main drive.",
    "Accessing the mainframe archive. decrypting security protocols.",
    "Scanning for vulnerabilities. Please stand by for results.",
    "System integrity is at one hundred percent efficient capacity.",
    "I am Gabriel. I am the voice of the system. I am here to serve."
]

def record_phrase(text, index):
    # Determine absolute index (offset by existing 30 files if needed, but we'll overwrite/extend 101-200)
    # Actually, let's just use 100+ numbering to not conflict with previous 30
    file_idx = index + 100 
    filename = f"{OUTPUT_DIR}/jamie_{file_idx:03d}.aiff"
    wav_file = f"{OUTPUT_DIR}/jamie_{file_idx:03d}.wav"
    
    # Generate with Jamie Premium
    subprocess.run(["say", "-v", "Jamie (Premium)", "-r", "145", text, "-o", filename])
    
    # Convert to WAV (22050Hz mono is ideal for XTTS)
    subprocess.run([
        "ffmpeg", "-y", "-i", filename, "-ar", "22050", "-ac", "1", wav_file
    ], capture_output=True)
    
    print(f"✅ Recorded: jamie_{file_idx:03d}")
    return wav_file

def main():
    print("🎙️  RECORDING MASSIVE DATASET EXPANSION")
    print("=" * 50)
    
    for i, phrase in enumerate(PHRASES):
        record_phrase(phrase, i)
        
    print("=" * 50)
    print(f"✅ Added {len(PHRASES)} new high-quality samples.")
    print(f"📁 Total Dataset Location: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
