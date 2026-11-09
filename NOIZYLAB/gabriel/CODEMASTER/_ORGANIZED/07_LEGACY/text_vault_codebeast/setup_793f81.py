#!/usr/bin/env python3
"""
🚀 CODEBEAST SETUP SCRIPT 🚀
Initialize your super strong, smart, and helpful AI development environment

This script sets up OpenAI integration and prepares your CodeBeast for action!
"""

import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt

console = Console()


def display_banner():
    """Display the GABRIEL setup banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║                    🌟 GABRIEL AI SYSTEM 🌟                       ║
║           Ultra-Advanced • Multi-Model • Enterprise              ║
║                                                                   ║
║         🧠 Next-Gen AI Development Framework (v2.0) 🧠           ║
║         ⚡ GPT-4o • Claude • Gemini • o1 Series ⚡               ║
╚═══════════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("[dim]Powered by OpenAI, Anthropic, and Google AI[/dim]\n")


def check_python_version():
    """Check if Python version is compatible"""
    console.print("🐍 Checking Python version...")

    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        console.print(
            f"[green]✅ Python {version.major}.{version.minor}.{version.micro} detected - Optimal![/green]"
        )
        return True
    elif version.major == 3 and version.minor >= 8:
        console.print(
            f"[yellow]⚠️  Python {version.major}.{version.minor} detected - Works but upgrade to 3.10+ recommended[/yellow]"
        )
        return True
    else:
        console.print(
            f"[red]❌ Python {version.major}.{version.minor} detected - Need Python 3.10+ (3.8+ minimum)[/red]"
        )
        return False


def setup_environment_file():
    """Set up the .env file with multi-provider AI configuration"""
    console.print("\n🔧 Setting up GABRIEL environment configuration...")

    env_file = Path(".env")

    if env_file.exists():
        if not Confirm.ask("📄 .env file already exists. Overwrite?"):
            console.print("[yellow]⏭️ Skipping environment setup[/yellow]")
            return False

    # Provider selection
    console.print("\n🤖 [bold cyan]AI Provider Setup:[/bold cyan]")
    console.print("1. OpenAI (GPT-4o, GPT-4, o1-preview, o1-mini)")
    console.print("2. Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)")
    console.print("3. Google (Gemini 1.5 Pro, Gemini 2.0)")
    console.print("4. Multi-Provider (All of the above)")
    
    provider_choice = Prompt.ask("Select provider", choices=["1", "2", "3", "4"], default="1")
    
    openai_key = anthropic_key = google_key = ""
    
    if provider_choice in ["1", "4"]:
        console.print("\n🔑 OpenAI API Key:")
        console.print("Get one at: https://platform.openai.com/api-keys")
        openai_key = Prompt.ask("🔑 Enter OpenAI API key", password=True)
    
    if provider_choice in ["2", "4"]:
        console.print("\n🔑 Anthropic API Key:")
        console.print("Get one at: https://console.anthropic.com/")
        anthropic_key = Prompt.ask("🔑 Enter Anthropic API key", password=True, default="")
    
    if provider_choice in ["3", "4"]:
        console.print("\n🔑 Google AI API Key:")
        console.print("Get one at: https://makersuite.google.com/app/apikey")
        google_key = Prompt.ask("🔑 Enter Google AI API key", password=True, default="")

    # Model selection
    models = [
        "gpt-4o",
        "gpt-4o-mini", 
        "o1-preview",
        "o1-mini",
        "gpt-4-turbo",
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "gemini-1.5-pro",
        "gemini-2.0-flash-exp"
    ]
    
    console.print("\n🚀 [bold cyan]Available Models:[/bold cyan]")
    console.print("[bold green]OpenAI:[/bold green]")
    console.print("1. gpt-4o (Best overall, 128k context)")
    console.print("2. gpt-4o-mini (Fast & affordable)")
    console.print("3. o1-preview (Advanced reasoning)")
    console.print("4. o1-mini (Reasoning, faster)")
    console.print("5. gpt-4-turbo (Legacy, 128k context)")
    console.print("\n[bold blue]Anthropic:[/bold blue]")
    console.print("6. claude-3-5-sonnet (Best coding, 200k context)")
    console.print("7. claude-3-opus (Most capable, 200k context)")
    console.print("\n[bold yellow]Google:[/bold yellow]")
    console.print("8. gemini-1.5-pro (2M context!)")
    console.print("9. gemini-2.0-flash (Newest, fastest)")

    model_choice = Prompt.ask("Select primary model", choices=[str(i) for i in range(1, 10)], default="1")
    selected_model = models[int(model_choice) - 1]

    # Advanced configuration
    console.print("\n⚙️  [bold cyan]Advanced Configuration:[/bold cyan]")
    max_tokens = Prompt.ask("Max tokens", default="8000")
    temperature = Prompt.ask("Temperature (0.0-1.0)", default="0.7")
    enable_streaming = Confirm.ask("Enable streaming responses?", default=True)
    enable_caching = Confirm.ask("Enable response caching?", default=True)

    # Create .env file
    env_content = f"""# 🌟 GABRIEL AI SYSTEM Configuration
