"""
CPU panel component for OverWatch dashboard.
"""

from rich.panel import Panel
from rich.table import Table
from rich.progress import BarColumn, Progress
from rich.text import Text
from typing import Dict, Any


def render(data: Dict[str, Any]) -> Panel:
    """
    Render CPU information as a Rich panel.
    
    Args:
        data: CPU data from core.cpu.get()
        
    Returns:
        Rich Panel object
    """
    if "error" in data:
        return Panel(f"[red]Error: {data['error']}[/red]", title="🔴 CPU", border_style="red")
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Label", style="cyan")
    table.add_column("Value", style="white")
    
    # Overall CPU usage
    total = data.get("total", 0)
    color = "green" if total < 50 else "yellow" if total < 80 else "red"
    table.add_row("Overall Usage", f"[{color}]{total}%[/{color}]")
    
    # Core count
    table.add_row(
        "Cores",
        f"{data.get('count_physical', 0)} physical / {data.get('count_logical', 0)} logical"
    )
    
    # Frequency
    freq = data.get("frequency", {})
    if freq.get("current"):
        table.add_row(
            "Frequency",
            f"{freq['current']:.0f} MHz (min: {freq.get('min', 0):.0f}, max: {freq.get('max', 0):.0f})"
        )
    
    # Per-core usage
    per_core = data.get("per_core", [])
    if per_core:
        cores_display = ", ".join([f"{c:.0f}%" for c in per_core[:8]])  # Show first 8 cores
        if len(per_core) > 8:
            cores_display += f" ... ({len(per_core)} cores total)"
        table.add_row("Core Usage", cores_display)
    
    return Panel(table, title="💻 CPU", border_style="blue")
