#!/usr/bin/env python3
"""
🚀 NOIZYVOX AI MANAGER - Complete AI Management & Assistance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A unified command center for all AI services, API keys, and voice capabilities.

Features:
  🔐 API Key Management - Store, rotate, validate keys
  🎙️ Voice Assistant - Talk to Claude with voice I/O
  🤖 Multi-Model Chat - Claude, GPT-4, Gemini, Mistral
  📊 Usage Tracking - Monitor costs and quotas
  🔄 Model Routing - Auto-select best model for task
  💾 Conversation History - Save and resume chats
  🎨 Rich Terminal UI - Beautiful, interactive interface

Usage:
  # Interactive mode (full dashboard)
  python noizyvox_ai_manager.py
  
  # Quick commands
  python noizyvox_ai_manager.py chat "Your question here"
  python noizyvox_ai_manager.py voice
  python noizyvox_ai_manager.py keys
  python noizyvox_ai_manager.py status
  python noizyvox_ai_manager.py models

Requirements:
  pip install anthropic openai rich prompt_toolkit httpx
"""

import argparse
import json
import os
import sys
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, List, Any

# Rich terminal UI
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.markdown import Markdown
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.box import ROUNDED, DOUBLE, HEAVY
    from rich.style import Style
    from rich.tree import Tree
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("⚠️  Install rich for better UI: pip install rich")

# API clients
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

# =============================================================================
# Configuration
# =============================================================================

console = Console() if HAS_RICH else None

# Config paths
CONFIG_DIR = Path.home() / ".noizyvox"
HISTORY_DIR = CONFIG_DIR / "history"
MODELS_CACHE = CONFIG_DIR / "models_cache.json"

# Ensure directories exist
CONFIG_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)

# =============================================================================
# Model Definitions
# =============================================================================

class Provider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    MISTRAL = "mistral"
    GROQ = "groq"
    XAI = "xai"

@dataclass
class ModelInfo:
    """Information about an AI model."""
    id: str
    provider: Provider
    name: str
    description: str
    context_window: int
    max_output: int
    input_price: float  # per 1M tokens
    output_price: float  # per 1M tokens
    capabilities: List[str] = field(default_factory=list)
    is_default: bool = False

