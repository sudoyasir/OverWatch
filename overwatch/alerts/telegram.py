"""
Telegram notification handler for OverWatch alerts.
"""

import os
from typing import Optional
import requests


class TelegramNotifier:
    """Send alerts via Telegram bot."""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token (or set TELEGRAM_BOT_TOKEN env var)
            chat_id: Telegram chat ID (or set TELEGRAM_CHAT_ID env var)
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.bot_token and self.chat_id)
        
        if not self.enabled:
            print("Warning: Telegram notifier not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
    
    def send_alert(self, alert_type: str, message: str, value: float):
        """
        Send an alert via Telegram.
        
        Args:
            alert_type: Type of alert
            message: Alert message
            value: Current value
        """
        if not self.enabled:
            return
        
        # Format message with emoji
        emoji = self._get_emoji(alert_type)
        formatted_message = f"{emoji} *OverWatch Alert*\n\n"
        formatted_message += f"*Type:* {alert_type.upper()}\n"
        formatted_message += f"*Message:* {message}\n"
        formatted_message += f"*Value:* {value}"
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": formatted_message,
                "parse_mode": "Markdown",
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
        except requests.RequestException as e:
            print(f"Error sending Telegram notification: {e}")
    
    def _get_emoji(self, alert_type: str) -> str:
        """
        Get emoji for alert type.
        
        Args:
            alert_type: Type of alert
            
        Returns:
            Emoji string
        """
        emojis = {
            "cpu": "🔥",
            "memory": "💾",
            "disk": "💿",
            "temperature": "🌡️",
            "network": "🌐",
        }
        return emojis.get(alert_type, "⚠️")
    
    def test_connection(self) -> bool:
        """
        Test Telegram connection.
        
        Returns:
            True if connection successful
        """
        if not self.enabled:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
