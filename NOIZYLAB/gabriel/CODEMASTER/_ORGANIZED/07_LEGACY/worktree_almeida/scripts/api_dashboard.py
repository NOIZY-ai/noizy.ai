# ... (rest of your code above unchanged)

def ensure_secure_dir():
    """Create secure directory with proper permissions."""
    if not SECURE_DIR.exists():
        SECURE_DIR.mkdir(exist_ok=True)
        os.chmod(SECURE_DIR, 0o700)

def simple_encrypt(data: str, password: str) -> bytes:
    """
    Simple XOR encryption (NOT SECURE! Use cryptography package for production).
    """
    key = (password * (len(data) // len(password) + 1))[:len(data)]
    return bytes(ord(a) ^ ord(b) for a, b in zip(data, key))

def simple_decrypt(data: bytes, password: str) -> str:
    """Simple XOR decryption."""
    key = (password * (len(data) // len(password) + 1))[:len(data)]
    return ''.join(chr(a ^ ord(b)) for a, b in zip(data, key))

def load_keys(password: str) -> Dict[str, str]:
    """Load and decrypt keys from disk."""
    if not KEYS_FILE.exists():
        return {}
    try:
        encrypted = KEYS_FILE.read_bytes()
        decrypted = simple_decrypt(encrypted, password)
        return json.loads(decrypted)
    except Exception as e:
        print(f"Error loading keys: {e}")
        return {}

# ... (rest of your code unchanged)
