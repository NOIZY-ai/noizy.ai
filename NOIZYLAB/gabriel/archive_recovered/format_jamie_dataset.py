import os
import csv

# We need the original phrases to map back to files
PHRASES = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump.",
    "Sphinx of black quartz, judge my vow.",
    "Two driven jocks help fax my big quiz.",
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
    "This is absolutely fascinating! Tell me more.",
    "I'm deeply sorry to hear that. What happened?",
    "Remarkable. Simply remarkable.",
    "Hmm, let me consider that for a moment.",
    "Yes. Yes, I believe you are correct.",
    "No, I'm afraid that won't do at all.",
    "Ha! That reminds me of something amusing.",
    "The fundamental frequency of the human voice varies with age.",
    "Consider the polyrhythmic structures in West African drumming.",
    "In cinema, the rule of thirds guides our visual composition.",
    "A well-crafted algorithm is elegant in its simplicity.",
    "The brain processes language in Broca's and Wernicke's areas.",
    "Throughout my many years, I have discovered that the greatest wisdom lies not in the accumulation of knowledge, but in the thoughtful application of what we have learned. Each conversation is an opportunity to grow, to understand, and to share.",
    "When I walk through the streets of London, I am reminded of my youth. The cobblestones, the architecture, the very air itself speaks of history. And yet, the city evolves, as must we all."
]

DATA_DIR = "/Users/m2ultra/NOIZYLAB/GABRIEL/voice_data/jamie_samples"
METADATA_FILE = os.path.join(DATA_DIR, "metadata.csv")

def format_data():
    print("📝 Formatting dataset metadata...")
    rows = []
    
    # Check existing files
    files = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".wav")])
    if len(files) != len(PHRASES):
        print(f"⚠️  Warning: File count ({len(files)}) does not match phrase count ({len(PHRASES)})")
        # We will map strictly by index assuming order was preserved
    
    with open(METADATA_FILE, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        for i, phrase in enumerate(PHRASES):
            filename = f"jamie_{i+1:03d}.wav"
            if os.path.exists(os.path.join(DATA_DIR, filename)):
                writer.writerow([filename, phrase, "jamie"])
                rows.append((filename, phrase))
            else:
                print(f"❌ Missing: {filename}")
                
    print(f"✅ Created metadata.csv with {len(rows)} entries")
    print(f"📍 Location: {METADATA_FILE}")

if __name__ == "__main__":
    format_data()

# --- APPENDED FOR EXPANSION ---
EXPANDED_PHRASES = [
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

def format_expanded():
    print("📝 Appending expanded metadata...")
    with open(METADATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        for i, phrase in enumerate(EXPANDED_PHRASES):
            # Matches logic in record_expanded_dataset.py (offset 100)
            file_idx = i + 100
            filename = f"jamie_{file_idx:03d}.wav"
            if os.path.exists(os.path.join(DATA_DIR, filename)):
                writer.writerow([filename, phrase, "jamie"])
                print(f"➕ Added metadata: {filename}")
            else:
                print(f"❌ Missing: {filename}")

if __name__ == "__main__":
    format_data()     # Run original logic (001-030)
    format_expanded() # Run specific logic (100-199)
