import sys
import os

# Add the mvent package directory to Python path
mvent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mvent")
if mvent_dir not in sys.path:
    sys.path.insert(0, mvent_dir)

try:
    from mvent import SharedMemoryPool
except ImportError:
    # Fallback: try direct import from core module
    from mvent.core.shared_memory import SharedMemoryPool


class IPC:
    @staticmethod
    def connect(name: str = "codemate-subsystem") -> SharedMemoryPool:
        x = SharedMemoryPool(pool_name=name, auto_cleanup=False)
        return x
