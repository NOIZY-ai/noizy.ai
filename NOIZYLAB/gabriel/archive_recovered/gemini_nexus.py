#!/usr/bin/env python3
"""
⚡ GEMINI NEXUS - The Infinite Terminal Interface
Interact with Google's Gemini models directly from your console.
"""

import sys, os, time
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
import google.generativeai as genai

console = Console()

def setup_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        console.print(Panel("⚠️  Gemini API Key Needed", style="yellow"))
        key = Prompt.ask("Enter your Google AI Studio API Key")
        if not key: return None
        os.environ["GEMINI_API_KEY"] = key
    return key

def animate_thought():
    with console.status("[bold blue]Gemini is thinking...", spinner="dots"):
        pass

def main():
    console.clear()
    console.print(Panel.fit("[bold cyan]⚡ GEMINI NEXUS[/bold cyan] [dim]// OMEGA INTERFACE[/dim]", border_style="cyan"))
    
    key = setup_key()
    if not key:
        console.print("[red]API Key required to proceed.[/red]")
        return

    try:
        genai.configure(api_key=key)
        # model = genai.GenerativeModel('gemini-1.5-pro-latest') 
        # Fallback to flash if pro not available or reliable
        model = genai.GenerativeModel('gemini-1.5-flash') 
        chat = model.start_chat(history=[])
        
        console.print("[green]✅ Connected to Gemini 1.5 Flash[/green]")
        console.print("[dim]Type 'exit' to quit. Type 'clear' to clear screen.[/dim]\n")

        while True:
            user_input = Prompt.ask("\n[bold cyan]YOU[/bold cyan]")
            
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'clear':
                console.clear()
                console.print(Panel.fit("[bold cyan]⚡ GEMINI NEXUS[/bold cyan]", border_style="cyan"))
                continue
                
            if not user_input.strip(): continue

            with console.status("[bold blue]Thinking...[/bold blue]", spinner="dots"):
                try:
                    response = chat.send_message(user_input, stream=True)
                    console.print("\n[bold magenta]GEMINI[/bold magenta]")
                    
                    full_text = ""
                    for chunk in response:
                        if chunk.text:
                            print(chunk.text, end="", flush=True)
                            full_text += chunk.text
                    print() # Newline
                    
                    # Store history if managing manually, but chat object handles it
                except Exception as e:
                    console.print(f"\n[red]Error: {e}[/red]")

    except Exception as e:
        console.print(f"[bold red]System Error: {e}[/bold red]")

if __name__ == "__main__":
    main()