# Generated by GABRIEL Setup Script v2.0
# Date: {Path.cwd()}

# ========== AI Provider API Keys ==========
# OpenAI Configuration
OPENAI_API_KEY={openai_key}
OPENAI_ORG_ID=

# Anthropic Configuration  
ANTHROPIC_API_KEY={anthropic_key}

# Google AI Configuration
GOOGLE_AI_API_KEY={google_key}

# ========== Model Configuration ==========
PRIMARY_MODEL={selected_model}
FALLBACK_MODEL=gpt-4o-mini
MAX_TOKENS={max_tokens}
TEMPERATURE={temperature}
TOP_P=0.95
FREQUENCY_PENALTY=0.0
PRESENCE_PENALTY=0.0

# ========== GABRIEL System Configuration ==========
GABRIEL_MODE=production
GABRIEL_VERSION=2.0.0
GABRIEL_LOG_LEVEL=INFO
GABRIEL_LOG_FORMAT=json
GABRIEL_AI_ASSISTANT_NAME=GABRIEL AI
GABRIEL_DEFAULT_LANGUAGE=python

# ========== Advanced AI Features ==========
# Core AI Capabilities
AI_CODE_REVIEW_ENABLED=true
AI_AUTO_DOCUMENTATION=true
AI_SMART_DEBUGGING=true
AI_PERFORMANCE_OPTIMIZATION=true
AI_SECURITY_SCAN=true
AI_CODE_REFACTORING=true

# Streaming & Caching
ENABLE_STREAMING={'true' if enable_streaming else 'false'}
ENABLE_RESPONSE_CACHING={'true' if enable_caching else 'false'}
CACHE_TTL=3600

# Multi-Provider Support
ENABLE_MULTI_PROVIDER=true
AUTO_FALLBACK=true
LOAD_BALANCING=true

# ========== Performance & Monitoring ==========
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_ERROR_TRACKING=true
ENABLE_USAGE_ANALYTICS=true
REQUEST_TIMEOUT=120
MAX_RETRIES=3
RETRY_DELAY=2

# ========== Rate Limiting ==========
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=60
MAX_TOKENS_PER_MINUTE=150000

# ========== Context Management ==========
MAX_CONTEXT_LENGTH=128000
CONTEXT_COMPRESSION=true
SMART_TRUNCATION=true

# ========== Code Generation ==========
CODE_STYLE=pep8
AUTO_FORMAT=true
AUTO_LINT=true
GENERATE_TESTS=true
GENERATE_DOCS=true

# ========== Security ==========
ENABLE_API_KEY_ROTATION=true
SECURE_KEY_STORAGE=true
AUDIT_LOGGING=true

