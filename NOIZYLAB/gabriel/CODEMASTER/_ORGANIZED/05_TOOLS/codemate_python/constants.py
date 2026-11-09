import ssl
import certifi
from pathlib import Path
from ipc import IPC

SSL_CERT_FILE = certifi.where()
SSL_CONTEXT = ssl.create_default_context(cafile=SSL_CERT_FILE)

# Socket.IO Configuration for Sleep/Wake Resilience
SOCKETIO_PING_INTERVAL = 25  # Seconds between ping packets (increased for sleep mode)
SOCKETIO_PING_TIMEOUT = 300000  # Seconds to wait for ping response before disconnecting
SOCKETIO_MAX_HTTP_BUFFER_SIZE = 100 * 1024 * 1024  # 100 MB limit for Socket.IO messages


ipc_ = IPC.connect()

HOME_PATH = Path.home() / ".codemate"


general: str = "https://backend.v3.codemate.ai"
chat: str = "https://backend.v3.codemate.ai"
codebase: str = "https://codebase.v3.codemate.ai"
autocomplete: str = "https://autocomplete.codemate.ai"
embeddings: str = "https://embeddings.v3.codemate.ai"
cloud: str = "https://backend.v3.codemateai.dev"
llm_: str = "https://backend.v3.codemateai.dev/v2"
auth: str = "https://api.identity.codemate.ai"
analytics: str = "https://analytics.v3.codemate.ai"
chat_pro: str = "http://34.16.2.178/v1"
