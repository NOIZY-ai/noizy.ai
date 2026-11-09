import platform
import subprocess
import time
import sys
import os
from datetime import datetime

# MC96Universe Mission Control
# The central brain for network monitoring

TARGET_IP = "10.90.90.90" # Default Switch IP
PING_INTERVAL = 2 # Seconds
PACKET_SIZE = 8100 # Jumbo payload test

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_platform_ping_command(ip, size):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    size_flag = '-l' if platform.system().lower() == 'windows' else '-s'
    
    # Mac/Linux ping usually adds 8 bytes of ICMP header, so 8100 is safe for 9000 MTU.
    # Windows '-l' is payload size.
    
    # We add -D (Mac) or -f (Windows) to set "Don't Fragment" bit to prove Jumbo Frames works.
    df_flag = '-f' if platform.system().lower() == 'windows' else '-D'
    
    return ['ping', param, '1', df_flag, size_flag, str(size), ip]

def run_heartbeat():
    log(f"MC96Universe Mission Control Active.")
    log(f"Tracking Target: {TARGET_IP} with Super-Sonic Packets ({PACKET_SIZE} bytes)")
    
    consecutive_fails = 0
    
    while True:
        try:
            cmd = get_platform_ping_command(TARGET_IP, PACKET_SIZE)
            # Suppress output for clean log, capture return code
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                sys.stdout.write(f"\r>>> STATUS: GREEN | SUPER-SONIC LINK ESTABLISHED | CONNECTION STABLE")
                sys.stdout.flush()
                consecutive_fails = 0
            else:
                sys.stdout.write(f"\r!!! STATUS: RED   | PACKET LOSS DETECTED | LINK UNSTABLE     ")
                sys.stdout.flush()
                consecutive_fails += 1
                if consecutive_fails > 5:
                    print("\n")
                    log("!!! CRITICAL ALERT: Link requires attention. Check TCAT cables and MTU settings.")
                    consecutive_fails = 0 # Reset warning
            
            time.sleep(PING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n")
            log("Mission Control shutting down.")
            sys.exit(0)
        except Exception as e:
            log(f"System Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TARGET_IP = sys.argv[1]
    
    print("""
    __  ___      __________________                            
   /  |/  /_____/ __/ ___/_  __/ /  ______________  ___  ____ 
  / /|_/ / ___/ /_  \__ \ / / / /  / ___/ ___/ __ \/ _ \/ __ \\
 / /  / / /__/ __/ ___/ // / / /__/ /__/ /__/ /_/ /  __/ / / /
/_/  /_/\___/_/   /____//_/ /____/\___/\___/\____/\___/_/ /_/ 
                                                              
    MC96Universe Network Monitoring System v1.0
    """)
    run_heartbeat()
