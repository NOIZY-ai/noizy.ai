#!/usr/bin/env python3
"""
GABRIEL VOICE UPLINK - Voice-to-GABRIEL Transmission
"The Preacher" Module
TARGET: GABRIEL (HP-OMEN) @ VPN 10.100.0.2 or LAN 10.0.0.160
PROTOCOL: TCP 9999 "THE WORD"
"""

import sys
import os
import socket
import subprocess
import time
import warnings

# Suppress FP16 warning
warnings.filterwarnings("ignore")

# Configuration
GABRIEL_VPN_IP = "10.100.0.2"
GABRIEL_LAN_IP = "10.0.0.160"
GABRIEL_PORT = 9999
CHUNK_DURATION = 10  # Seconds per sermon chunk

def get_gabriel_ip():
    """Determine which IP to use for GABRIEL"""
    for ip in [GABRIEL_VPN_IP, GABRIEL_LAN_IP]:
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-t", "2", ip],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return ip
        except:
            pass
    return GABRIEL_VPN_IP  # Default to VPN

def record_chunk(filename, duration):
    """Record audio chunk from microphone"""
    print(f"\n>>> [PREACHER] RECORDING SERMON ({duration}s)...")
    # macOS: -f avfoundation -i ":0" is typical default mic
    cmd = [
        "ffmpeg", "-y", "-f", "avfoundation", "-i", ":0",
        "-t", str(duration), "-ac", "1", "-ar", "16000",
        "-v", "quiet", filename
    ]
    subprocess.run(cmd)

def transmit_word(text, gabriel_ip):
    """Transmit transcribed text to GABRIEL"""
    print(f">>> [UPLINK] BEAMING TO GABRIEL ({gabriel_ip})...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((gabriel_ip, GABRIEL_PORT))
            payload = f"SERMON|{text}".encode('utf-8')
            s.sendall(payload)
            print("    -> WORD RECEIVED.")
            return True
    except Exception as e:
        print(f"!!! GABRIEL IS DEAF: {e}")
        return False

def preach_session():
    """Main preaching session loop"""
    try:
        import whisper
    except ImportError:
        print("!!! ERROR: Whisper missing. Run: pip install openai-whisper")
        sys.exit(1)

    gabriel_ip = get_gabriel_ip()
    print(f"GABRIEL VOICE UPLINK v1.0 | TARGET: {gabriel_ip}")
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
                    transmit_word(text, gabriel_ip)
                else:
                    print("    -> (Silence)")

            # Zero Latency Loop
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n>>> PREACHING CONCLUDED.")
        if os.path.exists(chunk_file):
            os.remove(chunk_file)

if __name__ == "__main__":
    preach_session()
