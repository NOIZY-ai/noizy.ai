# 🤖 SYSTEM FILE: neural_link.py
# Purpose: Zero-Dependency WebSocket Server (Pure Python)
# "TinyLink" Protocol Implementation
# Tech: socket, threading, hashlib, base64

import socket
import threading
import json
import logging
import hashlib
import base64
import struct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NeuralLink")

MAGIC_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class NeuralLink:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.server_socket = None
        self.running = False
        self.thread = threading.Thread(target=self._run_server, daemon=True)

    def start(self):
        if not self.running:
            self.running = True
            self.thread.start()
            logger.info(f"🧠 NEURAL LINK: Zero-Dep Server active on ws://{self.host}:{self.port}")

    def _run_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            while self.running:
                client_sock, addr = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(client_sock,), daemon=True).start()
        except Exception as e:
            logger.error(f"Neural Link Server Error: {e}")

    def _handle_client(self, client_sock):
        try:
            # 1. Handshake
            data = client_sock.recv(1024).decode('utf-8', errors='ignore')
            headers = self._parse_headers(data)
            
            if 'Sec-WebSocket-Key' not in headers:
                client_sock.close()
                return

            key = headers['Sec-WebSocket-Key']
            accept_key = self._generate_accept_key(key)
            
            handshake = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n"
                "\r\n"
            )
            client_sock.sendall(handshake.encode())
            
            self.clients.add(client_sock)
            logger.info("🧠 NEURAL LINK: Synapse Connected (Pure Python).")
            
            # 2. Listen Loop (Keep alive)
            # We don't really process input for now, just keep connection open
            while self.running:
                msg = client_sock.recv(1024)
                if not msg: break
                # TODO: Implement Ping/Pong if needed
        except Exception:
            pass
        finally:
            self.clients.discard(client_sock)
            try: client_sock.close() 
            except: pass

    def _parse_headers(self, data):
        headers = {}
        lines = data.split('\r\n')
        for line in lines[1:]:
            parts = line.split(': ', 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        return headers

    def _generate_accept_key(self, key):
        hash_val = hashlib.sha1((key + MAGIC_GUID).encode()).digest()
        return base64.b64encode(hash_val).decode()

    def broadcast(self, event_type, data=None):
        """Broadcasts a JSON message to all connected clients."""
        if not self.clients: return
        
        payload = json.dumps({"type": event_type, "data": data or {}})
        frame = self._encode_frame(payload)
        
        to_remove = set()
        for client in self.clients:
            try:
                client.sendall(frame)
            except:
                to_remove.add(client)
        
        for client in to_remove:
            self.clients.discard(client)

    def _encode_frame(self, message):
        """Encodes a message into a WebSocket frame."""
        msg_bytes = message.encode('utf-8')
        msg_len = len(msg_bytes)
        
        # Frame: Fin=1, Opcode=1 (Text) -> 10000001 -> 0x81
        frame = bytearray([0x81])
        
        if msg_len < 126:
            frame.append(msg_len)
        elif msg_len < 65536:
            frame.append(126)
            frame.extend(struct.pack(">H", msg_len))
        else:
            frame.append(127)
            frame.extend(struct.pack(">Q", msg_len))
            
        frame.extend(msg_bytes)
        return frame

# Singleton factory
_link_instance = None
def get_neural_link():
    global _link_instance
    if _link_instance is None:
        _link_instance = NeuralLink()
    return _link_instance

if __name__ == "__main__":
    link = NeuralLink()
    link.start()
    import time
    print("Link Active. Broadcasting every 2s...")
    while True:
        time.sleep(2)
        link.broadcast("voice_active", {"test": True})