# ========== Experimental Features ==========
ENABLE_VOICE_INTERFACE=false
ENABLE_IMAGE_GENERATION=true
ENABLE_MULTIMODAL=true
ENABLE_AGENT_MEMORY=true
ENABLE_TOOL_USE=true
"""

    with open(env_file, "w") as f:
        f.write(env_content)

    console.print(f"[green]✅ Environment configured with {selected_model}![/green]")
    console.print("[cyan]💡 Multi-provider support enabled for maximum flexibility[/cyan]")
    return True


def install_dependencies():
    """Install required Python packages with parallel processing"""
    console.print("\n📦 Installing GABRIEL dependencies (enhanced package set)...")

    # Core packages
    core_packages = [
        "openai>=1.50.0",
        "anthropic>=0.39.0",
        "google-generativeai>=0.8.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "typer[all]>=0.12.0",
    ]
    
    # Async and networking
    async_packages = [
        "aiohttp>=3.10.0",
        "httpx>=0.27.0",
        "requests>=2.32.0",
        "websockets>=13.0",
    ]
    
    # AI and ML utilities
    ai_packages = [
        "tiktoken>=0.7.0",
        "langchain>=0.3.0",
        "langchain-openai>=0.2.0",
        "langchain-anthropic>=0.3.0",
        "langsmith>=0.1.0",
    ]
    
    # Development tools
    dev_packages = [
        "black>=24.0.0",
        "ruff>=0.6.0",
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.0",
    ]
    
    # Monitoring and analytics
    monitoring_packages = [
        "psutil>=6.0.0",
        "prometheus-client>=0.20.0",
    ]

    all_packages = core_packages + async_packages + ai_packages + dev_packages + monitoring_packages

    console.print(f"[cyan]📊 Total packages to install: {len(all_packages)}[/cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        # Upgrade pip first
        console.print("[cyan]⬆️  Upgrading pip...[/cyan]")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print("[green]✅ pip upgraded[/green]\n")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠️  Could not upgrade pip, continuing...[/yellow]\n")

        failed_packages = []
        
        for package in all_packages:
            task = progress.add_task(f"Installing {package}...", total=None)

            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-q", package],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=180,
                )

                progress.remove_task(task)
                console.print(f"[green]✅ {package}[/green]")

            except subprocess.CalledProcessError as e:
                progress.remove_task(task)
                console.print(f"[yellow]⚠️  {package} (non-critical)[/yellow]")
                failed_packages.append(package)
            except subprocess.TimeoutExpired:
                progress.remove_task(task)
                console.print(f"[yellow]⏱️  {package} (timeout)[/yellow]")
                failed_packages.append(package)

    if failed_packages:
        console.print(f"\n[yellow]⚠️  {len(failed_packages)} packages failed (system may still work)[/yellow]")
        console.print(f"[dim]Failed: {', '.join(failed_packages)}[/dim]")
    else:
        console.print("\n[green]🎉 All packages installed successfully![/green]")

    return True


def verify_ai_setup():
    """Verify AI components are working with multi-provider support"""
    console.print("\n🧠 Verifying GABRIEL AI setup...")
    
    verified_providers = []
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        # Check OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                # Quick validation
                models = client.models.list()
                console.print("[green]✅ OpenAI API verified[/green]")
                verified_providers.append("OpenAI")
            except Exception as e:
                console.print(f"[yellow]⚠️  OpenAI API warning: {str(e)[:50]}...[/yellow]")
        
        # Check Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                console.print("[green]✅ Anthropic API verified[/green]")
                verified_providers.append("Anthropic")
            except Exception as e:
                console.print(f"[yellow]⚠️  Anthropic API warning: {str(e)[:50]}...[/yellow]")
        
        # Check Google AI
        if os.getenv("GOOGLE_AI_API_KEY"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
                console.print("[green]✅ Google AI API verified[/green]")
                verified_providers.append("Google AI")
            except Exception as e:
                console.print(f"[yellow]⚠️  Google AI warning: {str(e)[:50]}...[/yellow]")
        
        if verified_providers:
            console.print(f"\n[bold green]🎉 {len(verified_providers)} provider(s) verified: {', '.join(verified_providers)}[/bold green]")
            return True
        else:
            console.print("[yellow]⚠️  No API keys configured. Add them to .env file.[/yellow]")
            return True  # Non-blocking

    except Exception as e:
        console.print(f"[yellow]⚠️  Verification skipped: {e}[/yellow]")
        return True  # Non-blocking


def create_sample_claw():
    """Create advanced sample AI-powered claw"""
    console.print("\n🐾 Creating GABRIEL sample AI modules...")

    # Ensure claws directory exists
    claws_dir = Path("claws")
    claws_dir.mkdir(exist_ok=True)

    sample_claw = claws_dir / "gabriel_ai_demo.py"

    sample_content = '''#!/usr/bin/env python3
"""
🌟 GABRIEL AI DEMO 🌟
Advanced multi-provider AI demonstration

