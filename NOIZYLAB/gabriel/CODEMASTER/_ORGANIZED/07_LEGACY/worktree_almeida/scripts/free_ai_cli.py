#!/usr/bin/env python3
"""
🆓 FREE AI CLI - NOIZYVOX
==========================
Maximum power, zero cost!

Supports:
- Groq (FREE - Llama 3.3 70B, Mixtral, Gemma)
- Google AI (FREE - Gemini)
- Together AI (FREE $25 credits)
- Hugging Face (FREE inference)

Usage:
  python free_ai_cli.py "your prompt"
  python free_ai_cli.py --interactive
  python free_ai_cli.py --model llama "your prompt"
  python free_ai_cli.py --provider google "your prompt"
"""

import os
import sys
import argparse
from typing import Optional, Generator

# =============================================================================
# 🆓 FREE PROVIDERS CONFIGURATION
# =============================================================================

PROVIDERS = {
    "groq": {
        "name": "Groq",
        "env_key": "GROQ_API_KEY",
        "models": {
            "llama": "llama-3.3-70b-versatile",      # Best free model!
            "llama-small": "llama-3.1-8b-instant",   # Faster
            "mixtral": "mixtral-8x7b-32768",         # Good for code
            "gemma": "gemma2-9b-it",                 # Google's model
        },
        "default": "llama",
        "url": "https://console.groq.com/keys",
    },
    "google": {
        "name": "Google AI",
        "env_key": "GOOGLE_API_KEY",
        "models": {
            "gemini": "gemini-1.5-flash",
            "gemini-pro": "gemini-1.5-pro",
        },
        "default": "gemini",
        "url": "https://aistudio.google.com/apikey",
    },
    "together": {
        "name": "Together AI",
        "env_key": "TOGETHER_API_KEY",
        "models": {
            "llama": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "qwen": "Qwen/Qwen2.5-72B-Instruct-Turbo",
            "deepseek": "deepseek-ai/DeepSeek-V3",
        },
        "default": "llama",
        "url": "https://api.together.xyz/settings/api-keys",
    },
    "huggingface": {
        "name": "Hugging Face",
        "env_key": "HUGGINGFACE_TOKEN",
        "models": {
            "zephyr": "HuggingFaceH4/zephyr-7b-beta",
            "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
        },
        "default": "zephyr",
        "url": "https://huggingface.co/settings/tokens",
    },
}

# =============================================================================
# 🚀 PROVIDER IMPLEMENTATIONS
# =============================================================================

def chat_groq(prompt: str, model: str = "llama", stream: bool = False, system: str = None) -> str:
    """Chat using Groq (FREE!)."""
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Get free key at: https://console.groq.com/keys")
    
    client = Groq(api_key=api_key)
    model_id = PROVIDERS["groq"]["models"].get(model, model)
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    if stream:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4096,
            stream=True,
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print()
        return full_response
    else:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4096,
        )
        return response.choices[0].message.content


def chat_google(prompt: str, model: str = "gemini", stream: bool = False, system: str = None) -> str:
    """Chat using Google AI (FREE!)."""
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set. Get free key at: https://aistudio.google.com/apikey")
    
    genai.configure(api_key=api_key)
    model_id = PROVIDERS["google"]["models"].get(model, model)
    
    model_obj = genai.GenerativeModel(model_id)
    
    full_prompt = prompt
    if system:
        full_prompt = f"{system}\n\n{prompt}"
    
    if stream:
        response = model_obj.generate_content(full_prompt, stream=True)
        full_response = ""
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
        print()
        return full_response
    else:
        response = model_obj.generate_content(full_prompt)
        return response.text


def chat_together(prompt: str, model: str = "llama", stream: bool = False, system: str = None) -> str:
    """Chat using Together AI (FREE $25 credits!)."""
    from together import Together
    
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not set. Get free credits at: https://api.together.xyz/")
    
    client = Together(api_key=api_key)
    model_id = PROVIDERS["together"]["models"].get(model, model)
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    if stream:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4096,
            stream=True,
        )
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print()
        return full_response
    else:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4096,
        )
        return response.choices[0].message.content


def chat_huggingface(prompt: str, model: str = "zephyr", stream: bool = False, system: str = None) -> str:
    """Chat using Hugging Face (FREE!)."""
    from huggingface_hub import InferenceClient
    
    api_key = os.getenv("HUGGINGFACE_TOKEN")
    if not api_key:
        raise ValueError("HUGGINGFACE_TOKEN not set. Get free token at: https://huggingface.co/settings/tokens")
    
    client = InferenceClient(token=api_key)
    model_id = PROVIDERS["huggingface"]["models"].get(model, model)
    
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    if stream:
        full_response = ""
        for message in client.chat_completion(
            model=model_id,
            messages=messages,
            max_tokens=2048,
            stream=True,
        ):
            content = message.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content
        print()
        return full_response
    else:
        response = client.chat_completion(
            model=model_id,
            messages=messages,
            max_tokens=2048,
        )
        return response.choices[0].message.content


# Provider dispatch
CHAT_FUNCTIONS = {
    "groq": chat_groq,
    "google": chat_google,
    "together": chat_together,
    "huggingface": chat_huggingface,
}


# =============================================================================
# 🎯 SMART PROVIDER SELECTION
# =============================================================================

def get_available_providers() -> list:
    """Get list of providers with valid API keys."""
    available = []
    for provider, config in PROVIDERS.items():
        if os.getenv(config["env_key"]):
            available.append(provider)
    return available


def get_best_provider() -> Optional[str]:
    """Get the best available free provider."""
    # Priority order: groq > together > google > huggingface
    priority = ["groq", "together", "google", "huggingface"]
    for p in priority:
        if os.getenv(PROVIDERS[p]["env_key"]):
            return p
    return None


