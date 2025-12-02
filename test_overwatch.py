#!/usr/bin/env python3
"""
Quick test script for OverWatch.
Tests all core modules and displays sample output.
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def test_imports():
    """Test that all modules can be imported."""
    console.print("[cyan]Testing imports...[/cyan]")
    try:
        from overwatch.core import cpu, memory, disk, network, processes, sensors
        from overwatch.ui import dashboard
        from overwatch.alerts import manager
        from overwatch.api import server
        from overwatch.utils import loader, system_info
        console.print("[green]✓ All modules imported successfully[/green]\n")
        return True
    except ImportError as e:
        console.print(f"[red]✗ Import error: {e}[/red]\n")
        return False

def test_monitoring():
    """Test monitoring modules."""
    console.print("[cyan]Testing monitoring modules...[/cyan]")
    
    from overwatch.core import cpu, memory, disk, network, processes
    
    table = Table(title="System Metrics Sample")
    table.add_column("Module", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Sample Data", style="white")
    
    # CPU
    try:
        cpu_data = cpu.get()
        table.add_row("CPU", "✓", f"{cpu_data.get('total', 0)}%")
    except Exception as e:
        table.add_row("CPU", "✗", str(e))
    
    # Memory
    try:
        mem_data = memory.get()
        table.add_row("Memory", "✓", f"{mem_data['ram']['percent']}%")
    except Exception as e:
        table.add_row("Memory", "✗", str(e))
    
    # Disk
    try:
        disk_data = disk.get()
        table.add_row("Disk", "✓", f"{len(disk_data.get('partitions', []))} partitions")
    except Exception as e:
        table.add_row("Disk", "✗", str(e))
    
    # Network
    try:
        net_data = network.get()
        table.add_row("Network", "✓", f"{len(net_data.get('io_per_interface', {}))} interfaces")
    except Exception as e:
        table.add_row("Network", "✗", str(e))
    
    # Processes
    try:
        proc_data = processes.get(limit=5)
        table.add_row("Processes", "✓", f"{proc_data.get('total_count', 0)} total")
    except Exception as e:
        table.add_row("Processes", "✗", str(e))
    
    console.print(table)
    console.print()

def test_system_info():
    """Test system info module."""
    console.print("[cyan]Testing system info...[/cyan]")
    
    from overwatch.utils.system_info import get_system_info
    
    try:
        info = get_system_info()
        table = Table(title="System Information")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        for key, value in list(info.items())[:5]:
            table.add_row(key, str(value))
        
        console.print(table)
        console.print("[green]✓ System info retrieved successfully[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]\n")

def test_plugins():
    """Test plugin loader."""
    console.print("[cyan]Testing plugin system...[/cyan]")
    
    from overwatch.utils.loader import PluginLoader
    
    try:
        loader = PluginLoader()
        loader.load_all_plugins()
        plugins = loader.list_plugins()
        
        if plugins:
            console.print(f"[green]✓ Loaded {len(plugins)} plugin(s)[/green]")
            for plugin in plugins:
                console.print(f"  - {plugin['name']} v{plugin['version']}")
        else:
            console.print("[yellow]⚠ No plugins loaded[/yellow]")
        console.print()
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]\n")

def main():
    """Run all tests."""
    console.print(Panel.fit(
        "[bold cyan]OverWatch Test Suite[/bold cyan]\n"
        "Testing all components...",
        border_style="cyan"
    ))
    console.print()
    
    # Run tests
    if not test_imports():
        console.print("[red]Failed to import modules. Please install dependencies:[/red]")
        console.print("[yellow]pip install -e .[/yellow]")
        sys.exit(1)
    
    test_monitoring()
    test_system_info()
    test_plugins()
    
    console.print(Panel.fit(
        "[bold green]✓ All tests completed![/bold green]\n\n"
        "To start OverWatch:\n"
        "  [cyan]overwatch start[/cyan]     - Launch dashboard\n"
        "  [cyan]overwatch api[/cyan]       - Start API server\n"
        "  [cyan]overwatch --help[/cyan]    - Show all commands",
        border_style="green"
    ))

if __name__ == "__main__":
    main()
