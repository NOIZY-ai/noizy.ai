"""
NOIZYLAB CORE v2.0 - GORUNFREE EDITION
Main package initialization and exports
"""

from .router import SmartRouter
from .generators import AIGenerator
from .agents import AGENT_PROMPTS, get_agent

__version__ = "2.0.0"
__author__ = "Rob Plowman"
__all__ = ["SmartRouter", "AIGenerator", "AGENT_PROMPTS", "get_agent"]