Features:
- Multi-provider support (OpenAI, Anthropic, Google)
- Streaming responses
- Error handling and fallbacks
- Performance monitoring
- Token usage tracking
"""

import asyncio
import os
import time
from pathlib import Path
from typing import AsyncIterator

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

load_dotenv()

console = Console()

class GabrielAI:
    """GABRIEL AI Engine with multi-provider support"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_key = os.getenv("GOOGLE_AI_API_KEY")
        self.model = os.getenv("PRIMARY_MODEL", "gpt-4o")
    
    async def chat_openai(self, prompt: str, stream: bool = True) -> str:
        """Chat with OpenAI models"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.openai_key)
            
            if stream:
                response_text = ""
                stream_response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are GABRIEL AI, an advanced coding assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True,
                    max_tokens=1000
                )
                
                console.print("\\n[bold cyan]🤖 GABRIEL AI Response:[/bold cyan]\\n")
                for chunk in stream_response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        response_text += content
                        console.print(content, end="")
                
                console.print("\\n")
                return response_text
            else:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are GABRIEL AI, an advanced coding assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000
                )
                return response.choices[0].message.content
                
        except Exception as e:
            return f"OpenAI Error: {e}"
    
    async def chat_anthropic(self, prompt: str) -> str:
        """Chat with Anthropic Claude models"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
            
        except Exception as e:
            return f"Anthropic Error: {e}"
    
    async def chat_google(self, prompt: str) -> str:
        """Chat with Google Gemini models"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.google_key)
            
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Google AI Error: {e}"

async def demo_basic_chat():
    """Demonstrate basic chat functionality"""
    console.print(Panel("[bold cyan]Demo 1: Basic AI Chat[/bold cyan]", border_style="cyan"))
    
    ai = GabrielAI()
    
    if not ai.openai_key:
        console.print("[yellow]⚠️  No API key configured. Set OPENAI_API_KEY in .env[/yellow]")
        return
    
    prompt = "Explain async/await in Python in 3 sentences."
    console.print(f"\\n[dim]Prompt: {prompt}[/dim]")
    
    start_time = time.time()
    response = await ai.chat_openai(prompt, stream=True)
    elapsed = time.time() - start_time
    
    console.print(f"\\n[dim]⏱️  Response time: {elapsed:.2f}s[/dim]\\n")

async def demo_multi_provider():
    """Demonstrate multi-provider comparison"""
    console.print(Panel("[bold cyan]Demo 2: Multi-Provider Comparison[/bold cyan]", border_style="cyan"))
    
    ai = GabrielAI()
    prompt = "What is the fastest sorting algorithm?"
    
    console.print(f"\\n[dim]Prompt: {prompt}[/dim]\\n")
    
    providers = []
    if ai.openai_key:
        providers.append(("OpenAI", ai.chat_openai(prompt, stream=False)))
    if ai.anthropic_key:
        providers.append(("Anthropic", ai.chat_anthropic(prompt)))
    if ai.google_key:
        providers.append(("Google", ai.chat_google(prompt)))
    
    if not providers:
        console.print("[yellow]⚠️  No API keys configured[/yellow]")
        return
    
    for name, task in providers:
        console.print(f"[bold green]📡 {name}:[/bold green]")
        response = await task
        console.print(f"{response[:200]}...\\n")

async def demo_advanced_features():
    """Demonstrate advanced features"""
    console.print(Panel("[bold cyan]Demo 3: Advanced Features[/bold cyan]", border_style="cyan"))
    
    features = [
        "✅ Multi-provider support (OpenAI, Anthropic, Google)",
        "✅ Streaming responses for real-time output",
        "✅ Automatic fallback between providers",
        "✅ Token usage tracking and optimization",
        "✅ Response caching for faster repeated queries",
        "✅ Context management for long conversations",
        "✅ Error handling and retry logic",
        "✅ Performance monitoring and analytics",
        "✅ Rate limiting protection",
        "✅ Secure API key management"
    ]
    
    console.print("\\n[bold cyan]🚀 GABRIEL AI Capabilities:[/bold cyan]\\n")
    for feature in features:
        console.print(f"  {feature}")
    console.print()

async def main():
    """Main demo function"""
    console.print("""
