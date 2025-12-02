"""
System information utilities for OverWatch.
"""

import platform
import socket
import psutil
from datetime import datetime
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """
    Get comprehensive system information.
    
    Returns:
        Dict with system details
    """
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        # Format uptime
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        info = {
            "System": platform.system(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Architecture": " ".join(platform.architecture()),
            "Hostname": socket.gethostname(),
            "Python Version": platform.python_version(),
            "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Uptime": uptime_str,
        }
        
        # Add IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            info["IP Address"] = ip_address
        except Exception:
            info["IP Address"] = "N/A"
        
        return info
        
    except Exception as e:
        return {"error": str(e)}


def get_cpu_info() -> Dict[str, Any]:
    """
    Get detailed CPU information.
    
    Returns:
        Dict with CPU details
    """
    return {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Logical Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "N/A",
        "Min Frequency": f"{psutil.cpu_freq().min:.2f} MHz" if psutil.cpu_freq() else "N/A",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A",
    }


def get_memory_info() -> Dict[str, Any]:
    """
    Get detailed memory information.
    
    Returns:
        Dict with memory details
    """
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        "Total RAM": f"{vm.total / (1024**3):.2f} GB",
        "Available RAM": f"{vm.available / (1024**3):.2f} GB",
        "Used RAM": f"{vm.used / (1024**3):.2f} GB",
        "RAM Usage": f"{vm.percent}%",
        "Total Swap": f"{swap.total / (1024**3):.2f} GB",
        "Used Swap": f"{swap.used / (1024**3):.2f} GB",
        "Swap Usage": f"{swap.percent}%",
    }


def get_disk_info() -> Dict[str, Any]:
    """
    Get detailed disk information.
    
    Returns:
        Dict with disk details
    """
    partitions = psutil.disk_partitions()
    disk_info = {}
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.mountpoint] = {
                "Device": partition.device,
                "Filesystem": partition.fstype,
                "Total": f"{usage.total / (1024**3):.2f} GB",
                "Used": f"{usage.used / (1024**3):.2f} GB",
                "Free": f"{usage.free / (1024**3):.2f} GB",
                "Usage": f"{usage.percent}%",
            }
        except PermissionError:
            continue
    
    return disk_info


def bytes_to_human(bytes_value: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Human-readable string
    """
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} EB"
