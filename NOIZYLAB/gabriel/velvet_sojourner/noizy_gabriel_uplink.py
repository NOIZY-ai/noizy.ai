import sys
import os
import socket
import subprocess
import time
import warnings
from noizy_memcell import memory_core

# Suppress FP16 warning
warnings.filterwarnings("ignore")

try:
    import whisper
except ImportError:
    print("!!! ERROR: Whisper missing. Run pip install openai-whisper")
    sys.exit(1)

# NOIZYLAB GABRIEL UPLINK v1.0
# "The Preacher" Module: Voice-to-Gabriel Transmission
# TARGET: GABRIEL (HP-OMEN) @ 10.90.90.91
# PROTOCOL: TCP 9999 "THE WORD"

GABRIEL_IP = "10.90.90.91"
GABRIEL_PORT = 9999
CHUNK_DURATION = 10 # Seconds per sermon chunk

def record_chunk(filename, duration):
    print(f"\n>>> [PREACHER] RECORDING SERMON ({duration}s)...")
    # Quick FFmpeg capture from default mic
    # macOS: -f avfoundation -i ":0" is typical default mic
    cmd = [
        "ffmpeg", "-y", "-f", "avfoundation", "-i", ":0",
        "-t", str(duration), "-ac", "1", "-ar", "16000",
        "-v", "quiet", filename
    ]
    subprocess.run(cmd)

def transmit_word(text):
    print(f">>> [UPLINK] BEAMING TO GABRIEL ({GABRIEL_IP})...")
    try:
        # Fire and forget TCP packet
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((GABRIEL_IP, GABRIEL_PORT))
            payload = f"SERMON|{text}".encode('utf-8')
            s.sendall(payload)
            print("    -> WORD RECEIVED.")
            memory_core.log_interaction(f"Preached to Gabriel: {text[:30]}...", "UPLINK_SUCCESS", "SHIRL")
    except Exception as e:
        print(f"!!! GABRIEL IS DEAF: {e}")
        # Log it anyway, maybe he hears in spirit
        memory_core.log_interaction(f"Preached (Gabriel Offline): {text[:30]}...", "UPLINK_FAIL", "SHIRL")

def preach_session():
    print(f"NOIZY GABRIEL UPLINK v1.0 | TARGET: {GABRIEL_IP}")
    print(">>> PREPARING THE ALTAR...")
    
    model = whisper.load_model("base")
    chunk_file = "temp_sermon.wav"
    
    try:
        while True:
            # 1. Record
            record_chunk(chunk_file, CHUNK_DURATION)
            
            # 2. Transcribe
            if os.path.exists(chunk_file):
                print("    -> TRANSCRIBING REVELATION...")
                result = model.transcribe(chunk_file)
                text = result["text"].strip()
                
                if text:
                    print(f"    -> \"{text}\"")
                    # 3. Transmit
                    transmit_word(text)
                else:
                    print("    -> (Silence)")
            
            # Zero Latency Loop
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n>>> PREACHING CONCLUDED.")
        if os.path.exists(chunk_file): os.remove(chunk_file)

if __name__ == "__main__":
    preach_session()
