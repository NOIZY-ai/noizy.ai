
import os
import time
import subprocess
import requests
from voice_core import VoiceCore
from memcell_core import MemCellCore

GABRIEL_IP = "10.100.0.2"
API_URL = "http://localhost:5173/api/voice/say"

def ping_gabriel():
    """Ping the Gabriel Node (HP-OMEN) until it responds."""
    print(f"📡 SCANNING FOR GABRIEL NODE ({GABRIEL_IP})...")
    
    while True:
        try:
            # Ping with 1 second timeout
            res = subprocess.run(
                ["ping", "-c", "1", "-W", "1000", GABRIEL_IP], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            if res.returncode == 0:
                print("✅ GABRIEL NODE DETECTED!")
                return True
                
        except Exception as e:
            print(f"Error scanning: {e}")
            
        time.sleep(2) # Scan every 2 seconds

def announce_arrival():
    """Announce the arrival of the node."""
    voice = VoiceCore()
    memcell = MemCellCore()
    
    msg = "Network Uplink Established. Gabriel Node is Online. The Family is Complete."
    
    print(f"🗣️ ANNOUNCING: {msg}")
    
    # Speak locally (M2 Ultra)
    voice.speak(msg)
    
    # Speak remotely (iPhone) via Server Queue
    try:
        requests.post(API_URL, json={"text": msg})
    except:
        pass
        
    # Log to Brain
    memcell.collect("GABRIEL_NODE_CONNECTION", {
        "ip": GABRIEL_IP, 
        "status": "ONLINE", 
        "event": "HANDSHAKE_COMPLETE"
    })

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║             GABRIEL HANDSHAKE PROTOCOL ACTIVATED               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    
    if ping_gabriel():
        announce_arrival()
        print("🎉 HANDSHAKE COMPLETE. GORUNFREE!!!")
