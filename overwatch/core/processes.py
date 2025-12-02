"""
Process monitoring module for OverWatch.
Provides process information and statistics using psutil.
"""

import psutil
from typing import Dict, List, Any


def get(limit: int = 10, sort_by: str = "cpu") -> Dict[str, Any]:
    """
    Get process information sorted by resource usage.
    
    Args:
        limit: Maximum number of processes to return
        sort_by: Sort criteria ("cpu", "memory", "name")
        
    Returns:
        Dict containing:
            - processes: List of top processes
            - total_count: Total number of processes
    """
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']):
            try:
                pinfo = proc.info
                processes.append({
                    "pid": pinfo['pid'],
                    "name": pinfo['name'],
                    "username": pinfo['username'],
                    "cpu_percent": round(pinfo['cpu_percent'], 2),
                    "memory_percent": round(pinfo['memory_percent'], 2),
                    "status": pinfo['status'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort processes
        if sort_by == "cpu":
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        elif sort_by == "memory":
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        elif sort_by == "name":
            processes.sort(key=lambda x: x['name'])
        
        total_count = len(processes)
        
        return {
            "processes": processes[:limit],
            "total_count": total_count,
        }
    except Exception as e:
        return {
            "processes": [],
            "total_count": 0,
            "error": str(e),
        }


def get_process_by_pid(pid: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific process.
    
    Args:
        pid: Process ID
        
    Returns:
        Dict with detailed process information
    """
    try:
        proc = psutil.Process(pid)
        return {
            "pid": proc.pid,
            "name": proc.name(),
            "username": proc.username(),
            "status": proc.status(),
            "create_time": proc.create_time(),
            "cpu_percent": round(proc.cpu_percent(interval=0.1), 2),
            "memory_percent": round(proc.memory_percent(), 2),
            "memory_info": proc.memory_info()._asdict(),
            "num_threads": proc.num_threads(),
            "cmdline": proc.cmdline(),
        }
    except psutil.NoSuchProcess:
        return {"error": f"Process {pid} not found"}
    except psutil.AccessDenied:
        return {"error": f"Access denied to process {pid}"}
    except Exception as e:
        return {"error": str(e)}


def get_process_count() -> Dict[str, int]:
    """
    Get process count by status.
    
    Returns:
        Dict with process counts by status
    """
    try:
        counts = {
            "total": 0,
            "running": 0,
            "sleeping": 0,
            "stopped": 0,
            "zombie": 0,
        }
        
        for proc in psutil.process_iter(['status']):
            try:
                counts["total"] += 1
                status = proc.info['status']
                if status in counts:
                    counts[status] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return counts
    except Exception as e:
        return {"error": str(e)}
