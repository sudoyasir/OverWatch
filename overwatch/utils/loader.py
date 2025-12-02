"""
Plugin loader for OverWatch.
Automatically discovers and loads plugins from the plugins directory.
"""

import os
import importlib.util
from typing import List, Dict, Any
from pathlib import Path


class PluginLoader:
    """Loads and manages OverWatch plugins."""
    
    def __init__(self, plugin_dir: str = None):
        """
        Initialize the plugin loader.
        
        Args:
            plugin_dir: Path to plugins directory
        """
        if plugin_dir is None:
            # Default to plugins directory in package
            plugin_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "plugins"
            )
        
        self.plugin_dir = plugin_dir
        self.plugins = {}
    
    def discover_plugins(self) -> List[str]:
        """
        Discover all Python files in the plugins directory.
        
        Returns:
            List of plugin file paths
        """
        if not os.path.exists(self.plugin_dir):
            return []
        
        plugin_files = []
        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py") and not file.startswith("__"):
                plugin_files.append(os.path.join(self.plugin_dir, file))
        
        return plugin_files
    
    def load_plugin(self, plugin_path: str) -> Dict[str, Any]:
        """
        Load a single plugin from file.
        
        Args:
            plugin_path: Path to plugin file
            
        Returns:
            Dict with plugin module and metadata
        """
        try:
            # Get plugin name from filename
            plugin_name = Path(plugin_path).stem
            
            # Load module dynamically
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                return {"error": f"Failed to load spec for {plugin_name}"}
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if plugin has required run() function
            if not hasattr(module, "run"):
                return {"error": f"Plugin {plugin_name} missing run() function"}
            
            # Get plugin metadata if available
            metadata = getattr(module, "PLUGIN_INFO", {
                "name": plugin_name,
                "version": "unknown",
                "description": "No description provided",
            })
            
            return {
                "name": plugin_name,
                "module": module,
                "metadata": metadata,
                "path": plugin_path,
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def load_all_plugins(self):
        """Load all discovered plugins."""
        plugin_files = self.discover_plugins()
        
        for plugin_path in plugin_files:
            result = self.load_plugin(plugin_path)
            if "error" not in result:
                plugin_name = result["name"]
                self.plugins[plugin_name] = result
            else:
                print(f"Warning: Failed to load plugin {plugin_path}: {result['error']}")
    
    def run_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """
        Run a specific plugin.
        
        Args:
            plugin_name: Name of the plugin to run
            
        Returns:
            Plugin execution result
        """
        if plugin_name not in self.plugins:
            return {"error": f"Plugin '{plugin_name}' not found"}
        
        try:
            plugin = self.plugins[plugin_name]
            module = plugin["module"]
            return module.run()
        except Exception as e:
            return {"error": str(e)}
    
    def run_all_plugins(self) -> Dict[str, Any]:
        """
        Run all loaded plugins.
        
        Returns:
            Dict with results from all plugins
        """
        results = {}
        for plugin_name in self.plugins:
            results[plugin_name] = self.run_plugin(plugin_name)
        return results
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        Get list of all loaded plugins with metadata.
        
        Returns:
            List of plugin information
        """
        plugin_list = []
        for plugin_name, plugin in self.plugins.items():
            metadata = plugin.get("metadata", {})
            plugin_list.append({
                "name": metadata.get("name", plugin_name),
                "version": metadata.get("version", "unknown"),
                "description": metadata.get("description", "No description"),
                "author": metadata.get("author", "Unknown"),
            })
        return plugin_list
    
    def get_plugin(self, plugin_name: str) -> Dict[str, Any]:
        """
        Get information about a specific plugin.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin information
        """
        return self.plugins.get(plugin_name, {"error": "Plugin not found"})
