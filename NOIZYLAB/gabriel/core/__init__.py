"""
GABRIEL Core Module
====================
Central module for all GABRIEL system components.

Modules:
- automation.py    - Automated task execution
- cost_controller.py - Resource cost management
- observability.py - Metrics and monitoring
- run_manager.py   - Run lifecycle management
- security.py      - Security and authentication
- verifier.py      - Output verification
"""

__version__ = "2.0.0"
__author__ = "NOIZYLAB"

# Lazy imports to avoid circular dependencies
def get_version():
    return {
        "version": __version__,
        "name": "GABRIEL SYSTEM OMEGA",
        "protocol": "GORUNFREE"
    }

# Import core components
try:
    from .automation import Notifier, InboxWatcher, LaunchAgentManager, SafeMode
    from .cost_controller import CostCalculator, RateLimiter, UsageTracker, BudgetController
    from .observability import StructuredLogger, LogAggregator, Event, EventType
    from .run_manager import RunManager, RunState, RunStatus, RetryConfig
    from .security import KeychainManager, SecretRedactor, SecureKeyLoader, SimpleEncryption
    from .verifier import Verifier, ClaimExtractor, VerificationResult, CitationsContract
except ImportError as e:
    # Graceful degradation if modules have issues
    import sys
    print(f"[CORE] Warning: Some modules failed to import: {e}", file=sys.stderr)

__all__ = [
    'get_version',
    # Automation
    'Notifier', 'InboxWatcher', 'LaunchAgentManager', 'SafeMode',
    # Cost Control
    'CostCalculator', 'RateLimiter', 'UsageTracker', 'BudgetController',
    # Observability
    'StructuredLogger', 'LogAggregator', 'Event', 'EventType',
    # Run Management
    'RunManager', 'RunState', 'RunStatus', 'RetryConfig',
    # Security
    'KeychainManager', 'SecretRedactor', 'SecureKeyLoader', 'SimpleEncryption',
    # Verification
    'Verifier', 'ClaimExtractor', 'VerificationResult', 'CitationsContract'
]
