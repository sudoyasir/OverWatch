"""
Dashboard UI for OverWatch.
Main terminal interface using Rich.
"""

import time
import os
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from datetime import datetime
from dotenv import load_dotenv

from overwatch.core import cpu, memory, disk, network, processes, sensors
from overwatch.alerts.manager import AlertManager
from overwatch.alerts.email import EmailNotifier
from overwatch.ui.components import (
    cpu_panel,
    memory_panel,
    disk_panel,
    network_panel,
    process_panel,
)

# Load environment variables
load_dotenv()


class Dashboard:
    """Main dashboard class for OverWatch."""
    
    def __init__(self, refresh_rate: float = 1.0, enable_alerts: bool = True):
        """
        Initialize the dashboard.
        
        Args:
            refresh_rate: Refresh interval in seconds
            enable_alerts: Enable email alerts
        """
        self.console = Console()
        self.refresh_rate = refresh_rate
        self.plugin_data = []
        self.enable_alerts = enable_alerts
        
        # Initialize alert system
        if enable_alerts:
            self.alert_manager = AlertManager()
            self.email_notifier = EmailNotifier()
            if self.email_notifier.enabled:
                self.alert_manager.register_handler(self.email_notifier.send_alert)
        else:
            self.alert_manager = None
            self.email_notifier = None
    
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
        
        # Split body into left, middle, and right
        layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="middle", ratio=2),
            Layout(name="right", ratio=1),
        )
        
        # Split left into top and bottom
        layout["left"].split_column(
            Layout(name="system", ratio=2),
            Layout(name="disk", ratio=1),
        )
        
        # Middle column for processes and alerts
        layout["middle"].split_column(
            Layout(name="processes", ratio=3),
            Layout(name="alerts", ratio=1),
        )
        
        # Right side for network and email status
        layout["right"].split_column(
            Layout(name="network"),
            Layout(name="email_status", size=12),
        )
        
        # Split system into CPU and Memory
        layout["system"].split_row(
            Layout(name="cpu"),
            Layout(name="memory"),
        )
        
        return layout
    
    def generate_header(self) -> Panel:
        """
        Generate the dashboard header.
        
        Returns:
            Rich Panel for header
        """
        title = Text()
        title.append("OverWatch", style="bold bright_magenta")
        title.append(" - Advanced System Monitor", style="bright_white")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        grid = Table.grid(expand=True)
        grid.add_column(justify="left")
        grid.add_column(justify="right")
        grid.add_row(title, f"[bright_yellow]{timestamp}[/bright_yellow]")
        
        return Panel(grid, style="bright_white on #5f00af", border_style="bright_magenta")
    
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
        
        # Check alerts and update panels
        if self.enable_alerts and self.alert_manager:
            system_data = {
                "cpu": cpu_data,
                "memory": memory_data,
                "disk": disk_data,
            }
            self.alert_manager.check_all(system_data)
            layout["alerts"].update(self.generate_alerts_panel())
            layout["email_status"].update(self.generate_email_status_panel())
        else:
            layout["alerts"].update(Panel("[dim]Alerts disabled[/dim]", title="🔔 Alerts", border_style="dim"))
            layout["email_status"].update(Panel("[dim]Email disabled[/dim]", title="📧 Email", border_style="dim"))
    
    def generate_alerts_panel(self) -> Panel:
        """
        Generate the alerts status panel.
        
        Returns:
            Rich Panel for alerts
        """
        if not self.alert_manager:
            return Panel("[dim]No alert manager[/dim]", title="🔔 Alerts", border_style="dim")
        
        # Get alert history
        recent_alerts = self.alert_manager.get_alert_history(limit=5)
        
        if not recent_alerts:
            return Panel(
                "[bright_green]✓ No alerts triggered[/bright_green]",
                title="🔔 Alert Status",
                border_style="bright_green"
            )
        
        # Create alerts table
        table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
        table.add_column("Time", style="dim", width=8)
        table.add_column("Alert", style="bright_yellow")
        
        for alert in recent_alerts[-3:]:  # Show last 3 alerts
            timestamp = alert.get("timestamp", "")
            if timestamp:
                time_str = datetime.fromisoformat(timestamp).strftime("%H:%M:%S")
            else:
                time_str = "Unknown"
            
            alert_type = alert.get("type", "").upper()
            value = alert.get("value", 0)
            
            # Color based on alert type
            if alert_type == "CPU":
                color = "bright_red"
                icon = "🔥"
            elif alert_type == "MEMORY":
                color = "bright_yellow"
                icon = "💾"
            elif alert_type == "DISK":
                color = "bright_magenta"
                icon = "💿"
            else:
                color = "white"
                icon = "⚠️"
            
            table.add_row(
                time_str,
                f"[{color}]{icon} {alert_type}: {value:.1f}%[/{color}]"
            )
        
        total_alerts = len(recent_alerts)
        return Panel(
            table,
            title=f"🔔 Recent Alerts (Total: {total_alerts})",
            border_style="bright_yellow"
        )
    
    def generate_email_status_panel(self) -> Panel:
        """
        Generate the email status panel.
        
        Returns:
            Rich Panel for email status
        """
        if not self.email_notifier:
            return Panel("[dim]Email not configured[/dim]", title="📧 Email", border_style="dim")
        
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Label", style="bright_cyan")
        table.add_column("Value", style="bright_white")
        
        # SMTP status
        if self.email_notifier.enabled:
            table.add_row("Status", "[bright_green]✓ Enabled[/bright_green]")
            table.add_row("Server", f"{self.email_notifier.smtp_server}:{self.email_notifier.smtp_port}")
            table.add_row("From", self.email_notifier.from_email)
            table.add_row("To", self.email_notifier.to_email)
            
            # Count sent emails from alert history
            if self.alert_manager:
                sent_count = len(self.alert_manager.get_alert_history())
                table.add_row("Sent", f"[bright_yellow]{sent_count}[/bright_yellow]")
            
            border_style = "bright_green"
        else:
            table.add_row("Status", "[bright_red]✗ Disabled[/bright_red]")
            table.add_row("Info", "[dim]Configure .env[/dim]")
            border_style = "red"
        
        return Panel(table, title="📧 Email Alerts", border_style=border_style)
    
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


def start_dashboard(refresh_rate: float = 1.0, enable_alerts: bool = True):
    """
    Start the OverWatch dashboard.
    
    Args:
        refresh_rate: Refresh interval in seconds
        enable_alerts: Enable email alerts monitoring
    """
    dashboard = Dashboard(refresh_rate=refresh_rate, enable_alerts=enable_alerts)
    dashboard.run()
