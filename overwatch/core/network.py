"""
Network monitoring module for OverWatch.
Provides network I/O and connection statistics using psutil.
"""

import psutil
from typing import Dict, List, Any


def get() -> Dict[str, Any]:
    """
    Get network statistics.
    
    Returns:
        Dict containing:
            - io: Network I/O counters per interface
            - connections: Active network connections count
            - addresses: Network interface addresses
    """
    try:
        # Network I/O statistics per interface
        io_counters = psutil.net_io_counters(pernic=True)
        io_data = {}
        
        for interface, stats in io_counters.items():
            io_data[interface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errin": stats.errin,
                "errout": stats.errout,
                "dropin": stats.dropin,
                "dropout": stats.dropout,
                "mb_sent": round(stats.bytes_sent / (1024**2), 2),
                "mb_recv": round(stats.bytes_recv / (1024**2), 2),
            }
        
        # Total I/O (all interfaces combined)
        total_io = psutil.net_io_counters()
        total_data = {
            "bytes_sent": total_io.bytes_sent,
            "bytes_recv": total_io.bytes_recv,
            "packets_sent": total_io.packets_sent,
            "packets_recv": total_io.packets_recv,
            "mb_sent": round(total_io.bytes_sent / (1024**2), 2),
            "mb_recv": round(total_io.bytes_recv / (1024**2), 2),
        }
        
        # Network connections count by status
        try:
            connections = psutil.net_connections()
            connection_stats = {
                "total": len(connections),
                "established": len([c for c in connections if c.status == "ESTABLISHED"]),
                "listen": len([c for c in connections if c.status == "LISTEN"]),
            }
        except (PermissionError, psutil.AccessDenied):
            connection_stats = {"total": 0, "established": 0, "listen": 0}
        
        # Network interface addresses
        addresses = psutil.net_if_addrs()
        addr_data = {}
        for interface, addrs in addresses.items():
            addr_data[interface] = []
            for addr in addrs:
                addr_data[interface].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast,
                })
        
        return {
            "io_per_interface": io_data,
            "io_total": total_data,
            "connections": connection_stats,
            "addresses": addr_data,
        }
    except Exception as e:
        return {
            "io_per_interface": {},
            "io_total": {},
            "connections": {},
            "addresses": {},
            "error": str(e),
        }


def get_total_bandwidth() -> Dict[str, float]:
    """
    Get total bandwidth usage across all interfaces.
    
    Returns:
        Dict with sent and received MB
    """
    try:
        io = psutil.net_io_counters()
        return {
            "sent_mb": round(io.bytes_sent / (1024**2), 2),
            "recv_mb": round(io.bytes_recv / (1024**2), 2),
        }
    except Exception as e:
        return {"error": str(e)}
