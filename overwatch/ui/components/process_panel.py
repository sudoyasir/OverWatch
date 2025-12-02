"""
Process panel component for OverWatch dashboard.
"""

from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any


def render(data: Dict[str, Any]) -> Panel:
    """
    Render process information as a Rich panel.
    
    Args:
        data: Process data from core.processes.get()
        
    Returns:
        Rich Panel object
    """
    if "error" in data:
        return Panel(f"[red]Error: {data['error']}[/red]", title="🔴 Processes", border_style="red")
    
    processes = data.get("processes", [])
    total_count = data.get("total_count", 0)
    
    if not processes:
        return Panel(
            "[yellow]No processes found[/yellow]",
            title=f"⚙️  Processes (Total: {total_count})",
            border_style="blue"
        )
    
    table = Table(show_header=True, box=None, padding=(0, 1))
    table.add_column("PID", style="dim", width=8)
    table.add_column("Name", style="cyan", width=25)
    table.add_column("CPU%", style="yellow", width=8)
    table.add_column("MEM%", style="green", width=8)
    table.add_column("User", style="magenta", width=15)
    
    for proc in processes[:10]:  # Show top 10 processes
        name = proc.get("name", "")
        if len(name) > 23:
            name = name[:20] + "..."
        
        cpu = proc.get("cpu_percent", 0)
        mem = proc.get("memory_percent", 0)
        
        cpu_color = "red" if cpu > 50 else "yellow" if cpu > 20 else "white"
        mem_color = "red" if mem > 50 else "yellow" if mem > 20 else "white"
        
        table.add_row(
            str(proc.get("pid", "")),
            name,
            f"[{cpu_color}]{cpu:.1f}[/{cpu_color}]",
            f"[{mem_color}]{mem:.1f}[/{mem_color}]",
            proc.get("username", "")[:15]
        )
    
    return Panel(
        table,
        title=f"⚙️  Top Processes (Total: {total_count})",
        border_style="blue"
    )
