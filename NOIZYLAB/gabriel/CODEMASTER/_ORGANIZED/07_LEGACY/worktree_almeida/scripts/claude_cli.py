#!/usr/bin/env python3
"""
🤖 Claude CLI - Simple command-line interface for Claude

A lightweight CLI for interacting with Claude AI models.

Usage:
  # Single prompt
  claude-cli "Explain quantum computing in simple terms"
  
  # With options
  claude-cli --model claude-3-opus-20240229 --max-tokens 1000 --temperature 0.7 "Write a haiku about AI"
  
  # Batch mode
  claude-cli --file prompts.txt --output responses.csv
  
  # Streaming output
  claude-cli --stream "Tell me a story"
  
  # System prompt
  claude-cli --system "You are a pirate" "What's the weather like?"
  
  # JSON output
  claude-cli --json "List 3 programming languages"
  
  # Conversation mode (interactive)
  claude-cli --interactive

Requirements:
  pip install anthropic

Environment:
  ANTHROPIC_API_KEY - Your Anthropic API key
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# =============================================================================
# Configuration
# =============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model aliases for convenience
MODEL_ALIASES = {
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-sonnet-4-20250514",
    "sonnet-3.5": "claude-3-5-sonnet-20241022",
    "haiku": "claude-3-5-haiku-20241022",
    "haiku-3": "claude-3-haiku-20240307",
    "default": "claude-sonnet-4-20250514",
}

# Default settings
DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 1.0

# =============================================================================
# Claude Client
# =============================================================================

def get_client() -> "anthropic.Anthropic":
    """Initialize and return the Anthropic client."""
    if not HAS_ANTHROPIC:
        print("❌ Error: anthropic package not installed")
        print("   Run: pip install anthropic")
        sys.exit(1)
    
    if not ANTHROPIC_API_KEY:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("   Export your API key: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def resolve_model(model_name: str) -> str:
    """Resolve model alias to full model name."""
    return MODEL_ALIASES.get(model_name.lower(), model_name)


def send_message(
    prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    system: Optional[str] = None,
    stream: bool = False,
    json_mode: bool = False,
) -> str:
    """Send a message to Claude and return the response."""
    client = get_client()
    model = resolve_model(model)
    
    # Build messages
    messages = [{"role": "user", "content": prompt}]
    
    # Build system prompt
    system_prompt = system or ""
    if json_mode and system_prompt:
        system_prompt += "\n\nRespond only with valid JSON, no markdown."
    elif json_mode:
        system_prompt = "Respond only with valid JSON, no markdown."
    
    # API call kwargs
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    
    # Only include temperature if not default (1.0)
    if temperature != 1.0:
        kwargs["temperature"] = temperature
    
    if stream:
        # Streaming response
        response_text = ""
        with client.messages.stream(**kwargs) as stream_response:
            for text in stream_response.text_stream:
                print(text, end="", flush=True)
                response_text += text
        print()  # Newline after streaming
        return response_text
    else:
        # Regular response
        response = client.messages.create(**kwargs)
        return response.content[0].text


def send_batch(
    prompts: List[str],
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    system: Optional[str] = None,
    progress: bool = True,
) -> List[Dict[str, Any]]:
    """Send multiple prompts and return responses."""
    results = []
    total = len(prompts)
    
    for i, prompt in enumerate(prompts, 1):
        if progress:
            print(f"Processing {i}/{total}...", file=sys.stderr)
        
        try:
            start_time = datetime.now()
            response = send_message(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                stream=False,
            )
            elapsed = (datetime.now() - start_time).total_seconds()
            
            results.append({
                "prompt": prompt,
                "response": response,
                "model": resolve_model(model),
                "elapsed_seconds": round(elapsed, 2),
                "status": "success",
            })
        except Exception as e:
            results.append({
                "prompt": prompt,
                "response": "",
                "model": resolve_model(model),
                "elapsed_seconds": 0,
                "status": f"error: {str(e)}",
            })
    
    return results


def interactive_mode(
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    system: Optional[str] = None,
) -> None:
    """Run interactive conversation mode."""
    client = get_client()
    model = resolve_model(model)
    
    print(f"🤖 Claude Interactive Mode ({model})")
    print("   Type 'quit' or 'exit' to end, 'clear' to reset conversation")
    print("-" * 60)
    
    messages = []
    
    while True:
        try:
            user_input = input("\n📝 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == "clear":
            messages = []
            print("🗑️  Conversation cleared")
            continue
        
        if user_input.lower() == "history":
            print(f"\n📜 Conversation history ({len(messages)} messages):")
            for msg in messages:
                role = "You" if msg["role"] == "user" else "Claude"
                preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                print(f"   {role}: {preview}")
            continue
        
        # Add user message
        messages.append({"role": "user", "content": user_input})
        
        # Build API kwargs
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        
        if system:
            kwargs["system"] = system
        
        if temperature != 1.0:
            kwargs["temperature"] = temperature
        
        try:
            print("\n🤖 Claude: ", end="", flush=True)
            response_text = ""
            
            with client.messages.stream(**kwargs) as stream_response:
                for text in stream_response.text_stream:
                    print(text, end="", flush=True)
                    response_text += text
            print()
            
            # Add assistant response to history
            messages.append({"role": "assistant", "content": response_text})
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            # Remove the failed user message
            messages.pop()


# =============================================================================
# File I/O
# =============================================================================

def read_prompts_file(file_path: Path) -> List[str]:
    """Read prompts from a file (one per line or JSON array)."""
    content = file_path.read_text().strip()
    
    # Try JSON array first
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return [str(p).strip() for p in data if str(p).strip()]
    except json.JSONDecodeError:
        pass
    
    # Fall back to line-by-line
    return [line.strip() for line in content.split("\n") if line.strip()]


def write_results_csv(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Write results to CSV file."""
    if not results:
        return
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


