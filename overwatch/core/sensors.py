"""
Sensor monitoring module for OverWatch.
Provides temperature and fan sensor data using psutil.
"""

import psutil
from typing import Dict, List, Any


def get() -> Dict[str, Any]:
    """
    Get sensor data (temperatures, fans, battery).
    
    Returns:
        Dict containing:
            - temperatures: Temperature sensors data
            - fans: Fan speed data
            - battery: Battery information
    """
    data = {
        "temperatures": {},
        "fans": {},
        "battery": None,
    }
    
    # Temperature sensors
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                data["temperatures"][name] = []
                for entry in entries:
                    data["temperatures"][name].append({
                        "label": entry.label or name,
                        "current": round(entry.current, 1),
                        "high": round(entry.high, 1) if entry.high else None,
                        "critical": round(entry.critical, 1) if entry.critical else None,
                    })
    except AttributeError:
        # Not supported on this system
        data["temperatures"] = {"info": "Temperature sensors not available"}
    except Exception as e:
        data["temperatures"] = {"error": str(e)}
    
    # Fan sensors
    try:
        fans = psutil.sensors_fans()
        if fans:
            for name, entries in fans.items():
                data["fans"][name] = []
                for entry in entries:
                    data["fans"][name].append({
                        "label": entry.label or name,
                        "current": entry.current,
                    })
    except AttributeError:
        # Not supported on this system
        data["fans"] = {"info": "Fan sensors not available"}
    except Exception as e:
        data["fans"] = {"error": str(e)}
    
    # Battery
    try:
        battery = psutil.sensors_battery()
        if battery:
            data["battery"] = {
                "percent": round(battery.percent, 1),
                "secsleft": battery.secsleft,
                "power_plugged": battery.power_plugged,
            }
    except AttributeError:
        # Not supported on this system
        data["battery"] = {"info": "Battery sensor not available"}
    except Exception as e:
        data["battery"] = {"error": str(e)}
    
    return data


def get_temperatures() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get only temperature sensor data.
    
    Returns:
        Dict of temperature sensors
    """
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return {}
        
        result = {}
        for name, entries in temps.items():
            result[name] = []
            for entry in entries:
                result[name].append({
                    "label": entry.label or name,
                    "current": round(entry.current, 1),
                    "high": round(entry.high, 1) if entry.high else None,
                    "critical": round(entry.critical, 1) if entry.critical else None,
                })
        return result
    except AttributeError:
        return {"info": "Not supported on this system"}
    except Exception as e:
        return {"error": str(e)}
