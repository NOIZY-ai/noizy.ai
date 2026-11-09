from pythonosc import udp_client

HOST="127.0.0.1"
PORT=7000
_client = udp_client.SimpleUDPClient(HOST, PORT)

def state(name: str, value):
    _client.send_message(f"/gabriel/{name}", value)

if __name__ == "__main__":
    state("boot", 1)
    state("idle", 1)
    print(f"OSC SENT -> {HOST}:{PORT}  (/gabriel/boot, /gabriel/idle)")