# Complete model registry
MODELS: Dict[str, ModelInfo] = {
    # Anthropic Claude
    "claude-opus-4-20250514": ModelInfo(
        id="claude-opus-4-20250514",
        provider=Provider.ANTHROPIC,
        name="Claude Opus 4",
        description="Most capable Claude model for complex tasks",
        context_window=200000,
        max_output=32000,
        input_price=15.0,
        output_price=75.0,
        capabilities=["reasoning", "coding", "analysis", "creative", "vision"],
        is_default=False,
    ),
    "claude-sonnet-4-20250514": ModelInfo(
        id="claude-sonnet-4-20250514",
        provider=Provider.ANTHROPIC,
        name="Claude Sonnet 4",
        description="Best balance of speed and capability",
        context_window=200000,
        max_output=16000,
        input_price=3.0,
        output_price=15.0,
        capabilities=["reasoning", "coding", "analysis", "creative", "vision"],
        is_default=True,
    ),
    "claude-3-5-haiku-20241022": ModelInfo(
        id="claude-3-5-haiku-20241022",
        provider=Provider.ANTHROPIC,
        name="Claude 3.5 Haiku",
        description="Fast and efficient for quick tasks",
        context_window=200000,
        max_output=8192,
        input_price=0.80,
        output_price=4.0,
        capabilities=["coding", "analysis", "quick-tasks"],
    ),
    # OpenAI GPT
    "gpt-4o": ModelInfo(
        id="gpt-4o",
        provider=Provider.OPENAI,
        name="GPT-4o",
        description="OpenAI's most capable multimodal model",
        context_window=128000,
        max_output=16384,
        input_price=2.50,
        output_price=10.0,
        capabilities=["reasoning", "coding", "vision", "audio"],
    ),
    "gpt-4o-mini": ModelInfo(
        id="gpt-4o-mini",
        provider=Provider.OPENAI,
        name="GPT-4o Mini",
        description="Fast and affordable for most tasks",
        context_window=128000,
        max_output=16384,
        input_price=0.15,
        output_price=0.60,
        capabilities=["coding", "analysis", "quick-tasks"],
    ),
    "o1": ModelInfo(
        id="o1",
        provider=Provider.OPENAI,
        name="o1",
        description="Reasoning model for complex problems",
        context_window=200000,
        max_output=100000,
        input_price=15.0,
        output_price=60.0,
        capabilities=["reasoning", "math", "coding", "science"],
    ),
    "o1-mini": ModelInfo(
        id="o1-mini",
        provider=Provider.OPENAI,
        name="o1-mini",
        description="Fast reasoning model",
        context_window=128000,
        max_output=65536,
        input_price=1.10,
        output_price=4.40,
        capabilities=["reasoning", "math", "coding"],
    ),
    # Mistral
    "mistral-large-latest": ModelInfo(
        id="mistral-large-latest",
        provider=Provider.MISTRAL,
        name="Mistral Large",
        description="Mistral's most capable model",
        context_window=128000,
        max_output=8192,
        input_price=2.0,
        output_price=6.0,
        capabilities=["reasoning", "coding", "multilingual"],
    ),
    # Groq (fast inference)
    "llama-3.3-70b-versatile": ModelInfo(
        id="llama-3.3-70b-versatile",
        provider=Provider.GROQ,
        name="Llama 3.3 70B (Groq)",
        description="Ultra-fast inference via Groq",
        context_window=128000,
        max_output=32768,
        input_price=0.59,
        output_price=0.79,
        capabilities=["coding", "analysis", "fast"],
    ),
    # xAI Grok
    "grok-2": ModelInfo(
        id="grok-2",
        provider=Provider.XAI,
        name="Grok 2",
        description="xAI's latest model",
        context_window=131072,
        max_output=8192,
        input_price=2.0,
        output_price=10.0,
        capabilities=["reasoning", "coding", "real-time"],
    ),
}

# =============================================================================
# API Key Status
# =============================================================================

@dataclass
class APIKeyStatus:
    """Status of an API key."""
    provider: str
    env_var: str
    is_set: bool
    is_valid: Optional[bool] = None
    masked_key: Optional[str] = None
    error: Optional[str] = None

def check_api_keys() -> Dict[str, APIKeyStatus]:
    """Check status of all API keys."""
    keys = {
        "anthropic": APIKeyStatus(
            provider="Anthropic",
            env_var="ANTHROPIC_API_KEY",
            is_set=bool(os.getenv("ANTHROPIC_API_KEY")),
            masked_key=mask_key(os.getenv("ANTHROPIC_API_KEY")),
        ),
        "openai": APIKeyStatus(
            provider="OpenAI",
            env_var="OPENAI_API_KEY",
            is_set=bool(os.getenv("OPENAI_API_KEY")),
            masked_key=mask_key(os.getenv("OPENAI_API_KEY")),
        ),
        "google": APIKeyStatus(
            provider="Google AI",
            env_var="GOOGLE_API_KEY",
            is_set=bool(os.getenv("GOOGLE_API_KEY")),
            masked_key=mask_key(os.getenv("GOOGLE_API_KEY")),
        ),
        "mistral": APIKeyStatus(
            provider="Mistral",
            env_var="MISTRAL_API_KEY",
            is_set=bool(os.getenv("MISTRAL_API_KEY")),
            masked_key=mask_key(os.getenv("MISTRAL_API_KEY")),
        ),
        "groq": APIKeyStatus(
            provider="Groq",
            env_var="GROQ_API_KEY",
            is_set=bool(os.getenv("GROQ_API_KEY")),
            masked_key=mask_key(os.getenv("GROQ_API_KEY")),
        ),
        "xai": APIKeyStatus(
            provider="xAI",
            env_var="XAI_API_KEY",
            is_set=bool(os.getenv("XAI_API_KEY")),
            masked_key=mask_key(os.getenv("XAI_API_KEY")),
        ),
        "elevenlabs": APIKeyStatus(
            provider="ElevenLabs",
            env_var="ELEVENLABS_API_KEY",
            is_set=bool(os.getenv("ELEVENLABS_API_KEY")),
            masked_key=mask_key(os.getenv("ELEVENLABS_API_KEY")),
        ),
        "cloudflare": APIKeyStatus(
            provider="Cloudflare",
            env_var="CLOUDFLARE_API_TOKEN",
            is_set=bool(os.getenv("CLOUDFLARE_API_TOKEN")),
            masked_key=mask_key(os.getenv("CLOUDFLARE_API_TOKEN")),
        ),
    }
    return keys

