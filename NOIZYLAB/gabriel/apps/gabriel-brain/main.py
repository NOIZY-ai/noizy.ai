# 🤖 SYSTEM FILE: main.py
# Optimized by Healer Drone

import asyncio
import typer
from src.sentience import SentienceLoop

app = typer.Typer()

@app.command()
def start():
    """
    Ignite the Gabriel Sentience Loop.
    """
    loop = SentienceLoop()
    try:
        asyncio.run(loop.run_forever())
    except KeyboardInterrupt:
        print("\nGabriel Sleeping.")

if __name__ == "__main__":
    app()
