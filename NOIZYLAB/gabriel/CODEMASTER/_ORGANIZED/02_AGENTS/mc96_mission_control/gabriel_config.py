# GABRIEL CONFIGURATION - SYSTEM IDENTITY CARD
import os

YOUTUBE_IDENTITY = {"USER_ID": "PASTE_USER_ID_HERE", "CHANNEL_ID": "PASTE_CHANNEL_ID_HERE", "BROADCAST_NAME": "Gabriel [AI]", "MODERATION_THRESHOLD": 0.85}

API_KEYS = {"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""), "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY", "")}

OPENAI_CONFIG = {"REASONING_MODEL": "gpt-5.2", "REALTIME_MODEL": "gpt-5.2-realtime-2025-12-15", "VOICE_ID": "cedar", "REASONING_EFFORT": "high"}

PATHS = {"RAM_DISK": "/Volumes/GabrielVol/", "MEMCELL": "/Volumes/GabrielVol/memcell.msgpack", "MODELS": "/Volumes/GabrielVol/models/", "NKI_ROOT": "/Volumes/JOE/NKI", "PORTAL": "/Volumes/JOE/NKI/MC96_MISSION_CONTROL"}

NETWORK = {"SWITCH": {"name": "DGS1210-10", "ip": "192.168.0.1"}, "GABRIEL_HOST": {"name": "HP-OMEN", "ip": "192.168.0.100"}, "DISPLAY": {"name": "Planar2485", "ip": "192.168.0.248"}}

SERVER_CONFIG = {"HOST": "0.0.0.0", "PORT": 8096, "WS_PORT": 8765}

if __name__ == "__main__":
    print("GABRIEL CONFIG LOADED")
    print(f"  Model: {OPENAI_CONFIG['REASONING_MODEL']}")
    print(f"  Voice: {OPENAI_CONFIG['VOICE_ID']}")
    print(f"  Port: {SERVER_CONFIG['PORT']}")
