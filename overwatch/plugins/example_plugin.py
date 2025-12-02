"""
Example plugin for OverWatch.
This demonstrates how to create a custom plugin.

Every plugin must expose a run() function that returns a dictionary with:
- name: Plugin name
- data: Plugin output data
"""

from typing import Dict, Any
import platform


def run() -> Dict[str, Any]:
    """
    Run the example plugin.
    
    Returns:
        Dict with plugin name and data
    """
    # Example: Get system information
    system_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    
    return {
        "name": "Example System Info Plugin",
        "data": system_info,
        "status": "success",
    }


# Optional: Plugin metadata
PLUGIN_INFO = {
    "name": "Example Plugin",
    "version": "1.0.0",
    "description": "An example plugin that shows system information",
    "author": "OverWatch Team",
}
