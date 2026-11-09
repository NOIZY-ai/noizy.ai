# SystemGuardian Modules
# Part of GABRIEL SYSTEM OMEGA - MC96DIGIUNIVERSE

from .system_doctor import SystemDoctor
from .auto_fix import SystemRepair, quick_optimize, quick_memory_purge, quick_dns_flush

__all__ = ["SystemDoctor", "SystemRepair", "quick_optimize", "quick_memory_purge", "quick_dns_flush"]
__version__ = "1.1.0"
