import typer
from rich.console import Console
from rich.table import Table
from src.audit import AudioAuditor
from pathlib import Path

app = typer.Typer()
console = Console()

@app.command()
def audit(file_path: str):
    """
    Run GABRIEL AUDIO AUDIT on a target file.
    Outputs LUFS, Peak, Width, and Brightness.
    """
    console.print(f"[bold cyan]GABRIEL CREATIVE ENGINE[/bold cyan]: Auditing {file_path}...")
    
    auditor = AudioAuditor()
    metrics = auditor.analyze(file_path)
    
    if "error" in metrics:
        console.print(f"[bold red]Error:[/bold red] {metrics['error']}")
        return

    table = Table(title="Audio Artifact Metrics")
    table.add_column("Metric", style="magenta")
    table.add_column("Value", style="green")

    for k, v in metrics.items():
        table.add_row(str(k), str(v))

    console.print(table)
    
    # MemCell Ingestion Hint
    console.print(f"\n[dim]Artifact MemCell Ready: {metrics['filename']} (Hash pending)[/dim]")

@app.command()
def version():
    console.print("Gabriel Creative Engine v1.0 [M2 Ultra Optimized]")

if __name__ == "__main__":
    app()
