#!/usr/bin/env python3
"""
Monitor system metrics and send email alerts when thresholds are exceeded.
"""

import time
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table

# Load environment
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overwatch.core import cpu, memory, disk, network
from overwatch.alerts.manager import AlertManager
from overwatch.alerts.email import EmailNotifier

console = Console()


def create_status_table(system_data, alert_history):
    """Create a status table showing current metrics and alert status."""
    
    table = Table(title="System Monitoring Status", show_header=True, expand=True)
    table.add_column("Metric", style="cyan", width=15)
    table.add_column("Current", style="white", width=15)
    table.add_column("Threshold", style="yellow", width=15)
    table.add_column("Status", style="green", width=15)
    
    # CPU
    cpu_data = system_data.get("cpu", {})
    cpu_usage = cpu_data.get("total", 0)
    cpu_threshold = 90  # Default, will be loaded from config
    cpu_status = "🔴 ALERT" if cpu_usage > cpu_threshold else "✅ OK"
    cpu_color = "red" if cpu_usage > cpu_threshold else "green"
    
    table.add_row(
        "CPU",
        f"{cpu_usage:.1f}%",
        f"{cpu_threshold}%",
        f"[{cpu_color}]{cpu_status}[/{cpu_color}]"
    )
    
    # Memory
    mem_data = system_data.get("memory", {}).get("ram", {})
    mem_usage = mem_data.get("percent", 0)
    mem_threshold = 80
    mem_status = "🔴 ALERT" if mem_usage > mem_threshold else "✅ OK"
    mem_color = "red" if mem_usage > mem_threshold else "green"
    
    table.add_row(
        "Memory",
        f"{mem_usage:.1f}%",
        f"{mem_threshold}%",
        f"[{mem_color}]{mem_status}[/{mem_color}]"
    )
    
    # Disk
    disk_data = system_data.get("disk", {})
    partitions = disk_data.get("partitions", [])
    if partitions:
        disk_usage = partitions[0].get("percent", 0)
        disk_threshold = 85
        disk_status = "🔴 ALERT" if disk_usage > disk_threshold else "✅ OK"
        disk_color = "red" if disk_usage > disk_threshold else "green"
        
        table.add_row(
            "Disk",
            f"{disk_usage:.1f}%",
            f"{disk_threshold}%",
            f"[{disk_color}]{disk_status}[/{disk_color}]"
        )
    
    return table


def main():
    """Main monitoring loop."""
    
    console.print(Panel.fit(
        "[bold cyan]OverWatch Alert Monitor[/bold cyan]\n"
        "Monitoring system metrics and sending email alerts",
        border_style="cyan"
    ))
    console.print()
    
    # Setup alert manager
    alert_manager = AlertManager()
    
    # Setup email notifier
    console.print("[yellow]Initializing email notifier...[/yellow]")
    email_notifier = EmailNotifier()
    
    if not email_notifier.enabled:
        console.print("[red]❌ Email notifier not configured![/red]")
        console.print("Set EMAIL_* environment variables in .env file")
        return
    
    # Test connection
    console.print("[yellow]Testing email connection...[/yellow]")
    if not email_notifier.test_connection():
        console.print("[red]❌ Email connection test failed![/red]")
        return
    
    console.print("[green]✓ Email notifier ready[/green]\n")
    
    # Register email handler
    alert_manager.register_handler(email_notifier.send_alert)
    
    console.print("[green]🔍 Monitoring started...[/green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
    
    try:
        while True:
            # Gather metrics
            system_data = {
                "cpu": cpu.get(),
                "memory": memory.get(),
                "disk": disk.get(),
            }
            
            # Check thresholds and send alerts
            alert_manager.check_all(system_data)
            
            # Display status
            table = create_status_table(system_data, alert_manager.get_alert_history())
            
            # Show recent alerts
            recent_alerts = alert_manager.get_alert_history(limit=3)
            if recent_alerts:
                console.print(table)
                console.print("\n[yellow]Recent Alerts:[/yellow]")
                for alert in recent_alerts:
                    console.print(f"  • [{alert['type']}] {alert['message']}")
                console.print()
            else:
                console.print(table)
                console.print("[green]\n✅ No alerts triggered[/green]\n")
            
            # Wait before next check
            time.sleep(5)
            console.clear()
            
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Monitoring stopped by user[/yellow]")
        console.print(f"[dim]Total alerts sent: {len(alert_manager.get_alert_history())}[/dim]")


if __name__ == "__main__":
    main()