def mask_key(key: Optional[str]) -> Optional[str]:
    """Mask an API key for display."""
    if not key:
        return None
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}...{key[-4:]}"

# =============================================================================
# AI Client Manager
# =============================================================================

class AIManager:
    """Unified AI client manager."""
    
    def __init__(self):
        self.clients: Dict[Provider, Any] = {}
        self.conversation_history: List[Dict] = []
        self.current_model = "claude-sonnet-4-20250514"
        self._init_clients()
    
    def _init_clients(self):
        """Initialize available API clients."""
        # Anthropic
        if HAS_ANTHROPIC and os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.clients[Provider.ANTHROPIC] = anthropic.Anthropic()
            except Exception as e:
                print(f"⚠️  Anthropic init failed: {e}")
        
        # OpenAI
        if HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
            try:
                self.clients[Provider.OPENAI] = openai.OpenAI()
            except Exception as e:
                print(f"⚠️  OpenAI init failed: {e}")
    
    def get_available_providers(self) -> List[Provider]:
        """Get list of available providers."""
        return list(self.clients.keys())
    
    def get_available_models(self) -> List[ModelInfo]:
        """Get list of available models based on configured keys."""
        available = []
        for model_id, model in MODELS.items():
            if model.provider in self.clients:
                available.append(model)
        return available
    
    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        stream: bool = True,
    ) -> str:
        """Send a chat message to the AI."""
        model_id = model or self.current_model
        model_info = MODELS.get(model_id)
        
        if not model_info:
            raise ValueError(f"Unknown model: {model_id}")
        
        provider = model_info.provider
        
        if provider not in self.clients:
            raise ValueError(f"Provider {provider.value} not configured")
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
        })
        
        # Route to appropriate provider
        if provider == Provider.ANTHROPIC:
            response = self._chat_anthropic(message, model_id, system_prompt, stream)
        elif provider == Provider.OPENAI:
            response = self._chat_openai(message, model_id, system_prompt, stream)
        else:
            raise ValueError(f"Provider {provider.value} not implemented")
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "model": model_id,
            "timestamp": datetime.now().isoformat(),
        })
        
        return response
    
    def _chat_anthropic(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        stream: bool,
    ) -> str:
        """Chat with Anthropic Claude."""
        client = self.clients[Provider.ANTHROPIC]
        
        # Build messages from history
        messages = []
        for msg in self.conversation_history:
            if msg["role"] in ("user", "assistant"):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })
        
        # Add current message if not already in history
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        
        kwargs = {
            "model": model,
            "max_tokens": MODELS[model].max_output,
            "messages": messages,
        }
        
        if system_prompt:
            kwargs["system_prompt"] = system_prompt
        
        if stream and console:
            response_text = ""
            with client.messages.stream(**kwargs) as stream_response:
                for text in stream_response.text_stream:
                    console.print(text, end="")
                    response_text += text
            console.print()
            return response_text
        else:
            response = client.messages.create(**kwargs)
            return response.content[0].text
    
    def _chat_openai(
        self,
        message: str,
        model: str,
        system_prompt: Optional[str],
        stream: bool,
    ) -> str:
        """Chat with OpenAI."""
        client = self.clients[Provider.OPENAI]
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        for msg in self.conversation_history:
            if msg["role"] in ("user", "assistant"):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                })
        
        if not messages or messages[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        
        if stream and console:
            response_text = ""
            stream_response = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    console.print(text, end="")
                    response_text += text
            console.print()
            return response_text
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def save_conversation(self, name: Optional[str] = None) -> Path:
        """Save conversation to file."""
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filepath = HISTORY_DIR / f"{name}.json"
        with open(filepath, "w") as f:
            json.dump({
                "model": self.current_model,
                "created": datetime.now().isoformat(),
                "messages": self.conversation_history,
            }, f, indent=2)
        
        return filepath
    
    def load_conversation(self, filepath: Path):
        """Load conversation from file."""
        with open(filepath) as f:
            data = json.load(f)
        
        self.current_model = data.get("model", self.current_model)
        self.conversation_history = data.get("messages", [])

# =============================================================================
# Terminal UI
# =============================================================================

def print_banner():
    """Print welcome banner."""
    if not console:
        print("\n🚀 NOIZYVOX AI MANAGER\n")
        return
    
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🚀 NOIZYVOX AI MANAGER                                        ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                    ║
║   Complete AI Management & Assistance                            ║
║                                                                  ║
║   Commands:                                                       ║
║     chat    - Start AI conversation                              ║
║     voice   - Voice input/output mode                            ║
║     keys    - Manage API keys                                    ║
║     models  - List available models                              ║
║     status  - System status                                      ║
║     help    - Show help                                          ║
║     quit    - Exit                                               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    console.print(Panel(
        banner.strip(),
        style="cyan",
        box=DOUBLE,
    ))

def show_status():
    """Show system status."""
    if not console:
        print("\n📊 System Status")
        keys = check_api_keys()
        for key, status in keys.items():
            icon = "✅" if status.is_set else "❌"
            print(f"  {icon} {status.provider}: {status.masked_key or 'Not set'}")
        return
    
    # API Keys Table
    keys_table = Table(title="🔐 API Keys", box=ROUNDED)
    keys_table.add_column("Provider", style="cyan")
    keys_table.add_column("Status", style="green")
    keys_table.add_column("Key", style="dim")
    
    keys = check_api_keys()
    for key, status in keys.items():
        icon = "✅" if status.is_set else "❌"
        keys_table.add_row(
            status.provider,
            icon,
            status.masked_key or "[dim]Not configured[/dim]",
        )
    
    console.print(keys_table)
    
    # Available Models
    manager = AIManager()
    models = manager.get_available_models()
    
    if models:
        models_table = Table(title="🤖 Available Models", box=ROUNDED)
        models_table.add_column("Model", style="cyan")
        models_table.add_column("Provider", style="green")
        models_table.add_column("Context", style="yellow")
        models_table.add_column("Price (In/Out)", style="magenta")
        
        for model in models:
            default_mark = " ⭐" if model.is_default else ""
            models_table.add_row(
                f"{model.name}{default_mark}",
                model.provider.value,
                f"{model.context_window:,}",
                f"${model.input_price:.2f}/${model.output_price:.2f}",
            )
        
        console.print(models_table)

def show_models():
    """Show all models with details."""
    if not console:
        print("\n🤖 Available Models:")
        for model_id, model in MODELS.items():
            print(f"  - {model.name} ({model.provider.value})")
        return
    
    table = Table(title="🤖 AI Models Registry", box=ROUNDED, show_lines=True)
    table.add_column("Model ID", style="cyan", width=30)
    table.add_column("Name", style="green")
    table.add_column("Provider", style="yellow")
    table.add_column("Context", style="blue", justify="right")
    table.add_column("Max Out", style="blue", justify="right")
    table.add_column("$/M In", style="magenta", justify="right")
    table.add_column("$/M Out", style="magenta", justify="right")
    table.add_column("Capabilities", style="dim")
    
    for model_id, model in MODELS.items():
        caps = ", ".join(model.capabilities[:3])
        if len(model.capabilities) > 3:
            caps += f" +{len(model.capabilities)-3}"
        
        default_mark = " ⭐" if model.is_default else ""
        
        table.add_row(
            model_id,
            f"{model.name}{default_mark}",
            model.provider.value,
            f"{model.context_window:,}",
            f"{model.max_output:,}",
            f"${model.input_price:.2f}",
            f"${model.output_price:.2f}",
            caps,
        )
    
    if console:
        console.print(table)

def show_keys():
    """Show and manage API keys."""
    if not console:
        print("\n🔐 API Keys:")
        keys = check_api_keys()
        for key, status in keys.items():
            icon = "✅" if status.is_set else "❌"
            print(f"  {icon} {status.env_var}: {status.masked_key or 'Not set'}")
        return
    
    # Show current keys
    table = Table(title="🔐 API Key Status", box=ROUNDED)
    table.add_column("Provider", style="cyan")
    table.add_column("Environment Variable", style="yellow")
    table.add_column("Status", style="green")
    table.add_column("Value", style="dim")
    
    keys = check_api_keys()
    for key, status in keys.items():
        icon = "✅ Set" if status.is_set else "❌ Missing"
        table.add_row(
            status.provider,
            status.env_var,
            icon,
            status.masked_key or "-",
        )
    
    console.print(table)
    console.print("\n[dim]Use 'python api_key_manager.py' for full key management[/dim]")

def interactive_chat(manager: AIManager):
    """Interactive chat mode."""
    if console:
        console.print("\n[cyan]💬 Chat Mode[/cyan] (type 'exit' to quit, 'clear' to reset)")
        console.print(f"[dim]Model: {manager.current_model}[/dim]\n")
    else:
        print("\n💬 Chat Mode (type 'exit' to quit)")
    
    while True:
        try:
            if console:
                user_input = Prompt.ask("[green]You[/green]")
            else:
                user_input = input("You: ")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() == "exit":
                break
            
            if user_input.lower() == "clear":
                manager.clear_history()
                if console:
                    console.print("[dim]Conversation cleared[/dim]")
                else:
                    print("Conversation cleared")
                continue
            
            if user_input.lower().startswith("/model "):
                new_model = user_input[7:].strip()
                if new_model in MODELS:
                    manager.current_model = new_model
                    if console:
                        console.print(f"[dim]Switched to {new_model}[/dim]")
                    else:
                        print(f"Switched to {new_model}")
                else:
                    if console:
                        console.print(f"[red]Unknown model: {new_model}[/red]")
                    else:
                        print(f"Unknown model: {new_model}")
                continue
            
            if user_input.lower() == "/save":
                path = manager.save_conversation()
                if console:
                    console.print(f"[dim]Saved to {path}[/dim]")
                else:
                    print(f"Saved to {path}")
                continue
            
            # Get AI response
            if console:
                console.print("[cyan]Claude[/cyan]: ", end="")
            else:
                print("Claude: ", end="")
            
            response = manager.chat(user_input)
            
            if not console:
                print(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            if console:
                console.print(f"[red]Error: {e}[/red]")
            else:
                print(f"Error: {e}")

def voice_mode(manager: AIManager):
    """Voice input/output mode using claude_voice_cli."""
    script_dir = Path(__file__).parent
    voice_cli = script_dir / "claude_voice_cli.py"
    
    if not voice_cli.exists():
        if console:
            console.print("[red]Voice CLI not found. Please ensure claude_voice_cli.py is in the scripts folder.[/red]")
        else:
            print("Voice CLI not found.")
        return
    
    if console:
        console.print("\n[cyan]🎙️ Voice Mode[/cyan]")
        console.print("[dim]Launching voice assistant...[/dim]\n")
    
    # Launch voice CLI in full voice mode
    subprocess.run([
        sys.executable,
        str(voice_cli),
        "--voice-in",
        "--voice-out",
    ])

def show_help():
    """Show help information."""
    if not console:
        print("""
NOIZYVOX AI Manager - Help
━━━━━━━━━━━━━━━━━━━━━━━━━━

Commands:
  chat [message]  - Start chat (optional initial message)
  voice           - Voice input/output mode
  keys            - View/manage API keys
  models          - List available models
  status          - Show system status
  help            - Show this help
  quit/exit       - Exit the manager

Chat Commands (in chat mode):
  /model <name>   - Switch model
  /save           - Save conversation
  clear           - Clear conversation
  exit            - Exit chat mode
""")
        return
    
    help_text = """
## Commands

| Command | Description |
|---------|-------------|
| `chat [message]` | Start AI conversation |
| `voice` | Voice input/output mode |
| `keys` | View/manage API keys |
| `models` | List available models |
| `status` | Show system status |
| `help` | Show this help |
| `quit` | Exit |

## Chat Mode Commands

| Command | Description |
|---------|-------------|
| `/model <name>` | Switch to different model |
| `/save` | Save conversation to file |
| `clear` | Clear conversation history |
| `exit` | Exit chat mode |

## Examples

```bash
# Quick chat
python noizyvox_ai_manager.py chat "Explain quantum computing"

# Voice mode
python noizyvox_ai_manager.py voice

# Check API keys
python noizyvox_ai_manager.py keys
```
"""
    console.print(Panel(Markdown(help_text), title="📚 Help", border_style="cyan"))

# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🚀 NOIZYVOX AI Manager - Complete AI Management & Assistance"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=["interactive", "chat", "voice", "keys", "models", "status", "help"],
        help="Command to run",
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message for chat command",
    )
    parser.add_argument(
        "--model", "-m",
        default="claude-sonnet-4-20250514",
        help="Model to use for chat",
    )
    
    args = parser.parse_args()
    
    # Initialize AI manager
    manager = AIManager()
    manager.current_model = args.model
    
    # Handle commands
    if args.command == "status":
        show_status()
    elif args.command == "models":
        show_models()
    elif args.command == "keys":
        show_keys()
    elif args.command == "help":
        show_help()
    elif args.command == "voice":
        voice_mode(manager)
    elif args.command == "chat":
        if args.message:
            # Single message mode
            message = " ".join(args.message)
            if console:
                console.print(f"[green]You[/green]: {message}")
                console.print("[cyan]Claude[/cyan]: ", end="")
            response = manager.chat(message)
            if not console:
                print(f"You: {message}")
                print(f"Claude: {response}")
        else:
            # Interactive chat
            interactive_chat(manager)
    else:
        # Interactive mode
        print_banner()
        
        while True:
            try:
                if console:
                    cmd = Prompt.ask("\n[cyan]noizyvox[/cyan]").strip().lower()
                else:
                    cmd = input("\nnoizyvox> ").strip().lower()
                
                if not cmd:
                    continue
                
                if cmd in ("quit", "exit", "q"):
                    if console:
                        console.print("[dim]Goodbye! 👋[/dim]")
                    break
                elif cmd == "chat":
                    interactive_chat(manager)
                elif cmd == "voice":
                    voice_mode(manager)
                elif cmd == "keys":
                    show_keys()
                elif cmd == "models":
                    show_models()
                elif cmd == "status":
                    show_status()
                elif cmd == "help":
                    show_help()
                elif cmd.startswith("chat "):
                    message = cmd[5:].strip()
                    if console:
                        console.print(f"[cyan]Claude[/cyan]: ", end="")
                    response = manager.chat(message)
                    if not console:
                        print(f"Claude: {response}")
                else:
                    if console:
                        console.print(f"[yellow]Unknown command: {cmd}. Type 'help' for available commands.[/yellow]")
                    else:
                        print(f"Unknown command: {cmd}")
                
            except KeyboardInterrupt:
                if console:
                    console.print("\n[dim]Goodbye! 👋[/dim]")
                break
            except EOFError:
                break

if __name__ == "__main__":
    main()
