#!/usr/bin/env python3
"""
GABRIEL File Suite Package
Main entry point for all operations
"""

__version__ = "1.0.0"
__author__ = "GABRIEL Operations"
__description__ = "Production-ready file intelligence for network drives"

# Core modules
from src.deepscan import DeepScan
from src.sensemaker import SenseMaker
from src.hivesort import HiveSort, OrganizeMode

__all__ = [
    'DeepScan',
    'SenseMaker', 
    'HiveSort',
    'OrganizeMode'
]