def write_results_json(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Write results to JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="🤖 Claude CLI - Simple command-line interface for Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple prompt
  %(prog)s "Explain quantum computing in simple terms"
  
  # With model and options
  %(prog)s --model opus --max-tokens 1000 --temperature 0.7 "Write a haiku"
  
  # Streaming output
  %(prog)s --stream "Tell me a story about a robot"
  
  # System prompt
  %(prog)s --system "You are a helpful pirate" "What's 2+2?"
  
  # JSON output
  %(prog)s --json "List 3 colors as a JSON array"
  
  # Batch mode
  %(prog)s --file prompts.txt --output responses.csv
  
  # Interactive conversation
  %(prog)s --interactive

Model Aliases:
  opus     → claude-3-opus-20240229
  sonnet   → claude-sonnet-4-20250514 (default)
  sonnet-3.5 → claude-3-5-sonnet-20241022
  haiku    → claude-3-5-haiku-20241022

Environment:
  ANTHROPIC_API_KEY - Your Anthropic API key (required)
        """
    )
    
    # Positional argument
    parser.add_argument(
        "prompt",
        nargs="?",
        help="The prompt to send to Claude"
    )
    
    # Model options
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"Model to use (default: {DEFAULT_MODEL}). Aliases: opus, sonnet, haiku"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=DEFAULT_MAX_TOKENS,
        help=f"Maximum tokens in response (default: {DEFAULT_MAX_TOKENS})"
    )
    
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=DEFAULT_TEMPERATURE,
        help=f"Temperature 0.0-1.0 (default: {DEFAULT_TEMPERATURE})"
    )
    
    # Output options
    parser.add_argument(
        "-s", "--stream",
        action="store_true",
        help="Stream the response"
    )
    
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Request JSON output"
    )
    
    parser.add_argument(
        "--system",
        help="System prompt to set context"
    )
    
    # Batch mode
    parser.add_argument(
        "-f", "--file",
        type=Path,
        help="File with prompts (one per line or JSON array)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file for results (.csv or .json)"
    )
    
    # Interactive mode
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive conversation mode"
    )
    
    # Misc
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="claude-cli 1.0.0 (NOIZYVOX)"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available model aliases"
    )
    
    args = parser.parse_args()
    
    # List models
    if args.list_models:
        print("📋 Available Model Aliases:")
        for alias, full_name in sorted(MODEL_ALIASES.items()):
            marker = " (default)" if alias == "default" else ""
            print(f"   {alias:12} → {full_name}{marker}")
        return
    
    # Interactive mode
    if args.interactive:
        interactive_mode(
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            system=args.system,
        )
        return
    
    # Batch mode
    if args.file:
        if not args.file.exists():
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        
        prompts = read_prompts_file(args.file)
        if not prompts:
            print("❌ Error: No prompts found in file")
            sys.exit(1)
        
        print(f"📄 Processing {len(prompts)} prompts...")
        
        results = send_batch(
            prompts=prompts,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            system=args.system,
        )
        
        # Output results
        if args.output:
            if args.output.suffix.lower() == ".json":
                write_results_json(results, args.output)
            else:
                write_results_csv(results, args.output)
            print(f"✅ Results saved to: {args.output}")
        else:
            # Print to stdout
            for r in results:
                print(f"\n--- Prompt: {r['prompt'][:50]}... ---")
                print(r["response"])
        
        # Summary
        success = sum(1 for r in results if r["status"] == "success")
        print(f"\n📊 Completed: {success}/{len(results)} successful")
        return
    
    # Single prompt mode
    if not args.prompt:
        # Check for piped input
        if not sys.stdin.isatty():
            args.prompt = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)
    
    if not args.prompt:
        print("❌ Error: No prompt provided")
        sys.exit(1)
    
    # Send single message
    try:
        response = send_message(
            prompt=args.prompt,
            model=args.model,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            system=args.system,
            stream=args.stream,
            json_mode=args.json,
        )
        
        if not args.stream:
            print(response)
        
    except Exception as e:
        if "APIError" in type(e).__name__:
            print(f"❌ API Error: {e}")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
