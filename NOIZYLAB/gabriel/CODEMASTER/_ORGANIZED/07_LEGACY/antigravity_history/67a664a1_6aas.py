import asyncio
from rich.console import Console
from .reflector import ReflectorAgent

console = Console()

class SentienceLoop:
    """
    The Event-Driven Core of Gabriel (2026).
    Manages concurrent Listen (Ears), Think (Brain), and Act (Hands) loops.
    """
    def __init__(self):
        self.reflector = ReflectorAgent()
        self.state = "IDLE"
        self.short_term_memory = [] # Hot Cache

    async def listen_pulse(self):
        """ The Ears: WebAudio/Whisper Stream """
        while True:
            # await asyncio.sleep(0.1) # Simulate polling 10Hz
            # Check for OSC/Websocket messages
            await asyncio.sleep(1) 

    async def think_pulse(self):
        """ The Brain: MLX Speculative Decoding """
        while True:
            if self.state == "THINK":
                console.print("[bold purple]GABRIEL BRAIN[/bold purple]: Speculating tokens...")
                await asyncio.sleep(0.5) 
                self.state = "IDLE" # Return to idle after thought
            await asyncio.sleep(0.1)

    async def maintenance_pulse(self):
        """ The Janitor: Reflector Loop """
        while True:
            # Simulate random entropy check
            # await self.reflector.analyze_error("test_error", "sentience_core")
            await asyncio.sleep(60) # Run every minute

    async def run_forever(self):
        console.print("[bold cyan]GABRIEL SENTIENCE LOOP INITIALIZED[/bold cyan] (M2 Ultra Native)")
        console.print("[dim] systems: reflector=active, mlx=standby, osc=listening[/dim]")
        
        await asyncio.gather(
            self.listen_pulse(),
            self.think_pulse(),
            self.maintenance_pulse()
        )

if __name__ == "__main__":
    loop = SentienceLoop()
    asyncio.run(loop.run_forever())