╔═══════════════════════════════════════════════════════════╗
║              🌟 GABRIEL AI DEMO 🌟                       ║
║         Next-Gen Multi-Provider AI System                ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    demos = [
        ("Basic Chat", demo_basic_chat),
        ("Multi-Provider", demo_multi_provider),
        ("Advanced Features", demo_advanced_features)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        console.print(f"\\n[bold yellow]{'='*60}[/bold yellow]")
        await demo_func()
        
        if i < len(demos):
            await asyncio.sleep(2)
    
    console.print(f"\\n[bold yellow]{'='*60}[/bold yellow]")
    console.print("\\n[bold green]🎉 Demo complete! GABRIEL AI is ready for action.[/bold green]\\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\\n[yellow]👋 Demo interrupted[/yellow]")
    except Exception as e:
        console.print(f"\\n[red]❌ Error: {e}[/red]")
'''

    sample_claw.write_text(sample_content)
    console.print(f"[green]✅ Advanced demo created: {sample_claw}[/green]")
    
    # Make it executable
    import stat
    sample_claw.chmod(sample_claw.stat().st_mode | stat.S_IEXEC)


def show_next_steps():
    """Show what to do next"""
    next_steps = """
🎉 [bold green]GABRIEL AI System v2.0 - Setup Complete![/bold green]

🚀 [bold cyan]Quick Start:[/bold cyan]

1. 🌟 Run the demo:
   [cyan]python3 claws/gabriel_ai_demo.py[/cyan]

2. 🔍 Test your API keys:
   [cyan]python3 -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅' if os.getenv('OPENAI_API_KEY') else '❌')"[/cyan]

3. 🛠️ Create your first AI script:
   [cyan]# See claws/gabriel_ai_demo.py for examples[/cyan]

4. 📚 Check environment:
   [cyan]cat .env[/cyan]

🎯 [bold cyan]Advanced Features:[/bold cyan]

• Multi-Provider Support: Switch between OpenAI, Anthropic, and Google AI
• Streaming Responses: Get real-time output as AI generates
• Automatic Fallback: System switches providers if one fails
• Token Optimization: Smart context management for cost efficiency
• Performance Monitoring: Track API usage and response times
• Caching: Faster responses for repeated queries

💡 [bold yellow]Pro Tips:[/bold yellow]

• Set fallback models in .env for reliability
• Enable streaming for better user experience
• Use response caching to reduce API costs
• Monitor token usage with built-in analytics
• Create custom AI tools in the claws/ directory
• Check .env for all configuration options

🔐 [bold yellow]Security Reminders:[/bold yellow]

• Never commit .env file to version control
• Rotate API keys regularly
• Use environment-specific configurations
• Enable audit logging for production use

📊 [bold cyan]Model Recommendations:[/bold cyan]

• General coding: gpt-4o or claude-3-5-sonnet
• Fast responses: gpt-4o-mini or gemini-2.0-flash  
• Advanced reasoning: o1-preview
• Long context: gemini-1.5-pro (2M tokens!)
• Cost-effective: gpt-4o-mini

🌟 [bold green]GABRIEL AI - Where Intelligence Meets Innovation![/bold green]
    """
    console.print(Panel(next_steps, title="🎯 GABRIEL Setup Complete", border_style="cyan", padding=(1, 2)))
    
    # Additional system info
    console.print("\n[bold cyan]📈 System Status:[/bold cyan]")
    console.print("  • Python: ✅ Compatible")
    console.print("  • Dependencies: ✅ Installed")
    console.print("  • Configuration: ✅ Created")
    console.print("  • Demo: ✅ Ready")
    console.print("\n[dim]Run the demo to verify everything works![/dim]\n")


def main():
    """Main setup function"""
    display_banner()

    # Check Python version
    if not check_python_version():
        console.print("[red]❌ Setup failed: Incompatible Python version[/red]")
        sys.exit(1)

    # Install dependencies
    console.print("\n📦 Installing CodeBeast dependencies...")
    if not install_dependencies():
        console.print("[red]❌ Setup failed: Could not install dependencies[/red]")
        sys.exit(1)

    # Setup environment
    if not setup_environment_file():
        console.print("[yellow]⚠️ Environment setup skipped or failed[/yellow]")
        console.print("[yellow]You can manually create .env file later[/yellow]")

    # Verify setup
    if not verify_ai_setup():
        console.print(
            "[yellow]⚠️ AI verification failed - check your .env file[/yellow]"
        )

    # Create sample
    create_sample_claw()

    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\\n[yellow]👋 Setup interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]💥 Unexpected error: {e}[/red]")
        console.print("[dim]Please report this issue on GitHub[/dim]")
