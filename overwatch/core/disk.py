"""
Disk monitoring module for OverWatch.
Provides disk usage and I/O statistics using psutil.
"""

import psutil
from typing import Dict, List, Any


def get() -> Dict[str, Any]:
    """
    Get disk usage and I/O statistics.
    
    Returns:
        Dict containing:
            - partitions: List of disk partitions with usage info
            - io: Disk I/O statistics
    """
    try:
        # Get all disk partitions
        partitions_data = []
        partitions = psutil.disk_partitions(all=False)
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions_data.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": round(usage.percent, 2),
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                })
            except (PermissionError, OSError):
                # Skip partitions we can't access
                continue
        
        # Disk I/O statistics
        io = psutil.disk_io_counters()
        io_data = {
            "read_count": io.read_count,
            "write_count": io.write_count,
            "read_bytes": io.read_bytes,
            "write_bytes": io.write_bytes,
            "read_time": io.read_time,
            "write_time": io.write_time,
            "read_mb": round(io.read_bytes / (1024**2), 2),
            "write_mb": round(io.write_bytes / (1024**2), 2),
        } if io else {}
        
        return {
            "partitions": partitions_data,
            "io": io_data,
        }
    except Exception as e:
        return {
            "partitions": [],
            "io": {},
            "error": str(e),
        }


def get_partition_usage(mountpoint: str = "/") -> Dict[str, Any]:
    """
    Get usage statistics for a specific partition.
    
    Args:
        mountpoint: Mount point path (default: "/")
        
    Returns:
        Dict with partition usage data
    """
    try:
        usage = psutil.disk_usage(mountpoint)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": round(usage.percent, 2),
        }
    except Exception as e:
        return {"error": str(e)}
