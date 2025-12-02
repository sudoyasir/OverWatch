"""
CLI commands for OverWatch.
"""

import click
from overwatch.ui.dashboard import start_dashboard
from overwatch.api.server import start_server


@click.group()
@click.version_option(version="0.1.0", prog_name="OverWatch")
def cli():
    """
    OverWatch - Advanced System Monitoring Tool
    
    A powerful terminal-based system monitor with real-time dashboards,
    alerts, plugins, and API support.
    """
    pass


@cli.command()
@click.option(
    "--refresh",
    "-r",
    default=1.0,
    help="Refresh rate in seconds (default: 1.0)",
    type=float,
)
def start(refresh):
    """Start the OverWatch terminal dashboard."""
    click.echo(f"Starting OverWatch dashboard (refresh rate: {refresh}s)...")
    click.echo("Press Ctrl+C to exit")
    start_dashboard(refresh_rate=refresh)


@cli.command()
@click.option(
    "--host",
    "-h",
    default="0.0.0.0",
    help="Host address to bind to (default: 0.0.0.0)",
)
@click.option(
    "--port",
    "-p",
    default=8000,
    help="Port number to listen on (default: 8000)",
    type=int,
)
def api(host, port):
    """Start the OverWatch API server."""
    click.echo(f"Starting OverWatch API server on {host}:{port}...")
    click.echo(f"API documentation: http://{host}:{port}/docs")
    click.echo("Press Ctrl+C to exit")
    start_server(host=host, port=port)


@cli.command()
def version():
    """Show OverWatch version information."""
    import platform
    import sys
    
    click.echo("OverWatch v0.1.0")
    click.echo(f"Python: {sys.version}")
    click.echo(f"Platform: {platform.platform()}")
    click.echo(f"System: {platform.system()} {platform.release()}")


@cli.command()
def info():
    """Show system information."""
    from overwatch.utils.system_info import get_system_info
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    info = get_system_info()
    
    table = Table(title="System Information", show_header=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    for key, value in info.items():
        table.add_row(key, str(value))
    
    console.print(table)


@cli.command()
def plugins():
    """List available plugins."""
    from overwatch.utils.loader import PluginLoader
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    loader = PluginLoader()
    loader.load_all_plugins()  # Load plugins before listing
    plugin_list = loader.list_plugins()
    
    if not plugin_list:
        console.print("[yellow]No plugins found[/yellow]")
        return
    
    table = Table(title="Available Plugins", show_header=True)
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description", style="white")
    
    for plugin in plugin_list:
        table.add_row(
            plugin.get("name", "Unknown"),
            plugin.get("version", "N/A"),
            plugin.get("description", "No description"),
        )
    
    console.print(table)


@cli.command()
@click.option(
    "--format",
    "-f",
    default="json",
    type=click.Choice(["json", "yaml", "table"]),
    help="Output format (default: json)",
)
def metrics(format):
    """Display current system metrics."""
    from overwatch.core import cpu, memory, disk, network, processes
    from rich.console import Console
    from rich.json import JSON
    import json as json_lib
    
    console = Console()
    
    data = {
        "cpu": cpu.get(),
        "memory": memory.get(),
        "disk": disk.get(),
        "network": network.get(),
        "processes": processes.get(limit=5),
    }
    
    if format == "json":
        console.print(JSON(json_lib.dumps(data, indent=2)))
    elif format == "yaml":
        try:
            import yaml
            console.print(yaml.dump(data, default_flow_style=False))
        except ImportError:
            console.print("[red]PyYAML not installed. Using JSON format.[/red]")
            console.print(JSON(json_lib.dumps(data, indent=2)))
    elif format == "table":
        from rich.table import Table
        
        table = Table(title="System Metrics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("CPU Usage", f"{data['cpu']['total']}%")
        table.add_row("RAM Usage", f"{data['memory']['ram']['percent']}%")
        table.add_row("Swap Usage", f"{data['memory']['swap']['percent']}%")
        table.add_row("Processes", str(data['processes']['total_count']))
        
        console.print(table)


if __name__ == "__main__":
    cli()
