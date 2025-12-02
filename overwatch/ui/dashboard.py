"""
Dashboard UI for OverWatch.
Main terminal interface using Rich.
"""

import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from datetime import datetime

from overwatch.core import cpu, memory, disk, network, processes, sensors
from overwatch.ui.components import (
    cpu_panel,
    memory_panel,
    disk_panel,
    network_panel,
    process_panel,
)


class Dashboard:
    """Main dashboard class for OverWatch."""
    
    def __init__(self, refresh_rate: float = 1.0):
        """
        Initialize the dashboard.
        
        Args:
            refresh_rate: Refresh interval in seconds
        """
        self.console = Console()
        self.refresh_rate = refresh_rate
        self.plugin_data = []
    
    def create_layout(self) -> Layout:
        """
        Create the dashboard layout.
        
        Returns:
            Rich Layout object
        """
        layout = Layout()
        
        # Split into header and body
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
        )
        
        # Split body into left and right
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right"),
        )
        
        # Split left into top and bottom
        layout["left"].split_column(
            Layout(name="system", ratio=2),
            Layout(name="disk_net", ratio=1),
        )
        
        # Right side is processes
        layout["right"].split_column(
            Layout(name="processes"),
        )
        
        # Split system into CPU and Memory
        layout["system"].split_row(
            Layout(name="cpu"),
            Layout(name="memory"),
        )
        
        # Split disk_net
        layout["disk_net"].split_row(
            Layout(name="disk"),
            Layout(name="network"),
        )
        
        return layout
    
    def generate_header(self) -> Panel:
        """
        Generate the dashboard header.
        
        Returns:
            Rich Panel for header
        """
        title = Text()
        title.append("OverWatch", style="bold cyan")
        title.append(" - Advanced System Monitor", style="dim")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="right")
        grid.add_row(title, f"[dim]{timestamp}[/dim]")
        
        return Panel(grid, style="white on blue")
    
    def generate_content(self, layout: Layout):
        """
        Update layout with current system data.
        
        Args:
            layout: Layout to update
        """
        # Header
        layout["header"].update(self.generate_header())
        
        # CPU
        cpu_data = cpu.get()
        layout["cpu"].update(cpu_panel.render(cpu_data))
        
        # Memory
        memory_data = memory.get()
        layout["memory"].update(memory_panel.render(memory_data))
        
        # Disk
        disk_data = disk.get()
        layout["disk"].update(disk_panel.render(disk_data))
        
        # Network
        network_data = network.get()
        layout["network"].update(network_panel.render(network_data))
        
        # Processes
        process_data = processes.get(limit=10, sort_by="cpu")
        layout["processes"].update(process_panel.render(process_data))
    
    def add_plugin_data(self, plugin_name: str, content: str):
        """
        Add plugin output to dashboard.
        
        Args:
            plugin_name: Name of the plugin
            content: Plugin output content
        """
        self.plugin_data.append({
            "name": plugin_name,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def run(self):
        """Run the dashboard with live updates."""
        layout = self.create_layout()
        
        try:
            with Live(
                layout,
                console=self.console,
                screen=True,
                refresh_per_second=1 / self.refresh_rate
            ) as live:
                while True:
                    self.generate_content(layout)
                    time.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Dashboard stopped by user[/yellow]")


def start_dashboard(refresh_rate: float = 1.0):
    """
    Start the OverWatch dashboard.
    
    Args:
        refresh_rate: Refresh interval in seconds
    """
    dashboard = Dashboard(refresh_rate=refresh_rate)
    dashboard.run()
