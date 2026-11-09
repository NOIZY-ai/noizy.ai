"""
GABRIEL Bridges Module
======================
Cross-system integrations for hardware, native code, and AI services.
"""

from .unified_bridge import UnifiedBridge, GabrielVoice, GabrielIntelligence, MC96Controller
from .native_bridge import NativeBridge
from .hardware_monitor import GabrielHardwareMonitor

__all__ = [
    'UnifiedBridge',
    'GabrielVoice',
    'GabrielIntelligence',
    'MC96Controller',
    'NativeBridge',
    'GabrielHardwareMonitor'
]