def chat(prompt: str, provider: str = None, model: str = None, stream: bool = False, system: str = None) -> str:
    """Universal chat function - auto-selects best free provider."""
    if provider is None:
        provider = get_best_provider()
    
    if provider is None:
        print("❌ No API keys configured!")
        print("\n🆓 Get FREE API keys:")
        for p, config in PROVIDERS.items():
            status = "✅" if os.getenv(config["env_key"]) else "❌"
            print(f"   {status} {config['name']}: {config['url']}")
        sys.exit(1)
    
    if provider not in CHAT_FUNCTIONS:
        print(f"❌ Unknown provider: {provider}")
        sys.exit(1)
    
    chat_fn = CHAT_FUNCTIONS[provider]
    model = model or PROVIDERS[provider]["default"]
    
    return chat_fn(prompt, model=model, stream=stream, system=system)


# =============================================================================
# 💬 INTERACTIVE MODE
# =============================================================================

def interactive_mode(provider: str = None, model: str = None, system: str = None):
    """Interactive chat session."""
    provider = provider or get_best_provider()
    if not provider:
        print("❌ No API keys configured!")
        return
    
    model = model or PROVIDERS[provider]["default"]
    model_id = PROVIDERS[provider]["models"].get(model, model)
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🆓 FREE AI CLI - NOIZYVOX                                                   ║
║  Provider: {PROVIDERS[provider]['name']:15} Model: {model_id[:30]:30}        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Commands: /quit, /clear, /model <name>, /provider <name>, /help

""")
    
    history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Commands
        if user_input.startswith("/"):
            cmd = user_input[1:].split()
            if cmd[0] in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            elif cmd[0] == "clear":
                history = []
                print("🧹 History cleared")
                continue
            elif cmd[0] == "model" and len(cmd) > 1:
                model = cmd[1]
                print(f"✅ Model set to: {model}")
                continue
            elif cmd[0] == "provider" and len(cmd) > 1:
                if cmd[1] in PROVIDERS:
                    provider = cmd[1]
                    model = PROVIDERS[provider]["default"]
                    print(f"✅ Provider: {provider}, Model: {model}")
                else:
                    print(f"❌ Unknown provider. Available: {', '.join(PROVIDERS.keys())}")
                continue
            elif cmd[0] == "help":
                print("""
Commands:
  /quit, /q      - Exit
  /clear         - Clear history
  /model <name>  - Change model
  /provider <n>  - Change provider
  /help          - Show this help

Models by provider:""")
                for p, config in PROVIDERS.items():
                    if os.getenv(config["env_key"]):
                        print(f"  {p}: {', '.join(config['models'].keys())}")
                continue
        
        # Chat
        print("\nAI: ", end="")
        try:
            response = chat(user_input, provider=provider, model=model, stream=True, system=system)
            history.append({"user": user_input, "ai": response})
        except Exception as e:
            print(f"\n❌ Error: {e}")
        print()


# =============================================================================
# 📊 STATUS CHECK
# =============================================================================

def show_status():
    """Show status of all free providers."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🆓 FREE AI PROVIDERS STATUS                                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    for provider, config in PROVIDERS.items():
        key = os.getenv(config["env_key"])
        status = "✅ CONFIGURED" if key else "❌ Not set"
        
        if key:
            masked = key[:8] + "..." + key[-4:]
        else:
            masked = "—"
        
        print(f"  {config['name']:15} {status:15} {masked}")
        print(f"    Models: {', '.join(config['models'].keys())}")
        if not key:
            print(f"    🔗 {config['url']}")
        print()
    
    best = get_best_provider()
    if best:
        print(f"  🚀 Best available: {PROVIDERS[best]['name']}")
    else:
        print("  ⚠️  No providers configured! Get free keys above.")


# =============================================================================
# 🚀 MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🆓 FREE AI CLI - Maximum power, zero cost!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python free_ai_cli.py "Explain quantum computing"
  python free_ai_cli.py --stream "Write a poem"
  python free_ai_cli.py --model mixtral "Review this code"
  python free_ai_cli.py --provider google "Hello!"
  python free_ai_cli.py --interactive
  python free_ai_cli.py --status

Models:
  groq:      llama, llama-small, mixtral, gemma
  google:    gemini, gemini-pro
  together:  llama, qwen, deepseek
  huggingface: zephyr, mistral
        """
    )
    
    parser.add_argument("prompt", nargs="*", help="The prompt to send")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-s", "--stream", action="store_true", help="Stream response")
    parser.add_argument("-p", "--provider", choices=list(PROVIDERS.keys()), help="Provider to use")
    parser.add_argument("-m", "--model", help="Model to use")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--status", action="store_true", help="Show provider status")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    
    args = parser.parse_args()
    
    # Status check
    if args.status:
        show_status()
        return
    
    # List models
    if args.list_models:
        print("\n🆓 Available FREE Models:\n")
        for provider, config in PROVIDERS.items():
            key = os.getenv(config["env_key"])
            status = "✅" if key else "❌"
            print(f"{status} {config['name']}:")
            for alias, model_id in config["models"].items():
                print(f"    {alias:15} → {model_id}")
            print()
        return
    
    # Interactive mode
    if args.interactive:
        interactive_mode(provider=args.provider, model=args.model, system=args.system)
        return
    
    # Single prompt
    if args.prompt:
        prompt = " ".join(args.prompt)
        response = chat(
            prompt,
            provider=args.provider,
            model=args.model,
            stream=args.stream,
            system=args.system
        )
        if not args.stream:
            print(response)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
