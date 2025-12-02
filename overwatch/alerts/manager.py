"""
Alert manager for OverWatch.
Monitors system metrics and triggers notifications when thresholds are exceeded.
"""

import json
import os
from typing import Dict, Any, List, Callable
from datetime import datetime, timedelta
from pathlib import Path


class AlertManager:
    """Manages alerts and notifications for system metrics."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the alert manager.
        
        Args:
            config_path: Path to thresholds.json config file
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                "thresholds.json"
            )
        
        self.config_path = config_path
        self.thresholds = self.load_thresholds()
        self.alert_handlers: List[Callable] = []
        self.alert_history: List[Dict[str, Any]] = []
        self.cooldown_period = timedelta(minutes=5)
        self.last_alerts: Dict[str, datetime] = {}
    
    def load_thresholds(self) -> Dict[str, Any]:
        """
        Load threshold configuration from JSON file.
        
        Returns:
            Dict with threshold configurations
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default thresholds if file not found
            return {
                "cpu": {"threshold": 90, "enabled": True},
                "memory": {"threshold": 80, "enabled": True},
                "disk": {"threshold": 85, "enabled": True},
                "temperature": {"threshold": 80, "enabled": False},
            }
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.config_path}")
            return {}
    
    def save_thresholds(self):
        """Save current thresholds to JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.thresholds, f, indent=2)
        except Exception as e:
            print(f"Error saving thresholds: {e}")
    
    def register_handler(self, handler: Callable):
        """
        Register an alert handler function.
        
        Args:
            handler: Callable that accepts (alert_type, message, value)
        """
        self.alert_handlers.append(handler)
    
    def check_cpu(self, cpu_data: Dict[str, Any]):
        """
        Check CPU usage against threshold.
        
        Args:
            cpu_data: CPU data from core.cpu.get()
        """
        if not self.thresholds.get("cpu", {}).get("enabled", False):
            return
        
        threshold = self.thresholds["cpu"]["threshold"]
        current = cpu_data.get("total", 0)
        
        if current > threshold:
            self._trigger_alert(
                "cpu",
                f"CPU usage is {current}% (threshold: {threshold}%)",
                current
            )
    
    def check_memory(self, memory_data: Dict[str, Any]):
        """
        Check memory usage against threshold.
        
        Args:
            memory_data: Memory data from core.memory.get()
        """
        if not self.thresholds.get("memory", {}).get("enabled", False):
            return
        
        threshold = self.thresholds["memory"]["threshold"]
        current = memory_data.get("ram", {}).get("percent", 0)
        
        if current > threshold:
            self._trigger_alert(
                "memory",
                f"Memory usage is {current}% (threshold: {threshold}%)",
                current
            )
    
    def check_disk(self, disk_data: Dict[str, Any]):
        """
        Check disk usage against threshold.
        
        Args:
            disk_data: Disk data from core.disk.get()
        """
        if not self.thresholds.get("disk", {}).get("enabled", False):
            return
        
        threshold = self.thresholds["disk"]["threshold"]
        
        for partition in disk_data.get("partitions", []):
            current = partition.get("percent", 0)
            mountpoint = partition.get("mountpoint", "")
            
            if current > threshold:
                self._trigger_alert(
                    "disk",
                    f"Disk usage on {mountpoint} is {current}% (threshold: {threshold}%)",
                    current
                )
    
    def check_temperature(self, sensor_data: Dict[str, Any]):
        """
        Check temperature against threshold.
        
        Args:
            sensor_data: Sensor data from core.sensors.get()
        """
        if not self.thresholds.get("temperature", {}).get("enabled", False):
            return
        
        threshold = self.thresholds["temperature"]["threshold"]
        temps = sensor_data.get("temperatures", {})
        
        for sensor_name, entries in temps.items():
            if isinstance(entries, list):
                for entry in entries:
                    current = entry.get("current", 0)
                    label = entry.get("label", sensor_name)
                    
                    if current > threshold:
                        self._trigger_alert(
                            "temperature",
                            f"Temperature {label} is {current}°C (threshold: {threshold}°C)",
                            current
                        )
    
    def _trigger_alert(self, alert_type: str, message: str, value: float):
        """
        Trigger an alert if not in cooldown period.
        
        Args:
            alert_type: Type of alert (cpu, memory, disk, etc.)
            message: Alert message
            value: Current value that triggered the alert
        """
        now = datetime.now()
        
        # Check cooldown
        if alert_type in self.last_alerts:
            time_since_last = now - self.last_alerts[alert_type]
            if time_since_last < self.cooldown_period:
                return  # Still in cooldown
        
        # Update last alert time
        self.last_alerts[alert_type] = now
        
        # Record in history
        alert_record = {
            "type": alert_type,
            "message": message,
            "value": value,
            "timestamp": now.isoformat(),
        }
        self.alert_history.append(alert_record)
        
        # Call all registered handlers
        for handler in self.alert_handlers:
            try:
                handler(alert_type, message, value)
            except Exception as e:
                print(f"Error in alert handler: {e}")
    
    def check_all(self, system_data: Dict[str, Any]):
        """
        Check all metrics against thresholds.
        
        Args:
            system_data: Dict with all system metrics
        """
        if "cpu" in system_data:
            self.check_cpu(system_data["cpu"])
        
        if "memory" in system_data:
            self.check_memory(system_data["memory"])
        
        if "disk" in system_data:
            self.check_disk(system_data["disk"])
        
        if "sensors" in system_data:
            self.check_temperature(system_data["sensors"])
    
    def get_alert_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent alert history.
        
        Args:
            limit: Maximum number of alerts to return
            
        Returns:
            List of recent alerts
        """
        return self.alert_history[-limit:]
    
    def clear_history(self):
        """Clear alert history."""
        self.alert_history = []
        self.last_alerts = {}
