"""
Disk panel component for OverWatch dashboard.
"""

from rich.panel import Panel
from rich.table import Table
from typing import Dict, Any


def render(data: Dict[str, Any]) -> Panel:
    """
    Render disk information as a Rich panel.
    
    Args:
        data: Disk data from core.disk.get()
        
    Returns:
        Rich Panel object
    """
    if "error" in data:
        return Panel(f"[red]Error: {data['error']}[/red]", title="🔴 Disk", border_style="red")
    
    partitions = data.get("partitions", [])
    
    if not partitions:
        return Panel("[yellow]No disk partitions found[/yellow]", title="💾 Disk", border_style="bright_blue")
    
    table = Table(show_header=True, box=None, padding=(0, 1))
    table.add_column("Mount", style="bright_yellow")
    table.add_column("Type", style="dim")
    table.add_column("Usage", style="bright_white")
    table.add_column("Free", style="bright_green")
    
    for partition in partitions[:5]:  # Show first 5 partitions
        percent = partition.get("percent", 0)
        color = "bright_green" if percent < 70 else "bright_yellow" if percent < 90 else "bright_red"
        
        table.add_row(
            partition.get("mountpoint", ""),
            partition.get("fstype", ""),
            f"[{color}]{percent}%[/{color}] ({partition.get('used_gb', 0):.1f}/{partition.get('total_gb', 0):.1f} GB)",
            f"{partition.get('free_gb', 0):.1f} GB"
        )
    
    # Disk I/O
    io = data.get("io", {})
    io_info = ""
    if io:
        io_info = f"\n📊 I/O: ↓ {io.get('read_mb', 0):.0f} MB  ↑ {io.get('write_mb', 0):.0f} MB"
    
    return Panel(
        table.grid() if not table.row_count else table,
        title="💾 Disk" + io_info,
        border_style="bright_blue"
    )
