"""
Network panel component for OverWatch dashboard.
"""

from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any


def render(data: Dict[str, Any]) -> Panel:
    """
    Render network information as a Rich panel.
    
    Args:
        data: Network data from core.network.get()
        
    Returns:
        Rich Panel object
    """
    if "error" in data:
        return Panel(f"[red]Error: {data['error']}[/red]", title="🔴 Network", border_style="red")
    
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Label", style="bright_green")
    table.add_column("Value", style="bright_white")
    
    # Total bandwidth
    total = data.get("io_total", {})
    if total:
        table.add_row(
            "Total Sent",
            f"{total.get('mb_sent', 0):.2f} MB ({total.get('packets_sent', 0):,} packets)"
        )
        table.add_row(
            "Total Received",
            f"{total.get('mb_recv', 0):.2f} MB ({total.get('packets_recv', 0):,} packets)"
        )
    
    # Connections
    connections = data.get("connections", {})
    if connections:
        table.add_row(
            "Connections",
            f"{connections.get('total', 0)} total, {connections.get('established', 0)} established"
        )
    
    # Active interfaces (top 3)
    io_per_interface = data.get("io_per_interface", {})
    if io_per_interface:
        table.add_row("", "")  # Spacer
        table.add_row("[bold]Active Interfaces[/bold]", "")
        
        # Sort by total traffic
        sorted_interfaces = sorted(
            io_per_interface.items(),
            key=lambda x: x[1].get('bytes_sent', 0) + x[1].get('bytes_recv', 0),
            reverse=True
        )
        
        for name, stats in sorted_interfaces[:3]:
            table.add_row(
                f"  {name}",
                f"↓ {stats.get('mb_recv', 0):.1f} MB  ↑ {stats.get('mb_sent', 0):.1f} MB"
            )
    
    return Panel(table, title="🌐 Network", border_style="bright_green")
