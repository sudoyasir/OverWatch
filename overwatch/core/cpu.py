"""
CPU monitoring module for OverWatch.
Provides CPU usage statistics using psutil.
"""

import psutil
from typing import Dict, List, Any


def get() -> Dict[str, Any]:
    """
    Get CPU usage statistics.
    
    Returns:
        Dict containing:
            - total: Overall CPU usage percentage
            - per_core: List of per-core CPU usage percentages
            - count: Number of logical cores
            - freq_current: Current CPU frequency (MHz)
            - freq_min: Minimum CPU frequency (MHz)
            - freq_max: Maximum CPU frequency (MHz)
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        
        # CPU frequency (may not be available on all systems)
        freq = psutil.cpu_freq()
        freq_data = {
            "current": round(freq.current, 2) if freq else None,
            "min": round(freq.min, 2) if freq else None,
            "max": round(freq.max, 2) if freq else None,
        }
        
        # CPU stats
        stats = psutil.cpu_stats()
        
        return {
            "total": round(cpu_percent, 2),
            "per_core": [round(core, 2) for core in per_core],
            "count_logical": cpu_count,
            "count_physical": cpu_count_physical,
            "frequency": freq_data,
            "ctx_switches": stats.ctx_switches,
            "interrupts": stats.interrupts,
            "soft_interrupts": stats.soft_interrupts,
        }
    except Exception as e:
        return {
            "total": 0.0,
            "per_core": [],
            "count_logical": 0,
            "count_physical": 0,
            "frequency": {"current": None, "min": None, "max": None},
            "error": str(e),
        }


def get_load_average() -> List[float]:
    """
    Get system load average (1, 5, 15 minutes).
    Only available on Unix systems.
    
    Returns:
        List of three load average values
    """
    try:
        return list(psutil.getloadavg())
    except AttributeError:
        # Not available on Windows
        return [0.0, 0.0, 0.0]
