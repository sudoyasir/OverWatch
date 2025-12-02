"""
Memory monitoring module for OverWatch.
Provides RAM and swap memory statistics using psutil.
"""

import psutil
from typing import Dict, Any


def get() -> Dict[str, Any]:
    """
    Get memory usage statistics.
    
    Returns:
        Dict containing:
            - ram: Virtual memory statistics
            - swap: Swap memory statistics
    """
    try:
        # Virtual memory (RAM)
        vm = psutil.virtual_memory()
        
        # Swap memory
        swap = psutil.swap_memory()
        
        return {
            "ram": {
                "total": vm.total,
                "available": vm.available,
                "used": vm.used,
                "free": vm.free,
                "percent": round(vm.percent, 2),
                "total_gb": round(vm.total / (1024**3), 2),
                "available_gb": round(vm.available / (1024**3), 2),
                "used_gb": round(vm.used / (1024**3), 2),
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": round(swap.percent, 2),
                "total_gb": round(swap.total / (1024**3), 2),
                "used_gb": round(swap.used / (1024**3), 2),
            },
        }
    except Exception as e:
        return {
            "ram": {
                "total": 0,
                "available": 0,
                "used": 0,
                "free": 0,
                "percent": 0.0,
                "total_gb": 0.0,
                "available_gb": 0.0,
                "used_gb": 0.0,
            },
            "swap": {
                "total": 0,
                "used": 0,
                "free": 0,
                "percent": 0.0,
                "total_gb": 0.0,
                "used_gb": 0.0,
            },
            "error": str(e),
        }


def bytes_to_human(bytes_value: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        bytes_value: Number of bytes
        
    Returns:
        Human-readable string (e.g., "1.5 GB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"
