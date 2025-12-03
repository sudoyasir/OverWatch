#!/usr/bin/env python3
"""
Email configuration tester for OverWatch.
Tests email notifications and provides detailed error messages.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overwatch.alerts.email import EmailNotifier
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def test_email_config():
    """Test email configuration and send a test email."""
    
    console.print(Panel.fit(
        "[bold cyan]OverWatch Email Configuration Test[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    # Show configuration
    config_table = Table(title="Email Configuration", show_header=True)
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="white")
    
    smtp_server = os.getenv("EMAIL_SMTP_SERVER")
    smtp_port = os.getenv("EMAIL_SMTP_PORT", "587")
    smtp_username = os.getenv("EMAIL_SMTP_USERNAME")
    smtp_password = os.getenv("EMAIL_SMTP_PASSWORD")
    from_email = os.getenv("EMAIL_FROM")
    to_email = os.getenv("EMAIL_TO")
    
    config_table.add_row("SMTP Server", smtp_server or "[red]NOT SET[/red]")
    config_table.add_row("SMTP Port", smtp_port)
    config_table.add_row("SMTP Username", smtp_username or "[red]NOT SET[/red]")
    config_table.add_row("SMTP Password", "***" + smtp_password[-4:] if smtp_password else "[red]NOT SET[/red]")
    config_table.add_row("From Email", from_email or "[red]NOT SET[/red]")
    config_table.add_row("To Email", to_email or "[red]NOT SET[/red]")
    
    console.print(config_table)
    console.print()
    
    # Check if all required settings are present
    if not all([smtp_server, smtp_username, smtp_password, from_email, to_email]):
        console.print("[red]❌ Missing required configuration![/red]")
        console.print("\nPlease set the following environment variables:")
        console.print("  - EMAIL_SMTP_SERVER")
        console.print("  - EMAIL_SMTP_USERNAME")
        console.print("  - EMAIL_SMTP_PASSWORD")
        console.print("  - EMAIL_FROM")
        console.print("  - EMAIL_TO")
        return False
    
    # Initialize notifier
    console.print("[yellow]Initializing email notifier...[/yellow]")
    notifier = EmailNotifier()
    
    if not notifier.enabled:
        console.print("[red]❌ Email notifier not enabled![/red]")
        return False
    
    console.print("[green]✓ Email notifier initialized[/green]\n")
    
    # Test connection
    console.print("[yellow]Testing SMTP connection...[/yellow]")
    
    try:
        import smtplib
        with smtplib.SMTP(smtp_server, int(smtp_port), timeout=10) as server:
            server.set_debuglevel(0)  # Disable debug output
            console.print(f"[green]✓ Connected to {smtp_server}:{smtp_port}[/green]")
            
            console.print("[yellow]Starting TLS...[/yellow]")
            server.starttls()
            console.print("[green]✓ TLS started[/green]")
            
            console.print("[yellow]Authenticating...[/yellow]")
            server.login(smtp_username, smtp_password)
            console.print("[green]✓ Authentication successful[/green]\n")
            
    except smtplib.SMTPAuthenticationError as e:
        console.print(f"[red]❌ Authentication failed: {e}[/red]")
        console.print("\n[yellow]Troubleshooting tips:[/yellow]")
        console.print("  1. Check your email and password are correct")
        console.print("  2. If using Gmail, enable 2-factor authentication")
        console.print("  3. Generate an App Password: https://myaccount.google.com/apppasswords")
        console.print("  4. Use the App Password instead of your regular password")
        return False
    except smtplib.SMTPException as e:
        console.print(f"[red]❌ SMTP error: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Connection error: {e}[/red]")
        console.print("\n[yellow]Troubleshooting tips:[/yellow]")
        console.print("  1. Check your internet connection")
        console.print("  2. Verify SMTP server address and port")
        console.print("  3. Check firewall settings")
        return False
    
    # Send test email
    console.print("[yellow]Sending test email...[/yellow]")
    try:
        notifier.send_alert(
            "test",
            "This is a test alert from OverWatch. If you received this, email notifications are working!",
            0.0
        )
        console.print(f"[green]✓ Test email sent to {to_email}[/green]\n")
        
        console.print(Panel.fit(
            "[bold green]✓ Email configuration is working correctly![/bold green]\n"
            f"Check your inbox at {to_email}",
            border_style="green"
        ))
        return True
        
    except Exception as e:
        console.print(f"[red]❌ Failed to send test email: {e}[/red]")
        return False


if __name__ == "__main__":
    success = test_email_config()
    sys.exit(0 if success else 1)
