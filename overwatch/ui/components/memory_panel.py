"""
Memory panel component for OverWatch dashboard.
"""

from rich.panel import Panel
from rich.table import Table
from rich.progress import BarColumn, Progress
from typing import Dict, Any


def render(data: Dict[str, Any]) -> Panel:
    """
    Render memory information as a Rich panel.
    
    Args:
        data: Memory data from core.memory.get()
        
    Returns:
        Rich Panel object
    """
    if "error" in data:
        return Panel(f"[red]Error: {data['error']}[/red]", title="🔴 Memory", border_style="red")
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="white")
    
    ram = data.get("ram", {})
    swap = data.get("swap", {})
    
    # RAM usage
    ram_percent = ram.get("percent", 0)
    ram_color = "green" if ram_percent < 50 else "yellow" if ram_percent < 80 else "red"
    table.add_row(
        "RAM Usage",
        f"[{ram_color}]{ram_percent}%[/{ram_color}] - {ram.get('used_gb', 0):.2f} GB / {ram.get('total_gb', 0):.2f} GB"
    )
    table.add_row(
        "RAM Available",
        f"{ram.get('available_gb', 0):.2f} GB"
    )
    
    # Swap usage
    swap_percent = swap.get("percent", 0)
    swap_color = "green" if swap_percent < 50 else "yellow" if swap_percent < 80 else "red"
    if swap.get("total_gb", 0) > 0:
        table.add_row(
            "Swap Usage",
            f"[{swap_color}]{swap_percent}%[/{swap_color}] - {swap.get('used_gb', 0):.2f} GB / {swap.get('total_gb', 0):.2f} GB"
        )
    else:
        table.add_row("Swap Usage", "[dim]No swap configured[/dim]")
    
    return Panel(table, title="🧠 Memory", border_style="blue")
