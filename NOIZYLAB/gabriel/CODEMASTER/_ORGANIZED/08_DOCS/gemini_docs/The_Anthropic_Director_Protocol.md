# THE SUPER-SONIC ANTHROPIC GENIUS PROTOCOL
**Role**: Creative Director & Assistive Intelligence
**Engine**: Claude 3.5 Sonnet

## 1. THE CONCEPT
We do not just use AI to *make* the asset. We use Anthropic to *dream* the asset, and then use our local heavyweights (FFmpeg, AudioCraft) to forge it.

## 2. THE WORKFLOW

### PHASE 1: LISTENING (The Ears)
*   **Tool**: `noizy_cortex.py`
*   **Action**: Extracts the mathematical DNA of the song (Key, BPM, Emotion).
*   **Output**: JSON Telemetry.

### PHASE 2: DREAMING (The Brain)
*   **Tool**: `anthropic_director.py`
*   **Action**: Claude 3.5 Sonnet reads the telemetry.
*   **Creative Output**:
    *   "The song is D Minor, 140 BPM, High Energy."
    *   "Director's Vision: Cyberpunk strobe lights, cut every 0.42 seconds (matching BPM)."
    *   **Generates Prompts**: Writes the specific text prompts for Sora/Veo/MusicGen.

### PHASE 3: EXECUTION (The Hands)
*   **Video**: Feed Claude's prompts into Google Veo or OpenAI Sora.
*   **Edit**: Use `noizy_cinema.py` to auto-cut the video based on the BPM calculated in Phase 1.
*   **Remix**: Use `noizy_separator.py` (Spleeter) to isolate the vocals if Claude suggests a "Vocal-only breakdown."

## 3. HOW TO ACTIVATE
1.  **Export Key**: `export ANTHROPIC_API_KEY='sk-...'`
2.  **Run Director**: `python3 anthropic_director.py my_song.mp3`
3.  **Read Brief**: Open `my_song.mp3_DIRECTOR_BRIEF.md` and follow the genius instructions.
