import os
import time
import socket
import struct
import platform
import subprocess

# --- CONFIGURATION (DREAMCHAMBER) ---
PC_IP = "10.90.90.20"
PC_MAC = "XX:XX:XX:XX:XX:XX" # User must configure
CHECK_INTERVAL_SEC = 5

def ping_pc(ip):
    """
    Pings the PC Node. Returns True if alive.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '1000', ip]
    
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def wake_on_lan(mac_address):
    """
    Sends Magic Packet to wake the PC.
    """
    if mac_address == "XX:XX:XX:XX:XX:XX":
        print("⚠️ MAC ADDRESS NOT CONFIGURED. CANNOT WAKE.")
        return

    addrs = mac_address.split(':')
    hw_addr = struct.pack('BBBBBB', *[int(x, 16) for x in addrs])
    magic = b'\xff' * 6 + hw_addr * 16
    
    # Broadcast to LAN
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(magic, ('10.90.90.255', 9))
    sock.close()
    print(f"✨ MAGIC PACKET SENT TO {mac_address}")

def main():
    print(f"🌉 DREAMCHAMBER LINK: ACTIVE")
    print(f"   TARGET: {PC_IP}")
    print("--------------------------------")
    
    was_alive = False
    
    while True:
        is_alive = ping_pc(PC_IP)
        
        timestamp = time.strftime("%H:%M:%S")
        
        if is_alive:
            if not was_alive:
                print(f"[{timestamp}] 🟢 PC IS ONLINE (LINK ESTABLISHED)")
                # Optional: Auto-mount shares here
            was_alive = True
        else:
            if was_alive:
                print(f"[{timestamp}] 🔴 PC WENT OFFLINE")
            else:
                print(f"[{timestamp}] ...waiting for PC...")
            was_alive = False
            
        time.sleep(CHECK_INTERVAL_SEC)

if __name__ == "__main__":
    # Optional: CLI arg to wake
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "wake":
        wake_on_lan(PC_MAC)
    else:
        main()
