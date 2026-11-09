"""
NOIZYLAB CORE - MASTER CELL v2.4
ONE FILE. ALL POWER. ZERO LATENCY.
GORUNFREE x1000
"""

from .master_cell import *
from .agents import AGENT_PROMPTS, get_agent, list_agents, AGENT_INFO
from .generators import AIGenerator, GeneratorConfig
from .dreamchamber import DreamChamber, Dream, create_chamber
from .knowledge_graph import KnowledgeGraph, Entity, Relation
from .memcell import MemCell, MemCellStore
from .router import SmartRouter
from .slack_bridge import SlackBridge, SlackConfig, create_slack_bridge
from .turbo_dispatcher import TurboDispatcher, Command, get_dispatcher, dispatch
from .async_engine import AsyncAIEngine, AsyncConfig, create_async_engine
from .github_webhook import GitHubWebhookReceiver, GitHubEvent, WebhookConfig, create_webhook_receiver
from .realtime_watcher import RealtimeWatcher, WatchConfig, WatchEvent, create_watcher
from .unified_api import GabrielAPI, create_api
from .prompt_library import PromptLibrary, PromptModule, get_library, get_prompt, list_prompts
from .code_forge import CodeForge, CodeTemplate, create_forge, TEMPLATES
from .test_runner import TestRunner, TestResult, TestReport, create_runner

__version__ = "2.4.0"
__author__ = "Rob Plowman / NOIZYLAB / MC96DIGIUNIVERSE"

__all__ = [
    # Metadata
    '__version__', '__author__',
    # Core
    'AGENT_PROMPTS', 'get_agent', 'list_agents', 'AGENT_INFO',
    'AIGenerator', 'GeneratorConfig',
    'DreamChamber', 'Dream', 'create_chamber',
    'KnowledgeGraph', 'Entity', 'Relation',
    'MemCell', 'MemCellStore',
    'SmartRouter',
    # Integration modules
    'SlackBridge', 'SlackConfig', 'create_slack_bridge',
    'TurboDispatcher', 'Command', 'get_dispatcher', 'dispatch',
    'AsyncAIEngine', 'AsyncConfig', 'create_async_engine',
    'GitHubWebhookReceiver', 'GitHubEvent', 'WebhookConfig', 'create_webhook_receiver',
    # v2.3 modules
    'RealtimeWatcher', 'WatchConfig', 'WatchEvent', 'create_watcher',
    'GabrielAPI', 'create_api',
    'PromptLibrary', 'PromptModule', 'get_library', 'get_prompt', 'list_prompts',
    # v2.4 modules
    'CodeForge', 'CodeTemplate', 'create_forge', 'TEMPLATES',
    'TestRunner', 'TestResult', 'TestReport', 'create_runner',
]
